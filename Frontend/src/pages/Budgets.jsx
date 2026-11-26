import React, { useState, useEffect } from 'react';
import api from '../api/client';

export default function Budgets() {
  const [budgets, setBudgets] = useState([]);
  const [category, setCategory] = useState('');
  const [budgetLimit, setBudgetLimit] = useState('');
  const [warningThreshold, setWarningThreshold] = useState(80);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchBudgets();
  }, []);

  const fetchBudgets = async () => {
    try {
      const response = await api.get('/budgets');
      // For each budget, fetch its live spending status
      const budgetsWithStatus = await Promise.all(
        response.data.map(async (b) => {
          try {
            const statusRes = await api.get(`/budgets/${b.budgetID}/status`);
            return { ...b, statusData: statusRes.data.budget_status, message: statusRes.data.message };
          } catch {
            return { ...b, statusData: null, message: 'Unable to load status' };
          }
        })
      );
      setBudgets(budgetsWithStatus);
    } catch (err) {
      console.error('Failed to load budgets', err);
    }
  };

  const handleAddBudget = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await api.post('/budgets', {
        category,
        budget_limit: parseFloat(budgetLimit),
        warning_threshold: parseInt(warningThreshold, 10),
      });

      setSuccess('Budget created successfully!');
      setCategory('');
      setBudgetLimit('');
      setWarningThreshold(80);
      fetchBudgets();
    } catch (err) {
      const errorDetail = err.response?.data?.detail;
      setError(typeof errorDetail === 'string' ? errorDetail : 'Failed to create budget.');
    }
  };

  const handleDeleteBudget = async (id) => {
    try {
      await api.delete(`/budgets/${id}`);
      fetchBudgets();
    } catch (err) {
      console.error('Failed to delete budget', err);
    }
  };

  return (
    <div style={{ marginTop: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3>Manage Budgets & Limits</h3>

      {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}
      {success && <div style={{ color: 'green', marginBottom: '10px' }}>{success}</div>}

      <form onSubmit={handleAddBudget} style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', marginBottom: '30px' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '5px' }}>Category</label>
          <input
            type="text"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            placeholder="e.g., Food, Entertainment"
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '5px' }}>Budget Limit ($)</label>
          <input
            type="number"
            step="0.01"
            value={budgetLimit}
            onChange={(e) => setBudgetLimit(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '5px' }}>Warning Threshold (%)</label>
          <input
            type="number"
            min="1"
            max="100"
            value={warningThreshold}
            onChange={(e) => setWarningThreshold(e.target.value)}
            required
            style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
          />
        </div>

        <button type="submit" style={{ gridColumn: 'span 3', padding: '10px', backgroundColor: '#17a2b8', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Set Budget Limit
        </button>
      </form>

      <h4>Active Budgets & Spending Progress</h4>
      <div style={{ display: 'grid', gap: '15px', marginTop: '10px' }}>
        {budgets.length === 0 ? (
          <p>No budgets configured yet.</p>
        ) : (
          budgets.map((b) => {
            const pct = b.statusData?.percentage_used || 0;
            const spent = b.statusData?.total_spending || 0;
            const limit = b.budgetLimit;
            const isExceeded = spent > limit;
            const isWarning = pct >= b.warningThreshold && !isExceeded;

            return (
              <div key={b.budgetID} style={{ padding: '15px', border: '1px solid #ccc', borderRadius: '6px', background: '#fdfdfd' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <strong>{b.category}</strong>
                  <span>Spent: ${spent} / Limit: ${limit}</span>
                  <button onClick={() => handleDeleteBudget(b.budgetID)} style={{ background: '#dc3545', color: 'white', border: 'none', padding: '4px 8px', borderRadius: '4px', cursor: 'pointer' }}>
                    Remove
                  </button>
                </div>

                {/* Progress bar */}
                <div style={{ background: '#e9ecef', borderRadius: '4px', height: '12px', width: '100%', overflow: 'hidden' }}>
                  <div
                    style={{
                      width: `${Math.min(pct, 100)}%`,
                      background: isExceeded ? '#dc3545' : isWarning ? '#ffc107' : '#28a745',
                      height: '100%'
                    }}
                  />
                </div>
               
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85em', marginTop: '5px', color: '#666' }}>
                  <span>{pct}% used</span>
                  <span style={{ fontWeight: 'bold', color: isExceeded ? '#dc3545' : isWarning ? '#856404' : '#28a745' }}>
                    {b.message}
                  </span>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}