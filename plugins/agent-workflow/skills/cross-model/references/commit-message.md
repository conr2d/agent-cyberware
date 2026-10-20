# Commit messages and trailers

The shape of a sealed unit's record, and which lines earn their place in it.

## Commit message

```
<type>(<scope>): <intent line — why, not what>

<body: context and rationale>

Rejected: <alternative considered> | <reason rejected>
Not-tested: <known verification gap>
Lesson: <what would otherwise be learned twice>
Constraint: <active constraint, when the body does not already say it>
Reviewed: <the evidence, not the fact of review>
Scope-risk: <only when broad, and say what it touches>
Confidence: <only when medium or low, and say what is uncertain>
```

**The subject grammar is [Conventional Commits
1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).** That specification is
the carrier for the syntax; two things it does not give you are below, and both
are needed here.

**The type set, closed at five.** The specification mandates only `feat` and
`fix` and leaves the rest open (its rule 14); `docs`, `refactor` and `chore` come
from commitlint's Angular-derived config, not from the specification. Use those
five and nothing else. `build`, `test`, `ci` and `perf` are common elsewhere;
adopt one when your project has the thing it names, and not before — in a repository
with no build, test suite or CI they would have no referent.

**Which type applies, when the files are prose.** The specification's definitions
assume code, and where a project's product *is* documents — a skill, a spec, a
handbook — the first-time mistake is to read "all Markdown" as "all `docs`". Ask
what changes for someone who loads the thing:

| type | what changed |
|---|---|
| `feat` | a session must now do something it did not before |
| `fix` | a claim in a shipped file was false |
| `docs` | the record changed and no rule did |
| `refactor` | layout moved and no rule changed |
| `chore` | manifests, hooks, ignore files |

**Scope is required here**, though the specification makes it optional (its rule
4). It names the skill — `cross-model`, `non-interactive` — or `repo` for anything
above them, lower-case, matching `[a-z][a-z0-9-]*`. The file is in
`git show --stat`, which answers better and cannot be wrong. The specification's
breaking-change `!` is allowed where it applies. **Keep the subject to 72
characters**, which is what the gate enforces.

**Record the exception, not the field.** Every trailer is optional, and earns its
line on two tests: the diff cannot answer it, **and** no tracked document already
does. Prefer the one or two that would change a later decision over every line
that happens to apply.

**Wrap a trailer's continuation lines with two spaces**, and put the block last
with nothing after it. `git-interpret-trailers` needs both; a value that wraps
flush left makes git read the whole block as prose and return no trailers at all.
The defect hides where it is cheapest to miss: **a single-line trailer never
wraps**, so a project whose only trailer has ever been `Co-Authored-By:` can carry
the bug through its whole history without one message failing visibly. The symptom
is an empty column in `git log --format='%h %(trailers:only=true)'`, and that is
the check — not a reading of the messages, which look correct either way.

The reader to write for is someone — increasingly, some *agent* — reconstructing
a decision months later from `git log` alone. That reader can already see what
changed. What they cannot recover is what was considered and discarded, what was
never verified, and which constraint made the obvious alternative impossible.
Those are the trailers worth the keystrokes, and they are ordered above by how
often they turn out to be the thing someone needed.

The second test is the one that gets skipped, because a message written straight
after the work has every decision still in mind and all of them feel worth
keeping. Rationale that already lives in a tracked document — an ADR, a
maintenance record, the changed file's own prose — is findable where it will also
be kept current; copying it into the message creates a second copy that drifts
from the one people actually edit. Name that document if the connection is not
obvious from the diff, and leave the reasoning where it lives.

The two enum trailers were measured across the repositories that used them: 60
`Scope-risk: narrow` against 10 `moderate`, and 44 `Confidence: high` against
almost nothing else. **A field whose modal value is its uninformative one trains
readers to skip the whole block** — and the block is where `Not-tested:` lives.
So both are now exception-only and free text rather than enums, because
`Scope-risk: medium (rewrites the PTY command layer's state model)` carries what
`moderate` does not. For the enum version, `git show --stat` answers better and
cannot be wrong.

`Reviewed:` follows the same rule. "Reviewed: code review" is ritual;
"Reviewed: re-run in a virtualenv holding nothing but requirements.txt — gate
154/154" is evidence. Only the second is worth a line.

**History records decisions about the artefact, not the process that produced
them.** Which tool, plugin, harness or agent did the work belongs in the session
log; a trailer for it is metadata wearing the costume of rationale.

**The one exception is which model wrote the code.** What you need while writing
the message is the criterion, not the case for it: **the identity is the model;
how it was invoked is session-log material.** So the harness that drove it, the
service that served it, the effort level and the context window stay out — a
model served by one host and the same model served by another are the same
model, and none of those answers "which model". **No agent gets
`Signed-off-by:`, and none gets `Co-Authored-By:`.**

Why the exception is founded on observability rather than on policy, why
`Signed-off-by` is a claim a model cannot make, and what the convention replaced
are all in `attribution.md`, beside this file. The exact trailer strings are in
`../SKILL.md`, which is where the model is known accurately enough to name. This file used to argue all of it a second
time; two files arguing the same thing means neither is the one that gets
corrected.
