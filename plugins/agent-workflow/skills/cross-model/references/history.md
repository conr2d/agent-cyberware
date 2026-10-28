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
