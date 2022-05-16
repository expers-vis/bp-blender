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


from bpy.types import (       # type: ignore
    GreasePencil
)
from bpy.props import (       # type: ignore
    IntProperty,
    CollectionProperty
)

from .utils import (
    register_classes,
    unregister_classes,
    get_timestamp,
    log
)
from . import database
from .observers import (
    GPenObserver,
    LayerObserver
)
from .tracking import (
    ChangeGroup,
    LayerChangesGroup
)


# export database instance
data = database.data

__all__ = [
    'register_classes',
    'unregister_classes',
    'get_timestamp',
    'log',
    'data',
    'GPenObserver',
    'LayerObserver',
    'ChangeGroup'
]

classes = [
    ChangeGroup,
    LayerChangesGroup,
]


def register():
    register_classes(classes)

    GreasePencil.layer_index = IntProperty(
        name='layers_index',
        default=0,
        options={'HIDDEN'}
    )
    GreasePencil.layer_records = CollectionProperty(
        type=LayerChangesGroup,
        options={'HIDDEN'}
    )


def unregister():
    unregister_classes(classes)

    try:
        del GreasePencil.layer_index
        del GreasePencil.layer_records
    except AttributeError:
        pass
