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


from bpy.types import GPencilLayer      # type: ignore

from .utils import get_timestamp


class LayerObserver(object):
    """Observer class used to observe changes in GPencilLayer object."""

    def __init__(self, observee: GPencilLayer) -> None:
        self.id = id(observee)
        self.name = observee.info
        self.frame = observee
        self.strokes = observee.strokes
        self.last_count = self.strokes.__len__()

    def get_frame(self) -> GPencilLayer:
        return self.frame

    def get_frame_id(self) -> int:
        return id(self.frame)

    def get_stroke_count(self) -> int:
        return self.strokes.__len__()

    def on_add(self) -> None:
        print(get_timestamp() + ": stroke added.")

    def on_remove(self) -> None:
        print(get_timestamp() + ": stroke removed.")

    def notify(self) -> None:
        new_count = self.get_stroke_count()

        if(self.last_count < new_count):
            self.on_add()
        elif(self.last_count > new_count):
            self.on_remove()
        self.last_count = new_count
