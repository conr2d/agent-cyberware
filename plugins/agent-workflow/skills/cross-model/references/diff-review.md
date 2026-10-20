# Reading a diff — what to skip, what to look for, what it cannot reach

## Lockfiles and generated files

Lockfiles (`pnpm-lock.yaml`, `Cargo.lock`) and generated output (a codegen or compile `outdir`)
can dominate a diff and burn reviewer context while carrying ~zero line-by-line review value.

**Handle them by how you read the diff, not by how you commit.**

- **Keep them in the same atomic commit as the unit.** Splitting lockfiles into their own
  commit does *not* shrink the working-tree diff you review — commit structure is irrelevant to
  `git diff` — and a feature commit without its lockfile is not one sealed unit: it isn't
  reproducibly buildable, and a lock-only commit isn't a meaningful unit. Lockfiles stay
  committed and tracked, for reproducibility. You just don't *read* them.

- **Exclude them from the review diff:**

  ```bash
  git --no-pager diff ':(exclude)pnpm-lock.yaml' ':(exclude)Cargo.lock' ':(exclude)<generated-outdir>'
  ```

- **Sanity-check them cheaply, separately** — never ingest them whole:

  ```bash
  git diff --stat -- pnpm-lock.yaml Cargo.lock   # scope of change only
  ```

  Then confirm the change matches the **dependency delta the spec already dictated.** The spec
  names exact packages and versions, so the lockfile's expected change is known in advance;
  verify only that no *unspecified* dependency appeared. An unexpected new package in the
  lockfile is the one thing worth catching here, and it is the one thing the exclusion above
  would otherwise hide.

The same exclusion applies to any committed generated artifact: review the *source or
generator*, not its output. If reviewing the generator is not enough to be confident in the
output, that is an argument for a parity test — a single source of truth needs one — not
an argument for reading the generated file.

## Two things a cold read misses, and one it cannot reach

Reported from runs by the sessions that hit them, none re-executed here.

**A test's name is a claim about which case ran, and nothing enforces it.** Read each test's
*input* against the case its name asserts. In that run a suite of thirty-one passing tests held
one named for a failing-probe case whose scripted input was a *successful* probe, so the failure
path it existed for had never executed — and the implementation it certified would have failed
every first run on a clean machine. Green tests are evidence that the code does what the tests
do, which is the same thing only when the names are true. This one is *in* the diff — a cold read
can catch it, and this one did not.

**Two authors on one spec is an ambiguity detector, and the disagreements are the output.** Where
a unit has more than one site a rule must reach, running the same spec through two independent
authors and diffing them surfaces what a cold read cannot: a place where both implementations are
reasonable and the spec never said. Treat every divergence as a spec defect until shown
otherwise, **including the ones where both implementations work** — in that run both real
divergences were spec silences, and one of them was the exit-status rule the spec had stated at a
single step. That defect was found by the two authors disagreeing, not by review.

**The two lanes behave differently and consistently, which is what says how to read them.** Reported
from a later run, two units on one task, both authors given the same spec carrying the same
defect: one widened the scope correctly and did not mention it, the other stopped and named it.
Both are defensible readings of the same contract — one honours the spec's intent, the other its
letter — so this ranks nothing. What it buys is a reading order. Check a widening lane's *silence*
and a stopping lane's *objection*, because that is where each one puts the thing it did not say.

The two-author pass is conditional, which is why it is here and not in `../SKILL.md`: it costs a
second author and buys nothing on a unit with one decision point. Reach for it where a rule has
to land in several places at once — the case the spec contract's third item is about.
