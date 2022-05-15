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
from pathlib import Path


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

        context.scene.frame_end = data.get_active_observer().frame_count
        base_dir_path = data.render_settings.render_path
        render_dir_path = f'{base_dir_path}{path.sep}render'

        # render animation images
        context.scene.render.filepath = render_dir_path + path.sep + 'capture'
        render_call.render(
            animation=True,
            use_viewport=data.render_settings.use_viewport
        )

        # compile images into animation
        render_dir = Path(render_dir_path)
        images = sorted(list(render_dir.glob('*.png')))
        context.scene.sequence_editor_clear()
        editor = context.scene.sequence_editor_create()
        sequence = editor.sequences

        first = images.pop(0)
        image_strip = sequence.new_image(
            name=first.name,
            filepath=str(first),
            frame_start=1,
            channel=1
        )

        while images:
            image_strip.elements.append(images.pop(0).name)

        image_strip.frame_final_duration = data.get_active_observer().frame_count
        image_strip.update()
        context.scene.render.filepath = base_dir_path + path.sep + 'animation'
        context.scene.render.image_settings.file_format = 'AVI_JPEG'
        context.scene.render.fps = data.render_settings.framerate
        render_call.render(animation=True)

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
    fps: IntProperty(
        name='Framerate',
        description='number of frames per second in animation.',
        default=24
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
        data.render_settings.framerate = self.fps
        data.render_settings.use_viewport = self.viewport

        return {'INTERFACE'}
