# AI Model Forge: Technical Architecture & System Design

Tagline: *"Upload your data. Describe what you want. Get a ready-to-use AI model."*

## 1. System Philosophy

AI Model Forge is designed to eliminate manual data engineering, hyperparameter guessing, and complex packaging pipelines. The user provides:
1. What they want in natural language.
2. Their raw dataset.

The system performs automatic modality detection, task resolution, data cleaning, feature engineering, candidate model training, metric benchmarking, and produces **ONE downloadable, ready-to-use `.aiforge` model package**.

---

## 2. Universal Pipeline Architecture

```
                          USER
                            |
             +--------------+--------------+
             |                             |
             v                             v
       REQUIREMENT                    RAW DATASET
             |                             |
             v                             v
    RequirementAnalyzer            ModalityDetector
             |                             |
             +--------------+--------------+
                            |
                            v
                      TaskDetector
                            |
           +----------------+----------------+
           |                |                |
           v                v                v
     TABULAR ENGINE    IMAGE ENGINE     TEXT ENGINE
           |                |                |
           +----------------+----------------+
                            |
                            v
                     ModelRecommender
                            |
                            v
                     TrainerRegistry
                            |
           +----------------+----------------+
           |                |                |
           v                v                v
     TabularTrainer    ImageTrainer     TextTrainer
     (Classif/Regr)     (MobileNetV2)   (TF-IDF NLP)
           |                |                |
           +----------------+----------------+
                            |
                            v
                  Comprehensive Evaluation
                            |
                            v
                  Champion Model Selection
                            |
                            v
                  Complete Pipeline Assembly
                            |
                            v
                 Single .aiforge Packager
                            |
                            v
                 Pre-Download Verification
                            |
                            v
                  ONE .aiforge FILE
                            |
                            v
                 aiforge_runtime SDK
                            |
                            v
                  Production Inference
```

---

## 3. Supported Modalities & Tasks (Version 1)

| Modality | Tasks Supported | Default / Candidate Models | Preprocessing Automation |
| :--- | :--- | :--- | :--- |
| **Tabular** | Classification, Regression | Random Forest, HistGradientBoosting, LogisticRegression / Ridge | Median/mode imputation, Standard scaling, OneHotEncoding, ID column exclusion, leakage detection |
| **Image** | Image Classification | PyTorch MobileNetV2 Transfer Learning, ResNet18, Custom CNN | Corrupt file removal, RGB normalization, 224×224 resize, conservative augmentation |
| **Text** | Text Classification | TF-IDF + LogisticRegression, LinearSVC, MultinomialNB | Unicode normalization, whitespace trimming, sublinear TF-IDF vectorization |
| **Time Series** | Forecasting / Regression | Lag Regressor, HistGradientBoosting | Strict chronological split (no leakage), lag window creation, rolling mean stats |

### Honest Capability Boundary & Future Plugin Extensions
Tasks outside Version 1 (e.g. Object Detection, Video Classification, Speech Recognition) are **honestly identified and flagged**. The platform does not fake support; it returns a structured response explaining that the architecture is ready for future trainer plugins.

---

## 4. Single-File Artifact Format (`.aiforge`)

The user downloads **ONE file**:
`customer_churn_model.aiforge`

### Internal Structure:
```
manifest.json          # Format version, model name, checksum SHA-256, file manifest
metadata.json          # Metrics, task, modality, training duration, parameters
schema.json            # Expected input feature names, types, categories, target info
runtime_config.json    # Framework versions, predictor class, hardware configuration
model/
  model.joblib / model.pt  # Trained champion model weights
preprocessing/
  preprocessor.joblib      # Scikit-learn ColumnTransformer / Vectorizer
```

---

## 5. Pre-Download Integrity & Sanity Verification

Before any `.aiforge` artifact is declared "READY FOR DOWNLOAD":
1. The `.aiforge` package is compressed.
2. The runtime SDK reloads the package in an isolated session.
3. A held-out test sample is passed through the inference pipeline.
4. Output schema, probability distributions, and confidence scores are validated.
5. Checksum verification ensures no corrupted archives are provided to the user.

---

## 6. Runtime SDK (`aiforge_runtime`)

Users install the lightweight client:
```bash
pip install ./runtime_sdk
```

And run inference in any application:
```python
from aiforge_runtime import load_model

model = load_model("customer_churn_model.aiforge")
prediction = model.predict({
    "age": 35,
    "tenure_months": 18,
    "monthly_charges": 72.50,
    "contract_type": "month-to-month"
})

print(prediction)
# Output:
# {
#   "prediction": "no",
#   "confidence": 0.892,
#   "probabilities": {"no": 0.892, "yes": 0.108},
#   "task": "TABULAR_CLASSIFICATION"
# }
```
The user never has to re-scale numbers, one-hot encode categories, tokenize text, or resize images manually.
