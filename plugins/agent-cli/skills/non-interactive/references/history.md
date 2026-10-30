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
