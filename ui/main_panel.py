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
    """Main panel class containg Addon GUI."""

    bl_idname = "RECORDER_PT_main_panel"
    bl_label = "Action Recorder Panel"
    bl_category = "Recorder"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        if not data.is_observing:
            # no gpen selected for observation

            layout.label(text='Control trackers')
            layout.operator(
                'action_recorder.start_track_active',
                text='Track selected GPencil'
            )
        else:
            # gpen has been selected

            observer = data.observed_gpen

            layout.label(text=f'Tracking { observer.name }.')

            layout.operator(
                'action_recorder.stop_track_active',
                text='Stop tracking'
            )

            layout.separator()
            layout.label(text="Layer select:")
            layout.template_list(
                "RECORDER_UL_layer_list",
                "layer_list",
                observer,
                "layers",
                observer.gpen,
                "layer_index"
            )

            layout.separator()
            layout.label(text='Changes:')
            # layout.template_list(
            #     "RECORDER_UL_change_list",
            #     "change_list",
            #     scene,
            #     "observed_gpens",
            #     scene,
            #     "observed_gpens_index"
            # )
