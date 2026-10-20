---
name: tiered
description: Auditing a repository of skills for tier drift — a passage sitting in a file more expensive than it needs, a SKILL.md section that never passed the admission tests, a maintenance file that has quietly become a history. Invoked by name, on a whole marketplace, between passes of other work rather than during one.
user-invocable: true
---

# Keeping a skill thin

A skill's files are read by different readers at different moments, and each moment has a
price. This is the periodic pass that puts every passage back in the tier it belongs to, and
refuses the ones that belong in none.

**Invoked by name, on a repository, between passes of other work.** Running it while adding
something to a skill is the wrong moment — the session that wants the addition is the least
able to judge it, and the judgement is the whole product here. Nothing in this skill fires on
a condition.

## The tiers, and what each costs

| tier | file | paid | holds |
|---|---|---|---|
| 0 | frontmatter `description` | **every session, invoked or not** | the trigger |
| 1 | `SKILL.md` | every invocation | what a session gets wrong without it |
| 2 | `references/<topic>.md` | when the session judges it needs it | templates, perishable specifics, what only some callers need |
| 2 | an *opt-in* reference | only when the caller names its subject | a whole subject the reader may not have — another tool, another environment |
| 3 | `references/maintenance.md` | before an edit | the rules that govern editing, and only those |
| 4 | `references/history.md` | when someone asks why | the dated record; entries appended, never edited |

**A tier's cost is how often it is read, not how long it is.** A history at nine hundred lines
costs a session nothing, because nothing reads it front to back. A maintenance file at three
hundred does cost, because *read this before editing* stops happening. A person tracing one
decision through the history pays too, which is why each entry's title states that decision
and a grep over the titles is the index. Judge each file against its own tier and never
against one global length.

**Tier 0 is the only thing paid unconditionally.** Carrying a skill nobody invokes costs its
description and nothing else — so a marketplace is not made cheaper by holding fewer skills,
it is made cheaper by descriptions that name a trigger instead of summarising a body.

**The opt-in reference is the cheapest way to add coverage.** A whole subject reachable only
by callers who name it costs one line in `SKILL.md` and nothing on any other invocation. Reach
for it before concluding that something new has to grow the always-paid file. **Its subject
also needs a word in the description**: a caller who names it reaches that line only if the
skill fires at all, and one that does not name it in the description mostly does not.

**The usual failure is one shape:** a lower tier's content accumulating in a higher one. It is
invisible per commit and obvious per quarter, which is why this is a pass and not a rule.

## The three admission tests

Apply in order. A passage failing one moves down a tier; it does not get argued back up.

1. **Only carrier.** Is this skill the only thing that carries it? A rule already enforced by
   a gate, a hook, a commit template, or a reviewer in another context is the document
   *describing* a mechanism rather than being one. Name the other enforcer, or keep the rule.
   **An enforcer counts only if it speaks at the mistake**: a tool that refuses loudly and at
   once, naming the cause, carries its own warning, and a trap entry for it buys one saved
   retry on every invocation. A failure that is silent, or that surfaces only after the cost
   is paid, has no other carrier, and that stays.
2. **Reachability.** Can a reader following this document reach the situation at all? A trap
   behind a precondition the reader does not have is paid on every invocation and met by
   nobody. That is an opt-in reference, or it is nothing.
3. **Rot.** Does it have a shelf life — a version, a slug, a flag name, a measured number?
   Then the document names the command that prints it, not the value. A dated measurement is a
   record, not a rule.

What survives all three stays where it is.

## The pass

One repository at a time.

1. **Measure.** Per skill, the size of every tier and the section sizes inside `SKILL.md`.
   Where the repository has a shape printer, run it rather than writing the numbers down —
   a number written into prose rots on the next edit above it.
2. **Sweep tier 3 for tier 4.** Every dated block in `maintenance.md` — a verification record,
   a measurement table, an incident — is history wearing a rule's clothes. It moves. The
   exception is a block the update procedure itself sends a reader to: that becomes its own
   tier-2 reference, and the procedure points at the file instead of holding it.
3. **Sweep tier 1 for tier 2.** The three tests against each `SKILL.md` section.
4. **Sweep tier 2 for tier 1.** The converse, and the one that gets skipped: a reference a
   session gets something wrong without has become load-bearing and should be promoted.
5. **Check the section inventory.** Every `SKILL.md` section has one row in `maintenance.md`
   saying why this skill is its only carrier. A missing row is a section that entered without
   the test — write the row, or cut the section. Where a gate enforces this, it enforces that
   the row exists and can say nothing about whether it is true; step 5 is the part that reads.
6. **Sweep the open questions.** Each against the current `SKILL.md`. One whose stated
   condition has been met is closed with the date and what decided it, struck through rather
   than deleted, so the next reader finds the answer instead of re-deriving the question.
7. **Read tier 0, then measure it.** Each `description`: does it name *when to invoke*, or does
   it summarise what is inside? A summary is paid always-on and read by nobody who is deciding
   anything. Reading cannot tell whether it fires: where the repository has trigger evals, run
   them, one case per subject the description must catch, opt-in subjects included, and one
   per near-miss it must not.
8. **Check the host repository's own rendering.** A repository's `AGENTS.md` states these
   tiers and tests for someone writing in that repository, with its own examples; this file
   states them for whoever runs the pass. **The renderings are meant to differ — the model is
   not.** Read the host's against this one for a tier or a test that is present in one and
   absent from the other, or defined differently. Nothing can gate this: the wordings differ
   legitimately, so a byte comparison is the wrong instrument. **Reachability is not the reason
   and must not be mistaken for it** — a repository holding this skill in its own tree can open
   both files and still has nothing a gate could compare. **This file is canonical for the
   model; the pass travelling to each repository is what closes the gap**, which is why the
   check is a step and not a hook.
9. **Report, then let a different context seal.** A pass that finds nothing is a result — say
   so rather than finding something.

## What this pass must not do

- **Never prune or compress `history.md`.** The rules that survive were derived from those
  entries, and a summary of a correction is not evidence of one. The titles are the summary
  layer, and it costs nothing to keep.
- **Never treat a line count as the verdict.** It is the signal to look. The rule is the
  thinnest thing that prevents a first-time mistake.
- **Never widen a `description` to make a skill fire more often.** A skill that fires on
  everything is one that gets turned off, and then it is worth less than nothing. Naming a
  subject the skill already carries is not widening; the near-miss cases are what tell the two
  apart.
- **Never delete an open question that turned out to be answered.** Close it in place.
- **Never move a passage from a tracked file to an untracked one.** A recommendation whose
  counter-evidence the reader cannot open reads as support.

## Going further

- Editing this skill → `references/maintenance.md`; the dated record → `references/history.md`
