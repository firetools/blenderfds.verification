"""!
Test exporting Blender view layer FDS case variations
from Blender files to fds, and compare the result with a reference.
"""

import os
from lib.bl_io import blend_to_fds
from lib import config

BL_PATH = "./bl/"
EXCLUDE_DIRS = None
EXCLUDE_FILES = None
REF_PATH = "./bl_ref/"


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    results = list()
    results.extend(
        blend_to_fds(
            package=__package__,
            filepath=os.path.join(current_path, BL_PATH, "view_layer_1M.blend"),
            script=None,
            script_expected_msg=None,
            expected_msg=None,
            ref_path=os.path.join(current_path, REF_PATH),
            run_fds=config.RUN_FDS,
            set_ref=config.SET_REF,
        )
    )
    results.extend(
        blend_to_fds(
            package=__package__,
            filepath=os.path.join(current_path, BL_PATH, "view_layer_4M.blend"),
            script=None,
            script_expected_msg=None,
            expected_msg=None,
            ref_path=os.path.join(current_path, REF_PATH),
            run_fds=config.RUN_FDS,
            set_ref=config.SET_REF,
        )
    )
    return results
