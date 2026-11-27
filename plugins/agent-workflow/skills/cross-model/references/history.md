# History

Newest last. Entry titles state what was decided or found; they are the index.

### 2026-10-20 — first public version, as `agent-workflow:cross-model`

Renamed from `engineering:pair-workflow` in an earlier private marketplace whose record is not
published. Skill identifiers and plugin names now use the public marketplace names.
The reasons for separating contexts and models, the sealed-unit definition and the review-fix
rule are inline; commit-message guidance is local, with the ADR section dropped.
Private history pointers and the separate supporting skill were dropped; dated measurements stay.
Rules that survive were derived from that unpublished record; their reasoning is restated in
maintenance.md where a reader needs it.

### 2026-10-28 — a common word is not a proxy for a stale reference

Twice in one week a spec's Done-when banned a common word as a proxy for "no stale reference
remains", and both times the author satisfied the literal grep by rewriting otherwise-correct
prose: a sentence about the hook not running on `git merge`, and a section heading and
description using *authoring* that became *authorship*. Every check passed; the reviewer caught
both only by reading the diff line by line. Whether either author should have reported the
check as a spec error under correct-and-report is not settled from the reports alone. The rule
went into the Done-when item of the spec contract because written there it prevents the defect
before dispatch, where the other defences only catch it after. A review of the first wording
("identifiers, never ordinary words") narrowed it: a requirement can legitimately be about
wording, and an obsolete identifier can legitimately remain in a historical note.
Reasoned from two observed cases, not measured.

### 2026-11-18 — a settled design the reviewer cannot fully check steps the author tier up

From an operator-approved handoff by another session. **Operator-reported, not executed here**:
across repositories in active use, a top-tier reviewer's *design* errors were caught more than
once by the author lane when the author was a strong model from another family, and would have
passed the loop's gates otherwise. The handoff's mechanism said the response rule never fires on
a design error. The clause says instead that the rule reaches one only through an author that
sees the collision, so the tier plausibly bears on whether the rule gets a chance. Which half of the rule
then applies is left to *Roles*: a second review found that saying "a report, not a correction"
in this file reinterpreted the response rule from a tier it does not live in. That review also
found the comparative claim stated as fact; the clause now marks it reasoned, with no
smaller-tier comparison behind it. It is scoped to a design the reviewer has *settled* but cannot fully check, since an
unsettled one is outside the loop. Placed as one clause under *Model and effort* in
`codex-dispatch.md`, beside the rule it refines; `SKILL.md` is unchanged, so no inventory row.
The failure register was not extended either, because its rows map `SKILL.md` rules.

What would firm it up is run particulars: which unit, what the design error was, and which
author lane reported it. What would remove it is particulars showing that the defects were
really ambiguities, which the response rule requires every author to report.

Per-vendor portfolio and quota placement, raised in the same handoff, was not admitted: it rots
within weeks and is operator-specific, which is the editorial rule's exact case. It was routed
out of this repository.

In the same pass, step 1's two probes in `codex-dispatch.md` were re-run on codex-cli 0.169.1
and their stamps were extended rather than replaced: the key probe printed the same two lines as
before, and the cache reader the same shape, `fetched_at` and then one line per model, whose
values are expected to move. The key probe establishes that and no more: it prints `accepted`
for any failure without the unknown-field message. The rest of the file was not re-verified.

### 2026-11-18 — the agent name in `Assisted-by:` has one spelling per repository

Verified by execution on git 2.43.0: `git log main -F --grep 'Assisted-by: <name>:grok-4.7-build'`,
with `<name>` replaced by each spelling in turn, returns two commits for `Grok` and two others
for `grok`; with `-i`, all four. So a case-sensitive search finds only part of one lane.

**The first draft gave the wrong reason**, and a second review caught it. It said the split
weakens the skipped-loop row of the failure register. It does not: that row reads the number of
`Assisted-by:` lines on *one* commit, which no spelling changes. What the split breaks is the
warrant `attribution.md` gives for the trailer at all — observability, from `git log` alone, of
which units a model contributed to; the line records contribution, reviewer included, not role.
The paragraph there now says that.

The rule's shape is a half-clause in *Sealing policy* in `SKILL.md`, "in the one spelling the
repository keeps for it", with the reasoning in `attribution.md`. The first draft kept it out of
`SKILL.md` on cost. The second review answered that a sealing session reads the trailer shape
there and nowhere else, which is the ground the section inventory already gives for keeping the
strings in `SKILL.md`; the operator chose the half-clause. A third review found its first
wording, "spelled as the repository already spells it", gave two valid answers in a repository
that already holds both, as this one does; `attribution.md` now says to choose one. No new
section, so no new inventory row. The `attribution.md` paragraph names the pair as an example and
carries no count, since that file ships to installing projects, where "this repository" would be
false.

A commit-msg check was not written. No casing convention holds across agents (`opencode:` is
lowercase as the tool spells itself), so a gate needs either a comparison against names already
in history or a maintained list of canonical names; either is the operator's call. The four
existing commits are left as they are, and the history is not rewritten.

### 2026-11-27 — the orchestrator is a role, not a vendor

An operator setting up another vendor's agent as orchestrator asked whether this skill assumes
Claude in that seat. It does not: the roles were already written without a vendor, and the one
Claude string in `SKILL.md` is a trailer example. What did read as vendor-bound were the two
dispatch pointers, in the opening and in *Going further*, which named only `codex-dispatch.md`.
The opening paragraph now says no vendor is assumed for either role and that whichever agent
orchestrates holds the reviewer's duties; both pointers now send the other CLIs that
`agent-cli:non-interactive` covers to that skill. A review caught the first draft saying "any
other CLI", which that skill does not cover, and missing the second pointer.

Splitting the orchestrator from the reviewer and sealer was considered and not done, on the
operator's choice: the reviewer is the one holding the full context, which is the reason the
roles are joined. A project that wants review on a particular model puts that model in the
orchestrator's seat. No new section, so no new inventory row.

### 2026-11-27 — an author lane is a set of requirements, and reviews are evidence

An operator moving orchestration between vendors asked whether a session could derive a
non-Codex dispatch from this skill. The requirements were embedded in the Codex flags in
`codex-dispatch.md`. They now stand alone in `author-lane.md`, with a derivation procedure
that ends in running the derived form and keeping it with the run date and CLI version. The
first author run stopped before editing because the draft asserted that the Codex calls meet
every requirement. The table now records the shortfalls. The Codex column was based on a reading
of `codex-dispatch.md` without rerunning the calls, and an independent review then corrected
several cells against that file. The CLI-specific columns that would make derivation mechanical
belong in `agent-cli:non-interactive` as measurements and were left for a separate unit there.

The same operator read the joined orchestrator/reviewer role as possibly forbidding reviews
outside the orchestrator's session. *Roles* required an independent review for high-risk
units and left who judges independent findings unstated. It now says reviews may be added as
the unit warrants and that the orchestrator judges the findings and is accountable for what
lands. `Reviewed:` now names each review and what was done with its findings. No new section,
so no new inventory row.
