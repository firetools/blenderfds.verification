"""!
Test exporting all kind of geometries (eg. GEOM, GEOM terrain, XB, XYZ, PB).
"""

import os
from lib.bl_io import blend_tree_to_fds

BL_PATH = "./bl/"
BL_EXCLUDE_DIRS = None
BL_EXCLUDE_FILES = None
BL_REF_PATH = "./bl_ref/"


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return blend_tree_to_fds(
        package=__package__,
        path=os.path.join(current_path, BL_PATH),
        exclude_dirs=BL_EXCLUDE_DIRS,
        exclude_files=BL_EXCLUDE_FILES,
        ref_path=os.path.join(current_path, BL_REF_PATH),
        run_fds=True,
    )
