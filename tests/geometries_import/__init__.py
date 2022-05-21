"""!
Test importing all kind of geometries (eg. GEOM, GEOM terrain, XB, XYZ, PB).
"""

import os
from lib.bl_io import fds_tree_to_blend
from lib import config

FDS_PATH = "./fds/"
FDS_EXCLUDE_DIRS = None
FDS_EXCLUDE_FILES = None
FDS_REF_PATH = "./fds_ref/"


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return fds_tree_to_blend(
        package=__package__,
        path=os.path.join(current_path, FDS_PATH),
        exclude_dirs=FDS_EXCLUDE_DIRS,
        exclude_files=FDS_EXCLUDE_FILES,
        ref_path=os.path.join(current_path, FDS_REF_PATH),
        run_fds=config.RUN_FDS,
        set_ref=config.SET_REF,
    )
