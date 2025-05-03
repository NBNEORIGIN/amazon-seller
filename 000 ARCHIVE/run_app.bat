@echo off
REM Set WinPython as the Python environment
set WINPYDIR=%~dp0WPy64-31011
set PATH=%WINPYDIR%\python-3.10.11.amd64;%WINPYDIR%\python-3.10.11.amd64\Scripts;%PATH%

REM Create virtual environment if it doesn't exist
if not exist venv (
    python -m venv venv
)
REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements
pip install --upgrade pip
pip install -r requirements.txt

REM Run the Streamlit app
streamlit run app.py
pause