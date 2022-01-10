import datetime, os
from pathlib import Path
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
    results = list()
    for key, item in tests.items():
        if requested_test_names and not any(r in key for r in requested_test_names):
            continue
        print(f"\n{HEADER}Run <{key}>...{ENDC}")
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

    # Output, on screen
    print(f"\n{HEADER}Overall test results (see details in file):{ENDC}")
    for key, value in packages.items():
        nk, nf = len(value[0]), len(value[1])
        nt = nf + nk
        print(
            f"{nt:>7} = {OKGREEN}{nk:>5} ok{ENDC} + {FAIL}{nf:>5} failed{ENDC} in {key}"
        )
    print(f"{len(results):>7} completed")

    # Output, on file
    filename = datetime.datetime.now().strftime("%Y%m%d_%H%M_test.txt")
    filepath = os.path.join("log", filename)
    Path("log").mkdir(parents=True, exist_ok=True)
    with open(filepath, "w") as f:
        for key, value in packages.items():
            f.write(f"\n\n--- <{key}> ---\n")
            if not value[1]:
                f.write("No failures\n")
                continue
            for r in value[1]:
                f.write(r.detail + "\n")


class _TestResult:
    def __init__(self, package, name, log=None):
        self.package = package
        self.name = name
        self.log = log

    def __str__(self):
        return self.label

    @property
    def label(self):
        return (
            f"{self.package}:\n  {self.name[:28]}···{self.name[len(self.name) - 76 :]}"
        )

    @property
    def detail(self):
        return f"\n---\n{self.log}\n{self.label}"


class TestOk(_TestResult):
    def __init__(self, package, name, log=None):
        super().__init__(package, name, log)
        print(end=f"{OKGREEN}Ok {ENDC}")


class TestFail(_TestResult):
    def __init__(self, package, name, log=None):
        super().__init__(package, name, log)
        print(end=f"{FAIL}Fail {ENDC}")


class TestException(Exception):
    pass
