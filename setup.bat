@echo off
title AuraShop Setup Environment
echo ===================================================
echo             AURASHOP DJANGO SETUP ENGINE
echo ===================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.10+ and select "Add Python to PATH" during setup.
    pause
    exit /b
)

echo [1/5] Building virtual environment (venv)...
:: Delete corrupted venv if it exists
if exist venv (
    echo Cleaning existing virtual environment...
    rmdir /s /q venv
)
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b
)

echo [2/5] Activating virtual environment and installing packages...
call venv\Scripts\activate
:: Use python -m pip to avoid locking executables on Windows
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Package installations failed.
    pause
    exit /b
)

echo [3/5] Compiling database migrations...
python manage.py makemigrations store
python manage.py migrate
if %errorlevel% neq 0 (
    echo [ERROR] Database migrations failed.
    pause
    exit /b
)

echo [4/5] Seeding high-quality product catalog...
python populate_db.py
if %errorlevel% neq 0 (
    echo [WARNING] Database seeding script encountered issues.
)

echo.
echo [5/5] Creating Administrator Account...
echo If you would like to manage products and checkorders in the Admin Panel,
echo please create a superuser account now. Otherwise, press Ctrl+C to skip.
echo.
python manage.py createsuperuser

echo.
echo ===================================================
echo   AURASHOP COMPLETED SETUP SUCCESSFULLY!
echo ===================================================
echo   To launch the local web server, run: run.bat
echo   Then view in browser: http://127.0.0.1:8000/
echo ===================================================
echo.
pause
