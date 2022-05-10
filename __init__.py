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


from . import lib
from . import operators
from . import ui

verbose = True

bl_info = {
    "name": "Action Recorder",
    "author": "Martin Hiner (xhiner00)",
    "description": "Record your creative process and export it as a showcase animation.",       # noqa
    "blender": (3, 0, 0),
    "version": (1, 0, 0),
    "location": "3D View > UI > Recorder",
    "category": "User"
}


def register():
    try:
        lib.register()
        operators.register()
        ui.register()
    except Exception as e:
        unregister()
        raise e


def unregister():
    lib.unregister()
    operators.unregister()
    ui.unregister()


# run script directly from blender text editor
if __name__ == '__main__':
    register()
