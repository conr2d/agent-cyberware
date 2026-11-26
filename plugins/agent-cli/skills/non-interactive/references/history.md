# History

Newest last. Entry titles state what was decided or found; they are the index.

### 2026-10-20 — first public version, as `agent-cli:non-interactive`

Renamed from `agent-cli:headless` in an earlier private marketplace whose record is not published.
The port uses non-interactive terminology and the public skill identifiers throughout.
The opencode author lane was re-measured under srt; the unmeasured hermes lane was withdrawn.
Earlier history pointers and private context were removed.
Rules that survive were derived from that unpublished record; their reasoning is restated
in `maintenance.md` where a reader needs it.

### 2026-10-29 — use Codex danger-full-access inside srt and assert on files

Added first-hand, file-asserted measurements to `sandboxed.md`: codex-cli
0.165.0 under srt 0.0.81 reproduced both exit-zero traps. `workspace-write` could not start
the shell; `danger-full-access` edited the project while srt refused the outside write.
Kept the earlier bwrap measurements and the file assertion rule, qualified the startup-warning
check, and added an srt pair probe. Token refresh and domain narrowing remain unmeasured.
Recorded the separate, once-observed 2026-10-28 opencode dotfile trap: the spec tells the author
they belong to the lane. Added srt to the guide's existing opt-in pointer.

### 2026-10-29 — Codex under srt needs only `chatgpt.com`

Narrowed the measured srt settings in `sandboxed.md` from four domains to `chatgpt.com`, after a
run with only that domain succeeded and a run with none failed loudly, exit 1. Token refresh was
left unmeasured on purpose: forcing one means altering the real credential, and a rotated
refresh token could sign the host out.

### 2026-10-30 — Codex moves to the 6.x ladder; route by description, not priority

Re-read every model listing. Claude's four aliases map to the same ids as on 2026-10-19. Codex's
cache, identical under codex-cli 0.165.0 and 0.166.0, now lists `gpt-6.1-sol` and `gpt-6-astra`,
which ran without rows on 2026-10-19, beside `gpt-6.1-terra`, `gpt-6-luna` and the older 5.6
family. Each of those 6.x ids and `gpt-reserve` answered at exit 0; a bogus id failed at exit 1.
The priority integers now put the workhorse above the frontier model, so the routing table follows
the cache's descriptions: `gpt-6-luna`, `gpt-6.1-sol`, `gpt-6-astra`. `gpt-6.1-terra` names no
tier and is left out. Runnable examples moved to current ids; dated records kept theirs. grok's
listing gained `grok-4.5`; opencode still lists `deepseek-v4.1-flash-free`; agy's catalogue was
re-read by the operator and is unchanged.

### 2026-11-09 — opencode needs a key handoff; OpenRouter routing reaches the API

A keyed provider exposed what the free-model lane never could: on opencode 2.2.5 (2026-11-05)
and 2.2.6 (2026-11-09), a throwaway home holding only the `auth.json` symlink has no
credentials, under srt and without it. Passing the provider's key variable in the srt command's
`env` works, with only `openrouter.ai` allowed. Where opencode now keeps credentials was not
established. Added *Routing through OpenRouter*: a model's `options.provider` reaches OpenRouter,
shown by a ZDR-pinned non-ZDR endpoint failing with a routing funnel and its `zdr: false`
control passing. `flex` opt-in and other routing keys remain unmeasured. Providers, prices and
rankings are left out on purpose: they change within days, and the two listing endpoints print
them. The 2026-10-20 free-model results stay as dated.

### 2026-11-10 — srt's proxy sockets follow the caller's TMPDIR

A separate session reported that a lane with the home deny-read lost its network until the
outer `TMPDIR` moved to `/tmp`. Re-measured on srt 0.0.81 with one `curl` under the settings
named in srt trap 8: 200 with the outer `TMPDIR=/tmp`, and code 000 with `Proxy CONNECT
aborted` with it under `~`. srt itself exited 0 both times. The socket location was read from
srt's source. Added as srt trap 8, and the lane commands now set `TMPDIR=/tmp` on `srt`. The
earlier lane measurements here ran with `TMPDIR` unset.

### 2026-11-10 — Refresh pass: fable rolls, grok scopes session ids by directory, opencode's second home runs

