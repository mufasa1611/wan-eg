#!/usr/bin/env python3
"""
RTX 5090 Compatibility Patch for Wan2GP
Automatically applies RTX 5090 fixes after repository updates
"""

import os
import re
import shutil
from pathlib import Path

def backup_file(filepath):
    """Create a backup of the original file"""
    backup_path = f"{filepath}.rtx5090_backup"
    if not os.path.exists(backup_path):
        shutil.copy2(filepath, backup_path)
        print(f"✓ Backup created: {backup_path}")

def apply_wgp_fixes():
    """Apply fixes to wgp.py"""
    filepath = "wgp.py"
    if not os.path.exists(filepath):
        print(f"✗ {filepath} not found")
        return False
    
    backup_file(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix 1: Missing comma in comp_map
    content = re.sub(
        r'"vace_1\.3B"\s+"vace_multitalk_14B"',
        '"vace_1.3B", "vace_multitalk_14B"',
        content
    )
    
    # Fix 2: Help string formatting
    content = content.replace(
        'help="% of RAM allocated to Reserved RAM"',
        'help="Percentage of RAM allocated to Reserved RAM"'
    )
    
    # Fix 3: RTX 5090 compilation detection
    rtx5090_fix = '''# RTX 5090 specific: Disable PyTorch compilation due to Triton compatibility issues with RTX 5090 + PyTorch 2.7 nightly
try:
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name()
        if "RTX 5090" in device_name and torch.__version__.startswith("2.7"):
            if compile == "transformer":
                print("RTX 5090 + PyTorch 2.7 detected: Disabling transformer compilation to avoid Triton compatibility issues")
                compile = ""
except:
    pass

'''
    
    # Insert RTX 5090 fix after compile = server_config.get("compile", "")
    if "RTX 5090 + PyTorch 2.7 detected" not in content:
        content = re.sub(
            r'(compile = server_config\.get\("compile", ""\)\s*\n)',
            r'\1' + rtx5090_fix,
            content
        )
    
    # Fix 4: LoRA safety check
    content = content.replace(
        'if trans is not None: offload.unload_loras_from_model(trans2)',
        'if trans2 is not None: offload.unload_loras_from_model(trans2)'
    )
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Applied fixes to {filepath}")
        return True
    else:
        print(f"- No changes needed in {filepath}")
        return False

def apply_module_fixes():
    """Apply meta tensor fixes to wan modules"""
    modules = [
        ("wan/modules/t5.py", "T5"),
        ("wan/modules/clip.py", "CLIP"), 
        ("wan/modules/vae.py", "VAE")
    ]
    
    for filepath, module_name in modules:
        if not os.path.exists(filepath):
            print(f"✗ {filepath} not found")
            continue
            
        backup_file(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Meta tensor fix
        meta_tensor_fix = f'''        # Fix for RTX 5090 meta tensor issue - ensure proper tensor initialization
        try:
            offload.load_model_data({"model" if "vae" in filepath else "self.model" if "clip" in filepath else "model"}, {"checkpoint_path" if "t5" in filepath else "checkpoint_path.replace(\".pth\", \"-bf16.safetensors\")" if "clip" in filepath else "pretrained_path.replace(\".pth\", \".safetensors\")"}, writable_tensors=True)
        except NotImplementedError as e:
            if "Cannot copy out of meta tensor" in str(e):
                logging.warning("Meta tensor issue detected in {module_name}, attempting alternative loading...")
                # Use to_empty() for meta tensors as recommended by PyTorch
                try:
                    {"model = model.to_empty(device=device)" if "vae" in filepath or "t5" in filepath else "self.model = self.model.to_empty(device=self.device)"}
                except:
                    # Fallback: try regular to() method
                    {"model = model.to(device)" if "vae" in filepath or "t5" in filepath else "self.model = self.model.to(self.device)"}
                offload.load_model_data({"model" if "vae" in filepath else "self.model" if "clip" in filepath else "model"}, {"checkpoint_path" if "t5" in filepath else "checkpoint_path.replace(\".pth\", \"-bf16.safetensors\")" if "clip" in filepath else "pretrained_path.replace(\".pth\", \".safetensors\")"}, writable_tensors=True)
            else:
                raise'''
        
        # Replace the original load_model_data call
        if "writable_tensors= False" in content and "Meta tensor issue detected" not in content:
            # Pattern for each module type
            if "t5.py" in filepath:
                pattern = r'(\s+from mmgp import offload\s+)offload\.load_model_data\(model,checkpoint_path, writable_tensors= False \)'
                replacement = r'\1' + meta_tensor_fix
            elif "clip.py" in filepath:
                pattern = r'(\s+# self\.model\.load_state_dict\(\s+#     torch\.load\(checkpoint_path, map_location=\'cpu\'\), assign= True\)\s+)offload\.load_model_data\(self\.model, checkpoint_path\.replace\("\.pth", "-bf16\.safetensors"\), writable_tensors= False\)'
                replacement = r'\1' + meta_tensor_fix
            elif "vae.py" in filepath:
                pattern = r'(\s+# offload\.load_model_data\(model, pretrained_path\.replace\("\.pth", "_bf16\.safetensors"\), writable_tensors= False\)\s+)offload\.load_model_data\(model, pretrained_path\.replace\("\.pth", "\.safetensors"\), writable_tensors= False\)'
                replacement = r'\1' + meta_tensor_fix
            
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Applied meta tensor fix to {filepath}")
        else:
            print(f"- No changes needed in {filepath}")

def main():
    print("🔧 Applying RTX 5090 Compatibility Patches...")
    print("=" * 50)
    
    if not os.path.exists("wgp.py"):
        print("✗ Not in Wan2GP directory. Please run this script from the Wan2GP root folder.")
        return
    
    print("📁 Current directory:", os.getcwd())
    print()
    
    # Apply fixes
    print("🔨 Applying main script fixes...")
    apply_wgp_fixes()
    
    print("\n🔨 Applying module fixes...")
    apply_module_fixes()
    
    print("\n" + "=" * 50)
    print("✅ RTX 5090 compatibility patches applied!")
    print("🚀 You can now run: python wgp.py --t2v --listen --server-port 7860")
    print("\n💡 To restore original files, rename .rtx5090_backup files back to original names")

if __name__ == "__main__":
    main()
