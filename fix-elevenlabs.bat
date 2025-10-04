@echo off
echo ========================================
echo FIXING ELEVENLABS API ISSUE
echo ========================================
echo.
echo The issue: ElevenLabs blocked your API key
echo The solution: Using FREE Google TTS instead
echo.

cd backend

echo [1/3] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo [2/3] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [3/3] Configuration updated...
echo USE_GTTS_FALLBACK=true is set in .env
echo.

echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Now run: start-backend-fixed.bat
echo.
pause
