from pathlib import Path
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
from reportlab.lib import colors

def generate_cover_page(styles, logo_path: Path):
    story = []

    # 1. Top Logo
    if logo_path and logo_path.exists():
        im = Image(str(logo_path), width=160, height=70)
        im.hAlign = 'CENTER'
        story.append(im)
        story.append(Spacer(1, 10))

    # 2. Institution Details
    story.append(Paragraph("D.K.T.E. Society's Textile and Engineering Institute, Ichalkaranji.", styles['CoverInstitution']))
    story.append(Paragraph("(An Empowered Autonomous Institute, Affiliated to Shivaji University, Kolhapur)", styles['CoverSubInstitution']))
    story.append(Paragraph("Department of Computer Science & Engineering", styles['CoverDept']))
    story.append(Paragraph("Academic Year 2026 - 2027", styles['CoverYear']))

    story.append(HRFlowable(width="90%", thickness=1.5, color=colors.HexColor('#d97706'), spaceBefore=2, spaceAfter=14))

    # 3. Report Subject & Project Title
    story.append(Paragraph("AI Tools for Software Development Project Report On", styles['CoverType']))
    story.append(Paragraph("AI Model Forge: Universal Multimodal AutoML Platform and Single-File Artifact Packaging Engine", styles['CoverTitle']))
    story.append(Paragraph('"Upload your data. Describe what you want. Get a ready-to-use AI model."', styles['CoverTagline']))

    story.append(Spacer(1, 15))

    # 4. Guidance & Submission Details Table
    story.append(Paragraph("Under The Guidance Of", styles['CoverLabel']))
    story.append(Paragraph("Dr. P. M. Gavali", styles['CoverSignerName']))
    story.append(Paragraph("Department of Computer Science & Engineering", styles['CoverSignerRole']))

    story.append(Spacer(1, 18))

    story.append(Paragraph("Submitted By:", styles['CoverLabel']))
    student_table_data = [
        [Paragraph("<b>PRN Number</b>", styles['TableHead']), Paragraph("<b>Name of Student</b>", styles['TableHead'])],
        [Paragraph("23UCS025", styles['TableCellBold']), Paragraph("Vaibhav M Datar", styles['TableCellBold'])]
    ]
    student_table = Table(student_table_data, colWidths=[180, 260])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    student_table.hAlign = 'CENTER'
    story.append(student_table)

    story.append(Spacer(1, 35))

    # 5. Signatures Block (Matching Template)
    sig_data = [
        [
            Paragraph("<b>Dr. P. M. Gavali</b><br/>Project Guide", styles['CoverSignerName']),
            Paragraph("<b>Prof. (Dr.) D. V. Kodavade</b><br/>Head of Department", styles['CoverSignerName'])
        ],
        [Spacer(1, 30), Spacer(1, 30)],
        [
            Paragraph("<b>External Examiner</b>", styles['CoverSignerName']),
            Paragraph("<b>Department Seal & Date</b>", styles['CoverSignerName'])
        ]
    ]
    sig_table = Table(sig_data, colWidths=[240, 240])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    sig_table.hAlign = 'CENTER'
    story.append(sig_table)

    story.append(PageBreak())
    return story

def generate_certificate_page(styles):
    story = []
    story.append(Paragraph("D.K.T.E. Society's Textile and Engineering Institute, Ichalkaranji.", styles['CoverInstitution']))
    story.append(Paragraph("Department of Computer Science & Engineering", styles['CoverDept']))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=6, spaceAfter=20))

    story.append(Paragraph("CERTIFICATE", styles['CoverTitle']))
    story.append(Spacer(1, 15))

    cert_text = (
        "This is to certify that the project report entitled <b>'AI Model Forge: Universal Multimodal "
        "AutoML Platform and Single-File Artifact Packaging Engine'</b> submitted by <b>Vaibhav M Datar (PRN: 23UCS025)</b> "
        "is a bonafide record of work carried out by him under our supervision and guidance in partial fulfillment "
        "of the requirements for the course <i>AI Tools for Software Development</i> in the Department of Computer "
        "Science & Engineering during the academic year 2026-2027."
    )
    story.append(Paragraph(cert_text, styles['Paragraph']))
    story.append(Spacer(1, 15))

    cert_text_2 = (
        "The project demonstrates end-to-end autonomous machine learning across Tabular, Vision, Natural Language "
        "Processing, and Time-Series modalities, featuring automated data profiling, automated feature engineering, "
        "transfer learning, model benchmarking, single-file containerized packaging (.aiforge), and zero-configuration "
        "inference through an integrated runtime SDK. The work presented herein is genuine and satisfies all academic "
        "standards set by the Empowered Autonomous Institute and Shivaji University, Kolhapur."
    )
    story.append(Paragraph(cert_text_2, styles['Paragraph']))
    story.append(Spacer(1, 60))

    sig_data = [
        [
            Paragraph("<b>Dr. P. M. Gavali</b><br/>Project Guide<br/>Dept. of CSE, DKTE", styles['CoverSignerName']),
            Paragraph("<b>Prof. (Dr.) D. V. Kodavade</b><br/>Head of Department<br/>Dept. of CSE, DKTE", styles['CoverSignerName'])
        ],
        [Spacer(1, 60), Spacer(1, 60)],
        [
            Paragraph("<b>External Examiner</b>", styles['CoverSignerName']),
            Paragraph("<b>Director / Dean Academics</b>", styles['CoverSignerName'])
        ]
    ]
    t = Table(sig_data, colWidths=[240, 240])
    t.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    t.hAlign = 'CENTER'
    story.append(t)

    story.append(PageBreak())
    return story

