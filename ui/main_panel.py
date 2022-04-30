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

from ..lib import data


class RECORDER_PT_main_panel(bpy.types.Panel):
    """Main GUI component containing addon interface."""

    bl_idname = "RECORDER_PT_main_panel"
    bl_label = "Action Recorder Panel"
    bl_category = "Recorder"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        if not data.is_active():
            # no gpen selected for observation

            layout.label(text='Control trackers')
            layout.operator('action_recorder.start_track_active')
        else:
            # gpen has been selected

            gpen_observer = data.get_active_observer()
            selected_layer = gpen_observer.layers[
                gpen_observer.get_gpen().layer_index
            ]
            layer_records = gpen_observer.get_layer_records(
                selected_layer.info
            )

            layout.label(text=f'Tracking { gpen_observer.name }.')
            if gpen_observer.is_active():
                layout.operator('action_recorder.pause_tracking')
            else:
                layout.operator('action_recorder.resume_tracking')

            layout.operator('action_recorder.stop_track_active')

            layout.separator()
            layout.label(text="Layer select:")
            layout.template_list(
                "RECORDER_UL_layer_list",
                "layer_list",
                gpen_observer,
                "layers",
                gpen_observer.get_gpen(),
                "layer_index"
            )

            layout.separator()
            layout.label(text=f'Changes in layer { selected_layer.info }:')
            layout.template_list(
                "RECORDER_UL_change_list",
                "change_list",
                layer_records,
                "changes",
                layer_records,
                "change_index"
            )

            layout.separator()
            layout.label(text='Export')
            row = layout.row()
            row.operator('action_recorder.render')
            row.operator('action_recorder.render_settings', icon='SETTINGS')