Updated first, then ran `verify.md` top to bottom on Claude Code 2.1.321 and codex-cli 0.167.0;
versions matched at the end. Every probe held. `fable` now resolves to `claude-fable-5-2`; the
other aliases are unchanged. Codex's cache has the same ids and descriptions as 2026-10-30, with
priorities renumbered one to eleven; five 6.x ids and `gpt-reserve` answered at exit 0 and the bogus control
failed. `gpt-6-astra` was not invoked. The probes that pass no `-m` ran on the local Codex
default, whatever it is. The Claude envelope still carries every field the guide names.

grok 1.0.77, every probe in `grok.md` run. Two changes: the three `--session-id`/`--resume`
failures now also write an error object to stdout, and a reused `--session-id` from another
directory exits 0 as a new conversation under the same id. The second is silent, so it is
written up as a trap with a probe. `grok models` printed `You are not authenticated.` while
runs authenticated.

opencode 2.2.6, every probe in `opencode.md` run: surface, open stdin, permission floor,
loud failures, both home probes and the confined lane, which still wrote `EDITED` and nothing
outside. Two results changed. Eighteen of eighteen one-shots ended with `step_finish`,
which by that file's own probe retires the trap; the probe now asserts the fix. `run` in a
second home without `--standalone` exited 0 four times, with the session id in neither home's
data directory, while `auth list` there still failed on the port; `--standalone` stays. A `-s` of a missing session
still exited 1 with an error event, but its message named a stale directory from opencode's own
state rather than the session; not written up, since one machine's state produced it.

hermes updated to 0.23.1, version stamped, probes not re-run. agy 1.5.3, read by the operator in one `agy models` listing: the same six rows as 1.4.10; no agy probe was run.

### 2026-11-15 — Devin joins as an opt-in CLI; its stdout is not an envelope

Added `devin.md` and its trigger eval, keeping the surface, traps and probes opt-in.
Executed on devin 3000.12.57, Free plan, `swe-2-flash-medium`, inside srt 0.0.81:
version and model listing, trust refusal, discarded stdin and missing prompt, unknown model,
default and accept-edits tool rejection, accept-edits write, dangerous shell execution,
export/session round trips and missing-session refusal, stdout joining and startup timing.
The confined lane used copied credentials and config, a resolved binary, inner proxy handoff
and a throwaway home. File assertions confirmed inside edits, vanished outside-overlay writes,
read-only `.git`, blocked off-allowlist network, and session DB/logs confined to that home.
The empty-CA failure and group-readable credential mode were measured too.

Read from published terms, not executed: the Platform Terms and AUP judgment and data rules
in `devin.md`; the dated SWE-2 availability announcement is vendor-blog grade.
Read from `--help` only: `--sandbox`, export-after-each-turn and the `smart` mode description.
Not measured: `smart` mode, credential rotation, `devin update`, or a paid plan.
The author evaluation used throwaway synthetic content because the Free plan cannot opt out
of training. One run per model per task passed every hidden test, preserved protected files,
reproduced reported test counts and found all planted contradictions; neither flagged the
unspecified case. Those runs are a dated observation, not a ranking.

### 2026-11-16 — Devin on Pro: account state is cached, AGENTS.md is injected

Extended `devin.md` with Pro measurements on devin 3000.12.57, 2026-11-15/16, in the same
srt 0.0.81 lane. Executed: Pro model listing and `swe-2-medium`/`swe-2-high` runs, stale
plan refusal despite Pro status and available models, and recovery after moving four cache
files aside. After the account holder's training opt-out, refreshed the separate telemetry
cache and observed `Telemetry: disabled (zero-data-retention)`. Read from the vendor's
security documentation, not executed by the driver: the web app's Data Controls is the
opt-out location.

Executed: unasked `AGENTS.md` injection into an `always-on` rule, its effect on stdout and
the resumed turn, and resume combining a prompt file, another model, trust override and
export. Added the injection and cross-model resume probes; resume needs the same home.
Extended the author results with the same three synthetic tasks on Pro and the rubric-scored
design task; kept the Free-plan results dated and clarified that Pro content was synthetic too.

**Observed in a second lane, not reproduced here:** bwrap export truncation at compaction,
its repeated-tool-definition bulk, web-tool deny rules that do not cover the shell, leaving
network policy to the outer sandbox, and built-in skills/subagents that the brief must bind. The long design run on a
compiler codebase is also second-lane evidence, including the owner's judgment and the
reproducing citations and measurements alongside the two reasoning errors.

