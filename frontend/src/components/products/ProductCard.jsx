import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import {
  trackProductInteraction,
  toggleWishlist,
  isWishlisted,
} from '../../services/activityTracker';
import { formatPrice } from '../../utils/currency';

export default function ProductCard({ product }) {
  const { addToCart } = useCart();
  const { user } = useAuth();
  const [wishlisted, setWishlisted] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const [justAdded, setJustAdded] = useState(false);

  useEffect(() => {
    if (product?.id) {
      setWishlisted(isWishlisted(product.id));
    }
  }, [product?.id]);

  const discount = product.compare_at_price
    ? Math.round((1 - product.price / product.compare_at_price) * 100)
    : null;

  const imageUrl = product.images?.[0]?.url || `https://picsum.photos/seed/${product.id}/640/480`;

  const handleWishlistToggle = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const updated = toggleWishlist(product.id);
    setWishlisted(updated);
  };

  const handleAddToCart = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!user) {
      window.location.href = '/login';
      return;
    }
    if (isAdding) return;

    try {
      setIsAdding(true);
      await addToCart(product.id, 1);
      trackProductInteraction('cart', product.id);
      setJustAdded(true);
      setTimeout(() => {
        setJustAdded(false);
      }, 1600);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to add to cart');
    } finally {
      setIsAdding(false);
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
      <div className="card-image" style={{ position: 'relative' }}>
        <img src={imageUrl} alt={product.title} loading="lazy" />
        {discount && <span className="discount-badge">-{discount}%</span>}

        {/* Wishlist Heart Button */}
        <button
          onClick={handleWishlistToggle}
          title={wishlisted ? "Remove from wishlist" : "Add to wishlist"}
          aria-label="Wishlist"
          style={{
            position: 'absolute',
            top: '8px',
            right: '8px',
            zIndex: 12,
            background: wishlisted ? 'rgba(239, 68, 68, 0.95)' : 'rgba(255, 255, 255, 0.85)',
            color: wishlisted ? '#ffffff' : '#1f2937',
            border: 'none',
            borderRadius: '50%',
            width: '32px',
            height: '32px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            fontSize: '14px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.18)',
            transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
          }}
        >
          {wishlisted ? '❤️' : '🤍'}
        </button>

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
          <span className="price-current">{formatPrice(product.price)}</span>
          {product.compare_at_price && (
            <span className="price-compare">{formatPrice(product.compare_at_price)}</span>
          )}
        </div>
      </div>

      <div className="card-actions" style={{ marginTop: 'auto', paddingTop: 'var(--space-2)' }}>
        <button
          className={`btn ${justAdded ? 'btn-success' : 'btn-secondary'} btn-sm`}
          style={{
            width: '100%',
            fontSize: '0.75rem',
            fontWeight: 600,
            letterSpacing: '0.04em',
            textTransform: 'uppercase',
            transition: 'all 0.2s ease',
            background: justAdded ? 'var(--success, #10b981)' : undefined,
            color: justAdded ? '#ffffff' : undefined,
            borderColor: justAdded ? 'var(--success, #10b981)' : undefined,
          }}
          onClick={handleAddToCart}
          disabled={product.stock_quantity === 0 || isAdding}
        >
          {product.stock_quantity === 0
            ? 'Sold Out'
            : isAdding
            ? 'Adding...'
            : justAdded
            ? '✓ Added to Bag'
            : '+ Add to Bag'}
        </button>
      </div>
    </Link>
  );
}
