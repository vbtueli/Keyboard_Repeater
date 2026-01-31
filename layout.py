# -*- coding: utf-8 -*-
"""Keyboard layout definitions and key_id -> pynput mapping. Cross-platform: Windows, Linux, macOS."""
import sys
from pynput.keyboard import Key, KeyCode

_IS_WINDOWS = sys.platform == "win32"

# Windows VK codes for numpad (used only on Windows)
if _IS_WINDOWS:
    VK_NUMLOCK = 0x90
    VK_NUMPAD0, VK_NUMPAD1, VK_NUMPAD2, VK_NUMPAD3, VK_NUMPAD4 = 0x60, 0x61, 0x62, 0x63, 0x64
    VK_NUMPAD5, VK_NUMPAD6, VK_NUMPAD7, VK_NUMPAD8, VK_NUMPAD9 = 0x65, 0x66, 0x67, 0x68, 0x69
    VK_MULTIPLY, VK_ADD, VK_SUBTRACT, VK_DECIMAL, VK_DIVIDE = 0x6A, 0x6B, 0x6D, 0x6E, 0x6F

# Main keyboard: each row is (indent_px, [keys]). Key is (label, key_id) or (label, key_id, width_chars).
MAIN_LAYOUT = [
    (0, [("F1", "f1"), ("F2", "f2"), ("F3", "f3"), ("F4", "f4"), ("F5", "f5"), ("F6", "f6"),
         ("F7", "f7"), ("F8", "f8"), ("F9", "f9"), ("F10", "f10"), ("F11", "f11"), ("F12", "f12")]),
    (0, [("Esc", "esc"), ("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),
         ("6", "6"), ("7", "7"), ("8", "8"), ("9", "9"), ("0", "0"), ("-", "-"), ("=", "="), ("Backspace", "backspace", 10)]),
    (18, [("Tab", "tab", 7), ("Q", "q"), ("W", "w"), ("E", "e"), ("R", "r"), ("T", "t"),
          ("Y", "y"), ("U", "u"), ("I", "i"), ("O", "o"), ("P", "p"), ("[", "["), ("]", "]"), ("\\", "\\", 6)]),
    (36, [("Caps", "caps_lock", 8), ("A", "a"), ("S", "s"), ("D", "d"), ("F", "f"), ("G", "g"),
          ("H", "h"), ("J", "j"), ("K", "k"), ("L", "l"), (";", ";"), ("'", "'"), ("Enter", "enter", 8)]),
    (54, [("Shift", "shift", 10), ("Z", "z"), ("X", "x"), ("C", "c"), ("V", "v"), ("B", "b"),
          ("N", "n"), ("M", "m"), (",", ","), (".", "."), ("/", "/"), ("Shift", "shift_r", 10)]),
    (72, [("Ctrl", "ctrl", 6), ("Win", "cmd"), ("Alt", "alt", 6), ("Space", "space", 22), ("Alt", "alt_r", 6), ("Win", "cmd_r"), ("Ctrl", "ctrl_r", 6)]),
    (0, [("Insert", "insert"), ("Delete", "delete"), ("Home", "home"), ("End", "end"),
         ("PgUp", "page_up"), ("PgDn", "page_down"), ("↑", "up"), ("↓", "down"), ("←", "left"), ("→", "right")]),
]

NUMPAD_LAYOUT = [
    [("NumLock", "num_lock", 8), ("/", "numpad_divide"), ("*", "numpad_multiply"), ("-", "numpad_subtract")],
    [("7", "numpad_7"), ("8", "numpad_8"), ("9", "numpad_9"), ("+", "numpad_add", 5)],
    [("4", "numpad_4"), ("5", "numpad_5"), ("6", "numpad_6")],
    [("1", "numpad_1"), ("2", "numpad_2"), ("3", "numpad_3"), ("Enter", "numpad_enter", 6)],
    [("0", "numpad_0", 10), (".", "numpad_decimal")],
]

def _base_key_map():
    """Keys common to all platforms."""
    return {
        "esc": Key.esc, "tab": Key.tab, "caps_lock": Key.caps_lock, "shift": Key.shift, "shift_r": Key.shift_r,
        "ctrl": Key.ctrl, "ctrl_r": Key.ctrl_r, "alt": Key.alt, "alt_r": Key.alt_r,
        "cmd": Key.cmd, "cmd_r": Key.cmd_r,
        "space": Key.space, "enter": Key.enter, "backspace": Key.backspace,
        "f1": Key.f1, "f2": Key.f2, "f3": Key.f3, "f4": Key.f4, "f5": Key.f5, "f6": Key.f6,
        "f7": Key.f7, "f8": Key.f8, "f9": Key.f9, "f10": Key.f10, "f11": Key.f11, "f12": Key.f12,
        "insert": Key.insert, "delete": Key.delete, "home": Key.home, "end": Key.end,
        "page_up": Key.page_up, "page_down": Key.page_down,
        "up": Key.up, "down": Key.down, "left": Key.left, "right": Key.right,
    }


def _numpad_key_map_windows():
    """Numpad keys using Windows VK codes."""
    return {
        "num_lock": KeyCode.from_vk(VK_NUMLOCK),
        "numpad_0": KeyCode.from_vk(VK_NUMPAD0), "numpad_1": KeyCode.from_vk(VK_NUMPAD1),
        "numpad_2": KeyCode.from_vk(VK_NUMPAD2), "numpad_3": KeyCode.from_vk(VK_NUMPAD3),
        "numpad_4": KeyCode.from_vk(VK_NUMPAD4), "numpad_5": KeyCode.from_vk(VK_NUMPAD5),
        "numpad_6": KeyCode.from_vk(VK_NUMPAD6), "numpad_7": KeyCode.from_vk(VK_NUMPAD7),
        "numpad_8": KeyCode.from_vk(VK_NUMPAD8), "numpad_9": KeyCode.from_vk(VK_NUMPAD9),
        "numpad_decimal": KeyCode.from_vk(VK_DECIMAL), "numpad_add": KeyCode.from_vk(VK_ADD),
        "numpad_subtract": KeyCode.from_vk(VK_SUBTRACT), "numpad_multiply": KeyCode.from_vk(VK_MULTIPLY),
        "numpad_divide": KeyCode.from_vk(VK_DIVIDE), "numpad_enter": Key.enter,
    }


def _numpad_key_map_linux_or_mac():
    """Numpad keys on Linux/macOS: use char/Key fallback (platform keycodes vary)."""
    return {
        "num_lock": getattr(Key, "num_lock", Key.enter),
        "numpad_0": "0", "numpad_1": "1", "numpad_2": "2", "numpad_3": "3", "numpad_4": "4",
        "numpad_5": "5", "numpad_6": "6", "numpad_7": "7", "numpad_8": "8", "numpad_9": "9",
        "numpad_decimal": ".", "numpad_add": "+", "numpad_subtract": "-",
        "numpad_multiply": "*", "numpad_divide": "/", "numpad_enter": Key.enter,
    }


if _IS_WINDOWS:
    _numpad_map = _numpad_key_map_windows()
else:
    _numpad_map = _numpad_key_map_linux_or_mac()

KEY_ID_TO_PYNPUT = {**_base_key_map(), **_numpad_map}


def key_id_to_press(key_id: str):
    """Convert key_id to pynput Key or char for press/release."""
    if key_id in KEY_ID_TO_PYNPUT:
        return KEY_ID_TO_PYNPUT[key_id]
    return key_id
