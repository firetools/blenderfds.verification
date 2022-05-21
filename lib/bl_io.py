import os, bpy, tempfile, shutil
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
    package,
    path,
    exclude_dirs=None,
    exclude_files=None,
    ref_path=None,
    run_fds=False,
    set_ref=False,
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
                        set_ref=set_ref,
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
    set_ref=False,
):
    results = list()
    print(f"fds_case_to_blend: {filepath}")
    # New blend file with one new scene only
    open_blend_file(filepath=None)  # new file
    old_scs = bpy.data.scenes[:]  # get existing scenes
    sc = bpy.data.scenes.new("scene_tmp")  # get new scene
    for old_sc in old_scs:  # rm existing scenes
        bpy.data.scenes.remove(old_sc, do_unlink=True)

    context = bpy.context

    # fds case to Scene
    name = f"Scene from_fds: <{sc.name}> <{filepath}>"
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
            results.append(TestFail(package, name, f"Missed err: <{expected_msg}>"))
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
                set_ref=set_ref,
            )
        )

    return results


# Blender to FDS


def blend_tree_to_fds(
    package,
    path,
    exclude_dirs=None,
    exclude_files=None,
    ref_path=None,
    run_fds=False,
    set_ref=False,
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
                        set_ref=set_ref,
                    )
                )
    return results


def _exec_script(package, sc, script, expected_msg):
    results = list()
    name = f"Script on Scene: <{sc.name}>"
    try:
        exec(script)
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
            results.append(TestFail(package, name, f"Missed err: <{expected_msg}>"))
            return results
    results.append(TestOk(package, name))
    return results


def blend_to_fds(
    package,
    filepath,
    script=None,
    script_expected_msg=None,
    expected_msg=None,
    ref_path=None,
    run_fds=False,
    set_ref=False,
):
    results = list()
    print(f"blend_to_fds: {filepath}")

    # Open blend file
    open_blend_file(filepath=filepath)
    context = bpy.context

    for sc in bpy.data.scenes:
        with tempfile.TemporaryDirectory() as tmppath:

            # Execute script
            if script:
                results.extend(
                    _exec_script(
                        package=package,
                        sc=sc,
                        script=script,
                        expected_msg=script_expected_msg,
                    )
                )

            # Scene to fds case
            fds_path = tmppath
            fds_filepath = os.path.join(fds_path, sc.name + ".fds")  # /tmp/scene.fds
            name = f"Scene to_fds: <{sc.name}> <{fds_filepath}>"
            try:
                sc.bf_config_directory = fds_path
                sc.to_fds(context=context, full=True, save=True)
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

                # If requested, copy over /ref/filename.blend/scene/
                if set_ref:
                    print(f"Setting ref: {ref_sc_path}")
                    if os.path.exists(path=ref_sc_path):
                        shutil.rmtree(path=ref_sc_path)
                    shutil.copytree(src=fds_path, dst=ref_sc_path)

            # Run fds on result
            if run_fds:
                results.extend(
                    run_command.run_command(
                        package=package,
                        filepath=fds_filepath,
                        command="fds",
                        success="STOP:",
                        timeout=120,
                    )
                )

    return results
