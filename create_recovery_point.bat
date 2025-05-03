@echo off
REM Change directory to the project folder
cd /d "G:\My Drive\003 APPS\002 AmazonSeller"

REM Activate virtual environment if you use one
REM call .venv\Scripts\activate

REM Run the recovery point script
python create_recovery_point.py

pause