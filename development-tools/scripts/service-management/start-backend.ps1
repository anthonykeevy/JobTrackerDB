# JobTrackerDB Backend Startup Script for PowerShell
# This script properly handles Python path and environment variables

Write-Host "🚀 Starting JobTrackerDB Backend..." -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

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

Write-Host "🔧 Starting FastAPI server..." -ForegroundColor Cyan
Write-Host "Backend will be available at: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "API Documentation: http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the server with more stable reload configuration
python -m uvicorn app.main:app --reload --reload-dir app --reload-exclude "*.pyc" --reload-exclude "__pycache__" --reload-exclude "*.tmp" --host 127.0.0.1 --port 8000 