Not measured: the cache refresh timer, quota draw of `Free`-marked models, `smart` mode,
`devin update`, or credential rotation. One run each, not a ranking.

### 2026-11-18 — update step 4 names the stamp and when an example's model id may move

Step 4 said `SKILL.md` changes only when a shape or a trap does. Step 0 stamps it on every pass,
though, and the 2026-10-30 pass moved its runnable examples to current ids, so the procedure
described less than the practice it governs. Found by a cold review of the next refresh, which
had moved an example under that precedent. The step now allows both, and holds the example to a
run that succeeded with the documented result: a run stopped by auth or a quota limit has
executed the command and shown nothing about the model.

### 2026-11-18 — Codex's 6.2 generation takes the default and strong rungs

Updated first, against a previous stamp of 2.1.321 and 0.167.0: the installed Claude Code
2.1.327 was already current, and codex-cli went from 0.169.1 to 0.170.0; both matched at the
end. Then ran `verify.md` top to bottom. Every probe held, and no trap changed,
so `SKILL.md` changed only in its stamp and its runnable Codex example, which moved to
`gpt-6.2-sol` after that exact command ran: exit 0, `OK` in `-o`, the four documented events.
That same run showed no `model:` line on stderr in the `--json` form, as the guide says.

Claude's four aliases map to the same ids as on 2026-11-10. Codex's cache now has thirteen rows:
`gpt-6.2-sol` and `gpt-6.2-astra` are new, and its descriptions call `gpt-6.1-sol` and
`gpt-6-astra` *previous generation*. The routing table follows the descriptions:
`gpt-6.2-sol` for default, and `gpt-6.2-astra` for strong. **The strong row is listing-grade,
not execution-grade**: neither astra model was invoked, and the operator judged a cache row
with a level list sufficient for this pass. Seven ids answered at exit 0 and the bogus control
failed as documented. `gpt-6.1-terra`'s description now names a specialty rather than a rung,
and it stays out of the routing table.

The first config-key run failed on every row but the rejected one, from a subscription usage
limit: exit 1 with the reset time in the message. That matches the documented message and exit
code; the plain output cannot show the `error`-then-`turn.failed` event order, and it says
nothing about the keys. Re-run after the reset gave accepted, accepted, REJECTED, FAILED. An
API-key lane tried in between failed on an expired key and contributed no result. No opt-in
file was re-probed.

A second review, on another model family, found three things this pass then changed. The cache
reader in `verify.md` did not print the descriptions the routing table relies on, so a reader
could not reproduce it; it prints them now. The descriptions in `models.md` were read from the
2026-11-18 cache outside that reader. On 2026-11-19 the amended reader ran against a cache
fetched that day, still thirteen rows, and every row's description matched its note in the table
at the same priority. `models.md` said both ladders continue above `strong`, but Codex's example
was the same model at a higher effort, which its own routing rule calls a dial and not a rung;
it now says only Claude's does. And moving `SKILL.md`'s runnable
example had followed the 2026-10-30 precedent while step 4 of the update procedure said
`SKILL.md` changes only for a shape or a trap. The operator kept the move; the step itself was
corrected in the entry before this one.

### 2026-11-20 — research re-run: quota shapes hold, `MAX_THINKING_TOKENS=0` no longer reliable

Update step 6, by hand, after step 0 (`claude update` found 2.1.329 current, `codex update`
moved 0.170.0 to 0.171.0). Prompted by the second tier pass, which found the quarterly re-run coming due at the end of
November. The figures are recorded in `research.md` beside the sections they re-measure.

Verified by execution:
- Claude's `rate_limit_event` shape holds, and each window now carries a `status`.
  `--output-format json` still has no rate-limit key.
- Codex's rollout shape holds, with a new `limit_name` key. `--ephemeral` still leaves no
  rollout, and statusLine still does not fire under `-p`.
- Per-spawn latency on `haiku` and `gpt-6-luna`.
- **`MAX_THINKING_TOKENS=0` beside `--effort low` read zero thinking on four runs of eight**, so
  it is no longer the reliable lever it was measured as. `verify.md`'s block already asks the
  reader to check `thinking_tokens` rather than trust the knob, so it stands. **`models.md`'s
  sentence saying the variable turns thinking off does not**, and it is left for the next
  update pass's wholesale refresh, per step 3, rather than patched here.

