@echo off
cd /d Y:\test\Wan2GP
call wan2gp\Scripts\activate.bat

python wgp.py --profile 1 ^
  --advanced ^
  --compile transformer ^
  --tea-cache 1 ^
  --perc-reserved-mem-max 0.1 ^
  --preload 1500 ^
  --t2v-14B ^
  --lora-preset "T2V_acc_movii_detail" ^
  --verbose 2

pause