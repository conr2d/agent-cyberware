# hermes — additional support, and it has to be confined

> **Opt-in, like `opencode.md`.** `../SKILL.md` documents Claude Code and Codex. Open this file
> when a caller has named hermes, and nothing in the guide assumes any of it.
>
> Why it is here: hermes is local and its quota is whatever provider you point it at, so it
> survives a Claude or Codex subscription window the other lanes do not. That is the same reason
> `opencode.md` exists, and it is the reason a promotion offer on some third CLI is worth wiring
> up at all.

**Everything below was executed. Last verified: 2026-10-20** — hermes 0.22.2, bubblewrap
0.12.0, Linux 6.8, against the configured `nous` / `upstage/solar-mini4:free`; the day before,
the same probes ran against `openrouter` / `minimax/minimax-m3.1-flash:free` while the configured
provider had no token. First written 2026-09-03 on 0.21.0. Every probe at the end of this file
was re-run on both models. The output-limit and `--safe-mode` traps were not — neither
has a probe — and stand on their 0.21.0 measurement. The probes are at the end of this file
rather than in `verify.md`, so a standard pass neither runs them nor is made wrong by them
going stale.

**The version drifts the way agy's does.** The install reports its method as `git` and tells you
how far behind it is on every interactive start (`⚠ N commits behind — run hermes update`), so
the binary you tested is not necessarily the one that runs tomorrow. Stamp after `hermes update`,
never before.

## Read this before the first driven run

**A non-interactive hermes run executes shell commands unattended, including destructive ones.** No
approval prompt, no `--yolo` needed, non-TTY, exit 0. Measured against a sacrificial file:

```
hermes chat -q "Run exactly this shell command… rm -f <path>. Then reply DONE." --oneshot -Q
→ exit 0, response "DONE", and the file is gone
```

This is not a silent failure; it is a silent *capability*, and it is the single fact that decides
how hermes may be driven. Claude Code and Codex both need an explicit flag to reach that state.
hermes starts there. There is **no inner sandbox to turn on** — the flags are `--yolo` (loosen),
`--accept-hooks` (loosen), `--worktree` (git isolation, not security) and the `--ignore-*` family
(config isolation, not security). Confinement is therefore entirely *outer*, and mandatory.

One consequence worth stating plainly: the trap `sandboxed.md` documents for Codex — an inner
sandbox that fails to nest inside an outer one and reports success anyway — **cannot happen
here, because there is no inner sandbox to nest.** That is not an advantage. It means the outer
layer is the only layer.

The default toolset is wide, and two of its members leave a filesystem carve-out by design:

```
terminal  file  code_execution  browser  computer_use  cronjob  delegation  web  …
```

`cronjob` schedules runs that outlive the sandbox; `computer_use` drives desktop input rather
than the filesystem. **`-t` replaces the enabled set for one run** — measured: under `-t web`
the shell tool was genuinely absent ("I don't have a terminal/shell tool available"), and the
file the prompt asked for was never created. Name the toolsets an author actually needs. **On
0.22.2 the same probe still created nothing, but whether the model says so depends on the
model**: `solar-mini4` said it had no shell, while `minimax-m3.1-flash` called `web_search`
until hermes stopped it at fifty attempts, then exited 0 with a message about retrying. A toolset that cannot do the task is a budget sink, not a refusal;
`--max-turns` and `--run-budget` are what bound it.

## Quick reference

| | Prompt | Stdin | JSON out | Resume | Auth |
|---|---|---|---|---|---|
| **hermes** | `chat -q "<prompt>"` | `--query-file -` ✅ — a bare pipe is **discarded**, see traps | **none** | `--resume <id>` or `--continue [name]` | provider credentials under `~/.hermes` |

`-q` and `--query-file -` are mutually exclusive: passing both exits 2 before any model call.
`-Q/--quiet` implies `--oneshot`, and so does non-TTY stdio, so a driver needs neither spelled
out — but spell `-Q` out anyway, because it is what suppresses the banner.

**There is no JSON envelope on this path**, and that is the reason hermes stays out of
`../SKILL.md` rather than being promoted into it. A driver's success check is text and an exit
code, not a field. The model can still be asked to emit JSON as its answer; what is missing is
the wrapper around it.

## Canonical commands

```bash
# one shot, prompt on stdin — the form a driver wants
hermes chat --query-file - -Q --source tool -t terminal,file < prompt.txt

# one shot, prompt inline
hermes chat -q "<prompt>" -Q --source tool

# pin the model rather than inheriting config, and cap the run
hermes chat --query-file - -Q --source tool -m "<provider>/<model>" --provider <provider> \
            --max-turns 12 --run-budget 240 < prompt.txt

# resume: the id comes off STDERR, not stdout
SID=$(hermes chat --query-file - -Q --source tool < prompt.txt 2>&1 >/dev/null \
      | sed -n 's/^session_id: //p')
hermes chat --resume "$SID" --query-file - -Q --source tool < followup.txt
```

**`--source tool` keeps driven runs out of the user's own session list**, which is hygiene rather
than correctness, but it is the difference between reading your own chats back and reading a
driver's.

