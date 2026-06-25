@echo off
title AuraShop Local Server
echo ===================================================
echo             AURASHOP DEVELOPER UTILITY
echo ===================================================
echo.

if not exist venv (
    echo [ERROR] Virtual environment 'venv' not found.
    echo Please execute setup.bat first to initialize the project environment.
    echo.
    pause
    exit /b
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Launching Django server...
echo Point your browser to: http://127.0.0.1:8000/
echo.
python manage.py runserver

if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Server halted with error code: %errorlevel%
    pause
)
