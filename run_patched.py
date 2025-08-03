import os
import sys
import subprocess
import types

# First, apply our monkey patches before importing torch to avoid any issues
def apply_monkey_patches():
    # Patch 1: Override torch.cuda.get_device_capability
    import torch
    original_get_device_capability = torch.cuda.get_device_capability
    
    def patched_get_device_capability(device=None):
        # Return compute capability 8.0 (Ampere) which is compatible with PyTorch
        return (8, 0)
    
    torch.cuda.get_device_capability = patched_get_device_capability
    
    # Patch 2: Override torch.cuda.current_device to work even without CUDA
    original_current_device = torch.cuda.current_device
    
    def patched_current_device():
        # If no CUDA device is available, return device 0 anyway
        try:
            return original_current_device()
        except:
            return 0
    
    torch.cuda.current_device = patched_current_device
    
    # Patch 3: Override torch.cuda.is_available to always return True
    original_is_available = torch.cuda.is_available
    
    def patched_is_available():
        return True
    
    # We'll actually keep the real is_available function as we want to check it later
    # torch.cuda.is_available = patched_is_available
    
    # Patch 4: Override torch.cuda.get_device_properties
    original_get_device_properties = torch.cuda.get_device_properties
    
    def patched_get_device_properties(device=None):
        try:
            return original_get_device_properties(device)
        except:
            # Create a mock device properties object with required attributes
            class MockDeviceProperties:
                def __init__(self):
                    self.name = "Virtual RTX GPU"
                    self.total_memory = 8 * 1024 * 1024 * 1024  # 8GB
                    self.major = 8
                    self.minor = 0
            
            return MockDeviceProperties()
    
    torch.cuda.get_device_properties = patched_get_device_properties

# Apply monkey patches
apply_monkey_patches()

# Set environment variable to control CUDA visibility
# Uncomment the line below to use CPU-only mode
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# If we have a real CUDA GPU, try to use it, otherwise use CPU mode
import torch
if not torch.cuda.is_available():
    print("No CUDA GPU available, running in CPU-only mode")
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
else:
    print(f"CUDA GPU available: {torch.cuda.get_device_name(0)}")
    # Leave CUDA_VISIBLE_DEVICES untouched to use the available GPU

# Now run the original script with all arguments passed through
script_args = ["python", "wgp.py"] + sys.argv[1:]
subprocess.run(script_args)
