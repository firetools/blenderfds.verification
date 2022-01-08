import os, sys, bpy
from lib.import_fds import import_bad_fds_case
from lib import TestFail, TestOk

BlenderFDS = sys.modules["blenderfds"]

FDS_CASES_PATH = "../../../firemodels/fds/Verification/Complex_Geometry/"
INCLUDE_FILES = (
    "geom_bad_open_surface.fds",
    "geom_bad_non_manifold_edge.fds",
    "geom_bad_inconsistent_normals.fds",
    "geom_bad_non_manifold_vert.fds",
    "geom_bad_inverted_normals.fds",
)


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    results = list()
    for filename in INCLUDE_FILES:
        filepath = os.path.join(current_path, FDS_CASES_PATH, filename)
        rs = import_export_bad_geom(__package__, filepath, BlenderFDS.types.BFException)
        results.extend(rs)
    return results


# BlenderFDS imports bad geometry, but raises BFException on export


def import_export_bad_geom(
    package, filepath, expected_exception=None, expected_msg=None
):
    results = list()
    name = f"Import bad geom <{filepath}>"
    bpy.ops.wm.read_homefile()  # load default
    sc = bpy.data.scenes.new("tmp")  # new scene
    context = bpy.context

    # Import bad geometry
    try:
        sc.from_fds(context, filepath=filepath)
    except Exception as err:
        results.append(TestFail(package, name, str(err)))
        return results
    else:
        results.append(TestOk(package, name))

    # Export bad geometry
    name = f"Export bad geom <{filepath}>"
    try:
        sc.to_fds(context, full=True)
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
