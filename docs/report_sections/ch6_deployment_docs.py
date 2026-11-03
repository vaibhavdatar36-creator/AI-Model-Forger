from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from .styles_and_canvas import create_callout_box, create_prompt_box

def generate_ch6(styles):
    story = []

    # Chapter Header
    story.append(Paragraph("6. DEPLOYMENT AND DOCUMENTATION", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=12))

    # 6.1 Deployment and Execution Procedure
    story.append(Paragraph("6.1 Deployment and Execution Procedure", styles['SectionHeader']))

    story.append(Paragraph(
        "AI Model Forge is engineered for zero-friction deployment across heterogeneous environments. It supports both "
        "native bare-metal execution (for developer workstations, educational computer labs, and on-premise servers) and "
        "production containerized deployment via Docker Compose. The architecture guarantees zero external cloud dependencies, "
        "enabling completely air-gapped offline operation.",
        styles['Paragraph']
    ))

    # Table 6.1: Hardware & System Requirements
    story.append(Paragraph("<b>Table 6.1: Hardware and System Requirements Specification</b>", styles['ParagraphBold']))

    hw_data = [
        [Paragraph("<b>Resource Metric</b>", styles['TableHead']), Paragraph("<b>Minimum Required Specification</b>", styles['TableHead']), Paragraph("<b>Recommended Production Specification</b>", styles['TableHead'])],
        [
            Paragraph("<b>Processor (CPU)</b>", styles['TableCellBold']),
            Paragraph("Dual-Core x86_64 or ARM64 (e.g. Intel Core i3 / Apple M1)", styles['TableCell']),
            Paragraph("Quad-Core or Octa-Core (Intel Core i7/i9, AMD Ryzen 7, Apple M2/M3)", styles['TableCell'])
        ],
        [
            Paragraph("<b>System Memory (RAM)</b>", styles['TableCellBold']),
            Paragraph("4 GB Physical RAM (2 GB dedicated to Python process)", styles['TableCell']),
            Paragraph("16 GB Physical RAM (handles datasets &gt; 500,000 rows)", styles['TableCell'])
        ],
        [
            Paragraph("<b>Storage Space</b>", styles['TableCellBold']),
            Paragraph("3 GB free disk space (virtual environment + model storage)", styles['TableCell']),
            Paragraph("20 GB NVMe SSD (fast staging and caching of large datasets)", styles['TableCell'])
        ],
        [
            Paragraph("<b>Operating System</b>", styles['TableCellBold']),
            Paragraph("Windows 10/11 (64-bit), Ubuntu 20.04+, macOS 12+", styles['TableCell']),
            Paragraph("Ubuntu Linux 22.04 LTS / Debian 12 (container host)", styles['TableCell'])
        ],
        [
            Paragraph("<b>Software Prerequisites</b>", styles['TableCellBold']),
            Paragraph("Python 3.11.x, Node.js 18+, uv package manager", styles['TableCell']),
            Paragraph("Docker 24.0+, Docker Compose v2.20+, Python 3.11", styles['TableCell'])
        ],
        [
            Paragraph("<b>GPU Acceleration</b>", styles['TableCellBold']),
            Paragraph("Not Required (Fully functional CPU-only mode)", styles['TableCell']),
            Paragraph("NVIDIA GPU with CUDA 12.x (Accelerates CV fine-tuning by 8x)", styles['TableCell'])
        ]
    ]

    t_hw = Table(hw_data, colWidths=[110, 185, 192])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_hw)
    story.append(Spacer(1, 10))

    # Table 6.2: Environment Configuration
    story.append(Paragraph("<b>Table 6.2: Platform Environment Configuration Variables</b>", styles['ParagraphBold']))

    env_data = [
        [Paragraph("<b>Variable Key</b>", styles['TableHead']), Paragraph("<b>Default Value</b>", styles['TableHead']), Paragraph("<b>Operational Function & Description</b>", styles['TableHead'])],
        [
            Paragraph("<code>AIFORGE_ENV</code>", styles['TableCellBold']),
            Paragraph("<code>development</code>", styles['TableCell']),
            Paragraph("Environment profile: 'development' enables detailed stack traces; 'production' hardens errors.", styles['TableCell'])
        ],
        [
            Paragraph("<code>AIFORGE_PORT</code>", styles['TableCellBold']),
            Paragraph("<code>8000</code>", styles['TableCell']),
            Paragraph("TCP port on which the FastAPI ASGI server listens for client requests.", styles['TableCell'])
        ],
        [
            Paragraph("<code>AIFORGE_STORAGE_DIR</code>", styles['TableCellBold']),
            Paragraph("<code>./storage</code>", styles['TableCell']),
            Paragraph("Directory where uploaded datasets, training logs, and packaged .aiforge artifacts are stored.", styles['TableCell'])
        ],
        [
            Paragraph("<code>AIFORGE_MAX_UPLOAD_SIZE</code>", styles['TableCellBold']),
            Paragraph("<code>250MB</code>", styles['TableCell']),
            Paragraph("Maximum allowable file upload size to prevent denial-of-service memory exhaustion.", styles['TableCell'])
        ],
        [
            Paragraph("<code>AIFORGE_WORKER_CONCURRENCY</code>", styles['TableCellBold']),
            Paragraph("<code>2</code>", styles['TableCell']),
            Paragraph("Maximum number of simultaneous AutoML training jobs executed by background workers.", styles['TableCell'])
        ],
        [
            Paragraph("<code>AIFORGE_CORS_ORIGINS</code>", styles['TableCellBold']),
            Paragraph("<code>*</code>", styles['TableCell']),
            Paragraph("Allowed Cross-Origin Resource Sharing domains (restricted to frontend origin in production).", styles['TableCell'])
        ]
    ]

    t_env = Table(env_data, colWidths=[140, 105, 242])
    t_env.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_env)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Option A: Native Bare-Metal Local Deployment</b>", styles['ParagraphBold']))
    story.append(Paragraph(
        "In native deployment mode, the React frontend is compiled into static production assets (<code>frontend/dist</code>) "
        "and mounted directly onto the FastAPI ASGI server via <code>StaticFiles</code>. This allows the complete system (API and UI) "
        "to run on a single unified port (<code>8000</code>) with zero reverse-proxy overhead.",
        styles['Paragraph']
    ))

    local_steps = (
        "# Step 1: Clone or navigate to the project root\n"
        "cd C:\\Users\\Vaibhav\\.gemini\\antigravity\\scratch\\ai-model-forge\n\n"
        "# Step 2: Activate Python 3.11 virtual environment\n"
        ".\\.venv\\Scripts\\activate          # Windows PowerShell\n"
        "# source .venv/bin/activate       # Linux / macOS\n\n"
        "# Step 3: Compile React frontend production assets\n"
        "cd frontend\n"
        "npm install --silent\n"
        "npm run build\n"
        "cd ..\n\n"
        "# Step 4: Launch unified FastAPI backend and UI server\n"
        "python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload\n"
        "# Web Studio:   http://localhost:8000\n"
        "# Swagger Docs: http://localhost:8000/docs\n"
        "# Health API:   http://localhost:8000/api/health"
    )
    story.append(Paragraph(f"<font face='Courier' size='7.5'>{local_steps.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", styles['CodeBlock']))
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Option B: Production Containerized Deployment (Docker Compose)</b>", styles['ParagraphBold']))
    story.append(Paragraph(
        "For multi-tenant cloud and Kubernetes deployments, Docker Compose orchestrates two microservices: a Python 3.11 backend "
        "container hosting FastAPI, PyTorch, and Scikit-Learn, and an Nginx alpine container serving the optimized React frontend on port 3000.",
        styles['Paragraph']
    ))

    docker_steps = (
        "# Step 1: Build and launch all microservices in detached mode\n"
        "docker-compose up --build -d\n\n"
        "# Step 2: Verify container health and logs\n"
        "docker-compose ps\n"
        "docker-compose logs -f backend\n\n"
        "# Access points:\n"
        "# Web Studio UI:  http://localhost:3000\n"
        "# REST API Docs:  http://localhost:8000/docs\n"
        "# Health Probe:   http://localhost:8000/api/health"
    )
    story.append(Paragraph(f"<font face='Courier' size='7.5'>{docker_steps.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Listing 6.1: Multi-Stage Production Docker Compose Specification (docker-compose.yml)</b>", styles['ParagraphBold']))
    dc_code = (
        "version: '3.8'\n"
        "services:\n"
        "  backend:\n"
        "    build:\n"
        "      context: .\n"
        "      dockerfile: docker/Dockerfile.backend\n"
        "    ports:\n"
        "      - '8000:8000'\n"
        "    environment:\n"
        "      - AIFORGE_ENV=production\n"
        "      - AIFORGE_STORAGE_DIR=/app/storage\n"
        "    volumes:\n"
        "      - aiforge_storage:/app/storage\n"
        "    restart: unless-stopped\n\n"
        "  frontend:\n"
        "    build:\n"
        "      context: ./frontend\n"
        "      dockerfile: ../docker/Dockerfile.frontend\n"
        "    ports:\n"
        "      - '3000:80'\n"
        "    depends_on:\n"
        "      - backend\n"
        "    restart: unless-stopped\n\n"
        "volumes:\n"
        "  aiforge_storage:\n"
        "    driver: local"
    )
    story.append(Paragraph(f"<font face='Courier' size='7.5'>{dc_code.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Listing 6.2: Multi-Stage Backend Dockerfile with uv Toolchain (docker/Dockerfile.backend)</b>", styles['ParagraphBold']))
    df_code = (
        "FROM python:3.11-slim as builder\n"
        "WORKDIR /app\n"
        "RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential && rm -rf /var/lib/apt/lists/*\n"
        "RUN pip install --no-cache-dir uv\n"
        "COPY pyproject.toml README.md ./\n"
        "COPY runtime_sdk ./runtime_sdk\n"
        "RUN uv pip install --system --no-cache -e ./runtime_sdk torch torchvision --index-url https://download.pytorch.org/whl/cpu\n"
        "COPY backend ./backend\n"
        "EXPOSE 8000\n"
        "CMD [\"uvicorn\", \"backend.app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
    )
    story.append(Paragraph(f"<font face='Courier' size='7.5'>{df_code.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", styles['CodeBlock']))
    story.append(Spacer(1, 8))

    # Linux systemd service
    story.append(Paragraph("<b>Option C: Linux Production Daemon (systemd Service)</b>", styles['ParagraphBold']))
    story.append(Paragraph(
        "For unattended Linux server deployments, the platform can be configured as a systemd service with automatic restarts "
        "and journald logging integration:",
        styles['Paragraph']
    ))

    systemd_code = (
        "[Unit]\n"
        "Description=AI Model Forge AutoML Platform Service\n"
        "After=network.target\n\n"
        "[Service]\n"
        "Type=simple\n"
        "User=www-data\n"
        "WorkingDirectory=/var/www/ai-model-forge\n"
        "ExecStart=/var/www/ai-model-forge/.venv/bin/uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --workers 4\n"
        "Restart=always\n"
        "RestartSec=5s\n"
        "Environment=AIFORGE_ENV=production\n"
        "Environment=AIFORGE_STORAGE_DIR=/var/www/ai-model-forge/storage\n\n"
        "[Install]\n"
        "WantedBy=multi-user.target"
    )
    story.append(Paragraph(f"<font face='Courier' size='7.5'>{systemd_code.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", styles['CodeBlock']))
    story.append(Spacer(1, 10))

    # 6.2 Deployment Prompts and Configuration
    story.append(Paragraph("6.2 Deployment Prompts and Configuration", styles['SectionHeader']))

    story.append(create_prompt_box(
        "Multi-Stage Dockerfile Synthesis for Lightweight Production Builds",
        "Prompt: 'Generate a production-ready docker-compose.yml and multi-stage Dockerfiles for backend and frontend. "
        "The backend must install Python 3.11, uv, PyTorch CPU wheels, Scikit-Learn, and editable runtime_sdk. "
        "The frontend must use a node:20-alpine build stage and an nginx:alpine serving stage to minimize image size.'",
        "The AI produced docker/Dockerfile.backend (using python:3.11-slim, installing uv and caching PyTorch CPU wheels) "
        "and docker/Dockerfile.frontend (multi-stage build compiling Vite assets into Nginx html root). The compose file "
        "mounts storage/ as a persistent volume and maps ports 3000 and 8000 cleanly.",
        styles
    ))
    story.append(Spacer(1, 6))

    story.append(create_prompt_box(
        "Reverse-Proxy Nginx Configuration with Asset Caching",
        "Prompt: 'Write an optimized nginx.conf for serving the React frontend. It must proxy /api requests to the FastAPI backend "
        "at backend:8000, enable gzip compression for JSON and JS assets, configure 1-year immutable cache headers for static chunks, "
        "and implement try_files $uri $uri/ /index.html for client-side React Router navigation.'",
        "The AI generated the Nginx server block with upstream proxying, client body size set to 250M, gzip compression ratio 6, "
        "and correct SPA routing fallback.",
        styles
    ))

    story.append(Spacer(1, 10))

    # 6.3 User Manual and Technical Documentation
    story.append(Paragraph("6.3 User Manual and Technical Documentation", styles['SectionHeader']))

    story.append(Paragraph(
        "<b>Part I: Comprehensive Operator Guide for the Web Studio:</b>",
        styles['ParagraphBold']
    ))
    story.append(Paragraph("1. <b>Accessing the Studio:</b> Open any modern web browser and navigate to <code>http://localhost:8000</code> (or <code>http://localhost:3000</code> in Docker). The dark-themed landing page greets the operator with real-time hardware status indicators (CPU, RAM, and storage health).", styles['BulletItem']))
    story.append(Paragraph("2. <b>Initiating Model Creation:</b> Click the prominent 'Build Your AI Model Now' call-to-action button or 'Create Model' in the top navigation bar. The 3-step creation wizard appears.", styles['BulletItem']))
    story.append(Paragraph("3. <b>Providing Natural Language Intent:</b> Enter a project title and describe your objective in plain English (e.g., <i>'Predict customer churn from tenure and monthly charges'</i> or <i>'Classify cat and dog pet photos'</i>). Quick-fill sample chips are available for instant testing.", styles['BulletItem']))
    story.append(Paragraph("4. <b>Uploading Multimodal Data:</b> Drag and drop your raw file into the upload dropzone. Supported formats include tabular data (<code>.csv</code>, <code>.xlsx</code>, <code>.parquet</code>, <code>.json</code>) and image/text archives (<code>.zip</code>). The client validates file size and format before transmitting.", styles['BulletItem']))
    story.append(Paragraph("5. <b>Automated Strategy Review:</b> Click 'ANALYZE & BUILD MODEL'. The heuristic scanner inspects your data and displays detected Modality, Task, Target candidates, and ranked algorithm recommendations. If desired, expand 'Show Advanced Settings' to manually override target columns, test split ratios, or algorithm selections.", styles['BulletItem']))
    story.append(Paragraph("6. <b>Real-Time Training Telemetry:</b> Click 'CONFIRM & TRAIN MODEL'. The live telemetry dashboard tracks progress across 5 distinct stages (Validation, Preprocessing, Benchmarking, Champion Selection, and Packaging). Click 'Show Technical Engine Logs' to inspect real-time console messages and loss curves.", styles['BulletItem']))
    story.append(Paragraph("7. <b>Retrieving the Champion Model:</b> Upon completion, the Results view showcases the Champion Model badge, accuracy/F1 scorecards, confusion matrix, and candidate model comparison table. Click 'DOWNLOAD .AIFORGE' to save the self-contained single-file model package.", styles['BulletItem']))
    story.append(Paragraph("8. <b>Interactive In-Browser Playground:</b> Click 'Test in Live Playground'. Fill in tabular input fields or upload an image to receive instant predictions, confidence meters, and class probability distributions rendered directly in the browser.", styles['BulletItem']))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Part II: Comprehensive Developer Guide for the aiforge_runtime SDK:</b>",
        styles['ParagraphBold']
    ))
    story.append(Paragraph(
        "The <code>aiforge_runtime</code> package is a standalone, lightweight Python package designed to execute predictions "
        "with zero training-serving skew. The model package encapsulates all ColumnTransformers, scalers, encoders, and neural weights.",
        styles['Paragraph']
    ))

    # SDK Code Recipes
    story.append(Paragraph("<b>Recipe 1: Single-Record Dictionary Prediction (Tabular)</b>", styles['SubSectionHeader']))
    sdk_code1 = (
        "from aiforge_runtime import load_model\n\n"
        "# Load standalone package (zero server dependency)\n"
        "model = load_model('customer_churn_model.aiforge')\n"
        "print('Task:', model.task)             # TABULAR_CLASSIFICATION\n"
        "print('Champion:', model.model_type)    # Random Forest Classifier\n\n"
        "# Raw dictionary - preprocessing is 100% automated!\n"
        "record = {'age': 42, 'tenure_months': 18, 'monthly_charges': 79.50, 'contract_type': 'month-to-month'}\n"
        "res = model.predict(record)\n"
        "print(res)\n"
        "# {'prediction': 'yes', 'confidence': 0.884, 'probabilities': {'no': 0.116, 'yes': 0.884}}"
    )
    story.append(Paragraph(f"<font face='Courier' size='7.5'>{sdk_code1.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Recipe 2: High-Throughput Batch Scoring on Pandas DataFrame</b>", styles['SubSectionHeader']))
    sdk_code2 = (
        "import pandas as pd\n"
        "from aiforge_runtime import load_model\n\n"
        "model = load_model('customer_churn_model.aiforge')\n"
        "df_batch = pd.read_csv('unlabeled_customers.csv')\n\n"
        "# Score 10,000 records in one vectorized call\n"
        "predictions = model.predict_batch(df_batch)\n"
        "df_batch['churn_pred'] = [p['prediction'] for p in predictions]\n"
        "df_batch['confidence'] = [p['confidence'] for p in predictions]\n"
        "df_batch.to_csv('scored_customers.csv', index=False)"
    )
    story.append(Paragraph(f"<font face='Courier' size='7.5'>{sdk_code2.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Recipe 3: Computer Vision Image Classification</b>", styles['SubSectionHeader']))
    sdk_code3 = (
        "from aiforge_runtime import load_model\n"
        "from PIL import Image\n\n"
        "cv_model = load_model('pet_classifier.aiforge')\n"
        "# Accepts file path, PIL Image, or raw byte stream\n"
        "result = cv_model.predict('sample_dog.jpg')\n"
        "print(f\"Predicted: {result['prediction']} (Confidence: {result['confidence']*100:.1f}%)\")"
    )
    story.append(Paragraph(f"<font face='Courier' size='7.5'>{sdk_code3.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", styles['CodeBlock']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Recipe 4: Deploying .aiforge as a Microservice REST API in 15 Lines</b>", styles['SubSectionHeader']))
    sdk_code4 = (
        "from fastapi import FastAPI\n"
        "from aiforge_runtime import load_model\n\n"
        "app = FastAPI(title='Production Churn Predictor Microservice')\n"
        "model = load_model('customer_churn_model.aiforge')\n\n"
        "@app.post('/predict')\n"
        "def predict_churn(payload: dict):\n"
        "    return model.predict(payload)\n\n"
        "# Run: uvicorn microservice:app --port 9000"
    )
    story.append(Paragraph(f"<font face='Courier' size='7.5'>{sdk_code4.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", styles['CodeBlock']))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Part III: Complete cURL REST API Cheatsheet:</b>",
        styles['ParagraphBold']
    ))
    story.append(Paragraph(
        "Third-party external enterprise systems can fully automate model training and inference via HTTP REST calls:",
        styles['Paragraph']
    ))

    curl_cheatsheet = (
        "# 1. Health check probe\n"
        "curl -X GET http://localhost:8000/api/health\n\n"
        "# 2. Upload dataset\n"
        "curl -X POST http://localhost:8000/api/upload \\\n"
        "  -F \"file=@customer_churn.csv\"\n\n"
        "# 3. Trigger autonomous analysis\n"
        "curl -X POST http://localhost:8000/api/analyze \\\n"
        "  -H \"Content-Type: application/json\" \\\n"
        "  -d '{\"dataset_id\": \"ds_981a\", \"requirement\": \"Predict customer churn\"}'\n\n"
        "# 4. Launch training job\n"
        "curl -X POST http://localhost:8000/api/train \\\n"
        "  -H \"Content-Type: application/json\" \\\n"
        "  -d '{\"dataset_id\": \"ds_981a\", \"target_column\": \"churn\"}'\n\n"
        "# 5. Poll job status\n"
        "curl -X GET http://localhost:8000/api/jobs/job_4821\n\n"
        "# 6. Download .aiforge package\n"
        "curl -O http://localhost:8000/api/models/mod_8123/download"
    )
    story.append(Paragraph(f"<font face='Courier' size='7.5'>{curl_cheatsheet.replace(chr(10), '<br/>').replace(' ', '&nbsp;')}</font>", styles['CodeBlock']))

    story.append(PageBreak())
    return story
