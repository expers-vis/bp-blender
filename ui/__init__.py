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


import bpy                      # type: ignore

from .main_panel import RECORDER_PT_main_panel
from .layer_list import RECORDER_UL_layer_list


classes = [
    RECORDER_PT_main_panel,
    RECORDER_UL_layer_list,
]


def register():
    for cls in classes:
        print(cls)
        bpy.utils.register_class(cls)


def unregister():
    del_list = classes.copy()

    while len(del_list) > 0:
        try:
            cls = del_list.pop()
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
