from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from .styles_and_canvas import create_callout_box, create_prompt_box

def generate_ch2(styles):
    story = []

    # Chapter Header
    story.append(Paragraph("2. REQUIREMENT ANALYSIS", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=12))

    # 2.1 Functional and Non-Functional Requirements
    story.append(Paragraph("2.1 Functional and Non-Functional Requirements", styles['SectionHeader']))

    story.append(Paragraph(
        "A rigorous requirement engineering process was conducted to establish exact system boundaries, user interaction "
        "paradigms, security parameters, and autonomous decision thresholds. The requirements are categorized into Functional "
        "Requirements (FR) and Non-Functional Requirements (NFR).",
        styles['Paragraph']
    ))

    story.append(Paragraph("<b>Table 2.1: Functional Requirements Specification (FR-01 to FR-15)</b>", styles['ParagraphBold']))

    fr_data = [
        [Paragraph("<b>Req ID</b>", styles['TableHead']), Paragraph("<b>Requirement Name</b>", styles['TableHead']), Paragraph("<b>Detailed Functional Specification</b>", styles['TableHead']), Paragraph("<b>Priority</b>", styles['TableHead'])],
        [
            Paragraph("<b>FR-01</b>", styles['TableCellBold']),
            Paragraph("Multi-Format Ingestion", styles['TableCellBold']),
            Paragraph("The system shall accept raw dataset uploads in CSV, XLSX, XLS, JSON, JSONL, Parquet, and ZIP formats up to 500 MB without prior preprocessing.", styles['TableCell']),
            Paragraph("CRITICAL", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-02</b>", styles['TableCellBold']),
            Paragraph("Modality Detection", styles['TableCellBold']),
            Paragraph("The system shall autonomously inspect file extensions, MIME signatures, folder structures, and sample contents to determine modality (TABULAR, IMAGE, TEXT, TIME_SERIES, AUDIO, VIDEO, DOCUMENT) with an associated confidence metric.", styles['TableCell']),
            Paragraph("CRITICAL", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-03</b>", styles['TableCellBold']),
            Paragraph("Natural Language Requirement Parsing", styles['TableCellBold']),
            Paragraph("The system shall parse user natural language problem statements, extract the core objective, candidate target column, task type, and detect unsupported operations.", styles['TableCell']),
            Paragraph("HIGH", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-04</b>", styles['TableCellBold']),
            Paragraph("Transparent Task Boundary Enforcement", styles['TableCellBold']),
            Paragraph("If the parsed intent requires unsupported tasks (e.g., Object Detection, Video Action Recognition, Speech-to-Text), the system shall reject training with a clear explanation rather than training an inappropriate model.", styles['TableCell']),
            Paragraph("CRITICAL", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-05</b>", styles['TableCellBold']),
            Paragraph("Automated Data Profiling", styles['TableCellBold']),
            Paragraph("The system shall profile datasets to discover numerical, categorical, datetime, text, ID, and constant columns, computing missingness rates and class balance distributions.", styles['TableCell']),
            Paragraph("HIGH", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-06</b>", styles['TableCellBold']),
            Paragraph("Automated Feature Engineering (Tabular)", styles['TableCellBold']),
            Paragraph("The system shall construct Scikit-Learn ColumnTransformer pipelines applying median imputation and standard scaling to numericals, and most-frequent imputation and OneHotEncoder(handle_unknown='ignore') to categoricals.", styles['TableCell']),
            Paragraph("CRITICAL", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-07</b>", styles['TableCellBold']),
            Paragraph("ID & Leakage Column Exclusion", styles['TableCellBold']),
            Paragraph("The system shall identify and exclude identifiers (e.g., customer_id, uuid) and columns possessing extreme target correlation (|r| >= 0.99) to prevent artificial metric inflation.", styles['TableCell']),
            Paragraph("HIGH", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-08</b>", styles['TableCellBold']),
            Paragraph("Computer Vision Pipeline", styles['TableCellBold']),
            Paragraph("The system shall validate image readability, filter corrupted JPEG/PNG files, standardize to 224x224 RGB, apply data augmentation, and fine-tune PyTorch MobileNetV2 / ResNet18 backbones.", styles['TableCell']),
            Paragraph("CRITICAL", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-09</b>", styles['TableCellBold']),
            Paragraph("Natural Language Processing Pipeline", styles['TableCellBold']),
            Paragraph("The system shall normalize Unicode text, strip empty records, construct sublinear TF-IDF n-gram vectorizers (1,2), and train Logistic Regression / Linear SVM classifiers.", styles['TableCell']),
            Paragraph("CRITICAL", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-10</b>", styles['TableCellBold']),
            Paragraph("Chronological Time-Series Splitting", styles['TableCellBold']),
            Paragraph("The system shall strictly sort temporal series by timestamp, construct lag windows (t-1, t-2, t-3) and rolling means, and split train/test chronologically without random shuffling to avoid lookahead leakage.", styles['TableCell']),
            Paragraph("CRITICAL", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-11</b>", styles['TableCellBold']),
            Paragraph("Candidate Model Benchmarking", styles['TableCellBold']),
            Paragraph("The system shall train at least 2-3 candidate architectures per task, evaluating accuracy, F1-macro, weighted-F1, precision, recall, and confusion matrix (classification) or RMSE, MAE, and R2 (regression).", styles['TableCell']),
            Paragraph("HIGH", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-12</b>", styles['TableCellBold']),
            Paragraph("Champion Model Selection", styles['TableCellBold']),
            Paragraph("The system shall autonomously designate the champion model based on task-appropriate primary metrics (e.g., F1-macro for imbalanced classification, RMSE for regression).", styles['TableCell']),
            Paragraph("HIGH", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-13</b>", styles['TableCellBold']),
            Paragraph("Single-File Container Packaging (.aiforge)", styles['TableCellBold']),
            Paragraph("The system shall package champion weights, preprocessing transformers, schemas, metadata, and SHA-256 manifest into exactly ONE downloadable .aiforge archive file.", styles['TableCell']),
            Paragraph("CRITICAL", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-14</b>", styles['TableCellBold']),
            Paragraph("Pre-Download Sanity Verification", styles['TableCellBold']),
            Paragraph("Before making .aiforge available, the system shall reload the package via runtime SDK, pass a holdout sample, verify prediction format, and check archive checksum integrity.", styles['TableCell']),
            Paragraph("CRITICAL", styles['TableCell'])
        ],
        [
            Paragraph("<b>FR-15</b>", styles['TableCellBold']),
            Paragraph("Interactive In-Browser Testing Sandbox", styles['TableCellBold']),
            Paragraph("The web application shall provide an interactive testing playground allowing users to input raw values, text, or images and view real-time predictions, confidence scores, and class probability meters.", styles['TableCell']),
            Paragraph("MEDIUM", styles['TableCell'])
        ]
    ]

    fr_table = Table(fr_data, colWidths=[45, 105, 275, 62])
    fr_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(fr_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Table 2.2: Non-Functional Requirements Specification (NFR-01 to NFR-10)</b>", styles['ParagraphBold']))

    nfr_data = [
        [Paragraph("<b>Req ID</b>", styles['TableHead']), Paragraph("<b>Quality Attribute</b>", styles['TableHead']), Paragraph("<b>Non-Functional Specification & Constraint</b>", styles['TableHead']), Paragraph("<b>Metric / Benchmark</b>", styles['TableHead'])],
        [
            Paragraph("<b>NFR-01</b>", styles['TableCellBold']),
            Paragraph("Inference Latency", styles['TableCellBold']),
            Paragraph("The aiforge_runtime SDK shall execute tabular prediction and feature transformations in sub-millisecond to low-millisecond time.", styles['TableCell']),
            Paragraph("< 15 ms per tabular record; < 100 ms for vision on CPU", styles['TableCell'])
        ],
        [
            Paragraph("<b>NFR-02</b>", styles['TableCellBold']),
            Paragraph("Memory Awareness", styles['TableCellBold']),
            Paragraph("The system shall profile large tabular datasets exceeding 50 MB using chunked sampling (50,000 rows) to prevent out-of-memory (OOM) fatal crashes.", styles['TableCell']),
            Paragraph("Max heap footprint < 1.5 GB on CPU", styles['TableCell'])
        ],
        [
            Paragraph("<b>NFR-03</b>", styles['TableCellBold']),
            Paragraph("Security & Zip Slip Prevention", styles['TableCellBold']),
            Paragraph("Uploaded ZIP archives shall be validated against path traversal (../ or absolute paths) prior to extraction into an isolated temporary workspace.", styles['TableCell']),
            Paragraph("Zero path escape vulnerability (100% path verification)", styles['TableCell'])
        ],
        [
            Paragraph("<b>NFR-04</b>", styles['TableCellBold']),
            Paragraph("No Execution of Untrusted Code", styles['TableCellBold']),
            Paragraph("The server shall never execute uploaded Python scripts, shell scripts, or deserialize arbitrary external unverified pickle objects.", styles['TableCell']),
            Paragraph("Strict zero-code-execution policy on untrusted uploads", styles['TableCell'])
        ],
        [
            Paragraph("<b>NFR-05</b>", styles['TableCellBold']),
            Paragraph("Asynchronous Non-Blocking HTTP", styles['TableCellBold']),
            Paragraph("Long-running AutoML training routines shall execute on background worker threads, returning immediate job IDs and streaming status.", styles['TableCell']),
            Paragraph("HTTP POST /api/train response time < 350 ms", styles['TableCell'])
        ],
        [
            Paragraph("<b>NFR-06</b>", styles['TableCellBold']),
            Paragraph("Cross-Platform Portability", styles['TableCellBold']),
            Paragraph("The entire codebase and .aiforge packages shall operate seamlessly across Windows 10/11, Ubuntu Linux, and macOS without platform lock.", styles['TableCell']),
            Paragraph("Verified on Windows and Linux containers", styles['TableCell'])
        ],
        [
            Paragraph("<b>NFR-07</b>", styles['TableCellBold']),
            Paragraph("Data Privacy & Local Execution", styles['TableCellBold']),
            Paragraph("Raw customer datasets shall never be transmitted to external cloud LLM endpoints. All profiling and training must execute locally.", styles['TableCell']),
            Paragraph("100% on-premise execution; zero outbound telemetry", styles['TableCell'])
        ],
        [
            Paragraph("<b>NFR-08</b>", styles['TableCellBold']),
            Paragraph("Hardware Adaptability", styles['TableCellBold']),
            Paragraph("The training engine shall detect CPU cores, RAM, and CUDA availability, automatically adjusting batch sizes, epochs, and parallel worker threads.", styles['TableCell']),
            Paragraph("Graceful fallback to CPU if CUDA is unavailable", styles['TableCell'])
        ],
        [
            Paragraph("<b>NFR-09</b>", styles['TableCellBold']),
            Paragraph("Extensibility & Plugin Modularity", styles['TableCellBold']),
            Paragraph("New modalities (e.g. Audio, Video, Object Detection) must be implementable by registering a single BaseTrainer subclass without core rewrites.", styles['TableCell']),
            Paragraph("Zero modifications to API routing or packaging core", styles['TableCell'])
        ],
        [
            Paragraph("<b>NFR-10</b>", styles['TableCellBold']),
            Paragraph("Data Documentation Integrity", styles['TableCellBold']),
            Paragraph("Every model package shall generate an exhaustive, transparent Model Card detailing training sample counts, features, metrics, and limitations.", styles['TableCell']),
            Paragraph("Embedded in metadata.json within .aiforge", styles['TableCell'])
        ]
    ]

    nfr_table = Table(nfr_data, colWidths=[45, 100, 240, 102])
    nfr_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(nfr_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Table 2.3: Operational Dataset Scale Tiers and Resource Budgets</b>", styles['ParagraphBold']))

    scale_data = [
        [Paragraph("<b>Scale Tier</b>", styles['TableHead']), Paragraph("<b>Dataset Size Bounds</b>", styles['TableHead']), Paragraph("<b>Automated Profiling Strategy</b>", styles['TableHead']), Paragraph("<b>Candidate Models & Budget</b>", styles['TableHead']), Paragraph("<b>Target Hardware Execution</b>", styles['TableHead'])],
        [
            Paragraph("<b>Small Tier</b>", styles['TableCellBold']),
            Paragraph("< 2,000 rows / < 5 MB", styles['TableCell']),
            Paragraph("Full in-memory profiling, full descriptive statistics, zero down-sampling", styles['TableCell']),
            Paragraph("3-4 candidates; 100 estimators; full 5-fold cross-validation", styles['TableCell']),
            Paragraph("Standard multi-core CPU (< 10 seconds)", styles['TableCell'])
        ],
        [
            Paragraph("<b>Medium Tier</b>", styles['TableCellBold']),
            Paragraph("2,000 - 50,000 rows / 5 - 50 MB", styles['TableCell']),
            Paragraph("Full in-memory loading, parallel dtype profiling, automated correlation matrix", styles['TableCell']),
            Paragraph("3 candidates; 75 estimators; stratified holdout split (80/20)", styles['TableCell']),
            Paragraph("Multi-core CPU (10 - 45 seconds)", styles['TableCell'])
        ],
        [
            Paragraph("<b>Large Tier</b>", styles['TableCellBold']),
            Paragraph("50,000 - 500,000 rows / 50 - 250 MB", styles['TableCell']),
            Paragraph("Chunked CSV ingestion, 50,000-row representative random sampling for profiling", styles['TableCell']),
            Paragraph("2 top candidates; HistGradientBoosting with binned histograms (max_iter=100)", styles['TableCell']),
            Paragraph("Fast CPU / CUDA acceleration (< 2 minutes)", styles['TableCell'])
        ],
        [
            Paragraph("<b>Extreme Tier</b>", styles['TableCellBold']),
            Paragraph("> 500,000 rows / 250 - 500 MB", styles['TableCell']),
            Paragraph("Parquet conversion, memory-mapped streaming, strict 25,000-row sampling for search", styles['TableCell']),
            Paragraph("Fast histogram gradient boosting; linear SGD baseline; early stopping patience=5", styles['TableCell']),
            Paragraph("Dedicated worker thread / GPU pool (< 5 minutes)", styles['TableCell'])
        ]
    ]

    scale_table = Table(scale_data, colWidths=[65, 80, 130, 115, 97])
    scale_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(scale_table)
    story.append(Spacer(1, 10))

    # 2.2 User Stories and Acceptance Criteria
    story.append(Paragraph("2.2 User Stories and Acceptance Criteria", styles['SectionHeader']))

    story.append(Paragraph(
        "To ensure user-centric design and testable requirements, twelve core user stories were developed spanning business analysts, "
        "software developers, and computer vision engineers. Acceptance criteria are expressed using standard Gherkin Given-When-Then syntax.",
        styles['Paragraph']
    ))

    user_stories = [
        (
            "US-01: Autonomous Tabular Customer Churn Classification",
            "As a business product manager with no data science background, I want to upload a raw CSV containing customer demographic and subscription details, describe my intent as 'predict customer churn', and receive a trained champion model package so that our CRM software can predict which users are at risk of leaving.",
            "Given a raw CSV dataset containing customer demographics, tenure, charges, contract types, and a binary churn label;\n"
            "When the user uploads the file and inputs 'Predict customer churn' in Simple Mode;\n"
            "Then the system must identify Tabular Classification, automatically impute missing numeric values with medians, One-Hot Encode contract types with unknown handling, train Random Forest and Gradient Boosting models, select the champion model based on F1-macro, and package it into a single .aiforge file within 60 seconds."
        ),
        (
            "US-02: Single-File Artifact Inference in External Python Code",
            "As a backend Python developer building an automated customer portal, I want to load the downloaded customer churn model using a lightweight runtime SDK and pass un-preprocessed raw JSON dictionaries so that I do not need to import or replicate training-time encoders and scalers.",
            "Given a downloaded .aiforge model artifact and the installed aiforge_runtime package;\n"
            "When the developer calls model = load_model('churn_model.aiforge') and passes a raw dictionary {'age': 35, 'tenure_months': 14, 'monthly_charges': 65.4, 'contract_type': 'two-year'};\n"
            "Then the SDK must validate the schema, execute preprocessing transformations internally, and return a dictionary containing {'prediction': 'no', 'confidence': 0.942, 'probabilities': {...}} in under 15 milliseconds."
        ),
        (
            "US-03: Computer Vision Transfer Learning from Image Folders",
            "As a computer vision software engineer, I want to upload a ZIP archive of categorized image directories (e.g., cats/ and dogs/) and state 'Classify images of cats and dogs' so that the platform trains a fine-tuned convolutional neural network without requiring manual PyTorch training loops.",
            "Given a ZIP archive containing structured subdirectories of JPEG/PNG images;\n"
            "When the user uploads the archive and clicks 'Analyze & Build Model';\n"
            "Then the system must discover class folders, filter out corrupt/unreadable images, resize to 224x224 RGB, apply rotation and flip augmentations, fine-tune MobileNetV2, evaluate accuracy and confusion matrix on holdout images, and produce a verified .aiforge package."
        ),
        (
            "US-04: Transparent Rejection of Unsupported Advanced Tasks",
            "As a robotics engineer, I want to enter 'Detect pedestrians and cars using bounding boxes in road images' so that the platform honestly tells me if object detection is unsupported instead of falsely training an image classifier.",
            "Given a natural language requirement requesting bounding-box object detection;\n"
            "When the requirement analyzer executes task detection;\n"
            "Then the system must mark is_supported=False, display an honest alert explaining that Object Detection is slated for a future trainer plugin, and disable the train button to prevent inaccurate training."
        ),
        (
            "US-05: Non-Leakage Chronological Time-Series Forecasting",
            "As an energy analyst, I want to upload hourly electricity demand logs and forecast demand for future periods without information leaking from future timestamps into past features.",
            "Given a sequential tabular dataset containing hourly timestamps and energy demand values;\n"
            "When the system detects time-series structure;\n"
            "Then it must sort chronologically, engineer lag features (t-1, t-2, t-3) and rolling 3-hour means, apply a strict chronological train/test split without random shuffling, and evaluate RMSE on the latest 20% holdout period."
        ),
        (
            "US-06: Automatic Identifier and Target Leakage Elimination",
            "As a data scientist, I want the system to detect and exclude primary key IDs and target-derivative features so that the model does not achieve artificially high, meaningless training metrics.",
            "Given a dataset containing a customer_id column and a column identical to the target;\n"
            "When the dataset profiler and TabularDataEngineer inspect the data matrix;\n"
            "Then customer_id must be excluded from feature vectors, and the target-duplicate column must be flagged and omitted from model inputs."
        ),
        (
            "US-07: Real-Time Telemetry and Technical Log Streaming",
            "As a software engineer monitoring training jobs, I want to view live progress percentage, step descriptions, and collapsible terminal logs so that I have complete visibility into the training lifecycle.",
            "Given an active AutoML training background job;\n"
            "When viewing the TrainingView page;\n"
            "Then the UI must poll job status every 1.5 seconds, update an animated progress bar, show active steps (Analyzing, Preprocessing, Training, Evaluating, Packaging), and display real-time engine logs in an expandable terminal viewer."
        ),
        (
            "US-08: In-Browser Model Prediction Playground",
            "As an end user evaluating a freshly trained model, I want to test the model immediately in the browser by typing inputs or uploading an image so that I can qualitatively verify model behavior before exporting it.",
            "Given a completed training job with a packaged model artifact;\n"
            "When the user navigates to the Playground tab;\n"
            "Then the web interface must render input fields dynamically generated from schema.json, accept sample inputs, execute server-side prediction via load_model(), and display predicted class, confidence percentage, and probability distribution bars."
        ),
        (
            "US-09: Automated Real-Time Text NLP Sentiment Classification",
            "As an e-commerce customer support manager, I want to upload customer feedback CSVs and train a sentiment model to flag negative complaints in real time.",
            "Given a CSV containing unformatted text reviews and positive/negative labels;\n"
            "When the system ingests the dataset;\n"
            "Then it must normalize Unicode, build a sublinear TF-IDF n-gram vectorizer, train Logistic Regression, and package a model capable of classifying raw text strings with calibrated confidence probabilities."
        ),
        (
            "US-10: Target Column Ambiguity Confirmation Protocol",
            "As an analytical user uploading a medical dataset with multiple diagnostic columns (e.g. disease_type, disease_status), I want the system to prompt me for confirmation rather than guessing blindly.",
            "Given a dataset with two or more candidate target columns matching requirement keywords;\n"
            "When the AnalysisView loads;\n"
            "Then the UI must raise a confirmation alert displaying selectable target pills, requiring user confirmation before background training commences."
        ),
        (
            "US-11: Dockerized Zero-Configuration Edge Deployment",
            "As an infrastructure DevOps specialist, I want to deploy the AI Model Forge platform as containerized services so that it runs in air-gapped environments without external Internet access.",
            "Given a host machine with Docker and Docker Compose installed;\n"
            "When the operator executes docker-compose up --build;\n"
            "Then the backend API must start on port 8000 and the React Nginx frontend on port 3000, fully operational with local storage persistence."
        ),
        (
            "US-12: Client SDK Microservice Integration",
            "As a web backend engineer writing a Django or Flask payment service, I want to import aiforge_runtime directly as a standard Python module.",
            "Given a client application with a local .aiforge package;\n"
            "When executing from aiforge_runtime import load_model;\n"
            "Then the model object must be callable repeatedly in high-concurrency request threads with sub-15ms response latency."
        )
    ]

    for title, desc, criteria in user_stories:
        story.append(Paragraph(f"<b>{title}</b>", styles['SubSectionHeader']))
        story.append(Paragraph(f"<i>User Story:</i> {desc}", styles['Paragraph']))
        story.append(Paragraph("<b>Acceptance Criteria (Gherkin BDD):</b>", styles['TableCellBold']))
        story.append(Paragraph(criteria.replace('\n', '<br/>'), styles['CodeBlock']))
        story.append(Spacer(1, 4))

    # 2.3 Prompts, AI Outputs and Refinement
    story.append(Spacer(1, 8))
    story.append(Paragraph("2.3 Prompts, AI Outputs and Refinement", styles['SectionHeader']))

    story.append(Paragraph(
        "To establish these requirements with high precision, interactive prompt engineering sessions were conducted with AI "
        "software engineering assistants. The prompt interactions forced the AI to explore edge cases, challenge naive assumptions, "
        "and establish deterministic system safety guardrails.",
        styles['Paragraph']
    ))

    story.append(create_prompt_box(
        "Elicitation of System Safety Boundaries and Modality Constraints",
        "Prompt: 'We are architecting an intelligent Multimodal AutoML Platform. The goal is to allow users to upload arbitrary "
        "raw data and describe their requirements in plain English. However, we must ensure the system NEVER makes false capability claims "
        "or pretends to train models on unsupported tasks (e.g. object detection, segmentation, speech recognition). How should we structure "
        "our task detector and confidence system to ensure strict transparency and zero hallucinations?'",
        "The AI assistant recommended a three-tier decision engine: (1) ModalityDetector determines physical data format with confidence; "
        "(2) RequirementAnalyzer extracts intent and explicitly identifies unsupported keywords (e.g. 'bounding box', 'yolo', 'transcribe'); "
        "(3) TaskDetector evaluates compatibility. If an unsupported task is detected, is_supported=False is explicitly emitted with a human-readable "
        "explanation. The UI halts automated training and displays an architectural roadmap message explaining that the plugin is planned for a future release.",
        styles
    ))
    story.append(Spacer(1, 6))

    story.append(create_prompt_box(
        "Resolving the Multi-File Deployment Nightmare via Single-File Packaging",
        "Prompt: 'In traditional ML, models require separate preprocessor.pkl, model.pt, and config.json files, which causes fatal deployment "
        "bugs when external developers forget to preprocess incoming data. How can we package the entire pipeline into exactly ONE downloadable "
        "file that self-contains all transformations while remaining secure and verifiable?'",
        "The AI assistant formulated the .aiforge container specification: a versioned ZIP archive containing manifest.json (with SHA-256 integrity "
        "hashes), metadata.json (model card and metrics), schema.json (input validation rules), runtime_config.json, model/ (weights), and "
        "preprocessing/ (fitted ColumnTransformers). A lightweight companion SDK (aiforge_runtime) was designed with a load_model() function that "
        "unpacks the archive into a secure sandbox and wraps it in an AIForgeModel instance whose predict() method handles all raw transforms automatically.",
        styles
    ))
    story.append(Spacer(1, 6))

    story.append(create_prompt_box(
        "Formulating Non-Leakage Chronological Splitting for Time-Series AutoML",
        "Prompt: 'Standard AutoML frameworks randomly shuffle time-series data using K-Fold cross validation, causing severe lookahead leakage. "
        "How should our TimeSeriesTrainer guarantee that no future data leaks into the past, while automatically engineering lag features and rolling statistics?'",
        "The AI formulated strict chronological invariants: (1) Parse and validate the datetime column; (2) Strictly sort DataFrame ascending by time; "
        "(3) Synthesize lag features (t-1, t-2, t-3) and rolling 3-period means; (4) Drop initial NaN rows created by window shifting; (5) Split chronologically "
        "at split_idx = int(N * (1 - test_size)). Zero future information can cross into training folds.",
        styles
    ))
    story.append(Spacer(1, 6))

    story.append(create_prompt_box(
        "Memory-Aware Profiling Protocols for Massive Tabular Ingestion",
        "Prompt: 'Users may upload CSVs ranging from 50 MB to 500 MB. Blindly reading massive datasets entirely into RAM during initial profiling causes "
        "out-of-memory crashes on resource-constrained servers. What memory-aware profiling and sampling protocol should we enforce?'",
        "The AI assistant designed a tiered sampling policy: If file_size > 50 MB, DatasetProfiler reads exactly nrows=50,000 using Pandas chunking, "
        "computes descriptive statistics, infers column types, and checks distinct cardinalities on the representative sample. During training, "
        "HistGradientBoosting uses binned histograms to maintain sub-1GB RAM usage.",
        styles
    ))

    story.append(PageBreak())
    return story
