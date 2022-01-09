import os, bpy, tempfile
from . import compare
from .testing import TestFail, TestOk, TestException

# FDS to Blender


def fds_tree_to_blend(package, path, exclude_dirs=None, exclude_files=None):
    """!
    Import to blender all fds files from tree.
    """
    results = list()
    for p, dirs, files in os.walk(path):
        if exclude_dirs:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in files:
            if filename.endswith(".fds"):
                if exclude_files and filename in exclude_files:
                    continue
                filepath = os.path.join(p, filename)
                results.extend(fds_to_blend(package, filepath))
    return results


def fds_to_blend(package, filepath):
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
            sc.to_fds(context, full=True, filepath=fds_filepath)
        except Exception as err:
            results.append(TestFail(package, name, str(err)))
        else:
            results.append(TestOk(package, name))

    return results


def bad_fds_to_blend(package, filepath, expected_exception, expected_msg=None):
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
        results.append(TestFail(package, name, "Should raise a BFException"))

    return results


# Blender to FDS


def blend_tree_to_fds(
    package, path, exclude_dirs=None, exclude_files=None, ref_path=None
):
    """!
    Export to fds all blend files from tree and compare result to ref_path.
    """
    results = list()
    for p, dirs, files in os.walk(path):  # recursive, sends filename
        if exclude_dirs:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in files:
            if filename.endswith(".blend"):
                if exclude_files and filename in exclude_files:
                    continue
                filepath = os.path.join(p, filename)
                results.extend(blend_to_fds(package, filepath, ref_path))
    return results


def blend_to_fds(package, filepath, ref_path=None) -> list:
    """!
    Export all scenes to fds from blend file and compare result to ref_path.
    """
    results = list()

    # Open blend file
    context = bpy.context
    bpy.ops.wm.open_mainfile(filepath=filepath)

    # Export each scene to its fds_case and compare it with ref
    for sc in bpy.data.scenes:
        with tempfile.TemporaryDirectory() as tmppath:

            # Export scene
            bpy.context.window.scene = (
                sc  # make scene visible (FIXME should not be needed, see bpy.context)
            )
            fds_path = tmppath
            fds_filepath = os.path.join(fds_path, sc.name + ".fds")  # /tmp/scene.fds
            name = f"Export <{fds_filepath}>"
            try:
                sc.to_fds(context, full=True, filepath=fds_filepath)
            except Exception as err:
                results.append(TestFail(package, name, str(err)))
                return results
            else:
                results.append(TestOk(package, name))

            if ref_path:
                # Compare with /ref/filename.blend/scene/
                ref_sc_path = os.path.join(
                    ref_path, os.path.basename(filepath), sc.name
                )
                results.extend(
                    compare.compare_paths(
                        package=package,
                        ref_path=ref_sc_path,
                        path=fds_path,
                    )
                )

    return results
