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

from .gpen_observer import GPenObserver
from .utils import log

from typing import Union


# TODO: implement data storage
class ObserverDatabase():
    """Database class for storing tracked data."""

    def __init__(self) -> None:
        self.records: list[GPenObserver] = list()       # list of tracked gpens
        self.active_observer: Union[GPenObserver, None] = None
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

    def stop_tracking(self):
        """Stop tracking Grease Pencil."""

        self.active_observer = None

    def store_data(self):
        """Store recorded data."""

    def load_data(self):
        """Load recorded data."""


# universal database instance
data = ObserverDatabase()
