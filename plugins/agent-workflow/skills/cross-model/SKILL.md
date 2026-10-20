---
name: cross-model
description: Building with agents in separated roles — the spec, the authoring and the review each held by a different context, on different models where you can, so one model's blind spots do not pass every stage. Use when writing an author-spec for another CLI or model, dispatching that author, reviewing its diff, or sealing a unit it produced.
user-invocable: true
---

# Cross-Model Development Workflow

Two agents, distinct and non-overlapping: one **authors** code, a different one **reviews,
verifies, and seals** it.

**Why the roles are split, and why across models.** A model that plans, writes and reviews
its own work carries the same blind spots through every stage, so the review confirms what the
authoring assumed. Separating the roles removes self-approval; putting a different model in
each removes the shared bias as far as the models you have allow. Different contexts are the
requirement; different models are the strengthening, and a single-vendor setup still gets the
first.

The split makes self-approval **structurally impossible** rather than discouraged: the author
sees only the spec and cannot rationalize; the reviewer sees only the resulting diff, reads it
cold, runs the gates, and is accountable for sealing. The long form of that argument is in
`references/maintenance.md`.

The current instantiation pairs a code-authoring CLI agent with an orchestrator/reviewer, but
the pattern generalizes to any capable author paired with a different reviewer. Dispatch
mechanics — invocation, model, effort — are perishable and live in
`references/codex-dispatch.md`.

## Roles

**Author.** Receives a complete, deterministic spec and produces the implementation. Nothing
more.

- Runs inside the repo with write access, executes build/test commands to self-check, but
  **never commits** and **never pushes**.
- Has **no standing project context** — it does not see the planning conversation, the
  roadmap rationale, or prior review history. Whatever it needs must be in the spec or
  readable in the repo.
- **Makes no discretionary decisions.** Every architectural, naming, dependency, layout, and
  library-API choice is pre-decided in the spec. If the spec is ambiguous, the author must
  **stop and report it, not guess.** It never suppresses or works around a wrong spec line to
  make it pass — it writes the correct code and reports the discrepancy in the same
  message. Guessing is the failure mode this workflow exists to prevent.

**Orchestrator / reviewer / sealer.** Holds the full context — plan, prior decisions,
architecture invariants, conformance rules.

- Writes the airtight spec, dispatches the author, then **reviews the full diff cold**, runs
  the verification battery + conformance gates, folds fixes, and **seals** (commits) the unit.
- For high-risk units, adds an **independent third-agent review** — a dedicated
  reviewer/architect agent, not the author and not itself — on top of its own before sealing.
- Owns all git history. The author's output is raw material; the reviewer is accountable for
  what lands.

## The per-unit loop

A "unit" is the smallest change that passes its checks, can be reviewed on its own, and does one
thing — one intent line; if it needs "and", split it.

```
1. SPEC      Reviewer writes the deterministic author-spec for one unit.
2. AUTHOR    Author agent implements it. No commits. Self-checks with build/test.
3. REVIEW    Reviewer reads the FULL diff cold against the goal:
             - architecture-conformance (boundaries, invariants),
             - correctness, error handling, edge/negative cases,
             - adherence to the spec (did it do exactly what was asked?),
             - each test's INPUT against the case its name claims,
             - no scope creep, no out-of-scope files touched.
4. VERIFY    Reviewer runs the verification battery + automated conformance gates
             (the unit-seal gate). Records evidence.
5. FIX       Discrepancies → either a tightened follow-up spec back to the author,
             or a direct reviewer fix for trivia. Re-verify.
6. (RISK)    High-risk unit → independent third-agent review pass before sealing.
7. SEAL      Reviewer commits the unit with the trailers that apply (incl. `Reviewed:`).
             Author never seals.
```

A stage-4 failure cannot be sealed — same rule as any conformance gate. **A returned author is not
necessarily a finished one**: confirm the run completed before reading its diff.

How to read a stage-3 diff — what to skip when lockfiles and generated output dominate it, what
to look for that a passing suite hides, and what a cold read cannot reach at all →
`references/diff-review.md`.

## The author-spec contract

Because the author has zero standing context and must not improvise, **the spec is the entire
interface.** A spec is complete only if a competent implementer with no knowledge of the
project could execute it with no open questions. It must contain, explicitly:

1. **Context briefing** — what the project is, the architecture invariants that constrain this
   unit, and where to read more in-repo (point at the files, e.g. `docs/`,
   `AGENTS.md`). Never assume the author remembers anything from a prior unit.
2. **Scope** — the one thing this unit does. One intent.
3. **Every decision, pre-made** — exact dependency names *and versions*, exact file paths,
   exact config keys and values, exact library/API call signatures (verified against current docs
   beforehand — see *Verify the API surface* below), naming, directory layout.
   No "choose a suitable X". No "something like". And **a rule stated at one site governs that
   site alone** — state it at every site it reaches, or once with the sites named, the ones it
   deliberately does not govern included, since those otherwise read as omissions.
4. **Exact artifacts** — for files whose contents are determinate, give the contents (or a
   precise template). For generated files, give the generator command and options.
5. **Guardrails / prohibitions** — what the author must NOT touch (out-of-scope directories,
   unrelated deps, the commit history), must NOT do (no version bumps beyond those listed, no
   architecture changes, no new patterns), and both halves of the response rule:
   **stop-and-report on ambiguity, correct-and-report on error — never a suppression or
   workaround that makes a wrong spec line pass.**
