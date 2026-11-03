import os
import shutil
import tempfile
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import pytest

@pytest.fixture(scope="session")
def test_data_dir():
    temp_dir = tempfile.mkdtemp(prefix="aiforge_test_data_")
    data_path = Path(temp_dir)

    # 1. Tabular Classification: Churn
    np.random.seed(42)
    n = 200
    churn_df = pd.DataFrame({
        "customer_id": [f"CUST_{i:04d}" for i in range(n)],
        "age": np.random.randint(18, 75, size=n),
        "tenure_months": np.random.randint(1, 72, size=n),
        "monthly_charges": np.round(np.random.uniform(20.0, 120.0, size=n), 2),
        "contract_type": np.random.choice(["month-to-month", "one-year", "two-year"], size=n),
        "churn": np.random.choice(["yes", "no"], size=n, p=[0.3, 0.7])
    })
    # Add a few intentional missing values to test automatic imputation
    churn_df.loc[5:8, "age"] = np.nan
    churn_df.loc[12:14, "contract_type"] = np.nan
    churn_csv = data_path / "customer_churn.csv"
    churn_df.to_csv(churn_csv, index=False)

    # 2. Tabular Regression: House Prices
    n = 200
    sqft = np.random.randint(600, 4500, size=n)
    beds = np.random.randint(1, 6, size=n)
    baths = np.random.randint(1, 4, size=n)
    prices = sqft * 250 + beds * 15000 + baths * 10000 + np.random.normal(0, 5000, size=n)
    house_df = pd.DataFrame({
        "house_id": [f"H_{i:04d}" for i in range(n)],
        "square_feet": sqft,
        "bedrooms": beds,
        "bathrooms": baths,
        "neighborhood": np.random.choice(["Downtown", "Suburbs", "Northside", "Uptown"], size=n),
        "price": np.round(prices, 2)
    })
    house_csv = data_path / "house_prices.csv"
    house_df.to_csv(house_csv, index=False)

    # 3. Text Classification: Sentiment Reviews
    reviews = [
        ("The product is absolutely amazing and exceeded all expectations!", "positive"),
        ("Outstanding quality, fast delivery, and very helpful customer service.", "positive"),
        ("I love this so much, best purchase I have made all year.", "positive"),
        ("Terrific value and works flawlessly straight out of the box.", "positive"),
        ("Brilliant craftsmanship and superb performance. Five stars!", "positive"),
        ("Highly recommend this to everyone looking for reliable quality.", "positive"),
        ("Completely terrible experience, broke after two days of use.", "negative"),
        ("Awful customer support and extremely poor build materials.", "negative"),
        ("Do not buy this item, it is a complete waste of money.", "negative"),
        ("Disappointed with the defective product and late shipping.", "negative"),
        ("Worst service ever, misleading description and faulty parts.", "negative"),
        ("Fails repeatedly and crashes constantly. Very frustrating.", "negative")
    ] * 15
    review_df = pd.DataFrame(reviews, columns=["review_text", "sentiment"])
    text_csv = data_path / "reviews.csv"
    review_df.to_csv(text_csv, index=False)

    # 4. Time Series: Electricity Demand
    dates = pd.date_range(start="2026-01-01", periods=250, freq="h")
    base_demand = 500 + 100 * np.sin(np.linspace(0, 10 * np.pi, len(dates)))
    demand = base_demand + np.random.normal(0, 10, len(dates))
    ts_df = pd.DataFrame({
        "timestamp": dates,
        "temperature": np.random.uniform(10.0, 35.0, len(dates)),
        "electricity_demand": np.round(demand, 2)
    })
    ts_csv = data_path / "electricity_demand.csv"
    ts_df.to_csv(ts_csv, index=False)

    # 5. Image Classification Dataset: Cats vs Dogs
    img_dir = data_path / "animal_images"
    cats_dir = img_dir / "cats"
    dogs_dir = img_dir / "dogs"
    cats_dir.mkdir(parents=True, exist_ok=True)
    dogs_dir.mkdir(parents=True, exist_ok=True)

    # Generate synthetic colored images
    for i in range(6):
        # Cat image (circles)
        im = Image.new("RGB", (64, 64), color=(200, 100, 50))
        draw = ImageDraw.Draw(im)
        draw.ellipse([10, 10, 54, 54], fill=(240, 150, 100))
        im.save(cats_dir / f"cat_{i}.jpg")

        # Dog image (rectangles)
        im2 = Image.new("RGB", (64, 64), color=(50, 100, 200))
        draw2 = ImageDraw.Draw(im2)
        draw2.rectangle([10, 10, 54, 54], fill=(100, 150, 240))
        im2.save(dogs_dir / f"dog_{i}.jpg")

    # Add 1 corrupt file to verify corrupt rejection
    corrupt_file = cats_dir / "corrupt_sample.jpg"
    with open(corrupt_file, "wb") as f:
        f.write(b"NOT_A_VALID_JPEG_IMAGE_DATA_CORRUPTED")

    yield {
        "base_dir": data_path,
        "churn_csv": churn_csv,
        "house_csv": house_csv,
        "text_csv": text_csv,
        "ts_csv": ts_csv,
        "img_dir": img_dir
    }

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)