def generate_acknowledgements_and_abstract(styles):
    story = []
    story.append(Paragraph("ACKNOWLEDGEMENTS", styles['SectionHeader']))
    story.append(Paragraph(
        "I express my deepest gratitude to my project guide, <b>Dr. P. M. Gavali</b>, for his continuous encouragement, "
        "incisive technical feedback, and invaluable guidance throughout the ideation, system design, and implementation "
        "phases of the <b>AI Model Forge</b> project. His emphasis on software engineering discipline, edge-case mitigation, "
        "and reproducible benchmarking was pivotal in achieving high system robustness.",
        styles['Paragraph']
    ))
    story.append(Paragraph(
        "I am profoundly grateful to <b>Prof. (Dr.) D. V. Kodavade</b>, Head of the Department of Computer Science & Engineering, "
        "for providing advanced laboratory infrastructure, software resources, and an academically stimulating environment "
        "conducive to state-of-the-art software engineering research and AI development.",
        styles['Paragraph']
    ))
    story.append(Paragraph(
        "Furthermore, I acknowledge the management and academic leadership of D.K.T.E. Society's Textile and Engineering "
        "Institute for fostering innovation and technical excellence. Lastly, I extend sincere thanks to my peers and family "
        "whose unwavering support motivated the successful completion of this extensive engineering endeavor.",
        styles['Paragraph']
    ))

    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=0.75, color=colors.HexColor('#cbd5e1'), spaceBefore=8, spaceAfter=15))

    story.append(Paragraph("ABSTRACT", styles['SectionHeader']))
    story.append(Paragraph(
        "Modern artificial intelligence and machine learning (AI/ML) workflows are plagued by severe fragmentation, high "
        "cognitive overhead, and brittle multi-file deployment architectures. Practitioners are routinely forced to manually "
        "inspect raw data, write custom imputation and encoding logic, configure deep learning transfer backbones, manage "
        "disparate serialized files (.pkl, .pt, .json, .yaml), and manually synchronize inference-time data transformations "
        "with training-time features—leading to ubiquitous training-serving skew, memory leaks, and silent prediction failures.",
        styles['Paragraph']
    ))
    story.append(Paragraph(
        "This project presents <b>AI Model Forge</b>, an intelligent, universal multimodal AutoML platform and packaging engine "
        "governed by the philosophy: <i>'Upload your data. Describe what you want. Get a ready-to-use AI model.'</i> The platform "
        "implements an end-to-end automated pipeline comprising: (1) automated multimodal dataset understanding (Tabular, Vision, "
        "Text NLP, and Time-Series) with heuristic MIME and structural inspection; (2) natural language requirement parsing with "
        "strict task boundaries that honestly reject unsupported capabilities like object detection; (3) memory-aware profiling "
        "with automated data engineering, column classification, ID exclusion, and target leakage prevention; (4) a plugin-based "
        "TrainerRegistry supporting Random Forest, Histogram Gradient Boosting, PyTorch MobileNetV2 Transfer Learning, and TF-IDF "
        "vectorization; (5) strict chronological time-series splitting to eliminate future-lookahead leakage; and (6) a unified, "
        "single-file artifact container format (<b>.aiforge</b>) secured by SHA-256 manifests.",
        styles['Paragraph']
    ))
    story.append(Paragraph(
        "A companion Python runtime SDK (<code>aiforge_runtime</code>) enables external client applications to execute predictions "
        "with three lines of code on raw, un-preprocessed inputs. The platform features an asynchronous FastAPI backend, a modern "
        "React 18 / Vite frontend with live telemetry logs and in-browser interactive testing sandbox, and 100% automated test "
        "coverage across all modalities. The project establishes an accessible, production-grade standard for autonomous model training.",
        styles['Paragraph']
    ))

    story.append(PageBreak())
    return story

