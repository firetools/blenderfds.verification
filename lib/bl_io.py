import os, bpy, tempfile
from . import compare, run_command
from .testing import TestFail, TestOk, TestException

# Common


def open_blend_file(filepath=None):
    if filepath:
        bpy.ops.wm.open_mainfile(filepath=filepath)
    else:
        bpy.ops.wm.read_homefile()


class FakeException(Exception):
    pass


# FDS to Blender


def fds_tree_to_blend(
    package, path, exclude_dirs=None, exclude_files=None, ref_path=None, run_fds=False
):
    """!
    Import all fds files from dir tree to Blender.
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
                results.extend(
                    fds_case_to_blend(
                        package=package,
                        filepath=filepath,
                        ref_path=ref_path,
                        run_fds=run_fds,
                    )
                )
    return results


def fds_case_to_blend(
    package,
    filepath,
    expected_msg=None,
    to_fds_expected_msg=None,
    ref_path=None,
    run_fds=False,
):
    results = list()

    # New blend file with one new scene only
    open_blend_file(filepath=None)  # new file
    old_scs = bpy.data.scenes[:]  # get existing scenes
    sc = bpy.data.scenes.new("scene_tmp")  # get new scene
    for old_sc in old_scs:  # rm existing scenes
        bpy.data.scenes.remove(old_sc, do_unlink=True)

    context = bpy.context

    # fds case to Scene
    name = f"fds case to scene: <{filepath}> to <{sc.name}>"
    try:
        sc.from_fds(context, filepath=filepath)
    except Exception as err:
        if expected_msg:
            if expected_msg == str(err):
                results.append(TestOk(package, name, f"Ok err: <{str(err)}>"))
            else:
                results.append(TestFail(package, name, f"Unexpected msg: <{str(err)}>"))
        else:
            results.append(TestFail(package, name, f"Unexpected err: <{str(err)}>"))
        return results
    else:
        if expected_msg:
            results.append(TestFail(package, name, f"Missed error: <{expected_msg}>"))
            return results
    results.append(TestOk(package, name))

    # New tmp blend to fds
    with tempfile.TemporaryDirectory() as tmppath:

        # Save tmp blend file to set bpy.data.filepath
        bl_filepath = os.path.join(tmppath, sc.name + ".blend")  # /tmp/scene.blend
        bpy.ops.wm.save_as_mainfile(filepath=bl_filepath)

        results.extend(
            blend_to_fds(
                package=package,
                filepath=bl_filepath,
                expected_msg=to_fds_expected_msg,
                ref_path=ref_path,
                run_fds=run_fds,
            )
        )

    return results


# Blender to FDS


def blend_tree_to_fds(
    package, path, exclude_dirs=None, exclude_files=None, ref_path=None, run_fds=False
):
    """!
    Export all blend files from dir tree to fds.
    """
    results = list()
    for p, dirs, files in os.walk(path):
        if exclude_dirs:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in files:
            if filename.endswith(".blend"):
                if exclude_files and filename in exclude_files:
                    continue
                filepath = os.path.join(p, filename)
                results.extend(
                    blend_to_fds(
                        package=package,
                        filepath=filepath,
                        ref_path=ref_path,
                        run_fds=run_fds,
                    )
                )
    return results


def blend_to_fds(
    package,
    filepath,
    expected_msg=None,
    ref_path=None,
    run_fds=False,
):
    results = list()

    # Open blend file
    open_blend_file(filepath=filepath)
    context = bpy.context

    for sc in bpy.data.scenes:
        with tempfile.TemporaryDirectory() as tmppath:

            # Scene to fds case
            fds_path = tmppath
            fds_filepath = os.path.join(fds_path, sc.name + ".fds")  # /tmp/scene.fds
            name = f"scene to fds: <{sc.name}> to <{fds_filepath}>"
            try:
                sc.to_fds(context=context, full=True, save=True, filepath=fds_filepath)
            except Exception as err:
                if expected_msg:
                    if expected_msg == str(err):
                        results.append(TestOk(package, name, f"Ok err: <{str(err)}>"))
                    else:
                        results.append(
                            TestFail(package, name, f"Unexpected msg: <{str(err)}>")
                        )
                else:
                    results.append(
                        TestFail(package, name, f"Unexpected err: <{str(err)}>")
                    )
                return results
            else:
                if expected_msg:
                    results.append(
                        TestFail(package, name, f"Missed error: <{expected_msg}>")
                    )
                    return results
            results.append(TestOk(package, name))

            # Compare with /ref/filename.blend/scene/
            if ref_path:
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

            # Run fds on result
            if run_fds:
                results.extend(
                    run_command.run_command(
                        package=package,
                        filepath=fds_filepath,
                        command="fds",
                        success="STOP: FDS completed successfully",
                        timeout=120,
                    )
                )

    return results
