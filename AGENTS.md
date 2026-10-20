# AGENTS.md

This is the `agent-cyberware` marketplace. Plugins are the unit of installation, so a plugin
groups the skills a project would want together and nothing else: `agent-cli` holds
`agent-cli:non-interactive`, `agent-workflow` holds `agent-workflow:cross-model`, and
`agent-skill` holds `agent-skill:tiered`. A project adopting a workflow should not have to
carry, or pay the standing cost of, a skill for maintaining skills. Contributors need no
plugin installed: the procedures are readable in `plugins/agent-cli/skills/non-interactive/SKILL.md`,
`plugins/agent-workflow/skills/cross-model/SKILL.md`, and
`plugins/agent-skill/skills/tiered/SKILL.md`. A contributor who has the corresponding plugin
installed may invoke it as `agent-cli:non-interactive`, `agent-workflow:cross-model`, or
`agent-skill:tiered`.

## Layout

```
.claude-plugin/marketplace.json     one manifest, at the repository root
plugins/<plugin>/
├── .claude-plugin/plugin.json      name, description, author — no skills key
└── skills/
    ├── <skill>/
    │   ├── SKILL.md
    │   └── references/             loaded on demand, not on every invocation
    └── <skill>/                    a plugin may hold more than one
```

This follows `anthropics/claude-plugins-official`. Two things about it are easy to get
wrong:

- **A skill's name comes from the directory holding its `SKILL.md`, not from the frontmatter
  `name:` field.** Putting `SKILL.md` at a plugin's root therefore names the skill after the
  plugin, and `claude plugin details` reports `Skills (0)`. The `skills/<name>/` level is
  what gives a skill its own name and makes the identifier `<plugin>:<skill>`.
- **`plugin.json` declares no `skills` array.** Skills are discovered from `skills/`, and the
  first-party plugins in that repository do not list them. Listing them is only worth doing
  to deliberately *exclude* one that is present on disk. `version` is optional rather than
  absent, and with it omitted `claude plugin list` falls back to reporting the commit sha —
  more honest than a hand-maintained number nobody bumps.

A plugin is consumed by registering the marketplace, never by copying it into `~/.claude/skills/`:

```sh
claude plugin marketplace add <path-or-owner/repo>
claude plugin install <plugin>@agent-cyberware        # --scope user | project | local
claude plugin details <plugin>                      # inventory + projected token cost
```

## What this repository holds

Two kinds of content, which decay differently and are maintained differently. **Practice** —
rules about how work is planned, gated, reviewed and sealed — is revised when something is
*learned*, which no schedule predicts and no command detects. **Measurement** — verified
behaviour of running tools — is re-verified by running a probe, and a probe that stops failing
is itself a finding.

**The practical consequence is per-skill, not repository-wide.** A practice skill should not
carry a version, a slug or a flag name as a standing fact. A measurement skill is made of them,
and satisfies the same editorial rule the other way: it names the command that prints the
current value and stamps when it was last run.

**Every history appends newest last.** Newest last is what `>>` produces, and the title index
then reads in time order.

## Writing a skill here

**Aim for the thinnest thing that prevents a first-time mistake.** Check the cost with
`claude plugin details`, and read what it reports rather than assuming: the frontmatter
`description` is paid on **every session, invoked or not**, and the body only when something
names the skill. Three consequences. Carrying a skill nobody invokes costs almost nothing, so
this marketplace is not made cheaper by holding fewer skills. The description is the most
expensive line a skill has — write it to name a trigger, never to summarise a body. And what
`SKILL.md` costs is paid per invocation by the sessions that do name it.

**A tier costs what it is *read*, not what it is long.** A history at nine hundred lines costs
a session nothing; nothing reads it front to back. A maintenance file at three hundred does
cost, because *read this before editing* stops happening. A person tracing one decision through
the history pays too, and the entry titles, which state decisions, are the index that keeps
that cheap. Judge each file against its own reader:

| file | paid |
|---|---|
| frontmatter `description` | every session, invoked or not |
| `SKILL.md` | every invocation |
| `references/<topic>.md` | when the session judges it needs it |
| an *opt-in* reference | only when the caller names its subject |
| `references/maintenance.md` | before an edit |
| `references/history.md` | when someone asks why |

