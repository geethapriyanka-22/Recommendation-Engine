import { Link } from 'react-router-dom';

export default function Footer() {
  return (
    <footer style={{
      background: 'var(--bg-primary)',
      borderTop: '1px solid var(--border-default)',
      padding: 'var(--space-16) 0 var(--space-8)',
    }}>
      <div style={{
        maxWidth: 'var(--max-width)',
        margin: '0 auto',
        padding: '0 var(--space-8)',
      }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: 'var(--space-10)',
          marginBottom: 'var(--space-12)',
        }}>
          {/* Brand Column */}
          <div style={{ gridColumn: 'span 1' }}>
            <div style={{
              fontFamily: 'var(--font-serif)',
              fontSize: '1.25rem',
              fontWeight: 700,
              letterSpacing: '0.14em',
              textTransform: 'uppercase',
              color: 'var(--text-primary)',
              marginBottom: 'var(--space-3)',
            }}>
              NOVAMART<span style={{ color: 'var(--accent-primary)' }}>•</span>
            </div>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem', lineHeight: 1.7, maxWidth: '280px' }}>
              The quiet luxury e-commerce platform curated by neural vector search and authentic brand heritage.
            </p>
          </div>

          {/* Shop Column */}
          <div>
            <h4 style={{
              fontSize: '0.75rem',
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              color: 'var(--text-primary)',
              marginBottom: 'var(--space-4)',
            }}>
              Collections
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
              <Link to="/products" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>Full Catalog</Link>
              <Link to="/products?category=electronics" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>Electronics & Audio</Link>
              <Link to="/products?category=fashion" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>Fashion & Tailoring</Link>
              <Link to="/products?category=home-kitchen" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>Home & Kitchen</Link>
              <Link to="/products?category=beauty" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>Beauty & Fragrance</Link>
            </div>
          </div>

          {/* Experience Column */}
          <div>
            <h4 style={{
              fontSize: '0.75rem',
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              color: 'var(--text-primary)',
              marginBottom: 'var(--space-4)',
            }}>
              Experience
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
              <Link to="/ai-studio" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>✦ AI Studio & Concierge</Link>
              <Link to="/products?sort_by=rating" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>Top Curations</Link>
              <Link to="/products?sort_by=created_at" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>New Arrivals</Link>
              <Link to="/cart" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>Shopping Bag</Link>
            </div>
          </div>

          {/* Client Service */}
          <div>
            <h4 style={{
              fontSize: '0.75rem',
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              color: 'var(--text-primary)',
              marginBottom: 'var(--space-4)',
            }}>
              Client Care
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
              <Link to="/orders" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>Orders & Tracking</Link>
              <Link to="/login" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>Client Account</Link>
              <a href="/docs" target="_blank" rel="noopener noreferrer" style={{ color: 'var(--text-secondary)', fontSize: '0.8125rem' }}>API & Architecture</a>
            </div>
          </div>
        </div>

        {/* Bottom Line */}
        <div style={{
          borderTop: '1px solid var(--border-default)',
          paddingTop: 'var(--space-6)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 'var(--space-4)',
          fontSize: '0.75rem',
          color: 'var(--text-muted)',
        }}>
          <div>© 2026 NovaMart Inc. Quiet Luxury & Intelligent Commerce.</div>
          <div style={{ display: 'flex', gap: 'var(--space-6)' }}>
            <span>Privacy Policy</span>
            <span>Terms of Service</span>
            <span>Complimentary Returns</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
