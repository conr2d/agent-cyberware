# agy (Antigravity) — opt-in, because of who may drive it

> **Opt-in, like `sandboxed.md`.** `../SKILL.md` documents Claude Code and Codex, which any
> caller may drive. agy is different: its terms turn on *who* is driving, and the caller that
> loads this skill is usually the one that may not. Open this file when the driver is agy
> itself, or when you are writing a script or a CI job a person will run. Nothing in
> `../SKILL.md` assumes any of it.

**The terms judgement, 2026-08-31. Read from the published agreement, not verified with the
vendor** — a document-grade claim, weaker than the executed ones below, and the kind that
changes without notice. Re-read it before relying on this file. Antigravity's Additional Terms
of Service, section 6, *Prohibited Conduct*, carries two clauses that bear on a driver:

- *"Using third party software, tools, or services to access the Service (e.g. using OpenClaw
  with Antigravity OAuth) is a breach of this Agreement."*
- *"You must not abuse, harm, interfere with, or disrupt the Service. This includes, but is not
  limited to, using the Service in connection with products not provided by us."*

**Neither forbids non-interactive use. Both turn on the caller**, and the second is the one that
bites:

| driver | reading |
|---|---|
| A third-party client speaking to the backend on Antigravity OAuth | Prohibited. This is the example the agreement names. |
| **Another vendor's agent spawning `agy`** — Claude Code, Codex, an orchestrator | *In connection with products not provided by us.* This is the case to avoid, and it is the one a reader of this skill is most likely to be in. |
| agy driving agy, or a person's own script, CI job, or shell | No third party, no foreign product. Nothing here reaches it. |

The first clause is arguable for `agy` specifically, since the CLI is first-party rather than a
third-party client; the second is not, and it is sufficient on its own. Auth closes the obvious
escape: agy is **OAuth only**, so there is no API-key path that would make the account something
other than a subscription being used by a foreign product.

**Everything below was executed, not read off `--help`. Last verified: 2026-10-20** (agy 1.4.2;
first written on 1.1.16).
The probes are at the end of this file rather than in `verify.md`, so a standard pass neither
runs them nor is made wrong by them going stale.

## Quick reference

| | Prompt | Stdin | JSON out | Resume | Auth |
|---|---|---|---|---|---|
| **agy** | `-p "<prompt>"` inline, or stdin | plain text with no `-p` ✅; `-p` wins and stdin is dropped | `--output-format json` | `--conversation <id>` | OAuth only |

## Canonical commands

```bash
# either give the prompt inline with -p, or send it on stdin with no -p at all.
# -p wins when both are present, and the stdin side is then dropped without a word.
agy -p "<prompt>" --model gemini-3.8-flash-low --output-format json
agy --model gemini-3.8-flash-low --output-format json < prompt.txt
# resume by id is --conversation; -c is --continue and takes no value
agy --conversation "<uuid>" -p "<followup>" --output-format json

# many turns down one pipe: no -p, and both formats must be stream-json
echo '{"event":"user","message":{"role":"user","content":"<prompt>"}}' \
  | agy --input-format stream-json --output-format stream-json --model gemini-3.8-flash-low
```

**Long prompts go over stdin**, in the plain-text form with no `-p`. A single argv string is
capped near 128KB on Linux (`MAX_ARG_STRLEN`), and stream-json is the wrong escape because it
carries the prompt as a JSON string field that has to survive escaping.

## Reading the output

| | text | session id | success |
|---|---|---|---|
| agy (`json`) | `.response` | `.conversation_id` | `.status == "SUCCESS" && .response != ""`, and no `.denied_actions` |
| agy (`stream-json`) | final `.event == "result"` → `.result.response` | `.result.conversation_id` (top-level only on `init`) | the same three, under `.result` |

**agy adds `.error` on a failed run** — an unknown `--model` gives `status: "ERROR"`, exit 1
and `.error` naming the rejected slug, with the same message repeated on stderr (stderr was empty
for this on 1.1.22). The converse does not hold: a missing `.error` is not evidence the run did
any work (see the denied-tool trap below).

