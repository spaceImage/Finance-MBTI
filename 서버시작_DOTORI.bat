@echo off
title DOTORI Diagnosis PoC - Server Start
echo ==================================================
echo   Starting DOTORI Financial Diagnosis System...
echo ==================================================
echo [Backend]  FastAPI (http://localhost:8001)
echo [Frontend] React UI (http://localhost:3001)
echo ==================================================

cd /d "%~dp0"

:: Start FastAPI Backend on Port 8001
start "DOTORI Backend (Port 8001)" cmd /k "python backend\app\main.py"

:: Start Frontend on Port 3001
start "DOTORI Frontend (Port 3001)" cmd /k "cd frontend && cmd /c npm run dev"

echo.
echo DOTORI servers are starting!
echo Opening http://localhost:3001 in your browser...
timeout /t 3 >nul
start "" http://localhost:3001
