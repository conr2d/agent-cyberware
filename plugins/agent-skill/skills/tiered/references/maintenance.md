# Maintaining this skill

Read this before editing `../SKILL.md`. It carries what the skill deliberately leaves out —
how each claim was established, which judgment calls were made, and what has been rejected.

## What this skill is, and is not

**Positioning: the pass, and the canonical statement of what it applies.** This skill is the
periodic sweep that finds where the tier model has stopped being true. It is not a linter, not
a style guide, and it decides nothing a maintainer could not decide by reading — what it
supplies is the *occasion* to read, which is the thing that does not happen on its own.

**It is also where the model itself lives.** A repository's `AGENTS.md` renders the tiers and
the tests for someone writing in that repository, localised to that repository's examples, and
those renderings are meant to differ from this file and from each other. What must not differ is
the model underneath — a tier appearing in one and not another, a test redefined in one place.
No gate can hold that: the wordings differ on purpose, so bytes cannot be compared — even in a
repository that holds this skill in its own tree, where a gate could open both files. Step 8 of the pass is the instrument, and it works because the
skill travels to each repository while a path does not.

**It audits a repository of skills, including its own.** Nothing here is exempt: this
`SKILL.md` carries a section inventory below like any other, and its own tiers are subject to
the tests it states.

**It is invoked by name, and does not detect its moment.** The moment worth running it is
between passes of other work. A session that is adding to a skill will not run a pass whose
likely finding is that the addition does not belong, so a trigger condition on "editing a
skill" would fire exactly when it is least welcome and be turned off.

The editorial rule this skill shares with the repository it ships in:

> **What rots does not go in the document; the command that prints it does.**

This skill has almost nothing with a shelf life in it — the tiers and the tests are structural.
The one thing that would rot is a measured token cost, which is why `../SKILL.md` states the
*shape* of the cost (tier 0 is unconditional, tier 1 is per invocation) and names no number.

## Section inventory

One row per `../SKILL.md` section, saying why this skill is its only carrier. **A new section
lands here in the same commit or the pre-commit refuses it** — that requirement is the moment
the admission tests actually get applied, which is the whole reason the gate exists. The gate
can only see that a row is present; whether it is true is what a pass reads for.

| section | why this skill is its only carrier |
|---|---|
| The tiers, and what each costs | The canonical statement of the model. A repository's `AGENTS.md` renders it for someone writing there, in that repository's own terms and examples; this is the one against which those renderings are checked, and the only one that travels to a repository holding no rendering at all. |
| The three admission tests | Four different formulations were in circulation, across several `AGENTS.md` and maintenance files, and a session applied whichever it had read. This is the one place they are unified and ordered. |
| The pass | The procedure has no other home — no script runs it, and the one gate that exists covers a single step of it. Steps are not self-explanatory, so a compressed list would be improvised. It also carries the only check on whether a host repository's rendering of the model still matches this one, which nothing mechanical can reach. |
| What this pass must not do | Each entry is a mistake a restructuring pass actively invites — most of all pruning the history, which looks like exactly the cleanup this skill is for. |
| Going further | The pointers to tiers 3 and 4, and the only route to them from an installed skill. |

## Update procedure

1. Run the pass on this skill first. A skill that audits shape and has drifted has no standing.
2. Only edit `../SKILL.md` if a tier, a test, or a step in the pass actually changed. A new
   *finding* from running the pass is a history entry, not a new section.
3. Any addition to `../SKILL.md` adds its row to the inventory above in the same commit.
4. **Never write a line number, here or anywhere.** Name the section. The pre-commit refuses a
   `:N`, a `file.md:N`, and an *N lines* claim in any tracked Markdown.
5. Append to `history.md`, newest last: what moved, what was established by running the pass,
   and what is reasoned. **Keep an entry to about forty lines.** One that will not fit is
   asking for its own reference file. Title it with what was decided or found, since the
   titles are the index.

Claims established by running the pass and claims reasoned from the sources are not the same
strength. Say which is which.

## History

In `history.md`. What governs an edit is in this file; open the history to find out why
something is the way it is.

## Open questions

- **Whether the pass should be run on a schedule or on a signal.** It is currently neither —
  it is run when someone remembers, which is the condition it was written to fix one level
  down. A candidate signal exists and is mechanical: the ratio of dated blocks to governing
  rules inside a `maintenance.md`, which is what the first pass measured to find its largest
  finding. Not built, because one measurement is not enough to set a threshold, and a
  threshold set wrong produces a gate that cries wolf and gets bypassed.
- **Whether the inventory gate should judge the row and not only its presence.** It cannot,
  by the same argument the citation checker records about itself — a row can be false in a way
  no regex sees. The open part is whether a *length* bound on the row would help, on the theory
  that a justification that will not fit in one line is usually not one. Untested. **Whether
  to keep the gate at all was raised by an independent review and settled on
  2026-10-20: kept.** The review's point stands: the gate counts rows and cannot see a section
  grow. But a row costs one line per section, and the gate's job was only ever the occasion.
  Nothing yet shows it costing more than that.
- **Whether tier 2 and the opt-in reference are really one tier.** ~~They are written as one
  row each in `../SKILL.md`'s table with the same number, because both are opened on demand and
  differ only in what opens them. If a repository ever needs to treat them differently — a
  different review cadence, say — they are two tiers and the table is wrong.~~ **Answered
  2026-10-20: one tier by cost, two by what they require of tier 0.** A trigger eval showed an
  ordinary reference is reached whenever the skill fires, while an opt-in one is reached only if
  the description names its subject, since that caller's question is the trigger. The cost is
  the same, so the number stays shared; the difference is stated where the opt-in reference is
  introduced. Kept so the next reader finds the answer and the evidence.
