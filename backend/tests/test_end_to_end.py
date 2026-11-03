import time
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
import sys

backend_path = Path(__file__).resolve().parents[1]
sdk_path = Path(__file__).resolve().parents[2] / "runtime_sdk"
for p in [str(backend_path), str(sdk_path)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.main import app
from aiforge_runtime.loader import load_model

client = TestClient(app)

def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "hardware" in data

def test_full_end_to_end_workflow(test_data_dir, tmp_path):
    churn_csv = test_data_dir["churn_csv"]

    # 1. Upload dataset
    with open(churn_csv, "rb") as f:
        upload_resp = client.post(
            "/api/upload",
            files={"file": ("customer_churn.csv", f, "text/csv")}
        )
    assert upload_resp.status_code == 200
    upload_data = upload_resp.json()
    dataset_id = upload_data["dataset_id"]
    assert upload_data["modality"] == "TABULAR"

    # 2. Analyze dataset and requirement
    analyze_resp = client.post(
        "/api/analyze",
        json={
            "dataset_id": dataset_id,
            "requirement": "I want to predict whether a customer will churn based on their account info."
        }
    )
    assert analyze_resp.status_code == 200
    analyze_data = analyze_resp.json()
    assert analyze_data["detected_modality"] == "TABULAR"
    assert analyze_data["detected_task"] == "TABULAR_CLASSIFICATION"
    assert analyze_data["is_supported"] is True
    assert len(analyze_data["recommended_models"]) > 0

    # 3. Trigger Training Job
    train_resp = client.post(
        "/api/train",
        json={
            "dataset_id": dataset_id,
            "requirement": "Predict customer churn",
            "project_name": "Customer Churn Predictor"
        }
    )
    assert train_resp.status_code == 200
    train_data = train_resp.json()
    job_id = train_data["job_id"]

    # 4. Poll until job completion
    max_wait_seconds = 60
    start = time.time()
    final_status = None
    while time.time() - start < max_wait_seconds:
        status_resp = client.get(f"/api/jobs/{job_id}")
        assert status_resp.status_code == 200
        st = status_resp.json()
        if st["status"] in ["COMPLETED", "FAILED"]:
            final_status = st
            break
        time.sleep(1)

    assert final_status is not None, "Job timed out"
    assert final_status["status"] == "COMPLETED"
    assert final_status["has_artifact"] is True
    model_id = final_status["model_id"]

    # 5. Fetch Results
    res_resp = client.get(f"/api/results/{job_id}")
    assert res_resp.status_code == 200
    result_data = res_resp.json()
    assert "best_model_name" in result_data
    assert "model_card" in result_data
    assert len(result_data["data_processing_summary"]) > 0

    # 6. Download single .aiforge model artifact
    dl_resp = client.get(f"/api/models/{model_id}/download")
    assert dl_resp.status_code == 200
    assert len(dl_resp.content) > 1000

    downloaded_artifact_file = tmp_path / "downloaded_churn.aiforge"
    with open(downloaded_artifact_file, "wb") as f:
        f.write(dl_resp.content)

    # 7. Use runtime SDK to load the downloaded file in isolation and predict
    loaded = load_model(downloaded_artifact_file)
    assert loaded.task == "TABULAR_CLASSIFICATION"
    pred_res = loaded.predict({
        "age": 30,
        "tenure_months": 12,
        "monthly_charges": 70.0,
        "contract_type": "month-to-month"
    })
    assert "prediction" in pred_res
    assert "confidence" in pred_res
    assert pred_res["confidence"] > 0.0

    # 8. Test live prediction API endpoint as well
    api_pred_resp = client.post(
        f"/api/models/{model_id}/predict",
        json={
            "input_data": {
                "age": 55,
                "tenure_months": 36,
                "monthly_charges": 45.0,
                "contract_type": "two-year"
            }
        }
    )
    assert api_pred_resp.status_code == 200
    assert api_pred_resp.json()["success"] is True
    assert api_pred_resp.json()["prediction"] is not None
