# Maintaining this skill

Read this before editing `../SKILL.md`. It carries what the guide deliberately leaves out:
how each claim was established, which judgment calls were made and why, and what has
already been tried and rejected.

## What this skill is, and is not

**Positioning: the thinnest guide for driving a non-interactive agent session.** Not a
tool, not a model reference, not a competitor to any wrapper. The value is that someone can
read it once and not get it wrong the first time.

That positioning is load-bearing, because the one real defect this file has ever had came
from drifting away from it: an effort-key claim read from `--help` was written as though it
had been executed, and the wrong key was silently ignored. The editorial rule that prevents
a repeat:

> **What rots does not go in the document; the command that prints it does.**

Shapes and traps are stable and belong in `../SKILL.md`. Facts (versions, slugs, accepted
config keys) belong behind a command in `verify.md`. Recommendations that are useful but
perishable go in `models.md` with a date on them.

**A fourth tier exists as of 2026-08-27: opt-in files.** `opencode.md`, `hermes.md`,
`grok.md`, `sandboxed.md` and `agy.md` are each referenced from `../SKILL.md` by a single line
and opened only when the caller has named the thing they cover. Everything about them — surface,
traps, config, probes — lives in the one file, so a standard pass neither runs their probes nor
is made wrong by them going stale.

Two kinds qualify, and the test is the same in both: **who can reach it.**

- *Another CLI*, when it solves a problem the guide's own cannot. opencode's is that its quota
  is the caller's own API key, so it survives a Codex window the other lanes do not. hermes
  joined on the same ground 2026-09-03: local, and its quota is whatever provider it is pointed
  at, which is what makes a promotional offer on some third CLI worth wiring up at all.
- *A precondition the guide's reader does not have.* `sandboxed.md` needs an outer confinement
  layer; on a bare machine, following the canonical commands, none of it is reachable.
  `agy.md` needs a caller Antigravity's terms permit, which the reader of this skill usually
  is not.

The second kind was added 2026-08-28 after two genuinely silent Codex traps arrived aimed at
`../SKILL.md` and would have grown it 24 % for an audience that has to build a bwrap carve-out
first. The reachability corollary already settled that; what was missing was somewhere else for
them to go. Now there is. The bar for *promoting* any of these files' contents into
`../SKILL.md` is unchanged, and nothing has met it. hermes is the clearest case of the bar
holding: its traps are as reachable as any in the guide, and what keeps it out is that it has
no JSON envelope, so nothing it teaches can be stated in the guide's own output table.
The envelope is not sufficient on its own. grok has one and stayed out, because a driver
following this guide cannot reach its traps, measured 2026-09-25. **Promotion is the operator's
call about who the reader is**: on 2026-10-19 grok went in at the operator's direction and came
back out the same day, when the cost turned out to be about a third of the guide, paid on every invocation
for one CLI.

**grok has no confined author command, and the absence is deliberate.** A write without
`--yolo` comes back `cancelled` at exit 0, so the unattended state is that flag rather than
the start hermes has. No carve-out around the flag was measured. `opencode.md` carries a lane
because its defaults already do the work and its confinement was measured under srt; the hermes
lane is withdrawn until measured under srt. Copying a lane onto grok would document a procedure
this file has not executed. Recorded so the gap is not read as an omission and
filled in. An unknown `--disallowed-tools` name is ignored silently and stays out of
`grok.md` until a command there passes the flag — a confined lane would be that command.

**agy widened that second kind on 2026-08-31 rather than adding a third.** It had been one of
the guide's CLIs since the skill was written. What removed it is the same reachability test,
applied to the *caller* instead of the environment: Antigravity's terms turn on who is driving,
and an agent of another vendor spawning `agy` is the case they reach. The reader who pays for
`../SKILL.md` on every invocation is a session of exactly such an agent — **this skill is
installed in the one product that may not do what the page described.** A caller the terms do
permit, agy driving agy or a person's own script, is a precondition that reader lacks, which is
the second kind as already stated once *environment* is read as *precondition*. Nothing was
deleted: the surface, the four traps, the model notes and every probe moved intact, and the
terms judgement sits at the top of the file with its grade, because it is read from a published
agreement rather than executed and can change without notice.

Corollary: resist re-adding flag catalogs. `--bare`, `--ephemeral`, `--max-budget-usd`,
streaming-input mode and friends were all documented at one point and all removed — that is
`--help`'s job, and carrying them made the guide long enough to hide a real error.

