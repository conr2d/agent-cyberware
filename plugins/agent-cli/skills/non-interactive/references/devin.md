# Devin — additional support

> **Opt-in, like `opencode.md`.** `../SKILL.md` documents Claude Code and Codex. Open this file
> when a caller has named Devin or the Devin CLI; nothing in the guide assumes any of it.
>
> Why it is here: Cognition's Devin CLI (`devin`) runs Cognition's own SWE-2 models —
> post-trained from Kimi K3 per the vendor — on a Devin account, a quota and a model lineage
> the Claude, Codex and DeepSeek-backed opencode lanes do not share.

**Everything below was executed unless marked otherwise. Last verified: 2026-11-15** —
devin 3000.12.57 (`devin --version` prints `devin 3000.12.57 (<build>)`), on a Free plan,
model `swe-2-flash-medium`, all runs inside srt 0.0.81; see the lane below.
The update check was not run: `devin update` exists but was not exercised. The probes are at
the end of this file, not in `verify.md`.

## Quick reference

| | Prompt | Stdin | JSON out | Resume | Auth |
|---|---|---|---|---|---|
| **Devin** | `-p "<prompt>"`, `-p -- <prompt>`, or `-p --prompt-file <path>` | a pipe beside `-p` is **discarded**, see traps; `-p` without a prompt exits 1 | **none on stdout**; `--export <path>` writes a JSON transcript | `-r <name>` or `-c` (most recent) | `devin auth login` (interactive, once), stored in `~/.local/share/devin/credentials.toml` |

## Canonical commands

```bash
# one shot, unattended edits allowed, transcript to a file
devin -p --model swe-2-flash-medium --permission-mode accept-edits \
  --respect-workspace-trust false --export "$PWD/run.json" -- "<prompt>"
devin -p --model <model> --prompt-file "$PWD/prompt.txt" --respect-workspace-trust false
# resume by the session name the export carries, or the most recent session
devin -p -r "<session_id>" --respect-workspace-trust false -- "<followup>"
devin -p -c --respect-workspace-trust false -- "<followup>"
```

`--respect-workspace-trust false` is required in a directory never opened interactively.
Without it: exit 1, stdout empty, stderr `Error: Refusing to run in an untrusted workspace:
<dir>`, followed by a hint naming `respect_workspace_trust: false`. Loud, but every scratch
directory hits it.

`devin models` prints the families, ids and per-token prices the account can see; read that
rather than a copied list. On the Free plan only `swe-2-flash-*` ran. `swe-2-medium` exited 1,
stdout empty, stderr `Error: Upgrade to Pro to access this model`. An unknown id exits 1,
stderr `Error: Unknown model: '<id>'` followed by the available families.

There is no caller-pinned session id flag. The generated name has two words (measured:
`imaginary-almond`), available as `.session_id` in the export. Resuming that name recalled
the earlier declarative code word. An unknown name exits 1, stderr
`Error: No session found matching '<name>'`. `-c` recalled the most recent session from the
same directory. `devin list` is interactive and printed nothing usable from a non-tty;
do not use it in a driver.

On 2026-11-15, one OK turn took about 1.3 s wall time on the measured machine. This is one
measurement, not a startup guarantee.

## Reading the output

stdout carries assistant text only, no envelope. A completed turn exits 0; the loud failures
above exit 1. stderr carries warnings, including tool rejections below.

`--export <path>` writes JSON, measured with `schema_version` `ATIF-v1.7` and top-level keys
`agent`, `final_metrics`, `schema_version`, `session_id`, `steps`. **Read from `--help`, not
verified as a timing guarantee:** export happens after each turn.

| | accessor |
|---|---|
| text | `.message` of the last element of `.steps` whose `.source == "agent"` |
| session id | `.session_id` |
| model | that step's `.model_name`; `.agent.model_name` is a display name, e.g. `SWE-2 Flash Medium` |
| usage | `.final_metrics`: `total_prompt_tokens`, `total_completion_tokens`, `total_cached_tokens`, `total_steps`; also per-step `.metrics` |
| success | no success field; when asked to change a file, assert on the file |

A resumed export holds the whole session, earlier turns included: measured 13 steps and four
agent messages after two resumes. Select the **last agent step**, not the only agent step.
Exit 0 does not establish that the work happened.

The export also contains full tool definitions and system-injected skill text — about 70 KB
for a one-word turn. Keep it out of anything you publish.

## Traps — none of these look like failures to a driver

**A piped prompt beside `-p` is discarded, and the run exits 0.** Reached by porting a Claude
or Codex driver, both of which take prompts on stdin:

```
echo "The secret word is LARCH." | devin -p --respect-workspace-trust false -- \
  "What secret word came in on stdin? If none did, reply exactly NOSTDIN"
→ exit 0 · stdout NOSTDIN
```

A driver believing stdin supplied context gets an answer without it. With a pipe and `-p`
but no prompt, the failure is loud: exit 1, stdout empty, usage on stderr. The non-interactive
prompt sources are `-p <prompt>`, `-p -- <prompt>` and `-p --prompt-file <path>`.

