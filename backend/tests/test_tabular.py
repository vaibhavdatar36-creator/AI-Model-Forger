import pytest
import pandas as pd
from pathlib import Path
import sys

# Ensure backend and runtime_sdk are imported
backend_path = Path(__file__).resolve().parents[1]
sdk_path = Path(__file__).resolve().parents[2] / "runtime_sdk"
for p in [str(backend_path), str(sdk_path)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.trainers.tabular.tabular_trainer import TabularTrainer
from aiforge_runtime.loader import load_model

def test_tabular_classification_pipeline(test_data_dir, tmp_path):
    churn_csv = test_data_dir["churn_csv"]
    trainer = TabularTrainer(
        job_id="test_tabular_cls_01",
        dataset_path=churn_csv,
        requirement="Classify customer churn from demographic and contract features.",
        options={"target_column": "churn"}
    )

    # 1. Prepare data
    prep_res = trainer.prepare_data()
    assert prep_res["is_classification"] is True
    assert prep_res["train_samples"] > 0
    assert prep_res["test_samples"] > 0

    # 2. Train models
    evaluations = trainer.train()
    assert "Random Forest" in evaluations
    assert "accuracy" in evaluations["Random Forest"]
    assert evaluations["Random Forest"]["accuracy"] >= 0.0

    # 3. Best model selection
    best_name, best_obj, best_metrics = trainer.select_best_model()
    assert best_name is not None
    assert "f1_macro" in best_metrics

    # 4. Package into single .aiforge file
    package_file = trainer.package_model(output_dir=tmp_path)
    assert package_file.exists()
    assert package_file.suffix == ".aiforge"
    assert package_file.stat().st_size > 1000

    # 5. Independent loading using runtime SDK
    loaded_model = load_model(package_file)
    assert loaded_model.task == "TABULAR_CLASSIFICATION"
    assert loaded_model.modality == "TABULAR"

    # 6. Prediction on new raw data
    test_record = {
        "age": 45,
        "tenure_months": 24,
        "monthly_charges": 65.50,
        "contract_type": "two-year"
    }
    pred_res = loaded_model.predict(test_record)
    assert "prediction" in pred_res
    assert pred_res["prediction"] in ["yes", "no"]
    assert "confidence" in pred_res
    assert pred_res["confidence"] > 0.0

def test_tabular_regression_pipeline(test_data_dir, tmp_path):
    house_csv = test_data_dir["house_csv"]
    trainer = TabularTrainer(
        job_id="test_tabular_reg_01",
        dataset_path=house_csv,
        requirement="Predict house prices based on square feet and bedrooms.",
        options={"target_column": "price"}
    )

    prep_res = trainer.prepare_data()
    assert prep_res["is_classification"] is False

    evaluations = trainer.train()
    assert len(evaluations) > 0

    package_file = trainer.package_model(output_dir=tmp_path)
    assert package_file.exists()

    loaded_model = load_model(package_file)
    assert loaded_model.task == "TABULAR_REGRESSION"

    new_house = {
        "square_feet": 2500,
        "bedrooms": 3,
        "bathrooms": 2,
        "neighborhood": "Suburbs"
    }
    res = loaded_model.predict(new_house)
    assert "prediction" in res
    assert isinstance(res["prediction"], float)
    assert res["prediction"] > 100000.0
