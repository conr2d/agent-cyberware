# Dispatching the author agent

Everything here is perishable — model ids, config keys, flag names — so prefer the command
that prints the value over the value written down. Where that command reads a local cache rather
than the source it prints an age along with the value, and the age is part of the answer: the
catalog block below is one such, and the note beside it says which invocations were measured not
to refresh it. The stable part is in `../SKILL.md`; this file is the current instantiation.

**What follows is what is specific to dispatching an *author* under this workflow, plus the
subprocess traps the calls below depend on.** The general problem — how to drive a coding-agent
CLI from a subprocess at all, and which of its failures are silent — is out of scope here. It is
covered by `agent-cli:non-interactive`, in this marketplace's `agent-cli` plugin, which carries a
dated last-verified stamp against the binary versions it was checked on. Installing a plugin is not
loading it; name the skill to load it. **Nothing below depends on having it**: every command below
is runnable as written, and where a form is likely to have rotted this file names the command that
prints the current answer rather than assuming another
document will. That claim was false on 2026-08-21 in two places, which are now written out in
full. **The blocks below were rewritten twice on 2026-08-22**, each time because a review executed them and they failed — the second time at
argument parsing, before any turn. The forms now here were run end to end on 2026-08-22:
dispatch, then resume by id from the repo root, with the resumed session answering from the
first run's context. Any command here is worth re-running rather than trusting: the file names
how, and the note under each block says when that block was run and against what.

**Re-verified 2026-08-30 against codex-cli 0.150.1, and nothing below changed.** Three minor
versions on from the binary the notes name, every command block was run again as written and
produced what its note records — so those notes stand as when a form was established, not as the
last date anyone checked it. Re-run: both dispatch forms, the key probe, the catalog snippet, the
resume block end to end, the trust refusal on a dispatch and on a resume by both `--last` and an
id, the rejection of `--sandbox` and `-C` on resume, the `MAX_ARG_STRLEN` boundary, and the
model-mismatch literal's presence in the binary. **Not re-run, and still carrying their earlier
grade:** what `--last` resolves to in a *different* repository, and the mismatch warning seen on an
actual mismatched resume — only its presence in the binary was rechecked. One cosmetic difference,
recorded so a later pass does not read it as a mismatch: the header line now prints
`sandbox: workspace-write [workdir, /tmp, $TMPDIR]`, of which the string quoted below is the
prefix.

## The call

```bash
echo "<spec>" | codex exec - --model <model> \
  --sandbox workspace-write -C <repo-root> \
  -o <report-path> --strict-config \
  -c approval_policy=never -c model_reasoning_effort=<effort>
```

*Run 2026-08-22, codex-cli 0.147.0, with the placeholders filled and `<effort>` as `max`: exit 0,
and the header printed `sandbox: workspace-write` and `reasoning effort: max`.*

- `--sandbox workspace-write` lets the author edit files and run commands within the repo
  while staying sandboxed. It is the permission level the role needs and no more: the author
  self-checks with build/test, and never commits.
- **Prefer stdin (`exec -`) over an argv prompt — and not for size.** A single argv string is
  capped near 128 KB by `MAX_ARG_STRLEN` (131 071 bytes accepted, 131 072 rejected, measured
  2026-08-21 and again 2026-08-22), far below `ARG_MAX` (`getconf ARG_MAX`) but far *above* a
  spec — check yours with `wc -c`, and this skill's own always-loaded `../SKILL.md` with
  `wc -c ../SKILL.md`; that one comes back an order of magnitude under the cap. The two
  `MAX_ARG_STRLEN` figures are an ABI constant on 4 KiB pages — `getconf PAGESIZE` = 4096 where
  they were measured — and are written down because they do not move there. **Quoting is the
  reason.** It does not scale away with length, and it fails by mangling the spec rather than by
  refusing it.
- `-o` is `--output-last-message`. The CLI writes the author's final message there itself, and
  the author is not given the path — carried from the original author's observation on
  2026-08-07, not re-executed here. **So never ask for the report by path.** "Write your report
  to the path given by the output flag" is unfollowable here: this author does not read argv and
  cannot learn the path, so it spends a round trip stopping to report the spec's mistake. Moved
  here from `../SKILL.md` on 2026-08-27, which keeps the runtime-independent form of the rule —
  *Ask only for what the author can see* — and no longer asserts what any particular author
  runtime hides.
- The reviewer then works from `git diff` / `git status` — the author's uncommitted changes —
  and takes over at stage 3 of the loop.

If you pass the spec as an argument rather than on stdin, the argv form takes the prompt as a
positional argument, and closing stdin stops it waiting on a terminal that is not there:

```bash
codex exec "<spec>" --model <model> \
  --sandbox workspace-write -C <repo-root> \
  -o <report-path> --strict-config \
  -c approval_policy=never -c model_reasoning_effort=<effort> < /dev/null
```

*Run 2026-08-22, codex-cli 0.147.0, with the placeholders filled the same way: exit 0 from a cwd
outside the repo, `workdir` the `-C` target, and the same two header lines as the call above.*

