# -*- coding: utf-8 -*-
"""Save/load config to/from JSON. App object provides selected_keys, interval_var, unit_var, hotkeys, key_buttons."""
import json
import os
import sys
from datetime import datetime


def get_default_config_path() -> str:
    """Return path to the 'last session' config file (used by Confirm button and on startup)."""
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.path.join(os.path.expanduser("~"), ".config")
    folder = os.path.join(base, "KeyboardRepeater")
    return os.path.join(folder, "config.json")


def get_log_path() -> str:
    """Return path to the repeater log file (same folder as default config)."""
    folder = os.path.dirname(get_default_config_path())
    return os.path.join(folder, "repeater_log.txt")


def clear_log(path: str) -> None:
    """Clear the log file (truncate). Creates folder if needed. Call when starting a new run."""
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        pass


def write_log(path: str, message: str) -> None:
    """Append a timestamped line to the log file. Creates folder if needed."""
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + message + "\n")


def save_default_config(app) -> None:
    """Save current app state to default config path (for next startup)."""
    path = get_default_config_path()
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    save_config(path, app)


# Default values for Clear button (restore defaults).
DEFAULT_CONFIG = {
    "selected_keys": [],
    "interval": 11,
    "unit": "Seconds",
    "start_hotkey": "f9",
    "stop_hotkey": "f10",
    "target_exe": "",
}


def save_config(path: str, app) -> None:
    """Save app state to JSON file."""
    interval_sec = app._get_interval_seconds()
    unit = app.unit_var.get()
    interval_num = interval_sec / 60.0 if unit == "Minutes" else interval_sec
    data = {
        "selected_keys": list(app.selected_keys),
        "interval": interval_num,
        "unit": unit,
        "start_hotkey": app.start_hotkey,
        "stop_hotkey": app.stop_hotkey,
        "target_exe": getattr(app, "target_exe_var", None) and app.target_exe_var.get().strip() or "",
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_config(path: str) -> dict:
    """Load config dict from JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def apply_config_to_app(data: dict, app) -> None:
    """Apply loaded config dict to app (selection, interval, unit, hotkeys)."""
    app.selected_keys.clear()
    for key_id, btn_list in app.key_buttons.items():
        for btn in btn_list:
            btn.config(bg="SystemButtonFace", activebackground="SystemButtonFace")
    for key_id in data.get("selected_keys", []):
        app.selected_keys.add(key_id)
        for btn in app.key_buttons.get(key_id, []):
            btn.config(bg="#87CEEB", activebackground="#6BB3DD")
    app.interval_var.set(str(data.get("interval", 1)))
    raw_unit = data.get("unit", "Seconds")
    unit = "Minutes" if raw_unit in ("分鐘", "Minutes") else "Seconds"
    app.unit_var.set(unit)
    app.unit_combo.set(unit)
    app.start_hotkey = data.get("start_hotkey", "f9")
    app.stop_hotkey = data.get("stop_hotkey", "f10")
    app.start_hotkey_var.set(app.start_hotkey.upper())
    app.stop_hotkey_var.set(app.stop_hotkey.upper())
    app.start_hotkey_btn.config(text=app.start_hotkey.upper())
    app.stop_hotkey_btn.config(text=app.stop_hotkey.upper())
    if getattr(app, "target_exe_var", None) is not None:
        app.target_exe_var.set(data.get("target_exe", "") or "")