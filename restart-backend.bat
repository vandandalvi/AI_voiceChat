@echo off
echo ========================================
echo Restarting Backend with Whisper
echo ========================================
echo.

cd backend

echo Stopping any running Python processes...
taskkill /F /IM python.exe 2>nul

echo.
echo Starting backend server...
echo.
python app.py

pause
