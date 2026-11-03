from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib import colors
from .styles_and_canvas import create_callout_box

def generate_ch1(styles):
    story = []

    # Chapter Header
    story.append(Paragraph("1. INTRODUCTION", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=12))

    # 1.1 Project Overview and Problem Statement
    story.append(Paragraph("1.1 Project Overview and Problem Statement", styles['SectionHeader']))

    story.append(Paragraph(
        "Over the last decade, Machine Learning (ML) and Deep Learning (DL) have transitioned from specialized academic disciplines "
        "into the central computational engine driving modern digital software infrastructure. Organizations spanning healthcare, "
        "finance, autonomous logistics, e-commerce, telecommunications, and industrial manufacturing increasingly demand predictive "
        "intelligence integrated directly into production applications. However, despite the widespread availability of high-performance "
        "computational accelerators (GPUs, TPUs) and high-level software libraries (such as Scikit-Learn, PyTorch, and TensorFlow), "
        "the actual engineering journey from a raw dataset to an operational, production-ready model remains notoriously complex, "
        "brittle, and prohibitive.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "Traditionally, creating a machine learning model from raw, real-world data requires a multidisciplinary team composed of "
        "Data Engineers, Machine Learning Researchers, and MLOps Infrastructure Specialists. The canonical lifecycle requires navigating "
        "a sequence of interdependent, error-prone phases: exploratory data analysis, data cleaning, missing value imputation, categorical "
        "encoding, feature normalization, outlier mitigation, target leakage identification, algorithm selection, hyperparameter "
        "optimization, holdout benchmarking, serialization, container packaging, and deployment into client runtime applications. "
        "Each phase introduces immense cognitive load, human error, and opportunities for statistical corruption.",
        styles['Paragraph']
    ))

    story.append(create_callout_box(
        "CORE PROBLEM STATEMENT",
        "The modern AI/ML lifecycle is bottlenecked by three compounding systemic challenges: "
        "(1) Excessive cognitive toil and manual friction required for repetitive exploratory data analysis and feature engineering; "
        "(2) Severe tooling and framework fragmentation across different modalities (Tabular, Vision, NLP, and Time-Series); and "
        "(3) The 'Multi-File Deployment Nightmare,' wherein model weights, preprocessing transformers, schemas, and configurations "
        "are exported as disconnected artifacts, leading to fatal training-serving skew, memory leaks, and silent production degradation.",
        styles
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Theoretical Foundations of Automated Machine Learning (AutoML):</b> Formally, the challenge of automated model "
        "construction is cast as the Combined Algorithm Selection and Hyperparameter Optimization (CASH) problem. Given a dataset "
        "<i>D</i> partitioned into training and validation folds, the objective is to find a pipeline <i>A*</i> belonging to a vast, "
        "heterogeneous algorithm search space <i>A</i>, with hyperparameter configuration <i>&theta;*</i> belonging to space <i>&Theta;</i>, "
        "that minimizes a validation loss function <i>L</i>:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>(A*, &theta;*) = argmin<sub>A &isin; A, &theta; &isin; &Theta;</sub> E<sub>(x,y) &sim; D<sub>val</sub></sub> [ L(A<sub>&theta;</sub>(x), y) ]</b><br/>"
        "In practical enterprise software, this optimization problem is complicated by multimodal data structures. A tabular dataset requires "
        "heterogeneous column transformations; a visual dataset requires spatial convolutions and transfer learning; text datasets demand "
        "tokenization and sparse vectorization; and time-series data requires autoregressive lag window construction under strict temporal constraints.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "<b>The Multi-File Deployment Nightmare:</b> In traditional industrial machine learning workflows, once an engineer completes "
        "model training in an interactive Jupyter notebook, the resulting artifacts are exported as a chaotic collection of loose files: "
        "a pickled scaler (<code>scaler.pkl</code>), an encoder dictionary (<code>encoder.joblib</code>), a neural network weight tensor "
        "(<code>model.pt</code> or <code>weights.bin</code>), configuration JSONs (<code>config.json</code>), and arbitrary helper functions "
        "(<code>preprocess_utils.py</code>). When an external application team attempts to consume this model, they must painstakingly "
        "recreate the exact preprocessing sequence, align feature orders, and match library versions. Any minor discrepancy—such as "
        "a transposed column, an unseen category string, an unexpected NaN, or a different torchvision resize interpolation algorithm—triggers "
        "runtime exceptions or, worse, <i>silent statistical failure</i> where predictions degrade without error alerts.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "<b>The Modality Silo Problem:</b> Existing AutoML tools are rigidly specialized. Tabular tools (Auto-Sklearn, TPOT) cannot process "
        "image folders; computer vision AutoML platforms cannot ingest CSV sales tables; and time-series tools cannot handle natural language text. "
        "Software teams are forced to integrate and maintain four or five disparate AutoML frameworks, creating massive infrastructure bloat, "
        "divergent deployment formats, and prohibitive maintenance costs.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "<b>The Problem of False Capability Claims:</b> A major hazard in modern low-code or AI-augmented tools is the temptation to make "
        "unrealistic capability claims—promising to 'solve any arbitrary problem from any dataset.' In reality, when an untrained or unsupported "
        "task is requested (e.g., bounding-box object detection, speech-to-text, or video action recognition), naive systems either hallucinate "
        "metrics or fit an inappropriate proxy model (such as flattening image pixels into linear regression). A robust engineering platform must "
        "enforce transparent architectural boundaries: solving supported tasks autonomously with industrial rigor, while honestly informing users "
        "when specialized domains require future plugin modules.",
        styles['Paragraph']
    ))

    story.append(Spacer(1, 10))

    # 1.2 Existing Project and Limitations
    story.append(Paragraph("1.2 Existing Project and Limitations", styles['SectionHeader']))

    story.append(Paragraph(
        "To establish clear engineering benchmarks, we conducted an exhaustive investigation into prevailing open-source and commercial "
        "AutoML frameworks. Table 1.1 summarizes this comparative analysis across modalities, preprocessing automation, packaging, and runtime simplicity.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "<b>Table 1.1: Detailed Comparative Analysis of Existing AutoML Systems vs. AI Model Forge</b>",
        styles['ParagraphBold']
    ))

    comp_table_data = [
        [
            Paragraph("<b>Platform</b>", styles['TableHead']),
            Paragraph("<b>Modality Scope</b>", styles['TableHead']),
            Paragraph("<b>Data Engineering</b>", styles['TableHead']),
            Paragraph("<b>Package Artifact (.aiforge)</b>", styles['TableHead']),
            Paragraph("<b>Client SDK Experience</b>", styles['TableHead']),
            Paragraph("<b>Operational Limitations</b>", styles['TableHead'])
        ],
        [
            Paragraph("<b>Auto-Sklearn</b>", styles['TableCellBold']),
            Paragraph("Tabular Only", styles['TableCell']),
            Paragraph("Bayesian search over Scikit-Learn transformers", styles['TableCell']),
            Paragraph("No (Emits raw ensemble dict / pkl)", styles['TableCell']),
            Paragraph("High Complexity (Requires Scikit-Learn setup)", styles['TableCell']),
            Paragraph("Linux only; no native Windows execution; heavy C-extensions; zero visual, text, or temporal support.", styles['TableCell'])
        ],
        [
            Paragraph("<b>AutoKeras</b>", styles['TableCellBold']),
            Paragraph("Vision, Text, Structured", styles['TableCell']),
            Paragraph("Fixed neural preprocessing layers", styles['TableCell']),
            Paragraph("No (Multi-directory SavedModel hierarchy)", styles['TableCell']),
            Paragraph("Heavy (Requires multi-GB TensorFlow/CUDA)", styles['TableCell']),
            Paragraph("Prohibitive GPU memory footprints; long search latency; fragile multi-file directory structures.", styles['TableCell'])
        ],
        [
            Paragraph("<b>TPOT</b>", styles['TableCellBold']),
            Paragraph("Tabular Only", styles['TableCell']),
            Paragraph("Genetic pipeline optimization", styles['TableCell']),
            Paragraph("No (Outputs generated Python script)", styles['TableCell']),
            Paragraph("Manual (User must compile and run script)", styles['TableCell']),
            Paragraph("Extremely slow genetic search; no visual or NLP support; prone to overfitting on small datasets.", styles['TableCell'])
        ],
        [
            Paragraph("<b>H2O Driverless AI</b>", styles['TableCellBold']),
            Paragraph("Tabular, Text, Time-Series", styles['TableCell']),
            Paragraph("Proprietary genetic feature engineering", styles['TableCell']),
            Paragraph("Partial (MOJO runtime archive)", styles['TableCell']),
            Paragraph("Moderate (Java JVM / C++ runtime required)", styles['TableCell']),
            Paragraph("High enterprise licensing fees; closed-source; complex enterprise server installation; no deep vision transfer learning.", styles['TableCell'])
        ],
        [
            Paragraph("<b>PyCaret</b>", styles['TableCellBold']),
            Paragraph("Tabular, Time-Series, NLP", styles['TableCell']),
            Paragraph("Semi-automated (Requires extensive setup code)", styles['TableCell']),
            Paragraph("No (Saves separate pkl, pipeline pkl)", styles['TableCell']),
            Paragraph("Moderate (Must match PyCaret environment)", styles['TableCell']),
            Paragraph("Not a true no-code UI platform; requires Python notebook programming; manual feature reconciliation.", styles['TableCell'])
        ],
        [
            Paragraph("<b>Google Vertex AI / AWS SageMaker</b>", styles['TableCellBold']),
            Paragraph("Multimodal (Cloud)", styles['TableCell']),
            Paragraph("Autonomous cloud data pipelines", styles['TableCell']),
            Paragraph("No (Locked to proprietary cloud endpoints)", styles['TableCell']),
            Paragraph("Vendor Locked (Requires cloud credentials)", styles['TableCell']),
            Paragraph("Expensive per-hour billing; vendor lock-in; impossible to run offline on air-gapped workstations or edge devices.", styles['TableCell'])
        ],
        [
            Paragraph("<b>AI Model Forge (Proposed)</b>", styles['TableCellBold']),
            Paragraph("Tabular, Vision, Text, Time-Series", styles['TableCell']),
            Paragraph("Autonomous cleaning, imputation, scaling, encoding, lag generation, and vision augmentation", styles['TableCell']),
            Paragraph("<b>YES (Exactly ONE single .aiforge file)</b>", styles['TableCell']),
            Paragraph("<b>Ultra-Simple (3-line SDK predict on raw inputs)</b>", styles['TableCell']),
            Paragraph("Open-source, runs natively on Windows/Linux or in Docker, zero cloud cost, 100% self-contained inference.", styles['TableCell'])
        ]
    ]

    comp_table = Table(comp_table_data, colWidths=[65, 65, 85, 75, 75, 122])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#eff6ff')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>In-Depth Analysis of Existing Architectural Limitations:</b>",
        styles['ParagraphBold']
    ))
    story.append(Paragraph(
        "1. <i>The Deployment Disconnect:</i> In every open-source tool surveyed (Auto-Sklearn, TPOT, PyCaret), the exported model "
        "is decoupled from its preprocessing pipeline. When an application engineer deploys the model in a FastAPI or Flask microservice, "
        "incoming HTTP JSON payloads must be manually scaled and encoded. If the training data had 15 categories for 'city' and a new "
        "record arrives with an unseen city, the pipeline throws unhandled exceptions. AI Model Forge eliminates this by guaranteeing that "
        "every .aiforge file encapsulates both the model weights AND the fitted ColumnTransformer configured with <code>handle_unknown='ignore'</code>.",
        styles['Paragraph']
    ))
    story.append(Paragraph(
        "2. <i>The Cloud Trap:</i> Cloud AutoML solutions (AWS SageMaker Autopilot, Google Vertex AI) solve multimodal ingestion, but at the cost "
        "of severe vendor lock-in, data privacy violations, and recurring hourly expenses. Confidential patient health records (e.g. chest X-rays) "
        "or proprietary financial transaction logs cannot legally be uploaded to public third-party endpoints. AI Model Forge runs 100% locally "
        "or on self-hosted infrastructure, ensuring strict data sovereignty and zero telemetry leakage.",
        styles['Paragraph']
    ))
    story.append(Paragraph(
        "3. <i>The Lack of Verification Gates:</i> Conventional frameworks write a model file to disk and immediately assume it is operational. "
        "They do not perform post-packaging re-loading or holdout sanity validation. AI Model Forge introduces the <code>ModelValidator</code>: "
        "a mandatory verification gate that reloads the newly compressed .aiforge package in an isolated process, executes inference on a holdout sample, "
        "checks SHA-256 integrity, and only unlocks the download button once sanity is proven.",
        styles['Paragraph']
    ))

    story.append(Spacer(1, 10))

    # 1.3 Objectives
    story.append(Paragraph("1.3 Objectives", styles['SectionHeader']))

    story.append(Paragraph(
        "The primary goal of AI Model Forge is to build a unified, accessible, and production-grade Multimodal AutoML Platform "
        "that automates the path from a user's natural language requirement to an operational, single-file model package.",
        styles['Paragraph']
    ))

    story.append(Paragraph("<b>Primary Architectural Objectives:</b>", styles['ParagraphBold']))
    story.append(Paragraph("1. <b>Autonomous Modality Detection:</b> Inspect uploaded files, MIME types, folder structures, and sample content to determine modality (Tabular, Vision, Text, Time-Series, Audio, Video, Document) with confidence metrics.", styles['BulletItem']))
    story.append(Paragraph("2. <b>Semantic Natural Language Parsing:</b> Extract business intent, candidate target columns, and task types (Classification, Regression, Forecasting), while strictly rejecting unsupported requests.", styles['BulletItem']))
    story.append(Paragraph("3. <b>Automated Data Cleaning & Leakage Prevention:</b> Automatically impute missing values (median/mode), scale numericals, One-Hot Encode categoricals with unknown handling, exclude IDs, and filter target leakage candidates (|r| >= 0.99).", styles['BulletItem']))
    story.append(Paragraph("4. <b>Unified Plugin Trainer Registry:</b> Architect an extensible <code>TrainerRegistry</code> supporting Tabular, PyTorch Computer Vision (MobileNetV2), Text NLP (sublinear TF-IDF), and strict chronological Time-Series autoregression.", styles['BulletItem']))
    story.append(Paragraph("5. <b>Single-File Container (.aiforge):</b> Package weights, ColumnTransformers, input/output schemas, and SHA-256 manifest into exactly ONE downloadable file.", styles['BulletItem']))
    story.append(Paragraph("6. <b>Lightweight Client Runtime SDK (aiforge_runtime):</b> Enable external developers to execute predictions with 3 lines of code on raw, un-preprocessed inputs.", styles['BulletItem']))
    story.append(Paragraph("7. <b>Interactive Web-Based Studio:</b> Provide an asynchronous FastAPI backend and modern React 18 / Vite frontend with drag-and-drop ingestion, live telemetry, and an in-browser prediction playground.", styles['BulletItem']))

    story.append(Spacer(1, 10))

    # 1.4 Proposed AI-Assisted Approach
    story.append(Paragraph("1.4 Proposed AI-Assisted Approach", styles['SectionHeader']))

    story.append(Paragraph(
        "To achieve production-grade quality, zero hallucinations, and high modularity across five distinct machine learning "
        "domains, this project utilized an advanced <b>AI-Assisted Software Development Methodology</b>. Rather than relying on "
        "unstructured or speculative code generation, development was orchestrated through systematic prompt engineering protocols, "
        "test-driven validation gates, and collaborative human-AI pair programming.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "The project methodology proceeded across four iterative, synergistic phases:",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "• <b>Phase I: Intent & Requirement Co-Design:</b> Interactive prompt sessions were conducted to define formal functional "
        "requirements, non-functional performance boundaries, and security constraints. Prompts forced the AI assistant to analyze "
        "operational failure modes—such as Zip Slip path-traversal exploits, out-of-memory crashes on large CSVs, and future information "
        "leakage in sequential time-series forecasting. The resulting requirements were codified into testable Gherkin acceptance criteria.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "• <b>Phase II: Architectural Synthesis and Module Decoupling:</b> Using structural design prompts, the AI assistant synthesized "
        "the <code>BaseTrainer</code> abstract base class and <code>TrainerRegistry</code> pattern. This decoupled heavy deep-learning dependencies "
        "(PyTorch, TorchVision) from lightweight classical tabular algorithms (Scikit-Learn), ensuring that new modalities (e.g. Audio, Video, "
        "Object Detection) can be registered without modifying the core web server or packaging pipeline.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "• <b>Phase III: Test-Driven Code Implementation with Safety Guardrails:</b> Code generation was conducted service by service. "
        "Strict prompt instructions prohibited dummy return values, fake training loops, or hardcoded predictions. Every trainer was required "
        "to execute real Scikit-Learn fit routines or PyTorch training loops on authentic data matrices. Security wrappers were applied "
        "to validate archive paths and verify input schemas.",
        styles['Paragraph']
    ))

    story.append(Paragraph(
        "• <b>Phase IV: AI-Assisted Test Synthesis and Automated Debugging:</b> Programmatic synthetic test datasets were constructed in "
        "<code>backend/tests/conftest.py</code> covering Tabular Churn, House Prices, Cats vs. Dogs Vision, Review Sentiment, and Electricity Demand. "
        "The AI generated 7 comprehensive test suites. When real-world edge-case bugs emerged during test runs—such as Starlette HTTPX deprecation, "
        "duplicate ZIP manifest entries, and continuous numeric column false-positive ID classification—AI-assisted diagnostic prompt cycles "
        "isolated root causes and synthesized hardened, regression-proof patches.",
        styles['Paragraph']
    ))

    story.append(PageBreak())
    return story
