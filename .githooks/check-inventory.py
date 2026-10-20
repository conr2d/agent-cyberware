#!/usr/bin/env python3
"""Refuse a `SKILL.md` section that has no row in its skill's section inventory.

`SKILL.md` is paid on every invocation. Whether a passage has earned that is decided
by the admission tests — is this skill the only carrier of it, can a reader following
it reach the situation, does it have a shelf life — and those tests were being applied
by whoever remembered to apply them. The session adding a feature is the one least
likely to remember, which is how a skill grows a section at a time into a reference
nobody meant to write.

So the test gets an artifact. Every skill's `references/maintenance.md` carries a
`## Section inventory` — a table with one row per `## ` section of its `SKILL.md`,
saying why this skill is that section's only carrier. Adding a section without a row
stops being committable, and writing the row is the moment the test gets applied.

    check-inventory.py            check every skill under this tree; exit 1 on a
                                  section with no row, or a row naming no section
    check-inventory.py <root>     check a tree other than this one (the hook runs
                                  the copy inside a checkout of the index)

**What it cannot do.** It sees that a row is present and that its first cell names a
real section. It cannot see whether the row is *true* — "needed" satisfies it exactly
as well as a real argument does. That is the same limit the citation checker records
about itself, and for the same reason: a sentence can be false in a way no regex sees.
The gate supplies the occasion; an `agent-skill:tiered` pass is what reads.

Kept deliberately small, per the lesson the frontmatter checker records. It compares
two lists of strings and does nothing else. It does not parse Markdown beyond skipping
fenced blocks, does not judge a row's contents, and has no exemptions — an exemption is
where the defect would live.
"""
import re, sys, pathlib

FENCE = re.compile(r"^\s*(?:```|~~~)")
SEPARATOR = re.compile(r"^\|[\s:|-]+\|$")


def normalise(text):
    """A heading and a table cell are the same section when they read the same.

    Backticks, bold markers and surrounding space are formatting, not identity, so a
    row may write a section's name however the table reads best.
    """
    return re.sub(r"\s+", " ", text.replace("`", "").replace("*", "")).strip()


def sections(path):
    out, in_fence = [], False
    for line in path.read_text(encoding="utf-8", errors="replace").split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence and line.startswith("## "):
            out.append(normalise(line[3:]))
    return out


def inventory(path):
    """The first column of the table under `## Section inventory`, or None if absent.

    None and an empty list are different answers: a file with no inventory at all has
    not been brought under the rule, and says so differently from one whose table has
    lost its rows.
    """
    if not path.exists():
        return None
    rows, in_section, in_fence, seen_table = [], False, False, False
    for line in path.read_text(encoding="utf-8", errors="replace").split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## "):
            in_section = normalise(line[3:]) == "Section inventory"
            continue
        if not in_section:
            continue
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        seen_table = True
        if SEPARATOR.match(stripped):
            continue
        cell = normalise(stripped.strip("|").split("|")[0])
        if cell.lower() != "section":            # the header row
            rows.append(cell)
    return rows if seen_table or in_section else None


def check(skill, root):
    rel = skill.relative_to(root)
    maint = skill.parent / "references" / "maintenance.md"
    rows = inventory(maint)
    if rows is None:
        return [f"{rel}: no `## Section inventory` in {maint.relative_to(root)} — "
                "every skill carries one, with a row per section"]
    have = sections(skill)
    bad = [f"{rel}: section `{s}` has no row in the inventory — "
           "say why this skill is its only carrier, or cut the section"
           for s in have if s not in rows]
    bad += [f"{maint.relative_to(root)}: inventory row `{r}` names no section of "
            f"{rel.name} — a section was renamed or removed and its row was not"
            for r in rows if r not in have]
    return bad


def main():
    if len(sys.argv) > 2:
        print("usage: check-inventory.py [<root>]", file=sys.stderr)
        return 2
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1
                        else pathlib.Path(__file__).resolve().parent.parent)
    if not root.is_dir():
        print(f"inventory check: {root} is not a directory", file=sys.stderr)
        return 2
    root = root.resolve()
    skills = sorted(root.glob("plugins/*/skills/*/SKILL.md"))
    if not skills:
        print(f"inventory check: no skill found under {root}", file=sys.stderr)
        return 2
    problems = [p for s in skills for p in check(s, root)]
    for p in problems:
        print(f"inventory check: {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
