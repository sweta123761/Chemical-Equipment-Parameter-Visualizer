import React from 'react';
import './HistoryPanel.css';

const HistoryPanel = ({ history, onSelectUpload }) => {
  const handleDownloadReport = async (uploadId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/report/?id=${uploadId}`, {
        headers: {
          'Authorization': 'Basic ' + btoa('admin:admin123'),
        },
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `equipment_report_${uploadId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Error downloading report:', error);
      alert('Failed to download report');
    }
  };

  if (history.length === 0) {
    return (
      <div className="history-panel-empty">
        <p>No upload history available</p>
      </div>
    );
  }

  return (
    <div className="history-panel">
      <h2>Upload History (Last 5)</h2>
      <div className="history-list">
        {history.map((upload) => (
          <div key={upload.id} className="history-item">
            <div className="history-item-header">
              <h3>{upload.filename}</h3>
              <span className="history-date">
                {new Date(upload.upload_timestamp).toLocaleString()}
              </span>
            </div>
            <div className="history-stats">
              <div className="history-stat">
                <span className="stat-label">Records:</span>
                <span className="stat-value">{upload.total_records}</span>
              </div>
              <div className="history-stat">
                <span className="stat-label">Avg Flowrate:</span>
                <span className="stat-value">{upload.avg_flowrate}</span>
              </div>
              <div className="history-stat">
                <span className="stat-label">Avg Pressure:</span>
                <span className="stat-value">{upload.avg_pressure}</span>
              </div>
              <div className="history-stat">
                <span className="stat-label">Avg Temperature:</span>
                <span className="stat-value">{upload.avg_temperature}</span>
              </div>
            </div>
            <div className="history-actions">
              <button
                className="btn-view"
                onClick={() => onSelectUpload(upload)}
              >
                View Data
              </button>
              <button
                className="btn-download"
                onClick={() => handleDownloadReport(upload.id)}
              >
                Download PDF Report
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HistoryPanel;
