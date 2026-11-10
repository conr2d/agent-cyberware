# grok — additional support

> **Opt-in, like `opencode.md`.** `../SKILL.md` documents Claude Code and Codex. Open this file
> when a caller has named grok, and nothing in the guide assumes any of it.
>
> Why it is here: a grok.com session, or `XAI_API_KEY` when no session is stored, is a quota
> the Claude and Codex windows do not share.

**Everything below was executed. Last verified: 2026-11-10** — grok 1.0.77, which
`grok update --check` reported current; previously verified 2026-10-19 on 1.0.62. Stamp from `grok --version` after that check reports
the running build current, or after `grok update` when it does not. The probes are at the end
of this file, not in `verify.md`.

## Quick reference

| | Prompt | Stdin | JSON out | Resume | Auth |
|---|---|---|---|---|---|
| **grok** | `-p "<prompt>"` or `--prompt-file <path>` | a pipe beside `-p` is **discarded**, see traps | `--output-format json`, one object | `--resume <id>` | grok.com session in `~/.grok/auth.json`; `XAI_API_KEY` is the fallback when no session is stored |

The fallback half of that auth cell was read from the product's authentication document, not
executed. What was executed: a bogus `XAI_API_KEY` left an existing grok.com session in
charge, and the run still answered.

## Canonical commands

```bash
# one shot. The prompt is an argument, or a real file.
grok -p "<prompt>" --output-format json
grok --prompt-file prompt.txt --output-format json
# with --cwd, a relative --prompt-file resolves against that directory, not the shell's
grok --prompt-file "$PWD/prompt.txt" --cwd <dir> --output-format json

# pin the id, then resume it. --session-id only creates.
SID=$(uuidgen)
grok -p "<prompt>" --session-id "$SID" --output-format json
grok -p "<followup>" --resume "$SID" --output-format json

# --yolo runs tools unattended. --cwd is the directory they edit.
grok -p "<prompt>" --cwd <dir> --output-format json --yolo
```

The model is whatever `grok models` marks as the default. `-m` overrides it. A slug that
listing does not contain exits 1 before a turn. On an unpinned run the id under `modelUsage`
and the id the listing marks as default were not the same string; read both when the id
matters. On 2026-10-19 the listing marked `grok-4.7` default beside `grok-4.7-build-fast` and
`grok-4.6`, and runs reported `grok-4.7-build`. Signed out, the same command listed an older
pair with no error, so read it signed in.

On 2026-10-30, `grok models` signed in on grok 1.0.70 listed default `grok-4.7` beside
`grok-4.7-build-fast`, `grok-4.6` and `grok-4.5`. On 2026-11-10, on 1.0.77, it listed the same
four while printing `You are not authenticated.` above them, although every run that day
authenticated with the stored session and no `XAI_API_KEY`. Do not read that line as the
sign-in state; a run is what shows it.

## Reading the output

`--output-format json` writes one pretty-printed object. Parse all of stdout. A line-oriented
reader stops on the opening brace.

| | accessor |
|---|---|
| text | `.text` — the string itself has no trailing newline |
| session id | `.sessionId` |
| success | exit 0 and `.stopReason == "end_turn"` |
| failure before a turn | exit non-zero, always. Auth, model and session-id errors also put `{"type":"error","message":…}` on stdout (session ids since 1.0.77); `--prompt-file` errors leave stdout empty and say it on stderr only |

stderr is empty on a successful one-shot run from the directory the session was created in.
Resuming that session from another directory printed a `found locally` line on stderr and
left stdout as the JSON object. That line is not the answer. `.thought` is reasoning, not
`.text`.

## Traps — none of these look like failures to a driver

**A piped prompt beside `-p` is discarded, and the run still exits 0.** Claude Code and Codex
both take the prompt on stdin, so this is reached by porting a working driver.

```
echo "The secret word is LARCH." \
  | grok -p "What secret word came in on stdin? If none did, reply exactly NOSTDIN" \
        --output-format json
→ exit 0 · .stopReason "end_turn" · .text "NOSTDIN"
```

Three other shapes were measured, and each fails loudly. `--prompt-file -` reads a file named
`-` and exits 1, stdout empty. `-p` with no value exits 2, stdout empty, usage on stderr. A
positional prompt and no `-p`, with no tty, exits 1, stdout empty, `Error: No such device or
address` on stderr. The non-interactive prompt sources are `-p` and `--prompt-file <path>`.

**A tool the run cannot approve exits 0 and does no work.** Without `--yolo`, a prompt that
has to edit a file:

```
→ exit 0 · .stopReason "cancelled" · .text a sentence of intent
→ stderr: permission required: … was not run, as a headless run cannot ask for approval
→ the file: unchanged
```

