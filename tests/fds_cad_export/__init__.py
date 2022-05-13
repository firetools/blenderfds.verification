"""!
Test exporting the official FDS cad blend files
from Blender files to fds, and compare the result with a reference.
"""

import os
from lib.bl_io import blend_tree_to_fds

BL_PATH = "../../../firemodels/cad/"  # blend tree
EXCLUDE_DIRS = None
EXCLUDE_FILES = None
REF_PATH = "./bl_ref/"


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return blend_tree_to_fds(
        package=__package__,
        path=os.path.join(current_path, BL_PATH),
        exclude_dirs=EXCLUDE_DIRS,
        exclude_files=EXCLUDE_FILES,
        ref_path=os.path.join(current_path, REF_PATH),
        run_fds=False,
    )
