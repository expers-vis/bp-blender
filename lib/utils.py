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

import bpy      # type: ignore

import logging
import time


logging_enabled = False

if logging_enabled:
    try:
        logging.basicConfig(
            filename='blender_recorder.log',
            level=logging.DEBUG
        )
        location = logging.getLoggerClass().root.handlers[0].baseFilename
        print("Action Recorder: logging enabled")
        print(f"Log file: {location}")
    except PermissionError:
        logging_enabled = False
        print('Action Recorder: logging disabled')

levels = ('critical', 'error', 'warning', 'info', 'debug')


def register_classes(class_list: list):
    """Register blender classes from a list"""

    for cls in class_list:
        bpy.utils.register_class(cls)


def unregister_classes(class_list: list):
    """Unregister blender classes from a list"""

    del_list = class_list.copy()
    while len(del_list) > 0:
        try:
            cls = del_list.pop()
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


def get_timestamp():
    """Get string of current time in HH:MM:SS format."""

    t = time.localtime()
    return time.strftime('%H:%M:%S', t)


def log(msg: str, level: str = 'info'):
    """Send a message onto the logging stream

    Args:
        msg (str): message string
        stream (str): logging level from (critical, error, warning,
        info, debug)
    """

    level = level.lower()
    if (level not in levels) or (not logging_enabled):
        return

    send_msg = getattr(logging, level)

    send_msg(msg)
