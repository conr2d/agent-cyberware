# Models and effort tiers

Cached recommendations. **The alias, cache and slug readings below are from 2026-11-10**; the
effort and fast-mode notes carry no newer measurement. All of it will rot — if a
suffix matters, re-read them from the CLI first (`verify.md`).

## Claude Code — `--model <alias|id>`

Re-read on 2026-11-10 with Claude Code 2.1.321 using `verify.md`’s alias loop and
`modelUsage`. `fable` moved from `claude-fable-5-1` to `claude-fable-5-2`; the other three are
unchanged since 2026-10-19.

| Alias | Full ID |
|---|---|
| `opus` | `claude-opus-5-5` |
| `sonnet` | `claude-sonnet-5-5` |
| `haiku` | `claude-haiku-5-5` |
| `fable` | `claude-fable-5-2` |

Aliases are stable while the full IDs roll forward, so prefer the alias unless you need to pin
an exact build. Three of the four rolled between 2026-08-31 and 2026-10-03, `haiku` followed by
2026-10-19, `fable` by 2026-11-10, and no alias moved. `fable` is the Mythos-class tier above Opus. **Each row was
read back from `modelUsage` in the `json` envelope of a real run**, which is the cheapest
source that states the mapping — `--help` names three aliases as examples and no ids at all, so
it cannot produce this table.

Effort is a separate flag: `--effort low|medium|high|xhigh|max`. Effort does not gate
thinking; `MAX_THINKING_TOKENS=0` does, and it is the larger lever on latency.
`CLAUDE_EFFORT` in the environment does **not** select effort — Claude Code emits that
variable, exposing the current turn's effort to hook commands and Bash-tool children, and
never reads it back. A driver spawned from inside Claude Code inherits it and must still
pass `--effort` to choose anything.
`--fallback-model <comma-list>` sets an overload retry chain (print mode only).
Fast mode is interactive-only; in non-interactive JSON it reports
`fast_mode_state:"off"`, `fast_mode_disabled_reason:"sdk_opt_in_required"`.

## Codex — `-m <id>` or `-c model="<id>"`

Read from `~/.codex/models_cache.json` with `verify.md`’s cache reader on 2026-11-10, under
codex-cli 0.167.0, `fetched_at` the same day. The ids and descriptions match 2026-10-30; the
priorities are now one to eleven with no ties:

| Priority | ID | Note |
|---|---|---|
| 1 | `gpt-6.1-sol` | latest workhorse model for coding and everyday work |
| 2 | `gpt-6-astra` | frontier intelligence for the most demanding work |
| 3 | `gpt-6-chat-thinking` | GPT-6 Chat Thinking for the paid CCA experiment |
| 4 | `gpt-6.1-terra` | GPT-6.1 Terra Codex model; description names no tier |
| 5 | `gpt-6-sol` | previous generation workhorse model |
| 6 | `gpt-reserve` | fast and affordable agentic coding model |
| 7 | `gpt-6-luna` | fast and affordable model for easier tasks |
| 8 | `gpt-5.6-sol` | older generation workhorse model |
| 9 | `gpt-5.6-terra` | older balanced model for straightforward work |
| 10 | `gpt-5.6-luna` | older fast and efficient model |
| 11 | `codex-auto-review` | automatic approval review model for Codex |

**Priority numbers do not follow the tiers.** The workhorse sorts above the frontier model.
Read the cache's descriptions, not its integers, to choose a tier.