**A tool the mode does not allow is rejected, and the run still exits 0.** Default `auto`
mode allows read-only tools only. Asked to replace a file:

```
→ exit 0 · stdout a sentence saying the modification was rejected · file unchanged
→ stderr: warning: rejected a tool call that requires confirmation. Running in non-interactive mode. Use --permission-mode dangerous to auto-approve all tools.
```

The warning appears once per rejected call and is the only signal outside the text. A driver
believing exit 0 means the edit landed is wrong. With `--permission-mode accept-edits`, the
same edit landed: exit 0, stdout `DONE`, stderr empty, file `EDITED`. A shell command in that
mode was still rejected with the same warning, exit 0. With `--permission-mode dangerous`,
`touch` created the file, exit 0. **Read from `--help` only:** `smart` uses a fast model to
judge safety; that mode was not measured.

**stdout joins every text segment of the turn with no separator.** A run said `Starting.`,
ran a command, said `Listing done.`, ran another, then replied `FINAL: EDITED`:

```
→ exit 0 · stdout exactly Starting.Listing done.FINAL: EDITED\n
```

Verified byte by byte. A driver asking for exactly a fixed number of lines gets narration
fused onto the first. Take the final message from the export's last agent step, or ask the
run to write a report file and assert on that file.

**`dangerous` means every tool, shell included, with no further confirm.** The shell probe
created its file at exit 0; stdout is still assistant text, not a tool-success field. A caller
believing the mode only permits edits has also authorized shell. Pair it only with a lane
supposed to mutate, inside an outer sandbox.

## Terms and data

**Read from the vendor's published terms, not executed; this is a terms-grade judgment.**
Cognition's Platform Terms of Service and Acceptable Use Policy, both last updated 2026-06-30,
were read 2026-11-15. Neither contained a clause about scripts, bots, or one agent driving the
CLI as a subprocess. Clauses that do exist make the account holder responsible for all
Services actions on their behalf, forbid sharing an account or credentials, require adherence
to the plan's usage limits, forbid resale, and require human oversight before irreversible
production actions. Unlike `agy.md`, nothing found puts a driver out of scope. Terms change;
re-read before relying on this judgment.

ToS §3.3.1 permits model training on customer data by default. A paid plan may opt out;
opting out also enables zero data retention with Cognition's model providers. The Free plan
has no opt-out. ZDR has stated exceptions for safety and abuse classifiers, AUP review and
legal process. No numeric retention period is stated. **Executed:** `devin auth status` on
the Free account reported `Telemetry: enabled`. On a Free plan, send only material you would
publish.

**Perishable, read from the vendor blog on 2026-11-15:** free use of SWE-2 in the Desktop app
and CLI was announced as permanent for paid plans on 2026-11-12. The executed Free-plan runs
could use `swe-2-flash-*` only. Usage allowances are not published as numbers.

## The confined author lane

**Executed 2026-11-15 — srt 0.0.81, devin 3000.12.57, `swe-2-flash-medium`.** Give the run a
throwaway HOME containing a **copy**, not a symlink, of `credentials.toml` and `config.json`.
The host's `~/.local/share/devin` stays unreadable except for the installed version directory
explicitly allowed below. Only the throwaway home and work directory are writable; `.git`
is denied writes. Deny-read every other tree holding caller data.

Write `s.json` outside the writable work directory. Replace `<home>`, `<work>` and `<uid>`
with the throwaway home, work directory and numeric user id. Re-allow srt's own install
directory if it lives under a denied tree, as described in `opencode.md`.

```json
{"network":{"allowedDomains":["server.codeium.com","app.devin.ai","api.devin.ai"],"deniedDomains":[],"allowAllUnixSockets":true},
 "filesystem":{"denyRead":["~","/run/user/<uid>","/tmp","/var/tmp","/mnt","/media"],
   "allowRead":["~/.local/share/devin/cli/_versions","<home>","<work>"],
   "allowWrite":["<home>","<work>"],"denyWrite":["<work>/.git"]}}
```

Measured launch requirements:

- Run the resolved binary: `readlink -f ~/.local/share/devin/cli/_versions/current/bin/devin`.
- Set `HOME`, `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_CACHE_HOME`, `XDG_RUNTIME_DIR` and
  `TMPDIR` to locations in the throwaway home inside the sandbox. With those set, `devin auth
  status` inside the lane reported the copied credentials file.
- srt sets proxy variables **inside** the sandbox. A wrapper using `env -i` must clear the
  environment in the inner shell and pass through `HTTPS_PROXY`, `HTTP_PROXY`, `ALL_PROXY`
  and their lower-case forms. Clearing outside dropped them: account lookup failed with
  `Connection failed` while `auth status` still printed `Logged in`.
- Passing `SSL_CERT_FILE` as an empty string made devin exit with `No CA certificates were
  loaded from the system`. Do not pass CA variables you have not set.
