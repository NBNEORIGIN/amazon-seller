@echo off
echo Starting Memorial Processor...
echo.

:: Check if Python is installed and show the version
echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo.
echo Running memorial processor script...
echo.

:: Run the main script and capture any errors
python main.py 2>&1

echo.
if errorlevel 1 (
    echo Script encountered an error!
) else (
    echo Script completed!
)

echo.
echo Press any key to exit...
pause >nul