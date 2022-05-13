"""!
Test importing official FDS verification suite cases related to bad Complex Geometries to Blender files.
"""

import os, sys, bpy
from lib import TestFail, TestOk
from lib.bl_io import fds_case_to_blend

# BlenderFDS = sys.modules["blenderfds"]
# ERR = BlenderFDS.types.BFException

FDS_PATH = "../../../firemodels/fds/Verification/Complex_Geometry/"
BAD_FILES = (
    (
        "geom_bad_open_surface.fds",
        "ERR: Cube_open: Bad geometry: Non manifold or open geometry detected (4 edges).",
    ),
    (
        "geom_bad_non_manifold_edge.fds",
        "ERR: Cube_non_manifold_edge: Bad geometry: Non manifold vertices detected (2 vertices).",
    ),
    (
        "geom_bad_inconsistent_normals.fds",
        "ERR: Cube_inconsistent_normals: Bad geometry: Inconsistent face normals detected (4 edges).",
    ),
    (
        "geom_bad_non_manifold_vert.fds",
        "ERR: Cube_non_manifold_vert: Bad geometry: Non manifold vertices detected (2 vertices).",
    ),
    (
        "geom_bad_inverted_normals.fds",
        "ERR: Cube_inverted_normals: Bad geometry: Inverted face normals detected.",
    ),
)

# BlenderFDS imports bad geometry, but raises BFException on export


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    results = list()
    for filename, expected_msg in BAD_FILES:
        results.extend(
            fds_case_to_blend(
                package=__package__,
                filepath=os.path.join(current_path, FDS_PATH, filename),
                expected_msg=None,
                to_fds_expected_msg=expected_msg,
                ref_path=None,
                run_fds=False,
            )
        )
    return results
