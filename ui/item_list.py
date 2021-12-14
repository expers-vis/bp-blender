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

from bpy.types import UIList      # type: ignore


class RECORDER_UL_item_list(UIList):
    """Display items from list in the UI."""

    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):

        # data == scene
        # We could write some code to decide which icon to use here...
        default_icon = 'OBJECT_DATAMODE'
        gpens = data.observed_gpens

        if len(gpens) == 0:
            return

        # Make sure your code supports all 3 layout types
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(
                text=item.name,
                icon=default_icon
            )

        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon=default_icon)
