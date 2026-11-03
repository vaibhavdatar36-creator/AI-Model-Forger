from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from .styles_and_canvas import create_callout_box, create_prompt_box

def build_block_diagram(styles):
    """
    Constructs a professional, high-impact graphical block diagram for Figure 3.1
    using structured, multi-tier ReportLab tables with corporate coloring,
    badge styling, and visual connector flow indicators.
    """
    flowables = []

    # Local styles for diagram typography
    t_hdr = ParagraphStyle('DHdr', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white, alignment=1)
    t_box_hdr = ParagraphStyle('DBoxHdr', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white, alignment=1)
    t_body = ParagraphStyle('DBody', fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#1e293b'))
    t_body_center = ParagraphStyle('DBodyC', fontName='Helvetica', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#1e293b'), alignment=1)
    t_body_bold = ParagraphStyle('DBodyB', fontName='Helvetica-Bold', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#0f172a'))
    t_conn = ParagraphStyle('DConn', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=colors.HexColor('#1d4ed8'), alignment=1)

    # -------------------------------------------------------------------------
    # TIER 1: Presentation & Workflow Studio
    # -------------------------------------------------------------------------
    t1_head = Table([[Paragraph("TIER 1: PRESENTATION & WORKFLOW STUDIO (REACT 18 + VITE + TAILWIND CSS)", t_hdr)]], colWidths=[487])
    t1_head.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1e3a8a')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    flowables.append(t1_head)

    t1_cells = [
        [
            Paragraph("<b>1. Upload Dropzone</b><br/>Drag & drop tabular CSV/XLSX or vision ZIP", t_body_center),
            Paragraph("<b>2. Intent Input</b><br/>Plain-English requirement phrasing & sample chips", t_body_center),
            Paragraph("<b>3. Strategy View</b><br/>Modality badge, detected task & override toggles", t_body_center),
            Paragraph("<b>4. Live Telemetry</b><br/>5-stage animated progress & worker console logs", t_body_center),
            Paragraph("<b>5. In-Browser Test</b><br/>Live sandbox with real-time prediction meters", t_body_center)
        ]
    ]
    t1_body = Table(t1_cells, colWidths=[97.4]*5)
    t1_body.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    flowables.append(t1_body)

    # Connector 1
    t_arr1 = Table([[Paragraph("▼  HTTP/1.1 REST API Calls • Multipart Streaming Ingestion • Server-Sent Telemetry (Port 8000)  ▼", t_conn)]], colWidths=[487])
    t_arr1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    flowables.append(t_arr1)

    # -------------------------------------------------------------------------
    # TIER 2: API Gateway & Service Orchestration
    # -------------------------------------------------------------------------
    t2_head = Table([[Paragraph("TIER 2: API GATEWAY & ASYNCHRONOUS ORCHESTRATION (FASTAPI + UVICORN ASGI)", t_hdr)]], colWidths=[487])
    t2_head.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0369a1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    flowables.append(t2_head)

    t2_cells = [
        [
            Paragraph("<b>Ingestion & Intent Routes</b><br/><code>POST /api/upload</code><br/><code>POST /api/analyze</code><br/><code>POST /api/train</code>", t_body_center),
            Paragraph("<b>Telemetry & Inference Routes</b><br/><code>GET /api/jobs/{id}</code><br/><code>GET /api/models/{id}/download</code><br/><code>POST /api/predict</code>", t_body_center),
            Paragraph("<b>Service Execution Architecture</b><br/>• Asynchronous Worker Threads (BackgroundTasks)<br/>• Pydantic v2 Contract Schema Validation<br/>• Zero-Lock Async Event Loop", t_body_center)
        ]
    ]
    t2_body = Table(t2_cells, colWidths=[162.3]*3)
    t2_body.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f9ff')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#7dd3fc')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bae6fd')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    flowables.append(t2_body)

    # Connector 2
    t_arr2 = Table([[Paragraph("▼  Dispatches Validated Payloads to Dual Intelligence and Persistence Engines  ▼", t_conn)]], colWidths=[487])
    t_arr2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    flowables.append(t_arr2)

    # -------------------------------------------------------------------------
    # TIER 3: Intelligence & State Management Grid (2 Columns)
    # -------------------------------------------------------------------------
    t3_head = Table([
        [Paragraph("INTELLIGENCE & HEURISTIC ANALYSIS ENGINE", t_hdr),
         Paragraph("STATE MANAGEMENT & PERSISTENCE ENGINE", t_hdr)]
    ], colWidths=[243.5, 243.5])
    t3_head.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#0f766e')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#4338ca')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    flowables.append(t3_head)

    t3_cells = [
        [
            Paragraph("• <b>ModalityDetector:</b> MIME inspection, ZIP traversal security, image/text/time heuristic tree<br/>"
                      "• <b>RequirementAnalyzer:</b> NLP keyword intent extraction, target column candidate scoring<br/>"
                      "• <b>TaskDetector:</b> Boundary verification; enforces supported tasks & rejects out-of-scope domains<br/>"
                      "• <b>DatasetProfiler:</b> Memory-aware chunked sampling (50k rows max), missingness profiling<br/>"
                      "• <b>LeakageDetector:</b> Pearson correlation screening (|r| &gt;= 0.98), duplicate column hashes", t_body),
            Paragraph("• <b>JobManager:</b> Thread-safe background worker pool & state machine lifecycle coordinator<br/>"
                      "• <b>SQLite Database:</b> Write-Ahead Logging (WAL) mode with StaticPool connection sharing<br/>"
                      "• <b>SQLAlchemy ORM:</b> Entity models: Projects, Datasets, TrainingJobs, ModelArtifacts<br/>"
                      "• <b>Storage Registry:</b> Staging volume for raw uploads, profiles, and packaged artifacts<br/>"
                      "• <b>Lifecycle Stages:</b> ANALYZING ➜ PREPROCESSING ➜ TRAINING ➜ PACKAGING", t_body)
        ]
    ]
    t3_body = Table(t3_cells, colWidths=[243.5, 243.5])
    t3_body.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#f0fdfa')),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor('#eef2ff')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    flowables.append(t3_body)

    # Connector 3
    t_arr3 = Table([[Paragraph("▼  Dispatches Clean Feature Matrix & Target Vectors to Modality Training Plugins  ▼", t_conn)]], colWidths=[487])
    t_arr3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    flowables.append(t_arr3)

    # -------------------------------------------------------------------------
    # TIER 4: Polymorphic AutoML Training Engine (Plugin Registry)
    # -------------------------------------------------------------------------
    t4_head = Table([[Paragraph("TIER 4: POLYMORPHIC AUTOML TRAINING ENGINE (TRAINER REGISTRY & BASE TRAINER)", t_hdr)]], colWidths=[487])
    t4_head.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#6d28d9')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    flowables.append(t4_head)

    t4_cells = [
        [
            Paragraph("<b>Tabular Engine</b><br/>"
                      "• ColumnTransformer<br/>"
                      "• Median/Mode Imputer<br/>"
                      "• OneHotEncoder(ignore)<br/>"
                      "• Random Forest Classifier<br/>"
                      "• HistGradientBoosting<br/>"
                      "• LogisticRegression / Ridge", t_body),
            Paragraph("<b>Computer Vision</b><br/>"
                      "• Corrupted JPEG filter<br/>"
                      "• RGB Tensor Normalization<br/>"
                      "• MobileNetV2 Backbone<br/>"
                      "• Transfer Learning Head<br/>"
                      "• Fallback 3-Layer CNN<br/>"
                      "• Cross-Entropy Loss", t_body),
            Paragraph("<b>NLP Text Engine</b><br/>"
                      "• Unicode NFKC Normalizer<br/>"
                      "• Sublinear TF-IDF (1,2)<br/>"
                      "• Vocabulary Capping<br/>"
                      "• Logistic Regression<br/>"
                      "• LinearSVC Classifier<br/>"
                      "• Multinomial Naive Bayes", t_body),
            Paragraph("<b>Time-Series Engine</b><br/>"
                      "• Chronological Ordering<br/>"
                      "• Zero-Lookahead Split<br/>"
                      "• Lag Features (t-1,2,3)<br/>"
                      "• 7-Step Rolling Statistics<br/>"
                      "• Cyclical Sine/Cosine<br/>"
                      "• Gradient Boosted Forecast", t_body)
        ]
    ]
    t4_body = Table(t4_cells, colWidths=[121.75]*4)
    t4_body.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#faf5ff')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#d8b4fe')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e9d5ff')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    flowables.append(t4_body)

    # Connector 4
    t_arr4 = Table([[Paragraph("▼  Champion Selection • Metric Scorecard Validation • Pre-Packaging Pipeline Assembly  ▼", t_conn)]], colWidths=[487])
    t_arr4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    flowables.append(t_arr4)

    # -------------------------------------------------------------------------
    # TIER 5: Single-File Packaging & Sandbox Verification
    # -------------------------------------------------------------------------
    t5_head = Table([[Paragraph("TIER 5: ARTIFACT PACKAGING & SECURITY VERIFICATION ENGINE", t_hdr)]], colWidths=[487])
    t5_head.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#b45309')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    flowables.append(t5_head)

    t5_cells = [
        [
            Paragraph("<b>Single-Pass Deterministic Container Packaging</b><br/>"
                      "• Serializes Fitted Preprocessors (<code>preprocessing/preprocessor.joblib</code>)<br/>"
                      "• Serializes Trained Weights (<code>model/model.joblib</code> or <code>model/model.pt</code>)<br/>"
                      "• Generates <code>manifest.json</code> with Cryptographic SHA-256 Hashes of all internal files<br/>"
                      "• Emits <code>metadata.json</code> (Model Card), <code>schema.json</code>, and <code>runtime_config.json</code><br/>"
                      "• Compiles Self-Contained <code>.aiforge</code> Single-File ZIP Archive", t_body),
            Paragraph("<b>Pre-Download Sandbox Verification Engine</b><br/>"
                      "• Unpacks generated package into isolated temporary RAM directory<br/>"
                      "• Recalculates and verifies SHA-256 hash against manifest signature<br/>"
                      "• Loads model via <code>aiforge_runtime</code> without server imports<br/>"
                      "• Executes holdout test prediction verifying shape and confidence range<br/>"
                      "• Protects against Zip Slip path traversal and corrupt byte archives", t_body)
        ]
    ]
    t5_body = Table(t5_cells, colWidths=[243.5, 243.5])
    t5_body.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fffbeb')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#fde68a')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#fef3c7')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    flowables.append(t5_body)

    # Connector 5
    t_arr5 = Table([[Paragraph("▼  Single-File (.aiforge) Portable Artifact Release  ▼", t_conn)]], colWidths=[487])
    t_arr5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    flowables.append(t_arr5)

    # -------------------------------------------------------------------------
    # TIER 6: Standalone Production Deployment SDK
    # -------------------------------------------------------------------------
    t6_head = Table([[Paragraph("TIER 6: STANDALONE RUNTIME SDK (INDEPENDENT CLIENT ENVIRONMENT)", t_hdr)]], colWidths=[487])
    t6_head.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#047857')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    flowables.append(t6_head)

    t6_cells = [
        [
            Paragraph("<b>Decoupled Client Architecture</b><br/>"
                      "• Zero dependency on training backend or web server<br/>"
                      "• Requires only standard wheels (NumPy, Scikit-Learn, PyTorch)<br/>"
                      "• Encapsulates complete preprocessing inside artifact", t_body),
            Paragraph("<b>3-Line Production Execution API</b><br/>"
                      "<code>from aiforge_runtime import load_model</code><br/>"
                      "<code>model = load_model('customer_churn.aiforge')</code><br/>"
                      "<code>result = model.predict(raw_input_data)</code>", t_body),
            Paragraph("<b>Operational Invariance</b><br/>"
                      "• 0% Training-Serving Feature Drift<br/>"
                      "• Automatic Missing Value Imputation<br/>"
                      "• Sub-10ms Inference Latency", t_body)
        ]
    ]
    t6_body = Table(t6_cells, colWidths=[162.3]*3)
    t6_body.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ecfdf5')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#a7f3d0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1fae5')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    flowables.append(t6_body)

    return flowables

