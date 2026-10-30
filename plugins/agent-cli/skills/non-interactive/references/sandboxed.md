# Driving these CLIs from inside an outer sandbox

> **Opt-in, like `opencode.md`.** `../SKILL.md` documents Claude Code and Codex as a caller
> meets them on a bare machine. Everything here needs a second confinement layer around the
> process — a bubblewrap or srt carve-out, a container, a CI runner with its own mount namespace — and
> a reader who is not doing that cannot reach any of it. Open this file when you are dispatching
> one of these CLIs into a sandbox you built.

**Verified 2026-08-28** — codex-cli 0.150.1, bubblewrap 0.11.2, Linux 6.8; **re-verified
2026-10-19** on codex-cli 0.163.0 and bubblewrap 0.12.0, every probe below as expected. Both
traps below were first observed 2026-08-27 by a worker driving Codex under bwrap, and
re-measured here first-hand before being written down. **Measured 2026-10-29 under srt** —
codex-cli 0.165.0, srt (`@anthropic-ai/sandbox-runtime`) 0.0.81, Ubuntu with
`kernel.apparmor_restrict_unprivileged_userns=1`; both traps reproduced, asserted on files.
The srt results and their limits are in *Under srt* below.

## The mechanism, first — it explains both traps

**Bubblewrap cannot nest on this machine, and Codex's Linux sandbox *is* bubblewrap.** That
single fact produces both failures below. It needs no CLI to demonstrate:

```sh
bwrap --dev-bind / / -- echo ok                                  # single: ok
bwrap --dev-bind / / --tmpfs /tmp -- bwrap --dev-bind / / -- echo ok   # nested: fails
```

The inner call reports `bwrap: No permissions to create a new namespace, likely because the
kernel does not allow non-privileged user namespaces… this can be enabled with 'sysctl
kernel.unprivileged_userns_clone=1'`.

**That suggestion is a red herring here**, and checking it is what pins the real cause:

| sysctl | value |
|---|---|
| `kernel.unprivileged_userns_clone` | `1` — already enabled |
| `user.max_user_namespaces` | `2060410` — not exhausted |
| `kernel.apparmor_restrict_unprivileged_userns` | **`1` — this is the one** |

So it is AppArmor's restriction on unprivileged user namespaces (Ubuntu's default), not the
kernel toggle bwrap names. **This is environment-dependent, not a property of Codex**: on a host
without that AppArmor policy the nesting may well work, and nothing here has been tested there.

## Trap: `-o` writes into whatever `/tmp` the process can see

Codex resolves `-o` inside its own mount namespace. Give it an absolute path under a `/tmp` the
sandbox replaced with a tmpfs and the caller gets nothing back, **with exit 0**:

```
[inside]  /tmp/reportdir exists?  NO          ← host has it; the tmpfs does not
[inside]  codex exit=0
[inside]  report file: ABSENT
[host]    /tmp/reportdir/report.txt: ABSENT
```

Codex does say so, but not where a driver is looking:

```
Failed to write last message file "/tmp/reportdir/report.txt": No such file or directory (os error 2)
```

That line goes to **stderr**, not stdout, and it is **not the last line** — `tokens used` and a
count follow it. A driver that reads the report path and the exit code sees an absent file and a
clean exit.

**`-o` must name a path the sandboxed process shares with the caller** — under the bound project
directory, or an explicitly bound scratch path. Redirecting the run's stdout on the caller's side
is unaffected: that redirection happens in the caller's namespace, not the child's.

## Trap: Codex's own sandbox does not nest — and the run still exits 0

Under `--sandbox workspace-write` inside a bwrap carve-out, every write fails. Same carve-out,
same prompt, same model, only the sandbox flag differs:

| `--sandbox` | exit | `shell.txt` | `target.txt` | final message |
|---|---|---|---|---|
| `workspace-write` | **0** | absent | `original` (unchanged) | **varies — see below** |
| `danger-full-access` | 0 | `SHELL_RAN` | `EDITED` | `DONE` |

**The exit code is the constant; the message is not.** Across five runs of the failing case the
model answered `DONE` once — claiming work it had not done — and named the failure the other
four times (`Unable to edit: the filesystem sandbox failed to start (bwrap namespace…)`,
`Blocked: filesystem sandbox failed.`). So the silent case is real but is not the common one,
and **nothing about the outcome is legible from the exit code, which is 0 either way.** Assert
on the file, never on the answer.

The failure is legible on stderr if you look for it —

```
ERROR codex_core::tools::router: error=apply_patch verification failed: Failed to read file to
update …/target.txt: fs sandbox helper failed with status exit status: 1: bwrap: No permissions
to create a new namespace…
```

