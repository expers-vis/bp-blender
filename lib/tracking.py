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

from bpy.types import (     # type: ignore
    PropertyGroup,
    Object
)
from bpy.props import (     # type: ignore
    PointerProperty,
    StringProperty,
    IntProperty,
    CollectionProperty
)

from .utils import log
from . import database


class ChangeGroup(PropertyGroup):
    """Property group for storing change data."""

    obj: PointerProperty(type=Object)
    text: StringProperty()
    icon: StringProperty(default='')


class LayerChangesGroup(PropertyGroup):
    """Property group for storing changes to a layer."""

    layer_name: StringProperty()
    change_index: IntProperty(default=0)
    changes: CollectionProperty(type=ChangeGroup)


# active observation functions
def observe_layers(observer) -> None:
    """Actively observe changes to the layer.

        This function will be called periodically by blender and will report
        changes to the active observer.
    """

    new_count = observer.get_layer_count()

    if(observer.last_count < new_count):
        observer.on_add()
    elif(observer.last_count > new_count):
        observer.on_remove()
    observer.last_count = new_count

    return observer.interval


def observe_strokes(observer) -> None:
    """Actively observe changes to the strokes inside the layer.

        This function will be called periodically by blender and will report
        changes to the active observer.
    """

    new_count = observer.get_stroke_count()

    if(observer.last_count < new_count):
        observer.on_add()
    elif(observer.last_count > new_count):
        observer.on_remove()
    observer.last_count = new_count

    return observer.interval


# passive observation functions
def get_active_layer_count(self) -> int:
    """Retrieve number of layers in observed gpen.

        This function will become method of the GreasePencil class called
        to get the number of layers.
    """

    log('getting layer count')

    return len(self.layers)


def notify_layer_change(self, context):
    """Function handling layer change.

        This function will become method of the GreasePencil class called
        when number of layers have changed.
    """

    if database.data.is_observed(self):
        database.data.get_observer(self).notify()
