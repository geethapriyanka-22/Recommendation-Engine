import { Link } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import { trackProductInteraction } from '../../services/activityTracker';

export default function ProductCard({ product }) {
  const { addToCart } = useCart();
  const { user } = useAuth();

  const discount = product.compare_at_price
    ? Math.round((1 - product.price / product.compare_at_price) * 100)
    : null;

  const imageUrl = product.images?.[0]?.url || `https://picsum.photos/seed/${product.id}/640/480`;

  const handleAddToCart = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!user) {
      window.location.href = '/login';
      return;
    }
    try {
      await addToCart(product.id, 1);
      trackProductInteraction('cart', product.id);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to add to cart');
    }
  };

  const renderStars = (rating) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span key={i} className={`star ${i <= Math.round(rating) ? 'filled' : ''}`}>★</span>
      );
    }
    return stars;
  };

  return (
    <Link to={`/products/${product.slug || product.id}`} className="product-card">
      <div className="card-image">
        <img src={imageUrl} alt={product.title} loading="lazy" />
        {discount && <span className="discount-badge">-{discount}%</span>}
        {product.stock_quantity === 0 && (
          <div style={{
            position: 'absolute', inset: 0,
            background: 'rgba(0,0,0,0.6)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            color: 'white', fontWeight: 700, fontSize: 'var(--text-sm)',
          }}>
            OUT OF STOCK
          </div>
        )}
      </div>
      <div className="card-body">
        {product.brand && <span className="card-brand">{product.brand}</span>}
        <h3 className="card-title">{product.title}</h3>
        <div className="star-rating">
          {renderStars(product.avg_rating)}
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', marginLeft: '4px' }}>
            ({product.review_count})
          </span>
        </div>
        <div className="card-price">
          <span className="price-current">${product.price.toFixed(2)}</span>
          {product.compare_at_price && (
            <span className="price-compare">${product.compare_at_price.toFixed(2)}</span>
          )}
        </div>
      </div>
      <div className="card-actions" style={{ marginTop: 'auto', paddingTop: 'var(--space-2)' }}>
        <button
          className="btn btn-secondary btn-sm"
          style={{ width: '100%', fontSize: '0.75rem', fontWeight: 600, letterSpacing: '0.04em', textTransform: 'uppercase' }}
          onClick={handleAddToCart}
          disabled={product.stock_quantity === 0}
        >
          {product.stock_quantity === 0 ? 'Sold Out' : '+ Add to Bag'}
        </button>
      </div>
    </Link>
  );
}
