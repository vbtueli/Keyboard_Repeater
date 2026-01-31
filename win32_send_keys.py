# -*- coding: utf-8 -*-
"""Send keystrokes to a specific window (hwnd) on Windows via PostMessage. Used when target app is set."""
import sys

if sys.platform != "win32":
    raise RuntimeError("win32_send_keys is Windows-only")

# Windows virtual key codes and OEM (VK_OEM_* for symbols)
VK_BACK, VK_TAB, VK_RETURN, VK_ESCAPE = 0x08, 0x09, 0x0D, 0x1B
VK_SHIFT, VK_CONTROL, VK_MENU, VK_CAPITAL = 0x10, 0x11, 0x12, 0x14
VK_SPACE = 0x20
VK_PRIOR, VK_NEXT, VK_END, VK_HOME = 0x21, 0x22, 0x23, 0x24
VK_LEFT, VK_UP, VK_RIGHT, VK_DOWN = 0x25, 0x26, 0x27, 0x28
VK_INSERT, VK_DELETE = 0x2D, 0x2E
VK_0, VK_9 = 0x30, 0x39
VK_A, VK_Z = 0x41, 0x5A
VK_LWIN, VK_RWIN = 0x5B, 0x5C
VK_NUMPAD0, VK_NUMPAD1, VK_NUMPAD2, VK_NUMPAD3, VK_NUMPAD4 = 0x60, 0x61, 0x62, 0x63, 0x64
VK_NUMPAD5, VK_NUMPAD6, VK_NUMPAD7, VK_NUMPAD8, VK_NUMPAD9 = 0x65, 0x66, 0x67, 0x68, 0x69
VK_MULTIPLY, VK_ADD, VK_SUBTRACT, VK_DECIMAL, VK_DIVIDE = 0x6A, 0x6B, 0x6D, 0x6E, 0x6F
VK_F1, VK_F12 = 0x70, 0x7B
VK_NUMLOCK = 0x90
VK_OEM_1, VK_OEM_PLUS, VK_OEM_COMMA, VK_OEM_MINUS = 0xBA, 0xBB, 0xBC, 0xBD
VK_OEM_PERIOD, VK_OEM_2, VK_OEM_3, VK_OEM_4, VK_OEM_5, VK_OEM_6, VK_OEM_7 = 0xBE, 0xBF, 0xC0, 0xDB, 0xDC, 0xDD, 0xDE

