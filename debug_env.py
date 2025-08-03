#!/usr/bin/env python3

import os
import sys

print("=== ENVIRONMENT DEBUG ===")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path[:3]}...")  # First 3 entries

print("\n=== CHECKING MODULES ===")

# Check conda environment
try:
    import conda
    print("✓ Running in conda environment")
except ImportError:
    print("- Not in conda environment")

# Check mmgp
try:
    import mmgp
    print(f"✓ mmgp found at: {mmgp.__file__}")
    from mmgp import offload, safetensors2, profile_type
    print("✓ mmgp submodules imported successfully")
except Exception as e:
    print(f"✗ mmgp error: {e}")

# Check torch
try:
    import torch
    print(f"✓ PyTorch {torch.__version__}")
    print(f"  CUDA: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"  GPU: {torch.cuda.get_device_name()}")
except Exception as e:
    print(f"✗ PyTorch error: {e}")

# Check wan module
try:
    sys.path.insert(0, os.getcwd())  # Add current directory
    import wan
    print(f"✓ wan module found at: {wan.__file__}")
    print(f"  wan contents: {dir(wan)}")
except Exception as e:
    print(f"✗ wan error: {e}")

print("\n=== FILE CHECKS ===")
print(f"wgp.py exists: {os.path.exists('wgp.py')}")
print(f"wgp.py size: {os.path.getsize('wgp.py') if os.path.exists('wgp.py') else 'N/A'} bytes")

# Try to compile wgp.py
try:
    with open('wgp.py', 'r', encoding='utf-8') as f:
        code = f.read()
    compile(code, 'wgp.py', 'exec')
    print("✓ wgp.py compiles without syntax errors")
except Exception as e:
    print(f"✗ wgp.py compilation error: {e}")

print("\n=== ENVIRONMENT ANALYSIS COMPLETE ===")

# Quick script execution test
print("\n=== TESTING BASIC WGP EXECUTION ===")
try:
    # This will test if the script can at least be imported
    import subprocess
    result = subprocess.run([sys.executable, '-c', 'import argparse; print("argparse OK")'], 
                          capture_output=True, text=True, cwd=os.getcwd())
    print(f"Basic subprocess test: {result.stdout.strip()}")
    
    # Test help specifically
    result = subprocess.run([sys.executable, 'wgp.py', '--help'], 
                          capture_output=True, text=True, cwd=os.getcwd())
    if result.returncode == 0:
        print("✓ wgp.py --help works")
        first_line = result.stdout.split('\n')[0]
        print(f"  First line: {first_line}")
    else:
        print(f"✗ wgp.py --help failed: {result.stderr[:200]}")
        
except Exception as e:
    print(f"✗ Subprocess test error: {e}")
