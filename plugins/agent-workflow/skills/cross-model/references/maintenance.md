# Maintaining this skill

Read this before editing `../SKILL.md`. It carries what the skill deliberately leaves out: how
each claim was established, which judgment calls were made and why, and what the workflow is
guarding against.

## What this skill is, and is not

**Positioning: the mechanism, with the principle it serves stated in `../SKILL.md`.** Separating
authoring from review, on different models where possible, is the principle; this skill is what
makes it structural.

The editorial rule:

> **What rots does not go in the document; the command that prints it does.**

Roles, the loop, the spec contract and the sealing rules are stable and belong in
`../SKILL.md`. Model ids, config keys and CLI flags rot within weeks and belong in
`codex-dispatch.md`, behind a command that prints the current value.

### Why the roles are split at all

The long form of the argument, kept here rather than in `../SKILL.md` because it explains the
design rather than instructing a session:

A single agent that writes code and then "reviews" its own work in the same context cannot
truly review it — it is anchored to its own choices and blind to its own assumptions. Splitting
authoring from review across two agents makes self-approval structurally impossible:

- The **author** sees only the spec, not the reviewer's judgement. It cannot rationalize; it
  must satisfy explicit criteria.
- The **reviewer** sees only the resulting diff against an independent understanding of the
  goal. It reads the code cold, runs the gates, and is the one accountable for sealing.

Here the separation is enforced by using two different agents and two different runtimes,
rather than by asking one agent to be disciplined.

### Failure modes this guards against

The design register. Each row is why some rule in `../SKILL.md` exists; a rule that stops
mapping to a row here is a rule that has lost its reason.

| Failure mode | What catches it |
|---|---|
| **Author improvisation** | the deterministic spec + the response rule + the cold diff review |
| **Self-approval / drift** | structurally impossible: different agents, and the reviewer runs the conformance gates |
| **Confidently-broken SDK usage** | verifying the API surface *before* writing the spec |
| **Scope creep / out-of-scope edits** | explicit guardrails in the spec + the reviewer checking the full file list of the diff |
| **Unreproducible "it worked on my machine"** | the reviewer re-runs the full verification battery itself, rather than trusting the author's self-report |
| **A wrong spec line obeyed and reported at once** | the *correct-and-report on error* half of the response rule — with only the stop-and-report half, an author can report the mistake accurately and still suppress around it, and the suppression outlives the fix. Upstream of both, the Done-when item asks for exact stale references rather than a common word as their proxy, so a check cannot be passed by rewriting correct prose |
| **An abandoned author run read as a finished unit** | the reviewer confirming the run completed before the cold read — a run can return without finishing, and a partial change can still pass the stage-4 gates |
| **Two of the spec's own lists in conflict** | deriving the file list from the Done-when as its own pass after it — the guardrail list and the checks are written at different moments and nothing else reconciles them, so the author receives the conflict and resolves it |
| **A file the spec's own change implies and no check names** | the second, structural derivation — callers of a changed signature, construction sites of a changed struct — and grepping the resulting paths rather than reading them |
| **A rejected option returning wearing a different vocabulary** | the cold diff read, and only it: a rejection on timing, ordering or lifetime is a claim about a mechanism, and the mechanism is in the code and in no document |
| **A branch reading as though every unit had a cold read** | the `Assisted-by:` count already says *which* units were paired; the body of a skipped unit says *why*, so the skip reads as a decision rather than as an omission |

## Section inventory

One row per `../SKILL.md` section, saying why this skill is its only carrier. **A new section
lands here in the same commit or the pre-commit refuses it.** The gate sees only that a row is
present; whether it is true is what an `agent-skill:tiered` pass reads for.

This file runs long against the sibling plugins' baseline, and that was considered rather
than overlooked — the rule is *the thinnest thing that prevents a first-time mistake*, not a
line count, and a baseline is not a budget. Three cuts have been weighed and rejected; each is
recorded in the row it defends. The un-headed positioning block above `Roles` carries no row and
states why different contexts are required and different models strengthen the separation.

| section | why this skill is its only carrier |
|---|---|
| Roles | What each agent may and may not do, and the response rule the author is held to. Nothing else states it, and an author that guesses instead of stopping is the failure the whole arrangement exists to prevent. |
| The per-unit loop | The seven stages and their order. **Compressing this to stage names was weighed and rejected**: the stages are not self-explanatory, and a loop whose steps must be looked up is a loop that gets improvised. |
| The author-spec contract | The seven required items, and the pass that derives the file list from the Done-when. This is the entire interface to a context-free author, so an omission here is not caught downstream by anything — it is implemented confidently and reads as an author judgement call in the diff. The derivation earns its place in the same file because the defect it prevents is a *conflict between* two of the items, which neither item can state about itself. |
| Verify the API surface before writing the spec, not after the diff | Names the highest-leverage stage and grades its evidence as two runs. It says re-verify external dependencies *before the spec*, which is the placement that matters when the reader is a context-free author. |
| Sealing policy | Who seals, and the exact trailer strings. **Moving the trailer shape to `attribution.md` was weighed and rejected**: a sealing session needs the strings in hand, and sending it to a reference at the moment of committing is the reliable way to get a guessed trailer. The *reasoning* did move; only the shape stayed. |
| When NOT to use this loop | The three cases where the round trip is pure overhead, the one exception to the first of them, and what a skipped loop owes the record. **Cutting it was weighed and rejected**: it is cheap, and it prevents the first-time mistake this skill most invites — running the loop on a two-line edit. The exception and the recording rule live here rather than beside the loop because both are about the *decision not to run it*, which is the only thing this section is read for. |
| Going further | The pointers to the reference files and the record. The only route to them from an installed skill. |