# key_id -> (vk_code, extended_flag). extended=1 for right modifiers, numpad enter, numpad /, etc.
KEY_ID_TO_VK = {
    "esc": (VK_ESCAPE, 0), "tab": (VK_TAB, 0), "caps_lock": (VK_CAPITAL, 0),
    "shift": (VK_SHIFT, 0), "shift_r": (VK_SHIFT, 1),
    "ctrl": (VK_CONTROL, 0), "ctrl_r": (VK_CONTROL, 1),
    "alt": (VK_MENU, 0), "alt_r": (VK_MENU, 1),
    "cmd": (VK_LWIN, 0), "cmd_r": (VK_RWIN, 1),
    "space": (VK_SPACE, 0), "enter": (VK_RETURN, 0), "backspace": (VK_BACK, 0),
    "f1": (VK_F1, 0), "f2": (VK_F1 + 1, 0), "f3": (VK_F1 + 2, 0), "f4": (VK_F1 + 3, 0),
    "f5": (VK_F1 + 4, 0), "f6": (VK_F1 + 5, 0), "f7": (VK_F1 + 6, 0), "f8": (VK_F1 + 7, 0),
    "f9": (VK_F1 + 8, 0), "f10": (VK_F1 + 9, 0), "f11": (VK_F1 + 10, 0), "f12": (VK_F1 + 11, 0),
    "insert": (VK_INSERT, 0), "delete": (VK_DELETE, 0),
    "home": (VK_HOME, 0), "end": (VK_END, 0),
    "page_up": (VK_PRIOR, 0), "page_down": (VK_NEXT, 0),
    "up": (VK_UP, 0), "down": (VK_DOWN, 0), "left": (VK_LEFT, 0), "right": (VK_RIGHT, 0),
    "num_lock": (VK_NUMLOCK, 0),
    "numpad_0": (VK_NUMPAD0, 0), "numpad_1": (VK_NUMPAD1, 0), "numpad_2": (VK_NUMPAD2, 0),
    "numpad_3": (VK_NUMPAD3, 0), "numpad_4": (VK_NUMPAD4, 0), "numpad_5": (VK_NUMPAD5, 0),
    "numpad_6": (VK_NUMPAD6, 0), "numpad_7": (VK_NUMPAD7, 0), "numpad_8": (VK_NUMPAD8, 0),
    "numpad_9": (VK_NUMPAD9, 0),
    "numpad_decimal": (VK_DECIMAL, 0), "numpad_add": (VK_ADD, 0),
    "numpad_subtract": (VK_SUBTRACT, 0), "numpad_multiply": (VK_MULTIPLY, 0),
    "numpad_divide": (VK_DIVIDE, 1), "numpad_enter": (VK_RETURN, 1),
    "1": (0x31, 0), "2": (0x32, 0), "3": (0x33, 0), "4": (0x34, 0), "5": (0x35, 0),
    "6": (0x36, 0), "7": (0x37, 0), "8": (0x38, 0), "9": (0x39, 0), "0": (0x30, 0),
    "-": (VK_OEM_MINUS, 0), "=": (VK_OEM_PLUS, 0),
    "q": (VK_A, 0), "w": (VK_A + 1, 0), "e": (VK_A + 2, 0), "r": (VK_A + 3, 0),
    "t": (VK_A + 4, 0), "y": (VK_A + 5, 0), "u": (VK_A + 6, 0), "i": (VK_A + 7, 0),
    "o": (VK_A + 8, 0), "p": (VK_A + 9, 0), "[": (VK_OEM_4, 0), "]": (VK_OEM_6, 0), "\\": (VK_OEM_5, 0),
    "a": (VK_A, 0), "s": (VK_A + 1, 0), "d": (VK_A + 2, 0), "f": (VK_A + 3, 0),
    "g": (VK_A + 4, 0), "h": (VK_A + 5, 0), "j": (VK_A + 6, 0), "k": (VK_A + 7, 0),
    "l": (VK_A + 8, 0), ";": (VK_OEM_1, 0), "'": (VK_OEM_7, 0),
    "z": (VK_A + 25, 0), "x": (VK_A + 26, 0), "c": (VK_A + 27, 0), "v": (VK_A + 28, 0),
    "b": (VK_A + 29, 0), "n": (VK_A + 30, 0), "m": (VK_A + 31, 0),
    ",": (VK_OEM_COMMA, 0), ".": (VK_OEM_PERIOD, 0), "/": (VK_OEM_2, 0),
}

MAPVK_VK_TO_VSC = 0
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101


def key_id_to_vk(key_id: str) -> tuple[int, int] | None:
    """Return (vk_code, extended_flag) for key_id, or None if unknown."""
    return KEY_ID_TO_VK.get(key_id.lower() if isinstance(key_id, str) else key_id)


def send_key_to_hwnd(hwnd: int, key_id: str) -> bool:
    """Send key down and key up to the given window via PostMessage. Returns True if sent."""
    vk_info = key_id_to_vk(key_id)
    if vk_info is None:
        return False
    vk, extended = vk_info
    from ctypes import windll
    user32 = windll.user32
    scan = user32.MapVirtualKeyW(vk, MAPVK_VK_TO_VSC)
    # lParam: repeat 1, scan in bits 16-23, extended in bit 24
    lparam_down = 1 | (scan << 16) | ((extended & 1) << 24)
    lparam_up = (1 | (scan << 16) | ((extended & 1) << 24)) | (1 << 31)  # bit 31 = transition (key up)
    user32.PostMessageW(hwnd, WM_KEYDOWN, vk, lparam_down)
    user32.PostMessageW(hwnd, WM_KEYUP, vk, lparam_up)
    return True
