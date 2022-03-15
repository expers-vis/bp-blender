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
        self.func = functools.partial(observing_func, self)

    def is_active(self) -> bool:
        """Returns whether observer is active"""

        return self.active

    def set_active(self, status: bool) -> None:
        """Set active status of observer."""

        self.active = status
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
class LayerObserver(ActiveObserver, PropertyGroup):
    """Observer class used to observe changes in GPencilLayer object.

        This class also doubles as PropertyGroup object used for displaying
        changes in observed layer in UIList.
    """

    def __init__(self, observee: GPencilLayer) -> None:
        super().__init__(observe_strokes)

        self.id = id(observee)
        self.name = observee.info
        self.layer = observee
        self.frame = observee.frames[0]
        self.strokes = self.frame.strokes
        self.last_count = self.strokes.__len__()

        # reference list for comparison with actual stroke list
        self.ref_strokes = list(self.strokes)
        # function to record new change on parent gpen observer
        self.add_change: Callable

    @property
    def changes(self):
        return self.layer.changes

    def set_add_function(self, func):
        """Set a function to report a change to."""

        self.add_change = func

    def equals(self, layer):
        """Returns whether layer is observed by this observer."""

        return self.layer == layer

    def get_layer(self) -> GPencilLayer:
        """Get tracked layer object."""

        return self.layer

    def get_stroke_count(self) -> int:
        """Get count of strokes in tracked layer."""

        return self.strokes.__len__()

    def on_add(self) -> None:
        """Method called in response to addition of a new stroke."""

        print(get_timestamp() + ": stroke added.")

        for stroke in reversed(self.strokes):
            if stroke not in self.ref_strokes:
                self.ref_strokes.append(stroke)

                self.add_change(
                    self.name,
                    None,       # TODO: work out referencing
                    'Stroke added.',
                    'PLUS',
                )

    def on_remove(self) -> None:
        """Method called in response to deletion of a stroke."""

        def is_removed(stroke):
            """'stroke not in self.strokes' replacement"""

            for s in self.strokes:
                if s == stroke:
                    return False

            return True

        print(get_timestamp() + ": stroke removed.")

        to_remove = list()

        for stroke in self.ref_strokes:
            if is_removed(stroke):
                to_remove.append(stroke)

                self.add_change(
                    self.name,
                    None,
                    'Stroke removed.',
                    'X'
                )

        for stroke in to_remove:
            self.ref_strokes.remove(stroke)

    def notify(self) -> None:
        """Method to notify observer of change in stroke count."""

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
            self.__add_layer__(layer)

        log(f'Observer for { observee } created.')
        # TODO: log new layers

    @property
    def layers(self):
        return self.gpen.layers

    def __add_layer__(self, layer):
        """Add a new layer to track list"""

        layer_observer = LayerObserver(layer)
        layer_observer.set_add_function(self.__new_record__)
        self.layer_observers[layer] = layer_observer

        item = self.gpen.layer_records.add()
        item.layer_name = layer.info

    def __remove_layer__(self, layer):
        """Remove a layer from track list"""

        name = layer.info
        self.layer_observers.pop(layer)

        for item in self.gpen.layer_records:
            if item.layer_name == name:
                self.gpen.layer_records.remove(item)
                break

    def __new_record__(self, layer_name, obj, text, icon):
        """Create a new record for a given layer"""

        for item in self.gpen.layer_records:
            if item.layer_name == layer_name:
                change = item.changes.add()
                change.obj = obj
                change.text = text
                change.icon = icon

                break

        # TODO: implement keyframe advance

    def get_gpen(self) -> GreasePencil:
        """Get observed GreasePencil object."""

        return self.gpen

    def get_layer_count(self) -> int:
        """Get number of observed layers."""

        return self.layers.__len__()

    def get_layer_records(self, layer_name):
        """Get layer records for given layer."""

        for item in self.gpen.layer_records:
            if item.layer_name == layer_name:
                return item

        return None

    def set_active(self, status: bool) -> None:
        """Set active status and propagate it to child observers."""

        super().set_active(status)

        for layer_observer in self.layer_observers.values():
            layer_observer.set_active(status)

    def on_add(self) -> None:
        """Method called in response to addition of a new layer."""

        log(get_timestamp() + ": layer added.", 'debug')
        print(get_timestamp() + ": layer added.")

        layers = self.gpen.layers

        for layer in layers:
            if layer not in self.layer_observers.keys():
                self.__add_layer__(layer)

    def on_remove(self) -> None:
        """Method called in response to deletion of a layer."""

        log(get_timestamp() + ": layer removed.", 'debug')
        print(get_timestamp() + ": layer removed.")

        gpen_layers = self.gpen.layers
        observed_layers = self.layer_observers.keys()

        to_remove = set(gpen_layers) ^ set(observed_layers)

        for layer in to_remove:
            self.__remove_layer__(layer)

        # adjust layer_index
        self.gpen.layer_index = min(
            max(0, self.gpen.layer_index - 1),
            len(gpen_layers) - 1
        )

    def notify(self) -> None:
        """Method to notify observer of change in layer count."""

        log(str(self.gpen) + ' notified of change', 'debug')
        new_count = self.get_layer_count()

        if(self.last_count < new_count):
            self.on_add()
        elif(self.last_count > new_count):
            self.on_remove()
        self.last_count = new_count
