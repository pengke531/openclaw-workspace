#!/usr/bin/env python3
"""
YOLO Dataset Tools

This script provides tools for dataset preparation, format conversion, and analysis.
Extracted from dataset_preparation.md to save token usage.
"""

import json
import xml.etree.ElementTree as ET
import shutil
from pathlib import Path
from sklearn.model_selection import train_test_split
import yaml

# ============================================================================
# FORMAT CONVERSION TOOLS
# ============================================================================

def coco_to_yolo(coco_json_path, output_dir):
    """
    Convert COCO format to YOLO format
    
    Args:
        coco_json_path: Path to COCO JSON annotation file
        output_dir: Output directory for YOLO format
    """
    
    # Load COCO annotations
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)
    
    # Create output directories
    images_dir = Path(output_dir) / 'images'
    labels_dir = Path(output_dir) / 'labels'
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    
    # Map category IDs to YOLO class indices
    categories = {cat['id']: idx for idx, cat in enumerate(coco_data['categories'])}
    
    # Process each image
    for img_info in coco_data['images']:
        img_id = img_info['id']
        img_width = img_info['width']
        img_height = img_info['height']
        img_name = img_info['file_name']
        
        # Find annotations for this image
        img_annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] == img_id]
        
        # Create label file
        label_file = labels_dir / f"{Path(img_name).stem}.txt"
        with open(label_file, 'w') as f:
            for ann in img_annotations:
                # Get bounding box [x, y, width, height] in COCO format
                bbox = ann['bbox']
                x_min, y_min, width, height = bbox
                
                # Convert to YOLO format
                x_center = (x_min + width / 2) / img_width
                y_center = (y_min + height / 2) / img_height
                width_norm = width / img_width
                height_norm = height / img_height
                
                # Get class ID
                class_id = categories.get(ann['category_id'], 0)
                
                # Write to file
                f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width_norm:.6f} {height_norm:.6f}\n")
    
    print(f"Conversion complete. Output directory: {output_dir}")
    return output_dir

def voc_to_yolo(voc_xml_path, output_dir, class_mapping):
    """
    Convert VOC XML format to YOLO format
    
    Args:
        voc_xml_path: Path to VOC XML annotation file
        output_dir: Output directory for YOLO format
        class_mapping: Dictionary mapping class names to YOLO class IDs
    """
    
    # Parse XML
    tree = ET.parse(voc_xml_path)
    root = tree.getroot()
    
    # Get image dimensions
    size = root.find('size')
    img_width = int(size.find('width').text)
    img_height = int(size.find('height').text)
    
    # Create output file
    output_file = Path(output_dir) / f"{Path(voc_xml_path).stem}.txt"
    
    with open(output_file, 'w') as f:
        # Process each object
        for obj in root.findall('object'):
            # Get class name
            class_name = obj.find('name').text
            class_id = class_mapping.get(class_name, 0)
            
            # Get bounding box
            bndbox = obj.find('bndbox')
            x_min = float(bndbox.find('xmin').text)
            y_min = float(bndbox.find('ymin').text)
            x_max = float(bndbox.find('xmax').text)
            y_max = float(bndbox.find('ymax').text)
            
            # Convert to YOLO format
            x_center = (x_min + x_max) / 2 / img_width
            y_center = (y_min + y_max) / 2 / img_height
            width = (x_max - x_min) / img_width
            height = (y_max - y_min) / img_height
            
            # Write to file
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")
    
    print(f"Conversion complete. Output file: {output_file}")
    return output_file

# ============================================================================
# DATASET SPLITTING TOOLS
# ============================================================================

