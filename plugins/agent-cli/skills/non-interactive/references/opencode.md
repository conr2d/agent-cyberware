# opencode — additional support

> **Not one of the two.** `../SKILL.md` covers Claude Code and Codex, and is paid for on every
> invocation. This file is loaded only when a caller has actually asked for opencode, and
> nothing in it is assumed by the rest of the skill.

Why it is here at all: both CLIs in the guide are bound to subscription windows. Codex enforces
a 5-hour window per account, and when it closes there is no second-opinion lane left — agy does
not fill the gap for an agent-driven caller, on terms grounds, which is why it is opt-in too
(`agy.md`). opencode's quota is whatever API key the caller holds, so it is the fallback that
does not share a limit with anything else.

**Verified 2026-10-19** — opencode 2.0.32, model `opencode/deepseek-v4.1-flash-free`,
bubblewrap 0.12.0. Everything below was executed unless it says otherwise. **2.0 is a different
program from the 1.18 this file was first written against**: `run` now goes through a resident
background server, three flags are gone, three traps are new or newly found, and the pre-turn
failures that used to name nothing now name what was wrong. Other providers and models are
untested here; the surface should hold, the latencies will not.

Installed at `~/.opencode/bin/opencode`, which is **not** on a default `PATH`. `opencode
upgrade` updates it; stamp after that, not before.

## Quick reference

| | opencode |
|---|---|
| Prompt | `opencode run "<prompt>"` (positional) — `--prompt` is gone in 2.0 |
| Stdin | plain text ✅ **when no positional prompt is given**; beside one it is **dropped**, see Traps |
| JSON out | `--format json` → NDJSON, one event per line |
| Resume | `-s <sessionID>`; `-c/--continue` for the last one; `--fork` to branch |
| Model | `-m <provider>/<model>`, effort as `-m <provider>/<model>#<variant>` — `--variant` is gone |
| Server | a background service by default; `--standalone` for a private one; `--server <url>` to name one |
| Auth | `opencode auth` (credentials in `~/.local/share/opencode/auth.json`) |

The provider slug is the one `opencode models` prints, which is not always the vendor's own
name. `opencode/…` is opencode's own hosted catalog, and its `-free` models need no balance.

## Canonical commands

```bash
# one shot. Close stdin when the prompt is an argument — an open stdin is waited on.
opencode run --format json --model <provider>/<model> "<prompt>" </dev/null
opencode run --format json --model <provider>/<model> < prompt.txt

# resume: read .sessionID off any event of the first run, pass it back with -s.
# The id survives — the resumed run reports the same one — and so does the context.
opencode run --format json --model <provider>/<model> -s "<sessionID>" "<followup>" </dev/null

# effort, where the model has levels (read them under Model notes first)
opencode run --format json --model "<provider>/<model>#high" "<prompt>" </dev/null

# what is installed, and under what slug
opencode models | grep -i <vendor>
```

## Reading the output

`--format json` emits NDJSON. Every event carries `.sessionID`; the payload is under `.part`.

| | accessor |
|---|---|
| text | last event with `.type == "text"` → `.part.text` |
| session id | `.sessionID` (on every event; a `-s` resume keeps the same one) |
| success | exit 0, **no** `error` event, and at least one `text` event — see Traps for why not `step_finish` |
| failure | exit 1 and an `error` event on stdout: `.error.type` (`provider.no-route`, `provider.quota`, …) and `.error.message`, which names the model or variant at fault |
| tokens / cost | `step_finish` → `.part.tokens`, `.part.cost` — **when one arrives** |

`reason` on a `step_finish` is `"tool-calls"` on the intermediate steps of a tool-using turn
and `"stop"` on the last, so when they do arrive take the final one. **The exit code now means
something**: every failure measured on 2.0 — unknown model, unknown variant, a provider 402
before the turn, and an unknown `-s` id, which `--help` says creates the session — exited 1
with an `error` event. On 1.18 a provider error mid-turn exited 0, and that was the reason the
old success test ignored the exit code; mid-turn was not re-induced here, so keep checking for
the `error` event as well.

