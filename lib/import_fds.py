import os, tempfile, bpy
from .testing import TestFail, TestOk, TestException


def import_bad_fds_case(package, filepath, expected_exception, expected_msg=None):
    """!
    Import bad fds case from filepath.
    """
    results = list()

    # Import fds case
    name = f"import bad <{filepath}>"
    bpy.ops.wm.read_homefile()  # load default
    sc = bpy.data.scenes.new("tmp")  # new scene
    context = bpy.context
    try:
        sc.from_fds(context, filepath=filepath)
    except expected_exception as err:
        if expected_msg:
            if str(err) == expected_msg:
                results.append(TestOk(package, name))
            else:
                results.append(TestFail(package, name, f"Unexpected error msg <{err}>"))
        else:
            results.append(TestOk(package, name))
    except Exception as err:
        results.append(TestFail(package, name, str(err)))
    else:
        results.append(TestFail(package, name, "Should raise BFException"))

    return results


def import_fds_case(package, filepath):
    """!
    Import fds case from filepath.
    """
    results = list()

    # Import fds case
    name = f"import <{filepath}>"
    bpy.ops.wm.read_homefile()  # load default
    sc = bpy.data.scenes.new("tmp")  # new scene
    context = bpy.context
    try:
        sc.from_fds(context, filepath=filepath)
    except Exception as err:
        results.append(TestFail(package, name, str(err)))
    else:
        results.append(TestOk(package, name))

    # Export imported case
    name = f"export imported <{filepath}>"
    with tempfile.TemporaryDirectory() as tmppath:
        # Save tmp blend file to set bpy.data.filepath
        bl_filepath = os.path.join(tmppath, sc.name + "_tmp.blend")
        bpy.ops.wm.save_as_mainfile(filepath=bl_filepath)
        # Export fds file
        fds_filepath = os.path.join(tmppath, sc.name + "_tmp.fds")
        try:
            bpy.ops.export_scene.fds(all_scenes=False, filepath=fds_filepath)
        except Exception as err:
            results.append(TestFail(package, name, err))
        else:
            results.append(TestOk(package, name))

    return results


def export_scene_to_fds_case(
    package, expected_exception=None, expected_msg=None
):  # FIXME unfinished
    results = list()
    context = bpy.context
    sc = context.scene
    name = f"export scene <{sc.name}>"
    with tempfile.TemporaryDirectory() as tmppath:
        # Save tmp blend file to set bpy.data.filepath
        bl_filepath = os.path.join(tmppath, sc.name + "_tmp.blend")

        bpy.ops.wm.save_as_mainfile(filepath=bl_filepath)
        # Export fds file
        fds_filepath = os.path.join(tmppath, sc.name + "_tmp.fds")
        try:
            bpy.ops.export_scene.fds(all_scenes=False, filepath=fds_filepath)
        except Exception as err:
            results.append(TestFail(package, name, err))
        else:
            results.append(TestOk(package, name))

    return results


def import_fds_tree(package, path, exclude_dirs=None, exclude_files=None):
    """!
    Import recursively all fds cases from path.
    """
    results = list()
    if not os.path.isdir(path):
        raise TestException(f"<{path}> is not a directory")
    for p, dirs, files in os.walk(path):  # recursive, sends filename
        # Exclude dirs
        # https://stackoverflow.com/questions/19859840/excluding-directories-in-os-walk
        if exclude_dirs:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
        # Loop on files
        for filename in files:
            if filename.endswith(".fds"):
                if exclude_files and filename in exclude_files:
                    continue
                filepath = os.path.join(p, filename)
                results.extend(import_fds_case(package, filepath))
    return results
