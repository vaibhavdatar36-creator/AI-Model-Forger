import React from 'react';
import { Sparkles, ArrowRight, Database, Cpu, CheckCircle2, PackageCheck, Zap, ShieldCheck } from 'lucide-react';

export default function Home({ onStartCreate }) {
  return (
    <div className="container">
      <div className="hero">
        <div className="hero-badge">
          <Sparkles size={14} />
          UNIVERSAL MULTIMODAL AUTOML PLATFORM v1.0
        </div>
        <h1 className="hero-title">
          Upload your data. Describe what you want. <br />
          <span>Get a ready-to-use AI model.</span>
        </h1>
        <p className="hero-subtitle">
          AI Model Forge automates the entire machine-learning lifecycle across Tabular, Vision, NLP, and Time-Series data. 
          Zero manual preprocessing required. Get one downloadable <code>.aiforge</code> artifact with complete self-contained inference.
        </p>
        <button className="btn btn-primary btn-lg" onClick={onStartCreate}>
          Build Your AI Model Now
          <ArrowRight size={20} />
        </button>
      </div>

      <div className="workflow-grid">
        <div className="step-card">
          <div className="step-num">01 / INPUT</div>
          <h3 className="step-title">Requirement & Raw Data</h3>
          <p className="step-desc">
            Provide your intent in natural language and upload raw CSV, Excel, Parquet, JSON, images, or time-series datasets.
          </p>
        </div>

        <div className="step-card">
          <div className="step-num">02 / UNDERSTAND</div>
          <h3 className="step-title">Automatic Intelligence</h3>
          <p className="step-desc">
            Detects modality, target variable, task type, handles class imbalances, outliers, and cleans raw data without human intervention.
          </p>
        </div>

        <div className="step-card">
          <div className="step-num">03 / TRAIN & EVAL</div>
          <h3 className="step-title">Resource-Aware AutoML</h3>
          <p className="step-desc">
            Trains and benchmarks candidate architectures (Random Forest, Gradient Boosting, Transfer Learning CNNs, TF-IDF NLP) with live progress.
          </p>
        </div>

        <div className="step-card">
          <div className="step-num">04 / DEPLOY</div>
          <h3 className="step-title">One .aiforge Artifact</h3>
          <p className="step-desc">
            Downloads a single versioned file containing model weights, preprocessors, and schemas. Run predictions anywhere via the Python Runtime SDK.
          </p>
        </div>
      </div>

      <div className="card" style={{ marginTop: '3rem' }}>
        <h3 className="card-title">
          <Zap className="text-indigo-400" size={22} />
          Supported Modalities & Architectures
        </h3>
        <p className="card-subtitle">
          Engineered with an extensible plugin registry allowing seamless additions of future modalities.
        </p>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.25rem' }}>
          <div style={{ padding: '1.25rem', background: 'rgba(15, 23, 42, 0.5)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <span className="badge badge-blue" style={{ marginBottom: '0.6rem' }}>TABULAR</span>
            <h4 style={{ fontWeight: 700, margin: '0.4rem 0' }}>Classification & Regression</h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              Random Forest, HistGradientBoosting, One-Hot Encoding, scaling, ID exclusion & leakage detection.
            </p>
          </div>

          <div style={{ padding: '1.25rem', background: 'rgba(15, 23, 42, 0.5)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <span className="badge badge-purple" style={{ marginBottom: '0.6rem' }}>IMAGE</span>
            <h4 style={{ fontWeight: 700, margin: '0.4rem 0' }}>Computer Vision Classification</h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              PyTorch MobileNetV2 / ResNet18 transfer learning, data augmentation, automatic 224x224 RGB standardization.
            </p>
          </div>

          <div style={{ padding: '1.25rem', background: 'rgba(15, 23, 42, 0.5)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <span className="badge badge-green" style={{ marginBottom: '0.6rem' }}>TEXT</span>
            <h4 style={{ fontWeight: 700, margin: '0.4rem 0' }}>Natural Language Processing</h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              TF-IDF sublinear n-gram vectorization, Logistic Regression, Linear SVM, Unicode text normalization.
            </p>
          </div>

          <div style={{ padding: '1.25rem', background: 'rgba(15, 23, 42, 0.5)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <span className="badge badge-yellow" style={{ marginBottom: '0.6rem' }}>TIME SERIES</span>
            <h4 style={{ fontWeight: 700, margin: '0.4rem 0' }}>Forecasting & Regressors</h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
              Strict chronological splitting (zero lookahead leakage), automated lag features, rolling statistics.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
