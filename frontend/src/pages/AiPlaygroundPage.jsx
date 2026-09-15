import { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { formatPrice } from '../utils/currency';

const PRESET_QUERIES = [
  'ergonomic workspace accessories for back pain',
  'high fidelity wireless audio gear with rich bass',
  'minimalist travel bag durable for rainy weather',
  'smart home lighting for circadian rhythm focus',
  'sustainable kitchen appliances energy efficient'
];

export default function AiPlaygroundPage() {
  const [query, setQuery] = useState(PRESET_QUERIES[0]);
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const runSemanticSearch = async (searchTerm) => {
    const q = searchTerm || query;
    if (!q.trim()) return;

    setLoading(true);
    setHasSearched(true);
    try {
      const { data } = await api.get(`/ai/semantic-search`, {
        params: { q, limit: 8 }
      });
      setResults(data.results || []);
    } catch (err) {
      console.error(err);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ padding: 'var(--space-8) var(--space-4)' }}>
      {/* Header */}
      <div style={{ textAlign: 'center', maxWidth: '760px', margin: '0 auto var(--space-8)' }}>
        <span className="badge badge-primary" style={{ marginBottom: 'var(--space-3)' }}>
          🧠 pgvector + Local Embedding Engine
        </span>
        <h1 style={{ fontSize: 'var(--text-4xl)', fontWeight: 800, margin: 'var(--space-2) 0 var(--space-3)' }}>
          AI Semantic Search & Similarity Studio
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: 'var(--text-base)' }}>
          Experience multi-modal vector search powered by local sentence embeddings,
          PostgreSQL <code style={{ color: 'var(--accent-primary)' }}>pgvector</code>, and our weighted hybrid ranking formula.
        </p>
      </div>

      {/* Algorithm Architecture Banner */}
      <div className="glass-card" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)', border: '1px solid var(--border-hover)' }}>
        <h3 style={{ fontSize: 'var(--text-sm)', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)', marginBottom: 'var(--space-3)' }}>
          ⚙️ Hybrid Relevance Scoring Formula
        </h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 'var(--space-4)' }}>
          <div style={{ padding: 'var(--space-3)', background: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)' }}>
            <div style={{ fontWeight: 700, color: 'var(--accent-primary)', fontSize: 'var(--text-lg)' }}>60% Weight</div>
            <div style={{ fontWeight: 600, fontSize: 'var(--text-sm)' }}>Vector Cosine Similarity</div>
            <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>Semantic meaning in dense vector space</div>
          </div>
          <div style={{ padding: 'var(--space-3)', background: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)' }}>
            <div style={{ fontWeight: 700, color: '#60a5fa', fontSize: 'var(--text-lg)' }}>25% Weight</div>
            <div style={{ fontWeight: 600, fontSize: 'var(--text-sm)' }}>PostgreSQL FTS (ts_rank)</div>
            <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>Keyword lexical exact match precision</div>
          </div>
          <div style={{ padding: 'var(--space-3)', background: 'var(--bg-tertiary)', borderRadius: 'var(--radius-md)' }}>
            <div style={{ fontWeight: 700, color: '#34d399', fontSize: 'var(--text-lg)' }}>15% Weight</div>
            <div style={{ fontWeight: 600, fontSize: 'var(--text-sm)' }}>Popularity & Rating Prior</div>
            <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>Customer review density and star rating</div>
          </div>
        </div>
      </div>

      {/* Search Bar & Presets */}
      <div className="glass-card" style={{ padding: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
        <form onSubmit={(e) => { e.preventDefault(); runSemanticSearch(); }}>
          <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Type conceptual queries (e.g. 'comfortable desk chair for long coding sessions')..."
              style={{ flex: 1, padding: 'var(--space-4)', fontSize: 'var(--text-base)' }}
            />
            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
              style={{ padding: 'var(--space-4) var(--space-8)', fontSize: 'var(--text-base)' }}
            >
              {loading ? 'Embedding...' : 'Vector Search'}
            </button>
          </div>
        </form>

        <div style={{ marginTop: 'var(--space-4)', display: 'flex', flexWrap: 'wrap', alignItems: 'center', gap: 'var(--space-2)' }}>
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)', fontWeight: 600 }}>Try queries:</span>
          {PRESET_QUERIES.map((pq, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => { setQuery(pq); runSemanticSearch(pq); }}
              className="btn btn-secondary btn-sm"
              style={{ fontSize: 'var(--text-xs)' }}
            >
              {pq}
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      {loading && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 'var(--space-6)' }}>
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="skeleton" style={{ height: '340px', borderRadius: 'var(--radius-lg)' }} />
          ))}
        </div>
      )}

      {!loading && hasSearched && results.length === 0 && (
        <div className="glass-card" style={{ padding: 'var(--space-8)', textAlign: 'center' }}>
          <span style={{ fontSize: '2.5rem', display: 'block', marginBottom: 'var(--space-2)' }}>🔍</span>
          <h3>No semantic matches found</h3>
          <p style={{ color: 'var(--text-secondary)' }}>Try broadening your search query or reindexing embeddings via the Admin page.</p>
        </div>
      )}

      {!loading && results.length > 0 && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-4)' }}>
            <h2 style={{ fontSize: 'var(--text-xl)', fontWeight: 700, margin: 0 }}>
              Semantic Matches ({results.length})
            </h2>
            <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-secondary)' }}>
              Ordered by computed hybrid cosine similarity
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 'var(--space-6)' }}>
            {results.map((product) => {
              const relevancePercent = Math.min(100, Math.round((product.relevance_score || 0.85) * 100));
              return (
                <div key={product.id} className="glass-card" style={{ overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
                  <div style={{ position: 'relative', height: '180px', overflow: 'hidden' }}>
                    <img
                      src={product.image_url || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400'}
                      alt={product.title}
                      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                    <div style={{
                      position: 'absolute',
                      top: 'var(--space-2)',
                      right: 'var(--space-2)',
                      background: 'rgba(0, 0, 0, 0.75)',
                      backdropFilter: 'blur(4px)',
                      color: 'white',
                      padding: 'var(--space-1) var(--space-2)',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: 'var(--text-xs)',
                      fontWeight: 700,
                      border: '1px solid rgba(255, 255, 255, 0.1)'
                    }}>
                      ⚡ {relevancePercent}% Match
                    </div>
                  </div>

                  <div style={{ padding: 'var(--space-4)', flex: 1, display: 'flex', flexDirection: 'column' }}>
                    <div style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                      {product.brand || 'NovaMart'}
                    </div>
                    <Link
                      to={`/products/${product.slug || product.id}`}
                      style={{
                        fontSize: 'var(--text-base)',
                        fontWeight: 700,
                        margin: 'var(--space-1) 0 var(--space-2)',
                        color: 'var(--text-primary)',
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden'
                      }}
                    >
                      {product.title}
                    </Link>

                    {product.short_description && (
                      <p style={{
                        fontSize: 'var(--text-xs)',
                        color: 'var(--text-secondary)',
                        margin: '0 0 var(--space-3)',
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden'
                      }}>
                        {product.short_description}
                      </p>
                    )}

                    {/* Similarity score meter */}
                    <div style={{ marginTop: 'auto', paddingTop: 'var(--space-3)', borderTop: '1px solid var(--border-default)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 'var(--text-xs)', marginBottom: 'var(--space-1)' }}>
                        <span style={{ color: 'var(--text-secondary)' }}>Relevance Score:</span>
                        <strong style={{ color: 'var(--accent-primary)' }}>{product.relevance_score?.toFixed(4)}</strong>
                      </div>
                      <div style={{ width: '100%', height: '4px', background: 'var(--bg-secondary)', borderRadius: '2px', overflow: 'hidden' }}>
                        <div style={{ width: `${relevancePercent}%`, height: '100%', background: 'var(--accent-gradient)' }} />
                      </div>

                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'var(--space-3)' }}>
                        <strong style={{ fontSize: 'var(--text-lg)', color: 'var(--accent-primary)' }}>
                          {formatPrice(product.price)}
                        </strong>
                        <Link to={`/products/${product.slug || product.id}`} className="btn btn-secondary btn-sm">
                          View Details
                        </Link>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
