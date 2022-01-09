import os
from lib.bl_io import fds_tree_to_blend

FDS_CASES_PATH = "../../../firemodels/fds/Validation/"
EXCLUDE_DIRS = ("Crown_Fires",)
EXCLUDE_FILES = None


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return fds_tree_to_blend(
        package=__package__,
        path=os.path.join(current_path, FDS_CASES_PATH),
        exclude_dirs=EXCLUDE_DIRS,
        exclude_files=EXCLUDE_FILES,
    )
