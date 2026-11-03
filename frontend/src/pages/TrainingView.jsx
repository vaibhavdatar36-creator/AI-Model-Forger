import React, { useState, useEffect, useRef } from 'react';
import { Cpu, Terminal, CheckCircle2, AlertCircle, Sparkles, Box } from 'lucide-react';
import { getJobStatus, getJobResults } from '../services/api';

const STEPS = [
  { key: 'ANALYZING', label: 'Dataset Understanding' },
  { key: 'PREPROCESSING', label: 'Data Cleaning & Engineering' },
  { key: 'TRAINING', label: 'Model Benchmarking' },
  { key: 'EVALUATING', label: 'Metric Evaluation' },
  { key: 'PACKAGING', label: 'Packaging .aiforge' }
];

export default function TrainingView({ jobId, onTrainingComplete }) {
  const [jobStatus, setJobStatus] = useState(null);
  const [showLogs, setShowLogs] = useState(false);
  const [logs, setLogs] = useState('');
  const [error, setError] = useState(null);
  const terminalRef = useRef(null);

  useEffect(() => {
    let intervalId;

    const poll = async () => {
      try {
        const status = await getJobStatus(jobId);
        setJobStatus(status);

        // Fetch logs if running or completed
        try {
          const results = await getJobResults(jobId);
          if (results && results.logs) {
            setLogs(results.logs);
          }
        } catch (_) {}

        if (status.status === 'COMPLETED') {
          clearInterval(intervalId);
          setTimeout(() => {
            onTrainingComplete(jobId);
          }, 1200);
        } else if (status.status === 'FAILED') {
          clearInterval(intervalId);
          setError(status.error_message || 'Training failed.');
        }
      } catch (err) {
        console.error('Polling error:', err);
      }
    };

    poll();
    intervalId = setInterval(poll, 1500);

    return () => clearInterval(intervalId);
  }, [jobId, onTrainingComplete]);

  const progress = jobStatus?.progress || 10;
  const currentStep = jobStatus?.current_step || 'Initializing training environment...';

  return (
    <div className="container" style={{ maxWidth: '850px' }}>
      <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
        <h2 style={{ fontSize: '2.25rem', fontWeight: 800, marginBottom: '0.4rem' }}>
          AutoML Forge Engine Active
        </h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Automating data engineering, candidate training, evaluation, and single-file packaging.
        </p>
      </div>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <Cpu className="text-indigo-400 animate-pulse" size={24} />
            <div>
              <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>
                Job ID: <span style={{ fontFamily: 'var(--font-mono)', color: '#a5b4fc' }}>{jobId.slice(0, 13)}</span>
              </div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                Status: <span style={{ color: '#38bdf8', fontWeight: 600 }}>{jobStatus?.status || 'RUNNING'}</span>
              </div>
            </div>
          </div>
          <div style={{ fontSize: '1.75rem', fontWeight: 800, fontFamily: 'var(--font-mono)', color: '#fff' }}>
            {progress}%
          </div>
        </div>

        {/* Progress Bar */}
        <div className="progress-bar-container">
          <div className="progress-bar-fill" style={{ width: `${progress}%` }} />
        </div>

        {/* Current Step Description */}
        <div style={{
          padding: '1rem 1.25rem',
          background: 'rgba(15, 23, 42, 0.6)',
          borderRadius: '12px',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
          marginBottom: '2rem'
        }}>
          <Sparkles className="text-indigo-400 animate-spin" size={20} />
          <span style={{ fontSize: '0.95rem', color: '#e2e8f0', fontWeight: 500 }}>
            {currentStep}
          </span>
        </div>

        {/* Step progression indicators */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(130px, 1fr))',
          gap: '0.75rem',
          marginBottom: '2rem'
        }}>
          {STEPS.map((s, idx) => {
            const isDone = progress >= ((idx + 1) * 20);
            const isCurrent = !isDone && progress >= (idx * 20);
            return (
              <div
                key={s.key}
                style={{
                  padding: '0.85rem 0.75rem',
                  borderRadius: '10px',
                  background: isDone ? 'rgba(16, 185, 129, 0.1)' : isCurrent ? 'rgba(99, 102, 241, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                  border: `1px solid ${isDone ? 'rgba(16, 185, 129, 0.3)' : isCurrent ? 'var(--accent-primary)' : 'rgba(255, 255, 255, 0.05)'}`,
                  textAlign: 'center'
                }}
              >
                <div style={{ fontSize: '0.75rem', color: isDone ? '#6ee7b7' : isCurrent ? '#a5b4fc' : 'var(--text-muted)', fontWeight: 600 }}>
                  STEP 0{idx + 1}
                </div>
                <div style={{ fontSize: '0.82rem', fontWeight: 600, color: '#f8fafc', marginTop: '0.2rem' }}>
                  {s.label}
                </div>
              </div>
            );
          })}
        </div>

        {/* Collapsible Technical Logs */}
        <div style={{ borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '1.25rem' }}>
          <button
            type="button"
            className="nav-btn"
            style={{ padding: '0.4rem 0', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
            onClick={() => setShowLogs(!showLogs)}
          >
            <Terminal size={16} />
            {showLogs ? 'Hide Technical Engine Logs' : 'Show Technical Engine Logs'}
          </button>

          {showLogs && (
            <div ref={terminalRef} className="log-viewer" style={{ marginTop: '1rem' }}>
              {logs || 'Connecting to training job console output...'}
            </div>
          )}
        </div>
      </div>

      {error && (
        <div style={{
          background: 'rgba(239, 68, 68, 0.15)',
          border: '1px solid rgba(239, 68, 68, 0.4)',
          borderRadius: '14px',
          padding: '1.5rem',
          color: '#fca5a5',
          marginTop: '1.5rem',
          display: 'flex',
          gap: '1rem',
          alignItems: 'center'
        }}>
          <AlertCircle size={28} />
          <div>
            <h4 style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: '0.25rem' }}>AutoML Training Stopped</h4>
            <p style={{ fontSize: '0.9rem' }}>{error}</p>
          </div>
        </div>
      )}
    </div>
  );
}
