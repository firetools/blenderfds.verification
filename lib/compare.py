import os, difflib, filecmp
from .testing import TestFail, TestOk


def _diff_txt_file(ref_filepath, txt_filepath) -> str:
    """!
    Diff two text files, header excluded
    """
    with open(ref_filepath, "r") as f0, open(txt_filepath, "r") as f1:
        ref_lines = f0.read().splitlines()
        txt_lines = f1.read().splitlines()
    log = str()
    for l in difflib.unified_diff(ref_lines, txt_lines, n=0):
        # Remove header
        if l[:3] in ("---", "+++", "@@ ") or l[1:4] == "!!!":
            continue
        log += f"\n{l}"
    return log


def compare_paths(package, ref_path, path) -> list:
    """!
    Compare two paths recursively.
    """
    results = list()

    # Check same files
    name = f"Compare files: <{ref_path}>"
    ok = True
    cmp = filecmp.dircmp(ref_path, path)
    if cmp.left_only:
        ok = False
        results.append(TestFail(package, name, f"Missing files: {cmp.left_only}"))
    if cmp.right_only:
        ok = False
        results.append(TestFail(package, name, f"Unexpected files: {cmp.right_only}"))
    if cmp.funny_files:
        ok = False
        results.append(TestFail(package, name, f"Funny files: {cmp.funny_files}"))
    if ok:
        results.append(TestOk(package, name))
    else:
        return results

    # Check file contents
    (_, mismatch, errors) = filecmp.cmpfiles(
        ref_path, path, cmp.common_files, shallow=False
    )
    mismatch.extend(errors)
    for f in mismatch:
        ref_filepath = os.path.join(ref_path, f)
        filepath = os.path.join(path, f)
        name = f"Compare content: <{ref_filepath}>"
        ok = True
        if f.endswith(".fds") or f.endswith(".ge1"):
            log = _diff_txt_file(ref_filepath, filepath)
            if log:
                ok = False
                results.append(TestFail(package, name, log))
        else:
            ok = False
            results.append(TestFail(package, name, f"Different file: <{ref_filepath}>"))
        if ok:
            results.append(TestOk(package, name))

    # Recurse
    for d in cmp.common_dirs:
        new_ref_path = os.path.join(ref_path, d)
        new_path = os.path.join(path, d)
        results.extend(compare_paths(package, new_ref_path, new_path))

    return results
