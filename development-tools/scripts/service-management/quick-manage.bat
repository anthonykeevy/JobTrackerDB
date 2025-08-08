@echo off
echo JobTrackerDB Service Management
echo =============================
echo.
echo Available commands:
echo   start   - Start services
echo   stop    - Stop services  
echo   restart - Restart services
echo   status  - Check service status
echo   cleanup - Clean up all processes
echo.

if "%1"=="" (
    echo Usage: quick-manage.bat [command]
    echo Example: quick-manage.bat status
    goto :end
)

powershell -ExecutionPolicy Bypass -File manage-services.ps1 %1

:end
pause
