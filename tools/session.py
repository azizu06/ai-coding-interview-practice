#!/usr/bin/env python3
"""Run one timed practice session in a scratch copy of a problem.

Usage:
    python tools/session.py start 03              # 50 minute session on 03_inventory_packer
    python tools/session.py start 03 --minutes 25
    python tools/session.py start 03 --fresh      # throw away an existing workspace copy
    python tools/session.py status                # time remaining, if a session is running
    python tools/session.py reset 03              # delete the workspace copy, after asking

start copies problems/<slug> to workspace/<slug> and leaves problems/ untouched, so a
second attempt at the same problem is a reset away and git status stays clean. The clock
runs in the foreground: it calls the time at every ten minute mark and again at five
minutes left, writing each call to workspace/<slug>/SESSION_LOG.md with a timestamp.
Ctrl-C ends the session early and cleanly.

At the end, whether the clock ran out or you stopped it, the session runs the domain
tests and the solver tests in the workspace copy, appends the pass or fail summary and
the elapsed time to SESSION_LOG.md, and tells you to get graded.

Standard library only.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import run as runner  # noqa: E402

ROOT = runner.ROOT
PROBLEMS_DIR = runner.PROBLEMS_DIR
WORKSPACE_DIR = runner.WORKSPACE_DIR
STATE_PATH = os.path.join(WORKSPACE_DIR, ".session.json")
LOG_NAME = "SESSION_LOG.md"
GITIGNORE = os.path.join(ROOT, ".gitignore")
TEST_TIMEOUT = 300

MODE_REMINDER = """Your agent starts in ASK MODE: it explains, proposes code in chat, and
answers complexity questions, but it does not edit files. You type. Say "edit mode" in
chat to let it edit files inside this problem folder, and "ask mode" to switch back.
The rules it follows are in AGENTS.md at the repository root."""

PHASES = ((0.20, "comprehension"), (0.40, "bugs"), (0.70, "implementation"), (1.01, "optimization"))


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def stamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clock(seconds):
    seconds = max(0, int(round(seconds)))
    return f"{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}"


def plural(count, word):
    return f"{count} {word}" + ("" if count == 1 else "s")


def phase_for(fraction):
    for edge, name in PHASES:
        if fraction < edge:
            return name
    return PHASES[-1][1]


def time_calls(minutes):
    """Elapsed minutes at which the session calls the time, in order."""
    marks = [m for m in range(10, int(minutes), 10)]
    five_left = minutes - 5
    if five_left > 0 and five_left not in marks:
        marks.append(five_left)
    return sorted(set(m for m in marks if 0 < m < minutes))


def append_log(folder, text):
    with open(os.path.join(folder, LOG_NAME), "a", encoding="utf-8") as handle:
        handle.write(text + "\n")


def ensure_workspace_ignored():
    line = "workspace/"
    existing = ""
    if os.path.exists(GITIGNORE):
        with open(GITIGNORE, encoding="utf-8") as handle:
            existing = handle.read()
    if line in existing.split():
        return False
    with open(GITIGNORE, "a", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(line + "\n")
    return True


def read_state():
    if not os.path.exists(STATE_PATH):
        return None
    try:
        with open(STATE_PATH, encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        return None


def write_state(state):
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")


def clear_state(slug=None):
    state = read_state()
    if state is None:
        return
    if slug is None or state.get("slug") == slug:
        os.remove(STATE_PATH)


# ---------------------------------------------------------------------------
# Running the tests at the end of a session
# ---------------------------------------------------------------------------

def summarize_unittest(stderr):
    """Pull 'Ran N tests' and the OK or FAILED line out of unittest output."""
    lines = [line.strip() for line in stderr.strip().split("\n") if line.strip()]
    ran = next((line for line in lines if line.startswith("Ran ")), "ran no tests")
    verdict = next((line for line in reversed(lines)
                    if line == "OK" or line.startswith(("OK ", "FAILED"))), "no verdict")
    return f"{ran.rstrip('.')}, {verdict}"


def run_tests(src, modules, label):
    if not modules:
        return f"{label}: none found"
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    command = [sys.executable, "-m", "unittest"] + modules
    try:
        proc = subprocess.run(command, cwd=src, env=env, capture_output=True,
                              text=True, timeout=TEST_TIMEOUT)
    except subprocess.TimeoutExpired:
        return f"{label} ({', '.join(modules)}): still running after {TEST_TIMEOUT}s, killed"
    return f"{label} ({', '.join(modules)}): {summarize_unittest(proc.stderr)}"


def final_report(folder, elapsed_seconds, stopped_early):
    src = runner.src_dir(folder)
    print()
    print("running the tests in the workspace copy, one moment")
    results = [
        run_tests(src, runner.domain_modules(src), "domain tests"),
        run_tests(src, ["test_solver"] if os.path.exists(os.path.join(src, "test_solver.py")) else [],
                  "solver tests"),
    ]
    ending = "stopped early" if stopped_early else "clock ran out"
    append_log(folder, "")
    append_log(folder, f"## Session end ({ending})")
    append_log(folder, "")
    append_log(folder, f"- {stamp()}  elapsed {clock(elapsed_seconds)}")
    for line in results:
        append_log(folder, f"- {line}")
    print()
    for line in results:
        print(line)
    print(f"elapsed {clock(elapsed_seconds)}, logged to {runner.relative(os.path.join(folder, LOG_NAME))}")
    print()
    print("paste RUBRIC.md into your agent chat to get graded")


# ---------------------------------------------------------------------------
# start
# ---------------------------------------------------------------------------

def copy_problem(slug, fresh):
    source = os.path.join(PROBLEMS_DIR, slug)
    destination = os.path.join(WORKSPACE_DIR, slug)
    if os.path.isdir(destination):
        if not fresh:
            raise runner.ProblemError(
                f"{runner.relative(destination)} already exists. Keep working in it, or "
                f"pass --fresh to start over, or run: python tools/session.py reset {slug}")
        print(f"--fresh: replacing {runner.relative(destination)}")
        shutil.rmtree(destination)
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    shutil.copytree(source, destination,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return destination


def start_log(folder, slug, minutes):
    calls = time_calls(minutes)
    header = [
        f"# Session log: {slug}",
        "",
        f"- started {stamp()}",
        f"- budget {plural(minutes, 'minute')}",
        "- time calls at " + (", ".join(f"{c} min" for c in calls) if calls
                              else "no mark, this session ends before the first one"),
        "",
        "## Time calls",
        "",
        "",
    ]
    with open(os.path.join(folder, LOG_NAME), "w", encoding="utf-8") as handle:
        handle.write("\n".join(header))


def run_clock(folder, minutes):
    """Foreground clock. Returns (elapsed_seconds, stopped_early)."""
    total = minutes * 60.0
    started = time.monotonic()
    events = [(m * 60.0, m) for m in time_calls(minutes)] + [(total, None)]
    try:
        for when, mark in events:
            while True:
                remaining = when - (time.monotonic() - started)
                if remaining <= 0:
                    break
                time.sleep(min(1.0, remaining))
            if mark is None:
                break
            left = minutes - mark
            phase = phase_for(mark / float(minutes))
            print(f"[{clock(mark * 60)} elapsed] {left} minutes left. Suggested phase: {phase}.",
                  flush=True)
            append_log(folder, f"- {stamp()}  {left} minutes left "
                               f"({mark} elapsed), suggested phase: {phase}")
    except KeyboardInterrupt:
        elapsed = time.monotonic() - started
        print()
        print(f"stopping early at {clock(elapsed)}")
        append_log(folder, f"- {stamp()}  stopped early at {clock(elapsed)}")
        return elapsed, True
    print()
    print(f"time. the {plural(minutes, 'minute')} are up.", flush=True)
    append_log(folder, f"- {stamp()}  time, the {plural(minutes, 'minute')} are up")
    return time.monotonic() - started, False


def command_start(args):
    slug = runner.find_slug(args.problem)
    if args.minutes <= 0:
        raise runner.ProblemError("--minutes must be greater than zero")
    running = read_state()
    if running and os.path.isdir(os.path.join(WORKSPACE_DIR, running.get("slug", ""))):
        if running.get("slug") != slug:
            print(f"note: a session for {running['slug']} was never closed out. "
                  f"python tools/session.py status")
    folder = copy_problem(slug, args.fresh)
    if ensure_workspace_ignored():
        print("added workspace/ to .gitignore")
    start_log(folder, slug, args.minutes)
    write_state({
        "slug": slug,
        "folder": folder,
        "minutes": args.minutes,
        "started": time.time(),
        "started_readable": stamp(),
    })
    readme = os.path.join(folder, "README.md")
    print()
    print(f"session: {slug}, {plural(args.minutes, 'minute')}")
    print(f"working copy: {runner.relative(folder)}")
    print(f"read this first: {runner.relative(readme)}")
    print(f"log: {runner.relative(os.path.join(folder, LOG_NAME))}")
    print()
    print(MODE_REMINDER)
    print()
    print(f"run things with: python tools/run.py {slug.split('_')[0]} main|domain|solver|timed")
    calls = time_calls(args.minutes)
    print("time calls at " + (", ".join(f"{c} min" for c in calls) if calls
                              else "no mark, this session ends before the first one"))
    print("Ctrl-C ends the session early. The clock starts now.")
    print()
    elapsed, stopped_early = run_clock(folder, args.minutes)
    final_report(folder, elapsed, stopped_early)
    clear_state(slug)
    return 0


# ---------------------------------------------------------------------------
# status and reset
# ---------------------------------------------------------------------------

def command_status(_args):
    state = read_state()
    if state is None:
        print("no session running. Start one with: python tools/session.py start 01")
        return 0
    slug = state.get("slug", "?")
    minutes = float(state.get("minutes", 0))
    elapsed = time.time() - float(state.get("started", 0))
    remaining = minutes * 60 - elapsed
    print(f"session: {slug}, {minutes:g} minute budget, started {state.get('started_readable', '?')}")
    print(f"working copy: {runner.relative(state.get('folder', ''))}")
    if remaining <= 0:
        print(f"the clock ran out {clock(-remaining)} ago, elapsed {clock(elapsed)}")
    else:
        print(f"time remaining: {clock(remaining)} of {clock(minutes * 60)}")
        print(f"suggested phase: {phase_for(elapsed / (minutes * 60))}")
    return 0


def describe_tree(folder):
    files = 0
    total = 0
    for root, _dirs, names in os.walk(folder):
        for name in names:
            path = os.path.join(root, name)
            files += 1
            try:
                total += os.path.getsize(path)
            except OSError:
                pass
    return files, total


def command_reset(args):
    slug = runner.find_slug(args.problem)
    folder = os.path.join(WORKSPACE_DIR, slug)
    if not os.path.isdir(folder):
        print(f"nothing to delete: {runner.relative(folder)} does not exist")
        return 0
    files, total = describe_tree(folder)
    log = os.path.join(folder, LOG_NAME)
    print(f"about to delete {runner.relative(folder)}")
    print(f"  {files} files, {total / 1024.0:.0f} KB, including every edit you made there")
    if os.path.exists(log):
        print(f"  including {runner.relative(log)}")
    print(f"problems/{slug} is not touched.")
    try:
        answer = input("delete it? [y/N] ").strip().lower()
    except EOFError:
        answer = ""
    if answer not in ("y", "yes"):
        print("left alone")
        return 0
    shutil.rmtree(folder)
    clear_state(slug)
    print(f"deleted {runner.relative(folder)}")
    return 0


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="python tools/session.py",
        description="Start, check, and reset a timed practice session.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start = subparsers.add_parser("start", help="copy a problem to workspace/ and start the clock")
    start.add_argument("problem", help="03, 03_inventory_packer, or a path to either")
    start.add_argument("--minutes", type=int, default=50, help="session length, default 50")
    start.add_argument("--fresh", action="store_true", help="replace an existing workspace copy")
    start.set_defaults(func=command_start)

    status = subparsers.add_parser("status", help="time remaining, if a session is running")
    status.set_defaults(func=command_status)

    reset = subparsers.add_parser("reset", help="delete a workspace copy, after asking")
    reset.add_argument("problem", help="03, 03_inventory_packer, or a path to either")
    reset.set_defaults(func=command_reset)
    return parser


def main(argv):
    args = build_parser().parse_args(argv[1:])
    try:
        return args.func(args)
    except runner.ProblemError as error:
        print(f"session.py: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
