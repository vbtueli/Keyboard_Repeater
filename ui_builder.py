# -*- coding: utf-8 -*-
"""Build keyboard repeater UI; attach widgets/vars to app."""
import tkinter as tk
from tkinter import ttk

from layout import MAIN_LAYOUT, NUMPAD_LAYOUT


def build_ui(root, app):
    """Build all UI; set app.key_buttons, app.interval_var, app.unit_var, app.unit_combo,
    app.start_hotkey_btn, app.stop_hotkey_btn, app.status_var, app.status_label, app.size_hint_var."""
    main = ttk.Frame(root, padding=(6, 6, 6, 2))
    main.pack(fill=tk.BOTH, expand=True)

    ttk.Label(main, text="Click keys to repeat (multi-select):", font=("Segoe UI", 10)).pack(anchor=tk.W)
    key_frame = ttk.Frame(main)
    key_frame.pack(fill=tk.X, pady=(2, 6))

    main_kb = ttk.Frame(key_frame)
    main_kb.pack(side=tk.LEFT, fill=tk.X, expand=True)
    for indent_px, row_keys in MAIN_LAYOUT:
        row_f = ttk.Frame(main_kb)
        row_f.pack(fill=tk.X, pady=1)
        if indent_px > 0:
            spacer = ttk.Frame(row_f, width=indent_px)
            spacer.pack(side=tk.LEFT)
            spacer.pack_propagate(False)
        for item in row_keys:
            _add_key_button(row_f, item, app)

    numpad_f = ttk.Frame(key_frame)
    numpad_f.pack(side=tk.RIGHT, padx=(12, 0))
    for row_keys in NUMPAD_LAYOUT:
        row_f = ttk.Frame(numpad_f)
        row_f.pack(fill=tk.X, pady=1)
        for item in row_keys:
            _add_key_button(row_f, item, app)

    interval_frame = ttk.Frame(main)
    interval_frame.pack(fill=tk.X, pady=4)
    ttk.Label(interval_frame, text="Interval:", width=10, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 4))
    app.interval_var = tk.StringVar(value="1")
    ttk.Entry(interval_frame, textvariable=app.interval_var, width=8).pack(side=tk.LEFT, padx=2)
    app.unit_var = tk.StringVar(value="Seconds")
    app.unit_combo = ttk.Combobox(
        interval_frame, textvariable=app.unit_var,
        values=["Seconds", "Minutes"], state="readonly", width=10
    )
    app.unit_combo.pack(side=tk.LEFT, padx=2)

    hotkey_frame = ttk.Frame(main)
    hotkey_frame.pack(fill=tk.X, pady=4)
    ttk.Label(hotkey_frame, text="Start hotkey:", width=10, anchor=tk.W).pack(side=tk.LEFT, padx=(0, 4))
    app.start_hotkey_var = tk.StringVar(value=app.start_hotkey.upper())
    app.start_hotkey_btn = ttk.Button(
        hotkey_frame, text=app.start_hotkey.upper(), width=8,
        command=lambda: app._begin_capture_hotkey("start")
    )
    app.start_hotkey_btn.pack(side=tk.LEFT, padx=2)
    ttk.Label(hotkey_frame, text="Stop hotkey:", width=10, anchor=tk.W).pack(side=tk.LEFT, padx=(8, 4))
    app.stop_hotkey_var = tk.StringVar(value=app.stop_hotkey.upper())
    app.stop_hotkey_btn = ttk.Button(
        hotkey_frame, text=app.stop_hotkey.upper(), width=8,
        command=lambda: app._begin_capture_hotkey("stop")
    )
    app.stop_hotkey_btn.pack(side=tk.LEFT, padx=2)
    ttk.Label(hotkey_frame, text="Status:", width=8, anchor=tk.W).pack(side=tk.LEFT, padx=(8, 4))
    app.status_var = tk.StringVar(value="Stopped")
    app.status_label = ttk.Label(hotkey_frame, textvariable=app.status_var, font=("Segoe UI", 10, "bold"))
    app.status_label.pack(side=tk.LEFT)

    btn_frame = ttk.Frame(main)
    btn_frame.pack(fill=tk.X, pady=2)
    ttk.Button(btn_frame, text="Save as...", command=app._save_config).pack(side=tk.LEFT, padx=4)
    ttk.Button(btn_frame, text="Open config", command=app._load_config).pack(side=tk.LEFT, padx=4)
    app.size_hint_var = tk.StringVar(value="")
    ttk.Label(btn_frame, textvariable=app.size_hint_var, font=("Segoe UI", 9), foreground="gray").pack(side=tk.RIGHT, padx=4)
    root.bind("<Configure>", app._on_configure)

    app._update_hotkey_button_states()


def _add_key_button(parent, item, app):
    label, key_id = item[0], item[1]
    w = item[2] if len(item) > 2 else (4 if len(label) <= 2 else 6)
    btn = tk.Button(
        parent, text=label, width=w,
        relief=tk.RAISED, bd=2, cursor="hand2",
        command=lambda k=key_id: app._toggle_key(k)
    )
    btn.pack(side=tk.LEFT, padx=1, pady=1)
    if key_id not in app.key_buttons:
        app.key_buttons[key_id] = []
    app.key_buttons[key_id].append(btn)
