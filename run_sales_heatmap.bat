@echo off
REM Batch file to run the Amazon sales heatmap generator script

REM Activate virtual environment if needed (uncomment and set path if using venv)
REM call "venv\Scripts\activate.bat"

REM Run the Python script
"C:\Users\zentu\AppData\Local\Programs\Python\Python311\python.exe" "generate_amazon_sales_heatmap.py"
pause

pause
