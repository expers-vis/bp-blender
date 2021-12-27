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
import bpy.app.timers as timers             # type: ignore

from .utils import get_timestamp, log
from .tracking import observe_layers


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

        # active observing
        self.active = False
        self.paused = False
        self.interval = 1.0

    @property
    def layers(self):
        return self.gpen.layers

    def is_active(self) -> bool:
        """Returns whether observer is active"""

        return self.active

    def set_active(self, status: bool) -> None:
        """Set active status of observer"""

        self.active = status
        registered = timers.is_registered(observe_layers)

        if status and (not registered):
            timers.register(observe_layers)
        elif (not status) and registered:
            timers.unregister(observe_layers)

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
