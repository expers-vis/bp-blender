# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from ..lib import (
    register_classes,
    unregister_classes
)

from .io import (
    RECORDER_OT_render,
    RECORDER_OT_render_settings
)

from .tracking import (
    RECORDER_OT_start_track_active,
    RECORDER_OT_stop_track_active,
    RECORDER_OT_pause_tracking,
    RECORDER_OT_resume_tracking
)


classes = [
    RECORDER_OT_render,
    RECORDER_OT_render_settings,
    RECORDER_OT_start_track_active,
    RECORDER_OT_stop_track_active,
    RECORDER_OT_pause_tracking,
    RECORDER_OT_resume_tracking,
]


def register():
    register_classes(classes)


def unregister():
    unregister_classes(classes)
