"""!
Test aligning MESHes by operator.
"""

import os
from lib.bl_io import blend_to_fds
from lib import config

BL_FILEPATH = "./bl/set_suggested_cell_size.blend"
SCRIPT = """
import bpy
bpy.context.window.scene = sc
bpy.ops.object.bf_set_suggested_mesh_cell_size(
    bf_max_hrr=2000.,
    bf_ncell=10,
    bf_poisson_restriction=True,
)
"""
BL_REF_PATH = "./bl_ref/"


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    results = list()
    results.extend(  # Run script and export
        blend_to_fds(
            package=__package__,
            filepath=os.path.join(current_path, BL_FILEPATH),
            script=SCRIPT,
            ref_path=os.path.join(current_path, BL_REF_PATH),
            run_fds=config.RUN_FDS,
            set_ref=config.SET_REF,
        )
    )
    return results
