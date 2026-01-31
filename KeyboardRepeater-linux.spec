# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Keyboard Repeater on Linux (single-file portable binary)
# Run on Linux: pyinstaller KeyboardRepeater-linux.spec

block_cipher = None

a = Analysis(
    ['keyboard_repeater.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pynput',
        'pynput.keyboard',
        'pynput.keyboard._xorg',
        'pynput._util',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='KeyboardRepeater',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)
