import React, { useState, useMemo } from 'react';
import './DataTable.css';

const DataTable = ({ data }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

  const filteredData = useMemo(() => {
    if (!data || !Array.isArray(data)) return [];
    
    return data.filter(item => {
      const searchLower = searchTerm.toLowerCase();
      return (
        (item['Equipment Name']?.toLowerCase().includes(searchLower)) ||
        (item.Type?.toLowerCase().includes(searchLower)) ||
        (item.Flowrate?.toString().includes(searchLower)) ||
        (item.Pressure?.toString().includes(searchLower)) ||
        (item.Temperature?.toString().includes(searchLower))
      );
    });
  }, [data, searchTerm]);

  const sortedData = useMemo(() => {
    if (!sortConfig.key) return filteredData;
    
    return [...filteredData].sort((a, b) => {
      const aVal = a[sortConfig.key];
      const bVal = b[sortConfig.key];
      
      if (aVal === bVal) return 0;
      
      const comparison = aVal > bVal ? 1 : -1;
      return sortConfig.direction === 'asc' ? comparison : -comparison;
    });
  }, [filteredData, sortConfig]);

  const handleSort = (key) => {
    setSortConfig(prevConfig => ({
      key,
      direction: prevConfig.key === key && prevConfig.direction === 'asc' ? 'desc' : 'asc',
    }));
  };

  if (!data || data.length === 0) {
    return <div className="data-table-empty">No data available</div>;
  }

  const columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'];

  return (
    <div className="data-table-container">
      <div className="data-table-header">
        <input
          type="text"
          placeholder="Search data..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <span className="results-count">
          Showing {sortedData.length} of {data.length} records
        </span>
      </div>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map(column => (
                <th
                  key={column}
                  onClick={() => handleSort(column)}
                  className="sortable"
                >
                  {column}
                  {sortConfig.key === column && (
                    <span className="sort-indicator">
                      {sortConfig.direction === 'asc' ? ' ↑' : ' ↓'}
                    </span>
                  )}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sortedData.map((row, index) => (
              <tr key={index}>
                {columns.map(column => (
                  <td key={column}>{row[column] ?? '-'}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;
