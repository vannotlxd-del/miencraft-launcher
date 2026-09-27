@echo off
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" (
    call ".venv\Scripts\activate.bat"
) else (
    echo Membuat virtual environment...
    py -m venv .venv
    call ".venv\Scripts\activate.bat"
)

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python night_launcher.py
