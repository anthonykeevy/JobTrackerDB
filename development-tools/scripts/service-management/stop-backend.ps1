# JobTrackerDB Backend Stop Script for PowerShell
# This script stops only the backend service

Write-Host "Stopping JobTrackerDB Backend..." -ForegroundColor Red
Write-Host "=================================" -ForegroundColor Red

# Find and stop Python processes running uvicorn
$pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue

if ($pythonProcesses) {
    Write-Host "Found backend processes:" -ForegroundColor Yellow
    foreach ($process in $pythonProcesses) {
        Write-Host "   PID: $($process.Id) - Started: $($process.StartTime)" -ForegroundColor Cyan
    }
    
    Write-Host "Stopping backend processes..." -ForegroundColor Yellow
    $pythonProcesses | Stop-Process -Force
    Write-Host "Backend processes stopped" -ForegroundColor Green
} else {
    Write-Host "No backend processes found" -ForegroundColor Blue
}

# Kill any processes on port 8000
Write-Host "Checking for processes on port 8000..." -ForegroundColor Yellow
$portProcesses = netstat -ano | findstr ":8000" | ForEach-Object {
    $parts = $_ -split '\s+'
    $processId = $parts[-1]
    if ($processId -match '^\d+$') {
        try {
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
            Write-Host "Killed process $processId on port 8000" -ForegroundColor Green
        } catch {
            Write-Host "Failed to kill process $processId" -ForegroundColor Red
        }
    }
}

Write-Host "Backend stop completed" -ForegroundColor Green
