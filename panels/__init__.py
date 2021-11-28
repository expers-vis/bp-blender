from .main_panel import RECORDER_PT_main_panel

classes = [
    RECORDER_PT_main_panel,
]


def register():
    import bpy      # type: ignore

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    import bpy      # type: ignore

    for cls in classes:
        bpy.utils.unregister_class(cls)
