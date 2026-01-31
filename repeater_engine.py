# -*- coding: utf-8 -*-
"""Background repeat loop: press selected keys at interval until stop_event is set."""
import sys
import threading

from foreground_exe import get_hwnd_for_exe
from layout import key_id_to_press

if sys.platform == "win32":
    from win32_send_keys import send_key_to_hwnd as _send_key_to_hwnd
else:
    _send_key_to_hwnd = None


def run_repeat_loop(
    controller,
    selected_keys_getter,
    interval_sec: float,
    stop_event: threading.Event,
    target_exe_getter=None,
    log_func=None,
) -> None:
    """
    Run in a thread. Press each selected key in order every interval_sec until stop_event is set.
    If target_exe_getter returns a non-empty path (Windows only), keys are sent directly to that
    app's window via PostMessage. Otherwise keys are sent to the foreground window.
    If log_func is set, it will be called with log messages (str) for debugging.
    """
    def _log(msg):
        if log_func:
            try:
                log_func(msg)
            except Exception:
                pass

    try:
        use_target_hwnd = sys.platform == "win32"
        keys_list = list(selected_keys_getter())
        _log(f"Repeat started: interval_sec={interval_sec}, platform={sys.platform}, use_target_hwnd={use_target_hwnd}, selected_keys={keys_list}")

        loop_count = 0
        while not stop_event.is_set():
            target_exe = (target_exe_getter() or "").strip() if target_exe_getter else ""
            hwnd = None
            if use_target_hwnd and target_exe:
                try:
                    hwnd = get_hwnd_for_exe(target_exe)
                except Exception as e:
                    _log(f"get_hwnd_for_exe error: {e}")
                if not hwnd:
                    if loop_count % 10 == 0:
                        _log(f"target_exe='{target_exe}' -> hwnd not found (no visible window?), skipping this round")
                    stop_event.wait(timeout=interval_sec)
                    loop_count += 1
                    continue
                if loop_count % 10 == 0:
                    _log(f"target_exe='{target_exe}' -> hwnd=0x{hwnd:X}, sending via PostMessage")
            else:
                if loop_count % 10 == 0:
                    _log(f"mode=foreground (target_exe empty or non-Windows), sending via pynput")
            for key_id in list(selected_keys_getter()):
                if stop_event.is_set():
                    break
                try:
                    if hwnd is not None and _send_key_to_hwnd:
                        ok = _send_key_to_hwnd(hwnd, key_id)
                        if log_func and not ok:
                            _log(f"send_key_to_hwnd failed for key_id='{key_id}'")
                    else:
                        k = key_id_to_press(key_id)
                        controller.press(k)
                        controller.release(k)
                except Exception as e:
                    _log(f"Exception sending key '{key_id}': {e}")
            stop_event.wait(timeout=interval_sec)
            loop_count += 1
            _log(f"round {loop_count}")
        _log("Repeat stopped")
    except Exception as e:
        _log(f"Repeat loop error (e.g. app closed): {e}")
