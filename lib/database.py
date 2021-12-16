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


# TODO: implement data storage
class ObserverDatabase():
    """Database class for storing tracked data."""

    def __init__(self) -> None:
        self.records: list[GPenObserver] = list()       # list of tracked gpens
        self.load_data()

    def __del__(self):
        self.store_data()

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

    def store_data(self):
        """Store recorded data."""

    def load_data(self):
        """Load recorded data."""


class DataGroup():
    """Property group containing addon data."""

    def __init__(self) -> None:
        self.__database__ = ObserverDatabase()
        self.__observed_gpen__ = None
        self.is_observing = False

    @property
    def database(self) -> ObserverDatabase:
        return self.__database__

    @property
    def observed_gpen(self) -> GPenObserver:
        return self.__observed_gpen__

    @observed_gpen.setter
    def observed_gpen(self, value: GPenObserver):
        self.__observed_gpen__ = value


# universal data group instance
data = DataGroup()
