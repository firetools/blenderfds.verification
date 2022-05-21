"""!
Test generation of free_text when importing.
"""

import os
from lib.bl_io import fds_tree_to_blend
from lib import config

FDS_CASES_PATH = "./fds/"
FDS_REF_PATH = "./fds_ref/"


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return fds_tree_to_blend(
        package=__package__,
        path=os.path.join(current_path, FDS_CASES_PATH),
        ref_path=os.path.join(current_path, FDS_REF_PATH),
        run_fds=config.RUN_FDS,
        set_ref=config.SET_REF,
    )
