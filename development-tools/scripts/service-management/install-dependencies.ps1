# JobTrackerDB Dependency Installation Script for PowerShell
# This script installs all dependencies for the project

Write-Host "📦 Installing JobTrackerDB Dependencies..." -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

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

# Check if virtual environment exists
if (Test-Path "..\venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & "..\venv\Scripts\Activate.ps1"
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv ..\venv
    & "..\venv\Scripts\Activate.ps1"
}

pip install -r requirements.txt
Set-Location ..

Write-Host "✅ All dependencies installed successfully!" -ForegroundColor Green
Write-Host "You can now run 'npm run dev' to start both services" -ForegroundColor Cyan 