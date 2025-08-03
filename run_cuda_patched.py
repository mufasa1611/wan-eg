import os
import sys
import subprocess
import torch
import types

# Original get_device_capability function
original_get_device_capability = torch.cuda.get_device_capability

# Override the device capability function to report a compatible architecture
def patched_get_device_capability(device=None):
    # Return compute capability 8.0 (Ampere) which is compatible with PyTorch
    return (8, 0)

# Apply the monkey patch
torch.cuda.get_device_capability = patched_get_device_capability

# Set environment variable to tell other parts of the code we're using CUDA
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Now run the original script with all arguments passed through
script_args = ["python", "wgp.py"] + sys.argv[1:]
subprocess.run(script_args)