def generate_index_page(styles):
    story = []
    story.append(Paragraph("INDEX", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=12))

    index_data = [
        [Paragraph("<b>Sr. No.</b>", styles['TableHead']), Paragraph("<b>Chapter / Topic Title</b>", styles['TableHead']), Paragraph("<b>Page No.</b>", styles['TableHead'])],
        [Paragraph("<b>1</b>", styles['TableCellBold']), Paragraph("<b>Introduction</b>", styles['TableCellBold']), Paragraph("<b>5</b>", styles['TableCellBold'])],
        [Paragraph("", styles['TableCell']), Paragraph("1.1 Project Overview and Problem Statement", styles['TableCell']), Paragraph("5", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("1.2 Existing Project and Limitations", styles['TableCell']), Paragraph("6", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("1.3 Objectives", styles['TableCell']), Paragraph("7", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("1.4 Proposed AI-Assisted Approach", styles['TableCell']), Paragraph("8", styles['TableCell'])],
        [Paragraph("<b>2</b>", styles['TableCellBold']), Paragraph("<b>Requirement Analysis</b>", styles['TableCellBold']), Paragraph("<b>9</b>", styles['TableCellBold'])],
        [Paragraph("", styles['TableCell']), Paragraph("2.1 Functional and Non-Functional Requirements", styles['TableCell']), Paragraph("9", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("2.2 User Stories and Acceptance Criteria", styles['TableCell']), Paragraph("11", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("2.3 Prompts, AI Outputs and Refinement", styles['TableCell']), Paragraph("13", styles['TableCell'])],
        [Paragraph("<b>3</b>", styles['TableCellBold']), Paragraph("<b>System Design</b>", styles['TableCellBold']), Paragraph("<b>15</b>", styles['TableCellBold'])],
        [Paragraph("", styles['TableCell']), Paragraph("3.1 System Architecture and Module Design", styles['TableCell']), Paragraph("15", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("3.2 User Interface Design / Wireframes", styles['TableCell']), Paragraph("18", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("3.3 Design Prompts, AI Outputs and Final Design", styles['TableCell']), Paragraph("19", styles['TableCell'])],
        [Paragraph("<b>4</b>", styles['TableCellBold']), Paragraph("<b>Coding and Implementation</b>", styles['TableCellBold']), Paragraph("<b>20</b>", styles['TableCellBold'])],
        [Paragraph("", styles['TableCell']), Paragraph("4.1 Development Environment and Technology Stack", styles['TableCell']), Paragraph("20", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("4.2 AI-Assisted Code Generation", styles['TableCell']), Paragraph("21", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("4.3 Debugging, Refactoring and Code Optimization", styles['TableCell']), Paragraph("21", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("4.4 In-Depth Component Implementations & Algorithms", styles['TableCell']), Paragraph("23", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("4.5 Coding Prompts, Generated Code and Modifications", styles['TableCell']), Paragraph("25", styles['TableCell'])],
        [Paragraph("<b>5</b>", styles['TableCellBold']), Paragraph("<b>Testing</b>", styles['TableCellBold']), Paragraph("<b>27</b>", styles['TableCellBold'])],
        [Paragraph("", styles['TableCell']), Paragraph("5.1 Testing Strategy and Test Plan", styles['TableCell']), Paragraph("27", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("5.2 AI-Generated Test Cases", styles['TableCell']), Paragraph("27", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("5.3 Unit, Integration and System Testing", styles['TableCell']), Paragraph("28", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("5.4 Defect Identification and AI-Assisted Debugging", styles['TableCell']), Paragraph("29", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("5.5 Hardware Profiling, Prompts and Actual Results", styles['TableCell']), Paragraph("30", styles['TableCell'])],
        [Paragraph("<b>6</b>", styles['TableCellBold']), Paragraph("<b>Deployment and Documentation</b>", styles['TableCellBold']), Paragraph("<b>32</b>", styles['TableCellBold'])],
        [Paragraph("", styles['TableCell']), Paragraph("6.1 Deployment and Execution Procedure", styles['TableCell']), Paragraph("32", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("6.2 Deployment Prompts and Configuration", styles['TableCell']), Paragraph("34", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("6.3 User Manual and Technical Documentation", styles['TableCell']), Paragraph("34", styles['TableCell'])],
        [Paragraph("<b>7</b>", styles['TableCellBold']), Paragraph("<b>References</b>", styles['TableCellBold']), Paragraph("<b>37</b>", styles['TableCellBold'])],
        [Paragraph("<b>8</b>", styles['TableCellBold']), Paragraph("<b>Appendices</b>", styles['TableCellBold']), Paragraph("<b>41</b>", styles['TableCellBold'])],
        [Paragraph("", styles['TableCell']), Paragraph("Appendix A: Complete Prompt Dictionary and Prompt History", styles['TableCell']), Paragraph("41", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("Appendix B: AI Tool Usage Log", styles['TableCell']), Paragraph("45", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("Appendix C: Important Source Code and Architecture Listings", styles['TableCell']), Paragraph("46", styles['TableCell'])],
        [Paragraph("", styles['TableCell']), Paragraph("Appendix D: Test Cases and Execution Evidence", styles['TableCell']), Paragraph("50", styles['TableCell'])],
    ]

    t = Table(index_data, colWidths=[55, 375, 57])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.2),
    ]))
    story.append(t)

    story.append(PageBreak())
    return story
