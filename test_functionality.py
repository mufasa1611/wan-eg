#!/usr/bin/env python3

import subprocess
import sys
import os

print("=== WAN2GP FUNCTIONALITY TEST ===")
print(f"Current directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")

print("\n=== TESTING SCRIPT STARTUP ===")

# Test with basic model selection
print("Testing script with basic T2V model...")
try:
    # Start the script with minimal configuration and capture first 10 seconds of output
    cmd = [sys.executable, 'wgp.py', '--t2v', '--verbose', '1']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                              text=True, bufsize=1, universal_newlines=True)
    
    # Wait a bit for initialization
    import time
    time.sleep(5)
    
    # Check if process is still running (good sign)
    if process.poll() is None:
        print("✓ Script started successfully and is running")
        print("✓ Process ID:", process.pid)
        
        # Try to terminate gracefully
        process.terminate()
        try:
            stdout, stderr = process.communicate(timeout=5)
            if stdout:
                print("Initial output:", stdout[:200])
            if stderr:
                print("Initial errors:", stderr[:200])
        except subprocess.TimeoutExpired:
            process.kill()
            print("Process terminated after timeout")
    else:
        # Process ended, check why
        stdout, stderr = process.communicate()
        print(f"✗ Script exited with code: {process.returncode}")
        if stdout:
            print("Output:", stdout[:500])
        if stderr:
            print("Errors:", stderr[:500])
            
except Exception as e:
    print(f"✗ Error testing script: {e}")

print("\n=== TESTING REQUIREMENTS ===")

# Check if all required models/files are available
required_dirs = ['ckpts', 'outputs', 'settings', 'defaults']
for dir_name in required_dirs:
    if os.path.exists(dir_name):
        print(f"✓ {dir_name}/ directory exists")
    else:
        print(f"⚠ {dir_name}/ directory missing (will be created)")

# Check some key model files
model_files = [
    'ckpts/Wan2.1_VAE.safetensors',
    'ckpts/umt5-xxl/models_t5_umt5-xxl-enc-bf16.safetensors',
    'ckpts/xlm-roberta-large/models_clip_open-clip-xlm-roberta-large-vit-huge-14-bf16.safetensors'
]

for file_path in model_files:
    if os.path.exists(file_path):
        size_mb = os.path.getsize(file_path) / (1024*1024)
        print(f"✓ {file_path} ({size_mb:.1f} MB)")
    else:
        print(f"⚠ {file_path} missing (will be downloaded)")

print("\n=== ANALYSIS COMPLETE ===")
