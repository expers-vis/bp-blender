import bpy      # type: ignore


class RECORDER_PT_main_panel(bpy.types.Panel):
    """Main panel class containg Addon GUI."""

    bl_idname = "RECORDER_PT_main_panel"
    bl_label = "Action Recorder Panel"
    bl_category = "Recorder"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        layout.label(text='Control trackers')

        row1 = layout.row()
        # row1.label(icon= 'BLENDER')
        row1.operator(
            'action_recorder.start_track_active',
            text='Track selected GPencils'
        )

        row2 = layout.row()
        row2.operator(
            'action_recorder.start_track_name',
            text='Track GPencil by name'
        )

        row3 = layout.row()
        row3.operator(
            'action_recorder.stop_track_active',
            text='Stop tracking selected GPencils'
        )
        
        row4 = layout.row()
        row4.operator(
            'action_recorder.stop_track_name',
            text='Stop tracking GPencil by name'
        )
