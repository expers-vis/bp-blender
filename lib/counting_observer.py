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


from ..lib import get_timestamp


class Observer():
    """Observer class used to observe changes in object.

        Change si detected when number of elements in selected
        attribute changes.
        Call method notify to evaluate change.
        Methods on_add and on_remove are called for their respective change.
    """

    def __init__(self, observee, observed_attr: str) -> None:
        self.observee = observee
        self.attribute = getattr(observee, observed_attr)
        self.last_count = self.attribute.__len__()

        # TODO: remove
        self.str_attr = observed_attr

    def get_observee(self):
        return self.observee

    def get_attribute_count(self) -> int:
        return self.attribute.__len__()

    def on_add(self) -> None:
        print(f"{ get_timestamp() }: { self.str_attr } added.")

    def on_remove(self) -> None:
        print(f"{ get_timestamp() }: { self.str_attr } added.")

    def notify(self) -> None:
        new_count = self.get_attribute_count()

        if(self.last_count < new_count):
            self.on_add()
        elif(self.last_count > new_count):
            self.on_remove()
        self.last_count = new_count
