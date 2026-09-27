$ErrorActionPreference = "Stop"

Write-Host "[Night Launcher] Membuat venv untuk Windows..."
if (-not (Test-Path ".venv")) {
    py -m venv .venv
}

. ".\.venv\Scripts\Activate.ps1"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pyinstaller --onefile --name NightLauncher --noconsole .\night_launcher.py

Write-Host "[Night Launcher] Build selesai. File: dist\NightLauncher.exe"
