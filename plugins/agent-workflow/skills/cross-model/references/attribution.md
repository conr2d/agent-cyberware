# Why the trailer is `Assisted-by:`, and why it carries a model

The exact strings are in `../SKILL.md`. This file is the reasoning behind them, which is worth
separating because the strings are what you copy and the reasoning is what you consult when a case
does not fit.

## The general rule cuts the other way, and the old exception no longer applies

History records decisions about the artefact, not the process that produced
them: which tool, model, plugin or agent did the work belongs in the session log, and a trailer for
it is metadata wearing the costume of rationale.

Until 2026-08-28 this skill used `Co-Authored-By`, and rested on the stated exception —
*attribution required by policy*. `Assisted-by:` cannot use that ground. Nothing requires it; it is
a convention this method adopts. So the exception has to be re-founded, and there is only one
honest footing left: **observability.** Which model authored which unit is a real question during a
model trial, and `git log` is the only place that answers it once the session logs are gone. That
is a narrower warrant than "policy requires it", and it should be spent on nothing else — it does
not license a trailer for the harness, the provider, or the effort level.

## Why not `Co-Authored-By`, and never `Signed-off-by`

The kernel's guidance for coding assistants (`Documentation/process/coding-assistants.rst`) states
that **AI agents must not add `Signed-off-by`**: that tag certifies the Developer Certificate of
Origin, and only a person can make that certification. The same page defines `Assisted-by:` for the
contribution itself and says nothing about `Co-developed-by` for an agent.

Both halves transfer here even though this repository runs no DCO. `Signed-off-by` is a claim a
model cannot make. `Co-Authored-By` is a claim about *authorship*, and in this workflow the author
agent implements a spec it did not choose against decisions it did not make — assistance is the
accurate word, and the accurate word is the one to use. The trailer got weaker and truer at once.

## The model is an id, not a display name

`Assisted-by: Claude:claude-opus-5-5`, not `Claude Opus 5.5`. The kernel's example is
`Claude:claude-3-opus`, and the id is what the orchestrator actually passed on the call, so it is
the thing that is *known* rather than transcribed. It also parses: one token, no spaces, and a
`git log --grep` that means something.

This reverses what this file said before 2026-08-28, which was to write the model as the model card
gives it. That rule existed to stop invented variants; an id stops them better, because there is
exactly one.

## What does not go in

The context window, the harness that drove the model, the service that served it, the effort level,
the sandbox mode. All of them are properties of *how the model was invoked*, which is the process
metadata the general rule excludes. `Claude Opus 5 (1M context)` appeared in twenty-one commits of
one repository before this was written down; a model served by one host and the same model served
by another are the same author.

The identity is the model. How it was invoked is session-log material.

## What this convention deleted

Two problems went with `Co-Authored-By`, and they are recorded because the effort spent on them was
real and a later reader may otherwise reintroduce the shape that caused them.

**Canonical identities.** The old form needed each tool's own published identity string — a name
and a `noreply@` address — so that tooling aggregating contributions across repositories would see
one author rather than several spellings. That required looking one up, and on 2026-08-27 a check
of one author tool came back empty in all four places it publishes anything: its attribution
setting, its config schema, its documentation, and the page describing the integration that commits
from CI. The answer then was to omit the trailer and put the authorship in the commit body, because
inventing an address is a claim the vendor never made. `Assisted-by:` needs no address, so there is
nothing to look up and nothing to invent.

**A task carrying two shapes.** *Reported* by the session that ran the second pairing on
2026-08-27, and not independently re-executed: a task whose author lane died partway through
was finished by a second tool, one of which published an identity and one of which did not, so
the same task's history carried a body sentence on two commits and a `Co-Authored-By` on a
third. Each rule was applied correctly and the result read as an inconsistency. Under one form for
every agent that case cannot arise.
