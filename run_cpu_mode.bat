@echo off
REM Create a batch file to run Wan2GP in CPU-only mode
echo Running Wan2GP in CPU-only mode...
echo.

REM Set environment variables to force CPU-only operation
set CUDA_VISIBLE_DEVICES=-1
set USE_CUDA=0
set FORCE_CPU=1

REM Run the main script
python wgp.py %*

echo.
echo Wan2GP execution completed.
