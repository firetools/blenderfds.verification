import subprocess, sys
from . import bcolors


def _first_run(script_pathfile, blender_pathfile):
    print(f"{bcolors.HEADER}Run Blender...{bcolors.ENDC}")
    # Prepare process
    process = [
        blender_pathfile,
        "--background",
        "--python",
        script_pathfile,
        "--",  # allow following user options
    ]
    # Add user options
    options = sys.argv[1:]  # send user options
    process.extend(options)
    # Run myself in Blender (second run)
    try:
        subprocess.run(
            process,
            check=True,
            # timeout=3600,
        )
    except subprocess.CalledProcessError as err:
        print(f"{bcolors.FAIL}Blender error.{bcolors.ENDC}\n{err}")
        exit(1)
    # Exit here when first run is finished
    # otherwise main would run again
    print(f"{bcolors.HEADER}\nBlender end.{bcolors.ENDC}")
    exit(0)


def run_script_in_blender(script_pathfile, blender_pathfile):
    """!
    Launch current script in Blender.
    """
    try:
        import bpy  # Blender running?
    except ModuleNotFoundError:  # No
        _first_run(script_pathfile, blender_pathfile)
    # Blender is running now