**agy's `.response` arrives with a trailing newline**; Claude's `.result` and Codex's
`item.text` do not. Strip it before comparing, or an equality check fails silently.

## Traps — none of these look like failures to a driver

**agy drops stdin without a word when `-p` is also present.** Both are valid prompt sources,
`-p` wins, and the pipe you attached is discarded — no warning, no `.error`, exit 0, and a
fluent answer to the wrong question. Of the agy prompt mistakes documented here it is the only
one that still fails silently, and it is easy to reach by templating a command that appends
`-p` onto a driver that already redirects a file in. Pick one source per call.

Its louder siblings need no trap of their own but are worth knowing, since all three used to
be silent: a value-less `-p` swallowing the next flag, a stray positional left over from
`-c "<id>"` (`-c` is `--continue` and takes no value — resume by id is `--conversation`), and
`-p` passed in stream-json mode all now exit 2 with stdout empty and a diagnostic on stderr.
The first two name the token; the third reports the mode conflict and has no swallowed token
to name.

**agy reports a denied tool as a successful run.** Without `--dangerously-skip-permissions`, a
tool-using print run exits **0** with `status: "SUCCESS"`, an empty `.response` and no `.error`
— it clears both the exit code and the status check having done nothing. Since some release
after 1.1.22 the envelope does carry the denial, as `"denied_actions":
[{"action":"command","display_name":"RunCommand"}]`, in `json` and on the stream-json `result`
alike; before that the only diagnostic was on stderr. The status is no more dependable than it
was: on 1.1.22 the stream-json denial sometimes came back `CANCELED`, and on 1.4.2 it was
`SUCCESS` in all four samples. **Check the empty `.response` and the presence of
`.denied_actions`**, not the status. Add the flag (either position relative to the print flags)
or a `permissions.allow` rule in `settings.json`.

**agy's stream-json input uses `event`, not `type`**, as
`{"event":"user","message":{"role":"user","content":"..."}}`. An unrecognised event *value*
costs you the turn with no error a driver can see: the warning goes to stderr, stdout carries
the `init` event and nothing else, and the process exits 0. Assert that a `result` event
arrived for each message you sent — stream-json runs a turn per line, so a later turn can die
after an earlier one has already reported — then that `.result.status == "SUCCESS"` on each.
The neighbouring mistakes are all loud: mismatching the two formats refuses to start
(`--input-format stream-json` requires `--output-format stream-json`), and passing `-p` in this
mode is rejected outright.

## Models and effort

Effort is either baked into the slug or given with `--effort low|medium|high|xhigh|max`, and the
two do not combine: `--model gemini-3.8-flash --effort high` runs, while a suffixed slug with a
different effort (`gemini-3.8-flash-low --effort high`) exits 1 with `.error` naming the conflict.
A bad effort value is refused the same way, listing the valid ones.

```
gemini-3.8-flash-{low,medium,high}      ← current default family
claude-sonnet-4-6
claude-opus-4-6-thinking
gpt-oss-120b-medium
```

**That is the whole catalogue on 2026-10-20, agy 1.4.2**, identical across six consecutive
`agy models` calls. The 3.7, 3.6 and 3.5 flash families and both `gemini-3.1-pro` rows are gone,
and invoking `gemini-3.7-flash-low`, `gemini-3.7-flash-high` or `gemini-3.1-pro-high` exits 1
with `status: "ERROR"` and `.error` printing the list agy will serve. Six listings agreeing is
not stability: on 2026-08-31, agy 1.1.22, the 3.5 family was present in three of twelve
consecutive listings and absent from the other nine, and `--model` tracked the listing rather
than the documentation (two of eight pinned runs succeeded). So a slug read back from
`agy models` is not a contract — **verify a pinned slug by invoking it, not by listing it.** The
failure is loud, which is why it is here rather than above; what it costs is a driver that
worked yesterday and a retry that fixes it, or, as with the 3.7 rows here, a driver whose every
call now fails.

Re-read 2026-10-30 on agy 1.4.10, run by the operator rather than an agent: the same six rows.

