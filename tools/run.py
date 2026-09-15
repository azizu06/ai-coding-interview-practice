#!/usr/bin/env python3
"""Run one piece of a practice problem, the way a Run dropdown would.

Usage:
    python tools/run.py 03 main        # the runnable demo, src/main.py
    python tools/run.py 03 domain      # the domain unit tests
    python tools/run.py 03 solver      # test_solver.py as it stands
    python tools/run.py 03 timed       # reveal the next timed test, then run test_solver.py
    python tools/run.py 03 all         # main, then domain, then solver
    python tools/run.py 03 --list      # which timed tests are revealed, which are hidden

The problem can be named as a number (03), a slug (03_inventory_packer), or a path
(problems/03_inventory_packer). A workspace copy at workspace/<slug> wins over the
pristine copy at problems/<slug>, so a session started with tools/session.py runs
against the session copy without any extra flags.

Timed tests are found by the convention the repository already relies on, the one
tools/verify.py documents: a timed test is a test function whose body assigns
expected_time. In nine of the ten problems those functions live in a commented-out
block under class TestSolverSpeed. Problem 06 keeps them at the bottom of class
TestSolver instead, so --list names the class it found them in rather than pretending
every problem is laid out the same way.

Revealing uncomments exactly one test function: the first still-commented timed test
after the last revealed one. Nothing else in the file is touched.

Standard library only.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS_DIR = os.path.join(ROOT, "problems")
WORKSPACE_DIR = os.path.join(ROOT, "workspace")
SLUG_RE = re.compile(r"^\d\d_\w+$")

COMMENTED_DEF_RE = re.compile(r"^(\s*)# (def (test_\w+)\(.*)$")
DEF_RE = re.compile(r"^(\s*)def (test_\w+)\(")
CLASS_RE = re.compile(r"^class (\w+)")
TIMED_MARKER = "expected_time"

ACTIONS = ("main", "domain", "solver", "timed", "all")


class ProblemError(Exception):
    """The problem folder could not be resolved, or its layout is unusable."""


# ---------------------------------------------------------------------------
# Locating a problem
# ---------------------------------------------------------------------------

def known_slugs():
    if not os.path.isdir(PROBLEMS_DIR):
        return []
    return sorted(d for d in os.listdir(PROBLEMS_DIR)
                  if SLUG_RE.match(d) and os.path.isdir(os.path.join(PROBLEMS_DIR, d)))


def find_slug(token):
    """Turn 03, 3, 03_inventory_packer or problems/03_inventory_packer into a slug."""
    name = os.path.basename(token.strip().rstrip("/").rstrip("\\"))
    slugs = known_slugs()
    if not slugs:
        raise ProblemError(f"no problems found under {PROBLEMS_DIR}")
    if name in slugs:
        return name
    if name.isdigit():
        number = name.zfill(2)
        matches = [s for s in slugs if s.split("_")[0] == number]
    else:
        matches = [s for s in slugs if s.startswith(name)]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise ProblemError(f"no problem matches {token!r}. Known: {', '.join(slugs)}")
    raise ProblemError(f"{token!r} matches several problems: {', '.join(matches)}")


def resolve(token):
    """Return (slug, folder, where). A workspace copy wins over problems/."""
    slug = find_slug(token)
    workspace_copy = os.path.join(WORKSPACE_DIR, slug)
    if os.path.isdir(workspace_copy):
        return slug, workspace_copy, "workspace"
    return slug, os.path.join(PROBLEMS_DIR, slug), "problems"


def src_dir(folder):
    src = os.path.join(folder, "src")
    if not os.path.isdir(src):
        raise ProblemError(f"missing src/ under {folder}")
    return src


def domain_modules(src):
    names = sorted(f[:-3] for f in os.listdir(src)
                   if f.startswith("test_") and f.endswith(".py"))
    return [n for n in names if n != "test_solver"]


def relative(path):
    try:
        return os.path.relpath(path, ROOT)
    except ValueError:
        return path


# ---------------------------------------------------------------------------
# Reading the timed tests out of test_solver.py
# ---------------------------------------------------------------------------

class TimedTest:
    def __init__(self, name, class_name, revealed, start, end):
        self.name = name
        self.class_name = class_name
        self.revealed = revealed
        self.start = start
        self.end = end


def commented_block_end(lines, start):
    """End of the commented-out block that begins at lines[start], exclusive."""
    indent = COMMENTED_DEF_RE.match(lines[start]).group(1)
    prefix = indent + "# "
    bare = indent + "#"
    index = start + 1
    while index < len(lines):
        line = lines[index]
        if COMMENTED_DEF_RE.match(line):
            break
        if line.startswith(prefix) or line.rstrip() == bare:
            index += 1
            continue
        break
    return index


def live_block_end(lines, start):
    """End of the real (uncommented) function that begins at lines[start], exclusive."""
    indent = len(DEF_RE.match(lines[start]).group(1))
    index = start + 1
    while index < len(lines):
        line = lines[index]
        if line.strip() and len(line) - len(line.lstrip()) <= indent:
            break
        index += 1
    return index


def parse_tests(text):
    """Every test function in file order, commented out or not."""
    lines = text.split("\n")
    found = []
    class_name = "<module>"
    index = 0
    while index < len(lines):
        line = lines[index]
        class_match = CLASS_RE.match(line)
        if class_match:
            class_name = class_match.group(1)
            index += 1
            continue
        commented = COMMENTED_DEF_RE.match(line)
        if commented:
            end = commented_block_end(lines, index)
            body = "\n".join(lines[index:end])
            found.append((commented.group(3), class_name, False, index, end, body))
            index = end
            continue
        live = DEF_RE.match(line)
        if live:
            end = live_block_end(lines, index)
            body = "\n".join(lines[index:end])
            found.append((live.group(2), class_name, True, index, end, body))
            index = end
            continue
        index += 1
    return [TimedTest(name, cls, revealed, start, end)
            for name, cls, revealed, start, end, body in found
            if TIMED_MARKER in body]


def read_timed(src):
    path = os.path.join(src, "test_solver.py")
    if not os.path.exists(path):
        raise ProblemError(f"missing {relative(path)}")
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    timed = parse_tests(text)
    if not timed:
        raise ProblemError(
            f"{relative(path)}: found no timed tests. A timed test is a test function "
            f"whose body assigns {TIMED_MARKER}. This problem does not follow that "
            f"convention, so run.py cannot reveal its timed tests.")
    return path, text, timed


def uncomment(lines, start, end):
    """Strip the comment prefix from one commented-out block, in place."""
    indent = COMMENTED_DEF_RE.match(lines[start]).group(1)
    prefix = indent + "# "
    bare = indent + "#"
    for index in range(start, end):
        line = lines[index]
        if line.startswith(prefix):
            lines[index] = indent + line[len(prefix):]
        elif line.rstrip() == bare:
            lines[index] = ""


def next_hidden(timed):
    """The first hidden timed test after the last revealed one."""
    last_revealed = -1
    for position, test in enumerate(timed):
        if test.revealed:
            last_revealed = position
    for test in timed[last_revealed + 1:]:
        if not test.revealed:
            return test
    for test in timed:
        if not test.revealed:
            return test
    return None


def reveal_next(src):
    """Uncomment one timed test. Returns the test, or None when all are revealed."""
    path, text, timed = read_timed(src)
    target = next_hidden(timed)
    if target is None:
        return None, timed
    lines = text.split("\n")
    uncomment(lines, target.start, target.end)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    target.revealed = True
    return target, timed


# ---------------------------------------------------------------------------
# Running things
# ---------------------------------------------------------------------------

def run_python(src, args):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    printable = " ".join(["python"] + args)
    print(f"$ cd {relative(src)} && {printable}", flush=True)
    return subprocess.run([sys.executable] + args, cwd=src, env=env).returncode


def run_main(src):
    return run_python(src, ["main.py"])


def run_domain(src):
    modules = domain_modules(src)
    if not modules:
        raise ProblemError(f"no domain test file under {relative(src)}")
    return run_python(src, ["-m", "unittest", "-v"] + modules)


def run_solver(src):
    return run_python(src, ["-m", "unittest", "-v", "test_solver"])


def run_timed(src, where):
    target, timed = reveal_next(src)
    total = len(timed)
    if target is None:
        print(f"all {total} timed tests are already revealed in {relative(src)}/test_solver.py")
    else:
        revealed = sum(1 for t in timed if t.revealed)
        print(f"revealed {target.name} in {target.class_name} "
              f"({revealed} of {total} timed tests now revealed)")
        if where == "problems":
            print(f"note: that edit is in problems/, restore it with "
                  f"git checkout -- {relative(os.path.dirname(src))}")
    return run_solver(src)


def show_list(slug, folder, where, src):
    _path, _text, timed = read_timed(src)
    classes = sorted({t.class_name for t in timed})
    print(f"{slug}  ({relative(folder)}, {where} copy)")
    print(f"timed tests in {', '.join(classes)}:")
    for test in timed:
        print(f"  [{'revealed' if test.revealed else 'hidden  '}] {test.name}")
    revealed = sum(1 for t in timed if t.revealed)
    print(f"{revealed} revealed, {len(timed) - revealed} hidden")
    if "TestSolverSpeed" not in classes:
        print("note: this problem keeps its timed tests outside class TestSolverSpeed, "
              "so they were found by the expected_time convention instead")
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="python tools/run.py",
        description="Run the demo, the domain tests, or the solver tests for one problem.")
    parser.add_argument("problem", help="03, 03_inventory_packer, or a path to either")
    parser.add_argument("action", nargs="?", choices=ACTIONS,
                        help="what to run: " + ", ".join(ACTIONS))
    parser.add_argument("--list", action="store_true",
                        help="show which timed tests are revealed and which are hidden")
    return parser


def main(argv):
    args = build_parser().parse_args(argv[1:])
    if not args.action and not args.list:
        build_parser().error("give an action (" + ", ".join(ACTIONS) + ") or --list")
    try:
        slug, folder, where = resolve(args.problem)
        src = src_dir(folder)
        if args.list:
            return show_list(slug, folder, where, src)
        print(f"{slug}  ({relative(folder)}, {where} copy)")
        if args.action == "main":
            return run_main(src)
        if args.action == "domain":
            return run_domain(src)
        if args.action == "solver":
            return run_solver(src)
        if args.action == "timed":
            return run_timed(src, where)
        codes = [run_main(src), run_domain(src), run_solver(src)]
        return next((c for c in codes if c), 0)
    except ProblemError as error:
        print(f"run.py: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
