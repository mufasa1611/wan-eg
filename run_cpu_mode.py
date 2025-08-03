#!/usr/bin/env python
"""
CPU-only mode runner for Wan2GP
This script forces Wan2GP to run in CPU-only mode by setting the appropriate environment variables
before importing torch or running the main script.
"""

import os
import sys
import subprocess

# Force CPU-only mode
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["USE_CUDA"] = "0"
os.environ["FORCE_CPU"] = "1"

print("Running Wan2GP in CPU-only mode...")

# Run the main script with all arguments passed through
cmd = [sys.executable, "wgp.py"] + sys.argv[1:]
subprocess.run(cmd)
