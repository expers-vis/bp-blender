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


tracked_gpens = list()        # list of ids of tracked objects


def tracked_gpen_len() -> int:
    """Get number of tracked Grease Pencils."""

    return len(tracked_gpens)


def is_gpen_tracked(obj: object) -> bool:
    """Determine if Grease Pencil is tracked."""

    return obj in tracked_gpens


def add_gpen_tracker(obj: object) -> int:
    """Add Grease Pencil on the list of tracked objects.

        Returns:
            int: Object ID if objects is added, 0 if object is already present
    """

    if is_gpen_tracked(obj):
        return 0

    tracked_gpens.append(obj)
    return id(obj)


def remove_gpen_tracker(obj: object) -> int:
    """Remove object from the list of tracked objects.

        Returns:
            int: index of Grease Pencil on the list
    """

    if obj in tracked_gpens:
        index = tracked_gpens.index(obj)
        tracked_gpens.remove(obj)
        return index


def observe_frame(frame: bpy.types.GPencilFrame) -> FrameObserver:
    """Put observer onto the frame."""

    observer = FrameObserver(frame)

    bpy.types.GPencilFrame.stroke_count = bpy.props.IntProperty(
        name='stroke_count_' + str(id(frame)),
        update=observer.notify(),
        get=observer.get_stroke_count()
    )

    return observer
