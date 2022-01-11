import os, subprocess
from .testing import TestOk, TestFail, TestException


def run_command_on_tree(
    package,
    path,
    exclude_dirs=None,
    exclude_files=None,
    command="fds",
    success="STOP: FDS completed successfully",
    extension=".fds",
    timeout=3600,
):
    """!
    Run command on dir tree.
    """
    results = list()
    for p, dirs, files in os.walk(path):
        if exclude_dirs:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in files:
            if filename.endswith(extension):
                if exclude_files and filename in exclude_files:
                    continue
                filepath = os.path.join(p, filename)
                results.extend(
                    run_command(package, filepath, command, success, timeout)
                )
    return results


def run_command(
    package,
    filepath,
    command="fds",
    success="STOP: FDS completed successfully",
    timeout=3600,
) -> list:
    """!
    Execute FDS case
    """
    path, _ = os.path.split(filepath)
    name = f"{command} {filepath}"
    try:
        c = subprocess.run(
            [command, filepath],
            cwd=path,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
            encoding="utf-8",
        )
    except subprocess.CalledProcessError as err:
        return (TestFail(package, name, f"Unknown subprocess error: {err}"),)
    log = f"stdout:\n{c.stdout}\nstderr:\n{c.stderr}"
    print()
    if log.find(success) > 0:
        return (TestOk(package, name),)
    return (TestFail(package, name, log),)


# FIXME not used


def rm_clean_fds(path, full=False):
    """!
    Clean all FDS runtime files from path.
    @param path: path to be cleaned.
    """
    extensions = [
        ".binfo",
        ".sinfo",
        ".end",
        ".out",
        ".s3d",
        ".s3d.sz",
        ".csv",
        "_git.txt",
        ".smv",
        ".ge",
        ".ge2",
        ".bf",
        ".bf.bnd",
        ".sf",
        ".sf.bnd",
        ".prt5",
        ".prt5.bnd",
    ]
    if full:
        extensions.extend((".fds", ".bingeom"))
    print(f"Cleaning <{path}> from FDS runtime files.")
    for file in os.scandir(path):
        n = file.name
        for e in extensions:
            if n.endswith(e):
                os.unlink(file.path)
                break
