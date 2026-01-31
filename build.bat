@echo off
REM Build portable KeyboardRepeater.exe (requires Python + pip install -r requirements.txt -r requirements-build.txt)
echo Installing build deps...
pip install -r requirements.txt -r requirements-build.txt -q
echo Building...
pyinstaller --noconfirm KeyboardRepeater.spec
if %ERRORLEVEL% equ 0 (
    echo Done. Output: dist\KeyboardRepeater.exe
) else (
    echo Build failed.
    exit /b 1
)
