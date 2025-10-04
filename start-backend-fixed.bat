@echo off
echo Starting Talkito Backend with gTTS fallback...
echo.

cd backend

call venv\Scripts\activate.bat

echo.
echo ========================================
echo Using FREE Google Text-to-Speech (gTTS)
echo ElevenLabs is bypassed due to API issues
echo ========================================
echo.
echo Starting Flask server on http://localhost:5000
echo.

python app_test.py
