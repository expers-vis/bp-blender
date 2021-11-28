import bpy      # type: ignore
from . import get_timestamp


class FrameObserver(object):
    def __init__(self, observee: bpy.types.GPencilFrame) -> None:
        self.frame = observee
        self.strokes = observee.strokes
        self.last_count = self.strokes.__len__()

    def get_frame(self) -> bpy.types.GPencilFrame:
        return self.frame

    def get_frame_id(self) -> int:
        return id(self.frame)

    def get_strokes(self) -> bpy.types.bpy_prop_collection:
        return self.strokes

    def get_stroke_count(self) -> int:
        return self.strokes.__len__()

    def on_add(self) -> None:
        print(get_timestamp() + ": stroke added.")

    def on_remove(self) -> None:
        print(get_timestamp() + ": stroke removed.")

    def notify(self) -> None:
        new_count = self.get_stroke_count()

        if(self.last_count < new_count):
            self.on_add()
        elif(self.last_count > new_count):
            self.on_remove()
        self.last_count = new_count
