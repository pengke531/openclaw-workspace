---
name: yolo-vision-tools
description: Use Ultralytics YOLO for computer vision tasks: object detection, instance segmentation, image classification, pose estimation, oriented bounding box detection. Provides best practices for YOLO installation, configuration, model selection, Python/CLI usage, and environment troubleshooting. Use when working with image/video analysis, installing/debugging YOLO environment, selecting appropriate models, or configuring parameters.
---

# Ultralytics YOLO Vision Tools

Ultralytics YOLO is a state-of-the-art computer vision framework supporting multiple tasks including object detection, instance segmentation, image classification, pose estimation, and oriented bounding box detection. This skill provides comprehensive guidance for using YOLO effectively.

**Latest Model**: YOLO26 (released January 2026) features end-to-end NMS-free inference and optimized edge deployment. For stable production workloads, both YOLO26 and YOLO11 are recommended.

## Quick Start

### 1. Installation & Environment Check

```bash
# Install/update Ultralytics
pip install -U ultralytics

# Verify installation and check environment
yolo checks
```

The `yolo checks` command validates Python version, PyTorch, CUDA, GPU availability, and all dependencies. For detailed environment troubleshooting, see [Environment Check](./references/environment_check.md) or use the provided environment check script: `python scripts/check_environment.py`.

### 2. Basic Usage Examples

#### Python Interface
```python
from ultralytics import YOLO

# Load a model (YOLO automatically infers task from model)
model = YOLO("yolo26n.pt")  # or your custom model path

# Predict on various sources
results = model("image.jpg")                     # image file
results = model("video.mp4", stream=True)        # video with streaming
results = model("https://example.com/image.jpg") # URL
results = model(0, show=True)                   # webcam with display
```

#### CLI Interface
```bash
# Basic syntax: yolo TASK MODE ARGS
yolo predict model=yolo26n.pt source="image.jpg"

# Task-specific examples
yolo detect predict model=yolo26n.pt source="video.mp4"
yolo segment predict model=yolo26n-seg.pt source="image.jpg"
yolo pose predict model=yolo26n-pose.pt source="image.jpg"
```

### 3. Model Selection

For quick start, use these default models:
- **Detection**: `yolo26n.pt` (nano), `yolo26s.pt` (small), `yolo26m.pt` (medium)
- **Segmentation**: `yolo26n-seg.pt`, `yolo26s-seg.pt`, `yolo26m-seg.pt`
- **Classification**: `yolo26n-cls.pt`, `yolo26s-cls.pt`, `yolo26m-cls.pt`
- **Pose Estimation**: `yolo26n-pose.pt`, `yolo26s-pose.pt`, `yolo26m-pose.pt`
- **Oriented Detection**: `yolo26n-obb.pt`, `yolo26s-obb.pt`, `yolo26m-obb.pt`

For complete model list and selection guidance: [Model Names](./references/model_names.md) | [Model Selection](./references/model_selection.md)

## Core Workflow

### Step 1: Understand YOLO Tasks
YOLO supports five main computer vision tasks. Choose the right task for your application:
- **Detection**: Identify and localize objects with bounding boxes
- **Segmentation**: Generate pixel-level masks for objects
- **Classification**: Categorize entire images
- **Pose Estimation**: Detect keypoints for pose analysis
- **Oriented Detection**: Detect rotated objects with angle parameter

Detailed comparison: [Task Types](./references/task_types.md)

### Step 2: Select Appropriate Model
Consider these factors when selecting a model:
- **Speed vs. Accuracy**: Nano (fastest) → X (most accurate)
- **Hardware Constraints**: GPU memory, CPU performance
- **Application Requirements**: Real-time vs. batch processing

Guidance: [Model Selection](./references/model_selection.md)

### Step 3: Configure Parameters
Common configuration parameters:
- `conf`: Confidence threshold (default: 0.25)
- `iou`: IoU threshold for NMS (default: 0.7)
- `imgsz`: Input image size (default: 640)
- `device`: Device ID (`0` for first GPU, `cpu` for CPU)
- `save`: Save results to disk
- `show`: Display results in real-time

Complete examples: [Configuration Samples](./references/configuration_samples.md)

