import React, { useState } from 'react';
import api from '../api/client';

export default function Reports() {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [reportData, setReportData] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleGenerateSummary = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setReportData(null);

    try {
      const response = await api.post('/reports/summary', {
        start_date: startDate,
        end_date: endDate,
      });
      setReportData(response.data.report);
      setSuccess(response.data.message);
    } catch (err) {
      const errorDetail = err.response?.data?.detail;
      setError(typeof errorDetail === 'string' ? errorDetail : 'Failed to generate report.');
    }
  };

  const handleDownloadCSV = async (endpoint, filename) => {
    setError('');
    try {
      const response = await api.post(
        endpoint,
        { start_date: startDate, end_date: endDate },
        { responseType: 'blob' } // Important for handling binary file downloads
      );

      // Create a temporary URL to trigger file download in browser
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError('Failed to download CSV report.');
    }
  };

  return (
    <div style={{ marginTop: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3>Financial Reports & CSV Exports</h3>

      {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}
      {success && <div style={{ color: 'green', marginBottom: '10px' }}>{success}</div>}

      <form onSubmit={handleGenerateSummary} style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px', marginBottom: '20px' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '5px' }}>Start Date (YYYY-MM-DD)</label>
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '5px' }}>End Date (YYYY-MM-DD)</label>
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>

        <button type="submit" style={{ gridColumn: 'span 2', padding: '10px', backgroundColor: '#6c757d', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Generate Period Summary
        </button>
      </form>

      {reportData && (
        <div style={{ marginTop: '20px', padding: '15px', background: '#f8f9fa', borderRadius: '6px' }}>
          <h4>Summary Results ({reportData.start_date} to {reportData.end_date})</h4>
          <p><strong>Total Transactions:</strong> {reportData.number_of_transactions}</p>
          <p><strong>Total Income:</strong> ${reportData.total_income}</p>
          <p><strong>Total Expenses:</strong> ${reportData.total_expenses}</p>
          <p><strong>Net Balance:</strong> ${reportData.balance}</p>

          <h5 style={{ marginTop: '15px' }}>Category Breakdown</h5>
          <ul>
            {Object.entries(reportData.category_summary).length === 0 ? (
              <li>No expenses recorded in this period.</li>
            ) : (
              Object.entries(reportData.category_summary).map(([cat, amt]) => (
                <li key={cat}><strong>{cat}:</strong> ${amt}</li>
              ))
            )}
          </ul>

          <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
            <button
              onClick={() => handleDownloadCSV('/reports/export/transactions', 'transaction_report.csv')}
              style={{ padding: '8px 12px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
            >
              Export Transactions CSV
            </button>
            <button
              onClick={() => handleDownloadCSV('/reports/export/summary', 'summary_report.csv')}
              style={{ padding: '8px 12px', backgroundColor: '#17a2b8', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
            >
              Export Summary CSV
            </button>
          </div>
        </div>
      )}
    </div>
  );
}