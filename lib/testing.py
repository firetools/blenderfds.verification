import datetime
from typing import List, Tuple
from . import import_mod
from .bcolors import HEADER, ENDC, OKGREEN, FAIL


def run_tests(test_py_module, requested_test_names=None):
    """!
    Execute tests from test_py_module.
    """
    tests = import_mod.import_submodules(test_py_module, recursive=False)
    print(f"{HEADER}Available tests:{ENDC}")
    print("  " + "\n  ".join(tests))
    print(f"{HEADER}Requested tests:{ENDC}")
    print("  " + "\n  ".join(requested_test_names or ("all",)))
    # Run
    print(f"{HEADER}Run tests...{ENDC}")
    results = list()
    for key, item in tests.items():  # FIXME improve test selection (regex?)
        if requested_test_names and key.split(".")[1] not in requested_test_names:
            continue
        rs = item.run()
        # Check and pile results
        if isinstance(rs, _TestResult):
            results.append(rs)
        elif isinstance(rs, (List, Tuple)) and isinstance(rs[0], _TestResult):
            results.extend(rs)
        else:
            raise Exception(f"<{item}> is sending bad result <{rs}>")
    # Classify failed by test
    packages = dict()
    for r in results:
        if r.package not in packages:
            packages[r.package] = list((list(), list()))
        if isinstance(r, TestOk):
            packages[r.package][0].append(r)
        else:
            packages[r.package][1].append(r)

    # Output
    # Repeat failed
    lines = list()
    for key, value in packages.items():
        lines.append(f"\n{HEADER}Detailed failures of <{key}>:{ENDC}")
        if not value[1]:
            lines.append("None")
        else:
            for r in value[1]:
                lines.append(r.detail)
    # Results
    lines.append(f"\n{HEADER}Overall test results:{ENDC}")
    for key, value in packages.items():
        nok = len(value[0])
        nfail = len(value[1])
        ntot = nfail + nok
        lines.append(
            f"{ntot:>8} = {OKGREEN}{nok:>6} ok{ENDC} + {FAIL}{nfail:>6} failed{ENDC} in {key}"
        )
    lines.append(f"{len(results):>8} completed")
    # Print and save
    print("\n".join(lines))
    filename = (
        "./results/"
        + datetime.datetime.now().replace(microsecond=0).isoformat()
        + ".txt"
    )
    with open(filename, "w") as f:
        for key, value in packages.items():
            f.write(f"\n-------- Detailed failures of <{key}> --------\n")
            if not value[1]:
                f.write("None\n")
            else:
                for r in value[1]:
                    f.write(r.detail + "\n")


class _TestResult:
    def __init__(self, package, name, log=None):
        self.package = package
        self.name = name
        self.log = log
        print(self)

    @property
    def label(self):
        return f"{self.package}:\n{self.name[:30]}···{self.name[len(self.name) - 76 :]}"

    @property
    def detail(self):
        return f"\n---\n{self.log}\n{self}"


class TestOk(_TestResult):
    def __str__(self):
        return f"{OKGREEN}{self.label}{ENDC}"


class TestFail(_TestResult):
    def __str__(self):
        return f"{FAIL}{self.label}{ENDC}"


class TestException(Exception):
    pass
