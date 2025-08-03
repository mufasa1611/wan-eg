import os
import sys
import subprocess

# Set environment variables to:
# 1. Force CPU mode
# 2. Disable CUDA to prevent CUDA compatibility checks
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Now run the original script with all arguments passed through
script_args = ["python", "wgp.py"] + sys.argv[1:]
subprocess.run(script_args)