The boundary that replaced the blanket rule (2026-08-20): the flag stays out, and its
*silent* failure earns a trap entry **only if a driver following this guide can reach it**.
`--help` documents what a flag does and never what it does wrong, so that half is nobody
else's job — but a reader who never learns a flag from here cannot be trapped by it either,
and pays for the warning on every invocation regardless. Stream-json input passes both
tests: the guide's multi-turn canonical command is what sends a caller there, so its failure
modes are ours. (That example is agy's, and moved to `agy.md` with it on 2026-08-31 — the
test is unchanged and the file it applies in is the one that hands the reader the command.)
`--bare` passes the first and fails the second, which is why it went back out the same day
it went in. And a trap entry that cannot name an exit code, a stream, and a field the caller
would have believed is not one.

## Section inventory

One row per `../SKILL.md` section, saying why this skill is its only carrier. **A new section
lands here in the same commit or the pre-commit refuses it** — that requirement is the moment
the admission test gets applied, rather than a quarter later by whoever remembers. The gate sees
only that a row is present; whether it is true is what an `agent-skill:tiered` pass reads for.

| section | why this skill is its only carrier |
|---|---|
| Quick reference | Both CLIs' prompt, stdin, JSON, resume and auth surfaces side by side. `--help` gives one CLI at a time and never says which of two prompt sources wins when both are passed. |
| Canonical commands | The exact call per CLI, carrying the flags whose absence fails silently — `--skip-git-repo-check`, `--strict-config`, a pinned `--session-id`. Assembling these from `--help` is precisely how the traps below get reached. |
| Reading the output | Which field carries the text, the session id and the success verdict, per CLI and per format. A success check written against the wrong field is the failure this skill exists for, and no one document states both shapes. |
| Traps — none of these look like failures to a driver | The core of the skill, and the one thing no `--help` will ever supply: a flag's documentation says what it does and never what it does wrong. Each entry names an exit code, a stream, and a field the caller would have believed. |
| Going further | The pointers to the reference files, and the one-line naming of the opt-in files. That line is the entire mechanism by which opencode, hermes, grok, sandbox and agy coverage cost nothing on an ordinary invocation. It is also the only place a reader learns that agy is out on terms grounds rather than missing, which is what stops a session assembling the calls from `--help` instead. The hermes pointer earns its clause the same way and is held to the same limit: it says a precondition exists and does not say what it is, because the frontmatter names hermes only so the skill fires for a caller who asks, and says nothing of the precondition, so this line is the only notice a session gets that the file has to be read before that CLI is driven. **What the precondition actually is belongs to `hermes.md` alone** — a review on 2026-09-03 found the unattended-execution fact itself restated here and removed it, which is the leak this row exists to keep out. **It deliberately does not point here**, unlike the sibling plugins' skills: a maintainer's pointer in a caller-facing list is paid by every caller who will never edit, and an updater arrives through this file's own procedure or through the notice at the top of `verify.md`, which is where a re-verification pass starts. Recorded so the absence is not read as an omission and filled in. |

## Update procedure

0. Update both first, then stamp: `claude update && codex update`. Both subcommands exist and
   are no-ops when current (verified 2026-08-27). Do this *before* reading versions, not after.
   Codex moved mid-pass on 2026-08-27. Updating up front collapses that into one known version
   per CLI for the whole pass, and it is also the honest target: a driver written against this
   file runs whatever is current, not whatever was installed here. Re-read both versions at the
   *end* anyway and confirm they still match the stamp. **agy is stamped in `agy.md`, not
   here** — it self-updates on its own schedule and did so mid-pass on 2026-08-22 and
   2026-08-27, invalidating every agy verdict taken before it, so that file's own procedure
   updates and stamps it when someone opens it. **hermes is the same case for the same reason**
   and is stamped in `hermes.md`: its install announces on every start how far behind it is, so
   a pass that has not run `hermes update` first is measuring a version nobody will be running.
   **grok is stamped in `grok.md`**, from `grok --version` after `grok update --check` reports
   that build current.
1. Run everything in `verify.md`, top to bottom.
2. Any behaviour probe that *stops* failing means a trap was fixed upstream — remove it
   from `../SKILL.md` rather than leaving a stale warning. **Keep the probe and invert it**,
   so it now asserts the fix. An upstream fix is a claim like any other and can be reversed;
   on 2026-08-27 one was, in a form worse than the original, and the only reason it was caught
   is that the retired trap's probe had been left in place.
