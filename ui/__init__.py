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
from bpy.types import Scene     # type: ignore
from bpy.props import (         # type: ignore
    CollectionProperty,
    IntProperty
)

from .main_panel import RECORDER_PT_main_panel
from .item_list import RECORDER_UL_item_list
from .items import (
    GPenListItem,
    LayerListItem
)


classes = [
    LayerListItem,
    GPenListItem,
    RECORDER_PT_main_panel,
    RECORDER_UL_item_list,
]


def register():
    for cls in classes:
        print(cls)
        bpy.utils.register_class(cls)

    Scene.observed_gpens = CollectionProperty(
        name='observed_gpens',
        type=GPenListItem,
        options={'HIDDEN'}
    )
    Scene.observed_gpens_index = IntProperty(
        name='observed_gpens_index',
        default=0,
        options={'HIDDEN'}
    )


def unregister():
    scene_props = [
        'observed_gpens',
        'observed_gpens_index'
    ]

    while len(scene_props) > 0:
        try:
            prop_name = scene_props.pop()
            exec(f'del Scene.{ prop_name }')
        except (RuntimeError, ValueError):
            pass

    del_list = classes.copy()
    while len(del_list) > 0:
        try:
            cls = del_list.pop()
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
