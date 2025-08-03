#!/usr/bin/env python3

print("Starting import test...")

try:
    from mmgp import offload, safetensors2, profile_type
    print("✓ mmgp imports successful")
except Exception as e:
    print(f"✗ mmgp import failed: {e}")

try:
    import wan
    print("✓ wan module imported")
except Exception as e:
    print(f"✗ wan import failed: {e}")

try:
    import torch
    print(f"✓ PyTorch {torch.__version__} with CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  CUDA version: {torch.version.cuda}")
        print(f"  Device count: {torch.cuda.device_count()}")
        print(f"  Current device: {torch.cuda.current_device()}")
        print(f"  Device name: {torch.cuda.get_device_name()}")
except Exception as e:
    print(f"✗ PyTorch import/info failed: {e}")

try:
    import gradio as gr
    print(f"✓ Gradio {gr.__version__} imported")
except Exception as e:
    print(f"✗ Gradio import failed: {e}")

print("Import test completed.")
