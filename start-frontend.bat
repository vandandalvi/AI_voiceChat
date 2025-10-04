@echo off
echo Starting Talkito Frontend...
echo.

cd frontend\vite-project

if not exist node_modules (
    echo Node modules not found. Installing...
    npm install
)

echo.
echo Starting Vite dev server...
echo Frontend will be available at http://localhost:5173
echo.
npm run dev