— and when the model does claim `DONE`, that claim is exactly what `-o` hands a driver. There is
also an earlier signal, printed at startup before any turn:

```
warning: Codex's Linux sandbox uses bubblewrap and needs access to create user namespaces.
```

Treat that warning as fatal for `workspace-write` when it appears; it is the cheapest place to
catch this. A different startup warning preceded the srt failure; see *Under srt* below.

**So when an outer sandbox already confines the process, the inner one is not a second layer but
a failure mode.** Turning it off with `--sandbox danger-full-access` is not a loosening wherever
the outer carve-out is narrower than `workspace-write` would have granted on a bare machine —
`workspace-write` writes to `[workdir, /tmp, $TMPDIR]`, which a carve-out binding only the project
directory already beats. `codex exec --help` anticipates the situation for the neighbouring flag,
documenting `--dangerously-bypass-approvals-and-sandbox` as *"Intended solely for running in
environments that are externally sandboxed"* — but that the nesting fails **this way**, silently
and with a success message, is written down nowhere.

## Under srt

**Both traps reproduced 2026-10-29** with the versions and host policy stamped above.
The project `W` and throwaway home `H` were both under `/var/tmp`. `CODEX_HOME=$H/.codex`
held only a symlink to `~/.codex/auth.json`. Use `opencode.md`'s *The confined author lane*
and *Traps under srt* for the outer lane's setup and traps; in particular, its trap 3 explains
the `network.allowAllUnixSockets=true` setting used here.

For Codex, the settings were this shape. Replace `<repo>`, `<home>`, `<srt-dir>` and `<uid>`
as in that lane, and keep the settings outside the writable project:

```json
{"network":{"allowedDomains":["chatgpt.com"],"deniedDomains":[],"allowAllUnixSockets":true},
 "filesystem":{"denyRead":["~","/run/user/<uid>"],
   "allowRead":["~/.codex/packages","~/.codex/auth.json","<srt-dir>"],
   "allowWrite":["<repo>","<home>"],"denyWrite":["<repo>/.git"]}}
```

Use the Codex binary's real path under `~/.codex/packages` for `<codex>`:
`denyRead` hides `~/.local/bin`. The measured command was:

```sh
cd "$W" && srt --settings /path/to/s.json -- env HOME="$H" CODEX_HOME="$H/.codex" PATH=/usr/bin:/bin \
  <codex> exec - --skip-git-repo-check --model <model> --sandbox <mode> \
  -c approval_policy=never -o "$W/report.txt" < prompt
```

The prompt asked for `target.txt` to be replaced with `EDITED` via shell, then a write to a
file in another `/var/tmp` directory, and a reply of `DONE` or `BLOCKED`.

| `--sandbox` | runs | exit | `target.txt` | outside write | `-o` report |
|---|---|---|---|---|---|
| `workspace-write` | 3 | **0** each | `original` | not attempted (shell never started) | `BLOCKED: … namespace … ENOSPC` all 3 |
| `danger-full-access` | 1 | 0 | `EDITED` | `Read-only file system` (srt blocked it) | `DONE` |

The failing runs' stderr held:

```
bwrap: Creating new namespace failed: nesting depth or /proc/sys/user/max_*_namespaces exceeded (ENOSPC)
```

The startup warning was different from the one in the second trap:

```
warning: Codex could not find bubblewrap on PATH. … Codex will use the bundled bubblewrap in the meantime.
```

`/usr/bin` was on `PATH`. That warning was followed by ENOSPC; checking only for the earlier
warning misses this failure. The model answered `BLOCKED` in all three runs here, versus
`DONE` in one of five in the 2026-08-28 bwrap measurement. Three runs do not retire the silent
case: **assert on the file**. **`danger-full-access` is the working setting inside this srt
lane; srt is what confines it.**

The `-o` trap also reproduced with `danger-full-access`: a report path
`/var/tmp/<dir>/r.txt` outside `allowWrite`, whose directory existed on the host, gave exit 0,
target `EDITED`, report **ABSENT**. Stderr held:

```
Failed to write last message file "…/r.txt": Read-only file system (os error 30)
```

It was not the last line: `tokens used` and a count followed. Under srt a host path outside
`allowWrite` is still there but read-only, so this is `Read-only file system`, rather than the bwrap tmpfs
case's `No such file or directory`.

Read-only auth through the single-file symlink was enough for these runs. **Token refresh,
which writes `auth.json`, was not exercised.**

