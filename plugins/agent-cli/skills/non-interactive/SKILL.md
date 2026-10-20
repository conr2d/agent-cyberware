---
name: non-interactive
description: Canonical non-interactive (headless) invocation patterns and silent-failure traps for the Claude Code and Codex CLIs, with opt-in references for opencode, hermes, grok, and Antigravity (agy) where its terms allow a driver. Use whenever spawning any of these non-interactively — Bash tool, scripts, CI, or any subprocess driver.
user-invocable: true
---

# Driving AI CLIs non-interactively

The minimum you need to drive Claude Code or Codex from a subprocess without getting
it wrong. Everything here was executed, not read off `--help`.
**Last verified: 2026-10-19** (Claude Code 2.1.303, Codex 0.163.0).

When the CLI disagrees with this file, the CLI is right — see `references/verify.md`.

## Quick reference

| | Prompt | Stdin | JSON out | Resume | Auth |
|---|---|---|---|---|---|
| **Claude** | `-p` (argv) | `-p` w/o arg + stdin ✅ | `--output-format json` | `--session-id <uuid>` then `--resume <id>` | `ANTHROPIC_API_KEY`, else subscription OAuth |
| **Codex** | `exec` (argv) or `exec -` | `exec -` ✅ | `--json` (JSONL) | `exec resume <id\|name> -` | `OPENAI_API_KEY`, else subscription OAuth |

## Canonical commands

```bash
# Prompts go on stdin: one argv string is capped near 128KB on Linux (MAX_ARG_STRLEN).
# Claude — pin your own session id if you will resume
claude --session-id "$(uuidgen)" -p --output-format json --model sonnet < prompt.txt
claude --resume "<sessionId>"    -p --output-format json --model sonnet < followup.txt

# Codex — --skip-git-repo-check is required outside a git repo. Resume is a subcommand,
# not a flag, and -p inside exec means --profile.
codex exec - --model gpt-5.6-terra --json --skip-git-repo-check --strict-config \
  -c approval_policy=never -c model_reasoning_effort=medium -o out.txt < prompt.txt
codex exec resume "<threadId>" - --json --skip-git-repo-check --strict-config < followup.txt
```

## Reading the output

| | text | session id | success |
|---|---|---|---|
| Claude (`json`) | `.result` | `.session_id` | `.is_error == false && .subtype == "success"` |
| Codex (`--json` JSONL) | `item.completed` where `item.type=="agent_message"` → `.item.text`, or use `-o <file>` | `thread.started` → `.thread_id` | `turn.completed` arrives (carries `.usage`) |

Claude's envelope also carries `permission_denials` (check it when a tool-using run
underdelivers), `total_cost_usd`, `stop_reason`, and `terminal_reason`. Neither `.result` nor
Codex's `item.text` carries a trailing newline.

**Only Claude's envelope names the model.** Claude carries `modelUsage`, keyed by the resolved
id, which is also how an alias is mapped to one. Codex emits no model on any `--json` event and
`-o` receives the final message alone; it names `model:` and `reasoning effort:` on **stderr**,
before the turn, and only in the plain `exec` form. A driver that has to record or check which
model actually ran must capture Codex's stderr.

## Traps — none of these look like failures to a driver

**Codex ignores an unknown `-c` key instead of failing.** The effort key is
`model_reasoning_effort`, *not* `reasoning_effort` — the latter is accepted at the command
line, silently dropped, and the run proceeds at default effort. **Pass `--strict-config` in
every driver**; it turns a typo'd or renamed key into an exit-1 error:

```
$ codex exec - --strict-config -c reasoning_effort=low
Error loading config.toml: unknown configuration field `reasoning_effort` in -c/--config override
```

**Codex refuses to run in a directory it does not trust, with empty stdout.** Exit 1, message
on stderr only (`Not inside a trusted directory and --skip-git-repo-check was not
specified.`) — a driver that parses stdout sees "no output", not an error. A git repository
passes by default, so in practice this fires on scratch directories: pass
`--skip-git-repo-check` there, and check the exit code rather than the output.

**Claude may hand back a session id it did not persist.** Resuming with the id echoed from
a `-p` run can fail with `No conversation found`. Generate a UUID up front, pass
`--session-id <uuid>` on the first call, and trust your own id. (`--fork-session` is the
sanctioned way to branch instead.)

## Going further

- Choosing a model, an effort level, or a fast/default/strong tier → `references/models.md`
- Suspect anything above is stale, or you want the current values yourself → `references/verify.md`
- Dispatching any of these into an outer sandbox (bwrap, a container) → `references/sandboxed.md`

**Additional support, on request only.** Four files, each opened by a caller who has named
its subject and assumed by nothing here. opencode (`opencode run`, third-party models under
your own API key) is in `references/opencode.md`; hermes (local, quota is whatever provider you
point it at) is in `references/hermes.md`, which opens with what has to be true before it may be
driven — read that before dispatching it; grok (`grok -p`, a grok.com session or `XAI_API_KEY`)
is in `references/grok.md`. All three are the lane for when a subscription window rather than a
bug is what stopped you. agy (Antigravity) is in `references/agy.md`, out of the guide on terms
grounds rather than for lack of coverage: another vendor's agent spawning it is the case they
reach, so open it only when the driver is agy itself or a person's own script.