It carries the same `-c` pair as the canonical call, and that is not symmetry for its own sake.
**`--strict-config` cannot catch a flag that is simply absent** — no key is wrong, so the run
proceeds at whatever `~/.codex/config.toml` holds, or at the built-in default when it holds
nothing. An earlier form of this block omitted the effort key and ran at `reasoning effort: none`;
the header says so, and a driver reading only `-o` does not see the header.

## Model and effort — stated on every call

Every dispatch and every resume under this workflow names its `model` and its effort on the call,
**whatever `~/.codex/config.toml` holds**. The ground is the trailer: it names the model exactly,
and that is only true when the orchestrator states it on the call. Emptying the config does not
buy that — a call that omits the flag then inherits the built-in default instead of the
configured one, which is the same silent substitution from a different source. So the config is
yours to set for interactive use, and nothing here depends on it.

**`--strict-config` is not optional on any dispatch under this workflow.** Without it an unknown
`-c` key is accepted silently, the run proceeds at default effort, and nothing in the output
names the dropped key — the header shows the effort it ran at, but a driver reading only `-o`
does not see the header. With it, a typo'd or renamed key is an exit-1 error before any turn
starts.

**The effort key is `model_reasoning_effort`.** Plain `reasoning_effort` is not a real field:
`--strict-config` rejects it with `unknown configuration field` (executed against codex-cli
0.147.0 on 2026-08-21, both keys, one accepted and one rejected). Earlier revisions of this
document had these two exactly backwards.

Verify a key you are unsure of rather than trusting this file:

```sh
for k in 'model_reasoning_effort="low"' 'suspected_key=1'; do
  if echo "" | codex exec - --skip-git-repo-check --strict-config -c "$k" 2>&1 \
     | grep -q 'unknown configuration field'; then echo "REJECTED  $k"; else echo "accepted  $k"; fi
done
```

*Run 2026-08-21, codex-cli 0.147.0, verbatim: `accepted` for `model_reasoning_effort="low"`,
`REJECTED` for `suspected_key=1`.*

(Empty stdin makes this cost nothing: an accepted key gets as far as `No prompt provided via
stdin` and stops before a turn runs.)

**Tiers are size; effort is a separate axis.** Both dials exist independently — pick the tier
for how much context the unit needs held at once, then move effort within it. The catalog of
reasoning levels each *listed* model supports is the local cache — and the block prints
`fetched_at` first because not every invocation refreshes it: `codex --version`, `--help`,
`exec --help` and `exec resume --help` all left it byte-identical (measured 2026-08-22,
codex-cli 0.147.0):

```sh
python3 -c "
import json; d=json.load(open('$HOME/.codex/models_cache.json'))
print('fetched_at:', d['fetched_at'])
for m in d['models']:
    print(m['priority'], m['slug'], '|', m['display_name'],
          '|', [l['effort'] for l in m['supported_reasoning_levels']])
"
```

*Run 2026-08-22, codex-cli 0.147.0, verbatim: exit 0, printing `fetched_at` and then one line per
model.*

**That cache is a listing, not a contract.** A model absent from it can still run. One dispatched
by id returned a completed turn at exit 0 with no fallback-metadata item, while the block above
printed a `fetched_at` minutes old and no row for that id — so absence is not evidence, and the
way to settle a slug is to invoke it. An id the binary genuinely has no metadata for is loud:
exit 1, with `Model metadata for ... not found. Defaulting to fallback metadata` as an error item
on stdout before the server refuses the turn. A clean exit 0 is therefore the model answering
rather than a substitution.

*Run 2026-10-02, codex-cli 0.159.3: the current author id, absent from the cache, exit 0 and no
warning item; a deliberately bogus id, exit 1 carrying that message.*

**The default for a narrow, fully-specified unit is the smallest tier at maximum effort.** A small
model given maximum thinking holds its own against a larger one given less on work whose Done-when
is mechanical — which is what a complete author-spec makes every unit. Step up a tier when a unit
needs to hold more than its spec can carry — larger refactors, anything spanning several files'
conventions — and step the effort down with it, to a middle level rather than the new tier's
maximum. That pairing is a statement about this workflow rather than about any particular model,
and it survives the catalog changing under it.

**Both dials are set here, on every dispatch** — which is why the command blocks in this file
leave `<effort>` a placeholder beside `<model>`. A literal in a block that gets copied outranks a
rule read further down. Leaving the key out is not the alternative: `--strict-config` cannot catch
an absent key, as above, so a value is always named.

**The stderr header is the only place a run names the model and effort it used.** `--json` leaves
both out of every event it emits, and `-o` receives the author's final message and nothing else —
so a driver capturing only those two cannot say afterwards what it dispatched. The plain `exec`
form prints them on stderr before the turn:

```
OpenAI Codex v<version>
--------
workdir: <dir>
model: <model>
provider: openai
approval: never
sandbox: read-only
reasoning effort: <effort>
```

