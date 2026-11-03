import React, { useState, useEffect } from 'react';
import { History, Download, Play, Box, Sparkles, Layers } from 'lucide-react';
import { listModels } from '../services/api';

export default function HistoryView({ onNavigatePlayground }) {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const data = await listModels();
        setModels(data);
      } catch (e) {
        console.error('Failed to list models:', e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h2 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '0.4rem' }}>
            Model Vault & Training History
          </h2>
          <p style={{ color: 'var(--text-secondary)' }}>
            All production-ready <code>.aiforge</code> artifacts trained and verified on this platform.
          </p>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '4rem 1rem' }}>
          <Sparkles className="animate-spin text-indigo-400" size={32} style={{ margin: '0 auto 1rem auto' }} />
          <h3>Loading Vault...</h3>
        </div>
      ) : models.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '4rem 1rem' }}>
          <Box size={44} style={{ color: 'var(--text-muted)', margin: '0 auto 1rem auto', opacity: 0.5 }} />
          <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem' }}>No Models Trained Yet</h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Create your first model to download single-file artifacts and test them.
          </p>
        </div>
      ) : (
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <div style={{ overflowX: 'auto' }}>
            <table className="data-table" style={{ margin: 0 }}>
              <thead>
                <tr style={{ background: 'rgba(15, 23, 42, 0.7)' }}>
                  <th>Artifact Name</th>
                  <th>Modality</th>
                  <th>Task</th>
                  <th>Champion Architecture</th>
                  <th>Primary Metric</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {models.map((m) => (
                  <tr key={m.id}>
                    <td>
                      <div style={{ fontWeight: 700, color: '#fff' }}>{m.name}.aiforge</div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        {(m.file_size / 1024).toFixed(1)} KB
                      </div>
                    </td>
                    <td>
                      <span className="badge badge-purple">{m.modality}</span>
                    </td>
                    <td>
                      <span className="badge badge-blue">{m.task?.replace('_', ' ')}</span>
                    </td>
                    <td style={{ fontWeight: 600 }}>{m.model_type}</td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: '#10b981' }}>
                      {m.best_metric_name}: {m.best_metric_value.toFixed(4)}
                    </td>
                    <td style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                      {new Date(m.created_at).toLocaleDateString()}
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        <a
                          href={m.download_url}
                          className="btn btn-secondary"
                          style={{ padding: '0.4rem 0.75rem', fontSize: '0.82rem', textDecoration: 'none' }}
                          download={`${m.name}.aiforge`}
                        >
                          <Download size={14} /> Download
                        </a>
                        <button
                          className="btn btn-primary"
                          style={{ padding: '0.4rem 0.75rem', fontSize: '0.82rem' }}
                          onClick={() => onNavigatePlayground(m.id)}
                        >
                          <Play size={14} /> Test
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
