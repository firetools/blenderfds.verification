"""!
Test importing the CATF namelist and all its variations
from fds cases to Blender files, export them again to fds,
and compare the result with a reference.
"""

import os
from lib.bl_io import fds_tree_to_blend
from lib import config

FDS_PATH = "./fds/"
EXCLUDE_DIRS = None
EXCLUDE_FILES = None
REF_PATH = "./fds_ref/"


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return fds_tree_to_blend(
        package=__package__,
        path=os.path.join(current_path, FDS_PATH),
        exclude_dirs=EXCLUDE_DIRS,
        exclude_files=EXCLUDE_FILES,
        ref_path=os.path.join(current_path, REF_PATH),
        run_fds=config.RUN_FDS,
        set_ref=config.SET_REF,
    )
