# -*- coding: utf-8 -*-
"""Global hotkey listener and one-shot capture for start/stop hotkeys."""
from pynput import keyboard


class HotkeyManager:
    def __init__(self, root, on_start, on_stop):
        self.root = root
        self.on_start = on_start
        self.on_stop = on_stop
        self.start_hotkey = "f9"
        self.stop_hotkey = "f10"
        self.listener = None
        self.capture_listener = None
        self.capturing_which = None
        self.capture_callback = None

    def set_hotkeys(self, start: str, stop: str):
        self.start_hotkey = start.lower()
        self.stop_hotkey = stop.lower()

    def start_listener(self):
        if self.listener and self.listener.running:
            try:
                self.listener.stop()
            except Exception:
                pass
        self.listener = keyboard.Listener(on_press=self._on_key)
        self.listener.start()

    def stop_listener(self):
        if self.listener and self.listener.running:
            try:
                self.listener.stop()
            except Exception:
                pass
        self.listener = None
        if self.capture_listener and self.capture_listener.running:
            try:
                self.capture_listener.stop()
            except Exception:
                pass
        self.capture_listener = None
        self.capturing_which = None
        self.capture_callback = None

    def _on_key(self, key):
        if self.capturing_which is not None:
            return
        try:
            if not self.root.winfo_exists():
                return
            name = key.name.lower() if hasattr(key, "name") else (key.char or "").lower()
        except Exception:
            return
        if not name:
            return
        try:
            if name == self.start_hotkey and self.root.winfo_exists():
                self.root.after(0, self.on_start)
            elif name == self.stop_hotkey and self.root.winfo_exists():
                self.root.after(0, self.on_stop)
        except Exception:
            pass

    def capture(self, which: str, callback):
        """Start one-shot capture; on key press call callback(which, key_name) and restart global listener."""
        self.capturing_which = which
        self.capture_callback = callback
        self.stop_listener()
        self.capture_listener = keyboard.Listener(on_press=self._on_capture_key)
        self.capture_listener.start()

    def _on_capture_key(self, key):
        try:
            name = key.name if hasattr(key, "name") else (key.char or "")
            name = name.lower() if name else ""
        except Exception:
            return
        if not name:
            return
        if self.capture_callback and self.root.winfo_exists():
            self.root.after(0, lambda: self._finish_capture(which=self.capturing_which, name=name))

    def _finish_capture(self, which, name):
        self.capturing_which = None
        cb = self.capture_callback
        self.capture_callback = None
        if self.capture_listener and self.capture_listener.running:
            try:
                self.capture_listener.stop()
            except Exception:
                pass
        self.capture_listener = None
        try:
            if self.root.winfo_exists() and cb:
                cb(which, name)
            if self.root.winfo_exists():
                self.start_listener()
        except Exception:
            pass
