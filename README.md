# AI Model Forge

> **"Upload your data. Describe what you want. Get a ready-to-use AI model."**

AI Model Forge is an extensible, universal Multimodal AutoML Platform. It automatically analyzes uploaded datasets, detects the data modality and machine learning task, performs automated data cleaning and feature engineering, trains and benchmarks candidate models, selects the champion architecture, and packages the complete inference pipeline into **ONE downloadable `.aiforge` model file**.

---

## 🌟 Key Capabilities

- **Natural Language Intent**: State your objective in plain English (e.g. *"Predict customer churn"*, *"Classify review sentiment"*).
- **Universal Modality Detection**: Handles Tabular (`.csv`, `.xlsx`, `.parquet`, `.json`), Computer Vision (`.jpg`, `.png`, folders, ZIPs), Text (`.txt`, CSV text corpora), and Time-Series datasets.
- **Zero-Manual Data Engineering**:
  - Imputes missing values automatically (median/mode).
  - Normalizes & standardizes numerical features.
  - Automatically One-Hot Encodes categorical features (`handle_unknown="ignore"`).
  - Detects and removes ID columns, constants, and target leakage candidates.
  - Standardizes images to 224×224 RGB with data augmentation.
  - Generates lag features and rolling statistics with strict chronological splitting for time series.
- **Transfer Learning & Modern Baselines**:
  - Tabular: Random Forest, Histogram-based Gradient Boosting, Logistic Regression, Ridge.
  - Vision: PyTorch MobileNetV2 Transfer Learning with fine-tuning.
  - Text: TF-IDF sublinear vectorization + Logistic Regression & Linear SVM.
  - Time Series: Lag-Feature HistGradientBoosting & Random Forest Regressors.
- **Single-File `.aiforge` Artifact**: Download exactly ONE portable file containing weights, preprocessors, input schema, and runtime config.
- **Python Runtime SDK (`aiforge_runtime`)**: Load and predict anywhere with 3 lines of code. Raw input is transformed automatically.
- **Interactive Playground**: Test any trained model directly in the browser with live prediction outputs, confidence scores, and probability breakdown charts.

---

## 📁 Project Structure

```
ai-model-forge/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI application entry point
│   │   ├── api/                       # REST endpoints (upload, analyze, train, models, predict)
│   │   ├── core/                      # Config, logging, security (Zip Slip & traversal protection)
│   │   ├── database/                  # SQLAlchemy models & SQLite database
│   │   ├── services/                  # Modality, Task, Profiler, Packager, Recommender, Validator
│   │   ├── trainers/                  # BaseTrainer, Tabular, Image, Text, TimeSeries trainers
│   │   ├── jobs/                      # Background worker managing AutoML training lifecycle
│   │   └── utils/                     # Hardware and resource-aware limits
│   └── tests/                         # Pytest test suite (Tabular, Image, Text, TimeSeries, E2E)
├── frontend/
│   ├── src/                           # React 18 + Vite frontend
│   │   ├── components/                # Navbar, Dropzone, Status badges, Metric cards
│   │   ├── pages/                     # Home, CreateModel, AnalysisView, TrainingView, ResultsView, Playground
│   │   └── services/                  # API client
│   └── dist/                          # Production build served directly by FastAPI
├── runtime_sdk/
│   ├── aiforge_runtime/               # Portable Python inference SDK
│   │   ├── loader.py                  # load_model() entrypoint
│   │   ├── model.py                   # AIForgeModel wrapper
│   │   ├── predictors/                # Tabular, Image, Text, TimeSeries inference wrappers
│   │   └── validators/                # Schema validation
│   └── setup.py                       # Pip-installable runtime package
├── storage/                           # Uploads, models, and SQLite database
├── docker/                            # Backend & Frontend Dockerfiles
├── docs/                              # Technical architecture specification
└── docker-compose.yml
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+ (Python 3.11 recommended)
- Node.js 18+ & npm
- (Optional) Docker & Docker Compose

### 1. Installation

#### Clone & Environment Setup
```bash
cd ai-model-forge

# Create and activate Python virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install backend dependencies
pip install fastapi "uvicorn[standard]" pydantic sqlalchemy python-multipart \
    numpy pandas scikit-learn pillow pytest requests openpyxl pyarrow joblib httpx \
    torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install runtime SDK in editable mode
