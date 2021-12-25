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


from bpy.types import (                 # type: ignore
    PropertyGroup,
    GreasePencil
)

from .database import data
from .utils import get_timestamp, log


class GPenObserver(PropertyGroup):
    """Observer class used to observe changes in GreasePencil object.

        This class also doubles as PropertyGroup object used for displaying
        items in UiList.
    """

    def __init__(self, observee: GreasePencil) -> None:
        self.id = id(observee)
        self.name = observee.name
        self.gpen = observee
        self.last_count = self.layers.__len__()

    @property
    def layers(self):
        return self.gpen.layers

    def get_gpen(self) -> GreasePencil:
        """Get observed GreasePencil object."""

        return self.gpen

    def get_layer_count(self) -> int:
        """Get number of observed layers."""

        return self.layers.__len__()

    def on_add(self) -> None:
        print(get_timestamp() + ": layer added.")

    def on_remove(self) -> None:
        print(get_timestamp() + ": layer removed.")

    def notify(self) -> None:
        log(str(self.gpen) + ' notified of change', 'debug')
        new_count = self.get_layer_count()

        if(self.last_count < new_count):
            self.on_add()
        elif(self.last_count > new_count):
            self.on_remove()
        self.last_count = new_count


def get_active_layer_count(self) -> int:
    """Retrieve number of layers in observed gpen.

        This function will become method of the GreasePencil class called
        to get the number of layers.
    """

    print('getting layer count')
    log('getting layer count')

    return len(self.layers)


def notify_layer_change(self, context):
    """Function handling layer change.

        This function will become method of the GreasePencil class called
        when number of layers have changed.
    """

    print('notifying ' + str(self))
    log('notifying ' + str(self), 'debug')

    if data.is_observed(self):
        data.get_observer(self).notify()
