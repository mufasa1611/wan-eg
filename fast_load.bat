@echo off
echo Starting WanGP with FAST single-file model (15-second loading like Pinokio)
echo.
echo RTX 5090 optimizations preserved:
echo - 75%% memory reservation 
echo - 16GB preload for 14B models
echo - Profile 1 auto-selection
echo - PyTorch optimizations enabled
echo.
python wgp.py --t2v-14B --perc-reserved-mem-max 0.75
pause
