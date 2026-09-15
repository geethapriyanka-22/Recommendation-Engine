import { useState, useEffect, useRef } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useCart } from '../../context/CartContext';
import { useTheme } from '../../context/ThemeContext';
import { trackSearch, getWishlistIds } from '../../services/activityTracker';

const NAV_CATEGORIES = [
  { name: 'All Departments', path: '/products' },
  { name: 'Electronics', path: '/products?category=electronics' },
  { name: 'Fashion & Apparel', path: '/products?category=fashion' },
  { name: 'Home & Kitchen', path: '/products?category=home-kitchen' },
  { name: 'Beauty & Luxury', path: '/products?category=beauty' },
  { name: 'Sports & Outdoors', path: '/products?category=sports-outdoors' },
];

export default function Navbar() {
  const { user, logout, isAdmin } = useAuth();
  const { cart } = useCart();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const [searchQuery, setSearchQuery] = useState('');
  const [showSearch, setShowSearch] = useState(false);
  const [showCatMenu, setShowCatMenu] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [wishlistCount, setWishlistCount] = useState(() => getWishlistIds().length);
  const searchInputRef = useRef(null);

  // Keep wishlist count synced across windows & components
  useEffect(() => {
    const handleActivityChange = () => {
      setWishlistCount(getWishlistIds().length);
    };
    window.addEventListener('novamart_activity_updated', handleActivityChange);
    return () => window.removeEventListener('novamart_activity_updated', handleActivityChange);
  }, []);

  // Sync search input with URL
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const q = params.get('q') || '';
    setSearchQuery(q);
    if (q) setShowSearch(true);
  }, [location.search]);

  useEffect(() => {
    if (showSearch && searchInputRef.current) {
      searchInputRef.current.focus();
    }
  }, [showSearch]);

  const handleSearch = (e) => {
    e.preventDefault();
    const query = searchQuery.trim();
    if (query) {
      trackSearch(query);
      navigate(`/products?q=${encodeURIComponent(query)}`);
    } else {
      navigate('/products');
    }
  };

  const isActive = (path) => {
    if (path === '/products' && location.pathname === '/products' && !location.search) return true;
    return location.pathname + location.search === path;
  };

  return (
    <nav className="navbar">
      <div className="nav-content">
        {/* ─── BRAND LOGO ────────────────────────────────────────── */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-8)' }}>
          <Link to="/" className="nav-logo">
            NOVAMART<span className="nav-logo-dot"></span>
          </Link>

          {/* ─── CENTER NAVIGATION: Categories, New Arrivals, Deals ─ */}
          <div className="nav-links">
            {/* Categories Dropdown */}
            <div
              style={{ position: 'relative' }}
              onMouseEnter={() => setShowCatMenu(true)}
              onMouseLeave={() => setShowCatMenu(false)}
            >
              <Link
                to="/products"
                className={`nav-link-item ${location.pathname === '/products' && !location.search.includes('sort_by') ? 'active' : ''}`}
                style={{ display: 'flex', alignItems: 'center', gap: '4px' }}
              >
                Categories
                <span style={{ fontSize: '9px', opacity: 0.7 }}>▼</span>
              </Link>

              {showCatMenu && (
                <div
                  className="animate-fade-slide-down"
                  style={{
                    position: 'absolute',
                    top: '100%',
                    left: 0,
                    paddingTop: '8px',
                    zIndex: 200,
                  }}
                >
                  <div style={{
                    background: 'var(--bg-card)',
                    border: '1px solid var(--border-default)',
                    borderRadius: 'var(--radius-md)',
                    boxShadow: 'var(--shadow-lg)',
                    minWidth: '220px',
                    padding: 'var(--space-2) 0',
                  }}>
                    {NAV_CATEGORIES.map((c) => (
                      <Link
                        key={c.name}
                        to={c.path}
                        onClick={() => setShowCatMenu(false)}
                        style={{
                          display: 'block',
                          padding: 'var(--space-2) var(--space-4)',
                          fontSize: '0.8125rem',
                          fontWeight: 500,
                          color: 'var(--text-primary)',
                          transition: 'background 0.15s ease',
                        }}
                        onMouseEnter={(e) => { e.currentTarget.style.background = 'var(--bg-tertiary)'; }}
                        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
                      >
                        {c.name}
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <Link
              to="/products?sort_by=created_at"
              className={`nav-link-item ${location.search.includes('sort_by=created_at') ? 'active' : ''}`}
            >
              New Arrivals
            </Link>

            <Link
              to="/products?sort_by=rating"
              className={`nav-link-item ${location.search.includes('sort_by=rating') ? 'active' : ''}`}
            >
              Deals
            </Link>

            <Link
              to="/ai-studio"
              className={`nav-link-item ${location.pathname === '/ai-studio' ? 'active' : ''}`}
              style={{ color: 'var(--accent-primary)', display: 'flex', alignItems: 'center', gap: '4px' }}
            >
              <span>✦</span> AI Studio
            </Link>
          </div>
        </div>

        {/* ─── RIGHT ACTION ICONS: 🔍  🛒  👤 ──────────────────── */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
          {/* Search Bar / Expandable */}
          {showSearch ? (
            <form onSubmit={handleSearch} style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
              <input
                ref={searchInputRef}
                type="text"
                placeholder="Search catalog..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{
                  width: '240px',
                  padding: '6px 28px 6px 12px',
                  fontSize: '0.8125rem',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-default)',
                  background: 'var(--bg-secondary)',
                  color: 'var(--text-primary)',
                }}
              />
              <button
                type="button"
                onClick={() => {
                  if (searchQuery) {
                    setSearchQuery('');
                    if (location.pathname === '/products') {
                      navigate('/products');
                    }
                  } else {
                    setShowSearch(false);
                  }
                }}
                style={{
                  position: 'absolute',
                  right: '8px',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  color: 'var(--text-muted)',
                  fontSize: '12px',
                }}
              >
                ✕
              </button>
            </form>
          ) : (
            <button
              className="nav-btn"
              onClick={() => setShowSearch(true)}
              title="Search products"
              style={{ fontSize: '1.1rem' }}
            >
              🔍
            </button>
          )}

          {/* Theme Toggle (Subtle) */}
          <button
            className="nav-btn"
            onClick={toggleTheme}
            title={theme === 'dark' ? 'Light Theme' : 'Nocturnal Theme'}
            style={{ fontSize: '1.05rem' }}
          >
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>

          {/* Wishlist Icon */}
          <button
            className="nav-btn"
            onClick={() => navigate('/products')}
            title={`Wishlist (${wishlistCount})`}
            style={{ fontSize: '1.2rem', position: 'relative' }}
          >
            ♡
            {wishlistCount > 0 && (
              <span className="cart-badge" style={{ background: '#ef4444' }}>{wishlistCount}</span>
            )}
          </button>

          {/* Cart Icon */}
          <button
            className="nav-btn"
            onClick={() => navigate('/cart')}
            title="Bag"
            style={{ fontSize: '1.2rem', position: 'relative' }}
          >
            🛍️
            {cart.item_count > 0 && (
              <span className="cart-badge">{cart.item_count}</span>
            )}
          </button>

          {/* User Profile or Sign In */}
          {user ? (
            <div style={{ position: 'relative' }}>
              <button
                className="nav-btn"
                onClick={() => setShowUserMenu(!showUserMenu)}
                title={user.full_name}
                style={{ fontSize: '1.15rem' }}
              >
                👤
              </button>
              {showUserMenu && (
                <div
                  className="animate-fade-slide-down"
                  style={{
                    position: 'absolute',
                    right: 0,
                    top: '100%',
                    marginTop: '8px',
                    background: 'var(--bg-card)',
                    border: '1px solid var(--border-default)',
                    borderRadius: 'var(--radius-md)',
                    padding: 'var(--space-3) 0',
                    minWidth: '210px',
                    boxShadow: 'var(--shadow-lg)',
                    zIndex: 200,
                  }}
                >
                  <div style={{
                    padding: '0 var(--space-4) var(--space-3)',
                    borderBottom: '1px solid var(--border-subtle)',
                    marginBottom: 'var(--space-2)',
                  }}>
                    <div style={{ fontWeight: 600, fontSize: 'var(--text-sm)' }}>{user.full_name}</div>
                    <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)' }}>{user.email}</div>
                  </div>
                  <Link to="/orders" onClick={() => setShowUserMenu(false)} style={{
                    display: 'block', padding: 'var(--space-2) var(--space-4)',
                    fontSize: 'var(--text-sm)', color: 'var(--text-secondary)',
                  }}>My Orders</Link>
                  {isAdmin && (
                    <Link to="/admin" onClick={() => setShowUserMenu(false)} style={{
                      display: 'block', padding: 'var(--space-2) var(--space-4)',
                      fontSize: 'var(--text-sm)', color: 'var(--text-secondary)',
                    }}>Admin Dashboard</Link>
                  )}
                  <button onClick={() => { logout(); setShowUserMenu(false); navigate('/'); }} style={{
                    display: 'block', width: '100%', textAlign: 'left',
                    padding: 'var(--space-2) var(--space-4)',
                    fontSize: 'var(--text-sm)', color: 'var(--danger)', marginTop: 'var(--space-1)',
                  }}>Sign Out</button>
                </div>
              )}
            </div>
          ) : (
            <Link
              to="/login"
              className="btn btn-primary btn-sm"
              style={{ padding: '6px 14px', fontSize: '0.75rem', letterSpacing: '0.06em', textTransform: 'uppercase' }}
            >
              Sign In
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
}
