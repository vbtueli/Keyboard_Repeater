# -*- coding: utf-8 -*-
"""Keyboard repeater main application."""
import os
import threading

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from pynput.keyboard import Controller as KeyController

from config_io import (
    save_config as config_save,
    load_config as config_load,
    apply_config_to_app,
    clear_log,
    get_default_config_path,
    get_log_path,
    save_default_config,
    write_log,
    DEFAULT_CONFIG,
)
from ui_builder import build_ui
from repeater_engine import run_repeat_loop
from hotkey_manager import HotkeyManager


class KeyboardRepeaterApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Keyboard Repeater")
        self.root.geometry("835x380")
        self.root.minsize(680, 360)
        self.root.resizable(True, True)

        self.selected_keys = set()
        self.key_buttons = {}
        self.running = False
        self.repeat_thread = None
        self.stop_event = threading.Event()
        self.key_controller = KeyController()
        self.start_hotkey = "f9"
        self.stop_hotkey = "f10"
        self._closing = False

        self.hotkey_mgr = HotkeyManager(self.root, self._start_repeat, self._stop_repeat)
        self.hotkey_mgr.set_hotkeys(self.start_hotkey, self.stop_hotkey)
        build_ui(self.root, self)
        self._center_on_screen()
        self._load_default_config_if_exists()
        self.hotkey_mgr.start_listener()

    def _center_on_screen(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"+{x}+{y}")

    def _on_configure(self, event):
        if event.widget != self.root:
            return
        self.size_hint_var.set(f"{self.root.winfo_width()} × {self.root.winfo_height()}")

    def _update_hotkey_button_states(self):
        start_id, stop_id = self.start_hotkey.lower(), self.stop_hotkey.lower()
        for key_id, btn_list in self.key_buttons.items():
            is_hotkey = key_id == start_id or key_id == stop_id
            for btn in btn_list:
                if is_hotkey:
                    btn.config(state=tk.DISABLED, bg="#C0C0C0", activebackground="#C0C0C0", cursor="")
                    self.selected_keys.discard(key_id)
                else:
                    btn.config(state=tk.NORMAL, cursor="hand2")
                    btn.config(bg="#87CEEB" if key_id in self.selected_keys else "SystemButtonFace",
                               activebackground="#6BB3DD" if key_id in self.selected_keys else "SystemButtonFace")

    def _toggle_key(self, key_id: str):
        if key_id in (self.start_hotkey.lower(), self.stop_hotkey.lower()):
            return
        if key_id in self.selected_keys:
            self.selected_keys.discard(key_id)
            for btn in self.key_buttons.get(key_id, []):
                btn.config(bg="SystemButtonFace", activebackground="SystemButtonFace")
        else:
            self.selected_keys.add(key_id)
            for btn in self.key_buttons.get(key_id, []):
                btn.config(bg="#87CEEB", activebackground="#6BB3DD")

    def _get_interval_seconds(self) -> float:
        try:
            val = float(self.interval_var.get().strip())
        except ValueError:
            return 1.0
        if val <= 0:
            return 1.0
        return val * 60.0 if self.unit_var.get() == "Minutes" else val

    def _begin_capture_hotkey(self, which: str):
        if self.hotkey_mgr.capturing_which:
            messagebox.showinfo("Info", "Please press the key you want to set.")
            return
        if which == "start":
            self.start_hotkey_btn.config(text="Press key...")
        else:
            self.stop_hotkey_btn.config(text="Press key...")
        self.hotkey_mgr.capture(which, self._set_captured_hotkey)

    def _set_captured_hotkey(self, which: str, name: str):
        if which == "start":
            self.start_hotkey = name
            self.start_hotkey_var.set(name.upper())
            self.start_hotkey_btn.config(text=name.upper())
        else:
            self.stop_hotkey = name
            self.stop_hotkey_var.set(name.upper())
            self.stop_hotkey_btn.config(text=name.upper())
        self.hotkey_mgr.set_hotkeys(self.start_hotkey, self.stop_hotkey)
        self._update_hotkey_button_states()

    def _start_repeat(self):
        if getattr(self, "_closing", False):
            return
        if self.running:
            return
        if not self.selected_keys:
            messagebox.showwarning("Warning", "Please select at least one key to repeat.")
            return
        self.running = True
        self.stop_event.clear()
        self.status_var.set("Running")
        self.status_label.config(foreground="green")
        interval = self._get_interval_seconds()
        target_exe_getter = lambda: self.target_exe_var.get().strip() if getattr(self, "target_exe_var", None) else ""
        log_enabled = getattr(self, "log_enabled_var", None) and self.log_enabled_var.get()
        if log_enabled:
            try:
                clear_log(get_log_path())
            except Exception:
                pass
        log_func = (lambda msg: write_log(get_log_path(), msg)) if log_enabled else None
        self.repeat_thread = threading.Thread(
            target=run_repeat_loop,
            args=(self.key_controller, lambda: self.selected_keys, interval, self.stop_event),
            kwargs={"target_exe_getter": target_exe_getter, "log_func": log_func},
            daemon=True
        )
        self.repeat_thread.start()

    def _stop_repeat(self):
        self.running = False
        self.stop_event.set()
        if getattr(self, "_closing", False):
            return
        if not getattr(self, "status_var", None):
            return
        try:
            self.status_var.set("Stopped")
            if getattr(self, "status_label", None):
                self.status_label.config(foreground="")
        except Exception:
            pass

    def _save_config(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON config", "*.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            config_save(path, self)
            messagebox.showinfo("Saved", "Config saved to:\n" + path)
        except Exception as e:
            messagebox.showerror("Error", "Save failed: " + str(e))

    def _load_config(self):
        path = filedialog.askopenfilename(filetypes=[("JSON config", "*.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            data = config_load(path)
        except Exception as e:
            messagebox.showerror("Error", "Load failed: " + str(e))
            return
        apply_config_to_app(data, self)
        self.hotkey_mgr.set_hotkeys(self.start_hotkey, self.stop_hotkey)
        self._update_hotkey_button_states()
        messagebox.showinfo("Loaded", "Config loaded:\n" + path)

    def _load_default_config_if_exists(self):
        """Load last-saved config from default path if the file exists."""
        path = get_default_config_path()
        if not os.path.isfile(path):
            return
        try:
            data = config_load(path)
            apply_config_to_app(data, self)
            self.hotkey_mgr.set_hotkeys(self.start_hotkey, self.stop_hotkey)
            self._update_hotkey_button_states()
        except Exception:
            pass

    def _confirm_save_default(self):
        """Save current settings as default; next startup will load them."""
        try:
            save_default_config(self)
            messagebox.showinfo("Confirm", "Settings saved as default. They will be loaded on next startup.")
        except Exception as e:
            messagebox.showerror("Error", "Save failed: " + str(e))

    def _clear_to_defaults(self):
        """Restore all settings to default values."""
        apply_config_to_app(DEFAULT_CONFIG, self)
        self.hotkey_mgr.set_hotkeys(self.start_hotkey, self.stop_hotkey)
        self._update_hotkey_button_states()
        messagebox.showinfo("Clear", "Restored to default values.")

    def _view_log(self):
        """Open a window showing the repeater log file (last 500 lines) with Refresh button."""
        path = get_log_path()
        win = tk.Toplevel(self.root)
        win.title("Repeater Log")
        win.geometry("700x400")
        win.minsize(400, 200)
        top_bar = ttk.Frame(win)
        top_bar.pack(fill=tk.X, padx=4, pady=2)

        def load_log():
            text.config(state=tk.NORMAL)
            text.delete("1.0", tk.END)
            if os.path.isfile(path):
                try:
                    with open(path, "r", encoding="utf-8", errors="replace") as f:
                        lines = f.readlines()
                    content = "".join(lines[-500:]) if len(lines) > 500 else "".join(lines)
                    text.insert("1.0", content or "(empty)")
                except Exception as e:
                    text.insert("1.0", f"Could not read log: {e}")
            else:
                text.insert("1.0", f"(Log file not created yet.)\nPath: {path}\n\nEnable \"Enable log\" and start repeat to write logs.")
            text.config(state=tk.DISABLED)
            text.see(tk.END)

        ttk.Button(top_bar, text="Refresh", command=load_log).pack(side=tk.LEFT, padx=2)
        text = tk.Text(win, wrap=tk.WORD, font=("Consolas", 9))
        scroll = ttk.Scrollbar(win, command=text.yview)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        text.config(yscrollcommand=scroll.set)
        load_log()
        win.update_idletasks()
        w, h = win.winfo_width(), win.winfo_height()
        x = (win.winfo_screenwidth() - w) // 2
        y = (win.winfo_screenheight() - h) // 2
        x -= 120
        y -= 80
        win.geometry(f"+{max(0, x)}+{max(0, y)}")

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()

    def _on_close(self):
        if self.running:
            if not messagebox.askyesno("Confirm exit", "Repeat is running. Are you sure you want to exit?"):
                return
        self._closing = True
        try:
            self._stop_repeat()
            self.hotkey_mgr.stop_listener()
        except Exception:
            pass
        try:
            self.root.destroy()
        except Exception:
            pass
