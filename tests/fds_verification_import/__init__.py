"""!
Test importing official FDS verification suite cases except Complex Geometries to Blender files.
"""

import os
from lib.bl_io import fds_tree_to_blend

FDS_CASES_PATH = "../../../firemodels/fds/Verification/"
EXCLUDE_DIRS = ("Complex_Geometry","Heat_Transfer","Miscellaneous")
EXCLUDE_FILES = (
    "ht3d_sphere_51.fds",
    "ht3d_sphere_50.fds",
    "obst_cylinder_mass_flux.fds",
    "obst_sphere_mass_flux.fds",
    "obst_box_mass_flux.fds",
    "obst_cone_mass_flux.fds",
    "obst_cylinder.fds",
    "obst_sphere.fds",
    "obst_cone.fds",
    "obst_rotbox.fds",
    "Morvan_TGA_2.fds",
    "Morvan_TGA.fds",
    "part_baking_soda_450K.fds",
    "part_baking_soda_500K.fds",
    "part_baking_soda_420K.fds"
)

def run():
    current_path = os.path.dirname(os.path.abspath(__file__))
    return fds_tree_to_blend(
        package=__package__,
        path=os.path.join(current_path, FDS_CASES_PATH),
        exclude_dirs=EXCLUDE_DIRS,
        exclude_files=EXCLUDE_FILES,
    )
