import os
import platform
import multiprocessing
from typing import Dict, Any

def get_hardware_info() -> Dict[str, Any]:
    """Detect hardware resources and GPU availability."""
    cpu_count = multiprocessing.cpu_count()
    system_os = platform.system()
    
    # Check GPU / CUDA via PyTorch
    cuda_available = False
    device_name = "CPU"
    gpu_count = 0
    
    try:
        import torch
        cuda_available = torch.cuda.is_available()
        if cuda_available:
            gpu_count = torch.cuda.device_count()
            device_name = torch.cuda.get_device_name(0)
    except Exception:
        pass

    # Approximate memory
    total_ram_gb = 8.0
    try:
        import psutil
        total_ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 2)
    except Exception:
        # Fallback heuristic
        if system_os == "Windows":
            total_ram_gb = 16.0
            
    return {
        "cpu_count": cpu_count,
        "cuda_available": cuda_available,
        "device_name": device_name,
        "gpu_count": gpu_count,
        "total_ram_gb": total_ram_gb,
        "os": system_os,
        "platform": platform.platform()
    }

def get_resource_aware_limits(dataset_size_rows: int = 1000) -> Dict[str, Any]:
    """Provide resource-aware training budgets."""
    hw = get_hardware_info()
    has_gpu = hw["cuda_available"]
    
    # Max candidates to evaluate based on dataset and hardware
    if dataset_size_rows > 100000:
        max_candidates = 2
        tabular_sample_size = 50000
    elif dataset_size_rows > 20000:
        max_candidates = 3
        tabular_sample_size = 20000
    else:
        max_candidates = 4
        tabular_sample_size = None
        
    return {
        "device": "cuda" if has_gpu else "cpu",
        "max_candidates": max_candidates,
        "tabular_sample_size": tabular_sample_size,
        "image_batch_size": 32 if has_gpu else 16,
        "image_max_epochs": 15 if has_gpu else 5,
        "tabular_n_estimators": 100 if has_gpu or hw["cpu_count"] >= 8 else 50,
        "hardware": hw
    }
