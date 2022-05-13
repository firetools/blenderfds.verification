"""!
Test copy FDS paramters by operator.
"""

import os
from lib.bl_io import blend_to_fds

BL_FILEPATH_SCENE = "./bl/copy_scene.blend"
SCRIPT_SCENE = """
import bpy
bpy.context.window.scene = sc
bpy.ops.scene.bf_props_to_scene(bf_dest_element="scene_copied")
"""

BL_FILEPATH_OBJECTS = "./bl/copy_objects.blend"
SCRIPT_OBJECTS = """
import bpy
bpy.context.window.scene = sc
bpy.ops.object.bf_props_to_sel_obs()
"""

BL_REF_PATH = "./bl_ref/"


def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    results = list()
    
    results.extend(  # Run scene script and export
        blend_to_fds(
            package=__package__,
            filepath=os.path.join(current_path, BL_FILEPATH_SCENE),
            script=SCRIPT_SCENE,
            ref_path=os.path.join(current_path, BL_REF_PATH),
            run_fds=False,
        )
    )
    
    results.extend(  # Run obs script and export
        blend_to_fds(
            package=__package__,
            filepath=os.path.join(current_path, BL_FILEPATH_OBJECTS),
            script=SCRIPT_OBJECTS,
            ref_path=os.path.join(current_path, BL_REF_PATH),
            run_fds=False,
        )
    )
    
    return results
