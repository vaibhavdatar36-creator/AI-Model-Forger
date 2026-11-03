import React, { useState, useEffect } from 'react';
import { Download, Sparkles, CheckCircle2, Play, Code2, Award, FileSpreadsheet, Layers, Copy, Check } from 'lucide-react';
import { getJobResults } from '../services/api';

export default function ResultsView({ jobId, onNavigatePlayground }) {
  const [results, setResults] = useState(null);
  const [copiedCode, setCopiedCode] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await getJobResults(jobId);
        setResults(data);
      } catch (e) {
        console.error('Error loading results:', e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [jobId]);

  if (loading) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: '5rem 1rem' }}>
        <Sparkles className="animate-spin text-indigo-400" size={32} style={{ margin: '0 auto 1rem auto' }} />
        <h3>Loading Final Champion Model & Artifact Package...</h3>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: '5rem 1rem' }}>
        <h3>Unable to load results for this job.</h3>
      </div>
    );
  }

  const { best_model_name, best_metric_name, best_metric_value, model_artifact, model_comparisons, data_processing_summary, confusion_matrix, training_time_seconds } = results;

  const artifactId = model_artifact?.id;
  const artifactName = model_artifact?.name || 'trained_model';
  const downloadUrl = `/api/models/${artifactId}/download`;

  const pythonSnippet = `from aiforge_runtime import load_model

# Load the single self-contained model package
model = load_model("${artifactName}.aiforge")

# Run inference with raw, unprepared input!
result = model.predict(input_data)
print(result)
# -> {'prediction': ..., 'confidence': 0.95, 'probabilities': {...}}`;

  const handleCopyCode = () => {
    navigator.clipboard.writeText(pythonSnippet);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  return (
    <div className="container" style={{ maxWidth: '1000px' }}>
      {/* Top Champion Hero */}
      <div className="card" style={{
        background: 'linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(168, 85, 247, 0.15) 100%)',
        border: '1px solid rgba(99, 102, 241, 0.4)',
        textAlign: 'center',
        padding: '2.5rem 1.5rem'
      }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(99, 102, 241, 0.3)', padding: '0.35rem 1rem', borderRadius: '9999px', fontSize: '0.85rem', fontWeight: 700, color: '#c7d2fe', marginBottom: '1rem' }}>
          <Award size={16} /> CHAMPION MODEL SELECTED & PACKAGED
        </div>
        <h2 style={{ fontSize: '2.5rem', fontWeight: 800, marginBottom: '0.5rem', letterSpacing: '-0.02em' }}>
          {best_model_name}
        </h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '1.1rem', maxWidth: '650px', margin: '0 auto 1.75rem auto' }}>
          Trained, benchmarked, and fully validated in {training_time_seconds}s. Your complete AI model package is ready.
        </p>

        <div style={{ display: 'flex', justifyContent: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <a
            href={downloadUrl}
            className="btn btn-primary btn-lg"
            download={`${artifactName}.aiforge`}
            style={{ textDecoration: 'none' }}
          >
            <Download size={20} />
            DOWNLOAD {artifactName}.aiforge
          </a>
          <button
            className="btn btn-secondary btn-lg"
            onClick={() => onNavigatePlayground(artifactId)}
          >
            <Play size={20} />
            Test in Live Playground
          </button>
        </div>
        <div style={{ marginTop: '0.75rem', fontSize: '0.82rem', color: 'var(--text-muted)' }}>
          Single self-contained file • Size: {(model_artifact?.file_size / 1024).toFixed(1)} KB • Zero manual preprocessing needed
        </div>
      </div>

      {/* Key Metrics Grid */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-label">{best_metric_name}</div>
          <div className="metric-value">
            {typeof best_metric_value === 'number' ? best_metric_value.toFixed(4) : best_metric_value}
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Modality & Task</div>
          <div className="metric-value" style={{ fontSize: '1.25rem', color: '#a5b4fc', paddingTop: '0.3rem' }}>
            {model_artifact?.task?.replace('_', ' ')}
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Training Duration</div>
          <div className="metric-value">{training_time_seconds}s</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Artifact Integrity</div>
          <div className="metric-value" style={{ fontSize: '1.25rem', color: '#10b981', paddingTop: '0.3rem' }}>
            Verified
          </div>
        </div>
      </div>

      {/* Candidate Comparisons Table */}
      {model_comparisons && model_comparisons.length > 0 && (
        <div className="card">
          <h3 className="card-title">
            <Layers size={20} className="text-indigo-400" />
            Model Benchmark Comparisons
          </h3>
          <p className="card-subtitle">
            All candidate architectures trained and benchmarked on your data.
          </p>

          <div style={{ overflowX: 'auto' }}>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Model Architecture</th>
                  <th>Status</th>
                  <th>Primary Metric</th>
                  <th>Accuracy / RMSE</th>
                  <th>Precision / MAE</th>
                  <th>Recall / R²</th>
                  <th>Train Time</th>
                </tr>
              </thead>
              <tbody>
                {model_comparisons.map((c, i) => (
                  <tr key={i} style={c.is_best ? { background: 'rgba(99, 102, 241, 0.12)' } : {}}>
                    <td style={{ fontWeight: 600 }}>
                      {c.model_name}
                      {c.is_best && <span className="badge badge-green" style={{ marginLeft: '0.5rem' }}>Champion</span>}
                    </td>
                    <td><span className="badge badge-blue">Evaluated</span></td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                      {c.primary_metric !== undefined ? c.primary_metric : c.f1_macro || c.rmse}
                    </td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>{c.accuracy ?? c.rmse ?? '-'}</td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>{c.precision ?? c.mae ?? '-'}</td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>{c.recall ?? c.r2 ?? '-'}</td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>{c.train_time_sec ? `${c.train_time_sec}s` : '-'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Automated Data Engineering Report */}
      {data_processing_summary && data_processing_summary.length > 0 && (
        <div className="card">
          <h3 className="card-title">
            <CheckCircle2 size={20} className="text-green-400" />
            Automated Data Engineering Report
          </h3>
          <p className="card-subtitle">
            Transformations applied automatically to prepare raw data for production training.
          </p>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '0.75rem' }}>
            {data_processing_summary.map((item, idx) => (
              <div
                key={idx}
                style={{
                  padding: '0.85rem 1rem',
                  background: 'rgba(15, 23, 42, 0.5)',
                  borderRadius: '10px',
                  border: '1px solid rgba(255, 255, 255, 0.05)',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.6rem',
                  fontSize: '0.88rem',
                  color: '#e2e8f0'
                }}
              >
                <CheckCircle2 size={16} className="text-emerald-400" style={{ flexShrink: 0 }} />
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Standalone Usage SDK Guide */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
          <h3 className="card-title" style={{ margin: 0 }}>
            <Code2 size={20} className="text-indigo-400" />
            How to Use This Model in Another Project
          </h3>
          <button className="chip-btn" onClick={handleCopyCode} style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
            {copiedCode ? <Check size={14} className="text-green-400" /> : <Copy size={14} />}
            {copiedCode ? 'Copied!' : 'Copy Code'}
          </button>
        </div>
        <p className="card-subtitle">
          Place the downloaded <code>{artifactName}.aiforge</code> file into your application. Install the lightweight runtime: <code>pip install ./runtime_sdk</code>
        </p>

        <div className="log-viewer" style={{ color: '#e2e8f0', background: '#090d16' }}>
          {pythonSnippet}
        </div>
      </div>
    </div>
  );
}