Reproduced twice on 1.0.41 and twice on 1.0.62. The stderr line is new in between — it was
empty — and is the only signal outside the object; a driver that does not read stderr still
sees success. `num_turns` was 2 then and 1 now, under `--max-turns 4`, so this is not a turn
cap. Exit 0 and a non-empty `.text` both look like success. **Require `.stopReason ==
"end_turn"`, and when the run was told to change a file, assert on the file.**

**`--yolo` runs tools unattended, shell included.** The same edit then left the file
`EDITED`. A run told to `rm` a sacrificial file removed it, exit 0, `.stopReason
"end_turn"`. There is no further confirm. Pass `--yolo` only for a lane that is supposed to
mutate. No confined command is measured in this file. An outer sandbox measured for Codex
is `sandboxed.md`; that file is not a procedure for grok.

**A relative `--prompt-file` beside `--cwd` resolves against `--cwd`.** Exit 1, stdout empty
even with `--output-format json`, `Failed to read '<path>'` on stderr. Loud, but it is the
call a driver writes when it keeps prompts next to itself and points the run elsewhere; pass
the path absolute.

**`--session-id` creates. Resume is `--resume`.** The id has to be a UUID; `not-a-uuid`
exits 1. A second `--session-id` of an id already used **from the same directory** exits 1,
with `already in use` on stderr. The id you pinned is the `.sessionId` echoed back, and an id
you did not pin is stored too: `--resume` of that echo recalled the previous turn. A missing id
exits 1 after trying, per stderr, to restore it remotely. On 1.0.77 (2026-11-10) each of these three
failures also writes `{"type":"error","message":…}` to stdout, where 1.0.62 left stdout empty,
so test the exit code or `.type`, not an empty stdout.

**A reused `--session-id` from another directory is not refused.** Measured 2026-11-10 on
1.0.77: an id created in one directory, passed to `--session-id` from a second one, exited 0
and answered as a new conversation, with no memory of the first turn and the same `.sessionId`
echoed. The directory that counts is the process's own; `--cwd` pointing elsewhere still got
`already in use`. `--resume` of an id from a fresh directory did find the original (stderr:
`found locally (originally in <dir>)`) and recalled it. A driver that pins ids must make them
unique itself.

## Verifying this file

Run these when this file is what is being checked.

```sh
grok update --check --json && grok --version
grok models

# a pipe beside -p is still discarded
echo "The secret word is LARCH." \
  | grok -p "What secret word came in on stdin? If none did, reply exactly NOSTDIN" \
        --output-format json
# expected: exit 0, .text NOSTDIN, .stopReason end_turn

# --prompt-file - is still a filename, and a relative one resolves against --cwd
echo hi | grok --prompt-file - --output-format json
# expected: exit 1, stdout empty
echo "Reply OK" > p.txt; grok --prompt-file p.txt --cwd "$(mktemp -d)" --output-format json
# expected: exit 1, stdout empty, Failed to read on stderr

# a pinned id round-trips; creating it again is loud
SID=$(uuidgen)
# Declarative on purpose: a "remember X" prompt is how a probe ends up writing memory.
grok -p "The code word is LARCH. Reply with exactly: OK" --session-id "$SID" --output-format json
grok -p "What was the code word? Reply with that word only." --resume "$SID" --output-format json
# expected: OK, then LARCH, and the same .sessionId
grok -p "Reply NO" --session-id "$SID" --output-format json
# expected: exit 1, .type error, `already in use` on stderr (1.0.62: stdout empty)
(cd "$(mktemp -d)" && grok -p "What was the code word? Reply with that word only, or NONE." \
  --session-id "$SID" --output-format json)
# expected: exit 0, .text NONE — a second directory gets a new session under the same id
grok -p x --session-id not-a-uuid --output-format json
grok -p x --resume "$(uuidgen)" --output-format json
# expected: exit 1 each, .type error on stdout

# an unknown model is loud, and the message is on stdout
grok -p "Reply OK" -m no-such-model-9x --output-format json
# expected: exit 1, .type error

# without --yolo a write is cancelled. ASSERT ON THE FILE, not on .text.
D=$(mktemp -d); echo original > "$D/target.txt"
grok -p "Replace the contents of target.txt with exactly EDITED and nothing else. Then reply DONE." \
  --cwd "$D" --output-format json --max-turns 4
# expected: exit 0, .stopReason cancelled, `permission required` on stderr, target.txt original

# with --yolo the same write lands
D=$(mktemp -d); echo original > "$D/target.txt"
grok -p "Replace the contents of target.txt with exactly EDITED and nothing else. Then reply DONE." \
  --cwd "$D" --yolo --output-format json --max-turns 4
# expected: exit 0, .stopReason end_turn, target.txt is EDITED
```