## Reading the output

| | accessor |
|---|---|
| response text | **stdout, in full** — there is no header line to strip |
| session id | **stderr**, as a line `session_id: <id>` after a blank line |
| failure | non-zero exit; the error text arrives on **stdout**, where the answer would have been |
| verdict | the exit code, plus an assertion on what the run was supposed to change |

**The streams are the other way round from what a reader expects, and getting it wrong is
expensive in both directions.** stdout carries the response alone, with a trailing newline;
`session_id:` never appears there. So a driver that strips a leading `session_id:` line from
stdout deletes the first line of the answer instead, silently — and one that requires such a
line in stdout to declare success will call every successful run a failure.

An error does not move to stderr. An unknown model exits 1 with the message on stdout, where a
driver capturing stdout as "the answer" will store it as one. **The exit code is what separates
the two**, which is why it belongs in the verdict even though, on its own, it settles nothing.

## Traps — none of these look like failures to a driver

**A piped prompt with no `--query-file -` is discarded, and the run still exits 0.** Claude Code,
Codex and agy all accept a bare pipe, so this is reached by porting a working driver rather than
by doing anything unusual. What comes back is the interactive banner:

```
echo "Reply with exactly: BARE_OK" | hermes chat --oneshot -Q
→ exit 0 · stdout: the ASCII banner, "Welcome to Hermes Agent!", "Goodbye!"
→ the prompt appears nowhere, no session_id: line, and -Q does NOT suppress the banner here
→ the only diagnostic, on stderr: "Warning: Input is not a terminal (fd=0)."
```

That warning reads as a note about terminal detection, not as *your prompt was thrown away*.
`--oneshot` is inert in this shape because it applies only to `-q`/`--query-file`. Pick a prompt
source explicitly, every time. The neighbouring mistake is loud: `-q` together with
`--query-file -` exits 2 with stdout empty and usage on stderr.

**Hitting the output limit reports success and does no work.** Every documented success signal is
satisfied and the run is empty:

```
→ exit 0 · a real session_id: on stderr · stdout non-empty
→ stdout, in full: "Response truncated due to output length limit"
→ the file the prompt asked it to edit: unchanged
```

Re-run in the same lane with a single-task prompt and it completes in seconds. So the limit is
reachable from an ordinary multi-part author spec, and nothing in the envelope distinguishes it
from a run that did the work. **Assert on the files the run was told to change, never on its
final message** — this is the trap that makes that rule non-optional for hermes.

**`--safe-mode` and `--ignore-user-config` discard the configured model along with the config.**
The published description says they fall back to built-in defaults; it does not say the model is
one of them. The fallback can be a paid model the account never chose, and on an account that can
pay for it the run simply proceeds and bills it. Here it surfaced as an exit-1 billing error,
which is luck, not a guarantee. **If you want an isolated run, pin `-m`/`--provider` explicitly**
rather than trusting what is left after the config is dropped.

**Observed, not deterministic:** a warning about the command scanner
(`⚠ tirith security scanner enabled but not available …`) appeared on **stdout**, ahead of the
response body, in some confined runs and not others. Not enough evidence for a rule; enough to
say that "stdout is the response" is a claim a parser should not stake a whole lane on.

**No confined lane is published for hermes yet.** One was measured under an earlier wrapper
but not under srt; the opencode lane in `opencode.md` shows the shape, and hermes differs in
needing its own tool and install trees readable and its lock files writable. Until it is
measured, do not dispatch hermes as an author outside a sandbox you have verified yourself.

## Verifying this file

Run these when this file is what is being checked. The first two cost no turn.

```sh
hermes update && hermes --version      # self-updates on its own schedule; stamp after
hermes tools list                      # the default-enabled set, live

# -q and --query-file - together must stay LOUD
echo hi | hermes chat -q "x" --query-file - -Q
# expected: exit 2, stdout empty, usage on stderr

# the streams, which have been wrong in a published description once
hermes chat -q "Reply with exactly: OK" -Q --source tool 2>/dev/null | cat -A
# expected: "OK$" and nothing else — no session_id: on stdout
hermes chat -q "Reply with exactly: OK" -Q --source tool 2>&1 >/dev/null
# expected: a blank line then "session_id: <id>"

# is a bare pipe still discarded? (the first silent one)
echo "Reply with exactly: BARE_OK" | hermes chat --oneshot -Q
# expected: exit 0, the banner on stdout, BARE_OK absent, no session_id:,
# and "Warning: Input is not a terminal (fd=0)." on stderr.
# If it answers instead, the trap is retired and the Quick reference stdin cell changes.

# does an unknown model still fail loudly, with its message on stdout?
hermes chat -q "say OK" -m "no-such-model-9x" -Q --source tool
# expected: exit 1, error text on stdout, session_id: still on stderr

# does the toolset restriction still hold?
hermes chat -q "Run this shell command then reply DONE: echo T > t.txt" -t web -Q --source tool
# expected: no t.txt. The answer is the model's: solar-mini4 said it had no shell, minimax
# ran web_search until stopped. Assert on the file, and bound the run.
```
