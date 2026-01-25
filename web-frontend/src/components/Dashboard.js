import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Scatter } from 'react-chartjs-2';
import './Dashboard.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Dashboard = ({ data }) => {
  if (!data) return null;

  // Equipment Type Distribution Chart
  const equipmentTypes = Object.keys(data.equipment_type_distribution || {});
  const equipmentCounts = Object.values(data.equipment_type_distribution || {});

  const barChartData = {
    labels: equipmentTypes,
    datasets: [
      {
        label: 'Equipment Count',
        data: equipmentCounts,
        backgroundColor: [
          'rgba(102, 126, 234, 0.8)',
          'rgba(118, 75, 162, 0.8)',
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(255, 206, 86, 0.8)',
        ],
        borderColor: [
          'rgba(102, 126, 234, 1)',
          'rgba(118, 75, 162, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  // Flowrate vs Pressure Scatter Plot
  const rawData = data.raw_data || [];
  const scatterData = {
    datasets: [
      {
        label: 'Flowrate vs Pressure',
        data: rawData.map(item => ({
          x: item.Pressure,
          y: item.Flowrate,
        })),
        backgroundColor: 'rgba(102, 126, 234, 0.6)',
        borderColor: 'rgba(102, 126, 234, 1)',
        pointRadius: 5,
        pointHoverRadius: 7,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          color: 'white',
          font: {
            size: 14,
          },
        },
      },
      title: {
        display: true,
        color: 'white',
        font: {
          size: 18,
          weight: 'bold',
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: 'white',
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
      y: {
        ticks: {
          color: 'white',
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)',
        },
      },
    },
  };

  const barOptions = {
    ...chartOptions,
    plugins: {
      ...chartOptions.plugins,
      title: {
        ...chartOptions.plugins.title,
        text: 'Equipment Type Distribution',
      },
    },
  };

  const scatterOptions = {
    ...chartOptions,
    plugins: {
      ...chartOptions.plugins,
      title: {
        ...chartOptions.plugins.title,
        text: 'Flowrate vs Pressure',
      },
    },
  };

  return (
    <div className="dashboard">
      <div className="stats-summary">
        <div className="stat-card">
          <h3>Average Flowrate</h3>
          <p className="stat-value">{data.avg_flowrate}</p>
        </div>
        <div className="stat-card">
          <h3>Average Pressure</h3>
          <p className="stat-value">{data.avg_pressure}</p>
        </div>
        <div className="stat-card">
          <h3>Average Temperature</h3>
          <p className="stat-value">{data.avg_temperature}</p>
        </div>
        <div className="stat-card">
          <h3>Total Records</h3>
          <p className="stat-value">{data.total_records}</p>
        </div>
      </div>
      <div className="charts-container">
        <div className="chart-wrapper">
          <Bar data={barChartData} options={barOptions} />
        </div>
        <div className="chart-wrapper">
          <Scatter data={scatterData} options={scatterOptions} />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
