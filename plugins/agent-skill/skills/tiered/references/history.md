# History

Newest last. Entry titles state what was decided or found; they are the index.

### 2026-10-20 — first public version, as `agent-skill:tiered`

Renamed from `authoring:skill-shape` in an earlier private marketplace whose record is not published.
The public skill is `agent-skill:tiered`; its tiers, admission tests, and pass are retained.
Repository-specific history was removed from the maintenance guidance; the host comparison remains a step.
Rules that survive were derived from that unpublished record; their reasoning is restated in
`maintenance.md` where a reader needs it.

### 2026-11-20 — second pass: three wording fixes, one model mismatch left to the operator

Run on the whole marketplace, all three skills, on a clean `main`. Established by running:
`check-citations.py --show`, the three gates (all pass), both plugins' trigger evals with
`--ablation none` (agent-cli twelve of twelve cases, agent-workflow nine of nine, three runs
each, opt-in and near-miss cases included), and `gh issue view` on the Cline blocker (still
open). Everything else is reasoned from reading.

Moved or corrected, each its own commit:

- `non-interactive` maintenance called the opt-in files "a fourth tier". The model gives them
  tier 2's number, as the open question below closed on 2026-10-20. Reworded.
- `cross-model` and this skill's maintenance both said the pre-commit refuses an *N lines*
  claim "in any tracked Markdown". The gate sees one only where the paragraph names a subject,
  as `AGENTS.md` says. Both now say so.

Found and **not** changed, because each is the operator's call:

- **Step 8: test 3 is defined differently in the host's rendering.** `AGENTS.md` splits
  practice skills from measurement skills and lets a measurement skill carry values if it names
  the printing command and stamps the run. Test 3 here says to name the command *instead of*
  the value. `non-interactive` relies on the host's version (a version stamp and a model id in
  its canonical command). Either this file gains the distinction, which changes a test, or the
  host's rendering is stale.
- `cross-model`'s *Sealing policy* example names `Codex:gpt-6.1-sol`, one generation behind the
  sibling skill's example, and nothing in its update procedure moves it the way
  `non-interactive` update step 4 does.
- `non-interactive` update step 6, the quarterly re-run of `research.md`, was last done in late
  August, so it is due. That is a maintenance pass, not this one.
- This skill has no trigger evals. Its description says it is invoked by name, so firing
  matters less than not firing; a near-miss case or two (writing a new skill, reviewing one
  skill's prose) would test that.

No `maintenance.md` block was moved to a history. `non-interactive`'s holds far more dates than
the other two, about one line in eight against a handful, which is the signal in the first open
question. Read, each date there is provenance for a rule that is still in force, not a record,
so the ratio flagged it and the reading cleared it. That is a second data point for that
question, and it argues against using the ratio alone as a threshold. Its *Going further*
inventory row runs to a paragraph, which bears on the row-length question too.
No open question in any skill had its stated condition met.

### 2026-11-20 — test 3 splits practice skills from measurement skills

The second pass found test 3 defined differently in `AGENTS.md`, and the operator chose to bring
this file to the host's definition rather than the reverse. Applied as this file read before,
test 3 condemned what a measurement skill is made of: `non-interactive` carries a version stamp
and a runnable model id in its canonical command, and stripping them would make every caller run
a probe before the first call, which is thicker, not thinner. The host's rendering already said a
measurement skill satisfies the editorial rule the other way, naming the printing command and
stamping the run, and that skill's update procedure is the mechanism that keeps the stamp honest.

What changed is test 3's second sentence. The tier table, tests 1 and 2, and the pass are
unchanged, so `AGENTS.md` needed no edit. Reasoned from the two files and the skill that relies
on the split; nothing was executed beyond the gates.
