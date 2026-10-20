#!/usr/bin/env python3
"""Refuse line numbers in tracked Markdown.

A line number written into prose rots on every edit above it. `AGENTS.md` says
what rots does not go in the document — the command that prints it does. So no
document here writes one. Name the section instead, or say the number in words if
you are quoting a past value.

    check-citations.py            check the tracked `.md` files, or every one in the
                                  tree when there is no repository; exit 1 on a hit
    check-citations.py --show     print each skill's shape, for reading
    check-citations.py <root>     check a tree other than this one (the hook runs
                                  the copy inside a checkout of the index)

Refused, anywhere in a tracked `.md`:

    `:27-52`                a bare line citation
    SKILL.md:27             a file:line citation, backticks or not
    #L27-L52                a line anchor
    line 27 / lines 27-52   a line reference in words
    "…181 lines…"           a line-count claim, where the paragraph — or the sentence
                            introducing the table — says `SKILL.md`, "this skill", or a
                            skill's own name

A line containing `citation check:` is skipped, so a document can quote what the gate
prints.

`--show` prints what a maintainer would otherwise be tempted to write down. It is
deliberately **not** pasteable — there is no marker, nothing compares its output to
anything, and nothing in any document is derived from it. Read it, then write prose.

**Why it is this small.** Five earlier designs tried to *keep* the numbers and
verify them: check a hand-written paragraph, then generate the paragraph and
compare it byte for byte. Six independent reviews found roughly twenty ways
through, several landed as real commits — a renamed skill file, a symlink out of
the repository, a permuted table, and four separate corners of CommonMark fence
syntax, because deriving a heading structure means reimplementing a Markdown
parser and losing to it. The numbers were decoration on an editorial argument that
reads fine without them. Deleting them deleted every one of those bypasses.

This still cannot police prose: a sentence can be false in a way no regex sees.
It refuses the forms that rot mechanically, and that is all it claims.
"""
import re, subprocess, sys, pathlib

BARE = re.compile(r"`:\d+(?:-\d+)?`")
# a file:line pointer. The number must end at a non-digit that is not `-` or `.`, so a date or an
# ordinal (`guide.md:1st`, `notes.md:2026-08-28`) is prose, not a citation.
FILELINE = re.compile(r"`?(?:\.\./)?[\w./-]+\.md:\d+(?:-\d+)?(?![\d.\w-])")
ANCHOR = re.compile(r"#L\d+(?:-L?\d+)?\b")
LINEWORD = re.compile(r"\blines?\s+\d+(?:\s*[-–]\s*\d+)?\b")
COUNT = re.compile(r"\b\d+\s+lines\b")
# what a length claim may be *about*: the file, a skill directory name, or "this skill".
# The skill names are discovered rather than listed: a hardcoded alternation goes stale the
# moment a skill is added, and it goes stale *silently* -- the gate keeps passing and stops
# covering the new one. Discovered from the same glob `--show` walks.
SUBJECT_FIXED = r"SKILL\.md|\bthis skill\b"


def subject_re(root):
    names = sorted({s.parent.name for s in root.glob("plugins/*/skills/*/SKILL.md")})
    alt = "|".join(re.escape(n) for n in names)
    return re.compile(SUBJECT_FIXED + (f"|`(?:{alt})`" if alt else ""))
ESCAPE = "citation check:"      # so the documents can quote what the gate prints


def tracked_markdown(root):
    """Every Markdown under `root`.

    `git ls-files` when there is a repository, and a walk of the tree when there is not.
    The walk is not the exceptional path: the hook checks a `git checkout-index` copy, which
    is not a repository, so the walk is what runs on every commit. Whatever is in that copy
    is what is being committed, so nothing there may be filtered out.
    """
    try:
        out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "*.md"],
                             capture_output=True, text=True)
        if out.returncode == 0 and out.stdout:
            return [root / p for p in out.stdout.split("\0") if p]
    except (OSError, UnicodeDecodeError):
        pass                                   # no git on the path, or a path git cannot decode
    # `or p.is_symlink()` so a broken link is reported rather than skipped: it is a
    # file no runtime can read, and skipping it is how it would reach one.
    return [p for p in sorted(root.rglob("*.md")) if p.is_file() or p.is_symlink()]


def scan(path, root, subject):
    rel = path.relative_to(root)
    if path.is_symlink():
        return [f"{rel}: is a symlink"]
    bad, para, start, table_subject = [], [], None, False
    lines = path.read_text(encoding="utf-8", errors="replace").split("\n")

    def count_in(text, at):
        m = COUNT.search(text)
        if m and subject.search(text):
            bad.append(f"{rel}:{at}: a line-count claim, `{m.group(0)}` — "
                       "say it in words, or run `check-citations.py --show`")

    for i, line in enumerate(lines + [""], 1):
        if ESCAPE not in line:
            for pat, what in ((BARE, "a bare line citation"), (FILELINE, "a file:line citation"),
                              (ANCHOR, "a line anchor"), (LINEWORD, "a line reference")):
                m = pat.search(line)
                if m:
                    bad.append(f"{rel}:{i}: {what}, `{m.group(0).strip('`')}` — name the section")
        row = line.lstrip().startswith("|")
        # a length claim spans a wrapped paragraph; a table row is its own unit, but a table
        # introduced by a sentence naming the skill carries that subject into every row
        if row or not line.strip():
            if para:
                text = " ".join(para)
                count_in(text, start)
                table_subject = bool(subject.search(text))
            para, start = [], None
            if row:
                count_in(line + (" SKILL.md" if table_subject else ""), i)
        else:
            para.append(line)
            start = start or i
    return bad


def show(root):
    for skill in sorted(root.glob("plugins/*/skills/*/SKILL.md")):
        lines = skill.read_text(encoding="utf-8").split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        heads = [(i, l[3:].strip()) for i, l in enumerate(lines, 1) if l.startswith("## ")]
        print(f"\n{skill.relative_to(root)} — {len(lines)} lines, {len(heads)} sections")
        for k, (i, name) in enumerate(heads):
            end = heads[k + 1][0] - 1 if k + 1 < len(heads) else len(lines)
            print(f"  {end - i + 1:>4}  {name}")
        print("   (read, do not paste: nothing is derived from this)")


def main():
    argv = [a for a in sys.argv[1:] if a != "--show"]
    if len(argv) > 1:
        print("usage: check-citations.py [--show] [<root>]", file=sys.stderr)
        return 2
    root = pathlib.Path(argv[0] if argv else pathlib.Path(__file__).resolve().parent.parent)
    if not root.is_dir():
        print(f"citation check: {root} is not a directory", file=sys.stderr)
        return 2
    root = root.resolve()
    if "--show" in sys.argv:
        show(root)
        return 0
    docs = tracked_markdown(root)
    if not docs:
        print(f"citation check: no Markdown found under {root}", file=sys.stderr)
        return 2
    subject = subject_re(root)
    problems = [p for d in docs for p in scan(d, root, subject)]
    for p in problems:
        print(f"citation check: {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
