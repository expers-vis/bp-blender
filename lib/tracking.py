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


from bpy.types import (                 # type: ignore
    GPencilFrame
)
from bpy.props import IntProperty       # type: ignore

from .layer_observer import LayerObserver


def observe_frame(frame: GPencilFrame) -> LayerObserver:
    """Put observer onto the frame."""

    observer = LayerObserver(frame)

    GPencilFrame.stroke_count = IntProperty(
        name='stroke_count_' + str(id(frame)),
        update=observer.notify(),
        get=observer.get_stroke_count()
    )

    return observer
