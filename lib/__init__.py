import time


def get_timestamp():
    """Get string of current time in HH:MM:SS format."""

    t = time.localtime()
    return time.strftime('%H:%M:%S', t)


from .frame_observer import FrameObserver
from .tracking import (
    tracked_len,
    is_tracked,
    add_tracker,
    remove_tracker,
    observe_frame
)
