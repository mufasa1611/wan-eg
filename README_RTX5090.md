# Wan2GP RTX 5090 Optimized

This is an optimized version of Wan2GP specifically tuned for RTX 5090 systems with high RAM configurations.

## RTX 5090 Optimizations

### Performance Improvements
- **Early Memory Management**: 70% RAM reservation (65.6GB of 94GB) for optimal model loading
- **Aggressive Preload**: 24GB VRAM preload for cocktail models (3-file loading)
- **Global PyTorch Acceleration**: TF32, CuDNN benchmark, aggressive memory management
- **Cocktail Model Speed**: Optimized loading sequence for complex multi-file models

### Features
- **RTX 5090 Auto-Detection**: Automatic hardware detection and optimization
- **Memory Pressure Relief**: Advanced memory management for 14B+ models
- **Loading Time Tracking**: Performance monitoring and reporting
- **Profile Auto-Selection**: Optimal configuration based on hardware

### Hardware Requirements
- RTX 5090 32GB VRAM
- 96GB+ System RAM
- PyTorch 2.7.0+cu128 (CUDA 12.8)

### Key Optimizations Applied
1. **Early Memory Override**: Forces 70% memory reservation before model loading
2. **Cocktail Model Optimization**: 24GB preload for 3-file models vs 16GB for single models  
3. **PyTorch Acceleration**: TF32, CuDNN benchmark, high precision matmul
4. **Budget Multipliers**: 1.5x memory budgets for multi-file models
5. **Loading Performance**: Real-time loading speed reporting

### Usage
```bash
python wgp.py  # Auto-detects RTX 5090 and applies optimizations
```

### Configuration
The optimized configuration in `wgp_config.json` includes:
- `preload_in_VRAM: 24576` (24GB preload)
- `preload_model_policy: ["transformer", "text_encoder", "vae", "transformer2"]`
- Automatic cocktail model detection and optimization

## Original Project
Based on [DeepBeepMeep/Wan2GP](https://github.com/deepbeepmeep/Wan2GP)

## Performance Results
- **Loading Speed**: Optimized for cocktail model 3-file loading
- **Memory Efficiency**: 70% RAM utilization with RTX 5090
- **VRAM Management**: 24GB aggressive preload for maximum speed

---
*Optimized by Assistant for RTX 5090 + 96GB RAM systems*
