"""!
Test exporting geometry with imperial units.
"""

import os
from lib.bl_io import blend_tree_to_fds
from lib import config

BL_PATH = "./bl/"
EXCLUDE_DIRS = None
EXCLUDE_FILES = None
SCRIPT = """
import bpy
bpy.context.window.scene = sc
sc.unit_settings.system = "IMPERIAL"
print(f"Units set to {sc.unit_settings.system}")
"""
BL_REF_PATH = "./bl_ref/"

def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return blend_tree_to_fds(
        package=__package__,
        path=os.path.join(current_path, BL_PATH),
        exclude_dirs=EXCLUDE_DIRS,
        exclude_files=EXCLUDE_FILES,
        script=SCRIPT,
        ref_path=os.path.join(current_path, BL_REF_PATH),
        run_fds=config.RUN_FDS,
        set_ref=config.SET_REF,
    )
