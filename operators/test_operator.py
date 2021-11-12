import bpy      # type: ignore


class TestOP(bpy.types.Operator):
    """Testing operator."""

    bl_idname = "action_recorder.test_op"
    bl_label = "Test OP"
    bl_description = "Perform test action"

    owner = object()

    def execute(self, context):
        print("Clicked")

        objects = bpy.context.editable_objects
    
        for o in objects:
            bpy.msgbus.subscribe_rna(
                key=o,
                owner=self.owner,
                args=(1, 2 ,3),
                notify=callback
            )
        
        return {'FINISHED'}

def callback(*args):
    print("change: ", args)
