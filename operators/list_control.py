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

from bpy.types import Operator      # type: ignore

from ..lib import (
    tracked_gpen_len,
    remove_gpen_tracker
)


class RECORDER_OT_list_remove(Operator):
    bl_idname = "action_recorder.list_remove_selected"
    bl_label = "Remove selected item"
    bl_description = "Remove selected Grease Pencil from trackers"

    @classmethod
    def poll(cls, context):
        return tracked_gpen_len() > 0

    def execute(self, context):
        index = context.scene.observed_gpens_index
        gpen_list = context.scene.observed_gpens

        gpen_item = gpen_list[index]
        remove_gpen_tracker(gpen_item.gpen)
        gpen_list.remove(index)

        index = min(max(0, index - 1), len(gpen_list) - 1)      # reset index

        return {"FINISHED"}
