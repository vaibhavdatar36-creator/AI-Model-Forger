import React, { useState } from 'react';
import { CheckCircle2, AlertTriangle, ArrowRight, ArrowLeft, Cpu, Database, Eye, ShieldAlert, Sparkles } from 'lucide-react';
import { startTraining } from '../services/api';

export default function AnalysisView({ buildData, onStartTraining, onBack }) {
  const { analysis, datasetId, requirement, projectName, advancedSettings } = buildData;
  const [selectedTarget, setSelectedTarget] = useState(analysis.suggested_target || '');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleLaunch = async () => {
    setLoading(true);
    setError(null);
    try {
      const settings = {
        ...(advancedSettings || {}),
        target_column: selectedTarget || advancedSettings?.target_column
      };

      const jobResponse = await startTraining(
        datasetId,
        requirement,
        projectName,
        settings?.model_choice,
        settings
      );

      onStartTraining(jobResponse.job_id);
    } catch (err) {
      setError(err.message || 'Failed to start AutoML training job');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '950px' }}>
      <button className="nav-btn" onClick={onBack} style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
        <ArrowLeft size={16} /> Back to Edit
      </button>

      <div style={{ marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '0.4rem' }}>
          Dataset Understanding & Strategy
        </h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Review the automated analysis and architecture recommendations before training starts.
        </p>
      </div>

      {error && (
        <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.4)', borderRadius: '12px', padding: '1rem', color: '#fca5a5', marginBottom: '1.5rem' }}>
          {error}
        </div>
      )}

      {/* Unsupported Task Alert */}
      {!analysis.is_supported && (
        <div style={{
          background: 'rgba(245, 158, 11, 0.15)',
          border: '1px solid rgba(245, 158, 11, 0.4)',
          borderRadius: '16px',
          padding: '1.5rem',
          marginBottom: '2rem',
          display: 'flex',
          gap: '1rem',
          alignItems: 'flex-start'
        }}>
          <ShieldAlert size={28} className="text-yellow-400" />
          <div>
            <h4 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fde047', marginBottom: '0.4rem' }}>
              Unsupported Task Detected
            </h4>
            <p style={{ color: '#fef08a', fontSize: '0.95rem', lineHeight: 1.5 }}>
              {analysis.unsupported_message || 'The requested ML/DL task is not currently enabled in Version 1. AI Model Forge does not fake training results.'}
            </p>
            <div style={{ marginTop: '0.75rem', fontSize: '0.85rem', color: '#cbd5e1' }}>
              Architecture status: Ready for future trainer plugin.
            </div>
          </div>
        </div>
      )}

      {/* Confirmation Alert if Confidence is moderate or multiple targets */}
      {analysis.needs_user_confirmation && (
        <div style={{
          background: 'rgba(59, 130, 246, 0.12)',
          border: '1px solid rgba(59, 130, 246, 0.35)',
          borderRadius: '16px',
          padding: '1.5rem',
          marginBottom: '2rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.6rem' }}>
            <AlertTriangle size={20} className="text-blue-400" />
            <h4 style={{ fontWeight: 700, color: '#93c5fd' }}>Target Column Confirmation</h4>
          </div>
          <p style={{ color: '#bfdbfe', fontSize: '0.95rem', marginBottom: '1rem' }}>
            {analysis.confirmation_prompt}
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.6rem' }}>
            {analysis.candidate_targets.map((tgt) => (
              <button
                key={tgt}
                type="button"
                className={`btn ${selectedTarget === tgt ? 'btn-primary' : 'btn-secondary'}`}
                style={{ padding: '0.45rem 1rem', fontSize: '0.85rem' }}
                onClick={() => setSelectedTarget(tgt)}
              >
                {selectedTarget === tgt && <CheckCircle2 size={14} />}
                {tgt}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Detection Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem', marginBottom: '2rem' }}>
        <div className="card" style={{ marginBottom: 0, padding: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Detected Modality
            </span>
            <span className="badge badge-purple">
              {(analysis.modality_confidence * 100).toFixed(0)}% Confidence
            </span>
          </div>
          <div style={{ fontSize: '1.65rem', fontWeight: 800, color: '#fff', marginBottom: '0.5rem' }}>
            {analysis.detected_modality}
          </div>
          <ul style={{ paddingLeft: '1.2rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            {analysis.modality_reasons?.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>

        <div className="card" style={{ marginBottom: 0, padding: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              Detected Task
            </span>
            <span className="badge badge-green">
              {(analysis.task_confidence * 100).toFixed(0)}% Confidence
            </span>
          </div>
          <div style={{ fontSize: '1.65rem', fontWeight: 800, color: '#fff', marginBottom: '0.5rem' }}>
            {analysis.detected_task?.replace('_', ' ')}
          </div>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            {analysis.suggested_target ? `Target Variable: '${analysis.suggested_target}'` : 'Automatic task pipeline configured.'}
          </p>
        </div>
      </div>

      {/* Recommended Models Section */}
      {analysis.recommended_models && analysis.recommended_models.length > 0 && (
        <div className="card">
          <h3 className="card-title">
            <Cpu size={20} className="text-indigo-400" />
            Recommended Candidate Models
          </h3>
          <p className="card-subtitle">
            Ranked candidate architectures tailored to your dataset modality and hardware capability.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {analysis.recommended_models.map((rec, i) => (
              <div
                key={rec.model_name}
                style={{
                  padding: '1.25rem',
                  background: rec.is_recommended ? 'rgba(99, 102, 241, 0.12)' : 'rgba(15, 23, 42, 0.4)',
                  border: `1px solid ${rec.is_recommended ? 'rgba(99, 102, 241, 0.4)' : 'rgba(255, 255, 255, 0.08)'}`,
                  borderRadius: '12px'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                    <h4 style={{ fontWeight: 700, fontSize: '1.05rem' }}>{rec.display_name}</h4>
                    {rec.is_recommended && (
                      <span className="badge badge-blue">Champion Recommendation</span>
                    )}
                  </div>
                  <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                    Score: {(rec.suitability_score * 100).toFixed(0)}%
                  </span>
                </div>
                <div style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', marginBottom: '0.4rem' }}>
                  <strong>Why:</strong> {rec.reasons?.join(' ')}
                </div>
                {rec.tradeoffs && rec.tradeoffs.length > 0 && (
                  <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                    <strong>Tradeoffs:</strong> {rec.tradeoffs.join(' ')}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Footer */}
      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '2rem' }}>
        <button className="btn btn-secondary" onClick={onBack}>
          Adjust Settings
        </button>
        <button
          className="btn btn-primary btn-lg"
          onClick={handleLaunch}
          disabled={!analysis.is_supported || loading}
        >
          {loading ? (
            <>
              <Sparkles className="animate-spin" size={18} />
              Initializing AutoML Engine...
            </>
          ) : (
            <>
              CONFIRM & TRAIN MODEL
              <ArrowRight size={20} />
            </>
          )}
        </button>
      </div>
    </div>
  );
}
