import pytest
from pathlib import Path
import sys

backend_path = Path(__file__).resolve().parents[1]
sdk_path = Path(__file__).resolve().parents[2] / "runtime_sdk"
for p in [str(backend_path), str(sdk_path)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.trainers.text.text_trainer import TextTrainer
from aiforge_runtime.loader import load_model

def test_text_classification_pipeline(test_data_dir, tmp_path):
    text_csv = test_data_dir["text_csv"]
    trainer = TextTrainer(
        job_id="test_text_01",
        dataset_path=text_csv,
        requirement="Classify customer reviews as positive or negative."
    )

    prep_res = trainer.prepare_data()
    assert prep_res["train_samples"] > 0
    assert "positive" in prep_res["classes"]
    assert "negative" in prep_res["classes"]

    evaluations = trainer.train()
    assert "Logistic Regression" in evaluations
    assert evaluations["Logistic Regression"]["accuracy"] > 0.6

    package_file = trainer.package_model(output_dir=tmp_path)
    assert package_file.exists()
    assert package_file.suffix == ".aiforge"

    # Runtime SDK loading
    loaded_model = load_model(package_file)
    assert loaded_model.task == "TEXT_CLASSIFICATION"
    assert loaded_model.modality == "TEXT"

    # Predict positive
    pos_res = loaded_model.predict("The product is absolutely amazing with outstanding quality and performance!")
    assert pos_res["prediction"] == "positive"
    assert pos_res["confidence"] > 0.5
    assert "positive" in pos_res["probabilities"]

    # Predict negative
    neg_res = loaded_model.predict("Do not buy this item, completely terrible waste of money and broke.")
    assert neg_res["prediction"] == "negative"
    assert neg_res["confidence"] > 0.5
