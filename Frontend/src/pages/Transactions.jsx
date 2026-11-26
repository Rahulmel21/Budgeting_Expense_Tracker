import React, { useState, useEffect } from 'react';
import api from '../api/client';

export default function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [amount, setAmount] = useState('');
  const [transactionType, setTransactionType] = useState('expense');
  const [category, setCategory] = useState('');
  const [date, setDate] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('');
  const [notes, setNotes] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Fetch transactions on component load
  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      const response = await api.get('/transactions');
      setTransactions(response.data);
    } catch (err) {
      console.error('Failed to load transactions', err);
    }
  };

  const handleAddTransaction = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await api.post('/transactions', {
        amount: parseFloat(amount),
        transaction_type: transactionType,
        category,
        date,
        payment_method: paymentMethod,
        notes,
      });

      setSuccess('Transaction added successfully!');
      // Reset form fields
      setAmount('');
      setCategory('');
      setDate('');
      setPaymentMethod('');
      setNotes('');
     
      // Refresh list
      fetchTransactions();
    } catch (err) {
      const errorDetail = err.response?.data?.detail;
      setError(typeof errorDetail === 'string' ? errorDetail : 'Failed to add transaction.');
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/transactions/${id}`);
      fetchTransactions();
    } catch (err) {
      console.error('Failed to delete transaction', err);
    }
  };

  return (
    <div style={{ marginTop: '20px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
      <h3>Manage Transactions</h3>

      {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}
      {success && <div style={{ color: 'green', marginBottom: '10px' }}>{success}</div>}

      <form onSubmit={handleAddTransaction} style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px', marginBottom: '30px' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '5px' }}>Amount</label>
          <input type="number" step="0.01" value={amount} onChange={(e) => setAmount(e.target.value)} required style={{ width: '100%', padding: '8px' }} />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '5px' }}>Type</label>
          <select value={transactionType} onChange={(e) => setTransactionType(e.target.value)} style={{ width: '100%', padding: '8px' }}>
            <option value="expense">Expense</option>
            <option value="income">Income</option>
          </select>
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '5px' }}>Category</label>
          <input type="text" value={category} onChange={(e) => setCategory(e.target.value)} placeholder="e.g., Food, Salary" required style={{ width: '100%', padding: '8px' }} />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '5px' }}>Date (YYYY-MM-DD)</label>
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required style={{ width: '100%', padding: '8px' }} />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '5px' }}>Payment Method</label>
          <input type="text" value={paymentMethod} onChange={(e) => setPaymentMethod(e.target.value)} placeholder="e.g., Credit Card, Cash" required style={{ width: '100%', padding: '8px' }} />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '5px' }}>Notes</label>
          <input type="text" value={notes} onChange={(e) => setNotes(e.target.value)} placeholder="Optional notes" style={{ width: '100%', padding: '8px' }} />
        </div>

        <button type="submit" style={{ gridColumn: 'span 2', padding: '10px', backgroundColor: '#28a745', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          Add Transaction
        </button>
      </form>

      <h4>Transaction History</h4>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
        <thead>
          <tr style={{ background: '#f1f1f1', textAlign: 'left' }}>
            <th style={{ padding: '8px', border: '1px solid #ddd' }}>Date</th>
            <th style={{ padding: '8px', border: '1px solid #ddd' }}>Category</th>
            <th style={{ padding: '8px', border: '1px solid #ddd' }}>Type</th>
            <th style={{ padding: '8px', border: '1px solid #ddd' }}>Amount</th>
            <th style={{ padding: '8px', border: '1px solid #ddd' }}>Method</th>
            <th style={{ padding: '8px', border: '1px solid #ddd' }}>Action</th>
          </tr>
        </thead>
        <tbody>
          {transactions.length === 0 ? (
            <tr>
              <td colSpan="6" style={{ textAlign: 'center', padding: '15px' }}>No transactions recorded yet.</td>
            </tr>
          ) : (
            transactions.map((tx) => (
              <tr key={tx.transactionID}>
                <td style={{ padding: '8px', border: '1px solid #ddd' }}>{tx.date}</td>
                <td style={{ padding: '8px', border: '1px solid #ddd' }}>{tx.category}</td>
                <td style={{ padding: '8px', border: '1px solid #ddd', textTransform: 'capitalize' }}>{tx.transactionType}</td>
                <td style={{ padding: '8px', border: '1px solid #ddd', color: tx.transactionType === 'income' ? 'green' : 'red' }}>
                  ${tx.amount}
                </td>
                <td style={{ padding: '8px', border: '1px solid #ddd' }}>{tx.paymentMethod}</td>
                <td style={{ padding: '8px', border: '1px solid #ddd' }}>
                  <button onClick={() => handleDelete(tx.transactionID)} style={{ background: '#dc3545', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '4px', cursor: 'pointer' }}>
                    Delete
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}