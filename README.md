# agent-cyberware

> *"A rudimentary implant."*
> — Adam Smasher, *Cyberpunk: Edgerunners*

Cyberware for coding agents — small parts, each doing one thing, installed one at a time.
Nothing here is clever, and everything that can be measured was run rather than read off
`--help`.

| plugin | skill | what it is for |
|---|---|---|
| `agent-cli` | `non-interactive` | Driving Claude Code or Codex from a script, CI job or another agent without the failures that do not look like failures. opencode, hermes, grok and agy are opt-in references, opened only when you name them. |
| `agent-workflow` | `cross-model` | Separating the spec, the authoring and the review into different contexts — on different models where you can — so one model's blind spots do not pass every stage. |
| `agent-skill` | `tiered` | The periodic pass that keeps a skill thin: every passage in the tier its readers pay for. |

## The premise

Agents produce more code than one person can meaningfully read. The scarce resource stops being
the writing and becomes the *judgment* — deciding what is worth building, and catching work that
is technically correct but wrong. Nearly everything here follows from that: small sealed units,
acceptance criteria a machine can check, review by a context that did not author the code, and a
record of every deviation so the same argument is not had twice.

None of it assumes the agent is good. It assumes the agent is fast and occasionally confidently
wrong, which is the harder problem.

## Installing

```sh
claude plugin marketplace add conr2d/agent-cyberware
claude plugin install agent-cli@agent-cyberware        # --scope user | project | local
claude plugin install agent-workflow@agent-cyberware
claude plugin install agent-skill@agent-cyberware
claude plugin details agent-cli                         # inventory + projected token cost
```

Install only what you use — each plugin stands alone. `agent-workflow:cross-model` dispatches
Codex with commands written out in full; for other author CLIs it leans on
`agent-cli:non-interactive`, so install both if you use them.

`agent-cli:non-interactive` and `agent-workflow:cross-model` trigger on concrete conditions:
spawning a CLI non-interactively; writing an author-spec, dispatching, reviewing or sealing.
`agent-skill:tiered` is invoked by name, on a repository, between passes of other work. Refer
to them by full identifier in your own instructions: two plugins from different marketplaces
can share a skill name, and a bare name then resolves to only one of them.

## What is in a skill

Each skill's `references/` holds what is consulted rather than carried, plus a `maintenance.md`
with the editorial rules and the update procedure, and a `history.md` holding the dated record
of what was decided or found. Read the maintenance file before editing a skill; it distinguishes
claims established by execution from those that are reasoned rather than measured.

## Status

In daily use by its author, written for and tested with Claude Code. The skills change when
something is learned, recorded in each skill's `references/history.md` and in the commit
history, not in a changelog.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Documents are under [CC BY 4.0](LICENSE); the scripts in `.githooks/` are under
[MIT](LICENSE-CODE).
