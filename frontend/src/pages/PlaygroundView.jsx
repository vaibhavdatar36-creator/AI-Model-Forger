import React, { useState, useEffect } from 'react';
import { Play, Sparkles, AlertCircle, ArrowLeft, Image as ImageIcon, Send, RefreshCw } from 'lucide-react';
import { getModelDetails, runPrediction, runFilePrediction } from '../services/api';

export default function PlaygroundView({ modelId, onBack }) {
  const [modelDetails, setModelDetails] = useState(null);
  const [loadingModel, setLoadingModel] = useState(true);
  
  // Inputs
  const [tabularInputs, setTabularInputs] = useState({});
  const [textInput, setTextInput] = useState('');
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  // Prediction result
  const [predicting, setPredicting] = useState(false);
  const [predictionResult, setPredictionResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const details = await getModelDetails(modelId);
        setModelDetails(details);

        // Pre-fill default sample input for tabular if schema has features
        if (details.schema && details.schema.features) {
          const initial = {};
          for (const [key, feat] of Object.entries(details.schema.features)) {
            if (feat.sample_values && feat.sample_values.length > 0) {
              initial[key] = feat.type === 'integer' || feat.type === 'float'
                ? parseFloat(feat.sample_values[0]) || 0
                : feat.sample_values[0];
            } else {
              initial[key] = feat.type === 'integer' || feat.type === 'float' ? 0 : '';
            }
          }
          setTabularInputs(initial);
        } else if (details.modality === 'TEXT') {
          setTextInput('The product is absolutely amazing with exceptional performance!');
        }
      } catch (err) {
        setError(err.message || 'Failed to load model details.');
      } finally {
        setLoadingModel(false);
      }
    }
    load();
  }, [modelId]);

  const handlePredict = async (e) => {
    e.preventDefault();
    setPredicting(true);
    setError(null);
    setPredictionResult(null);

    try {
      if (modelDetails.modality === 'IMAGE') {
        if (!imageFile) throw new Error('Please select an image file to predict.');
        const res = await runFilePrediction(modelId, imageFile);
        if (!res.success) throw new Error(res.error || 'Prediction failed');
        setPredictionResult(res);
      } else if (modelDetails.modality === 'TEXT') {
        if (!textInput.trim()) throw new Error('Please enter text to classify.');
        const res = await runPrediction(modelId, textInput);
        if (!res.success) throw new Error(res.error || 'Prediction failed');
        setPredictionResult(res);
      } else {
        // Tabular / Time-series
        const res = await runPrediction(modelId, tabularInputs);
        if (!res.success) throw new Error(res.error || 'Prediction failed');
        setPredictionResult(res);
      }
    } catch (err) {
      setError(err.message || 'Inference error.');
    } finally {
      setPredicting(false);
    }
  };

  const handleImageChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setImageFile(file);
      setImagePreview(URL.createObjectURL(file));
    }
  };

  if (loadingModel) {
    return (
      <div className="container" style={{ textAlign: 'center', padding: '5rem 1rem' }}>
        <Sparkles className="animate-spin text-indigo-400" size={32} style={{ margin: '0 auto 1rem auto' }} />
        <h3>Loading Model Runtime Playground...</h3>
      </div>
    );
  }

  const modality = modelDetails?.modality || 'TABULAR';
  const schema = modelDetails?.schema || {};

  return (
    <div className="container" style={{ maxWidth: '950px' }}>
      <button className="nav-btn" onClick={onBack} style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
        <ArrowLeft size={16} /> Back to Model Details
      </button>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h2 style={{ fontSize: '2rem', fontWeight: 800, marginBottom: '0.3rem' }}>
            Interactive Prediction Playground
          </h2>
          <p style={{ color: 'var(--text-secondary)' }}>
            Model: <strong style={{ color: '#fff' }}>{modelDetails?.name}</strong> • Architecture: {modelDetails?.model_type}
          </p>
        </div>
        <span className="badge badge-purple" style={{ fontSize: '0.85rem' }}>
          {modelDetails?.task}
        </span>
      </div>

      {error && (
        <div style={{ background: 'rgba(239, 68, 68, 0.15)', border: '1px solid rgba(239, 68, 68, 0.4)', borderRadius: '12px', padding: '1rem', color: '#fca5a5', marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '2rem' }}>
        {/* Left: Input Form */}
        <div className="card" style={{ marginBottom: 0 }}>
          <h3 className="card-title" style={{ fontSize: '1.15rem', marginBottom: '1.25rem' }}>
            Input Raw Inference Data
          </h3>

          <form onSubmit={handlePredict}>
            {/* Tabular Form */}
            {modality === 'TABULAR' && schema.features && (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {Object.entries(schema.features).map(([featName, featInfo]) => (
                  <div key={featName}>
                    <label className="form-label" style={{ fontSize: '0.85rem' }}>
                      {featName} <span style={{ color: 'var(--text-muted)' }}>({featInfo.type})</span>
                    </label>
                    {featInfo.categories ? (
                      <select
                        className="form-select"
                        value={tabularInputs[featName] ?? ''}
                        onChange={(e) => setTabularInputs({ ...tabularInputs, [featName]: e.target.value })}
                      >
                        {featInfo.categories.map((cat) => (
                          <option key={cat} value={cat}>{cat}</option>
                        ))}
                      </select>
                    ) : (
                      <input
                        type={featInfo.type === 'integer' || featInfo.type === 'float' ? 'number' : 'text'}
                        step="any"
                        className="form-input"
                        value={tabularInputs[featName] ?? ''}
                        onChange={(e) => setTabularInputs({
                          ...tabularInputs,
                          [featName]: featInfo.type === 'integer' || featInfo.type === 'float' ? parseFloat(e.target.value) || 0 : e.target.value
                        })}
                      />
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Text Input */}
            {modality === 'TEXT' && (
              <div className="form-group">
                <label className="form-label">Input Text to Classify</label>
                <textarea
                  className="form-textarea"
                  value={textInput}
                  onChange={(e) => setTextInput(e.target.value)}
                  placeholder="Type or paste any sentence or paragraph..."
                  rows={5}
                  required
                />
              </div>
            )}

            {/* Image Input */}
            {modality === 'IMAGE' && (
              <div className="form-group">
                <label className="form-label">Upload Image</label>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  style={{ marginBottom: '1rem' }}
                />
                {imagePreview && (
                  <div style={{ textAlign: 'center', background: 'rgba(0,0,0,0.4)', padding: '1rem', borderRadius: '12px' }}>
                    <img
                      src={imagePreview}
                      alt="Preview"
                      style={{ maxWidth: '100%', maxHeight: '200px', borderRadius: '8px', objectFit: 'contain' }}
                    />
                  </div>
                )}
              </div>
            )}

            <button
              type="submit"
              className="btn btn-primary"
              style={{ width: '100%', marginTop: '1.5rem' }}
              disabled={predicting}
            >
              {predicting ? (
                <>
                  <RefreshCw className="animate-spin" size={18} />
                  Running Inference...
                </>
              ) : (
                <>
                  <Play size={18} />
                  Run Prediction
                </>
              )}
            </button>
          </form>
        </div>

        {/* Right: Prediction Output */}
        <div className="card" style={{ marginBottom: 0, display: 'flex', flexDirection: 'column' }}>
          <h3 className="card-title" style={{ fontSize: '1.15rem', marginBottom: '1.25rem' }}>
            Model Inference Output
          </h3>

          {predictionResult ? (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
              <div style={{
                background: 'rgba(99, 102, 241, 0.1)',
                border: '1px solid rgba(99, 102, 241, 0.3)',
                borderRadius: '16px',
                padding: '1.75rem',
                textAlign: 'center',
                marginBottom: '1.5rem'
              }}>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.4rem' }}>
                  Predicted Outcome
                </div>
                <div style={{ fontSize: '2.5rem', fontWeight: 800, color: '#fff', letterSpacing: '-0.02em' }}>
                  {typeof predictionResult.prediction === 'number'
                    ? predictionResult.prediction.toLocaleString(undefined, { maximumFractionDigits: 2 })
                    : String(predictionResult.prediction)}
                </div>

                {predictionResult.confidence !== undefined && predictionResult.confidence !== null && (
                  <div style={{ marginTop: '0.5rem' }}>
                    <span className="badge badge-green" style={{ fontSize: '0.9rem', padding: '0.35rem 0.85rem' }}>
                      {(predictionResult.confidence * 100).toFixed(1)}% Confidence
                    </span>
                  </div>
                )}
              </div>

              {/* Class Probability Distribution */}
              {predictionResult.probabilities && (
                <div style={{ marginBottom: '1.5rem' }}>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
                    Class Probabilities Breakdown
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
                    {Object.entries(predictionResult.probabilities).map(([className, prob]) => (
                      <div key={className}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.2rem' }}>
                          <span style={{ fontWeight: 500 }}>{className}</span>
                          <span style={{ fontFamily: 'var(--font-mono)', color: '#a5b4fc' }}>{(prob * 100).toFixed(1)}%</span>
                        </div>
                        <div style={{ height: '6px', background: 'rgba(255,255,255,0.08)', borderRadius: '9999px', overflow: 'hidden' }}>
                          <div style={{ width: `${prob * 100}%`, height: '100%', background: 'var(--accent-gradient)' }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div style={{ marginTop: 'auto', borderTop: '1px solid rgba(255,255,255,0.06)', paddingTop: '0.75rem', fontSize: '0.82rem', color: 'var(--text-muted)', display: 'flex', justifyContent: 'space-between' }}>
                <span>Inference Latency</span>
                <span style={{ fontFamily: 'var(--font-mono)' }}>{predictionResult.inference_time_ms} ms</span>
              </div>
            </div>
          ) : (
            <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', textAlign: 'center', color: 'var(--text-muted)' }}>
              <Play size={40} style={{ opacity: 0.3, marginBottom: '1rem' }} />
              <p style={{ fontSize: '0.95rem' }}>
                Configure inputs on the left and click "Run Prediction" to execute the model runtime.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