Read, not run: headless-cli from the GitHub API. It is unchanged in every respect the decision
rested on.

**Not re-measured:**
- The Codex pull endpoint. This session's permission layer refused the authenticated call
  before it was sent.
- The `premium` bucket and the 100.0 finding, which need a limit hit.
- Resident-mode latency.
- Everything agy, on terms grounds.

The quota readers did not go stale a second time, so the open question on making them
caller-facing keeps its revisit condition unmet.

### 2026-11-20 — agy refresh: 1.5.13 verified, denied-tool trap holds, resident latency measured

Agy coverage refreshed by an agy session driving agy, completing the research re-run. Update step 0
confirmed `agy update` reports current at 1.5.13 before and after.

Verified by execution:
- Every probe in `agy.md` ran against 1.5.13. The stdin drop when `-p` is passed, the plain-text stdin
  prompt without `-p`, the three loud argv mistakes (exit 2), the quiet bad stream event (exit 0, `init` only),
  and the loud bad model slug (exit 1, `.error`) all hold as documented.
- **The denied-tool trap holds.** Without `--dangerously-skip-permissions`, a tool-using print run exits 0
  with `status: "SUCCESS"`, response `""`, no `.error` key, `.denied_actions` naming `action: "command"`
  (`display_name: "Bash"` on 1.5.13, was `"RunCommand"` on 1.4.2), and the diagnostic on stderr. In
  `stream-json`, status remained `SUCCESS` in both samples. Control with `--dangerously-skip-permissions`
  (either position) executes cleanly and returns output. The three-part success check stands.
- All six model slugs in `agy models` were invoked and answered with exit 0. Effort conflicts and invalid
  effort values exit 1 with `.error`. Ladder stands with `gemini-3.8-flash-low` fast, `gemini-3.8-flash-high` default.
- Per-spawn latency on `gemini-3.8-flash-low` averaged 8.5s wall (7.6–9.7s) with a ~1KB prompt; resident
  `stream-json` measured TTFT 2.4–4.6s and complete 3.0–4.7s.
- Streaming shape holds: text streams inside `step_update` (`step_type == "agent_response"`, `.text_delta`).
- Quota check confirmed none found: neither JSON envelope, stream-json events, nor local config files
  surface quota or rate limits.

Read, not run: Antigravity Additional Terms of Service section 6. The prohibited conduct clauses are
unchanged, leaving the terms judgement date extended.

Not run: none for agy.


### 2026-11-20 — agy refresh review: probes need a plain shell, and the evidence goes back in

A cold review of the agy refresh above, by a session of another vendor that does not drive agy.

**The refresh ran twice.** The first agy session ran inside srt. There, the denied-tool probe
came back with no `.denied_actions` and a tool failure explained in `.response`. That run's
commit rewrote the success check, the trap and the probe to match. The review attributed it to
agy's own sandbox failing to nest under srt, the same shape as Codex's in `sandboxed.md`, so
that nothing was denied and nothing reported a denial. That cause is inferred and was not isolated. The second session ran from a plain shell,
and the trap held as documented. That commit replaced the first, which is not in this history
because it was never sealed. `agy.md` now states the environment beside its stamp and says to
run its probes outside any outer sandbox.

**Evidence restored.** The second commit still deleted the evidence behind two of `agy.md`'s
rules: the twelve-listing drift measurement and the operator's two re-reads (behind *verify a
pinned slug by invoking it*), and the two mid-pass self-update dates (behind *pin the model*).
That was the refresh prompt's doing: it asked for *Models and effort* to be refreshed as a
whole, meaning the values, not the record. The passages are back as they were, with the
2026-11-20 result above them.

**Quota downgraded from none to not yet ruled out.** The refresh saw an internal
`retrieveUserQuotaSummary` call in agy's debug log. Whether `--log-file` records that call's
response was not checked, so the entry above saying nothing was left unrun is not accurate
on this point.

Reasoned and edited by the reviewer; nothing re-executed. A probe of the `--log-file`
question has to come from agy or from a person.