def generate_ch3(styles):
    story = []

    # Chapter Header
    story.append(Paragraph("3. SYSTEM DESIGN", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=12))

    # 3.1 System Architecture and Module Design
    story.append(Paragraph("3.1 System Architecture and Module Design", styles['SectionHeader']))

    story.append(Paragraph(
        "AI Model Forge is engineered using a decoupled, layered micro-service architecture that enforces strict separation "
        "between ingestion, heuristic analysis, data engineering, model training, packaging, and client-side inference runtime. "
        "The system is organized into six core functional tiers:",
        styles['Paragraph']
    ))

    arch_tiers = [
        ("Presentation & Telemetry Tier", "Modern responsive Single Page Application built with React 18, Vite, and Lucide React. Features drag-and-drop file upload, real-time training progress polling, interactive prediction playground, model card visualizations, and technical engine console log streaming."),
        ("API Gateway & Orchestration Tier", "Asynchronous FastAPI web service providing REST endpoints for dataset ingestion (/api/upload), intelligent requirement analysis (/api/analyze), background AutoML orchestration (/api/train), job telemetry (/api/jobs/{id}), model asset management (/api/models), and server-side prediction (/api/predict)."),
        ("Intelligence & Analysis Tier", "Specialized heuristic and analytical services comprising ModalityDetector (file, MIME, and structural inspection), RequirementAnalyzer (NLP objective and target extraction), TaskDetector (modality-task reconciliation), DatasetProfiler (memory-aware profiling and sampling), and LeakageDetector (correlation and target-derivative screening)."),
        ("AutoML Training Engine Tier", "Decoupled plugin architecture governed by TrainerRegistry and BaseTrainer. Concrete trainers include TabularTrainer (classification/regression via Random Forest, HistGradientBoosting, LogisticRegression/Ridge), ImageTrainer (PyTorch transfer learning via MobileNetV2/ResNet18), TextTrainer (TF-IDF vectorizer + LinearSVC/LogisticRegression), and TimeSeriesTrainer (chronological lag-feature gradient boosting)."),
        ("Packaging & Security Engine Tier", "Containerized single-file packaging engine (ModelPackager) creating self-contained .aiforge archives, validated pre-download by ModelValidator in an isolated execution sandbox."),
        ("Production Runtime SDK Tier", "Decoupled client-side runtime SDK (aiforge_runtime) providing a 3-line Python API executing end-to-end inference on raw data with zero training-serving skew.")
    ]

    for tier_name, tier_desc in arch_tiers:
        story.append(Paragraph(f"• <b>{tier_name}:</b> {tier_desc}", styles['Paragraph']))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Figure 3.1: Complete End-to-End System Block Diagram & Data Flow</b>", styles['ParagraphBold']))
    story.append(Spacer(1, 4))

    # Add the professional graphical block diagram
    diagram_elements = build_block_diagram(styles)
    for element in diagram_elements:
        story.append(element)

    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Component Micro-Architectures & Detailed Subsystem Design:</b>", styles['ParagraphBold']))

    story.append(Paragraph(
        "<b>1. ModalityDetector Subsystem:</b> The modality detector inspects inputs through an intelligent decision tree: "
        "(a) If the target is an archive (.zip), it checks for inner directory hierarchies and image/text counts without uncompressing unverified paths; "
        "(b) If tabular (.csv, .xlsx, .parquet, .json), it scans for columns referencing image paths (e.g. <code>image_path,label</code>), classifying "
        "them as IMAGE_WITH_METADATA; (c) It searches for prominent text columns with average string length &gt; 40 characters in few-column tables, classifying "
        "them as TEXT_NLP; (d) It checks for explicit datetime index columns and verifies that sample values parse as valid timestamps to detect TIME_SERIES; "
        "(e) Otherwise, it classifies the data as TABULAR.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "<b>2. RequirementAnalyzer & TaskDetector Subsystem:</b> Formulates a semantic parser that identifies keywords matching classification "
        "('predict whether', 'churn', 'sentiment', 'classify') vs regression ('price', 'demand', 'continuous', 'cost') vs forecasting ('tomorrow', 'future'). "
        "Crucially, it checks for unsupported task patterns ('bounding box', 'yolo', 'detect objects', 'segmentation', 'speech to text'). When found, "
        "TaskDetector sets <code>is_supported=False</code> and injects clear user-facing rationale, preventing erroneous model fitting.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "<b>3. TabularDataEngineer & LeakageDetector Subsystem:</b> Automatically constructs Scikit-Learn <code>ColumnTransformer</code> instances. "
        "It partitions features into Numerical (imputed with median, standardized with StandardScaler) and Categorical (imputed with most-frequent, "
        "encoded with OneHotEncoder with <code>handle_unknown='ignore'</code>). It identifies ID columns (e.g. names matching <code>*_id</code>, <code>uuid</code>, "
        "or non-numeric strings with 100% unique values) and completely excludes them. It tests Pearson correlation between each numerical feature "
        "and target, flagging any feature with |r| &gt;= 0.98 as direct target leakage.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "<b>4. Single-File Container Format (.aiforge):</b> Rather than leaving models as loose files, the <code>ModelPackager</code> compiles a versioned ZIP "
        "archive containing: (1) <code>manifest.json</code> containing the SHA-256 cryptographic checksum of all inner components and package inventory; "
        "(2) <code>metadata.json</code> containing model cards, hyperparameters, and evaluation metrics; (3) <code>schema.json</code> detailing input "
        "feature names, data types, and categorical options; (4) <code>runtime_config.json</code> detailing Python and framework requirements; "
        "(5) <code>model/model.joblib</code> or <code>model/model.pt</code>; and (6) <code>preprocessing/preprocessor.joblib</code>. The resulting single file "
        "guarantees that preprocessing and model weights can never be desynchronized.",
        styles['Paragraph']
    ))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Table 3.1: RESTful API Endpoint Specifications</b>", styles['ParagraphBold']))

    api_data = [
        [Paragraph("<b>Endpoint Route</b>", styles['TableHead']), Paragraph("<b>HTTP Method</b>", styles['TableHead']), Paragraph("<b>Request Payload</b>", styles['TableHead']), Paragraph("<b>Response Output</b>", styles['TableHead']), Paragraph("<b>Description</b>", styles['TableHead'])],
        [
            Paragraph("<code>/api/upload</code>", styles['TableCellBold']),
            Paragraph("POST", styles['TableCell']),
            Paragraph("Multipart form file (up to 500 MB)", styles['TableCell']),
            Paragraph("<code>{dataset_id, modality, confidence}</code>", styles['TableCell']),
            Paragraph("Uploads raw dataset, validates file safety, detects modality.", styles['TableCell'])
        ],
        [
            Paragraph("<code>/api/analyze</code>", styles['TableCellBold']),
            Paragraph("POST", styles['TableCell']),
            Paragraph("<code>{dataset_id, requirement, overrides}</code>", styles['TableCell']),
            Paragraph("<code>{task, is_supported, target, recommendations}</code>", styles['TableCell']),
            Paragraph("Parses requirement, profiles data, recommends candidate architectures.", styles['TableCell'])
        ],
        [
            Paragraph("<code>/api/train</code>", styles['TableCellBold']),
            Paragraph("POST", styles['TableCell']),
            Paragraph("<code>{dataset_id, requirement, project_name}</code>", styles['TableCell']),
            Paragraph("<code>{job_id, status: 'ANALYZING', progress}</code>", styles['TableCell']),
            Paragraph("Spawns background AutoML thread, returns immediate tracking ID.", styles['TableCell'])
        ],
        [
            Paragraph("<code>/api/jobs/{id}</code>", styles['TableCellBold']),
            Paragraph("GET", styles['TableCell']),
            Paragraph("None (Path parameter: job_id)", styles['TableCell']),
            Paragraph("<code>{status, progress, current_step, model_id}</code>", styles['TableCell']),
            Paragraph("Returns real-time training progress and step updates.", styles['TableCell'])
        ],
        [
            Paragraph("<code>/api/results/{id}</code>", styles['TableCellBold']),
            Paragraph("GET", styles['TableCell']),
            Paragraph("None (Path parameter: job_id)", styles['TableCell']),
            Paragraph("<code>{best_model, metrics, comparisons, logs}</code>", styles['TableCell']),
            Paragraph("Returns evaluation report, model comparisons, and Model Card.", styles['TableCell'])
        ],
        [
            Paragraph("<code>/api/models/{id}/download</code>", styles['TableCellBold']),
            Paragraph("GET", styles['TableCell']),
            Paragraph("None (Path parameter: model_id)", styles['TableCell']),
            Paragraph("Binary attachment: <code>model_name.aiforge</code>", styles['TableCell']),
            Paragraph("Transmits the single, complete, verified .aiforge package.", styles['TableCell'])
        ],
        [
            Paragraph("<code>/api/models/{id}/predict</code>", styles['TableCellBold']),
            Paragraph("POST", styles['TableCell']),
            Paragraph("<code>{input_data: {...}}</code>", styles['TableCell']),
            Paragraph("<code>{prediction, confidence, probabilities, latency_ms}</code>", styles['TableCell']),
            Paragraph("Executes real-time inference on raw data via loaded .aiforge package.", styles['TableCell'])
        ],
        [
            Paragraph("<code>/api/health</code>", styles['TableCellBold']),
            Paragraph("GET", styles['TableCell']),
            Paragraph("None", styles['TableCell']),
            Paragraph("<code>{status, hardware: {cpu, gpu, ram}}</code>", styles['TableCell']),
            Paragraph("Returns server health, detected hardware, and GPU availability.", styles['TableCell'])
        ]
    ]

    api_table = Table(api_data, colWidths=[95, 45, 115, 120, 112])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(api_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Table 3.2: CASH Algorithmic Hyperparameter Search Space Specification</b>", styles['ParagraphBold']))

    cash_data = [
        [Paragraph("<b>Modality / Engine</b>", styles['TableHead']), Paragraph("<b>Candidate Algorithm</b>", styles['TableHead']), Paragraph("<b>Hyperparameter Subspace</b>", styles['TableHead']), Paragraph("<b>Optimization &amp; Default Strategy</b>", styles['TableHead'])],
        [
            Paragraph("<b>Tabular Classification</b>", styles['TableCellBold']),
            Paragraph("Random Forest Classifier", styles['TableCell']),
            Paragraph("n_estimators ∈ [50, 300]<br/>max_depth ∈ [5, 25, None]<br/>min_samples_split ∈ [2, 5, 10]", styles['TableCell']),
            Paragraph("Resource-aware grid search with Gini impurity criterion and out-of-bag validation.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Tabular Gradient Boosting</b>", styles['TableCellBold']),
            Paragraph("HistGradientBoosting", styles['TableCell']),
            Paragraph("learning_rate ∈ [0.01, 0.1, 0.2]<br/>max_iter ∈ [100, 250]<br/>l2_regularization ∈ [0.0, 1.0]", styles['TableCell']),
            Paragraph("Histogram-based binning with early stopping on 15% validation split.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Tabular Linear Baseline</b>", styles['TableCellBold']),
            Paragraph("LogisticRegression / Ridge", styles['TableCell']),
            Paragraph("C ∈ [0.01, 0.1, 1.0, 10.0]<br/>penalty ∈ ['l2']<br/>solver = 'lbfgs'", styles['TableCell']),
            Paragraph("Fast convex baseline with L2 shrinkage for low-dimensional datasets.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Computer Vision (CV)</b>", styles['TableCellBold']),
            Paragraph("PyTorch MobileNetV2", styles['TableCell']),
            Paragraph("learning_rate ∈ [1e-4, 1e-3]<br/>batch_size ∈ [16, 32, 64]<br/>head_dropout ∈ [0.2, 0.4]", styles['TableCell']),
            Paragraph("Frozen inverted residual backbone + AdamW fine-tuning with cosine annealing.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Natural Language (NLP)</b>", styles['TableCellBold']),
            Paragraph("TF-IDF + LinearSVC", styles['TableCell']),
            Paragraph("ngram_range ∈ [(1,1), (1,2)]<br/>max_features ∈ [2500, 10000]<br/>C ∈ [0.1, 1.0, 5.0]", styles['TableCell']),
            Paragraph("Sublinear term frequency scaling with L2 normalized feature space.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Time-Series Forecast</b>", styles['TableCellBold']),
            Paragraph("HistGradientBoosting Lag Regressor", styles['TableCell']),
            Paragraph("lags ∈ [1, 2, 3, 7, 14]<br/>rolling_window ∈ [3, 7]<br/>cyclical_fourier = True", styles['TableCell']),
            Paragraph("Strict forward-chaining rolling window without random sample shuffling.", styles['TableCell'])
        ]
    ]

    t_cash = Table(cash_data, colWidths=[105, 115, 135, 132])
    t_cash.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_cash)
    story.append(Spacer(1, 10))

    # Figure 3.2: Graphical Relational Database Schema
    story.append(Paragraph("<b>Figure 3.2: Relational Database Entity-Relationship (ER) Schema</b>", styles['ParagraphBold']))
    story.append(Spacer(1, 4))

    # Structured 4-Table ER Schema Grid
    er_head_style = ParagraphStyle('ERHdr', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white, alignment=1)
    er_body_style = ParagraphStyle('ERBody', fontName='Courier', fontSize=6.5, leading=8.5, textColor=colors.HexColor('#0f172a'))
    er_rel_style = ParagraphStyle('ERRel', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=colors.HexColor('#1e40af'), alignment=1)

    er_top = [
        [
            Table([
                [Paragraph("PROJECTS", er_head_style)],
                [Paragraph("<b>PK id:</b> String(36) [UUID]<br/>"
                           "<b>&nbsp;&nbsp;name:</b> String(255)<br/>"
                           "<b>&nbsp;&nbsp;requirement:</b> Text<br/>"
                           "<b>&nbsp;&nbsp;created_at:</b> DateTime", er_body_style)]
            ], colWidths=[238]),
            Table([
                [Paragraph("DATASETS", er_head_style)],
                [Paragraph("<b>PK id:</b> String(36) [UUID]<br/>"
                           "<b>FK project_id:</b> String(36)<br/>"
                           "<b>&nbsp;&nbsp;filename:</b> String(255)<br/>"
                           "<b>&nbsp;&nbsp;filepath:</b> String(512)<br/>"
                           "<b>&nbsp;&nbsp;file_size:</b> Integer<br/>"
                           "<b>&nbsp;&nbsp;modality:</b> String(64)<br/>"
                           "<b>&nbsp;&nbsp;profile_json:</b> JSON", er_body_style)]
            ], colWidths=[238])
        ]
    ]
    t_er_top = Table(er_top, colWidths=[243.5, 243.5])
    t_er_top.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    # Style sub-tables
    er_top[0][0].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    er_top[0][1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0284c7')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_er_top)

    t_er_rel1 = Table([[Paragraph("▲ 1:N (Projects to Datasets) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1:N (Projects to Jobs) ▼", er_rel_style)]], colWidths=[487])
    t_er_rel1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(t_er_rel1)

    er_bottom = [
        [
            Table([
                [Paragraph("TRAINING_JOBS", er_head_style)],
                [Paragraph("<b>PK id:</b> String(36) [UUID]<br/>"
                           "<b>FK project_id:</b> String(36)<br/>"
                           "<b>FK dataset_id:</b> String(36)<br/>"
                           "<b>&nbsp;&nbsp;status:</b> String(32)<br/>"
                           "<b>&nbsp;&nbsp;progress:</b> Integer (0-100)<br/>"
                           "<b>&nbsp;&nbsp;current_step:</b> String(255)<br/>"
                           "<b>&nbsp;&nbsp;logs:</b> Text<br/>"
                           "<b>&nbsp;&nbsp;error_message:</b> Text<br/>"
                           "<b>&nbsp;&nbsp;created_at:</b> DateTime", er_body_style)]
            ], colWidths=[238]),
            Table([
                [Paragraph("MODEL_ARTIFACTS", er_head_style)],
                [Paragraph("<b>PK id:</b> String(36) [UUID]<br/>"
                           "<b>FK job_id:</b> String(36)<br/>"
                           "<b>&nbsp;&nbsp;name:</b> String(255)<br/>"
                           "<b>&nbsp;&nbsp;task:</b> String(64)<br/>"
                           "<b>&nbsp;&nbsp;modality:</b> String(64)<br/>"
                           "<b>&nbsp;&nbsp;model_type:</b> String(128)<br/>"
                           "<b>&nbsp;&nbsp;best_metric_name:</b> String(64)<br/>"
                           "<b>&nbsp;&nbsp;best_metric_value:</b> Float<br/>"
                           "<b>&nbsp;&nbsp;metrics_json:</b> JSON<br/>"
                           "<b>&nbsp;&nbsp;file_path:</b> String(512)<br/>"
                           "<b>&nbsp;&nbsp;schema_json:</b> JSON", er_body_style)]
            ], colWidths=[238])
        ]
    ]
    t_er_bottom = Table(er_bottom, colWidths=[243.5, 243.5])
    t_er_bottom.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    er_bottom[0][0].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#7c3aed')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    er_bottom[0][1].setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_er_bottom)
    story.append(Spacer(1, 12))

    # 3.2 User Interface Design / Wireframes
    story.append(Paragraph("3.2 User Interface Design / Wireframes", styles['SectionHeader']))

    story.append(Paragraph(
        "The web user interface is crafted using React 18, Vite, and Lucide React icons, styled with a high-contrast dark theme "
        "accented with indigo and violet gradients. The interface is engineered as an intuitive six-stage progressive disclosure state machine:",
        styles['Paragraph']
    ))

    story.append(Paragraph("<b>Figure 3.3: User Interface Wireframe Mockup (Create Model Screen)</b>", styles['ParagraphBold']))
    story.append(Spacer(1, 4))

    # Visual UI Card Mockup for Create Model
    ui_win_head = ParagraphStyle('UIWinHdr', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#94a3b8'))
    ui_nav_item = ParagraphStyle('UINav', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#38bdf8'))
    ui_label = ParagraphStyle('UILbl', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.HexColor('#0f172a'))
    ui_input = ParagraphStyle('UIInp', fontName='Helvetica', fontSize=7, leading=9, textColor=colors.HexColor('#334155'))
    ui_btn = ParagraphStyle('UIBtn', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white, alignment=1)

    btn_build = Table([[Paragraph("ANALYZE &amp; BUILD MODEL ➔", ui_btn)]], colWidths=[200])
    btn_build.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#2563eb')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))

    wireframe_create_table = Table([
        [Table([
            [Paragraph("● ● ● &nbsp; <b>AI Model Forge — Web Studio</b> &nbsp; | &nbsp; http://localhost:8000", ui_win_head),
             Paragraph("Overview &nbsp;&nbsp; <b>[+] Create Model</b> &nbsp;&nbsp; Model Vault &nbsp;&nbsp; Docs", ui_nav_item)]
        ], colWidths=[280, 195])],
        [Paragraph("<b>Build an AI Model:</b> Tell us what you want to achieve and provide your dataset. We handle the rest.", ui_label)],
        [Table([
            [Paragraph("<b>Project Name:</b>", ui_label), Paragraph("Customer Churn Predictor", ui_input)],
            [Paragraph("<b>AI Goal / Prompt:</b>", ui_label), Paragraph("Predict customer churn from demographic and subscription features...", ui_input)],
            [Paragraph("<b>Sample Chips:</b>", ui_label), Paragraph("[ Predict Churn ] &nbsp; [ House Prices ] &nbsp; [ Review Sentiment ] &nbsp; [ Pet Images ]", ui_input)],
            [Paragraph("<b>Upload Dataset:</b>", ui_label), Paragraph("<b>[ ^ ] Drag &amp; drop dataset file here</b><br/><code>customer_churn.csv (18.4 KB • Ready for analysis)</code>", ui_input)],
            [Paragraph("<b>Advanced Options:</b>", ui_label), Paragraph("[ &gt; ] Show Advanced Settings (Target override, algorithm checklist, split ratio)", ui_input)],
            [Paragraph("", ui_label), btn_build]
        ], colWidths=[110, 365])]
    ], colWidths=[487])

    wireframe_create_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f1f5f9')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#64748b')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(wireframe_create_table)
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>Figure 3.4: User Interface Wireframe Mockup (Results & Artifact Download Screen)</b>", styles['ParagraphBold']))
    story.append(Spacer(1, 4))

    btn_download = Table([[Paragraph("DOWNLOAD .AIFORGE", ui_btn)]], colWidths=[150])
    btn_download.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#16a34a')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))

    # Visual UI Card Mockup for Model Results
    wireframe_results_table = Table([
        [Table([
            [Paragraph("● ● ● &nbsp; <b>Model Results — Champion Evaluation</b>", ui_win_head),
             Paragraph("Status: <font color='#16a34a'><b>TRAINING COMPLETE</b></font>", ui_win_head)]
        ], colWidths=[320, 155])],
        [Table([
            [Paragraph("<b>CHAMPION MODEL: Random Forest Classifier</b><br/>Trained, benchmarked, and fully validated in 4.82s", ui_label),
             btn_download]
        ], colWidths=[315, 160])],
        [Table([
            [Paragraph("<b>Primary Metric (Macro-F1)</b><br/><b>0.7912</b>", ui_label),
             Paragraph("<b>Accuracy Score</b><br/><b>82.50%</b>", ui_label),
             Paragraph("<b>Total Duration</b><br/><b>4.82 s</b>", ui_label),
             Paragraph("<b>Security Checksum</b><br/><b>SHA-256 VERIFIED</b>", ui_label)]
        ], colWidths=[118]*4)],
        [Paragraph("<b>Automated Data Engineering Summary:</b> Excluded ID 'customer_id' • 7 NaNs imputed with median/mode • One-Hot Encoded 'contract_type'", ui_input)],
        [Paragraph("<b>Candidate Algorithm Comparison Table:</b><br/>"
                   "1. <b>Random Forest Classifier (Champion):</b> F1=0.7912 | Acc=82.50% | TrainTime=0.38s<br/>"
                   "2. <b>Histogram Gradient Boosting:</b> F1=0.7645 | Acc=80.00% | TrainTime=0.22s<br/>"
                   "3. <b>Logistic Regression:</b> F1=0.7320 | Acc=77.50% | TrainTime=0.05s", ui_input)]
    ], colWidths=[487])

    wireframe_results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f172a')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#eff6ff')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#f0fdf4')),
        ('BACKGROUND', (0, 4), (-1, 4), colors.white),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#64748b')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(wireframe_results_table)
    story.append(Spacer(1, 12))

    # 3.3 Design Prompts, AI Outputs and Final Design
    story.append(Paragraph("3.3 Design Prompts, AI Outputs and Final Design", styles['SectionHeader']))

    story.append(Paragraph(
        "During the architectural design phase, structured prompt engineering was employed to explore alternative "
        "packaging topologies and micro-service interaction paradigms. The following prompt case studies illustrate the design decisions:",
        styles['Paragraph']
    ))

    story.append(create_prompt_box(
        "Architectural Decoupling: Single-File Container vs. Multi-Artifact Bundles",
        "Prompt: 'We need to design the model artifact delivery format for AI Model Forge. Evaluate two approaches: "
        "(1) Multi-artifact export: emitting loose weights (.pkl), schema (.json), and preprocessor (.joblib) into a folder. "
        "(2) Single-file archive (.aiforge): a self-contained ZIP packaging weights, ColumnTransformers, metadata, and SHA-256 manifests. "
        "Which approach guarantees zero training-serving skew and easiest downstream deployment?'",
        "The AI produced a comparative tradeoff matrix concluding that Approach 2 (.aiforge) is vastly superior: "
        "it eliminates missing preprocessor bugs, prevents desynchronized column order, enables tamper verification via SHA-256, "
        "and permits a 3-line client SDK (load_model -> predict). The single-file architecture was adopted as a core design pillar.",
        styles
    ))
    story.append(Spacer(1, 6))

    story.append(create_prompt_box(
        "Task Boundary Guardrails: Transparent Rejection of Unsupported Tasks",
        "Prompt: 'Design the TaskDetector service. When a user uploads image data and enters a prompt like \"Detect cars and people with "
        "bounding boxes\", how should the system behave? Should it try to approximate with classification, or reject it?'",
        "The AI strongly advised explicit, transparent task rejection: 'Silent fallback or partial approximation leads to catastrophic user "
        "distrust. The system must set is_supported=False, state that Object Detection requires specialized anchor-box models (e.g. YOLO/Faster R-CNN) "
        "not yet bundled, and suggest classification or roadmap timelines.' This guardrail logic was incorporated into TaskDetector.",
        styles
    ))

    story.append(PageBreak())
    return story
