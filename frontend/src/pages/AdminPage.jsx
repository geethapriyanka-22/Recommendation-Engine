import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

export default function AdminPage() {
  const { user, isAdmin } = useAuth();
  const navigate = useNavigate();

  const [tab, setTab] = useState('overview'); // overview, orders, users, actions
  const [stats, setStats] = useState(null);
  const [orders, setOrders] = useState([]);
  const [usersList, setUsersList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState('');
  const [feedback, setFeedback] = useState(null);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    if (!isAdmin) {
      return;
    }
    loadData();
  }, [user, isAdmin]);

  const loadData = async () => {
    setLoading(true);
    try {
      const [statsRes, ordersRes, usersRes] = await Promise.all([
        api.get('/admin/dashboard'),
        api.get('/admin/orders?limit=25'),
        api.get('/admin/users?limit=50')
      ]);
      setStats(statsRes.data);
      setOrders(ordersRes.data.items || []);
      setUsersList(usersRes.data || []);
    } catch (err) {
      setFeedback({ type: 'error', message: err.response?.data?.detail || 'Failed to load admin data.' });
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateOrderStatus = async (orderId, newStatus) => {
    try {
      await api.patch(`/admin/orders/${orderId}/status`, { status: newStatus });
      setFeedback({ type: 'success', message: `Order updated to ${newStatus}` });
      loadData();
    } catch (err) {
      setFeedback({ type: 'error', message: err.response?.data?.detail || 'Failed to update order status.' });
    }
  };

  const handleToggleUserRole = async (userId, currentRole) => {
    const newRole = currentRole === 'admin' ? 'customer' : 'admin';
    try {
      await api.patch(`/admin/users/${userId}/role`, { role: newRole });
      setFeedback({ type: 'success', message: `User role updated to ${newRole}` });
      loadData();
    } catch (err) {
      setFeedback({ type: 'error', message: err.response?.data?.detail || 'Failed to change role.' });
    }
  };

  const handleTriggerSeed = async () => {
    setActionLoading('seed');
    try {
      const { data } = await api.post('/admin/seed');
      setFeedback({ type: 'success', message: `Synthetic data seeded! Created ${data.stats?.products || 'catalog'} items.` });
      loadData();
    } catch (err) {
      setFeedback({ type: 'error', message: err.response?.data?.detail || 'Seed failed.' });
    } finally {
      setActionLoading('');
    }
  };

  const handleReindexEmbeddings = async () => {
    setActionLoading('reindex');
    try {
      const { data } = await api.post('/admin/reindex-embeddings');
      setFeedback({ type: 'success', message: data.message || 'Embeddings re-indexed successfully!' });
    } catch (err) {
      setFeedback({ type: 'error', message: err.response?.data?.detail || 'Reindex failed.' });
    } finally {
      setActionLoading('');
    }
  };

  if (!isAdmin) {
    return (
      <div className="container" style={{ padding: 'var(--space-12) var(--space-4)', textAlign: 'center' }}>
        <div className="glass-card" style={{ maxWidth: '480px', margin: '0 auto', padding: 'var(--space-8)' }}>
          <span style={{ fontSize: '3rem', display: 'block', marginBottom: 'var(--space-3)' }}>🚫</span>
          <h2>Access Denied</h2>
          <p style={{ color: 'var(--text-secondary)', margin: 'var(--space-2) 0 var(--space-6)' }}>
            You need administrator privileges to access the NovaMart management console.
          </p>
          <button onClick={() => navigate('/')} className="btn btn-primary">
            Return to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container" style={{ padding: 'var(--space-8) var(--space-4)' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-6)', flexWrap: 'wrap', gap: 'var(--space-4)' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
            <h1 style={{ fontSize: 'var(--text-3xl)', fontWeight: 800, margin: 0 }}>
              Admin Operations Hub
            </h1>
            <span className="badge badge-primary">SYSTEM ACTIVE</span>
          </div>
          <p style={{ color: 'var(--text-secondary)', margin: 'var(--space-1) 0 0' }}>
            Telemetry, customer orders, synthetic engine control, and pgvector re-indexing
          </p>
        </div>

        <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
          <button
            onClick={handleReindexEmbeddings}
            disabled={actionLoading === 'reindex'}
            className="btn btn-secondary btn-sm"
          >
            {actionLoading === 'reindex' ? '⚡ Indexing...' : '🧠 Reindex Vectors'}
          </button>
          <button
            onClick={handleTriggerSeed}
            disabled={actionLoading === 'seed'}
            className="btn btn-primary btn-sm"
          >
            {actionLoading === 'seed' ? '🌱 Seeding...' : '🌱 Seed Synthetic Data'}
          </button>
        </div>
      </div>

      {feedback && (
        <div style={{
          padding: 'var(--space-3) var(--space-4)',
          borderRadius: 'var(--radius-md)',
          marginBottom: 'var(--space-6)',
          background: feedback.type === 'success' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
          color: feedback.type === 'success' ? '#34d399' : '#f87171',
          border: `1px solid ${feedback.type === 'success' ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)'}`,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <span>{feedback.message}</span>
          <button onClick={() => setFeedback(null)} style={{ color: 'inherit', fontWeight: 700 }}>✕</button>
        </div>
      )}

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 'var(--space-2)', borderBottom: '1px solid var(--border-default)', marginBottom: 'var(--space-6)' }}>
        {[
          { id: 'overview', label: '📊 Overview & KPIs' },
          { id: 'orders', label: `📦 Orders (${orders.length})` },
          { id: 'users', label: `👥 Users (${usersList.length})` },
        ].map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            style={{
              padding: 'var(--space-3) var(--space-5)',
              fontWeight: tab === t.id ? 700 : 500,
              color: tab === t.id ? 'var(--accent-primary)' : 'var(--text-secondary)',
              borderBottom: `2px solid ${tab === t.id ? 'var(--accent-primary)' : 'transparent'}`,
              transition: 'all 0.2s ease',
              background: 'none'
            }}
          >
            {t.label}
          </button>
        ))}
      </div>

      {loading ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 'var(--space-4)' }}>
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="skeleton" style={{ height: '120px', borderRadius: 'var(--radius-lg)' }} />
          ))}
        </div>
      ) : (
        <>
          {/* Overview Tab */}
          {tab === 'overview' && stats && (
            <div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: 'var(--space-5)', marginBottom: 'var(--space-8)' }}>
                <div className="glass-card" style={{ padding: 'var(--space-5)' }}>
                  <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Gross Revenue
                  </span>
                  <div style={{ fontSize: 'var(--text-3xl)', fontWeight: 800, color: 'var(--accent-primary)', marginTop: 'var(--space-1)' }}>
                    ${stats.total_revenue?.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                  </div>
                  <div style={{ fontSize: 'var(--text-xs)', color: 'var(--success)', marginTop: 'var(--space-2)' }}>
                    ↑ Atomic checkout ledger
                  </div>
                </div>

                <div className="glass-card" style={{ padding: 'var(--space-5)' }}>
                  <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Total Orders
                  </span>
                  <div style={{ fontSize: 'var(--text-3xl)', fontWeight: 800, marginTop: 'var(--space-1)' }}>
                    {stats.total_orders}
                  </div>
                  <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', marginTop: 'var(--space-2)' }}>
                    State-machine validated
                  </div>
                </div>

                <div className="glass-card" style={{ padding: 'var(--space-5)' }}>
                  <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Total Products
                  </span>
                  <div style={{ fontSize: 'var(--text-3xl)', fontWeight: 800, marginTop: 'var(--space-1)' }}>
                    {stats.total_products}
                  </div>
                  <div style={{ fontSize: 'var(--text-xs)', color: 'var(--warning)', marginTop: 'var(--space-2)' }}>
                    {stats.low_stock_products} low stock items (&lt;5)
                  </div>
                </div>

                <div className="glass-card" style={{ padding: 'var(--space-5)' }}>
                  <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Registered Users
                  </span>
                  <div style={{ fontSize: 'var(--text-3xl)', fontWeight: 800, marginTop: 'var(--space-1)' }}>
                    {stats.total_users}
                  </div>
                  <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', marginTop: 'var(--space-2)' }}>
                    RBAC enabled
                  </div>
                </div>
              </div>

              {/* Status breakdown */}
              <div className="glass-card" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
                <h3 style={{ fontSize: 'var(--text-lg)', fontWeight: 700, marginBottom: 'var(--space-4)' }}>
                  Orders Pipeline Status
                </h3>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: 'var(--space-3)' }}>
                  {Object.entries(stats.orders_by_status || {}).map(([st, count]) => (
                    <div key={st} style={{
                      padding: 'var(--space-4)',
                      background: 'var(--bg-tertiary)',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border-default)',
                      textAlign: 'center'
                    }}>
                      <div style={{ fontSize: 'var(--text-xs)', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>{st}</div>
                      <div style={{ fontSize: 'var(--text-xl)', fontWeight: 800, marginTop: 'var(--space-1)' }}>{count}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Orders Tab */}
          {tab === 'orders' && (
            <div className="glass-card" style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: 'var(--text-sm)' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid var(--border-default)', background: 'var(--bg-tertiary)' }}>
                    <th style={{ padding: 'var(--space-4)' }}>Order ID</th>
                    <th style={{ padding: 'var(--space-4)' }}>Created</th>
                    <th style={{ padding: 'var(--space-4)' }}>Items</th>
                    <th style={{ padding: 'var(--space-4)' }}>Total</th>
                    <th style={{ padding: 'var(--space-4)' }}>Current Status</th>
                    <th style={{ padding: 'var(--space-4)' }}>Update Status</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map((o) => (
                    <tr key={o.id} style={{ borderBottom: '1px solid var(--border-default)' }}>
                      <td style={{ padding: 'var(--space-4)', fontFamily: 'monospace', fontWeight: 600, color: 'var(--accent-primary)' }}>
                        {o.order_number}
                      </td>
                      <td style={{ padding: 'var(--space-4)', color: 'var(--text-secondary)' }}>
                        {new Date(o.created_at).toLocaleDateString()}
                      </td>
                      <td style={{ padding: 'var(--space-4)' }}>
                        {o.items?.length || 0}
                      </td>
                      <td style={{ padding: 'var(--space-4)', fontWeight: 700 }}>
                        ${o.total?.toFixed(2)}
                      </td>
                      <td style={{ padding: 'var(--space-4)' }}>
                        <span className="badge badge-primary">{o.status}</span>
                      </td>
                      <td style={{ padding: 'var(--space-4)' }}>
                        <select
                          value={o.status}
                          onChange={(e) => handleUpdateOrderStatus(o.id, e.target.value)}
                          style={{ padding: 'var(--space-1) var(--space-2)', fontSize: 'var(--text-xs)', width: 'auto' }}
                        >
                          <option value="pending">pending</option>
                          <option value="confirmed">confirmed</option>
                          <option value="processing">processing</option>
                          <option value="shipped">shipped</option>
                          <option value="delivered">delivered</option>
                          <option value="cancelled">cancelled</option>
                        </select>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Users Tab */}
          {tab === 'users' && (
            <div className="glass-card" style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: 'var(--text-sm)' }}>
                <thead>
                  <tr style={{ borderBottom: '1px solid var(--border-default)', background: 'var(--bg-tertiary)' }}>
                    <th style={{ padding: 'var(--space-4)' }}>Name</th>
                    <th style={{ padding: 'var(--space-4)' }}>Email</th>
                    <th style={{ padding: 'var(--space-4)' }}>Role</th>
                    <th style={{ padding: 'var(--space-4)' }}>Status</th>
                    <th style={{ padding: 'var(--space-4)' }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {usersList.map((u) => (
                    <tr key={u.id} style={{ borderBottom: '1px solid var(--border-default)' }}>
                      <td style={{ padding: 'var(--space-4)', fontWeight: 600 }}>
                        {u.full_name || 'N/A'}
                      </td>
                      <td style={{ padding: 'var(--space-4)', color: 'var(--text-secondary)' }}>
                        {u.email}
                      </td>
                      <td style={{ padding: 'var(--space-4)' }}>
                        <span className={`badge ${u.role === 'admin' ? 'badge-primary' : 'badge-success'}`}>
                          {u.role.toUpperCase()}
                        </span>
                      </td>
                      <td style={{ padding: 'var(--space-4)' }}>
                        {u.is_active ? 'Active' : 'Inactive'}
                      </td>
                      <td style={{ padding: 'var(--space-4)' }}>
                        <button
                          onClick={() => handleToggleUserRole(u.id, u.role)}
                          className="btn btn-secondary btn-sm"
                          style={{ fontSize: 'var(--text-xs)', padding: 'var(--space-1) var(--space-3)' }}
                        >
                          {u.role === 'admin' ? 'Demote to Customer' : 'Promote to Admin'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}
