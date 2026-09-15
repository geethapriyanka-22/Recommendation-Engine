import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';

export default function CheckoutPage() {
  const { cart, clearCart } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const [shippingInfo, setShippingInfo] = useState({
    fullName: user?.full_name || '',
    address: '100 Silicon Vista Blvd',
    city: 'San Francisco',
    state: 'CA',
    postalCode: '94107',
    country: 'United States',
    phone: '+1 (555) 019-2834'
  });

  const [paymentMethod, setPaymentMethod] = useState('card');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [orderComplete, setOrderComplete] = useState(null);

  const subtotal = cart?.items?.reduce((sum, item) => sum + item.product.price * item.quantity, 0) || 0;
  const tax = subtotal * 0.08;
  const shipping = subtotal > 50 ? 0 : 9.99;
  const total = subtotal + tax + shipping;

  const handleInputChange = (e) => {
    setShippingInfo(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmitOrder = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const orderNotes = `${notes ? notes + ' | ' : ''}Ship to: ${shippingInfo.fullName}, ${shippingInfo.address}, ${shippingInfo.city}, ${shippingInfo.state} ${shippingInfo.postalCode}. Payment: ${paymentMethod.toUpperCase()}`;
      const { data } = await api.post('/orders/checkout', {
        shipping_address_id: null,
        notes: orderNotes
      });

      setOrderComplete(data);
      if (clearCart) clearCart();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to place order. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (orderComplete) {
    return (
      <div className="container" style={{ padding: 'var(--space-12) var(--space-4)', maxWidth: '680px' }}>
        <div className="glass-card" style={{ padding: 'var(--space-8)', textAlign: 'center' }}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '80px',
            height: '80px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            color: 'white',
            fontSize: '2.5rem',
            marginBottom: 'var(--space-4)',
            boxShadow: '0 8px 24px rgba(16, 185, 129, 0.3)'
          }}>
            ✓
          </div>
          <h1 style={{ fontSize: 'var(--text-3xl)', fontWeight: 800, margin: '0 0 var(--space-2)' }}>
            Order Confirmed!
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: 'var(--text-base)', marginBottom: 'var(--space-6)' }}>
            Thank you for shopping with NovaMart. Your order has been placed and is being prepared.
          </p>

          <div style={{
            background: 'var(--bg-tertiary)',
            borderRadius: 'var(--radius-lg)',
            padding: 'var(--space-5)',
            marginBottom: 'var(--space-6)',
            textAlign: 'left'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-3)' }}>
              <span style={{ color: 'var(--text-secondary)', fontSize: 'var(--text-sm)' }}>Order Number:</span>
              <strong style={{ fontFamily: 'monospace', color: 'var(--accent-primary)' }}>{orderComplete.order_number}</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-3)' }}>
              <span style={{ color: 'var(--text-secondary)', fontSize: 'var(--text-sm)' }}>Status:</span>
              <span className="badge badge-success">{orderComplete.status.toUpperCase()}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-3)' }}>
              <span style={{ color: 'var(--text-secondary)', fontSize: 'var(--text-sm)' }}>Items:</span>
              <span>{orderComplete.items?.length || 0} product(s)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', borderTop: '1px solid var(--border-default)', paddingTop: 'var(--space-3)' }}>
              <span style={{ fontWeight: 600 }}>Total Paid:</span>
              <strong style={{ fontSize: 'var(--text-lg)', color: 'var(--accent-primary)' }}>
                ${orderComplete.total?.toFixed(2)}
              </strong>
            </div>
          </div>

          <div style={{ display: 'flex', gap: 'var(--space-4)', justifyContent: 'center' }}>
            <Link to="/orders" className="btn btn-primary">
              View Order History
            </Link>
            <Link to="/products" className="btn btn-secondary">
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (!cart?.items || cart.items.length === 0) {
    return (
      <div className="container" style={{ padding: 'var(--space-12) var(--space-4)', textAlign: 'center' }}>
        <div className="glass-card" style={{ padding: 'var(--space-8)', maxWidth: '500px', margin: '0 auto' }}>
          <span style={{ fontSize: '3rem', display: 'block', marginBottom: 'var(--space-3)' }}>🛒</span>
          <h2>Your cart is empty</h2>
          <p style={{ color: 'var(--text-secondary)', margin: 'var(--space-2) 0 var(--space-6)' }}>
            Add items to your cart before proceeding to checkout.
          </p>
          <Link to="/products" className="btn btn-primary">
            Explore Catalog
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container" style={{ padding: 'var(--space-8) var(--space-4)' }}>
      <h1 style={{ fontSize: 'var(--text-3xl)', fontWeight: 800, marginBottom: 'var(--space-6)' }}>
        Checkout
      </h1>

      {error && (
        <div style={{
          padding: 'var(--space-4)',
          borderRadius: 'var(--radius-md)',
          background: 'rgba(239, 68, 68, 0.12)',
          border: '1px solid rgba(239, 68, 68, 0.3)',
          color: '#f87171',
          marginBottom: 'var(--space-6)',
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--space-2)'
        }}>
          <span>⚠️</span>
          <span>{error}</span>
        </div>
      )}

      <form onSubmit={handleSubmitOrder}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: 'var(--space-8)',
          alignItems: 'start'
        }}>
          {/* Left Column: Shipping & Payment */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-6)' }}>
            {/* Shipping Address */}
            <div className="glass-card" style={{ padding: 'var(--space-6)' }}>
              <h2 style={{ fontSize: 'var(--text-lg)', fontWeight: 700, marginBottom: 'var(--space-4)', display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
                <span>📍</span> Shipping Address
              </h2>
              <div style={{ display: 'grid', gap: 'var(--space-4)' }}>
                <div>
                  <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: 'var(--space-1)' }}>
                    Full Recipient Name
                  </label>
                  <input
                    type="text"
                    required
                    name="fullName"
                    value={shippingInfo.fullName}
                    onChange={handleInputChange}
                  />
                </div>

                <div>
                  <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: 'var(--space-1)' }}>
                    Street Address
                  </label>
                  <input
                    type="text"
                    required
                    name="address"
                    value={shippingInfo.address}
                    onChange={handleInputChange}
                  />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr', gap: 'var(--space-3)' }}>
                  <div>
                    <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: 'var(--space-1)' }}>
                      City
                    </label>
                    <input
                      type="text"
                      required
                      name="city"
                      value={shippingInfo.city}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div>
                    <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: 'var(--space-1)' }}>
                      State
                    </label>
                    <input
                      type="text"
                      required
                      name="state"
                      value={shippingInfo.state}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div>
                    <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: 'var(--space-1)' }}>
                      ZIP Code
                    </label>
                    <input
                      type="text"
                      required
                      name="postalCode"
                      value={shippingInfo.postalCode}
                      onChange={handleInputChange}
                    />
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-3)' }}>
                  <div>
                    <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: 'var(--space-1)' }}>
                      Country
                    </label>
                    <input
                      type="text"
                      required
                      name="country"
                      value={shippingInfo.country}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div>
                    <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: 'var(--space-1)' }}>
                      Phone
                    </label>
                    <input
                      type="tel"
                      required
                      name="phone"
                      value={shippingInfo.phone}
                      onChange={handleInputChange}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Payment Method */}
            <div className="glass-card" style={{ padding: 'var(--space-6)' }}>
              <h2 style={{ fontSize: 'var(--text-lg)', fontWeight: 700, marginBottom: 'var(--space-4)', display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
                <span>💳</span> Payment Method
              </h2>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
                {[
                  { id: 'card', name: 'Credit / Debit Card (Mock)', desc: 'Instant demo clearance' },
                  { id: 'upi', name: 'UPI / Instant Bank Transfer', desc: 'Zero gateway fees' },
                  { id: 'cod', name: 'Cash on Delivery', desc: 'Pay when package arrives' },
                ].map((m) => (
                  <label
                    key={m.id}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 'var(--space-3)',
                      padding: 'var(--space-3) var(--space-4)',
                      borderRadius: 'var(--radius-md)',
                      background: paymentMethod === m.id ? 'var(--accent-glow)' : 'var(--bg-tertiary)',
                      border: `1px solid ${paymentMethod === m.id ? 'var(--accent-primary)' : 'var(--border-default)'}`,
                      cursor: 'pointer',
                      transition: 'all 0.2s ease'
                    }}
                  >
                    <input
                      type="radio"
                      name="payment"
                      value={m.id}
                      checked={paymentMethod === m.id}
                      onChange={() => setPaymentMethod(m.id)}
                      style={{ width: 'auto' }}
                    />
                    <div>
                      <div style={{ fontWeight: 600, fontSize: 'var(--text-sm)' }}>{m.name}</div>
                      <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>{m.desc}</div>
                    </div>
                  </label>
                ))}
              </div>

              {/* Order Notes */}
              <div style={{ marginTop: 'var(--space-4)' }}>
                <label style={{ fontSize: 'var(--text-xs)', fontWeight: 600, color: 'var(--text-secondary)', display: 'block', marginBottom: 'var(--space-1)' }}>
                  Delivery Instructions / Notes (Optional)
                </label>
                <textarea
                  rows={2}
                  placeholder="e.g. Leave at front porch, ring doorbell"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                />
              </div>
            </div>
          </div>

          {/* Right Column: Order Summary */}
          <div className="glass-card" style={{ padding: 'var(--space-6)', position: 'sticky', top: '100px' }}>
            <h2 style={{ fontSize: 'var(--text-lg)', fontWeight: 700, marginBottom: 'var(--space-4)' }}>
              Order Review ({cart.items.length})
            </h2>

            <div style={{ maxHeight: '280px', overflowY: 'auto', marginBottom: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: 'var(--space-3)' }}>
              {cart.items.map((item) => (
                <div key={item.id} style={{ display: 'flex', gap: 'var(--space-3)', alignItems: 'center' }}>
                  <img
                    src={item.product?.images?.[0]?.image_url || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=100'}
                    alt={item.product?.title}
                    style={{ width: '48px', height: '48px', objectFit: 'cover', borderRadius: 'var(--radius-sm)' }}
                  />
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 'var(--text-xs)', fontWeight: 600, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {item.product?.title}
                    </div>
                    <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
                      Qty: {item.quantity} × ${item.product?.price?.toFixed(2)}
                    </div>
                  </div>
                  <strong style={{ fontSize: 'var(--text-sm)' }}>
                    ${(item.product?.price * item.quantity).toFixed(2)}
                  </strong>
                </div>
              ))}
            </div>

            <div style={{ borderTop: '1px solid var(--border-default)', paddingTop: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: 'var(--space-2)', fontSize: 'var(--text-sm)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                <span>Subtotal:</span>
                <span>${subtotal.toFixed(2)}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                <span>Est. Tax (8%):</span>
                <span>${tax.toFixed(2)}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)' }}>
                <span>Shipping:</span>
                <span>{shipping === 0 ? <strong style={{ color: 'var(--success)' }}>FREE</strong> : `$${shipping.toFixed(2)}`}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', borderTop: '1px solid var(--border-default)', paddingTop: 'var(--space-3)', marginTop: 'var(--space-1)' }}>
                <span style={{ fontWeight: 700, fontSize: 'var(--text-base)' }}>Total:</span>
                <span style={{ fontWeight: 800, fontSize: 'var(--text-xl)', color: 'var(--accent-primary)' }}>
                  ${total.toFixed(2)}
                </span>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
              style={{ width: '100%', marginTop: 'var(--space-6)', padding: 'var(--space-4)', fontSize: 'var(--text-base)' }}
            >
              {loading ? 'Processing Order...' : `Place Order • $${total.toFixed(2)}`}
            </button>

            <div style={{ marginTop: 'var(--space-4)', textAlign: 'center', fontSize: 'var(--text-xs)', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 'var(--space-1)' }}>
              🔒 Simulated end-to-end checkout with atomic DB transaction
            </div>
          </div>
        </div>
      </form>
    </div>
  );
}
