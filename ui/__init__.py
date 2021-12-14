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
from bpy.types import (         # type: ignore
    Scene,
    GreasePencil
)
from bpy.props import (         # type: ignore
    PointerProperty,
    BoolProperty
)

from .main_panel import RECORDER_PT_main_panel


classes = [
    RECORDER_PT_main_panel,
]


def register():
    for cls in classes:
        print(cls)
        bpy.utils.register_class(cls)

    Scene.observed_gpen = PointerProperty(
        name='observed_gpen',
        type=GreasePencil,
        options={'HIDDEN'}

    )
    Scene.is_observing = BoolProperty(
        name='is_observing',
        default=False,
        options={'HIDDEN'}
    )


def unregister():
    scene_props = [
        'observed_gpen',
        'is_observing'
    ]

    while len(scene_props) > 0:
        try:
            prop_name = scene_props.pop()
            exec(f'del Scene.{ prop_name }')
        except AttributeError:
            pass

    del_list = classes.copy()
    while len(del_list) > 0:
        try:
            cls = del_list.pop()
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
