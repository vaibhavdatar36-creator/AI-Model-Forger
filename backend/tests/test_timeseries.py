import pytest
from pathlib import Path
import sys

backend_path = Path(__file__).resolve().parents[1]
sdk_path = Path(__file__).resolve().parents[2] / "runtime_sdk"
for p in [str(backend_path), str(sdk_path)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from app.trainers.timeseries.timeseries_trainer import TimeSeriesTrainer
from aiforge_runtime.loader import load_model

def test_timeseries_pipeline(test_data_dir, tmp_path):
    ts_csv = test_data_dir["ts_csv"]
    trainer = TimeSeriesTrainer(
        job_id="test_ts_01",
        dataset_path=ts_csv,
        requirement="Forecast electricity demand based on historical readings and temperature.",
        options={"target_column": "electricity_demand"}
    )

    prep_res = trainer.prepare_data()
    assert prep_res["train_samples"] > 0
    assert prep_res["test_samples"] > 0
    assert "electricity_demand" == prep_res["target_column"]

    evaluations = trainer.train()
    assert len(evaluations) > 0
    for name, metrics in evaluations.items():
        assert "rmse" in metrics
        assert metrics["rmse"] >= 0.0

    package_file = trainer.package_model(output_dir=tmp_path)
    assert package_file.exists()
    assert package_file.suffix == ".aiforge"

    loaded_model = load_model(package_file)
    assert loaded_model.task == "TIME_SERIES_FORECASTING"

    sample_input = trainer.test_df_sample
    res = loaded_model.predict(sample_input)
    assert "prediction" in res
    assert isinstance(res["prediction"], float)
    assert res["prediction"] > 0.0