## Update procedure

1. Re-verify everything in `codex-dispatch.md` against the running CLI — the effort key, the
   flag names, the catalog command. That file is where this skill rots.
2. Any claim in `../SKILL.md` that has become a *mechanism* rather than a rule — because a
   gate, a hook, or another skill now enforces it — moves to `references/` or out entirely. A
   rule with an enforcer elsewhere is a description, and descriptions are what make a skill
   long enough to hide a real error.
3. Only edit `../SKILL.md` if a role, the loop, the spec contract, or a sealing rule actually
   changed. Any addition adds its row to the inventory above in the same commit. A
   description edit re-runs the trigger evals in the plugin's `evals/`:
   `claude plugin eval plugins/agent-workflow --trust-plugin`.
4. **Evidence lives here, not in `../SKILL.md`.** The skill carries the rule and at most one
   clause saying how strongly it is established. Run counts, unit counts, and what each run's
   findings were belong in `history.md`. A new run is a reason to update a number inside that
   clause, never a reason to grow the passage around it.
5. **Never write a line number, in this file or any other.** Name the section. Quote a past
   value in words. `./.githooks/check-citations.py --show` prints a skill's shape for reading,
   and the pre-commit hook refuses a `:N`, a `file.md:N`, or an *N lines* claim in any tracked
   Markdown, judged against a checkout of the index. There is no exemption for dated entries:
   one was tried, and a review found it covered exactly the region where the defect kept coming
   back.
6. Append to `history.md`, newest last: what moved, what was verified by execution, and what is
   reasoned from the sources rather than measured. **Keep an entry to about forty lines.** A
   finding that genuinely will not fit is asking for its own reference file. Title it with what
   was decided or found, since the titles are the index.

Claims verified by execution and claims carried from a document are not the same strength. Say
which is which. The effort-key error survived precisely because a claim that had never been
executed read as though it had been.

## Records that would otherwise be re-litigated

**The `--strict-config` trap stays in `codex-dispatch.md`** rather than being promoted, and step
2 above is what would otherwise re-decide it every pass. Its placement originally rested on two
grounds: only a dispatching session can hit it, and another skill carries it too. **Neither
ground was removed, and an earlier version of this record said the second was.** The
`agent-cli:non-interactive` skill still carries the trap and `codex-dispatch.md` still names it,
under *Model and effort*. What was removed on 2026-08-21 is the *entitlement to assume the
reader has it* — the file no longer routes anyone there for a command. The first ground survives
untouched and is sufficient on its own.

## Open questions

- **Whether the workflow generalizes as claimed.** `../SKILL.md` says the pattern works for any
  capable author paired with a different reviewer. **A second pairing was run, and it did not
  finish.** `opencode` driving `minimax-m3`, same reviewer, 2026-08-27: two units authored and
  sealed, then the provider died mid-turn on the third and the unit was re-dispatched to the
  first runtime. **The pattern held for the two units it covered** — scope, no commits, honest
  self-checks, the ambiguity branch firing correctly.

  What the failure adds is a constraint the loop does not state: **it assumes an author lane
  exists for as long as the task does.** A hosted provider's balance is an external dependency
  with no warning and no honest exit code, and the pattern only survived because a second harness
  happened to be installed and authenticated. Finding an *author runtime* that may be driven, and
  keeping it, is where the difficulty sits — not the pattern.
- **Whether "the spec is the entire interface" holds in a harness that injects repo files.**
  `../SKILL.md` says the author has no standing context and that whatever it needs must be in the
  spec. On the 2026-08-27 run the author never opened `AGENTS.md` or `CLAUDE.md` and never ran the
  repo's own task CLI those files mandate — but **every spec carried a line overriding them**, so
  what happens without that line was never observed, and a system-prompt injection would not show
  as a tool call in any case. **One unit dispatched without the override answers it.** If the
  author starts following repo instructions the spec never gave it, the skill's central claim
  needs qualifying for that runtime; if it does not, three specs carried ceremony they did not
  need.
- **Whether the spec contract needs a clause on Done-when the author cannot run.** The loop has
  the author self-check with build/test, and reads as though a Done-when can always be handed
  over. On the 2026-08-27 run one could not: the acceptance criterion required reading resolved
  values out of a real browser engine in two colour schemes, the browser was on the machine but
  not bound into the author's sandbox, and the reviewer owned that criterion outright. The
  question is placement — does confirming a Done-when is *executable in the author's environment*
  become an eighth contract item, a sharpening of item 6 or 7, or nothing, on the ground that a
  criterion the reviewer keeps is not a defect? **One more unit whose acceptance needs a tool the
  author's environment lacks decides it; two would settle which.**
- **Whether stage 6 should have a mechanical trigger.** ~~Whether it has ever fired.~~ **That half
  closed 2026-08-28** — it has, twice, both times on the operator's request and both times
  returning blocking defects the reviewer's own pass had missed; it is skipped deliberately for
  throughput, and the intended home is a pull-request flow where the pass hangs off the review
  rather than being paid for inline. The stage stays. What is still open is the trigger, and the
  candidate is not "high-risk": **the reviewer wrote part of the diff.** Stage 5 lets the reviewer
  fold trivial fixes directly, and at that moment the reviewer is an author and the separation the
  rest of this skill rests on is gone. Unlike "high-risk unit" the condition is mechanical — does
  the diff contain lines the reviewer wrote. One report and one session is thin evidence for a
  rule in a file paid for on every invocation, so it **waits for a third instance.**

## History

The dated record is in `history.md`, newest last.