**`.part.cost` is computed from the models.dev catalog** cached at
`~/.cache/opencode/models.json`, not from what the provider billed. On 1.18 a free-tier run
still reported a non-zero list price. The free model measured here lists a cost of zero, so
that it is an estimate was not re-shown on 2.0; do not sum these into a spend figure either way.

## The background server

**`opencode run` no longer runs the agent in its own process.** It connects to a managed
service on a fixed `127.0.0.1` port (`opencode service status` prints the URL), starting it if
none is up. That service is now password-protected: `--server <url>` against it exits 1 with
`requires a password; set OPENCODE_PASSWORD`, where 1.18's `opencode serve` printed that it was
unsecured.

**A second `$HOME` cannot start its own service on the same port, and says so.** Anything that
runs opencode under a different home — the lane split under *Configure permissions*, a sandbox,
a CI job — exits **1** with `Managed service port <n> on 127.0.0.1 is already in use by another
process`, stdout empty. It is loud, and it fails closed: the run does not fall through to the
machine's own service. **`--standalone` runs a private server for the one call** and is what
those cases need. Measured cost: about 1.4 s through the service against 2.0 s standalone, for a
one-word answer from this model.

What an earlier version of this file warned against — building a serve/attach fast path — is now the default,
and its two reasons are gone with `--attach`: the answer comes back on stdout through the
service. **Spawn per call** stands only in the sense that each `run` is still one process.

## Configure permissions before the first real use

**`opencode run` executes shell and edit tools with no flag at all**, and `--auto` is not the
gate its help text suggests — it auto-approves what is not explicitly denied, but its *absence*
denies nothing. Verified by filesystem on 1.18: a run told to `echo … > proof.txt` created the
file, twice out of two. The session default denies only `question`, `plan_enter` and
`plan_exit`.

For a second-opinion lane, deny everything that mutates or reaches out. This belongs in
`~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "read": "allow", "list": "allow", "glob": "allow", "grep": "allow",
    "lsp": "allow", "todowrite": "allow",
    "edit": "deny", "bash": "deny",
    "external_directory": "deny", "task": "deny", "skill": "deny",
    "webfetch": "deny", "websearch": "deny",
    "question": "deny", "doom_loop": "deny"
  }
}
```

Keys and values come from the published schema (`https://opencode.ai/config.json` →
`$defs.PermissionConfig`), each `"ask" | "allow" | "deny"` or a pattern object. Re-measured on
2.0.32 through the background service:

- **`deny` holds, and holds against `--auto`.** `proof.txt` was not created either way.
- **Read-only tools keep working.** A run still reads a file and reports its contents.
- **A denied tool is visible in the answer, not in a field.** The model says the tool is
  unavailable, with exit 0 and no `error` event, so a driver that checks only those cannot tell
  a refusal from an answer — but the response is not empty, which is what separates this from
  agy's denial in `agy.md`.

**The block above is written for one lane, and a second lane needs the opposite.** An author
agent that writes code needs exactly the `edit` and `bash` this denies. Do not loosen the shared
file to get them: **the config is resolved from `$HOME`**, so a run given its own home gets its
own permission block. On 2.0 that run also needs **`--standalone`**, or it fails on the service
port as above. Measured 2026-10-19: a home whose config set `edit` and `bash` to `allow`, run
with `--standalone`, wrote `shell.txt` through the shell tool, exit 0; the same without
`--standalone` exited 1 on the port. On 1.18 the lane split was also measured on `edit`; on 2.0
only the shell half was.

Which means the safety is not in the config. **Give an author lane a `$HOME` of its own and
confine it; the config then states the lane's role rather than doing the work.**

