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


class RECORDER_PT_main_panel(bpy.types.Panel):
    """Main panel class containg Addon GUI."""

    bl_idname = "RECORDER_PT_main_panel"
    bl_label = "Action Recorder Panel"
    bl_category = "Recorder"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Tracked Grease Pencils")
        layout.template_list(
            "RECORDER_UL_item_list",
            "gpen_list",
            scene,
            "observed_gpens",
            scene,
            "observed_gpens_index"
        )

        layout.label(text='Control trackers')
        layout.operator(
            'action_recorder.start_track_active',
            text='Track selected GPencils'
        )

        layout.operator(
            'action_recorder.start_track_name',
            text='Track GPencil by name'
        )

        layout.operator(
            'action_recorder.stop_track_active',
            text='Stop tracking selected GPencils'
        )

        layout.operator(
            'action_recorder.stop_track_name',
            text='Stop tracking GPencil by name'
        )