6. **Done-when** — the concrete, observable checks (commands to run, expected outputs) that
   define success, including boundary/negative cases.
7. **Commands** — which commands the author should run to self-verify, and the explicit
   reminder: **do not commit, do not push.**

**Derive the file list from the Done-when, as its own pass after it.** The two get written at
different moments — the list while thinking about scope, the checks while thinking about
outcomes — and nothing reconciles them, so a spec ships requiring work in a file its own
guardrails withhold and the author is handed two of its instructions in conflict. Derive the
list twice: once for the files the checks *name*, once for the files the change *implies* — a
signature gaining a parameter implies its callers, a struct gaining a field implies every site
that constructs it, and no behavioural check mentions a construction site. Then grep each path
against the tree rather than reading the list by eye.

**Ask only for what the author can see.** An instruction depending on state the author cannot
observe — a path passed on the command line, an env var the harness set — is a spec defect, not
an author failure, and there is nothing correct to write in its place, so the author stops. Ask
for the report as **"your final message is the report."**

If the reviewer cannot fill in part of the spec because an SDK/API detail is uncertain, the
reviewer resolves it **before** dispatching — the uncertainty is never delegated to the author
as a judgement call.

## Verify the API surface before writing the spec, not after the diff

The author implements exactly what the spec says against external libraries. If the spec's API
details are stale or wrong, the author produces confidently-broken code. So re-verify external
API specifics against current official docs **immediately before
writing the spec** — exact package versions, import paths, config schemas, function signatures
— and embed the verified specifics. "I think the API is roughly…" is not good enough to hand to
a context-free author.

**This is the highest-leverage stage of the loop, not the diff review** — argued from two runs,
not from a series. What makes it worth acting on is that the mechanism is legible — a
context-free author cannot supply what the spec omits — not that the sample is large. Verify
every external version, URL and signature, **including the ones that feel too minor to
check.** Reviewing your own spec before sending it catches more than reviewing the diff
afterwards.

## Sealing policy

- **The reviewer seals, never the author.** Commit messages follow
  `references/commit-message.md` — the trailers that earn their line, not all of them — plus a
  `Reviewed:` trailer naming the evidence, not the fact of review. "cold diff review +
  independent re-run of the Done-when battery" earns its line; "reviewed" does not.
- **Review fixes fold into the unit before it is shared** — amend, or reset to the base and
  recommit — so history shows the reviewed state, not the back-and-forth. The exception is a
  fix carrying a lesson a later unit would otherwise re-learn: it gets its own commit, with a
  `Lesson:` trailer.
- **`Assisted-by:`, one line per agent that contributed, reviewer included.** The kernel's form
  (`Documentation/process/coding-assistants.rst`) narrowed: the agent's name, a colon, the
  **model id it was actually run as**, and nothing else — no email, no display name, and none of
  the analysis tools the kernel would allow after it. A reviewer-only seal carries just the
  reviewer's line, and **no agent gets `Co-Authored-By:` or `Signed-off-by:`**.

  ```
  Assisted-by: Codex:gpt-6.1-sol
  Assisted-by: Claude:claude-opus-5-5
  ```

- **The model is named because it is known, not guessed** — the orchestrator sets the author's on
  the call and the harness states the reviewer's. Where a pass is delegated to a sub-agent whose
  model is not certain, name it in `Reviewed:` and **omit the trailer** rather than inventing one.
- **Auto-seal is allowed.** Once a unit passes review + verification (+ independent review for
  high-risk), the reviewer seals without asking and reports the result. Per-unit human
  confirmation is not required.
- **Context budget is a hard stop**, not something to push through. When the reviewer's working
  context grows large enough that quality would degrade, it must stop and request a
  compact/reset rather than continue — finishing the current unit's seal first if safe.
  Carrying state forward in durable artifacts (plan, status memory, commit trailers) is what
  makes a mid-stream reset safe.

## When NOT to use this loop

- Trivial or mechanical edits the reviewer can do directly and verify in seconds — the author
  round-trip is pure overhead.
- Open-ended design, exploration, or requirements that aren't yet locked. Do the
  planning/design passes first; the author needs a settled spec and is not a design partner
  here.
- Anything where the goal can't yet be stated as deterministic Done-when. Tighten the goal
  before delegating.

**One exception to the first bullet, and it is not about size.** Where the plan rejected
something on grounds of *timing, ordering or lifetime*, the cold read is not skippable: dispatch
the unit rather than authoring it directly, and do not let restating the rejection in the spec
stand in for it. Timing is a property of the mechanism, and the mechanism exists only in the
code — a reactive declaration, a lifetime, an `await`, a lazily initialised handle each carry a
decision no document states — so the rejected option returns as an implementation shape that the
plan and the spec both read as consistent with themselves.

**A skipped loop is recorded, not silent.** The reviewer-only `Assisted-by:` line already says
who authored the unit; what the body owes is *why* the loop was skipped, so a later reader finds
a decision rather than an omission. Without that line, a branch whose units did not all get a
cold read reads as though they did, and the guarantee is extended to the commits that never
earned it.

## Going further

- Dispatching the author — invocation, model, effort → `references/codex-dispatch.md`
- Reading a stage-3 diff, and what reading one cannot reach → `references/diff-review.md`
- Why an agent's line names a model at all → `references/attribution.md`
- The commit message and which trailers earn their line →
  `references/commit-message.md`
- Editing this skill → `references/maintenance.md`; the dated record → `references/history.md`
