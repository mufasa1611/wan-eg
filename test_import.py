#!/usr/bin/env python3
import sys
print(f"Python executable: {sys.executable}")
print(f"Python path: {sys.path}")

try:
    import mmgp
    print(f"mmgp imported successfully from: {mmgp.__file__}")
    from mmgp import offload, safetensors2, profile_type
    print("All mmgp imports successful!")
except ImportError as e:
    print(f"Import error: {e}")
