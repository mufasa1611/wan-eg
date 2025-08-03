# RTX 5090 Update Management Guide

## The Problem
You've manually modified several files to make Wan2GP work with RTX 5090. When you pull updates from the repository, these changes will be overwritten and you'll get the "Cannot copy out of meta tensor" errors again.

## Solutions

### 🎯 **Recommended Solution: Quick Patch Script**

I've created `rtx5090_quick_fix.py` that will automatically reapply all RTX 5090 fixes after any update.

**Usage after each update:**
```bash
# 1. Pull the latest updates
git pull origin main

# 2. Apply RTX 5090 fixes
python rtx5090_quick_fix.py

# 3. Run the script
python wgp.py --t2v --listen --server-port 7860
```

Or simply double-click `apply_rtx5090_fix.bat` on Windows.

### 📋 **What the Patch Script Fixes:**

1. **Syntax Errors**:
   - Missing comma in line 1752
   - Argument parser formatting issue

2. **RTX 5090 Meta Tensor Issues**:
   - Changes `writable_tensors=False` to `writable_tensors=True`
   - Adds proper error handling with `to_empty()` fallback
   - Applies to: `wan/modules/t5.py`, `wan/modules/clip.py`, `wan/modules/vae.py`

3. **RTX 5090 Triton Compatibility**:
   - Auto-detects RTX 5090 + PyTorch 2.7
   - Automatically disables PyTorch compilation to prevent Triton crashes

4. **Memory Safety**:
   - Fixes LoRA unloading null pointer issues

### 🔄 **Update Workflow**

```bash
# Step 1: Check for updates
git fetch origin

# Step 2: See what changed
git log HEAD..origin/main --oneline

# Step 3: Pull updates
git pull origin main

# Step 4: Apply RTX 5090 fixes
python rtx5090_quick_fix.py

# Step 5: Test the script
python wgp.py --t2v --verbose 1
```

### 🛡️ **Alternative Solutions**

#### Option A: Git Branch Strategy
```bash
# Create a local branch for your RTX 5090 fixes
git checkout -b rtx5090-fixes

# After updates:
git checkout main
git pull origin main
git checkout rtx5090-fixes
git rebase main
# Resolve any conflicts manually
```

#### Option B: Git Stash Strategy
```bash
# Before pulling updates:
git stash push -m "RTX 5090 fixes"

# After pulling:
git pull origin main
git stash pop

# If conflicts occur:
python rtx5090_quick_fix.py
```

#### Option C: Fork the Repository
1. Fork the Wan2GP repository on GitHub
2. Apply your RTX 5090 fixes to your fork
3. Pull updates from upstream and merge with your fixes

### 🔍 **Monitoring for Conflicts**

Files to watch for changes in future updates:
- `wgp.py` (main script)
- `wan/modules/t5.py` (text encoder)
- `wan/modules/clip.py` (CLIP encoder)  
- `wan/modules/vae.py` (VAE decoder)

### 📝 **Manual Fix Reference**

If the patch script fails, here are the manual fixes:

**wgp.py:**
- Line ~1752: Add comma between `"vace_1.3B"` and `"vace_multitalk_14B"`
- Line ~1474: Change `help="% of RAM"` to `help="Percentage of RAM"`
- After line with `compile = server_config.get("compile", "")`: Add RTX 5090 detection code
- Line ~4788: Change `if trans is not None:` to `if trans2 is not None:`

**wan/modules/*.py:**
- Change all `writable_tensors=False` to `writable_tensors=True`
- Wrap `offload.load_model_data()` calls in try-catch with `to_empty()` fallback

### ✅ **Validation**

After applying patches, verify:
1. `python wgp.py --help` works without errors
2. Script starts without "Cannot copy out of meta tensor" errors
3. Web interface loads at http://localhost:7860
4. Video generation completes successfully

### 🆘 **If Something Goes Wrong**

1. **Restore from backup**: The patch script creates `.backup` files
2. **Reset to clean state**: 
   ```bash
   git checkout HEAD -- .
   python rtx5090_quick_fix.py
   ```
3. **Ask for help**: Contact me with the specific error message

---

**Remember**: Run `python rtx5090_quick_fix.py` after every repository update to maintain RTX 5090 compatibility!
