# Research kept out of the guide

Measurements and investigations behind decisions `../SKILL.md` does not carry — why a flag is
not documented, why a recommendation reads the way it does, what was compared and declined.
**Nothing here is invocation knowledge.** A caller driving one of these CLIs never needs this
file; it exists so that a maintainer re-deriving one of those decisions finds the evidence
instead of the conclusion.

**These sections have no probes, and that is deliberate — it also makes them cheap to leave
stale.** `maintenance.md`'s update procedure carries a step that re-runs them by hand, which is
a calendar reminder where a probe would be a test. Being out of the guide makes a claim cheap to
leave wrong, not exempt from being wrong: on 2026-08-27 the quota section was found wrong about
both CLIs it documents.

Split out of `maintenance.md` on 2026-08-30, where it had reached about half the file that a
maintainer is told to read before every edit.

### Streaming-input mode and `--bare`, re-explored and re-rejected (2026-08-20)

Both had been documented once and removed as flag-catalog bloat. They were re-examined
because a caller needed a non-interactive call fast enough for a person to watch, and the same
conclusion held for a second reason: the flags are `--help`'s job, but **their silent
failures are not**, so only the traps went into the guide — and of those, only the ones a
reader of the guide can actually reach stayed there (see the reachability corollary in
`maintenance.md`; `--bare`'s did not).

What was measured, on one machine, Claude Code 2.1.237 / Codex 0.147.0 / agy 1.1.14, with a
~1KB prompt and a three-sentence answer. Treat as an order-of-magnitude record, not a
current value — re-run `verify.md`'s latency snippet before citing any of it.

| | TTFT resident | complete resident | TTFT per-spawn | complete per-spawn |
|---|---|---|---|---|
| `claude --model haiku --effort low` | 1.16s | 2.86s | 2.43s | 4.52s |
| `agy --model gemini-3.7-flash-low` | 1.41s | 1.61s | — | 10.47s |
| `codex --model gpt-5.6-luna` effort low | — (no duplex) | — | 5.41s | 6.32s |

Findings behind the judgment calls:

- **`MAX_THINKING_TOKENS=0` was the single largest lever** — 6.5s → 2.9s. `--effort low`
  still spent 516 thinking tokens, and `MAX_THINKING_TOKENS=1` is not a cap that rounds
  down: it still spent 221. The line went to `models.md` because that is where a reader
  picks an effort level and would otherwise assume `low` buys less thinking — not on the
  stable/rotting split, which would have argued for `../SKILL.md`.
- **Claude's per-call startup is ~2.0s of config, plugin, hook and MCP loading**, not Node
  boot, which is 0.15s (`claude --version`). It is therefore proportional to what the
  invoking user has installed. Codex boots in 0.03s, agy in 0.14s.
- **Replacing the system prompt is not the optimisation it appears to be.** The default is
  ~33k tokens but served entirely from cache; a custom `--system-prompt-file` is cold on
  first use and only reaches parity once warm (2.2s vs 2.7s, inside the noise). It does not
  remove the tool definitions either — `cache_read` was still 26,884 afterwards. Documented
  nowhere in the guide, because "this thing you might try does not help" is not a trap.
- **Conversation state accumulates at very different rates.** Over six similar turns Claude
  grew ~600 tokens per turn; agy went 14k → 29k → 45k → 62k → 73k. Left out of the guide:
  it matters only to a resident driver, which the guide does not describe.
- **agy streams text inside `step_update`** (`step_type == "agent_response"` → `.text_delta`)
  rather than as a distinct delta event. A detector written against Claude's shape reports
  "agy does not stream", which is wrong; that error was made and corrected here.

Two measurement pitfalls, if this is ever redone: do not give the child `stderr=PIPE` and
read it only after `wait()` — `--verbose` fills the 64KB buffer and the child blocks forever;
and detect first-token per CLI rather than generically, for the reason just above.

### Comparison with `RobertTLange/headless-cli` (checked 2026-08-16)

Apache-2.0, TypeScript, ~310 commits, v0.6.1, 8 agents, plus Python SDK, Docker/Modal,
cron, and tmux session management. It independently encodes nearly every trap documented
here — `--skip-git-repo-check`, pinned `--session-id`, `exec resume`, agy's inline-prompt
requirement, `--print-timeout` forwarding — and it had `model_reasoning_effort` right.

It is **subscription-first, not API-key-first**: it unsets `ANTHROPIC_API_KEY` for the
child process when OAuth exists (opt into API with `HEADLESS_CLAUDE_AUTH=api`), seeds OAuth
credentials into Docker/Modal containers for every agent, and distinguishes
`native-reported` cost from `api-list-price-estimate` because the latter "is not actual
subscription spend".

Its built-in model defaults lag (`claude-opus-4-6`, `gpt-5.5`, `gemini-3.1-pro-preview`),
though its docs do tell users to pass `--model` explicitly. Decision: no upstream
contribution, and no competing tool. The two projects occupy different positions — it is a
wrapper, this is a guide — and they are complementary.

### Subscription quota is reachable non-interactively, for two of three

Investigated because a driver running against a subscription is bound by rate-limit windows
rather than dollars, and no wrapper surfaces them. Deliberately left out of `../SKILL.md`:
it is runtime telemetry, not invocation knowledge, and both formats are undocumented
internals that can change without notice — which they since did, in both directions. **Both
shapes below were re-measured 2026-08-27 on Claude Code 2.1.247 / Codex 0.150.1 / agy
1.1.22**, and the previous revision of this section was wrong about each of them.

| CLI | Path | Fields |
|---|---|---|
| **Codex** | `~/.codex/sessions/YYYY/MM/DD/rollout-<ts>-<thread_id>.jsonl`, `token_count` payload → `rate_limits` | `limit_id`, `primary` / `secondary` → `{used_percent, window_minutes, resets_at}` (300 = 5h, 10080 = 7d), `plan_type`, `credits{has_credits,unlimited,balance}`, `individual_limit`, `spend_control_reached`, `rate_limit_reached_type` |
| **Codex, pull** | `GET https://chatgpt.com/backend-api/wham/usage`, bearer `.tokens.access_token` and header `ChatGPT-Account-Id: .tokens.account_id` from `~/.codex/auth.json` | `plan_type`, `rate_limit.{allowed, limit_reached}`, `rate_limit.{primary,secondary}_window` → `{used_percent, limit_window_seconds, reset_after_seconds, reset_at}` |
| **Claude** | `-p --output-format stream-json --verbose` → `rate_limit_event` → `.rate_limit_info` | `status`, `rateLimitType`, `resetsAt`, `overageStatus`, `overageDisabledReason`, `isUsingOverage`, and `unifiedWindows.{five_hour,seven_day}.{utilization, resetsAt}` |
| **agy** | none found, still | — |

**Codex nested its windows.** `used_percent`, `window_minutes` and `resets_at` are no longer
directly under `rate_limits`; they sit inside `primary` (5h) and `secondary` (7d). Code
written against the old flat shape reads `None` and reports no limit rather than failing.

**Codex only writes the numbers on a run that completes a turn.** A run that fails on the
usage limit writes a *different* bucket — `limit_id: "premium"` with `primary`, `secondary`
and `plan_type` all null — instead of the populated `limit_id: "codex"`. Verified by
outcome, not by model: on 2026-08-27, two runs seconds apart at 05:58 and 05:59 completed and
wrote `codex` with figures, and the three that failed immediately after wrote `premium` with
nulls. So a driver cannot learn from the rollout that it is blocked; it learns that from the
error. **Absence of figures in the rollout is not evidence of headroom.**

**The pull endpoint answers that question without running anything** (2026-08-29). The row above
is the same figures on demand — no turn to complete, no run to spend — plus two booleans the
rollout has no equivalent of, `allowed` and `limit_reached`, which is what a pre-flight gate
actually wants. Same undocumented-internal grade as the rollout shape, and **the same integer 1 % resolution**: a dispatch costing under a percent reads
as zero on both, so the endpoint buys availability, not precision. What it removes is the trap
directly above — a driver can now ask before it dispatches rather than infer from a failure.

**And `used_percent: 100.0` is not a hard gate.** Both of those successful runs reported
primary at 100.0 with `resets_at` still 20 minutes out. Failures cluster there but are not
implied by it, so a pre-emptive threshold has to sit well below 100 and cannot be a
`== 100` test.

**Claude now reports utilization, which reverses this section's old conclusion.**
`unifiedWindows` carries `five_hour.utilization` and `seven_day.utilization` as fractions
(0.03 = 3 %, *not* a percentage) with a `resetsAt` each. The previous revision said Claude
exposes **no percentage** non-interactively and that the real figures lived only in the statusLine
payload — that is now false, and pre-emptive throttling works on both CLIs. Note the event
appears only in `stream-json`; `--output-format json`'s single object carries no rate-limit
key at all, checked.

Mechanics, all still holding: the rollout filename embeds the `thread_id` from
`thread.started`, so correlation is trivial (re-confirmed against a live run). `rate_limits`
rides on `token_count`, emitted at turn completion — an aborted run, including one killed by
closing the stdout pipe early, writes none. `--ephemeral` removes the file entirely
(re-verified: rollout count unchanged across an `--ephemeral` run, even one that failed).
statusLine still does **not** fire in print mode, re-tested by injecting one via `--settings`
and having it touch a file; it never ran. That fact now only matters as a dead end to not
go down, since the figures it once uniquely held are in the event stream.