- See `sandboxed.md` for srt's outer-TMPDIR rule; do not set it to a denied path.

Results, asserted on files:

- The inside edit landed.
- A write outside the writable set reported exit 0 **inside** the lane, but the file did not
  exist on the host afterwards. The denied home is a scratch overlay: the write vanishes
  rather than failing. Assert on the host file, not the inner command's exit status.
- `git add` exited 128 with `Unable to create '.git/index.lock': Read-only file system`.
- `https://example.com` returned no response, curl code 000.
- Devin's own session DB and logs were written under the throwaway home only.

**Read from `--help` only:** Devin's `--sandbox` is a Research Preview using bwrap and seccomp
for the exec tool and can read everything except denied paths. It was not used and is not a
substitute for the outer sandbox.

On 3000.12.57 the installer left `credentials.toml` mode 664 (group-readable), measured once;
`chmod 600 ~/.local/share/devin/credentials.toml`. A copied credential might go stale if the
CLI rotates it — not observed, not measured.

### How it did as an author

On 2026-11-15, three synthetic tasks with hidden tests covered a parser module, a multi-file
fix-and-extend with a CLI exit-code contract and a judgment call, and a spec with three planted
contradictions. One run each: `swe-2-flash-medium` and opencode's `deepseek-v4.1-flash-free`
each passed every hidden test, left protected files byte-identical, reported test counts that
reproduced, and found all three contradictions. Neither flagged a deliberately unspecified
case. Wall times, Devin first: 58 s vs 31 s, 100 s vs 364 s, 44 s vs 74 s. One run each —
not a ranking. The content was throwaway and synthetic because the Free plan cannot opt out
of training.

## Verifying this file

Run these only when this file is being checked. They cost turns on the account. Use
throwaway synthetic content. `<work>` is a fresh directory that `devin` has never been opened
in interactively — the trust refusal is what the first probe asserts. Run the following inside
the lane, starting in `<work>`. The recorded outcomes above are the 2026-11-15 measurements.

```sh
devin --version
devin models
devin -p --model swe-2-flash-medium -- "Reply OK"
# expected: exit 1, stdout empty, untrusted-workspace error on stderr

echo "The secret word is LARCH." | devin -p --model swe-2-flash-medium \
  --respect-workspace-trust false -- \
  "What secret word came in on stdin? If none did, reply exactly NOSTDIN"
# expected: exit 0, stdout NOSTDIN
echo "Reply OK" | devin -p --respect-workspace-trust false
# expected: exit 1, stdout empty, usage on stderr

devin -p --model no-such-model-9x --respect-workspace-trust false -- "Reply OK"
# expected: exit 1, unknown-model error on stderr

echo original > target.txt
devin -p --model swe-2-flash-medium --respect-workspace-trust false -- \
  "Replace target.txt with exactly EDITED and nothing else. Then reply DONE."
# expected: exit 0, rejection warning on stderr; assert target.txt is still original
test "$(cat target.txt)" = original

devin -p --model swe-2-flash-medium --permission-mode accept-edits \
  --respect-workspace-trust false -- \
  "Replace target.txt with exactly EDITED and nothing else. Then reply DONE."
# expected: exit 0, stdout DONE, stderr empty; assert the edit
test "$(cat target.txt)" = EDITED

devin -p --model swe-2-flash-medium --permission-mode accept-edits \
  --respect-workspace-trust false -- "Use a shell command to touch shell-created."
# expected: exit 0, rejection warning on stderr; no shell-created file
test ! -e shell-created

# Declarative on purpose: a request to remember could write memory instead.
devin -p --model swe-2-flash-medium --export "$PWD/roundtrip.json" \
  --respect-workspace-trust false -- "The code word is LARCH. Reply with exactly: OK"
SID=$(python3 -c 'import json; print(json.load(open("roundtrip.json"))["session_id"])')
devin -p -r "$SID" --export "$PWD/resumed.json" --respect-workspace-trust false -- \
  "What was the code word? Reply with that word only."
# expected: exit 0, OK then LARCH, same .session_id in both exports
devin -p -r no-such-session-9x --respect-workspace-trust false -- "Reply OK"
# expected: exit 1, no-session error on stderr

devin -p --model swe-2-flash-medium --permission-mode dangerous \
  --respect-workspace-trust false --export "$PWD/joined.json" -- \
  "First say 'Starting.' Then run: ls. Then say 'Listing done.' Then run: cat target.txt. Finally reply with exactly the line FINAL: <contents of target.txt>" \
  > joined.txt
# expected: exit 0, bytes exactly Starting.Listing done.FINAL: EDITED followed by newline
python3 -c 'from pathlib import Path; assert Path("joined.txt").read_bytes() == b"Starting.Listing done.FINAL: EDITED\n"'
# Final answer alone: last agent step from the export, not joined stdout.
python3 -c 'import json; d=json.load(open("joined.json")); print([s for s in d["steps"] if s["source"] == "agent"][-1]["message"])'
```