pip install -e ./runtime_sdk
```

#### Frontend Setup & Build
```bash
cd frontend
npm install
npm run build
cd ..
```

---

## 🏃 Running the Application

### Option A: Local Run (FastAPI + Embedded Frontend)
FastAPI automatically serves the built React frontend at `http://localhost:8000`:
```bash
# From ai-model-forge directory with .venv activated:
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!

### Option B: Local Development (With Vite Hot-Reloading)
Run backend and frontend dev servers concurrently:
```bash
# Terminal 1: Backend
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Frontend
cd frontend
npm run dev
```
Open **[http://localhost:5173](http://localhost:5173)** in your browser.

### Option C: Docker Compose
```bash
docker-compose up --build
```
Access the application at `http://localhost:3000` (Frontend) and `http://localhost:8000` (API).

---

## 🧪 Running the Test Suite

Run the full automated test suite covering all supported modalities, trainers, packaging, and the end-to-end API:
```bash
pytest backend/tests -v
```

All 7 test suites verify:
- ✅ **API Health & Endpoints**
- ✅ **Tabular Classification & Regression Pipeline** (OneHotEncoder, StandardScaler, Random Forest, single .aiforge packaging, SDK prediction)
- ✅ **Image Classification Pipeline** (Corrupt image filtering, PyTorch MobileNetV2 transfer learning, SDK image prediction)
- ✅ **Text NLP Pipeline** (TF-IDF, Logistic Regression, SDK text inference)
- ✅ **Time Series Pipeline** (Chronological split, lag features, rolling statistics, forecasting)
- ✅ **Complete End-to-End API Flow** (Upload -> Analysis -> Training -> .aiforge download -> external runtime inference)

---

## 📦 Using the Downloaded `.aiforge` Model

The user receives **ONE single file** (e.g. `customer_churn_model.aiforge`).

### Install the lightweight Runtime SDK:
```bash
pip install aiforge-runtime
# Or from local source:
pip install ./runtime_sdk
```

### Tabular Inference:
```python
from aiforge_runtime import load_model

model = load_model("customer_churn_model.aiforge")

# Pass raw dictionaries or DataFrames - preprocessing happens automatically!
result = model.predict({
    "age": 32,
    "tenure_months": 14,
    "monthly_charges": 65.40,
    "contract_type": "two-year"
})

print(result)
# {
#   "prediction": "no",
#   "confidence": 0.941,
#   "probabilities": {"no": 0.941, "yes": 0.059},
#   "task": "TABULAR_CLASSIFICATION"
# }
```

### Image Inference:
```python
from aiforge_runtime import load_model

model = load_model("animal_classifier.aiforge")

# Pass image file path, raw bytes, or PIL Image
result = model.predict("cat.jpg")
print(result)
# {
#   "prediction": "cats",
#   "confidence": 0.985,
#   "probabilities": {"cats": 0.985, "dogs": 0.015},
#   "task": "IMAGE_CLASSIFICATION"
# }
```

### Text NLP Inference:
```python
from aiforge_runtime import load_model

model = load_model("sentiment_model.aiforge")

result = model.predict("The customer service was exceptional and arrived fast!")
print(result)
# {
#   "prediction": "positive",
#   "confidence": 0.972,
#   "probabilities": {"positive": 0.972, "negative": 0.028},
#   "task": "TEXT_CLASSIFICATION"
# }
```

---

## 🔒 Security & Privacy

1. **Path Traversal Protection (Zip Slip Prevention)**: Zip archives are strictly validated before extraction to ensure entries cannot write outside the target sandbox.
2. **Safe Artifact Inspection**: Model packages are verified with SHA-256 integrity checksums and internal descriptor validation. Arbitrary external executable code execution is disallowed.
3. **Privacy Preserving**: Full raw dataset contents are never transmitted to external third-party LLMs by default. Requirement understanding uses deterministic parsing with optional metadata-only LLM integration.

---

## 🗺️ Roadmap & Extension Architecture

AI Model Forge is built on a plugin-based `TrainerRegistry`:
- **v1.0 (Current)**:
  - Tabular Classification & Regression
  - Image Classification (Transfer Learning)
  - Text Classification (NLP TF-IDF)
  - Time-Series Forecasting (Lagged Regressors)
- **v2.0 (Planned Plugins)**:
  - Object Detection (YOLO / Faster-RCNN plugin)
  - Audio Classification & Acoustic feature extraction
  - Multimodal Fusion (Joint Vision + Tabular architectures)
  - ONNX runtime export option
