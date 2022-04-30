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

from bpy.ops import render as render_call       # type: ignore
from bpy.props import (                         # type: ignore
    BoolProperty,
    IntProperty,
    StringProperty
)
from bpy.types import (                         # type: ignore
    Operator
)

from ..lib import data

from os import (
    environ,
    path
)


class RECORDER_OT_render(Operator):
    """Start rendering captured sequence."""

    bl_idname = "action_recorder.render"
    bl_label = "Render"
    bl_description = "Render the captured sequence"
    bl_options = {'BLOCKING'}

    @classmethod
    def poll(cls, context) -> bool:
        """Check if operator can be executed."""

        return data.is_active()

    def invoke(self, context, event):
        """Invoke the dialog window."""

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context) -> set:
        """Draw operator dialog."""

        self.layout.label(
            text='Please do not modify the scene until rendering is finished.'
        )

    def execute(self, context) -> set:
        """Execute the operator."""

        if not data.render_settings.valid():
            self.report(
                {'ERROR_INVALID_INPUT'},
                'Invalid render settings.'
            )
            return {'CANCELLED'}

        last_frame = context.scene.frame_current
        context.scene.frame_end = data.get_active_observer().frame_count
        fill_len = len(str(data.get_active_observer().frame_count))
        base_dir = data.render_settings.render_path

        for idx in range(0, data.get_active_observer().frame_count + 1):
            # redundant variable to save line length
            img_name = f'{path.sep}capture{str(idx).zfill(fill_len)}'
            context.scene.render.filepath = base_dir + img_name
            context.scene.frame_set(idx)

            render_call.render(
                write_still=True,
                use_viewport=data.render_settings.use_viewport
            )

        context.scene.frame_set(last_frame)
        self.report(
            {'INFO'},
            'Render has finished.'
        )

        return {'FINISHED'}


class RECORDER_OT_render_settings(Operator):
    """Get the settings for rendering."""

    bl_idname = "action_recorder.render_settings"
    bl_label = ""
    bl_description = "Edit render settings"

    path: StringProperty(
        name='Export path:',
        description='Path to export rendered images to.',
        default=path.join(environ['USERPROFILE'], 'Videos')
    )
    framerate: IntProperty(
        name='Framerate',
        description='Framerate for rendered animation.',
        default=1
    )
    viewport: BoolProperty(
        name='Use viewport',
        description=('Set whether animation should be '
                     'rendered using a viewport.'),
        default=True
    )

    def invoke(self, context, event):
        """Invoke the dialog window."""

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        """Execute the operator."""

        data.render_settings.render_path = self.path
        data.render_settings.framerate = self.framerate
        data.render_settings.use_viewport = self.viewport

        return {'INTERFACE'}
