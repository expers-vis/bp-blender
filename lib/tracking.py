import bpy      # type: ignore

from .frame_observer import FrameObserver


tracked_pencils = list()        # list of ids of tracked objects


def tracked_len() -> int:
    """Get number of tracked objects."""

    return len(tracked_pencils)


def is_tracked(obj: object) -> bool:
    """Determine if object is tracked."""

    return id(obj) in tracked_pencils


def add_tracker(obj: object) -> bool:
    """Add object on the list of tracked objects.

        Returns:
            bool: True if objects is added, False if object is already present
    """

    if is_tracked(obj):
        return False

    tracked_pencils.append(id(obj))
    return True


def remove_tracker(obj: object) -> None:
    """Remove object from the list of tracked objects."""

    oid = id(obj)
    if oid in tracked_pencils:
        tracked_pencils.remove(oid)


def observe_frame(frame: bpy.types.GPencilFrame) -> FrameObserver:
    """Put observer onto the frame."""

    observer = FrameObserver(frame)

    bpy.types.GPencilFrame.stroke_count = bpy.props.IntProperty(
        name='stroke_count_' + str(id(frame)),
        update=observer.notify(),
        get=observer.get_stroke_count()
    )

    return observer
