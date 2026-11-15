# One-click reproduction for VAL-LLM-BOOST-FRAMEWORK (Windows).
#
# Prereqs (all present on this machine): the Valhalla-main engine
# workspace, the valhalla-local engine shell, Python 3.12, CUDA 12.8.
# Steps: build the Fate engine -> (re)start the local engine on
# :8799 -> run the 560-line battery (needles / paraphrase / swap /
# absent / false-premise poison / injection / conflict).
#
# Full-stack variant (10k-line dialogue drift, needs the server
# gateway stack on :8780/:8787 + decode head): start the gateway
# from valhalla-server, then run tests\run_dialogue_drift.py 10006.
$ErrorActionPreference = 'Stop'
$env:CUDA_PATH = 'C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8'
$env:PATH = "$env:CUDA_PATH\bin;$env:PATH"

Write-Host '[1/3] Building Fate engine (hub-f64, release)...'
Push-Location 'C:\Ai\Valhalla-main\manifestsys'
cargo build -p hub-f64 --release --bin valhalla_base
Pop-Location

Write-Host '[2/3] (Re)starting local engine on :8799 with the fresh exe...'
Get-Process valhalla_base -ErrorAction SilentlyContinue |
    Where-Object { $_.Path -eq 'C:\Ai\rogue-products\valhalla-local\engine\valhalla_base.exe' } |
    Stop-Process -Force
Start-Sleep -Seconds 4
Copy-Item 'C:\Ai\Valhalla-main\target\release\valhalla_base.exe' 'C:\Ai\rogue-products\valhalla-local\engine\valhalla_base.exe' -Force
powershell -File 'C:\Ai\rogue-products\valhalla-local\start_engine.ps1' 8799
Start-Sleep -Seconds 12
curl.exe -s http://127.0.0.1:8799/health
Write-Host ''

Write-Host '[3/3] Running 560-line battery...'
& 'C:\Users\jouly\AppData\Local\Programs\Python\Python312\python.exe' 'C:\Ai\rogue-products\valhalla-local\tests\probe_battery560.py'