**The opt-in reference is the cheapest way to add coverage.** A whole subject a reader may
not have — another CLI, another environment — named from `SKILL.md` in one line and opened
only by a caller who asks for it, costs nothing on any other invocation. Its subject still
needs a word in the description, or the skill never fires for the caller who asks: measured
with `claude plugin eval` on 2026-10-20, the `agent-cli` skill fired on two of nine opt-in
questions before opencode, hermes and grok were named in its description, and fifteen of
fifteen after. The test is **who can reach it.** Reach for this before concluding that
something new has to grow the always-paid file.

Three tests decide where a passage goes, applied in order.
**`plugins/agent-skill/skills/tiered/SKILL.md` is canonical for these and for the table above**;
what follows is this repository's rendering, with this repository's examples, and the
renderings are meant to differ. If the two disagree about the model itself — a tier missing,
a test defined differently — that file is right and this is stale. A step of its pass is what
compares them, and it has to be a step rather than a hook: the wordings differ on purpose, so
a gate would be comparing bytes that are meant to differ. Read the file to carry out the pass;
a contributor who has the plugin installed may invoke it as `agent-skill:tiered`.

1. **Only carrier** — is this skill the only thing that carries it? Content already enforced by
   a gate, a hook, a wrapper, or a tool's own `--help` is the document *explaining* a mechanism
   rather than being one. An enforcer counts only if it speaks at the mistake: it refuses
   loudly and at once, naming the cause. The essential procedure and the traps that **fail
   silently**, or surface only after the cost is paid, stay, because no amount of debugging
   recovers those.
2. **Reachability** — can a reader following this document reach the situation at all? A trap
   behind a precondition the reader does not have is paid on every invocation and met by
   nobody. That is an opt-in reference, or it is nothing.
3. **Rot** — the rule below. Perishable specifics and recommendations go to `references/` with
   a date on them.

The editorial rule that keeps this stable:

> **What rots does not go in the document; the command that prints it does.**

Facts with a shelf life belong behind a command the reader can run, not in prose that will
quietly go stale. A skill that grew into a reference is how a wrong claim survives for
months without anyone noticing.

Every skill also carries a `references/maintenance.md` — the reasoning behind its judgment
calls, the editorial rules that keep it stable, and the procedure for re-verifying it. Read
that file before editing a skill. Distinguish claims verified by execution from claims read
out of `--help`; conflating the two is how errors persist.

It also carries the skill's **section inventory**: one row per `## ` section of `SKILL.md`,
with the heading text verbatim in the first column, saying why this skill is that section's
only carrier. `.githooks/check-inventory.py` refuses a section with no row, and a row naming
no section, judged against a checkout of the index. Writing the row is the moment the three
tests above actually get applied — they were previously applied by whoever remembered to,
and the session adding a trap is the one least likely to remember. The gate sees only that a
row is present, never whether it is true; it supplies the occasion, and the periodic pass in
`plugins/agent-skill/skills/tiered/SKILL.md` is what reads. A contributor who has the plugin
installed may invoke that pass as `agent-skill:tiered`.

Two more gates run from the same hook. **A line number is a fact with a shelf life, so no
document here writes one**, and a claim about a skill's own size is the same kind of fact.
Name the section instead, or say the number in words when quoting a past size. **The gate
reaches less than the rule does**: it sees a size claim only where the paragraph names its
subject, so digit line-counts survive in paragraphs that do not — those are the rule's
business, not the gate's. `./.githooks/check-citations.py` refuses bare numeric citations,
Markdown file-and-line citations, numeric line anchors, prose references to numbered lines,
and digit line-count claims where the paragraph — or the sentence introducing a table — says
`SKILL.md`, *this skill*, or a skill's own name — **discovered from the plugin tree rather
than listed**, since a hardcoded set of names goes stale silently, leaving the gate passing
and no longer covering the skill that was added; `--show` prints a skill's shape for reading,
and nothing is derived from its output. It is not a truth oracle: a sentence can still be
wrong in a way no regex sees. **There is no exemption for dated entries** — that would exempt
exactly the region where perishable claims accumulate.

`check-frontmatter.py` refuses four things in a `SKILL.md` and nothing else: a file that does
not open with a line holding exactly `---`, or whose frontmatter is never closed; a line inside
it starting with a space or a tab; a value holding a second `: ` or ending in a colon; and any
of YAML's four invisible line breaks. Quoting a value to keep the colon is refused with it —
quoting is the habit that preserves the defect, and the remedy is to rewrite the value. A
`SKILL.md` that is a symlink is refused unread, so the bytes checked are the bytes committed.
**A tool that cannot parse a frontmatter drops the whole skill and says nothing** — no error, no
warning, no missing-skill notice — which is why the gate exists and why it is deliberately
small.

