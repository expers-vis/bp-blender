import bpy      # type: ignore


class MainPanel(bpy.types.Panel):
    """Main panel class containg Addon GUI."""
    
    bl_idname = "PT_main_panel"
    bl_label = "Action Recorder Panel"
    bl_category = "Recorder"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.label(text= 'Sample text', icon= 'BLENDER')
