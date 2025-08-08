# JobTrackerDB Frontend Status Script for PowerShell
# This script checks only the frontend service status

Write-Host "JobTrackerDB Frontend Status" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

# Check for Node processes running vite
$nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue

if ($nodeProcesses) {
    Write-Host "Frontend (Node): Running ($($nodeProcesses.Count) processes)" -ForegroundColor Green
    foreach ($process in $nodeProcesses) {
        Write-Host "   PID: $($process.Id) - Started: $($process.StartTime)" -ForegroundColor White
    }
} else {
    Write-Host "Frontend (Node): Not running" -ForegroundColor Red
}

# Check if ports 5173 and 5174 are listening
$port5173 = netstat -ano | findstr ":5173" | findstr "LISTENING"
$port5174 = netstat -ano | findstr ":5174" | findstr "LISTENING"

if ($port5173) {
    Write-Host "Port 5173: Active" -ForegroundColor Green
} else {
    Write-Host "Port 5173: Not listening" -ForegroundColor Red
}

if ($port5174) {
    Write-Host "Port 5174: Active" -ForegroundColor Green
} else {
    Write-Host "Port 5174: Not listening" -ForegroundColor Red
}

# Test frontend connectivity
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5173" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "Frontend App: Responding" -ForegroundColor Green
    } else {
        Write-Host "Frontend App: Responding with status $($response.StatusCode)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Frontend App: Not responding" -ForegroundColor Red
}

Write-Host ""
Write-Host "Frontend URLs:" -ForegroundColor Cyan
Write-Host "   App: http://localhost:5173" -ForegroundColor White
Write-Host "   Alt: http://localhost:5174" -ForegroundColor White
