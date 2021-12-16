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
    GreasePencil,
    GPencilFrame
)
from bpy.props import IntProperty       # type: ignore

from ..lib import data
from .frame_observer import FrameObserver


def is_gpen_tracked(gpen: GreasePencil) -> bool:
    """Determine if Grease Pencil is currently being tracked."""

    observed_gpen = data.observed_gpen

    if not observed_gpen:
        return False

    return id(gpen) == id(observed_gpen.id)


def add_gpen_tracker(gpen: GreasePencil) -> bool:
    """Start tracking Grease Pencil.

        Returns:
            int: Object ID if objects is added, 0 if object is already present
    """

    if is_gpen_tracked(gpen):
        return False

    data.observed_gpen = data.database.get_observer(gpen)
    data.is_observing = True

    return True


def remove_gpen_tracker() -> None:
    """Stop tracking Grease Pencil."""

    data.observed_gpen = None
    data.is_observing = False


def observe_frame(frame: GPencilFrame) -> FrameObserver:
    """Put observer onto the frame."""

    observer = FrameObserver(frame)

    GPencilFrame.stroke_count = IntProperty(
        name='stroke_count_' + str(id(frame)),
        update=observer.notify(),
        get=observer.get_stroke_count()
    )

    return observer
