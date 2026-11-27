# The author lane, for any CLI

These are the stable requirements for an author dispatch under this workflow.
`codex-dispatch.md` records measured Codex behavior. The Codex column below records where its
calls fall short.
For another CLI, map each requirement to that CLI's mechanism using `agent-cli:non-interactive`
(in the `agent-cli` plugin) where it covers the CLI, then run the derived call before relying
on it. Keep perishable flags in the CLI references.

| requirement | why | Codex (codex-dispatch.md) |
|---|---|---|
| **Let the author run build and test commands, confine writes to the repository and temporary space, and prohibit commits and pushes.** | The author produces raw material. The orchestrator owns history. | *The call* documents repo writes and commands. The 2026-08-30 re-verification note quotes a header that also lists temporary space. The role rules in `SKILL.md` prohibit commits and pushes. *Resuming* sets the sandbox by a config key. Its effect was inferred from the key and remains unconfirmed from the resumed run's header. |
| **Never block on an approval prompt, and make a refusal visible.** | An approval prompt can hang an unattended run. A silent refusal can leave a partial change that passes the gates. | *The call* disables approval prompts. *Resuming* documents a visible trust refusal at startup. Visibility of a refusal during a run under that policy, such as a sandbox-denied command, remains undocumented. |
| **Pass the spec on stdin or from a file. Keep the spec out of argv.** | Shell quoting can mangle a spec passed as one argument at any length and let the run proceed. | *The call* — the workflow uses stdin. The section also documents an argv form. |
| **State model and effort explicitly on every call, regardless of configuration.** | The `Assisted-by:` trailer must name the exact model. Leaving either setting to a config file or default can silently change the run. | *Model and effort — stated on every call* — requires both on dispatch and resume. |
| **Fail the run on an unknown setting.** | A silently dropped key can leave the author running under defaults nobody chose. | *Model and effort — stated on every call* — documents rejection of an unknown configuration key before a turn. |
| **Write the report to a file outside the tree, apart from stdout.** | The report stays out of the diff and can be read without parsing a transcript. | *The call* writes the final message separately. The caller must choose an outside path. *Resuming* infers from the option being opt-in that omitting it leaves an existing report in place. That case was left untested. |
| **Name the working directory when launching the call.** | An author started elsewhere writes elsewhere. | *The call* — names the repository on initial dispatch. *Resuming* sets it through the launcher's own working directory. |
| **Resume the same session for follow-up specs on the same unit.** | The author keeps the unit's context without re-deriving it. | *Resuming* documents a 2026-08-22 run in which resuming by explicit session ID carried over the first run's context. |
| **Confirm each setting from the run's own output where the CLI prints it, and record it as unconfirmed otherwise.** | Passing a setting gives no evidence that it took effect. | *Model and effort — stated on every call* shows model, sandbox and effort in the plain run's header on stderr only. Model and effort are absent from the JSON stream and report file. *Resuming* leaves the resume sandbox unconfirmed. |

Treat each shortfall as a known gap to watch or cover explicitly, for example with an outer
sandbox or the reviewer's own checks.

## Deriving a dispatch for another CLI

1. For each requirement, find the CLI's mechanism in `agent-cli:non-interactive`. Where that
   skill does not cover the CLI, consult the CLI's own documentation and record what you learn
   as read until you run it.
2. Record any requirement the CLI cannot meet and what stands in for it. For example, use an
   outer sandbox to constrain writes or have the reviewer check the branch for commits it did
   not make.
3. Run the derived form once on a throwaway unit. Check each requirement against the run's
   output and record any setting the output leaves unconfirmed. A form based on `--help` alone
   is a hypothesis. The blocks in `codex-dispatch.md` were rewritten twice on 2026-08-22 after
   execution exposed failures.
4. Keep the derived form with the date and the CLI version used for the run. If it ships,
   publish it as a measurement in `agent-cli:non-interactive`.
