import os, difflib, filecmp


def diff_fds_file(ref_filepath, filepath):
    if not os.path.isfile(ref_filepath):
        raise IOError(f"<{ref_filepath}> does not exist")
    if not os.path.isfile(filepath):
        raise IOError(f"<{filepath}> does not exist")
    with open(ref_filepath, "r") as f0, open(filepath, "r") as f1:
        lines1 = f0.read().splitlines()
        lines2 = f1.read().splitlines()
    log = str()
    for l in difflib.unified_diff(lines1, lines2, n=0):
        if l[:3] in ("---", "+++", "@@ ") or l[1:7] in (
            "! Gene",
            "! Date",
            "! File",
        ):
            continue
        log += f"\n{l}"
    return log


def diff_bin_file(ref_filepath, filepath):
    if filecmp.cmp(ref_filepath, filepath):
        return
    else:
        return "Different binary files"
