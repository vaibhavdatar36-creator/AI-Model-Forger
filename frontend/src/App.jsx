import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import CreateModel from './pages/CreateModel';
import AnalysisView from './pages/AnalysisView';
import TrainingView from './pages/TrainingView';
import ResultsView from './pages/ResultsView';
import PlaygroundView from './pages/PlaygroundView';
import HistoryView from './pages/HistoryView';
import './App.css';

export default function App() {
  const [currentView, setCurrentView] = useState('home');
  const [buildData, setBuildData] = useState(null);
  const [activeJobId, setActiveJobId] = useState(null);
  const [activeModelId, setActiveModelId] = useState(null);

  // Workflow Handlers
  const handleAnalysisComplete = (data) => {
    setBuildData(data);
    setCurrentView('analysis');
  };

  const handleStartTraining = (jobId) => {
    setActiveJobId(jobId);
    setCurrentView('training');
  };

  const handleTrainingComplete = (jobId) => {
    setActiveJobId(jobId);
    setCurrentView('results');
  };

  const handleNavigatePlayground = (modelId) => {
    setActiveModelId(modelId);
    setCurrentView('playground');
  };

  return (
    <div className="app-layout">
      <Navbar currentView={currentView} setCurrentView={setCurrentView} />

      <main>
        {currentView === 'home' && (
          <Home onStartCreate={() => setCurrentView('create')} />
        )}

        {currentView === 'create' && (
          <CreateModel onAnalysisComplete={handleAnalysisComplete} />
        )}

        {currentView === 'analysis' && buildData && (
          <AnalysisView
            buildData={buildData}
            onStartTraining={handleStartTraining}
            onBack={() => setCurrentView('create')}
          />
        )}

        {currentView === 'training' && activeJobId && (
          <TrainingView
            jobId={activeJobId}
            onTrainingComplete={handleTrainingComplete}
          />
        )}

        {currentView === 'results' && activeJobId && (
          <ResultsView
            jobId={activeJobId}
            onNavigatePlayground={handleNavigatePlayground}
          />
        )}

        {currentView === 'playground' && activeModelId && (
          <PlaygroundView
            modelId={activeModelId}
            onBack={() => setCurrentView('results')}
          />
        )}

        {currentView === 'history' && (
          <HistoryView onNavigatePlayground={handleNavigatePlayground} />
        )}
      </main>
    </div>
  );
}
