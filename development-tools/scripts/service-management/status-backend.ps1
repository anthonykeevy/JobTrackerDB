# JobTrackerDB Backend Status Script for PowerShell
# This script checks only the backend service status

Write-Host "JobTrackerDB Backend Status" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan

# Check for Python processes running uvicorn
$pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue

if ($pythonProcesses) {
    Write-Host "Backend (Python): Running ($($pythonProcesses.Count) processes)" -ForegroundColor Green
    foreach ($process in $pythonProcesses) {
        Write-Host "   PID: $($process.Id) - Started: $($process.StartTime)" -ForegroundColor White
    }
} else {
    Write-Host "Backend (Python): Not running" -ForegroundColor Red
}

# Check if port 8000 is listening
$port8000 = netstat -ano | findstr ":8000" | findstr "LISTENING"
if ($port8000) {
    Write-Host "Port 8000: Active" -ForegroundColor Green
} else {
    Write-Host "Port 8000: Not listening" -ForegroundColor Red
}

# Test backend connectivity
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:8000/health" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "Backend API: Responding" -ForegroundColor Green
    } else {
        Write-Host "Backend API: Responding with status $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Backend API: Not responding" -ForegroundColor Red
}

Write-Host ""
Write-Host "Backend URLs:" -ForegroundColor Cyan
Write-Host "   API: http://127.0.0.1:8000" -ForegroundColor White
Write-Host "   Docs: http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "   Health: http://127.0.0.1:8000/health" -ForegroundColor White
