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


from bpy.types import GreasePencil     # type: ignore

from .observers import GPenObserver

from typing import Union
from os import (
    mkdir,
    environ,
    path
)


class RenderSettings():
    """Class for storing render settings."""

    def __init__(self) -> None:
        self._render_path = path.join(environ['USERPROFILE'], 'Videos')
        self.use_viewport = True
        self.framerate = 24
        self.create_dir = ''

    @property
    def render_path(self):
        if self.create_dir:
            mkdir(path.join(self._render_path, self.create_dir))

        self.create_dir = ''
        return self._render_path

    @render_path.setter
    def render_path(self, value):
        self._render_path = value

    def valid(self) -> bool:
        """Check if the render settings are valid."""

        if path.isdir(self._render_path):
            valid_path = True
        else:
            # check if last directory can be created
            dirs = self._render_path.rsplit(path.sep, 1)
            if len(dirs) == 2:
                self._render_path = dirs[0]
                self.create_dir = dirs[1]
                valid_path = True
            else:
                valid_path = False

        valid_framerate = self.framerate > 0

        return valid_path and valid_framerate


# TODO: implement data storage
class ObserverDatabase():
    """Database class for storing tracked data."""

    def __init__(self) -> None:
        self.records: list[GPenObserver] = list()       # list of tracked gpens
        self.active_observer: Union[GPenObserver, None] = None
        self.render_settings = RenderSettings()
        self.load_data()

    def __del__(self):
        self.store_data()

    def is_active(self) -> bool:
        """Check if any gpen is being observed."""

        return bool(self.active_observer)

    def is_observed(self, gpen: GreasePencil) -> bool:
        """Check if concrete gpen is being observed"""

        if self.is_active():
            return self.active_observer.id == id(gpen)
        else:
            return False

    def get_active_layer_count(self) -> int:
        """Get number of layers of observed gpen."""

        if self.is_active():
            return self.active_observer.get_layer_count()
        else:
            return 0

    def get_active_observer(self) -> Union[GPenObserver, None]:
        """Get active observer or None if there is no active observer"""

        return self.active_observer

    def get_observer(self, gpen: GreasePencil) -> GPenObserver:
        """Get GPenObserver object for gpen.

            Returns observer for new and previously tracked gpens.
        """

        gpen_id = id(gpen)
        for observer in self.records:
            if observer.id == gpen_id:
                return observer

        observer = GPenObserver(gpen)
        self.records.append(observer)

        return observer

    def start_tracking(self, gpen: GreasePencil):
        """Start tracking Grease Pencil."""

        self.active_observer = self.get_observer(gpen)
        self.active_observer.set_active(True)

    def stop_tracking(self):
        """Stop tracking Grease Pencil."""

        self.active_observer.set_active(False)
        self.active_observer = None

    def store_data(self):
        """Store recorded data."""

    def load_data(self):
        """Load recorded data."""


# universal database instance
data = ObserverDatabase()
