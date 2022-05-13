"""!
Test importing official FDS verification suite cases related to good Complex Geometries to Blender files.
"""

import os
from lib.bl_io import fds_tree_to_blend

FDS_CASES_PATH = "../../../firemodels/fds/Verification/Complex_Geometry/"
EXCLUDE_DIRS = None
EXCLUDE_FILES = (
    "geom_bad_open_surface.fds",
    "geom_bad_non_manifold_edge.fds",
    "geom_bad_inconsistent_normals.fds",
    "geom_bad_non_manifold_vert.fds",
    "geom_bad_inverted_normals.fds",
    "geom_terrain.fds",
    "geom_time4.fds",
    "geom_time3.fds",
    "geom_time2.fds",
    "geom_time.fds",
    "geom_simple.fds",
    "geom_simple2.fds",
    "geom_texture.fds",
    "geom_texture2.fds",
    "sphere_shadow.fds",
    "geom_scale.fds",
    "geom_volume.fds",
    "zero_thick_roof.fds",
    "geom_extruded_poly.fds",
    "geom_elev.fds",
    "sphere_cc_compute.fds",
    "geom_azim.fds",
    "sphere_leak.fds", 
)


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return fds_tree_to_blend(
        package=__package__,
        path=os.path.join(current_path, FDS_CASES_PATH),
        exclude_dirs=EXCLUDE_DIRS,
        exclude_files=EXCLUDE_FILES,
    )
