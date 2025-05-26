@echo off
echo ========================================
echo ParaDocs Case Management System Launcher
echo ========================================
echo.
echo Available Options:
echo 1. Master Index (MAIN HUB)
echo 2. Comprehensive EEO Investigation
echo 3. Timeline-Enhanced Dashboard
echo 4. Master Dashboard
echo 5. Enhanced Analysis System
echo 6. Original Document Index
echo.

:: Get the current directory
set CURRENT_DIR=%~dp0

:: Open Master Index by default
echo Opening ParaDocs Master Index...
start "" "%CURRENT_DIR%MASTER_INDEX.html"

echo.
echo ✓ Master Index opened!
echo.
echo This is your main hub with:
echo - $2.27M Total Damages tracked
echo - 1,340 Days of violations
echo - 8 Federal violations documented
echo - 24+ Analysis tools
echo - Links to all dashboards
echo - Search functionality
echo.
echo Other interfaces available:
echo - Legal Strategy Dashboard: %CURRENT_DIR%paradocs_legal_strategy_dashboard.html
echo - Comprehensive Investigation: %CURRENT_DIR%paradocs_comprehensive_eeo_investigation.html
echo - Timeline Dashboard: %CURRENT_DIR%paradocs_master_timeline_enhanced.html
echo - Master Dashboard: %CURRENT_DIR%paradocs_master_dashboard.html
echo - Enhanced System: %CURRENT_DIR%paradocs-enhanced.html
echo - Original Index: %CURRENT_DIR%paradocs-index.html
echo.
echo Data files:
echo - eeo_comprehensive_investigation.json
echo - eeo_comprehensive_timeline.csv
echo - eeo_investigation_questions.csv
echo.
pause 