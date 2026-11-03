import pytest
from pathlib import Path
import sys

backend_path = Path(__file__).resolve().parents[1]
sdk_path = Path(__file__).resolve().parents[2] / "runtime_sdk"
for p in [str(backend_path), str(sdk_path)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.trainers.image.image_trainer import ImageTrainer
from app.trainers.image.image_dataset_processor import ImageDatasetProcessor
from aiforge_runtime.loader import load_model

def test_image_dataset_processor_and_trainer(test_data_dir, tmp_path):
    img_dir = test_data_dir["img_dir"]

    # 1. Dataset processor checks corrupt images
    samples, classes, report = ImageDatasetProcessor.load_and_validate_dataset(img_dir)
    assert report["corrupt_images"] >= 1
    assert "cats" in classes
    assert "dogs" in classes
    assert len(samples) >= 12

    # 2. Image trainer
    trainer = ImageTrainer(
        job_id="test_img_01",
        dataset_path=img_dir,
        requirement="Classify images of cats and dogs.",
        options={"epochs": 1}
    )

    prep_res = trainer.prepare_data()
    assert prep_res["train_samples"] > 0
    assert prep_res["test_samples"] > 0

    # 3. Fast 1-epoch train test
    evals = trainer.train()
    assert "MobileNetV2" in evals
    assert "accuracy" in evals["MobileNetV2"]

    # 4. Package into single .aiforge
    package_file = trainer.package_model(output_dir=tmp_path)
    assert package_file.exists()
    assert package_file.suffix == ".aiforge"

    # 5. Runtime SDK loading and inference
    loaded_model = load_model(package_file)
    assert loaded_model.task == "IMAGE_CLASSIFICATION"
    assert loaded_model.modality == "IMAGE"

    test_img_path = trainer.test_sample_path
    res = loaded_model.predict(test_img_path)
    assert "prediction" in res
    assert res["prediction"] in classes
    assert "confidence" in res
    assert res["confidence"] > 0.0
    assert "probabilities" in res
