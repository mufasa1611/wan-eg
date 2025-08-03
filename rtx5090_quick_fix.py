#!/usr/bin/env python3
"""
Simple RTX 5090 Patch Applier for Wan2GP
Run this after any repository update to restore RTX 5090 compatibility
"""

import os
import shutil

def apply_patches():
    """Apply the essential RTX 5090 fixes"""
    
    print("🔧 Applying RTX 5090 Compatibility Fixes...")
    
    # 1. Fix wgp.py syntax error (missing comma)
    print("1. Fixing syntax error in wgp.py...")
    with open("wgp.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Fix missing comma
    content = content.replace(
        '"vace_1.3B" "vace_multitalk_14B"',
        '"vace_1.3B", "vace_multitalk_14B"'
    )
    
    # Fix help string
    content = content.replace(
        'help="% of RAM allocated to Reserved RAM"',
        'help="Percentage of RAM allocated to Reserved RAM"'
    )
    
    # Add RTX 5090 detection
    if "RTX 5090 + PyTorch 2.7 detected" not in content:
        rtx_fix = '''
# RTX 5090 specific: Disable PyTorch compilation due to Triton compatibility issues
try:
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name()
        if "RTX 5090" in device_name and torch.__version__.startswith("2.7"):
            if compile == "transformer":
                print("RTX 5090 + PyTorch 2.7 detected: Disabling transformer compilation")
                compile = ""
except:
    pass
'''
        content = content.replace(
            'compile = server_config.get("compile", "")',
            'compile = server_config.get("compile", "")' + rtx_fix
        )
    
    # Fix LoRA safety
    content = content.replace(
        'if trans is not None: offload.unload_loras_from_model(trans2)',
        'if trans2 is not None: offload.unload_loras_from_model(trans2)'
    )
    
    with open("wgp.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("   ✓ wgp.py patched")
    
    # 2. Fix meta tensor issues in modules
    modules = [
        ("wan/modules/t5.py", "model", "checkpoint_path"),
        ("wan/modules/clip.py", "self.model", 'checkpoint_path.replace(".pth", "-bf16.safetensors")'),
        ("wan/modules/vae.py", "model", 'pretrained_path.replace(".pth", ".safetensors")')
    ]
    
    for i, (filepath, model_var, checkpoint_var) in enumerate(modules, 2):
        print(f"{i}. Fixing meta tensor issue in {filepath}...")
        
        if not os.path.exists(filepath):
            print(f"   ⚠ {filepath} not found, skipping")
            continue
            
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Simple fix: change writable_tensors to True and add error handling
        if "writable_tensors= False" in content:
            content = content.replace("writable_tensors= False", "writable_tensors= True")
            
            # Add meta tensor error handling if not present
            if "Cannot copy out of meta tensor" not in content:
                old_pattern = f"offload.load_model_data({model_var}, {checkpoint_var}, writable_tensors= True )"
                new_pattern = f'''try:
            offload.load_model_data({model_var}, {checkpoint_var}, writable_tensors=True)
        except NotImplementedError as e:
            if "Cannot copy out of meta tensor" in str(e):
                logging.warning("Meta tensor issue detected, attempting alternative loading...")
                try:
                    {model_var} = {model_var}.to_empty(device={"device" if "self." not in model_var else "self.device"})
                except:
                    {model_var} = {model_var}.to({"device" if "self." not in model_var else "self.device"})
                offload.load_model_data({model_var}, {checkpoint_var}, writable_tensors=True)
            else:
                raise'''
                content = content.replace(old_pattern, new_pattern)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"   ✓ {filepath} patched")
    
    print("\n✅ All RTX 5090 patches applied successfully!")
    print("🚀 You can now run the script with: python wgp.py --t2v --listen --server-port 7860")

if __name__ == "__main__":
    if os.path.exists("wgp.py"):
        apply_patches()
    else:
        print("❌ Please run this script from the Wan2GP directory (where wgp.py is located)")
