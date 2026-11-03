import React from 'react';
import { Layers, PlusCircle, History, Sparkles, Box } from 'lucide-react';

export default function Navbar({ currentView, setCurrentView }) {
  return (
    <nav className="navbar">
      <div className="nav-brand" onClick={() => setCurrentView('home')}>
        <Layers className="w-6 h-6 text-indigo-400" />
        <span>AI MODEL FORGE</span>
      </div>
      <div className="nav-links">
        <button
          className={`nav-btn ${currentView === 'home' ? 'active' : ''}`}
          onClick={() => setCurrentView('home')}
        >
          Overview
        </button>
        <button
          className={`nav-btn ${currentView === 'create' ? 'active' : ''}`}
          onClick={() => setCurrentView('create')}
        >
          <PlusCircle size={18} />
          Create Model
        </button>
        <button
          className={`nav-btn ${currentView === 'history' ? 'active' : ''}`}
          onClick={() => setCurrentView('history')}
        >
          <History size={18} />
          Model Vault
        </button>
        <button
          className="nav-btn primary-cta"
          onClick={() => setCurrentView('create')}
        >
          <Sparkles size={16} />
          Build AI Model
        </button>
      </div>
    </nav>
  );
}
