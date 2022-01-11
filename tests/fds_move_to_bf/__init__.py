import os
from lib.bl_io import fds_tree_to_blend

FDS_PATH = "./fds/"
EXCLUDE_DIRS = None
EXCLUDE_FILES = None
REF_PATH = "./ref/"


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return fds_tree_to_blend(
        package=__package__,
        path=os.path.join(current_path, FDS_PATH),
        exclude_dirs=EXCLUDE_DIRS,
        exclude_files=EXCLUDE_FILES,
        ref_path=os.path.join(current_path, REF_PATH),
        run_fds=True,
    )
