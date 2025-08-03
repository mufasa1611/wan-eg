#!/usr/bin/env python
"""
RTX 5090 Compatibility Script for Wan2GP
This script enables CUDA JIT compilation for the RTX 5090 GPU architecture.
"""

import os
import sys
import subprocess

# Set environment variables for RTX 5090 support
os.environ["TORCH_CUDA_ARCH_LIST"] = "8.0;8.6;8.9;9.0;12.0" # Add sm_120 architecture
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"  # Better error reporting
os.environ["TORCH_USE_CUDA_DSA"] = "1"    # Enable device-side assertions for better debugging

# Enable JIT compilation for unsupported architectures
os.environ["PYTORCH_JIT_USE_NNC_NOT_NVFUSER"] = "1"
os.environ["TORCH_NVFUSER_DISABLE_FALLBACK"] = "0"
os.environ["TORCH_COMPILE_DISABLE_CUDA_KERNEL_CACHE"] = "0"  # Enable kernel caching

# Improve compatibility
os.environ["TORCH_ALLOW_UNSUPPORTED_GPU"] = "1"
os.environ["TORCH_COMPILE_ALLOW_UNSUPPORTED_GPU"] = "1"

print(f"Running Wan2GP with optimized settings for RTX 5090...")

# Run the original script with all arguments
cmd = [sys.executable, "-m", "torch.utils.run_with_custom_arch", "12.0", "wgp.py"] + sys.argv[1:]
subprocess.run(cmd)
