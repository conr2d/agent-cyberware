# Driving these CLIs from inside an outer sandbox

> **Opt-in, like `opencode.md`.** `../SKILL.md` documents Claude Code and Codex as a caller
> meets them on a bare machine. Everything here needs a second confinement layer around the
> process — a bubblewrap carve-out, a container, a CI runner with its own mount namespace — and
> a reader who is not doing that cannot reach any of it. Open this file when you are dispatching
> one of these CLIs into a sandbox you built.

**Verified 2026-08-28** — codex-cli 0.150.1, bubblewrap 0.11.2, Linux 6.8; **re-verified
2026-10-19** on codex-cli 0.163.0 and bubblewrap 0.12.0, every probe below as expected. Both
traps below were first observed 2026-08-27 by a worker driving Codex under bwrap, and
re-measured here first-hand before being written down.

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

Treat that warning as fatal for `workspace-write`; it is the cheapest place to catch this.

**So when an outer sandbox already confines the process, the inner one is not a second layer but
a failure mode.** Turning it off with `--sandbox danger-full-access` is not a loosening wherever
the outer carve-out is narrower than `workspace-write` would have granted on a bare machine —
`workspace-write` writes to `[workdir, /tmp, $TMPDIR]`, which a carve-out binding only the project
directory already beats. `codex exec --help` anticipates the situation for the neighbouring flag,
documenting `--dangerously-bypass-approvals-and-sandbox` as *"Intended solely for running in
environments that are externally sandboxed"* — but that the nesting fails **this way**, silently
and with a success message, is written down nowhere.

## Verifying this file

The mechanism check costs nothing and settles most of it. The two CLI probes cost one turn each.

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
```
