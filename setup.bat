@echo off
echo Setting up Talkito AI Interview Platform...
echo.

echo [1/4] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created! Please edit it and add your API keys.
) else (
    echo .env file already exists.
)

cd ..

echo.
echo [2/4] Setting up Frontend...
cd frontend\vite-project

echo Installing Node dependencies...
call npm install

cd ..\..

echo.
echo [3/4] Verifying FFmpeg...
if exist ffmpeg-8.0-essentials_build\bin\ffmpeg.exe (
    echo FFmpeg found!
) else (
    echo WARNING: FFmpeg not found in expected location!
)

echo.
echo [4/4] Setup Complete!
echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo 1. Edit backend\.env and add your API keys:
echo    - GEMINI_API_KEY
echo    - ELEVENLABS_API_KEY
echo.
echo 2. Start the backend:
echo    Double-click start-backend.bat
echo.
echo 3. Start the frontend:
echo    Double-click start-frontend.bat
echo.
echo 4. Open http://localhost:5173 in your browser
echo ========================================
echo.
pause
