# Keyboard Repeater

A keyboard repeat tool that runs in the background. You can choose which keys to repeat, set the interval, and use hotkeys to start/stop. Config can be saved and loaded. Supported: **Windows**, **Ubuntu** / **Fedora** (and other Linux with X11), **macOS**.

## Features

1. **Keyboard layout** – Click keys on the on-screen keyboard to select which keys to repeat (multi-select; selected keys are highlighted in blue).
2. **Interval** – Enter a number and choose **Seconds** or **Minutes**.
3. **Hotkeys** – Default: **F9** to start, **F10** to stop. You can change them by clicking the hotkey buttons and pressing a key. Status (Stopped / Running) is shown in the window.
4. **Save / Open config** – Save the current setup (selected keys, interval, hotkeys) to a JSON file and load it later.
5. **Confirm** – Save current settings as default; they are loaded automatically on next startup.
6. **Clear** – Restore all settings to default values.
7. **Target app (Windows only)** – Optionally choose an executable; repeat will send keys to that app’s window even when another window has focus.
8. **Enable log / View log** – Turn on logging and open a window to view the repeater log (last 500 lines, with Refresh).

## Config and log file locations

- **Default config** (used by Confirm and on startup):  
  - **Windows:** `%APPDATA%\KeyboardRepeater\config.json`  
  - **Linux / macOS:** `~/.config/KeyboardRepeater/config.json`
- **Repeater log** (when “Enable log” is on):  
  - Same folder as above, file `repeater_log.txt`.

## Install

**Windows**

```bash
pip install -r requirements.txt
```

**Linux (Ubuntu / Fedora)**

1. Install system packages (for tkinter GUI and pynput keyboard):
   - **Ubuntu/Debian:** `sudo apt install python3-tk python3-xlib`
   - **Fedora:** `sudo dnf install python3-tkinter python3-xlib`
2. Then: `pip install -r requirements.txt` (or `pip3 install -r requirements.txt`)

**macOS**

1. Install Python 3 (e.g. from [python.org](https://www.python.org/) or `brew install python`) and tkinter (often included with Python; if not, `brew install python-tk`).
2. Then: `pip3 install -r requirements.txt`
3. For global hotkeys and key simulation, grant **Accessibility** (and optionally **Input Monitoring**) in **System Settings → Privacy & Security → Accessibility**.

## Run

```bash
python keyboard_repeater.py
```

On Linux/macOS you may need: `python3 keyboard_repeater.py`

## Portable build (no Python needed on target machine)

**Windows**

1. On a machine with Python installed:
   ```bash
   pip install -r requirements.txt -r requirements-build.txt
   pyinstaller --noconfirm KeyboardRepeater.spec
   ```
   Or run `build.bat` (Windows).

2. Output: `dist\KeyboardRepeater.exe`. Copy to any Windows PC and run; no Python required.

**Linux (Ubuntu / Fedora)**

1. On a Linux machine with Python 3 and system deps (e.g. `python3-tk`, `python3-xlib`) installed:
   ```bash
   chmod +x build.sh
   ./build.sh
   ```
2. Output: `dist/KeyboardRepeater` (no extension). Copy to other Linux PCs of the **same architecture** (e.g. x86_64) and run with `./KeyboardRepeater`. No Python required on the target. The target still needs an X11 session (normal desktop).

**macOS**

1. On a Mac with Python 3 installed:
   ```bash
   chmod +x build-mac.sh
   ./build-mac.sh
   ```
2. Output: `dist/KeyboardRepeater`. Copy to other Macs of the **same architecture** (Intel x86_64 or Apple Silicon arm64) and run with `./KeyboardRepeater`. No Python required on the target. First run may require allowing the app in **System Settings → Privacy & Security → Accessibility**.

## Notes

- Without **Target app** set, repeated keys are sent to the **currently focused window**. Switch to the target app before pressing the start hotkey.
- With **Target app** set (Windows), keys are sent to that app’s window via PostMessage, so repeat continues even when you switch to another window (e.g. to view the log).
- Hotkeys work globally (e.g. F9/F10 work even when the app window is not focused).
- **Windows:** If hotkeys do not work, try running as administrator.
- **Linux:** Needs an X11 session (e.g. normal desktop). Numpad keys in the UI send the same characters as the main number row (some apps may not distinguish numpad vs main keyboard).
- **macOS:** Grant **Accessibility** (and **Input Monitoring** if prompted) for global hotkeys and key simulation. Numpad keys in the UI use the same character/Key fallback as on Linux.

