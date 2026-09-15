import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { formatPrice } from '../utils/currency';

export default function OrdersPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useAuth();

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const { data } = await api.get('/orders/');
      setOrders(data.items || []);
    } catch (err) {
      setError('Unable to load orders. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const s = status?.toLowerCase();
    if (s === 'delivered') return <span className="badge badge-success">Delivered</span>;
    if (s === 'shipped') return <span className="badge" style={{ background: 'rgba(59, 130, 246, 0.15)', color: '#60a5fa', border: '1px solid rgba(59, 130, 246, 0.3)' }}>Shipped</span>;
    if (s === 'processing' || s === 'confirmed') return <span className="badge badge-primary">Processing</span>;
    if (s === 'cancelled') return <span className="badge badge-danger">Cancelled</span>;
    return <span className="badge badge-warning">{status}</span>;
  };

  if (loading) {
    return (
      <div className="container" style={{ padding: 'var(--space-12) var(--space-4)' }}>
        <h1 style={{ fontSize: 'var(--text-3xl)', fontWeight: 800, marginBottom: 'var(--space-6)' }}>Your Orders</h1>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
          {[1, 2, 3].map((i) => (
            <div key={i} className="skeleton" style={{ height: '140px', borderRadius: 'var(--radius-lg)' }} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="container" style={{ padding: 'var(--space-8) var(--space-4)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-6)' }}>
        <div>
          <h1 style={{ fontSize: 'var(--text-3xl)', fontWeight: 800, margin: '0 0 var(--space-1)' }}>Your Orders</h1>
          <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
            Track and manage your order history
          </p>
        </div>
        <Link to="/products" className="btn btn-secondary btn-sm">
          Continue Shopping
        </Link>
      </div>

      {error && (
        <div style={{ padding: 'var(--space-4)', background: 'rgba(239, 68, 68, 0.1)', color: '#f87171', borderRadius: 'var(--radius-md)', marginBottom: 'var(--space-4)' }}>
          {error}
        </div>
      )}

      {orders.length === 0 ? (
        <div className="glass-card" style={{ padding: 'var(--space-12)', textAlign: 'center' }}>
          <span style={{ fontSize: '3rem', display: 'block', marginBottom: 'var(--space-3)' }}>📦</span>
          <h2>No orders yet</h2>
          <p style={{ color: 'var(--text-secondary)', margin: 'var(--space-2) 0 var(--space-6)' }}>
            When you place an order, it will appear here.
          </p>
          <Link to="/products" className="btn btn-primary">
            Explore Catalog
          </Link>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-5)' }}>
          {orders.map((order) => (
            <div key={order.id} className="glass-card" style={{ padding: 'var(--space-6)', overflow: 'hidden' }}>
              <div style={{
                display: 'flex',
                flexWrap: 'wrap',
                justifyContent: 'space-between',
                alignItems: 'center',
                gap: 'var(--space-4)',
                borderBottom: '1px solid var(--border-default)',
                paddingBottom: 'var(--space-4)',
                marginBottom: 'var(--space-4)'
              }}>
                <div>
                  <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Order Number
                  </div>
                  <div style={{ fontFamily: 'monospace', fontWeight: 700, fontSize: 'var(--text-base)', color: 'var(--accent-primary)' }}>
                    {order.order_number}
                  </div>
                </div>

                <div>
                  <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Date Placed
                  </div>
                  <div style={{ fontSize: 'var(--text-sm)' }}>
                    {new Date(order.created_at).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric'
                    })}
                  </div>
                </div>

                <div>
                  <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Total Amount
                  </div>
                  <div style={{ fontWeight: 800, fontSize: 'var(--text-base)' }}>
                    {formatPrice(order.total)}
                  </div>
                </div>

                <div>
                  <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 'var(--space-1)' }}>
                    Status
                  </div>
                  {getStatusBadge(order.status)}
                </div>
              </div>

              {/* Order Items */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                {order.items?.map((item) => (
                  <div key={item.id} style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: 'var(--space-2) 0',
                    fontSize: 'var(--text-sm)'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                      <span style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: '28px',
                        height: '28px',
                        borderRadius: 'var(--radius-sm)',
                        background: 'var(--bg-tertiary)',
                        fontSize: 'var(--text-xs)',
                        fontWeight: 600
                      }}>
                        {item.quantity}×
                      </span>
                      <div>
                        <span style={{ fontWeight: 600 }}>{item.product_title}</span>
                        <span style={{ marginLeft: 'var(--space-2)', fontSize: 'var(--text-xs)', color: 'var(--text-muted)' }}>
                          ({item.product_sku})
                        </span>
                      </div>
                    </div>
                    <div style={{ fontWeight: 600 }}>
                      {formatPrice(item.total_price)}
                    </div>
                  </div>
                ))}
              </div>

              {order.notes && (
                <div style={{
                  marginTop: 'var(--space-4)',
                  paddingTop: 'var(--space-3)',
                  borderTop: '1px dashed var(--border-default)',
                  fontSize: 'var(--text-xs)',
                  color: 'var(--text-secondary)'
                }}>
                  📝 <strong>Notes:</strong> {order.notes}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
