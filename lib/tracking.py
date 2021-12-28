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

from .utils import log
from . import database


# active observation functions
def observe_layers() -> None:
    """Actively observe changes to the layer.

        This function will be called periodically by blender and will report
        changes to the active observer.
    """

    observer = database.data.get_active_observer()
    new_count = observer.get_layer_count()

    if(observer.last_count < new_count):
        observer.on_add()
    elif(observer.last_count > new_count):
        observer.on_remove()
    observer.last_count = new_count

    return observer.interval


def observe_strokes() -> None:
    """Actively observe changes to the strokes inside the layer.

        This function will be called periodically by blender and will report
        changes to the active observer.
    """


# passive observation functions
def get_active_layer_count(self) -> int:
    """Retrieve number of layers in observed gpen.

        This function will become method of the GreasePencil class called
        to get the number of layers.
    """

    print('getting layer count')
    log('getting layer count')

    return len(self.layers)


def notify_layer_change(self, context):
    """Function handling layer change.

        This function will become method of the GreasePencil class called
        when number of layers have changed.
    """

    print('notifying ' + str(self))
    log('notifying ' + str(self), 'debug')

    if database.data.is_observed(self):
        database.data.get_observer(self).notify()
