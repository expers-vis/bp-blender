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


import bpy                  # type: ignore
from bpy.types import (     # type: ignore
    Operator
)

from ..lib import data


class Track():
    """Base class for tracking operators."""

    def add_tracker(self, context, gpen):
        """Add gpen to tracked list."""

        data.start_tracking(gpen)

    def remove_tracker(self, context):
        """Remove gpen from tracking list"""

        data.stop_tracking()


class TrackActiveABC(Track):
    """Parent class for tracking selected Grease Pencils."""

    @classmethod
    def selected(cls) -> bool:
        """Check if there are selected objects."""

        return len(bpy.context.selected_objects) > 0

    @classmethod
    def only_pencils(cls) -> bool:
        """Check if selected objects are only Grease Pencils."""

        for obj in bpy.context.selected_objects:
            if obj.type != 'GPENCIL':
                return False

        return True

    @classmethod
    def poll(cls, context) -> bool:
        """Check if operator can be executed."""

        return (
            context.area.type == "VIEW_3D"
            and cls.selected()
            and cls.only_pencils()
        )


class RECORDER_OT_start_track_active(TrackActiveABC, Operator):
    """Start tracking of selected Grease Pencil strokes."""

    bl_idname = "action_recorder.start_track_active"
    bl_label = "Tracker Start Operartor"
    bl_description = "Start tracking of selected Grease Pencil strokes."

    def execute(self, context) -> set:
        """Execute the operator."""

        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            gpen = obj.data

            if data.is_observed(gpen):
                self.report(
                    {'INFO'},
                    '{} is already being tracked!'.format(gpen.name)
                )
            else:
                self.add_tracker(context, gpen)
                print("Tracking " + str(gpen))

        return {'FINISHED'}


class RECORDER_OT_stop_track_active(Track, Operator):
    """Stop tracking of selected Grease Pencil strokes."""

    bl_idname = "action_recorder.stop_track_active"
    bl_label = "Tracker Stop Operartor"
    bl_description = "Stop tracking of selected Grease Pencil strokes."

    def execute(self, context) -> set:
        """Execute the operator."""

        self.remove_tracker(context)
        print("Stopped tracking.")

        return {'FINISHED'}