*Run 2026-10-02, codex-cli 0.159.3: `--json` emitted `thread.started`, `turn.started`,
`item.completed` and `turn.completed`, with no model field on any of them; `-o` held the final
message alone; the header above came from the same call with `--json` dropped.*

**Capture stderr on every dispatch, and assert those two lines against what you passed** rather
than reading them afterwards. The header reports the value that *applied*, not the one requested:
a misnamed effort key with no `--strict-config` exits 0 and the line shows the inherited default
— measured with an effort present in `~/.codex/config.toml`, which is what made the inheritance
visible. That makes the header a receipt for a window already
spent, which is why `--strict-config` is the rule and the header is only the check on it.

**Tier is also the dominant cost lever, and that argument survives someone disagreeing about
answer quality.** On one narrow unit, measured 2026-08-29 by a separate session and reported here
rather than re-executed: a larger tier at maximum effort spent about a seventh of the Codex 5-hour
window, the smallest tier at maximum effort spent less than the usage endpoint can resolve, and
both scored full marks on a hidden suite. On that unit the tier bought the throughput, not the
answer. **A third dispatch on 2026-09-01 put evidence under the step-down half of the rule**: the
larger tier at a middle effort cost a fiftieth of the window rather than a seventh — the same as
that tier's lowest measured effort — and still scored full marks, so stepping the effort down
while stepping the tier up costs nothing on this unit.

**Effort below maximum on the *smallest* tier has never been run, and that is not a debt.**
Effort is a cost lever, and the smallest tier's window cost already sits below what the usage
endpoint can resolve — so effort is free there, and no decision hangs on what a lower one would
have scored. Filling that cell would spend a dispatch to learn nothing you could act on. The
rule also matches practice reported outside this repository, which is a second and independent
support for it; that is a reported claim, not one executed here.

## Resuming

Follow-up specs to the same author go through the resume form rather than a fresh dispatch, so
the author still has the unit's context. It is a subcommand, not a flag:

**Run it from `<repo-root>`** — `resume` takes neither `--sandbox` nor `-C` (neither appears in
`codex exec resume --help`), and `-c cwd=…` is rejected by `--strict-config` (reproduced
2026-08-22, codex-cli 0.147.0), so set the directory with the orchestrator's own cwd:

```bash
cd <repo-root> && echo "<follow-up spec>" | codex exec resume <sessionId> - \
  --model <model> -o <report-path> --strict-config \
  -c approval_policy=never -c model_reasoning_effort=<effort> \
  -c sandbox_mode=workspace-write
```

*Run 2026-08-22, codex-cli 0.147.0, with the placeholders filled and `<effort>` as `max`: exit 0
after a dispatch, with the resumed session answering from the first run's context — the end-to-end
run named at the top of this file.*

**The sandbox moves from a flag to a key.** `--sandbox` and `-C` are `codex exec` flags and are
**usage errors on `resume`** — the run fails at argument parsing, before any turn. `-c
sandbox_mode=workspace-write` is accepted — the end-to-end run above carried it under
`--strict-config` — and that it grants the same permission level is reasoned from the key rather
than read off the resumed run's header. Check the flag set
against `codex exec resume --help` rather than against the dispatch above; the two subcommands do
not take the same arguments, and an earlier revision of this block assumed they did.

**The id is printed by the dispatch itself**, in the plain header, with no `--json`, on the
`session id:` line. Capture it there. Resuming by that id **keeps it** — the same id came back on
the resumed run when this was executed on 2026-08-22 — so an orchestrator can hold one id per unit.

**`cd <repo-root>` is doing two jobs, and only one of them is about `--last`.**

*Trust.* Resuming from a directory codex does not consider trusted exits 1 with *"Not inside a
trusted directory and --skip-git-repo-check was not specified"* — whether you name an id or pass
`--last` (both executed 2026-08-22, codex-cli 0.147.0). Naming the id does not help; `cd` into
the repo does, and `--skip-git-repo-check` is the escape where the orchestrator cannot.

*Which session.* `--last` resolves against the orchestrator's cwd rather than the author's repo,
and in a *different* repository it exits 0 and resumes **whatever that directory last recorded** —
another unit's, or a fresh conversation where there is none — with nothing in the output saying
which. That one an explicit id does fix, and it is why the block names one.

**State `--model` and the effort on every resume.** An omitted `--model` falls to whatever
`~/.codex/config.toml` holds, or to codex's built-in default, and the trailer then names a model
the author did not use. A resume that lands on a different model
prints *"This session was recorded with model `<recorded>` but is resuming with `<used>`"* —
observed on a resumed run 2026-08-22, codex-cli 0.147.0, and both halves of that literal are in
that binary (`strings`). Omitting `-o` leaves any existing report file untouched (reasoned from
the flag being opt-in, not executed), so a reviewer who reads that path reads the previous unit's
output.

Resume forms have changed more than once; `codex exec resume --help` is the current answer to the
spelling, to `--last`, and to whether the id is still positional.
