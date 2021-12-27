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


from bpy.types import GreasePencil      # type: ignore
from bpy.props import IntProperty       # type: ignore

from .utils import get_timestamp
from .database import data
from .gpen_observer import (
    GPenObserver
)
from .tracking import (
    get_active_layer_count,
    notify_layer_change
)
from .layer_observer import LayerObserver


# add classes to __all__ to comply with PEP8
__all__ = [
    'get_timestamp',
    'data',
    'GPenObserver',
    'LayerObserver'
]


def register():
    GreasePencil.layer_index = IntProperty(
        name='layers_index',
        default=0,
        options={'HIDDEN'}      # noqa
    )
    GreasePencil.layer_count = IntProperty(
        name='layer_count',
        get=get_active_layer_count,
        update=notify_layer_change,
        options={'HIDDEN'},     # noqa
    )


def unregister():
    try:
        del GreasePencil.layer_index
        del GreasePencil.layer_count
    except AttributeError:
        pass