### Step 4: Process Results
YOLO returns `Results` objects containing:
- `boxes`: Bounding boxes, confidence scores, class labels
- `masks`: Segmentation masks (for segmentation tasks)
- `keypoints`: Pose keypoints (for pose estimation)
- `probs`: Classification probabilities (for classification)
- `obb`: Oriented bounding boxes (for OBB tasks)

## Advanced Topics

### Training Custom Models
```python
from ultralytics import YOLO

# Load a model
model = YOLO("yolo26n.pt")

# Train on custom dataset
results = model.train(data="dataset.yaml", epochs=100, imgsz=640)
```

Training guide: [Training Basics](./references/training_basics.md) | [Dataset Preparation](./references/dataset_preparation.md)

### Installation Options
Multiple installation methods available:
- **pip**: `pip install -U ultralytics`
- **Conda**: `conda install -c conda-forge ultralytics`
- **Docker**: Pre-built images for GPU/CPU environments
- **From Source**: For development and customization

Detailed instructions: [Installation Guide](./references/installation_guide.md)

### Performance Optimization
- **Streaming Mode**: Use `stream=True` for videos/long sequences to reduce memory
- **Batch Processing**: Process multiple images together for efficiency
- **Hardware Acceleration**: Configure CUDA, TensorRT, or OpenVINO for optimal performance

## Reference Documentation

| Document | Description |
|----------|-------------|
| [Environment Check](./references/environment_check.md) | Comprehensive environment validation and troubleshooting |
| [Installation Guide](./references/installation_guide.md) | All installation methods (pip, Conda, Docker, source) |
| [Task Types](./references/task_types.md) | Detailed comparison of YOLO tasks and use cases |
| [Model Names](./references/model_names.md) | Complete YOLO26 model list with specifications |
| [Model Selection](./references/model_selection.md) | Strategy for choosing models based on requirements |
| [Configuration Samples](./references/configuration_samples.md) | Parameter configuration examples for various scenarios |
| [Dataset Preparation](./references/dataset_preparation.md) | Guide for preparing custom datasets for training |
| [Training Basics](./references/training_basics.md) | Fundamentals of training YOLO models on custom data |
| [Parameter Reference](./references/parameter_reference.md) | Complete reference for all YOLO configuration parameters |

## Utility Scripts

To save token usage and provide ready-to-use tools, the following Python scripts are available in the `scripts/` directory:

| Script | Description | Usage Example |
|--------|-------------|---------------|
| **check_environment.py** | Comprehensive environment diagnostics | `python scripts/check_environment.py` |
| **config_templates.py** | Ready-to-use configuration templates | `from scripts.config_templates import get_production_config` |
| **dataset_tools.py** | Dataset preparation and conversion tools | `from scripts.dataset_tools import coco_to_yolo` |
| **training_helpers.py** | Training, evaluation, and model management | `from scripts.training_helpers import evaluate_model` |
| **quick_tests.py** | Quick functionality tests | `python scripts/quick_tests.py --test environment` |
| **model_utils.py** | Model selection and validation utilities | `from scripts.model_utils import select_model` |

**Benefits of using scripts:**
- **Save tokens**: Large code blocks are extracted from documentation
- **Ready-to-use**: No need to copy-paste code from documentation
- **Modular**: Import only what you need
- **Maintainable**: Scripts can be updated independently

## Troubleshooting

### Common Issues

**Q: `yolo` command not found after installation?**
A: Try `python -m ultralytics yolo` or check Python environment PATH.

**Q: How to use specific GPU?**
A: Set `device=0` (first GPU) or `device=cpu` for CPU-only mode.

**Q: Model downloads slowly?**
A: Set `ULTRALYTICS_HOME` environment variable to control cache location.

**Q: How to filter specific classes?**
A: Use `classes` parameter: `classes=[0, 2, 5]` (class indices).

**Q: Memory issues with long videos?**
A: Use `stream=True` to process videos as generators.

**Q: Real-time webcam support?**
A: Yes, use `source=0` (default camera) with `show=True` for live display.

### Getting Help
- Run `yolo checks` to diagnose environment issues
- Check official documentation: https://docs.ultralytics.com
- Review configuration reference: https://docs.ultralytics.com/usage/cfg/

---

**License Note**: Ultralytics YOLO is available under AGPL-3.0 for open source use and Enterprise License for commercial applications. Review licensing at https://ultralytics.com/license.