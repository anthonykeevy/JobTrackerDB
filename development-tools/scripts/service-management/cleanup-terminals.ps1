# JobTrackerDB Terminal Cleanup Script
# This script safely cleans up extra PowerShell processes

Write-Host "🧹 Cleaning up extra PowerShell processes..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Get current process ID (this terminal)
$currentProcessId = $PID

# Get all PowerShell processes
$powershellProcesses = Get-Process | Where-Object {$_.ProcessName -eq "powershell"}

Write-Host "Current terminal process ID: $currentProcessId" -ForegroundColor Cyan
Write-Host "Found $($powershellProcesses.Count) total PowerShell processes" -ForegroundColor Yellow
Write-Host ""

# Show which processes will be kept vs cleaned up
foreach ($process in $powershellProcesses) {
    if ($process.Id -eq $currentProcessId) {
        Write-Host "✅ KEEPING: Process $($process.Id) (current terminal)" -ForegroundColor Green
    } else {
        Write-Host "🗑️  CLEANING: Process $($process.Id) (extra terminal)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "⚠️  WARNING: This will close all other PowerShell windows!" -ForegroundColor Red
Write-Host "Make sure you've saved any work in other terminals." -ForegroundColor Yellow
Write-Host ""

$confirmation = Read-Host "Do you want to continue? (y/N)"
if ($confirmation -eq "y" -or $confirmation -eq "Y") {
    Write-Host "Cleaning up extra processes..." -ForegroundColor Yellow
    
    foreach ($process in $powershellProcesses) {
        if ($process.Id -ne $currentProcessId) {
            try {
                Write-Host "Stopping process $($process.Id)..." -ForegroundColor Cyan
                Stop-Process -Id $process.Id -Force
                Write-Host "✅ Stopped process $($process.Id)" -ForegroundColor Green
            } catch {
                Write-Host "❌ Failed to stop process $($process.Id): $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }
    
    Write-Host ""
    Write-Host "✅ Cleanup complete!" -ForegroundColor Green
    Write-Host "Only the current terminal remains." -ForegroundColor Cyan
} else {
    Write-Host "❌ Cleanup cancelled." -ForegroundColor Yellow
    Write-Host "You can manually close extra PowerShell windows." -ForegroundColor White
}

Write-Host ""
Write-Host "To prevent this in the future:" -ForegroundColor Cyan
Write-Host "1. Use only the integrated terminal in Cursor" -ForegroundColor White
Write-Host "2. Close extra PowerShell windows manually" -ForegroundColor White
Write-Host "3. Restart Cursor if you have too many processes" -ForegroundColor White
