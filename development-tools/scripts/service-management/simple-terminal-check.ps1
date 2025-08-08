# JobTrackerDB Terminal Identification Script
# This script helps identify which PowerShell session is the integrated terminal

Write-Host "Identifying PowerShell Sessions..." -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Get all PowerShell processes
$powershellProcesses = Get-Process | Where-Object {$_.ProcessName -eq "powershell"}

Write-Host "Found $($powershellProcesses.Count) PowerShell processes:" -ForegroundColor Yellow
Write-Host ""

foreach ($process in $powershellProcesses) {
    Write-Host "Process ID: $($process.Id)" -ForegroundColor Cyan
    Write-Host "Start Time: $($process.StartTime)" -ForegroundColor White
    Write-Host "Memory Usage: $([math]::Round($process.WorkingSet64 / 1MB, 2)) MB" -ForegroundColor White
    Write-Host "---"
}

Write-Host ""
Write-Host "How to identify the integrated terminal:" -ForegroundColor Green
Write-Host "1. Look for the terminal with the most recent activity" -ForegroundColor Yellow
Write-Host "2. The integrated terminal usually has the project path in the prompt" -ForegroundColor Yellow
Write-Host "3. Try running 'pwd' in each terminal to see the current directory" -ForegroundColor Yellow
Write-Host ""

Write-Host "To clean up extra processes:" -ForegroundColor Red
Write-Host "1. Close any extra PowerShell windows manually" -ForegroundColor Yellow
Write-Host "2. Or run: .\cleanup-terminals.ps1" -ForegroundColor Yellow
Write-Host ""

# Check if we're in the project directory
$currentPath = Get-Location
if ($currentPath.Path -like "*JobTrackerDB*") {
    Write-Host "SUCCESS: This appears to be the integrated terminal (in JobTrackerDB directory)" -ForegroundColor Green
} else {
    Write-Host "WARNING: This terminal is not in the JobTrackerDB directory" -ForegroundColor Yellow
    Write-Host "Current path: $($currentPath.Path)" -ForegroundColor White
}

Write-Host ""
Write-Host "Tip: The integrated terminal should show:" -ForegroundColor Cyan
Write-Host "PS C:\Users\tonyk\OneDrive\Projects\JobTrackerDB>" -ForegroundColor White
