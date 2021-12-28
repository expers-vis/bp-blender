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


import logging
import time


logger = logging.getLogger(__name__ + '.recorder_addon')
streams = ('critical', 'error', 'warning', 'info', 'debug')


def get_timestamp():
    """Get string of current time in HH:MM:SS format."""

    t = time.localtime()
    return time.strftime('%H:%M:%S', t)


def log(msg: str, stream: str = 'info'):
    """Send a message onto the logging stream

    Args:
        msg (str): message string
        stream (str): stream type from (critical, error, warning, info, debug)
    """

    stream = stream.lower()
    if stream not in streams:
        return

    send_msg = getattr(logger, stream)

    send_msg(msg)