A `commit-msg` hook enforces the subject grammar and the trailer block from `CONTRIBUTING.md`:
a type from a closed set of five, a required scope, at most seventy-two characters, and a block
`git interpret-trailers` can actually read. It asks git's own parser rather than re-implementing
it.

All of these run only when `core.hooksPath` points at `.githooks`, and none runs on `git merge`,
`rebase`, `cherry-pick`, `revert`, `am`, or a commit made with `-n`/`--no-verify`. CI runs the
same checks on every push and pull request (`.github/workflows/gates.yml`), so a commit that
skipped them locally is still caught when it is pushed. **They are this repository's own hygiene,
not part of what the skills ship** — a project installing a plugin gets the convention as a rule
to follow, and copying `.githooks/` is the only way to have a gate.

**The per-pass record splits out, and the rule applies at both levels.** The record is the only
part that grows every pass, so left in place it crowds out the rules a maintainer is told to
read first. It belongs in `references/history.md`; research that needs its own reference belongs
in `references/research.md`. A file you must read before editing should grow only when the
rules change. A dated block sitting in one — a verification record, a measurement table, an
incident list — is history wearing a rule's clothes, and it moves; the exception is a block
the update procedure itself sends a reader to, which becomes its own reference with the
procedure pointing at it. Keep a history entry short: a finding that will not fit in about
forty lines is usually asking for a file of its own. Never prune or compress an old entry —
a summary of a correction is not evidence of one.

## Private context

Private context lives in `.private/`, untracked. Read it like any other context, and treat it
as **input only** — nothing from `.private/` reaches a tracked file, commit message, PR, or
issue unless it is first restated in a form that would be fine published. A rationale worth
keeping is *promoted* to a commit trailer or an ADR in publishable form, never copied across.

A contributor may keep a `.private/README.md` stating what belongs there; it is never tracked.

**Run this once per clone**, before the first commit from it:

```sh
git config core.hooksPath .githooks
ln -s AGENTS.md CLAUDE.md
```

`.gitignore` stops an accidental `git add .`; the tracked `.githooks/pre-commit` is the layer
that survives `git add -f` — for `.private/` and the runtime-state directories, which it refuses
by staged path. `CLAUDE.md` force-added is caught one gate further on, by the symlink refusal
described below. That hook only runs if `core.hooksPath` points at it, and **git does not carry
local config across a clone** — so a fresh clone starts with the guard off, silently, on a
machine where everything else looks configured. The same hook runs the citation, frontmatter and
inventory checks above, so a clone with `core.hooksPath` unset loses every one of them.

**`CLAUDE.md` is an untracked symlink to this file**, which is why it is in the setup block
rather than in the repository. Claude Code reads `CLAUDE.md` and not `AGENTS.md`, and a second
real file would drift from this one — but a tracked Markdown symlink is refused by
`check-citations.py`, and correctly: what git stores for a symlink is the target path, not the
document, so the gate would be checking bytes that are not the ones a reader gets. Making the
gate skip it to allow one convenience file is the edit that starts eroding a gate. It stays
untracked, and the cost is one line at clone time.

## Working in a tree another session is using

More than one session may have this repository open.

- **Another session's uncommitted work is not scratch space.** Do not write into a file that has
  unstaged changes you did not make; surface it and wait. A draft written into someone else's
  diff hunks is indistinguishable from their work when they come to read it.
- **`git stash` is a global operation on a tree you do not own**, and so are `checkout`, `reset`
  and `restore` against paths you did not touch. A stash and pop that "restored cleanly" still
  had a window in which another session's write would have been lost.

## Content rule

Nothing tracked here may name a private project, a contributor's domain or account, a path
outside a plain `~`, or an identity layer. Before adding or editing, re-read what you wrote
for those five. Three things are not what the rule is about and are allowed: this repository's
own name and URL, without which no install line can be written; a third-party vendor's or
upstream project's domain, as against the operator's; and a standard system path in a command
— `/tmp`, `/var/tmp`, `$TMPDIR`.

This holds because the unit of exposure is the commit, not the working tree — deleting a file
in a later commit publishes it just as surely as leaving it. Catching it late is what makes it
expensive: a history rewrite invalidates every clone and does not recover what was already
fetched or indexed.