def split_dataset(image_dir, label_dir, output_dir, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    """
    Split dataset into train/val/test sets
    
    Args:
        image_dir: Directory containing images
        label_dir: Directory containing labels
        output_dir: Output directory for split dataset
        train_ratio: Proportion for training set
        val_ratio: Proportion for validation set
        test_ratio: Proportion for test set
    """
    
    # Get all image files
    image_files = list(Path(image_dir).glob('*.jpg')) + list(Path(image_dir).glob('*.png'))
    
    # Split indices
    train_files, temp_files = train_test_split(image_files, train_size=train_ratio, random_state=42)
    val_files, test_files = train_test_split(temp_files, train_size=val_ratio/(val_ratio+test_ratio), random_state=42)
    
    # Create output directories
    splits = {
        'train': train_files,
        'val': val_files,
        'test': test_files
    }
    
    for split_name, files in splits.items():
        # Create directories
        img_split_dir = Path(output_dir) / 'images' / split_name
        label_split_dir = Path(output_dir) / 'labels' / split_name
        img_split_dir.mkdir(parents=True, exist_ok=True)
        label_split_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy files
        for img_file in files:
            # Copy image
            shutil.copy(img_file, img_split_dir / img_file.name)
            
            # Copy corresponding label
            label_file = Path(label_dir) / f"{img_file.stem}.txt"
            if label_file.exists():
                shutil.copy(label_file, label_split_dir / label_file.name)
    
    print(f"Dataset split complete: {len(train_files)} train, {len(val_files)} val, {len(test_files)} test")
    return splits

# ============================================================================
# DATASET ANALYSIS TOOLS
# ============================================================================

def analyze_dataset(labels_dir):
    """
    Analyze dataset statistics
    
    Args:
        labels_dir: Directory containing label files
    """
    
    from collections import Counter
    import matplotlib.pyplot as plt
    
    label_files = list(Path(labels_dir).glob('*.txt'))
    
    # Count objects per class
    class_counts = Counter()
    bbox_stats = {'widths': [], 'heights': []}
    
    for label_file in label_files:
        with open(label_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 5:
                    class_id = int(parts[0])
                    class_counts[class_id] += 1
                    
                    # Bbox dimensions
                    width = float(parts[3])
                    height = float(parts[4])
                    bbox_stats['widths'].append(width)
                    bbox_stats['heights'].append(height)
    
    # Print statistics
    print(f"Total label files: {len(label_files)}")
    print(f"Total objects: {sum(class_counts.values())}")
    print("\nClass distribution:")
    for class_id, count in sorted(class_counts.items()):
        print(f"  Class {class_id}: {count} objects ({count/sum(class_counts.values())*100:.1f}%)")
    
    # Plot distribution
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.hist(bbox_stats['widths'], bins=50, alpha=0.7)
    plt.title('Bounding Box Width Distribution')
    plt.xlabel('Normalized Width')
    
    plt.subplot(1, 2, 2)
    plt.hist(bbox_stats['heights'], bins=50, alpha=0.7)
    plt.title('Bounding Box Height Distribution')
    plt.xlabel('Normalized Height')
    
    plt.tight_layout()
    plt.show()
    
    return {
        'total_files': len(label_files),
        'total_objects': sum(class_counts.values()),
        'class_distribution': dict(class_counts),
        'bbox_stats': bbox_stats
    }

# ============================================================================
# DATASET CONFIGURATION TOOLS
# ============================================================================

def create_data_yaml(dataset_path, class_names, output_path='data.yaml'):
    """
    Create YOLO dataset configuration file
    
    Args:
        dataset_path: Path to dataset root directory
        class_names: List of class names or dictionary mapping class IDs to names
        output_path: Output path for data.yaml file
    """
    
    # Convert class_names to dictionary if it's a list
    if isinstance(class_names, list):
        class_dict = {i: name for i, name in enumerate(class_names)}
    else:
        class_dict = class_names
    
    # Create data.yaml content
    data = {
        'path': str(Path(dataset_path).absolute()),
        'train': 'images/train',
        'val': 'images/val',
        'test': 'images/test',
        'names': class_dict,
        'nc': len(class_dict),
    }
    
    # Write to file
    with open(output_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    
    print(f"Dataset configuration created: {output_path}")
    return output_path

def validate_dataset(dataset_path):
    """
    Validate YOLO dataset structure and files
    
    Args:
        dataset_path: Path to dataset root directory
    """
    
    dataset_path = Path(dataset_path)
    
    # Check directory structure
    required_dirs = ['images/train', 'images/val', 'labels/train', 'labels/val']
    missing_dirs = []
    
    for dir_path in required_dirs:
        if not (dataset_path / dir_path).exists():
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"Missing directories: {missing_dirs}")
        return False
    
    # Check for corresponding label files
    issues = []
    
    for split in ['train', 'val']:
        image_dir = dataset_path / 'images' / split
        label_dir = dataset_path / 'labels' / split
        
        if not image_dir.exists() or not label_dir.exists():
            continue
        
        # Get all images
        images = list(image_dir.glob('*.jpg')) + list(image_dir.glob('*.png'))
        
        for img_file in images:
            label_file = label_dir / f"{img_file.stem}.txt"
            
            if not label_file.exists():
                issues.append(f"Missing label for {img_file.relative_to(dataset_path)}")
            
            # Validate label file format
            if label_file.exists():
                with open(label_file, 'r') as f:
                    for line_num, line in enumerate(f, 1):
                        parts = line.strip().split()
                        if len(parts) != 5:
                            issues.append(f"Invalid format in {label_file.relative_to(dataset_path)} line {line_num}")
                            continue
                        
                        # Check values are within [0, 1]
                        try:
                            values = list(map(float, parts[1:]))
                            if any(v < 0 or v > 1 for v in values):
                                issues.append(f"Values out of range in {label_file.relative_to(dataset_path)} line {line_num}")
                        except ValueError:
                            issues.append(f"Non-numeric values in {label_file.relative_to(dataset_path)} line {line_num}")
    
    if issues:
        print(f"Validation issues found ({len(issues)}):")
        for issue in issues[:10]:  # Show first 10 issues
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more issues")
        return False
    
    print("Dataset validation passed!")
    return True

# ============================================================================
# AUGMENTATION TOOLS
# ============================================================================

def get_augmentation_pipeline(mode='train'):
    """
    Get augmentation pipeline for training or validation
    
    Args:
        mode: 'train' for training augmentations, 'val' for validation
    """
    
    try:
        import albumentations as A
        from albumentations.pytorch import ToTensorV2
        
        if mode == 'train':
            return A.Compose([
                A.Resize(640, 640),
                A.HorizontalFlip(p=0.5),
                A.VerticalFlip(p=0.1),
                A.RandomBrightnessContrast(p=0.2),
                A.RandomGamma(p=0.2),
                A.HueSaturationValue(p=0.3),
                A.Rotate(limit=15, p=0.5),
                A.Blur(blur_limit=3, p=0.1),
                A.CLAHE(p=0.1),
                A.ToGray(p=0.1),
                ToTensorV2()
            ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
        
        else:  # validation/test
            return A.Compose([
                A.Resize(640, 640),
                ToTensorV2()
            ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
    
    except ImportError:
        print("Warning: albumentations not installed. Augmentation pipeline not available.")
        print("Install with: pip install albumentations")
        return None

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("YOLO Dataset Tools")
    print("=" * 60)
    
    # Example: Create dataset configuration
    class_names = ['person', 'bicycle', 'car', 'motorcycle', 'airplane']
    config_path = create_data_yaml('./my_dataset', class_names)
    print(f"Created dataset config: {config_path}")
    
    # Example: Analyze dataset
    print("\nTo analyze a dataset:")
    print("  from dataset_tools import analyze_dataset")
    print("  stats = analyze_dataset('./my_dataset/labels/train')")
    
    # Example: Split dataset
    print("\nTo split a dataset:")
    print("  from dataset_tools import split_dataset")
    print("  splits = split_dataset('./images', './labels', './split_dataset')")
    
    print("\nAvailable functions:")
    print("  - coco_to_yolo(): Convert COCO format to YOLO format")
    print("  - voc_to_yolo(): Convert VOC format to YOLO format")
    print("  - split_dataset(): Split dataset into train/val/test")
    print("  - analyze_dataset(): Analyze dataset statistics")
    print("  - create_data_yaml(): Create dataset configuration")
    print("  - validate_dataset(): Validate dataset structure")
    print("  - get_augmentation_pipeline(): Get augmentation pipeline")