#!/usr/bin/env python3

# BlenderFDS, an open tool for the NIST Fire Dynamics Simulator
# Copyright (C) 2013  Emanuele Gissi, http://www.blenderfds.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""!
Automatic verification script for continous integration.
"""

import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from lib import run_blender, testing

try:
    import bpy
except ImportError:
    pass

BLENDER_PATHFILE = "./blender"
TEST_PY_MODULE = "tests"

if __name__ == "__main__":
    run_blender.run_script_in_blender(
        script_pathfile=os.path.abspath(__file__),  # myself
        blender_pathfile=BLENDER_PATHFILE,
    )
    testing.run_tests(test_py_module=TEST_PY_MODULE, requested_test_names=sys.argv[5:])
