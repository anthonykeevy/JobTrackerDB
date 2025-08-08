# JobTrackerDB Development Setup Script
# Run this script from Cursor's integrated terminal

param(
    [string]$Action = "dev",
    [switch]$Kill,
    [switch]$Install,
    [switch]$Clean
)

Write-Host "🚀 JobTrackerDB Development Setup" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Function to check if ports are in use
function Test-Port {
    param([int]$Port)
    $connection = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    return $connection -ne $null
}

# Function to kill processes on specific ports
function Stop-PortProcess {
    param([int]$Port)
    $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | ForEach-Object { Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue }
    if ($processes) {
        Write-Host "🛑 Stopping processes on port $Port..." -ForegroundColor Yellow
        $processes | Stop-Process -Force
        Start-Sleep -Seconds 2
    }
}

# Function to install dependencies
function Install-Dependencies {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Blue
    
    # Install root dependencies
    Write-Host "Installing root dependencies..." -ForegroundColor Cyan
    npm install
    
    # Install frontend dependencies
    Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
    Set-Location frontend
    npm install
    Set-Location ..
    
    # Install backend dependencies
    Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
    Set-Location backend
    pip install -r requirements.txt
    Set-Location ..
    
    Write-Host "✅ All dependencies installed!" -ForegroundColor Green
}

# Function to clean cache
function Clear-Cache {
    Write-Host "🧹 Cleaning cache..." -ForegroundColor Blue
    
    # Clean frontend cache
    if (Test-Path "frontend/node_modules/.cache") {
        Remove-Item -Path "frontend/node_modules/.cache" -Recurse -Force
        Write-Host "Frontend cache cleaned" -ForegroundColor Cyan
    }
    
    # Clean backend cache
    if (Test-Path "backend/__pycache__") {
        Remove-Item -Path "backend/__pycache__" -Recurse -Force
        Write-Host "Backend cache cleaned" -ForegroundColor Cyan
    }
    
    Write-Host "✅ Cache cleaned!" -ForegroundColor Green
}

# Main script logic
switch ($Action.ToLower()) {
    "kill" {
        Write-Host "🛑 Killing all development processes..." -ForegroundColor Red
        Stop-PortProcess -Port 8000
        Stop-PortProcess -Port 5173
        Write-Host "✅ All processes stopped!" -ForegroundColor Green
    }
    "install" {
        Install-Dependencies
    }
    "clean" {
        Clear-Cache
    }
    "dev" {
        # Check if ports are in use
        $backendPort = Test-Port -Port 8000
        $frontendPort = Test-Port -Port 5173
        
        if ($backendPort -or $frontendPort) {
            Write-Host "⚠️  Ports are in use. Stopping existing processes..." -ForegroundColor Yellow
            Stop-PortProcess -Port 8000
            Stop-PortProcess -Port 5173
            Start-Sleep -Seconds 3
        }
        
        Write-Host "🚀 Starting development servers..." -ForegroundColor Green
        Write-Host "Backend: http://127.0.0.1:8000" -ForegroundColor Cyan
        Write-Host "Frontend: http://localhost:5173" -ForegroundColor Cyan
        Write-Host "Press Ctrl+C to stop all services" -ForegroundColor Yellow
        Write-Host ""
        
        # Start both services concurrently using PowerShell
        Write-Host "Starting services with npm run dev..." -ForegroundColor Green
        npm run dev
    }
    default {
        Write-Host "Usage:" -ForegroundColor Yellow
        Write-Host "  .\dev-setup.ps1 dev      - Start both services" -ForegroundColor White
        Write-Host "  .\dev-setup.ps1 kill     - Kill all processes" -ForegroundColor White
        Write-Host "  .\dev-setup.ps1 install  - Install dependencies" -ForegroundColor White
        Write-Host "  .\dev-setup.ps1 clean    - Clean cache" -ForegroundColor White
    }
} 