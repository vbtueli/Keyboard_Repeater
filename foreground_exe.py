# -*- coding: utf-8 -*-
"""Get the executable path of the current foreground window (for target-app filtering)."""
import os
import sys


def get_foreground_process_exe() -> str | None:
    """
    Return the full path of the foreground window's process executable, or None on error/unsupported.
    Supported on Windows; returns None on Linux/macOS (target-app option then has no effect).
    """
    if sys.platform == "win32":
        return _get_foreground_exe_win32()
    return None


def _get_foreground_exe_win32() -> str | None:
    from ctypes import byref, c_ulong, create_unicode_buffer, windll
    from ctypes.wintypes import DWORD, HANDLE

    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    user32 = windll.user32
    kernel32 = windll.kernel32

    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return None
    pid = DWORD()
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    if not pid.value:
        return None
    h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
    if not h:
        return None
    try:
        size = DWORD(260)
        buf = create_unicode_buffer(size.value)
        if kernel32.QueryFullProcessImageNameW(HANDLE(h), 0, buf, byref(size)):
            return buf.value
    finally:
        kernel32.CloseHandle(HANDLE(h))
    return None


def normalize_exe_path(path: str) -> str:
    """Normalize an executable path for comparison (case and separators)."""
    if not path:
        return ""
    p = os.path.normpath(path.strip())
    if sys.platform == "win32":
        p = os.path.normcase(p)
    return p


def get_hwnd_for_exe(exe_path: str) -> int | None:
    """
    Return a top-level window handle (hwnd) belonging to the process with the given exe path.
    Returns None if not found or on non-Windows. Used to send keys to that window without focusing it.
    """
    if sys.platform != "win32":
        return None
    return _get_hwnd_for_exe_win32(normalize_exe_path(exe_path))


def _get_hwnd_for_exe_win32(target_norm: str) -> int | None:
    from ctypes import byref, c_bool, create_unicode_buffer, windll, WINFUNCTYPE
    from ctypes.wintypes import DWORD, HANDLE, HWND, LPARAM

    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    user32 = windll.user32
    kernel32 = windll.kernel32

    result = [None]  # mutable to store hwnd in callback

    def enum_callback(hwnd, _lparam):
        try:
            if not user32.IsWindowVisible(hwnd):
                return True  # continue
            pid = DWORD()
            user32.GetWindowThreadProcessId(HWND(hwnd), byref(pid))
            if not pid.value:
                return True
            h = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid.value)
            if not h:
                return True
            try:
                size = DWORD(260)
                buf = create_unicode_buffer(size.value)
                if kernel32.QueryFullProcessImageNameW(HANDLE(h), 0, buf, byref(size)):
                    path_norm = normalize_exe_path(buf.value)
                    if path_norm == target_norm:
                        result[0] = hwnd
                        return False  # stop
            finally:
                kernel32.CloseHandle(HANDLE(h))
        except Exception:
            pass
        return True  # continue

    WNDENUMPROC = WINFUNCTYPE(c_bool, HWND, LPARAM)
    user32.EnumWindows(WNDENUMPROC(enum_callback), 0)
    return result[0]
