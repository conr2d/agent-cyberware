# Contributing

Issues and pull requests are welcome. Keep one intent per pull request. For a change to a
skill, read its `references/maintenance.md` first — it holds the rules for editing that skill.
No plugin installation is needed to contribute; the procedures are files in this tree.

## Setup

Run once per clone, before the first commit:

```sh
git config core.hooksPath .githooks
ln -s AGENTS.md CLAUDE.md
```

The hooks refuse staged private context and runtime state, Markdown symlinks and perishable
citations, malformed skill frontmatter, missing or stale section-inventory rows, and invalid
commit subjects or trailer blocks; see [AGENTS.md](AGENTS.md) for detail.

## Commit messages

Use a [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) subject:

```
<type>(<scope>): <intent>
```

The type set is closed at five. For humans and agents alike, ask what changed for someone who
loads the thing:

| type | what changed |
|---|---|
| `feat` | a session must now do something it did not before |
| `fix` | a claim in a shipped file was false |
| `docs` | the record changed and no rule did |
| `refactor` | layout moved and no rule changed |
| `chore` | manifests, hooks, ignore files |

This repository keeps exactly these five, CI included: a change to `.github/` is `chore`.
The commit-msg hook and CI refuse any other type.

Scope is required: the skill name (`non-interactive`, `cross-model`, `tiered`) or `repo` for
work above them. Keep it lower-case, matching `[a-z][a-z0-9-]*`. The breaking-change `!` is
allowed where it applies. The subject is at most 72 characters; the body says why.

Trailers are all optional, and each earns its line on two tests: **the diff cannot answer it,
and no tracked document already does**. Prefer the one or two that would change a later
decision over every line that happens to apply:

- `Rejected:` — alternative considered and why it was rejected.
- `Not-tested:` — a known verification gap.
- `Lesson:` — what would otherwise be learned twice.
- `Constraint:` — an active constraint the body does not already state.
- `Reviewed:` — the evidence, not the fact of review.
- `Scope-risk:` — only when broad; say what it touches.
- `Confidence:` — only when medium or low; say what is uncertain.
- `Assisted-by:` — AI assistance, in the form below.

Indent continuation lines two spaces, and put the trailer block last, with nothing after it,
so `git interpret-trailers` can read it.

The full version, with its reasoning, is
`plugins/agent-workflow/skills/cross-model/references/commit-message.md`.

## AI assistance

AI assistance is welcome and expected to be disclosed. Use one `Assisted-by: AGENT:MODEL` line
per agent that contributed, naming the model id it actually ran as, and nothing else:

```
Assisted-by: Claude:claude-opus-5-5
```

No `Co-Authored-By:` or `Signed-off-by:` for an agent. The human submitting is responsible for
every line, whoever wrote it. The form originates in the Linux kernel's
[`Documentation/process/coding-assistants.rst`](https://github.com/torvalds/linux/blob/master/Documentation/process/coding-assistants.rst);
this repository narrows it to the agent and its actual model id.

## Claims

Measured claims name the command and the version they were run against, with a date. A claim
read from documentation or `--help` says so; "reasoned" and "measured" are kept apart. A
description change re-runs the plugin's trigger evals:

```sh
claude plugin eval plugins/<plugin> --trust-plugin
```

## License of contributions

Contributions are accepted under the repository's licences: documents under CC BY 4.0
([LICENSE](LICENSE)), scripts under MIT ([LICENSE-CODE](LICENSE-CODE)).
