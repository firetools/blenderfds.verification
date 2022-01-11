import lib


def run():
    name = "BlenderFDS exists"
    try:
        import bpy
    except:
        raise lib.TestException("Blender not working.")
    try:
        bpy.context.scene.bf_config_directory
    except:
        raise lib.TestException("BlenderFDS not preloaded.")
    return lib.TestOk(__package__, name)