**Found in the binary and never invoked — do not write these up as though they were tested.**
`OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR` and `OPENCODE_DISABLE_PROJECT_CONFIG` appeared in a
1.18 strings dump (with `OPENCODE_CONFIG_CONTENT` and `OPENCODE_AUTH_CONTENT`). Their presence
is evidence the symbols existed and nothing more:

```sh
strings -a "$(readlink -f "$(command -v opencode)")" | grep -oE 'OPENCODE_[A-Z_]+' | sort -u
```

## The confined author lane

**Measured 2026-10-20** — srt (`@anthropic-ai/sandbox-runtime`) 0.0.81, opencode 2.0.32,
bubblewrap 0.12.0, Ubuntu with `kernel.apparmor_restrict_unprivileged_userns=1`, model
`opencode/deepseek-v4.1-flash-free`.

srt (`@anthropic-ai/sandbox-runtime`) is Anthropic's open-source sandbox; on Linux it drives
bubblewrap. The lane makes the project writable except its `.git`, gives the run a throwaway
`$HOME`, hides everything else of yours, and limits the network to the provider's domains.

Write `s.json`, replacing `<repo>`, `<home>`, `<srt-dir>` and `<uid>` with the project,
throwaway home, srt's own install directory if under `~`, and your numeric user id. The project
and home in the measurement were both under `/var/tmp`.

```json
{"network":{"allowedDomains":["opencode.ai","*.opencode.ai"],"deniedDomains":[],"allowAllUnixSockets":true},
 "filesystem":{"denyRead":["~","/run/user/<uid>"],
   "allowRead":["~/.opencode","~/.local/share/opencode/auth.json","<srt-dir>"],
   "allowWrite":["<repo>","<home>"],"denyWrite":["<repo>/.git"]}}
```

Set `W` to that project and `H` to that throwaway home, and prepare the home's credential
symlink before running. **Keep `s.json` outside the project** — inside it, the file would sit in
the author's writable tree and in the reviewer's diff.

```sh
mkdir -p "$H/.local/share/opencode"
ln -s "$HOME/.local/share/opencode/auth.json" "$H/.local/share/opencode/auth.json"
mkdir -p /tmp/claude
cd "$W" && srt --settings /path/to/s.json -- env HOME="$H" PATH="$HOME/.opencode/bin:/usr/bin:/bin" \
  opencode run --standalone --format json --model <provider>/<model> "<spec>" </dev/null
```

Results, asserted on files, exit 0:

- `target.txt` in the project became `EDITED`, through both the write tool and shell.
- A shell write to another `/var/tmp` directory failed with `Read-only file system`; nothing
  was created there.
- `ls ~/.ssh` and the same path spelled absolutely returned `No such file or directory`;
  `denyRead` hides it. `ls /run/user/<uid>` was empty.
- `git add` failed with `Unable to create .../.git/index.lock: Read-only file system`.
- `curl https://example.com` inside failed with `CONNECT tunnel failed, response 403`;
  `https://opencode.ai` returned 200.
- opencode logged WARN `failed to capture snapshot ... .bash_profile: unsupported file type`.
  srt bind-mounts `/dev/null` over dotfiles (`.bashrc`, `.bash_profile`, `.gitconfig`,
  `.gitmodules`, …) in each writable directory to stop their creation; opencode's snapshot git
  trips on them. Warning only: the run succeeds, and nothing is left on the host afterwards.

**`--standalone` is needed and kept here.** Under the previous wrapper, measured 2026-10-19,
the carve-out shared the network namespace: without it the run tried to start the managed
service on the port the machine's own service already held and exited 1 before any turn.
The srt command above keeps `--standalone`; the port-collision control was measured under the
previous wrapper, not re-measured under srt.

**The permission block above is not what makes this lane an author, and does not need to be
copied into it.** A throwaway home has **no config at all**, so opencode's own defaults apply —
and its defaults already run shell and edit tools with no flag, which is the hazard the section
above opens with. Under the carve-out that default is exactly right. Do not allow-read the
shared permission config into it.

