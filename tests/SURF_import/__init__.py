"""!
Test import a new case and check effects on default case SURFs.
Only necessary SURFs should be exported.
"""

import os
from lib.bl_io import fds_case_to_blend
from lib import config

FDS_FILEPATH = "./fds/thouse5.fds"
REF_PATH = "./fds_ref/"


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return fds_case_to_blend(
        package=__package__,
        filepath=os.path.join(current_path, FDS_FILEPATH),
        expected_msg=None,
        to_fds_expected_msg=None,
        ref_path=os.path.join(current_path, REF_PATH),
        run_fds=config.RUN_FDS,
        set_ref=config.SET_REF,
        keep_default=True,  # export the default, too
    )
