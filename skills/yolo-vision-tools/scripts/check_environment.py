#!/usr/bin/env python3
"""
Ultralytics YOLO Environment Check Script

This script provides detailed environment information for Ultralytics YOLO,
including Python version, PyTorch configuration, CUDA availability, 
and dependency verification.
"""

import sys
import platform
import subprocess
import json
from pathlib import Path

def run_command(cmd):
    """Run command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"

def check_python():
    """Check Python environment"""
    print("=" * 60)
    print("PYTHON ENVIRONMENT")
    print("=" * 60)
    
    info = {
        "Python Version": platform.python_version(),
        "Python Implementation": platform.python_implementation(),
        "Python Executable": sys.executable,
        "Platform": platform.platform(),
        "System": platform.system(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
    }
    
    for key, value in info.items():
        print(f"{key:30}: {value}")
    
    return info

def check_pytorch():
    """Check PyTorch installation and CUDA availability"""
    print("\n" + "=" * 60)
    print("PYTORCH & CUDA")
    print("=" * 60)
    
    try:
        import torch
        info = {
            "PyTorch Version": torch.__version__,
            "CUDA Available": torch.cuda.is_available(),
        }
        
        if torch.cuda.is_available():
            info["CUDA Version"] = torch.version.cuda
            info["GPU Count"] = torch.cuda.device_count()
            info["Current Device"] = torch.cuda.current_device()
            info["GPU Name"] = torch.cuda.get_device_name(0) if torch.cuda.device_count() > 0 else "No GPU"
            info["GPU Memory"] = f"{torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB" if torch.cuda.device_count() > 0 else "N/A"
        else:
            info["CUDA Version"] = "Not available"
            info["GPU Count"] = 0
        
        # Check PyTorch build configuration
        build_info = str(torch.__config__).split('\n')
        info["PyTorch Build"] = build_info[0] if build_info else "Unknown"
        
    except ImportError:
        info = {"PyTorch Status": "NOT INSTALLED"}
    except Exception as e:
        info = {"PyTorch Check Error": str(e)}
    
    for key, value in info.items():
        print(f"{key:30}: {value}")
    
    return info

def check_ultralytics():
    """Check Ultralytics YOLO installation"""
    print("\n" + "=" * 60)
    print("ULTRALYTICS YOLO")
    print("=" * 60)
    
    try:
        import ultralytics
        info = {
            "Ultralytics Version": ultralytics.__version__,
        }
        
        # Try to run yolo checks
        try:
            from ultralytics import YOLO
            # Simple test to verify basic functionality
            test_model = YOLO("yolo26n.pt")
            info["YOLO Load Test"] = "PASSED (yolo26n.pt loaded)"
        except Exception as e:
            info["YOLO Load Test"] = f"FAILED: {str(e)}"
            
    except ImportError:
        info = {"Ultralytics Status": "NOT INSTALLED"}
    except Exception as e:
        info = {"Ultralytics Check Error": str(e)}
    
    for key, value in info.items():
        print(f"{key:30}: {value}")
    
    return info

def check_dependencies():
    """Check key dependencies"""
    print("\n" + "=" * 60)
    print("KEY DEPENDENCIES")
    print("=" * 60)
    
    dependencies = [
        "numpy",
        "opencv-python",
        "matplotlib", 
        "pillow",
        "pyyaml",
        "requests",
        "scipy",
        "pandas",
        "psutil",
    ]
    
    info = {}
    for dep in dependencies:
        try:
            module = __import__(dep)
            version = getattr(module, '__version__', 'Unknown')
            info[dep] = f"✓ {version}"
        except ImportError:
            info[dep] = "✗ NOT INSTALLED"
        except Exception as e:
            info[dep] = f"Error: {str(e)}"
    
    for key, value in info.items():
        print(f"{key:30}: {value}")
    
    return info

def check_system_resources():
    """Check system resources"""
    print("\n" + "=" * 60)
    print("SYSTEM RESOURCES")
    print("=" * 60)
    
    info = {}
    
    try:
        import psutil
        # CPU
        info["CPU Count"] = psutil.cpu_count(logical=True)
        info["CPU Frequency"] = f"{psutil.cpu_freq().current:.0f} MHz" if psutil.cpu_freq() else "Unknown"
        info["CPU Usage"] = f"{psutil.cpu_percent(interval=1)}%"
        
        # Memory
        memory = psutil.virtual_memory()
        info["Total RAM"] = f"{memory.total / (1024**3):.2f} GB"
        info["Available RAM"] = f"{memory.available / (1024**3):.2f} GB"
        info["RAM Usage"] = f"{memory.percent}%"
        
        # Disk
        disk = psutil.disk_usage('/')
        info["Total Disk"] = f"{disk.total / (1024**3):.2f} GB"
        info["Available Disk"] = f"{disk.free / (1024**3):.2f} GB"
        info["Disk Usage"] = f"{disk.percent}%"
        
    except ImportError:
        info["psutil"] = "Not installed - resource info unavailable"
    except Exception as e:
        info["Resource Check Error"] = str(e)
    
    for key, value in info.items():
        print(f"{key:30}: {value}")
    
    return info

def generate_report(all_info):
    """Generate JSON report"""
    report_path = Path("yolo_environment_report.json")
    
    with open(report_path, 'w') as f:
        json.dump(all_info, f, indent=2)
    
    print(f"\n✅ Environment report saved to: {report_path.absolute()}")
    return report_path

def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("ULTRAIYICS YOLO ENVIRONMENT DIAGNOSTICS")
    print("=" * 60)
    print("Comprehensive environment check for Ultralytics YOLO\n")
    
    all_info = {}
    
    # Run all checks
    all_info["python"] = check_python()
    all_info["pytorch"] = check_pytorch()
    all_info["ultralytics"] = check_ultralytics()
    all_info["dependencies"] = check_dependencies()
    all_info["resources"] = check_system_resources()
    
    # Generate summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    # Check critical components
    critical_checks = {
        "Python 3.8+": float(all_info["python"].get("Python Version", "0")) >= 3.8,
        "PyTorch Installed": "NOT INSTALLED" not in str(all_info["pytorch"].get("PyTorch Status", "")),
        "CUDA Available": all_info["pytorch"].get("CUDA Available", False),
        "Ultralytics Installed": "NOT INSTALLED" not in str(all_info["ultralytics"].get("Ultralytics Status", "")),
    }
    
    all_passed = True
    for check, passed in critical_checks.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check:30}: {status}")
        if not passed:
            all_passed = False
    
    # Recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    
    if not critical_checks["Python 3.8+"]:
        print("❌ Upgrade Python to version 3.8 or higher")
    
    if not critical_checks["PyTorch Installed"]:
        print("❌ Install PyTorch: pip install torch torchvision")
    
    if not critical_checks["CUDA Available"] and all_info["pytorch"].get("PyTorch Version"):
        print("⚠️  CUDA not available - using CPU only")
        print("   For GPU acceleration, install CUDA-compatible PyTorch")
    
    if not critical_checks["Ultralytics Installed"]:
        print("❌ Install Ultralytics: pip install ultralytics")
    elif "FAILED" in all_info["ultralytics"].get("YOLO Load Test", ""):
        print(f"⚠️  YOLO load test failed: {all_info['ultralytics'].get('YOLO Load Test')}")
        print("   Check internet connection for model download")
    
    # Check RAM for training
    try:
        ram_gb = float(all_info["resources"].get("Total RAM", "0 GB").split()[0])
        if ram_gb < 8:
            print(f"⚠️  Low RAM ({ram_gb:.1f} GB) - 8+ GB recommended for training")
    except:
        pass
    
    # Generate report
    report_path = generate_report(all_info)
    
    # Final status
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ENVIRONMENT CHECK PASSED")
        print("   Ultralytics YOLO should work correctly")
    else:
        print("❌ ENVIRONMENT CHECK FAILED")
        print("   Fix the issues above before using YOLO")
    
    print(f"\nFor more details, run: yolo checks")
    print(f"Report saved to: {report_path.absolute()}")

if __name__ == "__main__":
    main()