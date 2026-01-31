# -*- coding: utf-8 -*-
"""Background repeat loop: press selected keys at interval until stop_event is set."""
import threading

from layout import key_id_to_press


def run_repeat_loop(controller, selected_keys_getter, interval_sec: float, stop_event: threading.Event) -> None:
    """Run in a thread. Press each selected key in order every interval_sec until stop_event is set."""
    while not stop_event.is_set():
        for key_id in list(selected_keys_getter()):
            if stop_event.is_set():
                break
            try:
                k = key_id_to_press(key_id)
                controller.press(k)
                controller.release(k)
            except Exception:
                pass
        stop_event.wait(timeout=interval_sec)
