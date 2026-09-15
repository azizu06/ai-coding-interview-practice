#!/usr/bin/env python3
"""Verify every practice problem end to end.

Usage:
    python tools/verify.py                # verify every problem under problems/
    python tools/verify.py 01_word_container 04_task_scheduler

For each problem the script works in a temporary copy and runs four stages:

  shipped  The src/ tree exactly as a candidate receives it. Every domain test
           file (test_*.py except test_solver.py) must pass as shipped, which
           means the tests that are commented out stay commented out.
  fixed    solutions/<slug>/<domain>.py and solutions/<slug>/solver.py are
           copied over src/, every commented-out test is uncommented, every
           "????" is replaced from solutions/<slug>/expected.json, and all
           domain tests plus the non-timed solver tests must pass.
  timed    With the reference solver, every timed test is run on its own and
           must pass with a wall time at or under half of its budget.
  brute    With solutions/<slug>/brute_force_solver.py copied to src/solver.py,
           at least one timed test must fail because of time (its own time
           assertion, or a hard timeout at three times the budget).

Exit status is non-zero when any stage of any problem fails.

Conventions the problem files must follow so the stages can be mechanical:

  * A commented-out test starts with a line of the form `    # def test_x(self):`
    and every following line of that test is `    # <code>` at the same indent.
    Blank lines inside a commented-out test are written as a bare `    #`.
    The block ends at the first line that is not a comment at that indent.
  * An unknown expected value is written as its own assignment line:
        expected = "????"
    or  expected_count = "????"
    The variable name must contain `expected`. It is replaced by the value in
    expected.json, keyed by the test method name. A value is either a string
    holding a Python expression, or an object mapping variable name to an
    expression when one test has several unknowns.
  * A timed test contains an assignment `expected_time = <number>` (seconds).
    The number is the budget verify uses for the timed and brute stages.
  * Heavy fixtures for timed tests belong in setUpClass so the wall time that
    verify measures reflects the solver rather than data loading.
  * solutions/<slug>/ holds solver.py, brute_force_solver.py, expected.json,
    ANSWER_KEY.md, and one fixed copy of each domain file. Every .py file that
    is not solver.py or brute_force_solver.py is treated as a domain file.

Standard library only.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROBLEMS_DIR = os.path.join(ROOT, "problems")
SOLUTIONS_DIR = os.path.join(ROOT, "solutions")
RUNNER_NAME = "_verify_runner.py"
MARK = "@@VERIFY "

RUNNER_SOURCE = r'''
import importlib
import json
import sys
import time
import traceback
import unittest

MARK = "@@VERIFY "


def emit(record):
    sys.stdout.write(MARK + json.dumps(record) + "\n")
    sys.stdout.flush()


class TimingResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self._start = {}
        self._status = {}
        self._message = {}

    def startTest(self, test):
        super().startTest(test)
        self._start[test] = time.perf_counter()
        self._status[test] = "pass"
        self._message[test] = ""

    def stopTest(self, test):
        super().stopTest(test)
        wall = time.perf_counter() - self._start[test]
        emit({
            "name": getattr(test, "_testMethodName", str(test)),
            "status": self._status[test],
            "wall": wall,
            "message": self._message[test],
        })

    def _record(self, test, status, err):
        exc_type, exc_value, _tb = err
        text = "".join(traceback.format_exception_only(exc_type, exc_value)).strip()
        self._status[test] = status
        self._message[test] = text.splitlines()[-1] if text else status

    def addFailure(self, test, err):
        self._record(test, "fail", err)

    def addError(self, test, err):
        if test in self._status:
            self._record(test, "error", err)
        else:
            exc_type, exc_value, _tb = err
            emit({
                "name": str(test),
                "status": "error",
                "wall": 0.0,
                "message": "".join(traceback.format_exception_only(exc_type, exc_value)).strip(),
            })

    def addSkip(self, test, reason):
        self._status[test] = "skip"
        self._message[test] = reason

    def addExpectedFailure(self, test, err):
        self._status[test] = "pass"

    def addUnexpectedSuccess(self, test):
        self._status[test] = "fail"
        self._message[test] = "unexpected success"


def main():
    module_name = sys.argv[1]
    include = set(x for x in sys.argv[2].split(",") if x) if len(sys.argv) > 2 else set()
    exclude = set(x for x in sys.argv[3].split(",") if x) if len(sys.argv) > 3 else set()
    try:
        module = importlib.import_module(module_name)
    except Exception:
        emit({"name": module_name, "status": "error", "wall": 0.0,
              "message": traceback.format_exc().strip().splitlines()[-1]})
        return 2
    loaded = unittest.defaultTestLoader.loadTestsFromModule(module)
    selected = []

    def walk(suite):
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                walk(item)
            else:
                name = getattr(item, "_testMethodName", "")
                if include and name not in include:
                    continue
                if name in exclude:
                    continue
                selected.append(item)

    walk(loaded)
    suite = unittest.TestSuite(selected)
    result = TimingResult()
    suite.run(result)
    emit({"name": "__summary__", "status": "done", "wall": 0.0,
          "message": "%d run" % result.testsRun})
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


# ---------------------------------------------------------------------------
# Source rewriting helpers
# ---------------------------------------------------------------------------

COMMENTED_TEST_RE = re.compile(r"^(\s*)# (def test_\w+\(.*)$")
TEST_DEF_RE = re.compile(r"^\s*def (test_\w+)\(")
UNKNOWN_RE = re.compile(r"""^(\s*)(\w*expected\w*)\s*=\s*(["'])\?\?\?\?\3\s*(#.*)?$""")
BUDGET_RE = re.compile(r"^\s*expected_time\s*=\s*([0-9]+(?:\.[0-9]+)?)\b")


def uncomment_tests(text: str) -> str:
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        match = COMMENTED_TEST_RE.match(lines[i])
        if not match:
            out.append(lines[i])
            i += 1
            continue
        indent = match.group(1)
        prefix = indent + "# "
        while i < len(lines):
            line = lines[i]
            if line.startswith(prefix):
                out.append(indent + line[len(prefix):])
            elif line.rstrip() == indent + "#":
                out.append("")
            else:
                break
            i += 1
    return "\n".join(out)


def fill_unknowns(text: str, mapping: dict) -> tuple[str, list[str]]:
    lines = text.split("\n")
    current = None
    missing = []
    for idx, line in enumerate(lines):
        def_match = TEST_DEF_RE.match(line)
        if def_match:
            current = def_match.group(1)
            continue
        unknown = UNKNOWN_RE.match(line)
        if not unknown:
            continue
        indent, name, _quote, comment = unknown.groups()
        value = mapping.get(current)
        if isinstance(value, dict):
            value = value.get(name)
        if value is None:
            missing.append(f"{current}.{name}")
            continue
        lines[idx] = f"{indent}{name} = {value}" + (f"  {comment}" if comment else "")
    return "\n".join(lines), missing


def timed_budgets(text: str) -> dict[str, float]:
    budgets = {}
    current = None
    for line in text.split("\n"):
        def_match = TEST_DEF_RE.match(line)
        if def_match:
            current = def_match.group(1)
            continue
        budget = BUDGET_RE.match(line)
        if budget and current:
            budgets[current] = float(budget.group(1))
    return budgets


def rewrite(path: str, func) -> None:
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(func(text))


# ---------------------------------------------------------------------------
# Test execution
# ---------------------------------------------------------------------------

class RunOutcome:
    def __init__(self, records, timed_out=False, stderr="", returncode=0):
        self.records = records
        self.timed_out = timed_out
        self.stderr = stderr
        self.returncode = returncode

    @property
    def tests(self):
        return [r for r in self.records if r["name"] != "__summary__"]

    def failures(self):
        return [r for r in self.tests if r["status"] not in ("pass", "skip")]


def run_module(src_dir, module, include=None, exclude=None, timeout=None) -> RunOutcome:
    runner_path = os.path.join(src_dir, RUNNER_NAME)
    if not os.path.exists(runner_path):
        with open(runner_path, "w", encoding="utf-8") as handle:
            handle.write(RUNNER_SOURCE)
    cmd = [sys.executable, RUNNER_NAME, module,
           ",".join(include or []), ",".join(exclude or [])]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        proc = subprocess.run(cmd, cwd=src_dir, capture_output=True, text=True,
                              timeout=timeout, env=env)
    except subprocess.TimeoutExpired as exc:
        partial = _parse(exc.stdout or "")
        return RunOutcome(partial, timed_out=True, stderr=(exc.stderr or ""))
    records = _parse(proc.stdout)
    return RunOutcome(records, stderr=proc.stderr, returncode=proc.returncode)


def _parse(stdout):
    if isinstance(stdout, bytes):
        stdout = stdout.decode("utf-8", "replace")
    records = []
    for line in stdout.splitlines():
        if line.startswith(MARK):
            try:
                records.append(json.loads(line[len(MARK):]))
            except json.JSONDecodeError:
                pass
    return records


def short(message: str, limit: int = 110) -> str:
    message = " ".join(message.split())
    return message if len(message) <= limit else message[: limit - 3] + "..."


# ---------------------------------------------------------------------------
# Per-problem verification
# ---------------------------------------------------------------------------

class ProblemReport:
    def __init__(self, slug):
        self.slug = slug
        self.stages = {"shipped": None, "fixed": None, "timed": None, "brute": None}
        self.notes = []

    def note(self, text):
        self.notes.append(text)

    @property
    def ok(self):
        return all(v is True for v in self.stages.values())


def domain_files(solution_dir):
    return sorted(
        f for f in os.listdir(solution_dir)
        if f.endswith(".py") and f not in ("solver.py", "brute_force_solver.py")
    )


def test_modules(src_dir):
    names = sorted(f[:-3] for f in os.listdir(src_dir)
                   if f.startswith("test_") and f.endswith(".py"))
    domain = [n for n in names if n != "test_solver"]
    return domain, ("test_solver" if "test_solver" in names else None)


def verify_problem(slug: str) -> ProblemReport:
    report = ProblemReport(slug)
    problem_dir = os.path.join(PROBLEMS_DIR, slug)
    solution_dir = os.path.join(SOLUTIONS_DIR, slug)
    if not os.path.isdir(problem_dir):
        report.note(f"missing problems/{slug}")
        return report
    if not os.path.isdir(solution_dir):
        report.note(f"missing solutions/{slug}")
        return report

    with tempfile.TemporaryDirectory(prefix="verify_") as tmp:
        work = os.path.join(tmp, slug)
        shutil.copytree(problem_dir, work,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        src = os.path.join(work, "src")
        if not os.path.isdir(src):
            report.note("missing src/")
            return report
        domain_tests, solver_test = test_modules(src)
        if not domain_tests:
            report.note("no domain test file found")
        if solver_test is None:
            report.note("no test_solver.py found")

        # Stage 1: shipped state, domain tests only.
        shipped_ok = bool(domain_tests)
        for module in domain_tests:
            outcome = run_module(src, module, timeout=300)
            bad = outcome.failures()
            if outcome.timed_out or bad or not outcome.tests:
                shipped_ok = False
                for rec in bad[:3]:
                    report.note(f"shipped {module}.{rec['name']}: {short(rec['message'])}")
                if not outcome.tests:
                    report.note(f"shipped {module}: no tests ran {short(outcome.stderr)}")
        report.stages["shipped"] = shipped_ok

        # Stage 2: apply fixed domain files and reference solver, open all tests.
        for name in domain_files(solution_dir):
            shutil.copy(os.path.join(solution_dir, name), os.path.join(src, name))
        ref_solver = os.path.join(solution_dir, "solver.py")
        brute_solver = os.path.join(solution_dir, "brute_force_solver.py")
        expected_path = os.path.join(solution_dir, "expected.json")
        fixed_ok = True
        if not os.path.exists(ref_solver):
            report.note("missing solutions solver.py")
            fixed_ok = False
        if not os.path.exists(expected_path):
            report.note("missing solutions expected.json")
            mapping = {}
        else:
            with open(expected_path, encoding="utf-8") as handle:
                mapping = json.load(handle)
        if fixed_ok:
            shutil.copy(ref_solver, os.path.join(src, "solver.py"))
        all_test_modules = domain_tests + ([solver_test] if solver_test else [])
        for module in all_test_modules:
            path = os.path.join(src, module + ".py")
            rewrite(path, uncomment_tests)
            with open(path, encoding="utf-8") as handle:
                text = handle.read()
            filled, missing = fill_unknowns(text, mapping)
            for item in missing:
                report.note(f"expected.json lacks {module}.{item}")
                fixed_ok = False
            if '"????"' in filled or "'????'" in filled:
                report.note(f"{module}: a ???? survived substitution")
                fixed_ok = False
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(filled)

        budgets = {}
        if solver_test:
            with open(os.path.join(src, solver_test + ".py"), encoding="utf-8") as handle:
                budgets = timed_budgets(handle.read())
            if not budgets:
                report.note("no timed tests (expected_time) found in test_solver.py")

        if fixed_ok:
            for module in domain_tests:
                outcome = run_module(src, module, timeout=300)
                bad = outcome.failures()
                if outcome.timed_out or bad or not outcome.tests:
                    fixed_ok = False
                    for rec in bad[:3]:
                        report.note(f"fixed {module}.{rec['name']}: {short(rec['message'])}")
                    if not outcome.tests:
                        report.note(f"fixed {module}: no tests ran {short(outcome.stderr)}")
            if solver_test:
                outcome = run_module(src, solver_test, exclude=list(budgets), timeout=300)
                bad = outcome.failures()
                if outcome.timed_out or bad or not outcome.tests:
                    fixed_ok = False
                    for rec in bad[:3]:
                        report.note(f"fixed {solver_test}.{rec['name']}: {short(rec['message'])}")
                    if not outcome.tests:
                        report.note(f"fixed {solver_test}: no tests ran {short(outcome.stderr)}")
        report.stages["fixed"] = fixed_ok

        # Stage 3: timed tests with the reference solver.
        timed_ok = bool(budgets) and fixed_ok
        if fixed_ok and solver_test:
            for name, budget in budgets.items():
                outcome = run_module(src, solver_test, include=[name],
                                     timeout=budget * 3 + 10)
                rec = next((r for r in outcome.tests if r["name"] == name), None)
                if outcome.timed_out or rec is None:
                    timed_ok = False
                    report.note(f"timed {name}: timeout (>{budget * 3 + 10:.1f}s) or no result")
                    continue
                wall = rec["wall"]
                status = rec["status"]
                verdict = "ok" if status == "pass" and wall <= budget * HEADROOM else "SLOW"
                if status != "pass":
                    verdict = status.upper()
                if verdict != "ok":
                    timed_ok = False
                report.note(f"timed {name}: {wall:.2f}s of {budget:.2f}s budget [{verdict}]"
                            + (f" {short(rec['message'], 70)}" if status != "pass" else ""))
        report.stages["timed"] = timed_ok

        # Stage 4: brute force must fail at least one timed test on time.
        brute_ok = False
        if not os.path.exists(brute_solver):
            report.note("missing solutions brute_force_solver.py")
        elif fixed_ok and solver_test and budgets:
            shutil.copy(brute_solver, os.path.join(src, "solver.py"))
            time_failures = 0
            passes = 0
            for name, budget in budgets.items():
                limit = budget * 3 + 2
                outcome = run_module(src, solver_test, include=[name], timeout=limit)
                rec = next((r for r in outcome.tests if r["name"] == name), None)
                if outcome.timed_out:
                    time_failures += 1
                    report.note(f"brute {name}: killed at {limit:.1f}s (>3x budget {budget:.2f}s) [FAILS]")
                    continue
                if rec is None:
                    report.note(f"brute {name}: no result {short(outcome.stderr)}")
                    continue
                if rec["status"] == "pass":
                    passes += 1
                    report.note(f"brute {name}: passes in {rec['wall']:.2f}s of {budget:.2f}s")
                elif rec["wall"] >= budget or "need <" in rec["message"]:
                    time_failures += 1
                    report.note(f"brute {name}: {rec['wall']:.2f}s of {budget:.2f}s [FAILS on time]")
                else:
                    report.note(f"brute {name}: failed for another reason: {short(rec['message'])}")
            brute_ok = time_failures > 0
            if passes == 0:
                report.note("warning: brute force passes no timed test (medium should pass)")
        report.stages["brute"] = brute_ok

    return report


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def discover_problems():
    if not os.path.isdir(PROBLEMS_DIR):
        return []
    return sorted(d for d in os.listdir(PROBLEMS_DIR)
                  if re.match(r"^\d\d_\w+$", d) and os.path.isdir(os.path.join(PROBLEMS_DIR, d)))


def cell(value):
    if value is True:
        return "PASS"
    if value is False:
        return "FAIL"
    return "----"


HEADROOM = 0.5


def main(argv):
    """Usage: verify.py [--headroom FRACTION] [NN_slug ...]

    --headroom sets how much of each timed budget the reference solver may use
    and still count as ok. The default 0.5 is the tuning gate for this repo's
    authors on a fast laptop. CI runners are slower, so the workflow passes
    --headroom 1.0, which is the rule a candidate is actually held to.
    """
    global HEADROOM
    args = list(argv[1:])
    if "--headroom" in args:
        i = args.index("--headroom")
        HEADROOM = float(args[i + 1])
        del args[i:i + 2]
    slugs = args or discover_problems()
    if not slugs:
        print("no problems found under problems/")
        return 1
    reports = []
    for slug in slugs:
        print(f"== {slug}")
        report = verify_problem(slug)
        for note in report.notes:
            print(f"   {note}")
        print(f"   result: {'PASS' if report.ok else 'FAIL'}")
        reports.append(report)

    width = max(len(r.slug) for r in reports)
    header = f"{'problem':<{width}}  shipped  fixed  timed  brute  result"
    print()
    print(header)
    print("-" * len(header))
    for r in reports:
        print(f"{r.slug:<{width}}  {cell(r.stages['shipped']):<7}  {cell(r.stages['fixed']):<5}  "
              f"{cell(r.stages['timed']):<5}  {cell(r.stages['brute']):<5}  "
              f"{'PASS' if r.ok else 'FAIL'}")
    failed = [r.slug for r in reports if not r.ok]
    print()
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        return 1
    print("all problems verified")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