With no `--model`, an unpinned run's `init` event omits `model` entirely, so the default is not
readable back from the envelope (observed on 1.1.16, 1.1.18, 1.1.22 and 1.4.2); a pinned run's
`init` does name it. **Pin the model explicitly** — the default has rolled before, and agy
updates itself without being asked, so the version you tested against is not necessarily the
one that runs. It self-updated mid-pass on both 2026-08-22 and 2026-08-27.

**Where agy sits on the fast / default / strong ladder**, for a caller routing by complexity
hint the way `models.md` describes for the other two: `gemini-3.8-flash-low` is fast,
`gemini-3.8-flash-high` default. No Gemini pro row is served on 1.4.2, so the strong rung that
was `gemini-3.1-pro-high` is unfilled; whether `claude-opus-4-6-thinking` should take it has not
been established here.

## Verifying this file

```sh
agy update && agy --version    # self-updates on its own schedule; stamp after, not before
agy models                     # slugs, live — and see the stability note above
```

```sh
# is a piped prompt still dropped when -p supplies one too? (the surviving silent one)
echo "The secret word is LARCH." \
  | agy -p "What secret word came in on stdin? If none did, reply exactly NOSTDIN." \
        --model gemini-3.8-flash-low --output-format json
# expected: exit 0, status SUCCESS, response NOSTDIN — stdin dropped, stderr silent

# does a plain-text prompt on stdin still work with no -p at all?
echo "Reply with exactly: PLAIN_STDIN_OK" \
  | agy --model gemini-3.8-flash-low --output-format json
# expected: exit 0, status SUCCESS, response "PLAIN_STDIN_OK\n" — the pipe implies print mode.
# This one checks the Quick reference stdin cell, which has now been wrong twice with no
# canonical command exercising it. If it fails, that cell is what needs the edit.

# are the three argv mistakes still LOUD? Each must exit 2 with stdout empty and a
# diagnostic on stderr. The first two name the offending token; the third reports the mode
# conflict and has no token to name, so do not assert one. Any of them answering instead, or
# exiting 0, means it has gone silent again and the trap above is needed in full.
echo hi | agy --print --model gemini-3.8-flash-low --output-format json          # -p ate --model
agy -c "$(uuidgen)" -p "say OK" --model gemini-3.8-flash-low --output-format json </dev/null
echo '{"event":"user","message":{"role":"user","content":"say OK"}}' \
  | agy -p "x" --input-format stream-json --output-format stream-json --model gemini-3.8-flash-low
# Time the -c one against its own exit, not a pipeline's: it used to hang, and a `sleep`
# feeding the pipe will report timeout 124 as though it still does.

# does a bad event value still cost the turn quietly?
echo '{"event":"userr","message":{"role":"user","content":"say OK"}}' \
  | agy --input-format stream-json --output-format stream-json --model gemini-3.8-flash-low
# expected: exit 0, stdout carries the init event only, warning on stderr
# and with --output-format json instead: refused outright, before any turn runs

# does a denied tool still come back looking like a success? (the second silent one)
agy -p "Run the shell command: echo TOOLRAN. Then reply with its output." \
  --model gemini-3.8-flash-low --output-format json
# expected: exit 0, status SUCCESS, response "", NO .error key, .denied_actions naming
# "command", and on stderr "jetski: no output produced — a tool required the \"command\"
# permission…". In stream-json the status was sometimes CANCELED on 1.1.22 — sample it more
# than once before concluding either value is fixed. If .error comes back, or the exit code is
# 1, the envelope has gone loud and the trap above can go; if .denied_actions disappears, the
# success column of the output table loses its third check.
# Control: add --dangerously-skip-permissions and it must return SUCCESS with the tool output,
# in either flag position.

# control for the above — does .error still appear on a genuine failure?
agy -p "say OK" --model no-such-model-9x --output-format json
# expected: exit 1, status ERROR, .error naming the rejected slug, envelope on stdout,
# the same message on stderr. This is what a real agy failure looks like; the permission probe above is
# what makes "no .error" unusable as a success signal.
```

```sh
# the output envelope, to re-derive the field list above
agy -p hi --model gemini-3.8-flash-low --output-format json \
  | python3 -c "import json,sys; print(sorted(json.load(sys.stdin)))"
```
