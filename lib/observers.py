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


import bpy                                  # type: ignore
import bpy.app.timers as timers             # type: ignore
from bpy.types import (                     # type: ignore
    PropertyGroup,
    GPencilFrame,
    GPencilLayer,
    GreasePencil
)

from .utils import (
    get_timestamp,
    log
)
from .tracking import (
    observe_layers,
    observe_strokes,
    LayerChangesGroup
)

from typing import Callable, Union
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


class FrameObserver(ActiveObserver):
    """Observer class used to observe changes in GPencilFrame object."""

    def __init__(self, observee: GPencilFrame,
                 layer_name: str, add_fn: Callable):
        super().__init__(observe_strokes)

        self.parent_layer = layer_name
        self.frame = observee
        self.strokes = self.frame.strokes
        self.last_count = self.strokes.__len__()
        self.add_change = add_fn

    def get_frame(self) -> GPencilFrame:
        """Get observed GPencilFrame object."""

        return self.frame

    def set_frame(self, frame: GPencilFrame) -> None:
        """Set new GPencilFrame object for observation."""

        self.frame = frame
        self.strokes = self.frame.strokes
        self.last_count = self.frame.strokes.__len__()

    def get_stroke_count(self) -> int:
        """Get count of strokes in tracked layer."""

        return self.strokes.__len__()

    def on_add(self) -> None:
        """Method called in response to addition of a new stroke."""

        print(get_timestamp() + ": stroke added.")

        self.add_change(
            self.parent_layer,
            None,       # TODO: work out referencing
            'Stroke added.',
            'PLUS',
        )

    def on_remove(self) -> None:
        """Method called in response to deletion of a stroke."""

        print(get_timestamp() + ": stroke removed.")

        self.add_change(
            self.parent_layer,
            None,
            'Stroke removed.',
            'X'
        )


class LayerObserver():
    """Observer class used to observe changes in GPencilLayer object.

        This class also doubles as PropertyGroup object used for displaying
        changes in observed layer in UIList.
    """

    def __init__(self, observee: GPencilLayer, add_fn: Callable) -> None:
        self.id = id(observee)
        self.layer = observee
        self.add_change = add_fn
        self.active_frame = FrameObserver(
            self.layer.frames[-1],
            self.layer.info,
            add_fn
        )

    def set_add_function(self, func: Callable) -> None:
        """Set a function to report a change to."""

        self.add_change = func

    def get_layer(self) -> GPencilLayer:
        """Get tracked layer object."""

        return self.layer

    def set_active(self, status: bool) -> None:
        """Propagate status to child observers."""

        self.active_frame.set_active(status)

    def advance_frame(self) -> None:
        """Advance frame for this layer."""

        current_frame = self.active_frame.get_frame()
        new_frame = self.layer.frames.copy(current_frame)
        self.active_frame.set_frame(new_frame)


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
        self.frame_count = 0

        self.layer_observers = dict()
        for layer in observee.layers:
            self.__add_layer__(layer)

        log(f'Observer for { observee } created.')
        # TODO: log new layers

    @property
    def layers(self):
        return self.gpen.layers

    def __add_layer__(self, layer: GPencilLayer) -> None:
        """Add a new layer to track list"""

        layer_observer = LayerObserver(layer, self.__new_record__)
        # layer_observer.set_add_function()
        self.layer_observers[layer] = layer_observer

        item = self.gpen.layer_records.add()
        item.layer_name = layer.info

    def __remove_layer__(self, layer: GPencilLayer) -> None:
        """Remove a layer from track list"""

        name = layer.info
        self.layer_observers.pop(layer)

        for item in self.gpen.layer_records:
            if item.layer_name == name:
                self.gpen.layer_records.remove(item)
                break

    def __new_record__(self, layer_name: str,
                       obj: object, text: str, icon: str) -> None:
        """Create a new record for a given layer"""

        for item in self.gpen.layer_records:
            if item.layer_name == layer_name:
                change = item.changes.add()
                change.obj = obj
                change.text = text
                change.icon = icon

                break

        for layer in self.layer_observers.values():
            layer.advance_frame()
        scene = bpy.context.scene
        scene.frame_set(scene.frame_current + 1)
        self.frame_count += 1

    def get_gpen(self) -> GreasePencil:
        """Get observed GreasePencil object."""

        return self.gpen

    def get_layer_count(self) -> int:
        """Get number of observed layers."""

        return self.layers.__len__()

    def get_layer_records(self,
                          layer_name: str) -> Union[LayerChangesGroup, None]:
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
