"""!
Test exporting/importing all kind of geometries (eg. GEOM, GEOM terrain, XB, XYZ, PB).
"""

import os
from lib.bl_io import blend_tree_to_fds, fds_tree_to_blend

BL_PATH = "./bl/"
BL_EXCLUDE_DIRS = None
BL_EXCLUDE_FILES = None
BL_REF_PATH = "./bl_ref/"

FDS_PATH = "./fds/"
FDS_EXCLUDE_DIRS = None
FDS_EXCLUDE_FILES = None
FDS_REF_PATH = "./fds_ref/"


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    results = list()
    results.extend(  # Export
        blend_tree_to_fds(
            package=__package__,
            path=os.path.join(current_path, BL_PATH),
            exclude_dirs=BL_EXCLUDE_DIRS,
            exclude_files=BL_EXCLUDE_FILES,
            ref_path=os.path.join(current_path, BL_REF_PATH),
            run_fds=True,
        )
    )
    results.extend(  # Import
        fds_tree_to_blend(
            package=__package__,
            path=os.path.join(current_path, FDS_PATH),
            exclude_dirs=FDS_EXCLUDE_DIRS,
            exclude_files=FDS_EXCLUDE_FILES,
            ref_path=os.path.join(current_path, FDS_REF_PATH),
            run_fds=True,
        )
    )
    return results
