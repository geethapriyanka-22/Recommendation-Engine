import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import ProductCard from '../components/products/ProductCard';

import { trackProductInteraction, toggleWishlist, isWishlisted } from '../services/activityTracker';
import { formatPrice } from '../utils/currency';

export default function ProductDetailPage() {
  const params = useParams();
  const idOrSlug = params.slug || params.id;
  const { addToCart } = useCart();
  const { user } = useAuth();
  const [product, setProduct] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [quantity, setQuantity] = useState(1);
  const [activeImage, setActiveImage] = useState(0);
  const [wishlisted, setWishlisted] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const [justAdded, setJustAdded] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      if (!idOrSlug) return;
      setLoading(true);
      try {
        const isUUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(idOrSlug);
        const endpoint = isUUID ? `/products/${idOrSlug}` : `/products/slug/${idOrSlug}`;
        const { data } = await api.get(endpoint);
        setProduct(data);
        setWishlisted(isWishlisted(data.id));
        // Track product view for personalized home recommendations
        trackProductInteraction('view', data.id);
        // Fetch reviews
        api.get(`/products/${data.id}/reviews`).then(r => setReviews(r.data.items || [])).catch(() => {});
        // Fetch recommendations
        api.get(`/ai/recommendations/${data.id}`, { params: { limit: 4 } })
          .then(r => setRecommendations(r.data.recommendations || [])).catch(() => {});
      } catch (err) {
        console.error('Failed to load product:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [idOrSlug]);

  const handleToggleWishlist = () => {
    if (!product) return;
    const nowWishlisted = toggleWishlist(product.id);
    setWishlisted(nowWishlisted);
  };

  const handleAddToCart = async () => {
    if (!user) { window.location.href = '/login'; return; }
    if (isAdding) return;
    setIsAdding(true);
    try {
      await addToCart(product.id, quantity);
      trackProductInteraction('cart', product.id);
      setJustAdded(true);
      setTimeout(() => setJustAdded(false), 2200);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to add to cart');
    } finally {
      setIsAdding(false);
    }
  };

  if (loading || !product) {
    return (
      <div className="container" style={{ padding: 'var(--space-8) var(--space-6)' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-8)' }}>
          <div className="skeleton" style={{ aspectRatio: '1', borderRadius: 'var(--radius-xl)' }}></div>
          <div>
            <div className="skeleton skeleton-text" style={{ width: '30%' }}></div>
            <div className="skeleton" style={{ height: '2em', width: '80%', marginBottom: 'var(--space-4)' }}></div>
            <div className="skeleton skeleton-text" style={{ width: '20%' }}></div>
            <div className="skeleton" style={{ height: '100px', marginTop: 'var(--space-4)' }}></div>
          </div>
        </div>
      </div>
    );
  }

  const discount = product.compare_at_price
    ? Math.round((1 - product.price / product.compare_at_price) * 100)
    : null;

  const images = product.images?.length > 0
    ? product.images
    : [{ url: `https://picsum.photos/seed/${product.id}/800/600`, alt_text: product.title }];

  const renderStars = (rating) => Array.from({ length: 5 }, (_, i) => (
    <span key={i} className={`star ${i < Math.round(rating) ? 'filled' : ''}`}>★</span>
  ));

  return (
    <div className="container animate-fade-in" style={{ padding: 'var(--space-8) var(--space-6)' }}>
      {/* Breadcrumb */}
      <div style={{ marginBottom: 'var(--space-6)', fontSize: 'var(--text-sm)', color: 'var(--text-muted)' }}>
        <Link to="/">Home</Link> / <Link to="/catalog">Catalog</Link> / <span style={{ color: 'var(--text-secondary)' }}>{product.title}</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-10)' }}>
        {/* ─── Image Gallery ──────────────────────────────── */}
        <div>
          <div className="glass-card" style={{ overflow: 'hidden', marginBottom: 'var(--space-4)' }}>
            <img src={images[activeImage]?.url} alt={images[activeImage]?.alt_text || product.title}
              style={{ width: '100%', aspectRatio: '1', objectFit: 'cover' }} />
          </div>
          {images.length > 1 && (
            <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
              {images.map((img, i) => (
                <button key={i} onClick={() => setActiveImage(i)} style={{
                  width: 72, height: 72, borderRadius: 'var(--radius-md)', overflow: 'hidden',
                  border: i === activeImage ? '2px solid var(--accent-primary)' : '1px solid var(--border-subtle)',
                  opacity: i === activeImage ? 1 : 0.6, transition: 'all var(--duration-fast) var(--ease-out)',
                }}>
                  <img src={img.url} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* ─── Product Info ───────────────────────────────── */}
        <div>
          {product.brand && (
            <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
              {product.brand}
            </span>
          )}
          <h1 style={{ fontSize: 'var(--text-3xl)', fontWeight: 700, lineHeight: 1.2, margin: 'var(--space-2) 0 var(--space-4)' }}>
            {product.title}
          </h1>

          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', marginBottom: 'var(--space-6)' }}>
            <div className="star-rating">{renderStars(product.avg_rating)}</div>
            <span style={{ fontSize: 'var(--text-sm)', color: 'var(--text-muted)' }}>
              {product.avg_rating.toFixed(1)} ({product.review_count} reviews)
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'baseline', gap: 'var(--space-3)', marginBottom: 'var(--space-6)' }}>
            <span style={{ fontSize: 'var(--text-4xl)', fontWeight: 800, fontFamily: 'var(--font-mono)' }}>
              {formatPrice(product.price)}
            </span>
            {product.compare_at_price && (
              <>
                <span style={{ fontSize: 'var(--text-xl)', color: 'var(--text-muted)', textDecoration: 'line-through' }}>
                  {formatPrice(product.compare_at_price)}
                </span>
                <span className="badge badge-danger">-{discount}%</span>
              </>
            )}
          </div>

          <p style={{ color: 'var(--text-secondary)', lineHeight: 1.8, marginBottom: 'var(--space-6)' }}>
            {product.description}
          </p>

          {/* Attributes */}
          {Object.keys(product.attributes || {}).length > 0 && (
            <div className="glass-card" style={{ padding: 'var(--space-4)', marginBottom: 'var(--space-6)' }}>
              <h3 style={{ fontSize: 'var(--text-sm)', fontWeight: 600, marginBottom: 'var(--space-3)', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                Specifications
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 'var(--space-2)' }}>
                {Object.entries(product.attributes).map(([key, val]) => (
                  <div key={key} style={{ padding: 'var(--space-2) 0', borderBottom: '1px solid var(--border-subtle)' }}>
                    <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', textTransform: 'capitalize' }}>{key.replace(/_/g, ' ')}</span>
                    <div style={{ fontSize: 'var(--text-sm)', fontWeight: 500 }}>{val}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Stock & Add to Cart */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)', marginBottom: 'var(--space-4)' }}>
            <span className={`badge ${product.stock_quantity > 0 ? 'badge-success' : 'badge-danger'}`}>
              {product.stock_quantity > 0 ? `${product.stock_quantity} in stock` : 'Out of stock'}
            </span>
            <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
              SKU: {product.sku}
            </span>
          </div>

          {product.stock_quantity > 0 && (
            <div style={{ display: 'flex', gap: 'var(--space-3)', alignItems: 'center' }}>
              <div style={{ display: 'flex', border: '1px solid var(--border-default)', borderRadius: 'var(--radius-md)', overflow: 'hidden' }}>
                <button onClick={() => setQuantity(Math.max(1, quantity - 1))} className="btn btn-ghost" style={{ padding: 'var(--space-2) var(--space-3)' }}>−</button>
                <span style={{ padding: 'var(--space-2) var(--space-4)', fontWeight: 600, minWidth: '3rem', textAlign: 'center' }}>{quantity}</span>
                <button onClick={() => setQuantity(Math.min(product.stock_quantity, quantity + 1))} className="btn btn-ghost" style={{ padding: 'var(--space-2) var(--space-3)' }}>+</button>
              </div>
              <button
                onClick={handleAddToCart}
                disabled={isAdding}
                className="btn btn-primary btn-lg"
                style={{
                  flex: 1,
                  background: justAdded ? '#10b981' : undefined,
                  borderColor: justAdded ? '#10b981' : undefined,
                  transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)'
                }}
              >
                {justAdded ? '✓ Added to Bag!' : isAdding ? 'Adding...' : `🛒 Add to Cart — ${formatPrice(product.price * quantity)}`}
              </button>
              <button
                type="button"
                onClick={handleToggleWishlist}
                title={wishlisted ? 'Remove from Wishlist' : 'Add to Wishlist'}
                className="btn btn-ghost"
                style={{
                  padding: 'var(--space-3)',
                  border: '1px solid var(--border-default)',
                  borderRadius: 'var(--radius-md)',
                  color: wishlisted ? '#ef4444' : 'var(--text-muted)',
                  fontSize: '1.3rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  transition: 'transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)'
                }}
              >
                {wishlisted ? '♥' : '♡'}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* ─── Reviews ──────────────────────────────────────── */}
      {reviews.length > 0 && (
        <section style={{ marginTop: 'var(--space-16)' }}>
          <h2 style={{ fontSize: 'var(--text-2xl)', fontWeight: 700, marginBottom: 'var(--space-6)' }}>
            Customer Reviews ({reviews.length})
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
            {reviews.slice(0, 5).map((review) => (
              <div key={review.id} className="glass-card" style={{ padding: 'var(--space-5)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-2)' }}>
                  <div>
                    <div className="star-rating">{renderStars(review.rating)}</div>
                    <span style={{ fontSize: 'var(--text-sm)', fontWeight: 600, marginLeft: 'var(--space-2)' }}>{review.title}</span>
                  </div>
                  {review.is_verified_purchase && <span className="badge badge-success">Verified</span>}
                </div>
                <p style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', lineHeight: 1.6 }}>{review.body}</p>
                <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', marginTop: 'var(--space-2)', display: 'block' }}>
                  by {review.user_name || 'Anonymous'}
                </span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* ─── Similar Products ─────────────────────────────── */}
      {recommendations.length > 0 && (
        <section style={{ marginTop: 'var(--space-16)' }}>
          <h2 style={{ fontSize: 'var(--text-2xl)', fontWeight: 700, marginBottom: 'var(--space-6)' }}>
            💡 Similar Products
          </h2>
          <div className="product-grid stagger-grid">
            {recommendations.map((item) => (
              <ProductCard key={item.id} product={{
                ...item, stock_quantity: 1,
                images: item.image_url ? [{ url: item.image_url }] : [],
              }} />
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
