import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import { formatPrice } from '../utils/currency';

export default function CartPage() {
  const { cart, updateItem, removeItem, clearCart, loading } = useCart();
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleCheckout = async () => {
    try {
      const { data } = await api.post('/orders/checkout', {});
      navigate(`/orders`);
      alert(`Order ${data.order_number} placed successfully!`);
    } catch (err) {
      alert(err.response?.data?.detail || 'Checkout failed');
    }
  };

  if (!user) {
    return (
      <div className="container" style={{ padding: 'var(--space-16) 0', textAlign: 'center' }}>
        <h2 style={{ marginBottom: 'var(--space-4)' }}>Please sign in to view your cart</h2>
        <Link to="/login" className="btn btn-primary">Sign In</Link>
      </div>
    );
  }

  return (
    <div className="container animate-fade-in" style={{ padding: 'var(--space-8) var(--space-6)' }}>
      <h1 style={{ fontSize: 'var(--text-3xl)', fontWeight: 700, marginBottom: 'var(--space-8)' }}>
        Shopping Cart
      </h1>

      {cart.items.length === 0 ? (
        <div style={{ textAlign: 'center', padding: 'var(--space-16) 0' }}>
          <div style={{ fontSize: '4rem', marginBottom: 'var(--space-4)' }}>🛒</div>
          <h2 style={{ marginBottom: 'var(--space-4)', color: 'var(--text-secondary)' }}>Your cart is empty</h2>
          <Link to="/catalog" className="btn btn-primary">Start Shopping</Link>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 360px', gap: 'var(--space-8)', alignItems: 'start' }}>
          {/* Cart Items */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
            {cart.items.map((item) => (
              <div key={item.id} className="glass-card" style={{ padding: 'var(--space-4)', display: 'flex', gap: 'var(--space-4)', alignItems: 'center' }}>
                <img
                  src={item.product_image || `https://picsum.photos/seed/${item.product_id}/200/200`}
                  alt={item.product_title}
                  style={{ width: 96, height: 96, objectFit: 'cover', borderRadius: 'var(--radius-md)' }}
                />
                <div style={{ flex: 1 }}>
                  <h3 style={{ fontSize: 'var(--text-sm)', fontWeight: 600, marginBottom: 'var(--space-1)' }}>
                    {item.product_title}
                  </h3>
                  <span style={{ fontSize: 'var(--text-sm)', fontFamily: 'var(--font-mono)', color: 'var(--text-secondary)' }}>
                    {formatPrice(item.product_price)} each
                  </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)' }}>
                  <button onClick={() => item.quantity > 1 ? updateItem(item.id, item.quantity - 1) : removeItem(item.id)} className="btn btn-ghost" style={{ padding: 'var(--space-1) var(--space-2)' }}>−</button>
                  <span style={{ minWidth: '2rem', textAlign: 'center', fontWeight: 600, fontSize: 'var(--text-sm)' }}>{item.quantity}</span>
                  <button onClick={() => updateItem(item.id, item.quantity + 1)} className="btn btn-ghost" style={{ padding: 'var(--space-1) var(--space-2)' }}>+</button>
                </div>
                <span style={{ fontWeight: 700, fontFamily: 'var(--font-mono)', minWidth: '80px', textAlign: 'right' }}>
                  {formatPrice(item.line_total)}
                </span>
                <button onClick={() => removeItem(item.id)} className="btn btn-ghost" style={{ color: 'var(--danger)', fontSize: 'var(--text-lg)' }}>×</button>
              </div>
            ))}
            <button onClick={clearCart} className="btn btn-ghost btn-sm" style={{ alignSelf: 'flex-start', color: 'var(--danger)' }}>
              🗑️ Clear Cart
            </button>
          </div>

          {/* Order Summary */}
          <div className="glass-card" style={{ padding: 'var(--space-6)', position: 'sticky', top: 'calc(var(--navbar-height) + var(--space-4))' }}>
            <h3 style={{ fontSize: 'var(--text-lg)', fontWeight: 600, marginBottom: 'var(--space-6)' }}>Order Summary</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-3)', marginBottom: 'var(--space-6)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)', fontSize: 'var(--text-sm)' }}>
                <span>Subtotal ({cart.item_count} items)</span>
                <span>{formatPrice(cart.total)}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)', fontSize: 'var(--text-sm)' }}>
                <span>Tax (8%)</span>
                <span>{formatPrice(cart.total * 0.08)}</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-secondary)', fontSize: 'var(--text-sm)' }}>
                <span>Shipping</span>
                <span style={{ color: 'var(--success)' }}>Free</span>
              </div>
              <div style={{ borderTop: '1px solid var(--border-default)', paddingTop: 'var(--space-3)', display: 'flex', justifyContent: 'space-between', fontWeight: 700, fontSize: 'var(--text-lg)' }}>
                <span>Total</span>
                <span style={{ fontFamily: 'var(--font-mono)' }}>{formatPrice(cart.total * 1.08)}</span>
              </div>
            </div>
            <button onClick={handleCheckout} className="btn btn-primary btn-lg" style={{ width: '100%' }}>
              Checkout →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
