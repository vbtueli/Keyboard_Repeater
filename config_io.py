# -*- coding: utf-8 -*-
"""Save/load config to/from JSON. App object provides selected_keys, interval_var, unit_var, hotkeys, key_buttons."""
import json


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
