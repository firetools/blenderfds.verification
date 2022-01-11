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
)


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return fds_tree_to_blend(
        package=__package__,
        path=os.path.join(current_path, FDS_CASES_PATH),
        exclude_dirs=EXCLUDE_DIRS,
        exclude_files=EXCLUDE_FILES,
    )
