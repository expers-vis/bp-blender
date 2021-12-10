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
from typing import Union

from ..lib import (
    is_tracked,
    add_tracker,
    remove_tracker,
    tracked_len
)


class Track():
    """Base class for tracking operators."""

    def add_tracker(self, context, obj):
        """Add object to tracked list."""

        add_tracker(obj)
        # TODO: add trackers based on class
        context.scene.observed_gpens.add()

    def remove_tracker(self, context, obj):
        """Remove object from tracking list"""

        remove_tracker(obj)
        # TODO: add trackers based on class
        context.scene.observed_gpens.remove()


# -- select tracking -- #
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


class RECORDER_OT_start_track_active(TrackActiveABC, bpy.types.Operator):
    """Start tracking of selected Grease Pencil strokes."""

    bl_idname = "action_recorder.start_track_active"
    bl_label = "Tracker Start Operartor"
    bl_description = "Start tracking of selected Grease Pencil strokes."

    def execute(self, context) -> set:
        """Execute the operator."""

        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            gpen = obj.data

            if is_tracked(gpen):
                self.report(
                    {'INFO'},
                    '{} is already being tracked!'.format(gpen.name)
                )
            else:
                self.add_tracker(context, gpen)
                print("Tracking " + str(gpen))

        return {'FINISHED'}


class RECORDER_OT_stop_track_active(TrackActiveABC, bpy.types.Operator):
    """Stop tracking of selected Grease Pencil strokes."""

    bl_idname = "action_recorder.stop_track_active"
    bl_label = "Tracker Stop Operartor"
    bl_description = "Stop tracking of selected Grease Pencil strokes."

    @classmethod
    def poll(cls, context) -> bool:
        """Check if operator can be executed."""

        return (
            TrackActiveABC.poll(context)
            and tracked_len() > 0
        )

    def execute(self, context) -> set:
        """Execute the operator."""

        selected_objects = bpy.context.selected_objects

        for obj in selected_objects:
            gpen = obj.data

            # TODO: remove check on implemetation
            if is_tracked(gpen):
                self.remove_tracker(context, gpen)
                print("Stopped tracking " + str(gpen))

        return {'FINISHED'}


# -- by name tracking -- #
class TrackNameABC(Track):
    """Parent class for tracking Grease Pencils by name."""

    def get_gpen(self, name: str) -> Union[bpy.types.GreasePencil, None]:
        """Get Grease Pencil by name.

            Returns:
                GreasePencil: if found
                None: if not found
        """

        gpen = None

        for obj in bpy.context.editable_objects:
            # take into account both object and GPen names
            name_match = (obj.name == name or obj.data.name == name)
            if name_match and (obj.type == 'GPENCIL'):
                gpen = obj.data
                break

        return gpen


class RECORDER_OT_start_track_name(TrackNameABC, bpy.types.Operator):
    """Start tracking of Grease pencil by name."""

    bl_idname = "action_recorder.start_track_name"
    bl_label = "Select Grease Pencil you would like to track"
    bl_description = "Start tracking of Grease Pencil by name."

    input_name: bpy.props.StringProperty(
        name='Grease Pencil name: ',        # noqa: F722
        default=''                          # noqa: F722
    )

    def execute(self, context) -> set:
        """Execute the operator."""

        gpen_name = self.input_name
        gpen = self.get_gpen(gpen_name)

        if not gpen:
            self.report(
                {'WARNING'},
                'Grease Pencil \"{}\" was not found!'.format(gpen_name)
            )
            return {'CANCELLED'}

        if is_tracked(gpen):
            self.report(
                {'INFO'},
                '{} is already being tracked!'.format(gpen.name)
            )
        else:
            self.add_tracker(context, gpen)
            print("Tracking " + str(gpen))

        return {'FINISHED'}

    def invoke(self, context, event):
        # show input pop-up
        return context.window_manager.invoke_props_dialog(self)


class RECORDER_OT_stop_track_name(TrackNameABC, bpy.types.Operator):
    """Stop tracking of Grease pencil by name."""

    bl_idname = "action_recorder.stop_track_name"
    bl_label = "Select Grease Pencil you would like to stop tracking"
    bl_description = "Stop tracking of Grease Pencil by name."

    input_name: bpy.props.StringProperty(
        name='Grease Pencil name: ',        # noqa: F722
        default=''                          # noqa: F722
    )

    @classmethod
    def poll(cls, context) -> bool:
        """Check if operator can be executed."""

        return (
            context.area.type == "VIEW_3D"
            and tracked_len() > 0
        )

    def execute(self, context) -> set:
        """Execute the operator."""

        gpen_name = self.input_name
        gpen = self.get_gpen(gpen_name)

        if not gpen:
            self.report(
                {'WARNING'},
                'Grease Pencil \"{}\" was not found!'.format(gpen_name)
            )
            return {'CANCELLED'}

        # TODO: remove check on implemetation
        if is_tracked(gpen):
            self.remove_tracker(context, gpen)
            print("Stopped tracking " + str(gpen))

        return {'FINISHED'}

    def invoke(self, context, event):
        # show input pop-up
        return context.window_manager.invoke_props_dialog(self)
