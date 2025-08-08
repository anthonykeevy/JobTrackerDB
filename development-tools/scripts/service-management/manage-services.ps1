# JobTrackerDB Service Management Script
# This script provides better control over the development environment

param(
    [Parameter(Position=0)]
    [ValidateSet("start", "stop", "restart", "status", "cleanup")]
    [string]$Action = "start"
)

function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Get-ServiceStatus {
    Write-ColorOutput Green "=== JobTrackerDB Service Status ==="
    
    # Check backend - count Python processes
    $pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
    if ($pythonProcesses) {
        $count = $pythonProcesses.Count
        Write-ColorOutput Green "✅ Backend (Python): Running ($count processes)"
        $pythonProcesses | ForEach-Object { Write-ColorOutput Yellow "   PID: $($_.Id) - Started: $($_.StartTime)" }
    } else {
        Write-ColorOutput Red "❌ Backend (Python): Not running"
    }
    
    # Check frontend - count Node processes
    $nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue
    if ($nodeProcesses) {
        $count = $nodeProcesses.Count
        Write-ColorOutput Green "✅ Frontend (Node): Running ($count processes)"
        $nodeProcesses | ForEach-Object { Write-ColorOutput Yellow "   PID: $($_.Id) - Started: $($_.StartTime)" }
    } else {
        Write-ColorOutput Red "❌ Frontend (Node): Not running"
    }
    
    # Check ports
    $port8000 = netstat -an | findstr ":8000"
    $port5173 = netstat -an | findstr ":5173"
    $port5174 = netstat -an | findstr ":5174"
    
    if ($port8000) {
        Write-ColorOutput Green "✅ Port 8000: Active"
    } else {
        Write-ColorOutput Red "❌ Port 8000: Not listening"
    }
    
    if ($port5173 -or $port5174) {
        Write-ColorOutput Green "✅ Frontend Port: Active ($(if($port5173) {'5173'} else {'5174'}))"
    } else {
        Write-ColorOutput Red "❌ Frontend Port: Not listening"
    }
}

function Stop-Services {
    Write-ColorOutput Yellow "=== Stopping JobTrackerDB Services ==="
    
    # Stop Python processes (backend)
    $pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
    if ($pythonProcesses) {
        Write-ColorOutput Yellow "Stopping Python processes..."
        $pythonProcesses | Stop-Process -Force
        Write-ColorOutput Green "✅ Python processes stopped"
    }
    
    # Stop Node processes (frontend)
    $nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*vite*" }
    if ($nodeProcesses) {
        Write-ColorOutput Yellow "Stopping Node processes..."
        $nodeProcesses | Stop-Process -Force
        Write-ColorOutput Green "✅ Node processes stopped"
    }
    
    # Kill processes on specific ports
    Write-ColorOutput Yellow "Killing processes on ports 8000, 5173, 5174..."
    netstat -ano | findstr ":8000\|:5173\|:5174" | ForEach-Object {
        $parts = $_ -split '\s+'
        $processId = $parts[-1]
        if ($processId -match '^\d+$') {
            try {
                Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                Write-ColorOutput Green "✅ Killed process $processId"
            } catch {
                Write-ColorOutput Red "❌ Failed to kill process $processId"
            }
        }
    }
}

function Start-Services {
    Write-ColorOutput Yellow "=== Starting JobTrackerDB Services ==="
    
    # Check if services are already running
    $backendRunning = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" }
    $frontendRunning = Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*vite*" }
    
    if ($backendRunning -or $frontendRunning) {
        Write-ColorOutput Yellow "⚠️  Services appear to be running. Use 'restart' to restart them."
        return
    }
    
    # Start services using npm
    Write-ColorOutput Yellow "Starting services with npm run dev:stable..."
    npm run dev:stable
    
    # Wait a moment and check status
    Start-Sleep -Seconds 3
    Get-ServiceStatus
}

function Restart-Services {
    Write-ColorOutput Yellow "=== Restarting JobTrackerDB Services ==="
    
    # Stop existing services
    Stop-Services
    
    # Wait a moment
    Start-Sleep -Seconds 2
    
    # Start services
    Start-Services
}

function Cleanup-Processes {
    Write-ColorOutput Yellow "=== Cleaning Up All Related Processes ==="
    
    # Stop all Python processes
    $pythonProcesses = Get-Process -Name "python" -ErrorAction SilentlyContinue
    if ($pythonProcesses) {
        Write-ColorOutput Yellow "Stopping all Python processes..."
        $pythonProcesses | Stop-Process -Force
        Write-ColorOutput Green "✅ All Python processes stopped"
    }
    
    # Stop all Node processes
    $nodeProcesses = Get-Process -Name "node" -ErrorAction SilentlyContinue
    if ($nodeProcesses) {
        Write-ColorOutput Yellow "Stopping all Node processes..."
        $nodeProcesses | Stop-Process -Force
        Write-ColorOutput Green "✅ All Node processes stopped"
    }
    
    # Kill any remaining processes on our ports
    Write-ColorOutput Yellow "Killing any remaining processes on development ports..."
    netstat -ano | findstr ":8000\|:5173\|:5174" | ForEach-Object {
        $parts = $_ -split '\s+'
        $processId = $parts[-1]
        if ($processId -match '^\d+$') {
            try {
                Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
                Write-ColorOutput Green "✅ Killed process $processId"
            } catch {
                Write-ColorOutput Red "❌ Failed to kill process $processId"
            }
        }
    }
    
    Write-ColorOutput Green "✅ Cleanup completed"
}

# Main execution
switch ($Action.ToLower()) {
    "start" {
        Start-Services
    }
    "stop" {
        Stop-Services
    }
    "restart" {
        Restart-Services
    }
    "status" {
        Get-ServiceStatus
    }
    "cleanup" {
        Cleanup-Processes
    }
    default {
        Write-ColorOutput Red "Invalid action. Use: start, stop, restart, status, or cleanup"
    }
}
