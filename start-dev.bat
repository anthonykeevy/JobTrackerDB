@echo off
echo 🚀 Starting JobTrackerDB Development Environment
echo ==============================================
echo.

REM Check if ports are in use and kill processes
echo Checking for existing processes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do taskkill /f /pid %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173') do taskkill /f /pid %%a >nul 2>&1

echo ✅ Ports cleared
echo.
echo 🎯 Starting Backend (http://127.0.0.1:8000) and Frontend (http://localhost:5173)
echo Press Ctrl+C to stop all services
echo.

REM Start both services using npm
npm run dev 