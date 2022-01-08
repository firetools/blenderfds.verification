from typing import List, Tuple
from . import bcolors, import_mod


def run_tests(test_py_module, requested_test_names=None):
    """!
    Execute tests from test_py_module.
    """
    tests = import_mod.import_submodules(test_py_module, recursive=False)
    print(f"{bcolors.HEADER}Available tests:{bcolors.ENDC}")
    print("  " + "\n  ".join(tests))
    print(f"{bcolors.HEADER}Requested tests:{bcolors.ENDC}")
    print("  " + "\n  ".join(requested_test_names or ("all",)))
    # Run
    print(f"{bcolors.HEADER}Run tests...{bcolors.ENDC}")
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
    # Repeat failed
    for key, value in packages.items():
        print(f"\n{bcolors.HEADER}Detailed failures of <{key}>:{bcolors.ENDC}")
        if not value[1]:
            print("None")
        else:
            for r in value[1]:
                print(r.detail)
    # Results
    print(f"\n{bcolors.HEADER}Overall test results:{bcolors.ENDC}")
    for key, value in packages.items():
        nok = len(value[0])
        nfail = len(value[1])
        print(
            f"{nfail+nok:>8} = {bcolors.OKGREEN}{nok:>6} ok{bcolors.ENDC} + {bcolors.FAIL}{nfail:>6} failed{bcolors.ENDC} in {key}"
        )
    print(f"{len(results):>8} completed")


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
        return f"{bcolors.OKGREEN}{self.label}{bcolors.ENDC}"


class TestFail(_TestResult):
    def __str__(self):
        return f"{bcolors.FAIL}{self.label}{bcolors.ENDC}"


class TestException(Exception):
    pass
