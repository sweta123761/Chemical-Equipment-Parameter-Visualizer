import React, { useState, useEffect } from 'react';
import './App.css';
import UploadComponent from './components/UploadComponent';
import Dashboard from './components/Dashboard';
import DataTable from './components/DataTable';
import HistoryPanel from './components/HistoryPanel';

function App() {
  const [currentData, setCurrentData] = useState(null);
  const [history, setHistory] = useState([]);
  const [activeTab, setActiveTab] = useState('upload');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/history/');
      if (response.ok) {
        const data = await response.json();
        setHistory(data);
      }
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const handleUploadSuccess = (data) => {
    setCurrentData(data);
    setActiveTab('dashboard');
    fetchHistory();
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Chemical Equipment Parameter Visualizer</h1>
      </header>
      <nav className="App-nav">
        <button 
          className={activeTab === 'upload' ? 'active' : ''} 
          onClick={() => setActiveTab('upload')}
        >
          Upload
        </button>
        <button 
          className={activeTab === 'dashboard' ? 'active' : ''} 
          onClick={() => setActiveTab('dashboard')}
          disabled={!currentData}
        >
          Dashboard
        </button>
        <button 
          className={activeTab === 'table' ? 'active' : ''} 
          onClick={() => setActiveTab('table')}
          disabled={!currentData}
        >
          Data Table
        </button>
        <button 
          className={activeTab === 'history' ? 'active' : ''} 
          onClick={() => setActiveTab('history')}
        >
          History
        </button>
      </nav>
      <main className="App-main">
        {activeTab === 'upload' && (
          <UploadComponent onUploadSuccess={handleUploadSuccess} />
        )}
        {activeTab === 'dashboard' && currentData && (
          <Dashboard data={currentData} />
        )}
        {activeTab === 'table' && currentData && (
          <DataTable data={currentData.raw_data || []} />
        )}
        {activeTab === 'history' && (
          <HistoryPanel history={history} onSelectUpload={setCurrentData} />
        )}
      </main>
    </div>
  );
}

export default App;