An independent review by another model family found two more things. `models.md` still said
`MAX_THINKING_TOKENS=0` turns thinking off, which the research re-run above had shown false;
leaving it for a wholesale refresh was publishing a known-false claim, so the sentence is now
corrected on its own. The sandbox-nesting cause was stated as measured; it is now marked
inferred. The research entry's "due" is corrected too: the quarter comes round at the end of
November.

### 2026-11-23 — a host-loopback model needs a bridge inside srt

`opencode.md` gained *A local OpenAI-compatible server* and trap 9. Executed on 2026-11-23 with
opencode 2.3.2, srt 0.0.81 and socat 1.8.1.3, against an OpenAI-compatible server on the host
at `127.0.0.1:8080`: every run with `baseURL` at `http://127.0.0.1:8080/v1`, and again at
`http://localhost:8080/v1`, retried with `.error.type` `provider.transport` and
`ECONNREFUSED`, and exited 1 with no turn — with `NO_PROXY` empty and with srt's default, which
lists loopback. In the same sandbox `curl` to that URL returned 200 through srt's proxy. The
documented fix is a `socat` bridge inside the sandbox, forwarding through `HTTP_PROXY` to the
host address; that exact wrapper ran, `curl` to the bridge returned 200, and an opencode smoke
run exited 0 with the shell tool writing and reading a file while `~/.ssh` stayed hidden. The
four task runs used an earlier wrapper that parsed `HTTP_PROXY` with `sed` to the same two
values, so both forms ran.

Read, not measured: the provider block's shape and the comment declaring `limit.input`
required or opencode never compacts; and SQLite's documentation, that WAL mode does not work
over a network filesystem. Reasoned only: why opencode does not send a loopback URL to the
proxy where curl does.

`inkling-2-mini-sq-20` (Inkling-2-Mini at `sq-20`, context 262,144) ran the same three author
tasks and the same design task as `devin.md`'s *How it did as an author*, one run each: 6/6,
15/16 and 5/6, and 7.5 of 8 on the rubric written before the runs. Its two errors the rubric
does not score were WAL mode as a SQLite-on-NFS fallback and a reaper keying on `started_at`
rather than the heartbeat the design defines. Wall times and every hardware-dependent figure
were left out deliberately: they would not reproduce. One run each, not a ranking.

### 2026-11-24 — opencode's read-only lane denies everything, then allows reads

The finding arrived as another session's handoff. Every executed claim below was re-run here on
opencode 2.3.2 before it was kept, in a throwaway home with `--standalone` rather than
the real `~/.config/opencode` that *Verifying this file* assumes; none is the handoff's alone.

Executed: the legacy `permission` object still loads and converts (`bash`→`shell`,
`task`→`subagent`, each deny becoming `{action, resource: "*", effect}`); `opencode debug agents`
prints the effective ruleset, last-match over an allow-all base; and the legacy deny block no
longer holds the lane read-only — the model got `execute` (Code Mode), created a git worktree
through it and renamed its session, while file writes from inside failed. The native
`permissions` array that denies `*` and allows the read tools created no worktree and no file,
and read a file correctly; with `--auto` the shell probe created nothing. Tool lists are the
model's own report, corroborated by those side effects.

The cold review found the gap that mattered most: **a project `opencode.json` or
`.opencode/opencode.json` re-allows what the home denies**, because its rules come later in the
same list. Measured on the ruleset, then fixed: `OPENCODE_DISABLE_PROJECT_CONFIG=1` restored the
denies, and the lane now sets it. Not checked on a `run`, nor what else the variable disables.
The review also measured that a legacy and a native key set together concatenate rather than
override, and the text says so.

Read, not measured: the schema (`permissions` is the ruleset; `provider`, `permission` and
`tools` are deprecated), the bundled source's last-match rule, Code Mode's permission check on
`execute` and each inner tool, and the `write`/`patch`/`apply_patch`→`edit` mapping.

Not measured: the native `providers.…settings.provider` OpenRouter form on a request — the
routing table keeps its legacy-form dates — whether `skill` is refused, a `.env` read or deny,
and `denyWrite` against worktree registration.

*Verifying this file* gained two probes beside the unchanged permission floor: a ruleset check
on `opencode debug agents`, and a worktree probe that now also asserts the run answered and
removes any worktree it made. Each was run as written and against a legacy block as a control:
`deny` ×4 against `allow` for `execute`, and ok against FAIL.
