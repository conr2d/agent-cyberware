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
