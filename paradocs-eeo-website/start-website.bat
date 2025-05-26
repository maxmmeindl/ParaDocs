@echo off
echo.
echo ====================================
echo Starting ParaDocs EEO Website
echo ====================================
echo.

echo Installing frontend dependencies...
cd frontend
call npm install

echo.
echo Starting the development server...
echo.
echo The website will open at http://localhost:5173
echo Press Ctrl+C to stop the server
echo.

call npm run dev

pause 