import React, { useState, useEffect } from 'react';
import Login from './pages/Login';
import Transactions from './pages/Transactions';
import Budgets from './pages/Budgets';
import Reports from './pages/Reports';
import api from './api/client';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [dashboardData, setDashboardData] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
      fetchDashboard();
    }
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await api.get('/dashboard');
      setDashboardData(response.data);
    } catch (err) {
      console.error('Session expired or unauthorized', err);
      handleLogout();
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    setIsAuthenticated(false);
    setDashboardData(null);
  };

  if (!isAuthenticated) {
    return <Login onLoginSuccess={() => { setIsAuthenticated(true); fetchDashboard(); }} />;
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Personal Budgeting & Expense Tracker</h1>
        <button onClick={handleLogout} style={{ padding: '8px 12px', backgroundColor: '#dc3545', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Logout
        </button>
      </div>

      <h2>Dashboard Summary</h2>
      {dashboardData ? (
        <div style={{ display: 'flex', gap: '20px', marginTop: '10px' }}>
          <div style={{ flex: 1, padding: '15px', background: '#d4edda', borderRadius: '6px' }}>
            <h3>Total Income</h3>
            <p style={{ fontSize: '1.2em', fontWeight: 'bold' }}>${dashboardData.total_income}</p>
          </div>
          <div style={{ flex: 1, padding: '15px', background: '#f8d7da', borderRadius: '6px' }}>
            <h3>Total Expenses</h3>
            <p style={{ fontSize: '1.2em', fontWeight: 'bold' }}>${dashboardData.total_expenses}</p>
          </div>
          <div style={{ flex: 1, padding: '15px', background: '#d1ecf1', borderRadius: '6px' }}>
            <h3>Balance</h3>
            <p style={{ fontSize: '1.2em', fontWeight: 'bold' }}>${dashboardData.balance}</p>
          </div>
        </div>
      ) : (
        <p>Loading dashboard data...</p>
      )}

      <Transactions />
      <Budgets />
      <Reports />
    </div>
  );
}