"""
Advanced CPU-only mode runner for Wan2GP
This script forces Wan2GP to run in CPU-only mode by disabling CUDA completely
and applying various monkey patches to ensure compatibility.
"""

import os
import sys
import importlib.util
import builtins
import types

# First, disable CUDA completely
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Create a backup of the original import function
original_import = builtins.__import__

# Define a custom import function that modifies torch.cuda behavior
def custom_import(name, *args, **kwargs):
    module = original_import(name, *args, **kwargs)
    
    # If importing torch, modify its cuda module
    if name == 'torch':
        # Create a fake device_capability function that returns a supported architecture
        def fake_get_device_capability(*args, **kwargs):
            return (8, 0)  # Return compute capability 8.0 (Ampere)
        
        # Create a fake is_available function that always returns False
        def fake_is_available(*args, **kwargs):
            return False
        
        # Create a fake get_device_properties function
        def fake_get_device_properties(*args, **kwargs):
            class FakeDeviceProperties:
                def __init__(self):
                    self.name = "CPU (CUDA disabled)"
                    self.total_memory = 8 * 1024 * 1024 * 1024  # 8GB
                    self.major = 8
                    self.minor = 0
            return FakeDeviceProperties()
        
        # Create a fake current_device function
        def fake_current_device(*args, **kwargs):
            raise RuntimeError("CUDA not available")
        
        # Replace the real functions with our fake ones
        module.cuda.get_device_capability = fake_get_device_capability
        module.cuda.is_available = fake_is_available
        module.cuda.get_device_properties = fake_get_device_properties
        module.cuda.current_device = fake_current_device
        
        # Create a fake CUDA context manager
        class FakeCUDADeviceContextManager:
            def __init__(self, *args, **kwargs):
                pass
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
        
        # Replace device context manager
        module.cuda.device = FakeCUDADeviceContextManager
    
    return module

# Replace the built-in import function with our custom one
builtins.__import__ = custom_import

print("Running Wan2GP in forced CPU-only mode with CUDA disabled...")

# Run the main script with all arguments passed through
import subprocess
cmd = [sys.executable, "wgp.py"] + sys.argv[1:]
subprocess.run(cmd)
