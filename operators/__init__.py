import bpy      # type: ignore

from .trackers import (
    RECORDER_OT_start_track_active,
    RECORDER_OT_stop_track_active,
    RECORDER_OT_start_track_name,
    RECORDER_OT_stop_track_name
)

classes = [
    RECORDER_OT_start_track_active,
    RECORDER_OT_stop_track_active,
    RECORDER_OT_start_track_name,
    RECORDER_OT_stop_track_name,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
