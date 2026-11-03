from reportlab.platypus import Paragraph, Spacer, PageBreak, HRFlowable
from reportlab.lib import colors

def generate_ch7(styles):
    story = []

    # Chapter Header
    story.append(Paragraph("7. REFERENCES", styles['ChapterHeader']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e3a8a'), spaceBefore=2, spaceAfter=14))

    story.append(Paragraph(
        "The development and architectural formulation of AI Model Forge are grounded in established peer-reviewed literature "
        "spanning Automated Machine Learning (AutoML), Combined Algorithm Selection and Hyperparameter optimization (CASH), "
        "software architectural patterns, cybersecurity sandboxing, and high-performance asynchronous web systems. "
        "The following academic papers, textbooks, and formal technical standards guided the project implementation:",
        styles['Paragraph']
    ))
    story.append(Spacer(1, 6))

    references = [
        ("[1] M. Feurer, A. Klein, K. Eggensperger, J. Springenberg, M. Blum, and F. Hutter, 'Efficient and Robust Automated Machine Learning,' in Advances in Neural Information Processing Systems (NeurIPS), vol. 28, pp. 2755–2763, 2015.",
         "Foundational formulation of the CASH problem, Bayesian optimization with surrogate models, and automated ensemble construction."),

        ("[2] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, et al., 'Scikit-learn: Machine Learning in Python,' Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.",
         "Core reference for ColumnTransformer pipelines, StratifiedKFold cross-validation, and standardized estimator interfaces."),

        ("[3] A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, et al., 'PyTorch: An Imperative Style, High-Performance Deep Learning Library,' in Advances in Neural Information Processing Systems (NeurIPS), vol. 32, pp. 8024–8035, 2019.",
         "Framework foundation for transfer learning routines, dynamic neural module execution, and tensor graph backpropagation."),

        ("[4] M. Sandler, A. Howard, M. Zhu, A. Zhmoginov, and L. C. Chen, 'MobileNetV2: Inverted Residuals and Linear Bottlenecks,' in IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pp. 4510–4520, 2018.",
         "Architectural specification for the inverted residual block and lightweight convolutional backbone enabling real-time edge computer vision."),

        ("[5] K. He, X. Zhang, S. Ren, and J. Sun, 'Deep Residual Learning for Image Recognition,' in IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pp. 770–778, 2016.",
         "Mathematical formulation of skip/identity connections overcoming vanishing gradient degradation in deep architectures."),

        ("[6] R. S. Olson and J. H. Moore, 'TPOT: A Tree-based Pipeline Optimization Tool for Automating Machine Learning,' in Proceedings of the Workshop on Automatic Machine Learning, ICML, pp. 66–74, 2016.",
         "Genetic programming paradigm for AutoML pipeline synthesis and feature transformation graph representation."),

        ("[7] H. Jin, Q. Song, and X. Hu, 'Auto-Keras: An Efficient Library for Automated Machine Learning,' in ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, pp. 1946–1956, 2019.",
         "Network morphism and neural architecture search principles guiding dynamic computer vision model generation."),

        ("[8] L. Breiman, 'Random Forests,' Machine Learning, vol. 45, no. 1, pp. 5–32, 2001.",
         "Theoretical foundations of bootstrap aggregating (bagging) and out-of-bag error estimation in tabular decision tree ensembles."),

        ("[9] J. H. Friedman, 'Greedy Function Approximation: A Gradient Boosting Machine,' Annals of Statistics, vol. 29, no. 5, pp. 1189–1232, 2001.",
         "Fundamental formulation of steepest descent in function space for iterative loss minimization in gradient boosted trees."),

        ("[10] G. Ke, Q. Meng, T. Finley, T. Wang, W. Chen, W. Ma, et al., 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree,' in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 3146–3154, 2017.",
         "Histogram-based feature binning and Gradient-based One-Side Sampling (GOSS) algorithms utilized for high-throughput tabular learning."),

        ("[11] T. Chen and C. Guestrin, 'XGBoost: A Scalable Tree Boosting System,' in ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp. 785–794, 2016.",
         "Second-order Taylor approximation and sparsity-aware split finding algorithms for robust non-linear feature interaction modeling."),

        ("[12] S. Bird, E. Klein, and E. Loper, 'Natural Language Processing with Python: Analyzing Text with the Natural Language Toolkit,' O'Reilly Media, Inc., 2009.",
         "Standard text tokenization, vocabulary stopword filtration, and n-gram statistical extraction methodologies."),

        ("[13] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, et al., 'Attention Is All You Need,' in Advances in Neural Information Processing Systems (NeurIPS), vol. 30, pp. 5998–6008, 2017.",
         "Self-attention mechanism and transformer architecture underpinning future multimodal embedding expansion."),

        ("[14] R. J. Hyndman and G. Athanasopoulos, 'Forecasting: Principles and Practice,' 3rd ed., OTexts: Melbourne, Australia, 2021.",
         "Theoretical principles of chronological time-series cross-validation, rolling window evaluation, and seasonal lag feature synthesis."),

        ("[15] S. Ramirez-Gallego, B. Krawczyk, S. García, M. Woźniak, and F. Herrera, 'A Survey on Data Preprocessing for Data Stream Mining: Current Status and Future Directions,' Neurocomputing, vol. 239, pp. 39–57, 2017.",
         "Survey of streaming data imputation, concept drift detection, and automated categorical encoding mechanisms."),

        ("[16] D. Sculley, G. Holt, D. Golovin, E. Davydov, T. Phillips, D. Ebner, et al., 'Hidden Technical Debt in Machine Learning Systems,' in Advances in Neural Information Processing Systems (NeurIPS), vol. 28, pp. 2503–2511, 2015.",
         "Analysis of glue code, pipeline jungles, and dead-ends in production ML systems that inspired AI Model Forge's single-file self-contained format."),

        ("[17] S. Schelter, J. H. Boese, E. Kitanov, M. Seeger, and F. Bießmann, 'Automatically Tracking Metadata and Provenance of Machine Learning Pipelines,' in ML Systems Workshop at NeurIPS, 2017.",
         "Design principles for end-to-end dataset profiling, lineage tracking, and cryptographic checksum auditing."),

        ("[18] M. Abadi, P. Barham, J. Chen, Z. Chen, A. Davis, J. Dean, et al., 'TensorFlow: A System for Large-Scale Machine Learning,' in 12th USENIX Symposium on Operating Systems Design and Implementation (OSDI 16), pp. 265–283, 2016.",
         "Computation graph execution paradigms and heterogeneous device scheduling."),

        ("[19] T. Ramírez et al., 'FastAPI: Modern, Fast (High-Performance) Web Framework for Building APIs with Python 3.7+ Based on Standard Type Hints,' 2018. [Online]. Available: https://fastapi.tiangolo.com/.",
         "Asynchronous ASGI request dispatching, automatic OpenAPI documentation, and Pydantic v2 data validation engines."),

        ("[20] React Development Team, 'React: A JavaScript Library for Building User Interfaces,' Meta Open Source, 2024. [Online]. Available: https://react.dev/.",
         "Virtual DOM reconciliation, declarative UI state management, and reusable component architectures."),

        ("[21] Vite Development Team, 'Vite: Next Generation Frontend Tooling,' 2024. [Online]. Available: https://vitejs.dev/.",
         "Native ES-module Hot Module Replacement (HMR) and Rollup-powered production bundling."),

        ("[22] S. Chacon and B. Straub, 'Pro Git,' 2nd ed., Apress, 2014.",
         "Distributed version control workflows, commit history hygiene, and software release branching strategies."),

        ("[23] E. Gamma, R. Helm, R. Johnson, and J. Vlissides, 'Design Patterns: Elements of Reusable Object-Oriented Software,' Addison-Wesley, 1994.",
         "Classic design patterns utilized across the platform: Abstract Factory, Strategy Pattern (TrainerRegistry), and Adapter (Predictors)."),

        ("[24] NIST, 'Secure Hash Standard (SHS),' Federal Information Processing Standards Publication (FIPS PUB 180-4), National Institute of Standards and Technology, 2015.",
         "Cryptographic specification for SHA-256 integrity verification implemented across single-file .aiforge manifests."),

        ("[25] OWASP Foundation, 'Zip Slip Vulnerability: Arbitrary File Overwrite Through Archive Extraction,' OWASP Security Guidelines, 2018. [Online]. Available: https://owasp.org/.",
         "Cybersecurity guidelines for mitigating directory traversal path manipulation attacks during ZIP archive extraction."),

        ("[26] N. V. Chawla, K. W. Bowyer, L. O. Hall, and W. P. Kegelmeyer, 'SMOTE: Synthetic Minority Over-sampling Technique,' Journal of Artificial Intelligence Research, vol. 16, pp. 321–357, 2002.",
         "Mathematical formulation of synthetic minority interpolation for extreme class imbalance compensation."),

        ("[27] J. MacQueen, 'Some Methods for Classification and Analysis of Multivariate Observations,' in 5th Berkeley Symposium on Mathematical Statistics and Probability, vol. 1, pp. 281–297, 1967.",
         "Foundational formulation of k-means clustering utilized in tabular exploratory profiling."),

        ("[28] C. E. Shannon, 'A Mathematical Theory of Communication,' Bell System Technical Journal, vol. 27, no. 3, pp. 379–423, 1948.",
         "Information entropy formulas applied in high-cardinality feature detection and target leakage measurement."),

        ("[29] K. Pearson, 'Notes on Regression and Inheritance in the Case of Two Variable,' Proceedings of the Royal Society of London, vol. 58, pp. 240–242, 1895.",
         "Linear correlation coefficients applied in LeakageDetector to intercept redundant or duplicate features."),

        ("[30] C. M. Bishop, 'Pattern Recognition and Machine Learning,' Springer, New York, 2006.",
         "Theoretical foundations of regularized empirical risk minimization, Ridge regression, and Bayesian model evidence."),

        ("[31] I. Goodfellow, Y. Bengio, and A. Courville, 'Deep Learning,' MIT Press, Cambridge, MA, 2016.",
         "Comprehensive treatise on convolutional neural networks, backpropagation, and regularization in deep learning."),

        ("[32] E. Alpaydin, 'Introduction to Machine Learning,' 4th ed., MIT Press, Cambridge, MA, 2020.",
         "Textbook treatment of model selection, cross-validation variance bounds, and nonparametric estimation."),

        ("[33] M. Fowler, 'Refactoring: Improving the Design of Existing Code,' 2nd ed., Addison-Wesley, Boston, MA, 2018.",
         "Core principles of code hygiene, extract-method refactoring, and automated test regression safety."),

        ("[34] R. C. Martin, 'Clean Architecture: A Craftsman's Guide to Software Structure and Design,' Prentice Hall, 2017.",
         "Decoupled architectural principles ensuring business logic remains independent of UI, databases, and frameworks."),

        ("[35] IEEE Computer Society, 'IEEE Standard for Software and System Test Documentation,' IEEE Std 829-2008, 2008.",
         "Standardized structure for test plans, edge-case test matrices, execution logs, and defect resolution reporting.")
    ]

    for ref, annot in references:
        story.append(Paragraph(f"<b>{ref}</b>", styles['ParagraphBold']))
        story.append(Paragraph(f"<i>Architectural Relevance:</i> {annot}", styles['CalloutText']))
        story.append(Spacer(1, 3))

    story.append(PageBreak())
    return story
