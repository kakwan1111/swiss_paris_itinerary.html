$ErrorActionPreference = 'Stop'

Write-Host 'Installing build dependencies...'
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

Write-Host 'Building single-file Windows executable...'
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue
py -m PyInstaller --clean --noconfirm --onefile --windowed --name iPhoneDuoMonitor iphone_duo_monitor.py

New-Item -ItemType Directory -Force release | Out-Null
Compress-Archive -Path dist/iPhoneDuoMonitor.exe -DestinationPath release/iPhoneDuoMonitor-Windows.zip -Force
Write-Host 'Created release/iPhoneDuoMonitor-Windows.zip'