| | on a bare machine | inside the carve-out |
|---|---|---|
| what keeps the run safe | the deny block in `~/.config/opencode` | the carve-out |
| what the permissive default is | the hazard | what an author needs |
| what to bind | — | not `~/.config/opencode` |

Which leaves a per-lane home doing one job rather than two: **persistence, not permission.**
A throwaway home means a cold model cache every dispatch, and opencode keeps one session database
across every project it has run in, so reusing a home for this lane gives it its own.

Two of the read allowances are not padding. **`allowRead` on `~/.opencode`** makes the binary
readable, and the explicit `PATH` puts it on the command path. **`allowRead` on
`~/.local/share/opencode/auth.json`** hands the credential in as a single read-only file,
symlinked into the throwaway home, so the run can authenticate without being able to rewrite
what it authenticates as. Allowing the whole directory instead broke the run on 1.18 because
opencode writes its log there; the single-file form above was measured under srt.

**`denyWrite` on `<repo>/.git`** turns *the author does not commit* from an instruction into a
property: reads keep working, while `git add` fails on the index lock and history stays the
reviewer's.

### Traps under srt

1. **A missing settings field is loud.** Omitting, for example, `network.deniedDomains`
   makes srt refuse with `does not hold a valid config — network.deniedDomains: Required`.
   Keep all of `network.allowedDomains`, `network.deniedDomains`, `filesystem.denyRead`,
   `filesystem.allowWrite` and `filesystem.denyWrite` present.
2. **`denyRead` on `~` also hides srt's own helper when it is installed there**, including an
   npx cache or npm prefix under `~`. Exit 127:
   `…/vendor/seccomp/x64/apply-seccomp: No such file or directory`.
   Re-allow srt's install directory with `allowRead`.
3. **Ubuntu 24.04+ with `kernel.apparmor_restrict_unprivileged_userns=1` blocks the seccomp
   helper's nested user namespace.** Exit 1:
   `apply-seccomp: write /proc/self/setgroups (nested userns is capability-restricted; caller must provide CAP_SYS_ADMIN): Permission denied`.
   Without sudo, set `network.allowAllUnixSockets=true`: this drops the helper and uses
   `bwrap --disable-userns` instead. Unix sockets are then unfiltered, so deny-read their
   directories, including `/run/user/<uid>` where ssh-agent and the session bus live.
   With sudo, srt's README names the sysctl or an AppArmor profile; that is a system-wide
   change and the operator's call. The same error occurs when srt runs inside another bwrap
   sandbox.
4. **`/tmp/claude` must exist first.** srt sets `TMPDIR=/tmp/claude` inside and makes it
   writable only if it already exists; otherwise it reports `Skipping non-existent write path`
   and opencode exits 1 with `EROFS: read-only file system, mkdir '/tmp/claude'`.
   Run `mkdir -p /tmp/claude` first.
5. **srt parses the wrapped command's short options without `--`.**
   `srt --settings s.json curl -sS …` fails with `Error: S does not exist.` because `-s`
   means `--settings` to srt. Always put `--` before the wrapped command.
6. **`git status` inside the lane can report untracked dotfiles the host does not have.**
   Observed once, 2026-10-28, with `opencode/deepseek-v4.1-flash-free`: the author ran
   `git status` and reported `.bashrc`, `.gitconfig`, `.mcp.json` and similar at the project
   root. These are srt's `/dev/null` bind-mounts over dotfiles, described above; the host had
   none after the run. Tell the author in the spec that they belong to the lane: not stray
   files to delete, stage or report. (Staging fails in this lane anyway, on `denyWrite` for
   `.git`.)

What the lane does not do: Unix sockets are not filtered with `allowAllUnixSockets` on, hence
the deny-read on `/run/user/<uid>`. The provider's domain is reachable, so the project's contents
can still leave through it. And srt does not nest inside another bwrap sandbox; see
`sandboxed.md`.

