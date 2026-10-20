# Getting the current truth yourself

> **Updating this skill rather than just using it? Read `maintenance.md` in this
> directory first** — it carries the editorial rules, the reasoning behind each judgment
> call, and the re-verification checklist.

Every fact in `../SKILL.md` and `models.md` came from one of the commands below. Run the
relevant one instead of trusting a cached value.

Scope: the two CLIs in `../SKILL.md`, on a bare machine. **`opencode.md`, `hermes.md`,
`grok.md`, `sandboxed.md` and `agy.md` each carry their own probes**, deliberately not here — a
standard pass does not run them, and their facts going stale does not make this file wrong. Run
those when opencode, hermes, grok, an outer sandbox, or agy is what you are checking.

## Versions

```sh
claude --version && codex --version
```

## Model catalogs

```sh
# Claude — which alias resolves to which id. `--help` names a few aliases as examples and no
# ids at all, so it cannot answer this; the envelope can, for the price of one haiku turn.
for a in haiku sonnet opus fable; do printf '%-8s ' "$a"
  echo hi | claude -p --output-format json --model $a --no-session-persistence \
    | python3 -c "import json,sys; print(' '.join((json.load(sys.stdin).get('modelUsage') or {}).keys()))"
done

# Codex — the cache the CLI itself reads. Any run that gets past the trust check rewrites it
# (`codex exec`, `codex exec resume`) — including one whose turn then fails, so a completed
# turn is not what triggers the write. `--version`, `--help`, `exec --help`, a run stopped by
# the trust check, and reading it the way this block does all leave it byte-identical. Start a
# session first if you need it current, and read the fetched_at this prints before trusting a
# row. A fresh fetched_at does not make the listing complete — see below.
python3 -c "
import json; d=json.load(open('$HOME/.codex/models_cache.json'))
print('fetched_at:', d['fetched_at'])
for m in d['models']:
    print(m['priority'], m['slug'], '|', m['display_name'],
          '|', [l['effort'] for l in m['supported_reasoning_levels']])
"
```

**The cache is a listing, not a contract, so absence from it settles nothing.** Verify a slug by
invoking it:

```sh
for m in <slug-you-mean> no-such-model-9x; do
  printf '%-20s ' "$m"
  echo "Reply with exactly: OK" | codex exec - -m "$m" --json --strict-config \
      -c approval_policy=never >/tmp/m.jsonl 2>/dev/null
  echo "exit=$?  $(grep -o 'Model metadata for `[^`]*` not found' /tmp/m.jsonl || echo 'no warning')"
done
# expected: a real id — exit 0, no warning, even when the block above gave it no row.
#           the bogus one — exit 1, the metadata warning as an error item on stdout.
```

The control is the point: a clean exit 0 means the model answered, and an id the binary has no
metadata for cannot reach one. `models.md` carries what this returned on 2026-10-19: two ids the
listing omits that run, and one it dropped that no longer does.

## Whether a Codex config key is real

`-c` silently accepts unknown keys; `--strict-config` rejects them. This is the only way to
tell a working override from a no-op. A key counts as accepted only when the run also
succeeded — a run that fails for any other reason (auth, quota, a bad value) says nothing
about the key, and the last row is the control that proves the third branch is reachable:

```sh
for k in 'model_reasoning_effort="low"' 'approval_policy=never' 'suspected_key=1' \
         'model="no-such-model-9x"'; do
  out=$(echo hi | codex exec - --skip-git-repo-check --strict-config -c "$k" 2>&1); rc=$?
  if grep -q 'unknown configuration field' <<<"$out"; then echo "REJECTED  $k"
  elif [ "$rc" -eq 0 ]; then echo "accepted  $k"
  else echo "FAILED($rc) $k  (says nothing about the key)"; fi
done
# expected: accepted, accepted, REJECTED, FAILED
```

## Behaviour probes

These assert the traps in `../SKILL.md` still hold. Each should reproduce the documented
failure; if one stops failing, the trap has been fixed and the guide needs an edit.

```sh
# codex: refusal outside a git repo — needs a directory with no .git ABOVE it either.
# $TMPDIR is the wrong place: one stray `.git` there — an empty directory that git itself
# rejects still counts — marks every mktemp dir trusted and this probe passes silently.
cd "$(TMPDIR=/var/tmp mktemp -d)" && echo hi | codex exec - >out.txt 2>err.txt
echo "exit=$?"; wc -c out.txt; cat err.txt
# expected: exit 1, out.txt 0 bytes, message on stderr

# claude: does a caller-pinned session id survive a resume round trip?
# Do NOT phrase this as "remember X" — see the note below the block.
SID=$(uuidgen)
echo "The code word is LARCH. Reply with exactly: OK" \
  | claude --session-id "$SID" -p --output-format json --model haiku \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['session_id'])"
echo "What was the code word? Reply with that word only." \
  | claude --resume "$SID" -p --output-format json --model haiku \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['result'])"
# expected: first prints $SID, second recalls the word
```

**A `-p` subprocess can write to the invoking project's memory, and the envelope never says
so.** The probe above asked the author to *remember* a word until 2026-10-03, and the run
persisted it as a memory file in the project the driver was invoked from — exit 0, nothing on
either stream, no field in the envelope naming the write. Running this pass therefore left a
junk entry behind, which is how the behaviour was found. The phrasing is now declarative for
that reason. **A driver whose prompts carry anything memory-shaped should expect the same**, and
the only place the write shows is the project's own memory directory.

## Output envelopes

To re-derive the field lists in `../SKILL.md`:

```sh
echo hi | claude -p --output-format json --model haiku --no-session-persistence \
  | python3 -c "import json,sys; print(sorted(json.load(sys.stdin)))"

echo hi | codex exec - --json --skip-git-repo-check \
  | python3 -c "
import json,sys
for l in sys.stdin: print(json.loads(l).get('type'))"
```

Note `claude --output-format stream-json` requires `--verbose`, and emits additional event
types the single-object `json` form does not.

## Latency, if it matters for your caller

Numbers rot faster than anything else here; measure rather than cite. Claude's envelope
already splits first token from the whole turn, so this needs no stream:

```sh
# one call, thinking off — compare against your own budget
MAX_THINKING_TOKENS=0 \
  claude -p --output-format json --model haiku --effort low < prompt.txt \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print("ttft", d["ttft_ms"], "total", d["duration_ms"], d["usage"]["output_tokens_details"])'
```

`ttft_ms` is first token and `duration_ms` the whole turn; **startup is whatever wall time
remains beyond `duration_ms`**, and it is proportional to what the invoking user has
installed, not to the model. Read `thinking_tokens` back as `0` to confirm the knob applied
— `--effort low` on its own does not get you there.
