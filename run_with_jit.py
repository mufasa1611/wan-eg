import os
import sys
import torch

# Enable JIT compilation for CUDA kernels - this allows PyTorch to compile kernels for your specific GPU
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"

# Set environment variables to enable verbose CUDA error reporting
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"

# Print system information
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA version: {torch.version.cuda}")
if torch.cuda.is_available():
    print(f"CUDA device: {torch.cuda.get_device_name(0)}")
    try:
        capability = torch.cuda.get_device_capability(0)
        print(f"CUDA compute capability: {capability[0]}.{capability[1]}")
    except Exception as e:
        print(f"Error getting capability: {e}")

# Set an environment variable to make PyTorch attempt to JIT-compile for unsupported architectures
os.environ["TORCH_ALLOW_UNSUPPORTED_GPU"] = "1"
os.environ["TORCH_COMPILE_ALLOW_UNSUPPORTED_GPU"] = "1"
os.environ["TORCH_COMPILE_FALLBACK"] = "1"

# Run the main wgp.py script with all arguments
script_args = ["python", "wgp.py"] + sys.argv[1:]
import subprocess
subprocess.run(script_args)
