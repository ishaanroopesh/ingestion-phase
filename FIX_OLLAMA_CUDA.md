# Fixing Ollama CUDA Memory Allocation Error

## Problem
```
Error: 500 Internal Server Error: llama runner process has terminated: error loading model: unable to allocate CUDA0 buffer
```

This means Ollama is trying to use GPU memory but there isn't enough available.

## Solutions (Try in Order)

### Solution 1: Run Ollama in CPU Mode (Easiest)

Force Ollama to use CPU instead of GPU:

**Windows:**
```bash
set OLLAMA_NUM_GPU=0
ollama serve
```

**Linux/Mac:**
```bash
export OLLAMA_NUM_GPU=0
ollama serve
```

Then test:
```bash
ollama run llama3 "Hello, test"
```

### Solution 2: Free Up GPU Memory

**Check what's using GPU:**
```bash
# Windows (if you have nvidia-smi)
nvidia-smi

# Or check Task Manager > Performance > GPU
```

**Close other applications using GPU:**
- Close any PyTorch/TensorFlow processes
- Close other AI applications
- Close video games or GPU-intensive apps
- Restart your computer if needed

### Solution 3: Use a Smaller Model

If LLaMA 3 is too large, try a smaller model:

```bash
# Try llama3:8b (8 billion parameters, smaller)
ollama pull llama3:8b

# Or try other smaller models
ollama pull llama3.2:1b
ollama pull llama3.2:3b
```

Then update your config to use the smaller model.

### Solution 4: Reduce Model Context Size

Limit the GPU memory used by setting environment variables:

**Windows:**
```bash
set OLLAMA_NUM_GPU=1
set OLLAMA_MAX_LOADED_MODELS=1
ollama serve
```

**Linux/Mac:**
```bash
export OLLAMA_NUM_GPU=1
export OLLAMA_MAX_LOADED_MODELS=1
ollama serve
```

### Solution 5: Restart Everything

1. **Stop all Ollama processes:**
   ```bash
   # Windows: Open Task Manager and end ollama.exe processes
   # Or use:
   taskkill /F /IM ollama.exe
   ```

2. **Restart Ollama:**
   ```bash
   ollama serve
   ```

3. **Test again:**
   ```bash
   ollama run llama3 "Hello, test"
   ```

## Recommended Quick Fix

**For immediate use, run in CPU mode:**

1. **Stop current Ollama** (Ctrl+C in the terminal running `ollama serve`)

2. **Set environment variable and restart:**
   
   **Windows Command Prompt:**
   ```cmd
   set OLLAMA_NUM_GPU=0
   ollama serve
   ```
   
   **Windows PowerShell:**
   ```powershell
   $env:OLLAMA_NUM_GPU=0
   ollama serve
   ```

3. **Test:**
   ```bash
   ollama run llama3 "Hello, test"
   ```

**Note:** CPU mode will be slower but will work reliably. For production, you may want to optimize GPU memory usage later.

## Make CPU Mode Permanent

To always use CPU mode, you can:

1. **Create a batch file** (`start_ollama_cpu.bat`):
   ```batch
   @echo off
   set OLLAMA_NUM_GPU=0
   ollama serve
   ```

2. **Or set it in system environment variables:**
   - Windows: System Properties > Environment Variables
   - Add: `OLLAMA_NUM_GPU` = `0`

## Check Your System

**Check GPU memory:**
```bash
nvidia-smi
```

**Check available RAM:**
- LLaMA 3 needs at least 8GB RAM for CPU mode
- More is better for performance

## Update Your Application

If you switch to CPU mode or a different model, you may need to update:

1. **Model name in config** (if using smaller model)
2. **No changes needed** if just switching GPU to CPU

The application will work the same, just potentially slower in CPU mode.

