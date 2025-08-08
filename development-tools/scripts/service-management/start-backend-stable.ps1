# JobTrackerDB Backend Startup Script for PowerShell (Stable Version)
# This script starts the backend without auto-reload to prevent restart issues

Write-Host "🚀 Starting JobTrackerDB Backend (Stable Mode)..." -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green

# Change to backend directory
Set-Location backend

# Set Python path to current directory
$env:PYTHONPATH = "."

# Check if virtual environment is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not detected. Attempting to activate..." -ForegroundColor Yellow
    if (Test-Path "..\venv\Scripts\Activate.ps1") {
        & "..\venv\Scripts\Activate.ps1"
        Write-Host "✅ Virtual environment activated" -ForegroundColor Green
    } else {
        Write-Host "❌ Virtual environment not found at ..\venv\Scripts\Activate.ps1" -ForegroundColor Red
        Write-Host "Please ensure you have a virtual environment set up" -ForegroundColor Yellow
        exit 1
    }
}

# Check if requirements are installed
if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ requirements.txt not found in backend directory" -ForegroundColor Red
    exit 1
}

Write-Host "📦 Installing/updating dependencies..." -ForegroundColor Blue
pip install -r requirements.txt

Write-Host "🔧 Starting FastAPI server (Stable Mode - No Auto-Reload)..." -ForegroundColor Cyan
Write-Host "Backend will be available at: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "API Documentation: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "Note: Manual restart required for code changes" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server without reload for stability
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