**A model absent from the cache may still run.** The rows with a priority are the local cache,
and the cache is a listing rather than a contract: on 2026-10-19, with a `fetched_at` minutes
old, `gpt-6.1-sol` and `gpt-6-astra` carried no row there and each returned a completed turn at
exit 0 with no fallback-metadata warning, as two ids left unnamed had on 2026-10-03. Both
`gpt-6.1-sol` and `gpt-6-astra` have cache rows as of 2026-11-10.
An id the binary genuinely does not know is loud instead — exit 1, `Model metadata for ... not
found. Defaulting to fallback metadata` as an error item on stdout, then a 400 from the server.
**So settle a slug by invoking it, not by its absence here**, and do not read a dropped row as
a retirement. `gpt-5.5` left the cache between 2026-10-03 and 2026-10-19 and *was* re-probed:
exit 1, the fallback-metadata warning, then a 400 reading *"The 'gpt-5.5' model is not
supported when using Codex with a ChatGPT account"* — retired for a subscription login,
measured, and not checked under an API key. `gpt-5.4` and `gpt-5.4-mini` left on 2026-10-03 and
were not re-probed, so their status is unknown rather than removed. The same goes for
`gpt-5.3-codex`, `gpt-5.2-codex`, `gpt-5.2`, `gpt-5.1-codex-max` and `gpt-5.1-codex-mini`,
which a previous pass recorded as unusable on the strength of their absence alone.

On 2026-11-10, `verify.md`’s slug probe with a ChatGPT sign-in returned exit 0 and no metadata
warning for `gpt-6.1-sol`, `gpt-6-chat-thinking`, `gpt-6.1-terra`, `gpt-6-sol`, `gpt-reserve`
and `gpt-6-luna`. The control `no-such-model-9x` returned exit 1 with `Model metadata for ...
not found`. `gpt-6-astra` was not invoked in this pass; it last returned `OK` on 2026-10-30.
The 5.6 family and `codex-auto-review` have not been invoked.

Effort — `-c model_reasoning_effort=<level>`, per the same 2026-11-10 cache's own
`supported_reasoning_levels`:

| Models | Levels |
|---|---|
| `gpt-6.1-sol`, `gpt-6-astra`, `gpt-6.1-terra`, `gpt-6-sol`, `gpt-5.6-sol`, `gpt-5.6-terra` | low, medium, high, xhigh, max, **ultra** |
| `gpt-6-chat-thinking`, `gpt-reserve`, `gpt-6-luna`, `gpt-5.6-luna`, `codex-auto-review` | low, medium, high, xhigh, max |

`ultra` means maximum reasoning plus automatic task delegation. A model with no row in the
cache has no published level list either, so an effort passed to one is unchecked — the
stderr header is where the value that applied is named.

Subscription quota is enforced per account and surfaces mid-run, not at launch: the turn
comes back as an `error` event followed by `turn.failed` with a reset time in the message,
exit 1. Model choice does not route around it.

## Complexity-hint routing

For a driver that classifies work as fast / default / strong:

| Hint | Claude | Codex |
|---|---|---|
| `fast` | `haiku` | `gpt-6-luna` (or `gpt-reserve`) |
| `default` | `sonnet` | `gpt-6.1-sol` |
| `strong` | `opus` | `gpt-6-astra` (last invoked 2026-10-30) |

**Each tier picks a model, on both.** Every vendor ships its own three-rung ladder and the
hint maps onto it directly — Codex's cache descriptions name *frontier, most demanding* /
*workhorse, everyday work* / *fast, affordable*. `gpt-6.1-terra` is left out of this routing
table because its description names no tier. Routing a tier by holding the model fixed and
moving effort throws that distinction away and substitutes a guess for it.
**The third vendor measured here agrees and is no longer in this table**: agy's ladder is in
`agy.md`, which left the guide on terms grounds rather than because the pattern broke.

**Effort is a second, orthogonal dial, and both expose one** — `--effort` on Claude,
`-c model_reasoning_effort=` on Codex. Use it to trim cost and latency *within* a tier, and
keep it free for whatever second knob the driver needs. It is not the tier mechanism.

**Both ladders continue above `strong`.** Claude's `fable` sits above `opus`, and
`gpt-6-astra` accepts `ultra` — maximum reasoning plus automatic task delegation. A driver
with a fourth hint has somewhere to send it.

The two-axis structure outlives the slugs, which have rolled repeatedly: **pick the rung,
then trim within it.** Swap the names, keep that.
