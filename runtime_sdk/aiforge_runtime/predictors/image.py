import os
import io
from pathlib import Path
from typing import Any, Dict, List, Union
import numpy as np
from PIL import Image
from .base import BasePredictor

class ImagePredictor(BasePredictor):
    def predict(self, input_data: Any) -> Dict[str, Any]:
        """
        Accepts:
            - File path string or Path
            - PIL Image
            - Raw bytes
        """
        import torch
        from torchvision import transforms

        # 1. Load image
        img = None
        if isinstance(input_data, (str, Path)):
            img_path = Path(input_data)
            if not img_path.exists():
                raise FileNotFoundError(f"Image not found at path: {img_path}")
            img = Image.open(img_path).convert("RGB")
        elif isinstance(input_data, bytes):
            img = Image.open(io.BytesIO(input_data)).convert("RGB")
        elif isinstance(input_data, Image.Image):
            img = input_data.convert("RGB")
        else:
            raise TypeError(f"Unsupported image input type: {type(input_data)}. Expected file path, PIL Image, or bytes.")

        # 2. Preprocess transformation
        expected_shape = self.schema.get("expected_shape", [3, 224, 224])
        target_size = (expected_shape[1], expected_shape[2])

        transform = transforms.Compose([
            transforms.Resize(target_size),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

        tensor = transform(img).unsqueeze(0) # [1, 3, H, W]

        # 3. Model forward pass
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(tensor)
            probs = torch.softmax(outputs, dim=1).squeeze(0).cpu().numpy()

        classes = self.schema.get("target", {}).get("classes", [])
        if not classes:
            classes = [f"class_{i}" for i in range(len(probs))]

        best_idx = int(np.argmax(probs))
        confidence = float(probs[best_idx])
        prediction_label = classes[best_idx] if best_idx < len(classes) else str(best_idx)

        prob_dict = {
            classes[i] if i < len(classes) else f"class_{i}": float(probs[i])
            for i in range(len(probs))
        }

        return {
            "prediction": prediction_label,
            "confidence": round(confidence, 4),
            "probabilities": prob_dict,
            "task": "IMAGE_CLASSIFICATION"
        }
