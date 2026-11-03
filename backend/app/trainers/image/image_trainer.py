import os
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Tuple
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

from app.trainers.base_trainer import BaseTrainer
from app.trainers.image.image_dataset_processor import ImageDatasetProcessor
from app.services.schema_detector import SchemaDetector
from app.services.model_packager import ModelPackager
from app.services.model_validator import ModelValidator
from app.utils.hardware import get_resource_aware_limits
from app.core.logging import logger

class SimplePyTorchImageDataset(Dataset):
    def __init__(self, samples: List[Tuple[Path, int]], transform=None):
        self.samples = samples
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label_idx = self.samples[idx]
        with Image.open(path) as img:
            img = img.convert("RGB")
            if self.transform:
                img = self.transform(img)
            return img, label_idx

class FallbackConvNet(nn.Module):
    """Clean, lightweight fallback CNN if torchvision pretrained downloads are blocked."""
    def __init__(self, num_classes: int):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.AdaptiveAvgPool2d((4, 4))
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 4 * 4, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)

class ImageTrainer(BaseTrainer):
    """AutoML trainer for Computer Vision Image Classification with Transfer Learning."""

    def __init__(self, job_id: str, dataset_path: Path, requirement: str, options: Optional[Dict[str, Any]] = None):
        super().__init__(job_id, dataset_path, requirement, options)
        self.samples = []
        self.classes = []
        self.class_to_idx = {}
        self.train_loader = None
        self.test_loader = None
        self.test_sample_path = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def analyze_dataset(self) -> Dict[str, Any]:
        samples, classes, report = ImageDatasetProcessor.load_and_validate_dataset(self.dataset_path)
        return {
            "modality": "IMAGE",
            "task": "IMAGE_CLASSIFICATION",
            "total_images": report["valid_samples"],
            "classes": classes,
            "corrupt_images": report["corrupt_images"]
        }

    def prepare_data(self) -> Dict[str, Any]:
        samples, classes, report = ImageDatasetProcessor.load_and_validate_dataset(self.dataset_path)
        if len(samples) < 4:
            raise ValueError(f"Insufficient valid images for training (found {len(samples)} images). Minimum 4 required.")

        self.classes = classes
        self.class_to_idx = {c: i for i, c in enumerate(classes)}
        indexed_samples = [(p, self.class_to_idx[lbl]) for p, lbl in samples]
        self.samples = indexed_samples

        self.data_processing_summary.append(f"Discovered {len(samples)} valid images across {len(classes)} classes: {classes}.")
        if report["corrupt_images"] > 0:
            self.data_processing_summary.append(f"Automatically excluded {report['corrupt_images']} corrupt or unreadable image files.")

        # Train / Test split
        test_size = float(self.options.get("test_size", 0.2))
        random_seed = int(self.options.get("random_seed", 42))

        # Check stratification capability
        labels_list = [s[1] for s in indexed_samples]
        unique_labels, counts = np.unique(labels_list, return_counts=True)
        can_stratify = (counts >= 2).all()

        train_s, test_s = train_test_split(
            indexed_samples,
            test_size=test_size,
            random_state=random_seed,
            stratify=labels_list if can_stratify else None
        )

        self.test_sample_path = test_s[0][0]

        # Augmentation & normalization transforms
        train_transforms = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        test_transforms = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        self.data_processing_summary.append("Configured RGB standardization, 224x224 resizing, and conservative data augmentation.")

        train_dataset = SimplePyTorchImageDataset(train_s, transform=train_transforms)
        test_dataset = SimplePyTorchImageDataset(test_s, transform=test_transforms)

        batch_size = 16 if torch.cuda.is_available() else 8
        self.train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        self.test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

        self.schema = SchemaDetector.detect_image_schema(image_size=(224, 224), channels=3, classes=classes)

        return {
            "train_samples": len(train_s),
            "test_samples": len(test_s),
            "num_classes": len(classes),
            "classes": classes
        }

    def recommend_models(self) -> List[Dict[str, Any]]:
        return [
            {"model_name": "mobilenet_v2", "display_name": "MobileNetV2 Transfer Learning", "is_recommended": True},
            {"model_name": "custom_cnn", "display_name": "Lightweight Custom CNN", "is_recommended": False}
        ]

    def _build_model(self, model_type: str = "mobilenet_v2", num_classes: int = 2) -> nn.Module:
        try:
            if model_type == "mobilenet_v2":
                # Use default pretrained weights
                model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)
                # Freeze backbone feature layers for fast transfer learning
                for param in model.features.parameters():
                    param.requires_grad = False
                in_features = model.classifier[1].in_features
                model.classifier = nn.Sequential(
                    nn.Dropout(0.2),
                    nn.Linear(in_features, num_classes)
                )
                return model
            elif model_type == "resnet18":
                model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
                for param in model.parameters():
                    param.requires_grad = False
                in_features = model.fc.in_features
                model.fc = nn.Linear(in_features, num_classes)
                return model
        except Exception as e:
            logger.warning(f"Could not download torchvision weights ({e}), falling back to custom CNN.")

        return FallbackConvNet(num_classes)

    def train(self, progress_callback: Optional[Callable[[int, str, Optional[Dict[str, Any]]], None]] = None) -> Dict[str, Any]:
        num_classes = len(self.classes)
        model = self._build_model("mobilenet_v2", num_classes).to(self.device)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3)

        epochs = int(self.options.get("epochs") or (5 if torch.cuda.is_available() else 3))
        start_time = time.time()

        for epoch in range(epochs):
            model.train()
            running_loss = 0.0
            correct = 0
            total = 0

            for batch_idx, (inputs, targets) in enumerate(self.train_loader):
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                _, predicted = outputs.max(1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()

            epoch_loss = running_loss / (total or 1)
            epoch_acc = correct / (total or 1)

            pct = int(25 + ((epoch + 1) / epochs) * 50)
            if progress_callback:
                progress_callback(
                    pct,
                    f"Epoch [{epoch+1}/{epochs}] - Loss: {epoch_loss:.4f}, Acc: {epoch_acc:.4f}",
                    {"epoch": epoch + 1, "loss": round(epoch_loss, 4), "accuracy": round(epoch_acc, 4)}
                )

        train_duration = time.time() - start_time
        self.trained_models["MobileNetV2"] = {
            "model": model,
            "train_time": round(train_duration, 2)
        }

        return self.evaluate()

    def evaluate(self) -> Dict[str, Any]:
        model = self.trained_models["MobileNetV2"]["model"]
        model.eval()

        all_preds = []
        all_targets = []

        with torch.no_grad():
            for inputs, targets in self.test_loader:
                inputs = inputs.to(self.device)
                outputs = model(inputs)
                _, preds = outputs.max(1)
                all_preds.extend(preds.cpu().numpy())
                all_targets.extend(targets.numpy())

        acc = float(accuracy_score(all_targets, all_preds))
        f1_macro = float(f1_score(all_targets, all_preds, average="macro", zero_division=0))
        f1_weighted = float(f1_score(all_targets, all_preds, average="weighted", zero_division=0))
        prec = float(precision_score(all_targets, all_preds, average="weighted", zero_division=0))
        rec = float(recall_score(all_targets, all_preds, average="weighted", zero_division=0))

        cm = confusion_matrix(all_targets, all_preds).tolist()

        self.evaluations = {
            "MobileNetV2": {
                "accuracy": round(acc, 4),
                "f1_macro": round(f1_macro, 4),
                "f1_weighted": round(f1_weighted, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "train_time_sec": self.trained_models["MobileNetV2"]["train_time"],
                "confusion_matrix": {"labels": self.classes, "matrix": cm},
                "primary_metric": round(f1_macro, 4)
            }
        }
        return self.evaluations

    def select_best_model(self) -> Tuple[str, Any, Dict[str, Any]]:
        self.best_model_name = "MobileNetV2"
        self.best_model_obj = self.trained_models["MobileNetV2"]["model"]
        return self.best_model_name, self.best_model_obj, self.evaluations["MobileNetV2"]

    def package_model(self, output_dir: Path) -> Path:
        best_name, best_obj, best_metrics = self.select_best_model()
        model_clean_name = f"image_classifier_{self.job_id[:8]}"
        out_file = output_dir / f"{model_clean_name}.aiforge"

        metadata = {
            "model_name": model_clean_name,
            "task": "IMAGE_CLASSIFICATION",
            "modality": "IMAGE",
            "model_type": "MobileNetV2 (PyTorch)",
            "best_metric_name": "f1_macro",
            "best_metric_value": best_metrics["f1_macro"],
            "metrics": best_metrics,
            "classes": self.classes,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        # Model is saved on CPU for portability
        cpu_model = best_obj.to("cpu")

        packaged_path = ModelPackager.package(
            output_filepath=out_file,
            model_obj=cpu_model,
            preprocessor_obj=None,
            metadata=metadata,
            schema=self.schema,
            predictor_type="image"
        )

        # Validate with test sample
        valid, msg, report = ModelValidator.validate_package(packaged_path, self.test_sample_path)
        if not valid:
            raise RuntimeError(f"Packaged image model validation failed: {msg}")

        return packaged_path
