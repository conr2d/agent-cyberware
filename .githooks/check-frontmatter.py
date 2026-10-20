#!/usr/bin/env python3
"""Refuse the one frontmatter defect this repository has actually shipped.

A skill's description carried an unquoted `condition: ` — a colon and
a space inside a plain YAML scalar — from the day the skill was written. YAML reads
that second colon as another key, so the frontmatter is invalid. Two runtimes parsed
it leniently and loaded the skill; a third refused the document and dropped the skill
**with no error, no warning and no missing-skill notice**, and every check inside this
repository still passed. It was found by asking that runtime to name every skill it
could see and noticing that the name was not in the answer.

    check-frontmatter.py           check every `SKILL.md` here; exit 1 on a hit, 2 if
                                   it could not run
    check-frontmatter.py <root>    check a tree other than this one (the hook runs the
                                   copy inside a checkout of the index)

Four rules about content, and no more:

    1. the file opens with a line holding exactly `---`, and the frontmatter ends at
       the next such line;
    2. no line inside it is indented — a wrapped or nested value is where two parsers
       stop agreeing;
    3. a value holds no second `: ` and does not end in `:`;
    4. the file carries none of YAML's four invisible line breaks — a lone carriage
       return, U+0085, U+2028, U+2029. A `\\r\\n` pair is ordinary and allowed.

Plus one rule about the file rather than its content: a `SKILL.md` that is a symlink
is refused unread, so the bytes checked are the bytes committed.

**This is not a YAML parser and does not try to be.** An earlier version did try, and
over five cold reads it never came back clean: one round found it refusing *every*
commit, and four landed a `SKILL.md` it passed and a parser rejects. Two of those were
holes in its rules; the rest were places where a Python string operation and YAML
disagree about what a *line* is, or about which files get looked at at all. Rule 4 is
there because that second kind is the failure mode itself: one invisible break makes
the checker read a single line where the parser reads two, and every other rule then
runs on the wrong text.

So the surface is deliberately small. A quoted value, a leading indicator, a control
character, a missing `name:` — all real ways to break a frontmatter, none of them
anything this repository has been bitten by, and every one of them another rule that
would have to be got right. What is left is the defect that shipped, plus the minimum
needed for the rules to see the lines a parser sees. What it does not cover, it does
not claim.
"""
import re, subprocess, sys, pathlib

FENCE = "---"
INVISIBLE = re.compile("[\r\u0085\u2028\u2029]")


def offences(text):
    text = text.replace("\r\n", "\n")
    m = INVISIBLE.search(text)
    if m:
        return [(1, f"U+{ord(m.group()):04X} splits a line where nothing shows it — YAML reads "
                    "two lines here, a reader sees one, and a diff shows neither")]
    lines = text.split("\n")
    if not lines or lines[0] != FENCE:
        return [(1, "no frontmatter: a SKILL.md opens with a line holding exactly ---")]
    end = next((i for i, l in enumerate(lines[1:], start=1) if l == FENCE), None)
    if end is None:
        return [(1, "the frontmatter is never closed by a --- line")]

    out = []
    for n, line in enumerate(lines[1:end], start=2):
        if not line.strip(" "):                # empty, or spaces: the only blank YAML takes here
            continue
        if line[0] in " \t":
            out.append((n, "indented: keep the frontmatter flat, one line per key — a wrapped "
                           "or nested value is where parsers stop agreeing"))
            continue
        key, sep, value = line.partition(": ")
        value = value.strip()
        if sep and (": " in value or value.endswith(":")):
            out.append((n, f"`{key}:` holds a colon — YAML reads it as a second key. Rewrite the "
                           "value; do not quote it, since quoting is the habit that keeps the "
                           "colon and brings its own parse errors"))
    return out


def skill_files(root):
    """Every `SKILL.md` under `root`.

    `git ls-files` when there is a repository, and a walk of the tree when there is not.
    The walk is not the exceptional path: the hook checks a `git checkout-index` copy, which
    is not a repository, so the walk is what runs on every commit. Whatever is in that copy is
    what is being committed, so nothing there may be filtered out.
    """
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "*/SKILL.md", "SKILL.md"],
                             capture_output=True, text=True)
        if out.returncode == 0 and out.stdout:
            return [root / p for p in out.stdout.split("\0") if p]
    except (OSError, UnicodeDecodeError):
        pass                                   # no git on the path, or a path git cannot decode
    # `or p.is_symlink()` so a broken link is reported rather than skipped: it is a
    # file no runtime can read, and skipping it is how it would reach one.
    return [p for p in sorted(root.rglob("SKILL.md")) if p.is_file() or p.is_symlink()]


def main():
    if len(sys.argv) > 2:
        print("usage: check-frontmatter.py [<root>]", file=sys.stderr)
        return 2
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1
                        else pathlib.Path(__file__).resolve().parent.parent)
    if not root.is_dir():
        print(f"frontmatter check: {root} is not a directory", file=sys.stderr)
        return 2
    root = root.resolve()

    problems = []
    for path in skill_files(root):
        rel = path.relative_to(root)
        if path.is_symlink():                  # ...so the file checked is the file committed
            problems.append(f"{rel}: is a symlink")
            continue
        try:
            # `newline=""` because the default translates a lone `\r` to `\n` before any rule
            # sees it — the same class of disagreement rule 4 exists to catch.
            with path.open(encoding="utf-8", newline="") as fh:
                text = fh.read()
        except (OSError, UnicodeDecodeError) as e:
            print(f"frontmatter check: {rel} is unreadable ({e.__class__.__name__})",
                  file=sys.stderr)
            return 2
        problems += [f"{rel}:{n}: {why}" for n, why in offences(text)]
    for p in problems:
        print(f"frontmatter check: {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
