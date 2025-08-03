@echo off
echo Testing Wan2GP script functionality...
echo.
echo Current directory: %CD%
echo Python version:
python --version
echo.
echo Testing imports:
python test_imports.py
echo.
echo Testing script compilation:
python -c "compile(open('wgp.py').read(), 'wgp.py', 'exec'); print('wgp.py compiles OK')"
echo.
echo Testing script help:
python wgp.py --help
echo.
pause
