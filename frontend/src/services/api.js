const API_BASE = '/api';

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error('Backend health check failed');
  return res.json();
}

export async function uploadDataset(file, onProgress) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(err.detail || 'Upload failed');
  }

  return res.json();
}

export async function analyzeDataset(datasetId, requirement, options = {}) {
  const payload = {
    dataset_id: datasetId,
    requirement,
    target_column: options.target_column || null,
    override_modality: options.override_modality || null,
    override_task: options.override_task || null
  };

  const res = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Analysis failed' }));
    throw new Error(err.detail || 'Analysis failed');
  }

  return res.json();
}

export async function startTraining(datasetId, requirement, projectName, selectedModel, advancedSettings) {
  const payload = {
    dataset_id: datasetId,
    requirement,
    project_name: projectName || 'AI Model Forge Project',
    selected_model: selectedModel || null,
    advanced_settings: advancedSettings || null
  };

  const res = await fetch(`${API_BASE}/train`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Failed to start training' }));
    throw new Error(err.detail || 'Failed to start training');
  }

  return res.json();
}

export async function getJobStatus(jobId) {
  const res = await fetch(`${API_BASE}/jobs/${jobId}`);
  if (!res.ok) throw new Error('Failed to fetch job status');
  return res.json();
}

export async function getJobResults(jobId) {
  const res = await fetch(`${API_BASE}/results/${jobId}`);
  if (!res.ok) throw new Error('Failed to fetch job results');
  return res.json();
}

export async function listModels() {
  const res = await fetch(`${API_BASE}/models`);
  if (!res.ok) throw new Error('Failed to fetch models list');
  return res.json();
}

export async function getModelDetails(modelId) {
  const res = await fetch(`${API_BASE}/models/${modelId}`);
  if (!res.ok) throw new Error('Failed to fetch model details');
  return res.json();
}

export async function runPrediction(modelId, inputData) {
  const res = await fetch(`${API_BASE}/models/${modelId}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ input_data: inputData }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Prediction request failed' }));
    throw new Error(err.detail || 'Prediction request failed');
  }

  return res.json();
}

export async function runFilePrediction(modelId, file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/models/${modelId}/predict_file`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) throw new Error('File prediction failed');
  return res.json();
}
