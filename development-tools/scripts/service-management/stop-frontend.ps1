# JobTrackerDB Frontend Stop Script for PowerShell
# This script stops only the frontend service

Write-Host "Stopping JobTrackerDB Frontend..." -ForegroundColor Red
Write-Host "==================================" -ForegroundColor Red

# Find and stop Node processes running vite
$nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue

if ($nodeProcesses) {
    Write-Host "Found frontend processes:" -ForegroundColor Yellow
    foreach ($process in $nodeProcesses) {
        Write-Host "   PID: $($process.Id) - Started: $($process.StartTime)" -ForegroundColor Cyan
    }
    
    Write-Host "Stopping frontend processes..." -ForegroundColor Yellow
    $nodeProcesses | Stop-Process -Force
    Write-Host "Frontend processes stopped" -ForegroundColor Green
} else {
    Write-Host "No frontend processes found" -ForegroundColor Blue
}

# Kill any processes on ports 5173 and 5174
Write-Host "Checking for processes on ports 5173, 5174..." -ForegroundColor Yellow
$portProcesses = netstat -ano | findstr ":5173\|:5174" | ForEach-Object {
    $parts = $_ -split '\s+'
    $processId = $parts[-1]
    if ($processId -match '^\d+$') {
        try {
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
            Write-Host "Killed process $processId on frontend port" -ForegroundColor Green
        } catch {
            Write-Host "Failed to kill process $processId" -ForegroundColor Red
        }
    }
}

Write-Host "Frontend stop completed" -ForegroundColor Green