## Traps

**A positional prompt with stdin beside it drops stdin, and exits 0.** 1.18 merged the two; 2.0
answers the argument alone:

```
echo "The secret word is LARCH." | opencode run --format json --model <m> \
  "What secret word came in on stdin? If none did, reply exactly NOSTDIN"
→ exit 0 · a text event · NOSTDIN
```

Stdin on its own still works. Send the whole prompt one way.

**An open stdin is waited on, even with a positional prompt.** A run whose stdin is a pipe that
never closes — a driver's inherited descriptor, a Bash tool's — produces nothing on either
stream until stdin reaches EOF, then answers and discards what it read. Measured: an open pipe
held a run past a 25 s timeout with zero bytes out; the same pipe closing at 8 s gave the
answer at 9 s. A run on an inherited stdin — against a model the account could not pay for —
produced nothing for over ten minutes; the same model with stdin closed failed in seconds with
a 402. **Redirect `</dev/null`** when the prompt is an argument, which is why every canonical
call above does.

**`step_finish` often never arrives, on a run that succeeded.** On 2.0.32 the final event of a
healthy one-shot was `text` in most runs measured — three of six in one batch, all six in
another, exit 0 and the answer present every time. A success test keyed on a final
`step_finish` with `reason: "stop"`, which is what this file prescribed for 1.18, reports those
runs as failures. Use the test in *Reading the output*, and treat tokens and cost as
best-effort.

**The first run on a home takes much longer than the rest.** Provider and model metadata are
cached under `$HOME/.cache/opencode/` on first use; on 1.18 a cold first run exceeded 120 s
and a seeded fresh home took 22.5 s against 9.4 s warm. *Not re-measured on 2.0*, whose warm
runs here took about 1.4 s. A throwaway home pays it every time; budget for it once per home.

## Model notes

`opencode/deepseek-v4.1-flash-free` — context 200,000, max output 32,000, cost 0, reasoning
`effort` with `low`, `high`, `max`, per opencode's own catalog. Re-read rather than trusting
that:

```sh
python3 -c "
import json; d=json.load(open('$HOME/.cache/opencode/models.json'))
for mid, m in d['opencode']['models'].items():
    print(mid, '|', m.get('limit'), '|', m.get('cost'), '|', m.get('reasoning_options'))"
```

**Reasoning is not always a dial.** The catalog carries four shapes — `[]`, `toggle`, `effort`
with a value list, and `budget_tokens` with a min/max — so read the shape, not just whether the
key is present. A `#variant` the model does not list exits 1 with `Variant unavailable for
<model>: <variant>`, so on 2.0 an effort that does not exist is loud; `#high` on this model
answered at exit 0. Whether reasoning tokens are counted could not be read, because the runs
that used `#high` were among those with no `step_finish`.

## Verifying this file

These are **not** part of the standard pass in `verify.md`; run them when this file is the thing
being checked. Each needs a scratch directory and the permission block above in place.

