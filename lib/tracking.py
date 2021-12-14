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


import bpy                              # type: ignore
from bpy.types import (                 # type: ignore
    GreasePencil,
    GPencilFrame
)
from bpy.props import IntProperty       # type: ignore

from .frame_observer import FrameObserver


def is_gpen_tracked(gpen: GreasePencil) -> bool:
    """Determine if Grease Pencil is tracked."""

    scene = bpy.context.scene

    return id(gpen) == id(scene.observed_gpen)


def add_gpen_tracker(gpen: GreasePencil) -> bool:
    """Start tracking Grease Pencil.

        Returns:
            int: Object ID if objects is added, 0 if object is already present
    """

    if is_gpen_tracked(gpen):
        return False

    scene = bpy.context.scene

    scene.observed_gpen = gpen
    scene.is_observing = True

    return True


# TODO
def remove_gpen_tracker() -> None:
    """Stop tracking Grease Pencil.

        Returns:
            data: TODO: return data from tracking
    """

    scene = bpy.context.scene

    scene.observed_gpen = None
    scene.is_observing = False


def observe_frame(frame: GPencilFrame) -> FrameObserver:
    """Put observer onto the frame."""

    observer = FrameObserver(frame)

    GPencilFrame.stroke_count = IntProperty(
        name='stroke_count_' + str(id(frame)),
        update=observer.notify(),
        get=observer.get_stroke_count()
    )

    return observer
