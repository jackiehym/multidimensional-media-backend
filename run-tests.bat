@echo off
chcp 65001 >nul
REM set color
echo ====================================
echo      Backend API Test Script      
echo ====================================
echo.

REM check python
python --version >nul 2>&1
if %errorlevel% neq 0 (
echo Error: Python not found. Please make sure Python is installed and added to system path.
pause
exit /b 1
)

REM check pytest 
python -m pytest --version >nul 2>&1
if %errorlevel% neq 0 (
echo Installing test dependencies...
pip install -r requirements-dev.txt
if %errorlevel% neq 0 (
echo Error: Failed to install test dependencies.
pause
exit /b 1
)
)

echo Running tests...
echo.

REM run all test
python -m pytest tests/ -v

if %errorlevel% eq 0 (
echo.
echo ====================================
echo Tests passed! All API endpoints are working correctly.
echo ====================================
) else (
echo.
echo ====================================
echo Tests failed! Please check error messages.
echo ====================================
)

echo.
echo Press any key to close this window...
pause >nul