```sh
export PATH="$HOME/.opencode/bin:$PATH"
opencode upgrade && opencode --version
M=opencode/deepseek-v4.1-flash-free

# surface: prompt, stdin, and both together
opencode run --format json --model $M "Reply with exactly: OK" </dev/null
echo "Reply with exactly: STDIN_OK" | opencode run --format json --model $M
echo "The secret word is LARCH." | opencode run --format json --model $M \
  "What secret word came in on stdin? If none did, reply exactly NOSTDIN"
# expected: OK / STDIN_OK / NOSTDIN — the third proves stdin is dropped beside an argument.
# If it says LARCH, stdin is merged again and the first trap is retired.

# an open stdin is waited on
sleep 45 | timeout 25 opencode run --format json --model $M "Reply with exactly: OK"
# expected: exit 124, nothing on stdout

# step_finish: count how often a healthy run ends without one
for i in 1 2 3 4 5 6; do opencode run --format json --model $M "Reply with exactly: OK" </dev/null \
  | python3 -c "import json,sys; print([json.loads(l)['type'] for l in sys.stdin if l.strip()][-1])"; done
# expected, today: a mix of text and step_finish. All step_finish retires the trap.

# failures are loud and named
opencode run --format json --model opencode/no-such-model-9x "Reply OK" </dev/null
opencode run --format json --model "$M#bogus" "Reply OK" </dev/null
opencode run --format json --model $M -s ses_doesnotexist123 "Reply OK" </dev/null
# expected: exit 1 each, an error event on stdout naming what was wrong

# permission floor: the shell tool must NOT create the file, with or without --auto.
cd "$(mktemp -d)"
rm -f proof.txt
opencode run --format json --model $M "Run the shell command: echo NOPE > proof.txt   Then reply DONE." </dev/null
test -f proof.txt && echo "FAIL: deny is not applied" || echo "ok: denied"
rm -f proof.txt
opencode run --format json --auto --model $M "Run the shell command: echo NOPE > proof.txt   Then reply DONE." </dev/null
test -f proof.txt && echo "FAIL: --auto overrides deny" || echo "ok: deny beats --auto"
echo "hello from probe" > sample.txt
opencode run --format json --model $M "Read sample.txt and reply with its exact contents." </dev/null
# expected: the reply contains "hello from probe"

# a second home needs --standalone, and fails loudly without it
H=$(mktemp -d); mkdir -p "$H/.local/share/opencode"
ln -s ~/.local/share/opencode/auth.json "$H/.local/share/opencode/auth.json"
env HOME="$H" opencode run --format json --model $M "Reply with exactly: OK" </dev/null
# expected: exit 1, `Managed service port … already in use` on stderr
env HOME="$H" opencode run --standalone --format json --model $M "Reply with exactly: OK" </dev/null
# expected: OK

# the confined lane — ASSERT ON THE FILES
W=$(mktemp -d -p /var/tmp); echo original > "$W/target.txt"; O=$(mktemp -d -p /var/tmp)
H=$(mktemp -d -p /var/tmp); C=$(mktemp -d -p /var/tmp)   # C holds the settings, outside W
mkdir -p "$H/.local/share/opencode"
ln -s "$HOME/.local/share/opencode/auth.json" "$H/.local/share/opencode/auth.json"
mkdir -p /tmp/claude
# SRT_DIR: srt's own install directory when it is under ~ (else leave it unset).
python3 - "$W" "$H" "${SRT_DIR:-}" "$(id -u)" "$C" <<'PYSETTINGS'
import json, sys
from pathlib import Path
repo, home, srt_dir, uid, cfg = sys.argv[1:]
settings = {
    "network": {"allowedDomains": ["opencode.ai", "*.opencode.ai"],
                "deniedDomains": [], "allowAllUnixSockets": True},
    "filesystem": {"denyRead": ["~", f"/run/user/{uid}"],
                   "allowRead": ["~/.opencode", "~/.local/share/opencode/auth.json"]
                                + ([srt_dir] if srt_dir else []),
                   "allowWrite": [repo, home], "denyWrite": [f"{repo}/.git"]}
}
Path(cfg, "s.json").write_text(json.dumps(settings))
PYSETTINGS
(cd "$W" && srt --settings "$C/s.json" -- env HOME="$H" PATH="$HOME/.opencode/bin:/usr/bin:/bin" \
  opencode run --standalone --format json --model "$M" \
    "Replace the contents of target.txt with exactly EDITED, then run: echo OUT > $O/out.txt" </dev/null)
test "$(cat "$W/target.txt")" = EDITED
test -z "$(ls -A "$O")"
# expected: both assertions pass — target.txt is EDITED, and $O stays empty.
```
