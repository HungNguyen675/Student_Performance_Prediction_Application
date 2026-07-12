@echo off
echo ===================================================
echo   STUDENT PERFORMANCE PREDICTION APP - STARTUP
echo ===================================================
echo.

echo [0] Checking and installing Python dependencies...
call pip install -r requirements.txt

echo.
echo [1] Starting FastAPI Backend on port 8000...
start cmd /k "python main.py"

echo.
echo [2] Checking and installing Node dependencies...
cd frontend
IF NOT EXIST "node_modules\" (
    echo "node_modules not found. Running npm install to download packages..."
    call npm install
)

echo.
echo [3] Starting React Vite Frontend...
start cmd /k "npm run dev"

echo.
echo ===================================================
echo Servers are starting up! 
echo - Backend will be available at: http://localhost:8000
echo - Frontend will be available at: http://localhost:5173
echo ===================================================
echo.
pause
