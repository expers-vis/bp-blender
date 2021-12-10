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


import bpy      # type: ignore

from .frame_observer import FrameObserver


tracked_pencils = list()        # list of ids of tracked objects


def tracked_len() -> int:
    """Get number of tracked objects."""

    return len(tracked_pencils)


def is_tracked(obj: object) -> bool:
    """Determine if object is tracked."""

    return id(obj) in tracked_pencils


def add_tracker(obj: object) -> bool:
    """Add object on the list of tracked objects.

        Returns:
            bool: True if objects is added, False if object is already present
    """

    if is_tracked(obj):
        return False

    tracked_pencils.append(id(obj))
    return True


def remove_tracker(obj: object) -> None:
    """Remove object from the list of tracked objects."""

    oid = id(obj)
    if oid in tracked_pencils:
        tracked_pencils.remove(oid)


def observe_frame(frame: bpy.types.GPencilFrame) -> FrameObserver:
    """Put observer onto the frame."""

    observer = FrameObserver(frame)

    bpy.types.GPencilFrame.stroke_count = bpy.props.IntProperty(
        name='stroke_count_' + str(id(frame)),
        update=observer.notify(),
        get=observer.get_stroke_count()
    )

    return observer
