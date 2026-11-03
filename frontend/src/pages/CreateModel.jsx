import React, { useState, useRef } from 'react';
import { Upload, FileCode, Sliders, Sparkles, CheckCircle2, AlertCircle, ArrowRight } from 'lucide-react';
import { uploadDataset, analyzeDataset } from '../services/api';

const SAMPLE_REQUIREMENTS = [
  "Predict customer churn from demographic and account features.",
  "Predict house prices based on characteristics and location.",
  "Classify customer reviews as positive or negative sentiment.",
  "Classify images of cats and dogs from folder data.",
  "Forecast tomorrow's electricity demand based on historical readings."
];

export default function CreateModel({ onAnalysisComplete }) {
  const [projectName, setProjectName] = useState('Customer Churn Predictor');
  const [requirement, setRequirement] = useState(SAMPLE_REQUIREMENTS[0]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Advanced settings
  const [targetColumn, setTargetColumn] = useState('');
  const [taskOverride, setTaskOverride] = useState('');
  const [modalityOverride, setModalityOverride] = useState('');
  const [modelChoice, setModelChoice] = useState('auto');
  const [testSize, setTestSize] = useState(0.2);

  const fileInputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setSelectedFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!requirement.trim()) {
      setError('Please provide a natural language requirement.');
      return;
    }
    if (!selectedFile) {
      setError('Please upload a dataset file (.csv, .xlsx, .parquet, .json, or .zip).');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 1. Upload dataset
      const uploadRes = await uploadDataset(selectedFile);
      const datasetId = uploadRes.dataset_id;

      // 2. Analyze dataset & requirement
      const analyzeRes = await analyzeDataset(datasetId, requirement, {
        target_column: targetColumn || undefined,
        override_modality: modalityOverride || undefined,
        override_task: taskOverride || undefined
      });

      onAnalysisComplete({
        datasetId,
        fileName: selectedFile.name,
        fileSize: selectedFile.size,
        projectName,
        requirement,
        analysis: analyzeRes,
        advancedSettings: showAdvanced ? {
          target_column: targetColumn || undefined,
          task: taskOverride || undefined,
          modality: modalityOverride || undefined,
          model_choice: modelChoice !== 'auto' ? modelChoice : undefined,
          test_size: parseFloat(testSize)
        } : null
      });
    } catch (err) {
      setError(err.message || 'An error occurred during dataset upload and analysis.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '850px' }}>
      <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
        <h2 style={{ fontSize: '2.25rem', fontWeight: 800, marginBottom: '0.5rem' }}>
          Build an AI Model
        </h2>
        <p style={{ color: 'var(--text-secondary)' }}>
          Tell us what you want to achieve and provide your dataset. We handle the rest.
        </p>
      </div>

      {error && (
        <div style={{
          background: 'rgba(239, 68, 68, 0.15)',
          border: '1px solid rgba(239, 68, 68, 0.4)',
          borderRadius: '12px',
          padding: '1rem',
          color: '#fca5a5',
          marginBottom: '1.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem'
        }}>
          <AlertCircle size={20} />
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleAnalyze}>
        <div className="card">
          <div className="form-group">
            <label className="form-label">Project Name</label>
            <input
              type="text"
              className="form-input"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              placeholder="e.g. Customer Churn Predictor"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">
              What do you want this AI model to do?
            </label>
            <textarea
              className="form-textarea"
              value={requirement}
              onChange={(e) => setRequirement(e.target.value)}
              placeholder="e.g. I want to predict whether a customer will churn based on their account and usage history..."
              required
            />
            <div style={{ marginTop: '0.75rem' }}>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Quick Examples:</span>
              <div className="chips-container">
                {SAMPLE_REQUIREMENTS.map((sample, idx) => (
                  <button
                    key={idx}
                    type="button"
                    className="chip-btn"
                    onClick={() => setRequirement(sample)}
                  >
                    {sample.slice(0, 48)}...
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Upload Raw Dataset</label>
            <div
              className={`dropzone ${isDragging ? 'active' : ''}`}
              onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
              onDragLeave={() => setIsDragging(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload className="dropzone-icon" style={{ margin: '0 auto 0.75rem auto' }} />
              <div className="dropzone-title">
                {selectedFile ? selectedFile.name : 'Drag and drop your dataset here, or click to browse'}
              </div>
              <div className="dropzone-hint">
                {selectedFile 
                  ? `${(selectedFile.size / (1024 * 1024)).toFixed(2)} MB • Ready for analysis`
                  : 'Supported formats: CSV, Excel, Parquet, JSON, Images, Audio, ZIP archives (up to 500MB)'}
              </div>
              <input
                ref={fileInputRef}
                type="file"
                style={{ display: 'none' }}
                onChange={handleFileChange}
                accept=".csv,.xlsx,.xls,.parquet,.json,.zip,.jpg,.jpeg,.png,.txt"
              />
            </div>
          </div>

          {/* Collapsible Advanced Settings */}
          <div style={{ marginTop: '1.5rem', borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '1.25rem' }}>
            <button
              type="button"
              className="nav-btn"
              style={{ padding: '0.4rem 0', color: '#818cf8', display: 'flex', alignItems: 'center', gap: '0.5rem' }}
              onClick={() => setShowAdvanced(!showAdvanced)}
            >
              <Sliders size={16} />
              {showAdvanced ? 'Hide Advanced Settings' : 'Show Advanced Settings (Optional)'}
            </button>

            {showAdvanced && (
              <div style={{
                marginTop: '1rem',
                padding: '1.25rem',
                background: 'rgba(10, 13, 20, 0.6)',
                borderRadius: '12px',
                border: '1px solid var(--border-color)',
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '1rem'
              }}>
                <div>
                  <label className="form-label" style={{ fontSize: '0.85rem' }}>Target Column Override</label>
                  <input
                    type="text"
                    className="form-input"
                    value={targetColumn}
                    onChange={(e) => setTargetColumn(e.target.value)}
                    placeholder="Auto-detect if blank"
                  />
                </div>

                <div>
                  <label className="form-label" style={{ fontSize: '0.85rem' }}>Task Override</label>
                  <select
                    className="form-select"
                    value={taskOverride}
                    onChange={(e) => setTaskOverride(e.target.value)}
                  >
                    <option value="">Auto-Detect Task</option>
                    <option value="TABULAR_CLASSIFICATION">Tabular Classification</option>
                    <option value="TABULAR_REGRESSION">Tabular Regression</option>
                    <option value="IMAGE_CLASSIFICATION">Image Classification</option>
                    <option value="TEXT_CLASSIFICATION">Text Classification</option>
                    <option value="TIME_SERIES_FORECASTING">Time Series Forecasting</option>
                  </select>
                </div>

                <div>
                  <label className="form-label" style={{ fontSize: '0.85rem' }}>Model Choice</label>
                  <select
                    className="form-select"
                    value={modelChoice}
                    onChange={(e) => setModelChoice(e.target.value)}
                  >
                    <option value="auto">Auto Champion Selection</option>
                    <option value="random_forest">Random Forest</option>
                    <option value="gradient_boosting">Gradient Boosting</option>
                    <option value="logistic_regression">Linear / Logistic</option>
                    <option value="mobilenet_v2">MobileNetV2 (Vision)</option>
                  </select>
                </div>

                <div>
                  <label className="form-label" style={{ fontSize: '0.85rem' }}>Test Split Ratio</label>
                  <select
                    className="form-select"
                    value={testSize}
                    onChange={(e) => setTestSize(e.target.value)}
                  >
                    <option value={0.15}>15% Test Split</option>
                    <option value={0.2}>20% Test Split (Standard)</option>
                    <option value={0.3}>30% Test Split</option>
                  </select>
                </div>
              </div>
            )}
          </div>

          <div style={{ marginTop: '2.5rem', textAlign: 'right' }}>
            <button
              type="submit"
              className="btn btn-primary btn-lg"
              disabled={loading}
              style={{ width: '100%' }}
            >
              {loading ? (
                <>
                  <Sparkles className="animate-spin" size={20} />
                  Analyzing Dataset & Preparing Pipeline...
                </>
              ) : (
                <>
                  ANALYZE & BUILD MODEL
                  <ArrowRight size={20} />
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
