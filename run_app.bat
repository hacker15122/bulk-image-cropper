@echo off
echo ========================================
echo    AI Bulk Image Cropper Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Checking version...
python --version

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

echo.
echo Installing required packages...
echo This may take a few minutes on first run...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install required packages with latest versions
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install some packages
    echo This might be due to missing Visual C++ build tools
    echo Please install Visual Studio Build Tools or try running as Administrator
    echo.
    echo Alternative: Try installing packages one by one:
    echo pip install Flask opencv-python numpy Pillow mediapipe Werkzeug python-dotenv
    pause
    exit /b 1
)

echo.
echo ========================================
echo    All packages installed successfully!
echo ========================================
echo.

REM Create necessary directories
if not exist "uploads" mkdir uploads
if not exist "cropped_images" mkdir cropped_images
if not exist "templates" mkdir templates

echo Testing setup...
python test_setup.py

if errorlevel 1 (
    echo.
    echo Setup test failed. Please check the errors above.
    pause
    exit /b 1
)

echo.
echo Testing MediaPipe specifically...
python test_mediapipe.py

if errorlevel 1 (
    echo.
    echo MediaPipe test failed. Trying to fix...
    echo.
    pip install mediapipe==0.10.21 --force-reinstall
    echo.
    echo Testing MediaPipe again...
    python test_mediapipe.py
    if errorlevel 1 (
        echo.
        echo MediaPipe still not working. Please check the errors above.
        pause
        exit /b 1
    )
)

echo.
echo Starting the application...
echo.
echo The web interface will open at: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.

REM Start the Flask application
python app.py

pause
