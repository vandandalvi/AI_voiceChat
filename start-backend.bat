@echo off
echo Starting Talkito Backend Server...
echo.

cd backend

if not exist venv (
    echo Virtual environment not found. Creating one...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/Updating dependencies...
pip install -r requirements.txt

echo.
echo Checking for .env file...
if not exist .env (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your API keys.
    echo.
    pause
    exit
)

echo.
echo Starting Flask server on http://localhost:5000
echo.
python app.py
