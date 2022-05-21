"""!
Test importing all official FDS validation suite cases to Blender files.
"""

import os
from lib.bl_io import fds_tree_to_blend
from lib import config

FDS_PATH = "../../../firemodels/fds/Validation/"
EXCLUDE_DIRS = ("Crown_Fires",)
EXCLUDE_FILES = (
    "free_conv_sphere_1_16.fds",
    "free_conv_sphere_1_8.fds",
)


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return fds_tree_to_blend(
        package=__package__,
        path=os.path.join(current_path, FDS_PATH),
        exclude_dirs=EXCLUDE_DIRS,
        exclude_files=EXCLUDE_FILES,
        set_ref=config.SET_REF,
    )
