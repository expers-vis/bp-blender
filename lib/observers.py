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


import bpy.app.timers as timers             # type: ignore
from bpy.types import (                 # type: ignore
    PropertyGroup,
    GPencilLayer,
    GreasePencil
)

from .utils import (
    get_timestamp,
    log
)
from .tracking import (
    observe_layers,
    observe_strokes
)

from typing import Callable
import functools


class ActiveObserver():
    """Observer class used to actively observe changes in object.

        Change is observed actively, meaning that the observing
        function is called periodically by blender.
    """

    def __init__(self, observing_func: Callable) -> None:
        self.active = False
        self.interval = 1.0
        self.func = observing_func

    def is_active(self) -> bool:
        """Returns whether observer is active"""

        return self.active

    def set_active(self, status: bool) -> None:
        """Set active status of observer."""

        self.active = status
        func = functools.partial(self.func, self)
        registered = timers.is_registered(self.func)

        if status and (not registered):
            timers.register(self.func)
        elif (not status) and registered:
            timers.unregister(self.func)

    def set_interval(self, interval: float) -> None:
        """Change the interval between observing functions calls"""

        if interval > 0.0:
            self.interval = interval
        else:
            log('Function interval cannot be negative or equal to 0.', 'error')


# NOTE: Initial limiting factor: only first frame is observed
class LayerObserver(ActiveObserver):
    """Observer class used to observe changes in GPencilLayer object."""

    def __init__(self, observee: GPencilLayer) -> None:
        super().__init__(observe_strokes)

        self.id = id(observee)
        self.name = observee.info
        self.layer = observee
        self.frame = observee.frames[0]
        self.last_count = self.frame.strokes.__len__()

        self.changes = list()

    def equals(self, layer):
        """Returns whether layer is observed by this observer."""

        return self.layer == layer

    def get_layer(self) -> GPencilLayer:
        return self.layer

    def get_stroke_count(self) -> int:
        return self.strokes.__len__()

    def on_add(self) -> None:
        print(get_timestamp() + ": stroke added.")

    def on_remove(self) -> None:
        print(get_timestamp() + ": stroke removed.")

    def notify(self) -> None:
        new_count = self.get_stroke_count()

        if(self.last_count < new_count):
            self.on_add()
        elif(self.last_count > new_count):
            self.on_remove()
        self.last_count = new_count


class GPenObserver(ActiveObserver, PropertyGroup):
    """Observer class used to observe changes in GreasePencil object.

        This class also doubles as PropertyGroup object used for displaying
        items in UIList.
    """

    def __init__(self, observee: GreasePencil) -> None:
        super().__init__(observe_layers)

        self.id = id(observee)
        self.name = observee.name
        self.gpen = observee
        self.last_count = self.layers.__len__()

        self.layer_observers = dict()
        for layer in observee.layers:
            self.layer_observers[layer] = LayerObserver(layer)

        log(f'Observer for { observee } created.')

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
        log(get_timestamp() + ": layer added.", 'debug')
        print(get_timestamp() + ": layer added.")

        layers = self.gpen.layers

        for layer in layers:
            if layer not in self.layer_observers.keys():
                self.layer_observers[layer] = LayerObserver(layer)

    def on_remove(self) -> None:
        log(get_timestamp() + ": layer removed.", 'debug')
        print(get_timestamp() + ": layer removed.")

        gpen_layers = self.gpen.layers
        observed_layers = self.layer_observers.keys()

        to_remove = set(gpen_layers) ^ set(observed_layers)

        for layer in to_remove:
            self.layer_observers.pop(layer)

        # adjust layer_index
        self.gpen.layer_index = min(
            max(0, self.gpen.layer_index - 1),
            len(gpen_layers) - 1
        )

    def notify(self) -> None:
        log(str(self.gpen) + ' notified of change', 'debug')
        new_count = self.get_layer_count()

        if(self.last_count < new_count):
            self.on_add()
        elif(self.last_count > new_count):
            self.on_remove()
        self.last_count = new_count
