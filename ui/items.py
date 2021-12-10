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

from bpy.types import PropertyGroup     # type: ignore
from bpy.props import (                 # type: ignore
    IntProperty,
    StringProperty,
    CollectionProperty
)


class LayerListItem(PropertyGroup):
    """List item representing layer of tracked Grease Pencil"""

    name: StringProperty(
        name='Name',                                                # noqa
        description='Name of this layer',                           # noqa
        default='Untitled',                                         # noqa
    )

    stroke_count: IntProperty(
        name='Number of strokes',                                   # noqa
        description='Number of strokes inside this layer',          # noqa
        default=0                                                   # noqa
    )


class GPenListItem(PropertyGroup):
    """List item representing tracked Grease Pencil."""

    name: StringProperty(
        name='Name',                                                # noqa
        description='Name of this Grease Pencil',                   # noqa
        default='Untitled',                                         # noqa
    )

    layer_list: CollectionProperty(
        name='Layers',                                              # noqa
        description='List of layers within this Grease Pencil',     # noqa
        type=LayerListItem                                          # noqa
    )