3. Refresh `models.md` wholesale and re-date it. Do not patch individual rows.
4. Only edit `../SKILL.md` if a shape or a trap actually changed. **A *new* trap passes the
   reachability corollary first** — can a driver following this guide reach it, and can the entry
   name an exit code, a stream, and a field the caller would have believed. If not, the flag is
   `--help`'s job, or the subject belongs in an opt-in file. That test is what took `--bare` back
   out the same day it went in, and it is stated in full under *What this skill is, and is not*;
   it is repeated here because this is the step where a trap gets added and the corollary is not
   read from here. Any new *section* adds its row to the section inventory above in the same
   commit — but the gate counts sections, so a trap added inside *Traps* reaches nothing
   mechanical, and this step is the whole of the check. **A description edit, or a new opt-in
   file, re-runs the trigger evals**: `claude plugin eval plugins/agent-cli --trust-plugin`, from the
   repository root. Its cases are in `evals/` at the plugin root, one per subject the
   description has to catch and one per near-miss it must not; a new opt-in file adds a case.
5. Append an entry to `history.md`, newest last: what moved, what was verified by execution,
   what was only read from `--help`. **Keep it under about forty lines.** On 2026-08-28,
   overlong entries showed that essay was crowding out record. A finding that genuinely cannot
   fit is a signal it wants a file of its own — an overlong entry was really `sandboxed.md`
   asking to exist. Title it with what was decided or found, since the titles are the index.
6. Once a quarter, or whenever one is about to be relied on, re-run `research.md` by hand.
   Those sections have no probes — that is the point of them — so nothing in steps 1–4 touches
   them, and on 2026-08-27 the quota section was found wrong about both CLIs it documents.
   Being out of the guide makes a claim cheap to leave stale, not exempt from being wrong.

Claims verified by execution and claims read from `--help` are not the same strength. Say
which is which; the effort-key bug survived because a `--help`-grade claim was written as
though it were execution-grade.

And a second rule, from the 2026-08-22 review: **a tracked file may not defer its own
counter-evidence to an untracked one.** Pass records live in an untracked directory; a
reader of the published skill cannot open them. So anything that qualifies a recommendation
— the caveat, the limit, the fact that would reverse it — has to be published alongside the
recommendation, not cited from it. A pointer the reader cannot follow reads as support.

A third rule, from 2026-08-28: **provenance is where private context leaks, so restate it
before writing it down.** This file asks every entry to say where a finding came from, and
when one crosses in from another session the honest answer often names something internal — an
agent, a worker, a host, a job id. None of that belongs in a tracked file or a commit message;
`AGENTS.md` requires it be restated in a publishable form first, and a later commit removing it
does not unpublish it. What a reader actually needs is the *grade*: that the finding arrived
already written, from runs this file had not seen, and what was re-measured before it was kept.
"A separate session" carries all of that and names nothing.

## History

See `history.md` for this skill's public decision record.

## Research kept out of the guide

In `research.md`, separated 2026-08-30 to keep the file a maintainer reads before every edit
focused on maintenance. It holds the measurements behind decisions
`../SKILL.md` does not carry: the latency comparison that settled `--bare` and streaming-input
mode, the comparison with a wrapper encoding the same traps, and the subscription-quota readers.
**It has no probes by construction**, which is why step 6 above is a calendar reminder where a
probe would be a test. Open it when step 6 comes due, or when re-deriving one of those decisions.

## Open questions

- Whether the Cline CLI becomes a lane. Deferred 2026-08-29 on one open upstream bug —
  non-interactive resume, [cline/cline#13239](https://github.com/cline/cline/issues/13239) — and on
  `--plan` not being read-only. Nothing else measured was a design problem, and its failure
  semantics are better than opencode's. **Re-check when #13239 closes**. Still failing on 3.0.73,
  re-checked 2026-10-20.
- **hermes under srt.** The opencode lane was re-measured under srt on 2026-10-20; hermes was
  not, so its lane is withdrawn rather than carried unmeasured. Condition to close: a hermes lane
  measured under srt the way `opencode.md`'s was — edit inside, write outside refused, `git add`
  refused — asserting on the files, with its probe added to `hermes.md`.
- Whether the quota readers should become a **caller-facing** reference. They moved into
  `research.md` on 2026-08-30, which answers nothing here — that move was about what a
  *maintainer* reads before editing, and this question is about what a *driver* can open. The
  question changed shape on 2026-08-27: the additional-support tier now exists, and the argument
  for promoting them is no longer "are they useful enough" but **"do they need probes"** — they
  rotted precisely because research carries none, and step 6 is a calendar reminder where a
  probe would be a test. Against it: they are not a CLI, so they do not meet that tier's stated
  entry bar, and inventing a second kind of opt-in file to hold them would cost more structure
  than the two shapes are worth. Unresolved; revisit if they go stale a second time.
