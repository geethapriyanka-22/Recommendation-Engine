import { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import ProductCard from '../components/products/ProductCard';
import {
  getInteractionPayload,
  getRecentSearchesPayload,
  getRecentlyViewedIds,
  clearRecentlyViewed,
} from '../services/activityTracker';

export default function HomePage() {
  const [recommended, setRecommended] = useState([]);
  const [recReason, setRecReason] = useState('');
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [newArrivals, setNewArrivals] = useState([]);
  const [recentlyViewed, setRecentlyViewed] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchPersonalizedData = useCallback(async () => {
    try {
      const interactionIds = getInteractionPayload();
      const searchQueries = getRecentSearchesPayload();
      const recRes = await api.get('/ai/personalized-recommendations', {
        params: {
          product_ids: interactionIds.length > 0 ? interactionIds.join(',') : undefined,
          search_queries: searchQueries.length > 0 ? searchQueries.join(',') : undefined,
          limit: 4,
        },
      });
      setRecommended(recRes.data.items || []);
      setRecReason(recRes.data.reason || '');
      setIsPersonalized(recRes.data.is_personalized || false);
    } catch (err) {
      console.error('Failed to load personalized recommendations:', err);
    }
  }, []);

  const fetchRecentlyViewed = useCallback(async () => {
    const recentIds = getRecentlyViewedIds();
    if (!recentIds || recentIds.length === 0) {
      setRecentlyViewed([]);
      return;
    }
    try {
      const productPromises = recentIds.slice(0, 6).map((id) =>
        api.get(`/products/${id}`).then((r) => r.data).catch(() => null)
      );
      const results = await Promise.all(productPromises);
      setRecentlyViewed(results.filter(Boolean));
    } catch (err) {
      console.error('Failed to load recently viewed products:', err);
    }
  }, []);

  useEffect(() => {
    const fetchInitial = async () => {
      setLoading(true);
      await Promise.all([
        fetchPersonalizedData(),
        fetchRecentlyViewed(),
        api.get('/products', { params: { limit: 4, sort_by: 'created_at' } })
          .then((res) => setNewArrivals(res.data.items || []))
          .catch(() => {}),
      ]);
      setLoading(false);
    };

    fetchInitial();

    const handleActivityChange = () => {
      fetchPersonalizedData();
      fetchRecentlyViewed();
    };

    window.addEventListener('novamart_activity_updated', handleActivityChange);
    return () => window.removeEventListener('novamart_activity_updated', handleActivityChange);
  }, [fetchPersonalizedData, fetchRecentlyViewed]);

  const handleClearRecentlyViewed = () => {
    clearRecentlyViewed();
    setRecentlyViewed([]);
  };

  return (
    <div style={{ background: 'var(--bg-primary)', minHeight: '100vh' }}>
      {/* ─── 1. HERO SECTION ────────────────────────────────────────── */}
      <section style={{
        padding: 'clamp(var(--space-10), 6vw, var(--space-20)) var(--space-6)',
        maxWidth: 'var(--max-width)',
        margin: '0 auto',
      }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          gap: 'var(--space-12)',
          alignItems: 'center',
        }}>
          {/* Hero Left Content */}
          <div style={{ maxWidth: '580px' }}>
            <span style={{
              display: 'inline-block',
              fontSize: '0.75rem',
              fontWeight: 700,
              letterSpacing: '0.14em',
              textTransform: 'uppercase',
              color: 'var(--accent-primary)',
              marginBottom: 'var(--space-4)',
            }}>
              Curated Selection • AI Powered
            </span>

            <h1 style={{
              fontSize: 'clamp(2.4rem, 5.5vw, 4rem)',
              fontWeight: 500,
              lineHeight: 1.12,
              letterSpacing: '-0.02em',
              color: 'var(--text-primary)',
              margin: '0 0 var(--space-5) 0',
              fontFamily: 'var(--font-serif)',
            }}>
              Discover products made for you.
            </h1>

            <p style={{
              fontSize: 'clamp(1rem, 1.8vw, 1.15rem)',
              color: 'var(--text-secondary)',
              lineHeight: 1.65,
              marginBottom: 'var(--space-8)',
              fontWeight: 400,
              maxWidth: '480px',
            }}>
              Personalized shopping, powered by AI. Thoughtfully sourced essentials from iconic houses, tailored dynamically to your taste.
            </p>

            <div style={{ display: 'flex', gap: 'var(--space-4)', flexWrap: 'wrap', alignItems: 'center' }}>
              <Link
                to="/products"
                className="btn btn-primary btn-lg"
                style={{
                  padding: '14px 32px',
                  fontSize: '0.8125rem',
                  letterSpacing: '0.08em',
                  textTransform: 'uppercase',
                  fontWeight: 600,
                }}
              >
                Explore Collection
              </Link>
              <Link
                to="/ai-studio"
                className="btn btn-secondary btn-lg"
                style={{
                  padding: '14px 28px',
                  fontSize: '0.8125rem',
                  letterSpacing: '0.06em',
                  fontWeight: 500,
                }}
              >
                Launch AI Studio →
              </Link>
            </div>
          </div>

          {/* Hero Right Visual */}
          <div style={{ position: 'relative' }}>
            <div style={{
              position: 'relative',
              borderRadius: 'var(--radius-lg)',
              overflow: 'hidden',
              boxShadow: 'var(--shadow-lg)',
              border: '1px solid var(--border-default)',
              aspectRatio: '4/3',
              background: 'var(--bg-tertiary)',
            }}>
              <img
                src="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=1200&auto=format&fit=crop&q=80"
                alt="Editorial luxury collection"
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'cover',
                  display: 'block',
                }}
              />
              <div style={{
                position: 'absolute',
                bottom: 'var(--space-4)',
                left: 'var(--space-4)',
                background: 'var(--card-overlay-bg)',
                backdropFilter: 'blur(8px)',
                padding: 'var(--space-3) var(--space-4)',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-default)',
              }}>
                <span style={{ fontSize: '0.6875rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--accent-primary)', fontWeight: 700, display: 'block' }}>
                  The Edit
                </span>
                <span style={{ fontSize: '0.875rem', fontWeight: 600, color: 'var(--text-primary)', fontFamily: 'var(--font-serif)' }}>
                  Autumn / Winter Essentials
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ─── 2. ASSURANCE STRIP (LIKE LUNA BOUTIQUE) ──────────────── */}
      <section style={{
        borderTop: '1px solid var(--border-default)',
        borderBottom: '1px solid var(--border-default)',
        background: 'var(--bg-secondary)',
        padding: 'var(--space-6) var(--space-6)',
      }}>
        <div style={{
          maxWidth: 'var(--max-width)',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: 'var(--space-6)',
        }}>
          {[
            { icon: '🚚', title: 'Complimentary Delivery', desc: 'On all orders over ₹1,500' },
            { icon: '✦', title: 'Curated Excellence', desc: '100% authentic designer heritage' },
            { icon: '🧠', title: 'AI Recommendation', desc: 'Intelligent semantic matching' },
            { icon: '🔒', title: 'Secure Checkout', desc: 'Encrypted & protected payments' },
          ].map((item, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
              <span style={{ fontSize: '1.4rem' }}>{item.icon}</span>
              <div>
                <div style={{ fontSize: '0.8125rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-primary)' }}>
                  {item.title}
                </div>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                  {item.desc}
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* ─── 3. RECOMMENDED FOR YOU (CORE REQUEST) ───────────────── */}
      <section style={{
        padding: 'clamp(var(--space-12), 6vw, var(--space-16)) var(--space-6)',
        maxWidth: 'var(--max-width)',
        margin: '0 auto',
      }}>
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-end',
          marginBottom: 'var(--space-8)',
          flexWrap: 'wrap',
          gap: 'var(--space-4)',
        }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)', marginBottom: 'var(--space-2)' }}>
              <h2 style={{
                fontSize: 'clamp(1.75rem, 3vw, 2.25rem)',
                fontFamily: 'var(--font-serif)',
                fontWeight: 500,
                color: 'var(--text-primary)',
                margin: 0,
              }}>
                Recommended for you
              </h2>
              {isPersonalized && (
                <span className="badge badge-accent" style={{ fontSize: '0.6875rem', letterSpacing: '0.06em' }}>
                  ✦ Tailored For You
                </span>
              )}
            </div>
            <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', margin: 0 }}>
              {recReason ? `${recReason} — tailored by our neural ranking engine.` : 'Curated by our neural ranking engine based on quality, ratings, and timeless appeal.'}
            </p>
          </div>
          <Link
            to="/products?sort_by=rating"
            style={{
              fontSize: '0.8125rem',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.08em',
              color: 'var(--text-primary)',
              borderBottom: '1px solid var(--text-primary)',
              paddingBottom: '2px',
            }}
          >
            View All →
          </Link>
        </div>

        {/* 4-Product Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))',
          gap: 'var(--space-6)',
        }}>
          {recommended.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      {/* ─── 3.5 RECENTLY VIEWED (DYNAMIC SESSION HISTORY) ─────────── */}
      {recentlyViewed.length > 0 && (
        <section style={{
          padding: '0 var(--space-6) clamp(var(--space-10), 5vw, var(--space-14))',
          maxWidth: 'var(--max-width)',
          margin: '0 auto',
        }}>
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'flex-end',
            marginBottom: 'var(--space-6)',
            flexWrap: 'wrap',
            gap: 'var(--space-3)',
            borderTop: '1px solid var(--border-default)',
            paddingTop: 'var(--space-8)',
          }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-3)' }}>
                <h2 style={{
                  fontSize: 'clamp(1.5rem, 2.5vw, 1.85rem)',
                  fontFamily: 'var(--font-serif)',
                  fontWeight: 500,
                  color: 'var(--text-primary)',
                  margin: 0,
                }}>
                  Recently Viewed
                </h2>
                <span className="badge badge-secondary" style={{ fontSize: '0.6875rem' }}>
                  {recentlyViewed.length} item{recentlyViewed.length > 1 ? 's' : ''}
                </span>
              </div>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', margin: 'var(--space-1) 0 0' }}>
                Items you recently explored in your browsing session.
              </p>
            </div>
            <button
              onClick={handleClearRecentlyViewed}
              className="btn btn-ghost"
              style={{
                fontSize: '0.75rem',
                color: 'var(--text-muted)',
                letterSpacing: '0.04em',
                textTransform: 'uppercase',
                padding: 'var(--space-1) var(--space-3)',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-sm)',
              }}
              title="Clear browsing history"
            >
              Clear History
            </button>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))',
            gap: 'var(--space-5)',
          }}>
            {recentlyViewed.map((product) => (
              <ProductCard key={`recent-${product.id}`} product={product} />
            ))}
          </div>
        </section>
      )}

      {/* ─── 4. CURATED DEPARTMENTS / CATEGORIES ──────────────────── */}
      <section style={{
        padding: 'var(--space-12) var(--space-6)',
        maxWidth: 'var(--max-width)',
        margin: '0 auto',
        borderTop: '1px solid var(--border-default)',
      }}>
        <div style={{ textAlign: 'center', marginBottom: 'var(--space-10)' }}>
          <span style={{
            fontSize: '0.75rem',
            fontWeight: 700,
            textTransform: 'uppercase',
            letterSpacing: '0.14em',
            color: 'var(--accent-primary)',
          }}>
            Departments
          </span>
          <h2 style={{
            fontFamily: 'var(--font-serif)',
            fontSize: 'clamp(1.75rem, 3vw, 2.25rem)',
            fontWeight: 500,
            color: 'var(--text-primary)',
            margin: 'var(--space-2) 0 0',
          }}>
            Curated Categories
          </h2>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
          gap: 'var(--space-5)',
        }}>
          {[
            {
              name: 'Electronics',
              slug: 'electronics',
              image: 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&auto=format&fit=crop&q=80',
              brands: 'Apple • Sony • Bose',
            },
            {
              name: 'Fashion & Apparel',
              slug: 'fashion',
              image: 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&auto=format&fit=crop&q=80',
              brands: "Nike • Patagonia • Levi's",
            },
            {
              name: 'Home & Kitchen',
              slug: 'home-kitchen',
              image: 'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=600&auto=format&fit=crop&q=80',
              brands: 'Dyson • Le Creuset • Vitamix',
            },
            {
              name: 'Beauty & Luxury',
              slug: 'beauty',
              image: 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=600&auto=format&fit=crop&q=80',
              brands: 'Dior • La Mer • Aesop',
            },
            {
              name: 'Sports & Outdoors',
              slug: 'sports-outdoors',
              image: 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=600&auto=format&fit=crop&q=80',
              brands: 'Garmin • Yeti • Arc\'teryx',
            },
          ].map((cat) => (
            <Link
              key={cat.slug}
              to={`/products?category=${cat.slug}`}
              style={{
                background: 'var(--bg-card)',
                borderRadius: 'var(--radius-md)',
                overflow: 'hidden',
                border: '1px solid var(--border-default)',
                textDecoration: 'none',
                transition: 'all var(--duration-base) var(--ease-out)',
                display: 'flex',
                flexDirection: 'column',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.borderColor = 'var(--border-hover)';
                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.borderColor = 'var(--border-default)';
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              <div style={{ aspectRatio: '1/1', overflow: 'hidden', background: 'var(--bg-tertiary)' }}>
                <img
                  src={cat.image}
                  alt={cat.name}
                  style={{ width: '100%', height: '100%', objectFit: 'cover', transition: 'transform 0.4s ease' }}
                />
              </div>
              <div style={{ padding: 'var(--space-4)', textAlign: 'center' }}>
                <h3 style={{
                  fontFamily: 'var(--font-serif)',
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  color: 'var(--text-primary)',
                  margin: '0 0 var(--space-1) 0',
                }}>
                  {cat.name}
                </h3>
                <span style={{ fontSize: '0.6875rem', textTransform: 'uppercase', letterSpacing: '0.08em', color: 'var(--text-secondary)' }}>
                  {cat.brands}
                </span>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* ─── 5. EDITORIAL FEATURE (VESPERA / QUIET LUXURY STYLE) ──── */}
      <section style={{
        maxWidth: 'var(--max-width)',
        margin: '0 auto var(--space-16)',
        padding: '0 var(--space-6)',
      }}>
        <div style={{
          background: 'var(--bg-card)',
          border: '1px solid var(--border-default)',
          borderRadius: 'var(--radius-lg)',
          overflow: 'hidden',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))',
          alignItems: 'center',
        }}>
          <div style={{ padding: 'clamp(var(--space-8), 5vw, var(--space-16))' }}>
            <span style={{
              fontSize: '0.75rem',
              fontWeight: 700,
              letterSpacing: '0.14em',
              textTransform: 'uppercase',
              color: 'var(--accent-primary)',
              display: 'block',
              marginBottom: 'var(--space-3)',
            }}>
              The Art of Quiet Luxury
            </span>
            <h2 style={{
              fontFamily: 'var(--font-serif)',
              fontSize: 'clamp(1.75rem, 3.5vw, 2.5rem)',
              fontWeight: 500,
              color: 'var(--text-primary)',
              lineHeight: 1.2,
              marginBottom: 'var(--space-4)',
            }}>
              Designed for longevity. Engineered for elegance.
            </h2>
            <p style={{
              fontSize: '0.9375rem',
              color: 'var(--text-secondary)',
              lineHeight: 1.65,
              marginBottom: 'var(--space-6)',
            }}>
              From Apple M3 Max silicon to Burberry tailored outerwear and handcrafted Le Creuset cast iron, each item is selected to transcend fleeting trends.
            </p>
            <Link
              to="/products?category=fashion"
              className="btn btn-primary"
              style={{ padding: '12px 28px', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.75rem', fontWeight: 600 }}
            >
              Explore Apparel & Design
            </Link>
          </div>
          <div style={{ height: '100%', minHeight: '340px' }}>
            <img
              src="https://images.unsplash.com/photo-1509631179647-0177331693ae?w=1000&auto=format&fit=crop&q=80"
              alt="Quiet luxury tailoring"
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
            />
          </div>
        </div>
      </section>

      {/* ─── 6. NEWSLETTER / CIRCLE STRIP ────────────────────────── */}
      <section style={{
        background: 'var(--bg-secondary)',
        borderTop: '1px solid var(--border-default)',
        padding: 'var(--space-12) var(--space-6)',
      }}>
        <div style={{
          maxWidth: '560px',
          margin: '0 auto',
          textAlign: 'center',
        }}>
          <h3 style={{
            fontFamily: 'var(--font-serif)',
            fontSize: '1.5rem',
            fontWeight: 500,
            color: 'var(--text-primary)',
            marginBottom: 'var(--space-2)',
          }}>
            Join the NovaMart Circle
          </h3>
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: 'var(--space-6)', lineHeight: 1.6 }}>
            Receive private exhibition invitations, early access to limited capsule releases, and AI-personalized curation edits.
          </p>
          <form
            onSubmit={(e) => { e.preventDefault(); alert('Thank you for joining the NovaMart Circle.'); }}
            style={{ display: 'flex', gap: 'var(--space-2)' }}
          >
            <input
              type="email"
              required
              placeholder="Enter your email address"
              style={{
                flex: 1,
                padding: '12px 16px',
                fontSize: '0.875rem',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border-default)',
                background: 'var(--bg-primary)',
                color: 'var(--text-primary)',
              }}
            />
            <button
              type="submit"
              className="btn btn-primary"
              style={{ padding: '12px 24px', textTransform: 'uppercase', letterSpacing: '0.06em', fontSize: '0.75rem', fontWeight: 600 }}
            >
              Subscribe
            </button>
          </form>
        </div>
      </section>
    </div>
  );
}
