@echo off
echo ================================
echo RTX 5090 Compatibility Patcher
echo ================================
echo.
echo This will apply RTX 5090 fixes after repository updates
echo.
pause

echo Applying patches...
python rtx5090_quick_fix.py

echo.
echo ================================
echo Patch process completed!
echo ================================
pause