**`chatgpt.com` alone is enough for a ChatGPT sign-in.** The runs in the table allowed
`chatgpt.com`, `*.chatgpt.com`, `openai.com` and `*.openai.com`; a later `danger-full-access` run
the same day with only `chatgpt.com` exited 0, wrote `EDITED`, reported `DONE`, and logged no
connection error. The control, `allowedDomains: []`, is loud: exit 1, target unchanged, no
report, and stderr holding `failed to refresh available models: Connection failed`. Sign-in with
an API key was not measured and likely needs another domain.

An earlier check on **2026-10-28**, with codex-cli 0.165.0 and no model turn, ran
`codex sandbox` inside the same srt lane: read-only and workspace-write gave the same ENOSPC;
danger-full-access wrote the project and srt refused the outside write.

## Verifying this file

The mechanism check costs nothing and settles most of it. The two CLI probes cost one turn each.
The additional srt pair costs two turns.

```sh
# 1. does bwrap nest here at all? (no CLI, no turn)
bwrap --dev-bind / / -- echo single-ok
bwrap --dev-bind / / --tmpfs /tmp -- bwrap --dev-bind / / -- echo nested-ok
sysctl kernel.unprivileged_userns_clone user.max_user_namespaces \
       kernel.apparmor_restrict_unprivileged_userns
# expected: single ok, nested fails, and apparmor_restrict_unprivileged_userns=1 is why.
# If nesting SUCCEEDS here, the second trap below may not reproduce — say so rather than
# deleting it, since the trap is about environments where nesting is blocked.

# 2. -o into a path the sandbox does not share
mkdir -p /tmp/reportdir && rm -f /tmp/reportdir/report.txt
W=$(mktemp -d); bwrap --dev-bind / / --tmpfs /tmp --bind "$W" "$W" --chdir "$W" -- sh -c '
  echo "Reply with exactly: OK" | codex exec - --skip-git-repo-check --model gpt-5.6-luna \
    -o /tmp/reportdir/report.txt >out.txt 2>err.txt
  echo "exit=$?"; test -f /tmp/reportdir/report.txt && echo EXISTS || echo ABSENT
  grep -c "Failed to write last message file" err.txt'
# expected: exit 0, ABSENT, and 1 matching stderr line

# 3. the inner sandbox failing while reporting success
W=$(mktemp -d); echo original > "$W/target.txt"
bwrap --dev-bind / / --tmpfs /tmp --bind "$W" "$W" --chdir "$W" -- sh -c '
  echo "Replace the contents of target.txt with exactly EDITED, then reply DONE." \
    | codex exec - --skip-git-repo-check --model gpt-5.6-terra \
        --sandbox workspace-write -c approval_policy=never >out.txt 2>err.txt
  echo "exit=$?"; tail -1 out.txt; cat target.txt'
# expected: exit 0 and target.txt still "original". ASSERT ON THE FILE, NOT THE MESSAGE:
# the model names the sandbox failure most of the time and claims DONE occasionally, so an
# honest-looking answer here is NOT evidence the trap is fixed. What would retire it is
# target.txt reading EDITED, or a non-zero exit.
# Swap to --sandbox danger-full-access and it must write correctly — that control is what
# separates "the inner sandbox blocked it" from "the model did not try".

# 4. srt: workspace-write versus danger-full-access — two model turns
# Prepare W and H under /var/tmp and s.json as in Under srt and opencode.md's lane.
# H/.codex must hold only the auth.json symlink. Set CODEX_BIN to the binary's real path
# under ~/.codex/packages, M to the model, and S to the settings file outside W.
O=$(mktemp -d -p /var/tmp)
for mode in workspace-write danger-full-access; do
  echo original > "$W/target.txt"
  (cd "$W" && printf '%s\n' \
    "Replace target.txt with EDITED via shell, then write OUT to $O/$mode.txt. Reply DONE or BLOCKED." \
    | srt --settings "$S" -- env HOME="$H" CODEX_HOME="$H/.codex" PATH=/usr/bin:/bin \
      "$CODEX_BIN" exec - --skip-git-repo-check --model "$M" --sandbox "$mode" \
      -c approval_policy=never -o "$W/$mode-report.txt" \
      >"$W/$mode-out.txt" 2>"$W/$mode-err.txt")
  echo "$mode exit=$?"; cat "$W/target.txt" "$W/$mode-report.txt"
  if [ "$mode" = workspace-write ]; then
    test "$(cat "$W/target.txt")" = original
    grep -F ENOSPC "$W/$mode-err.txt"
  else
    test "$(cat "$W/target.txt")" = EDITED
  fi
  test ! -e "$O/$mode.txt"
done
# expected: exit 0 both; workspace-write leaves original, stderr has ENOSPC,
# report BLOCKED in the three measured runs (the answer is not the assertion).
# danger-full-access writes EDITED, report DONE; srt refuses the outside write
# with Read-only file system. Both outside-file absence assertions pass.
```
