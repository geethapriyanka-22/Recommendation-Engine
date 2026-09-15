import { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import api from '../services/api';
import ProductCard from '../components/products/ProductCard';

export default function CatalogPage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [products, setProducts] = useState([]);
  const [total, setTotal] = useState(0);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [aiMode, setAiMode] = useState(searchParams.get('ai') === 'true');
  const [aiResults, setAiResults] = useState([]);
  const [expandedCategories, setExpandedCategories] = useState({});

  const q = searchParams.get('q') || '';
  const category = searchParams.get('category') || searchParams.get('category_id') || '';
  const sortBy = searchParams.get('sort_by') || 'created_at';
  const minPrice = searchParams.get('min_price') || '';
  const maxPrice = searchParams.get('max_price') || '';
  const page = parseInt(searchParams.get('page') || '1');
  const limit = 12;

  const [searchInput, setSearchInput] = useState(q);

  useEffect(() => {
    setSearchInput(q);
  }, [q]);

  useEffect(() => {
    api.get('/categories')
      .then(res => {
        setCategories(res.data);
      })
      .catch((err) => console.error('Error fetching categories:', err));
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [q, category, sortBy, minPrice, maxPrice, page, aiMode]);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      if (aiMode && q) {
        const { data } = await api.get('/ai/semantic-search', {
          params: {
            q,
            limit: 20,
            min_price: minPrice || undefined,
            max_price: maxPrice || undefined,
            category: category || undefined,
          },
        });
        setAiResults(data.results);
        setProducts([]);
        setTotal(data.total);
      } else {
        const { data } = await api.get('/products', {
          params: {
            skip: (page - 1) * limit,
            limit,
            q: q || undefined,
            category: category || undefined,
            sort_by: sortBy,
            min_price: minPrice || undefined,
            max_price: maxPrice || undefined,
            in_stock: true,
          },
        });
        setProducts(data.items);
        setTotal(data.total);
        setAiResults([]);
      }
    } catch (err) {
      console.error('Failed to fetch products:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateParam = (key, value) => {
    const params = new URLSearchParams(searchParams);
    if (key === 'category') {
      params.delete('category_id');
    }
    if (value) {
      params.set(key, value);
    } else {
      params.delete(key);
    }
    // Only reset page to 1 when changing filters/search, not when clicking pagination
    if (key !== 'page') {
      params.delete('page');
    }
    setSearchParams(params);
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    updateParam('q', searchInput.trim());
  };

  const clearAllFilters = () => {
    setSearchParams({});
  };

  // Find active category label
  let activeCategoryName = '';
  for (const cat of categories) {
    if (cat.slug === category || cat.id === category) {
      activeCategoryName = cat.name;
      break;
    }
    if (cat.children) {
      const child = cat.children.find(c => c.slug === category || c.id === category);
      if (child) {
        activeCategoryName = `${cat.name} → ${child.name}`;
        break;
      }
    }
  }

  const toggleCategoryExpand = (catId) => {
    setExpandedCategories(prev => ({
      ...prev,
      [catId]: !prev[catId]
    }));
  };

  const displayItems = aiMode && q ? aiResults : products;

  return (
    <div className="container" style={{ padding: 'var(--space-8) var(--space-6)' }}>
      {/* ─── Top Filter & Search Bar ────────────────────────── */}
      <div className="glass-card" style={{
        padding: 'var(--space-4) var(--space-6)',
        marginBottom: 'var(--space-6)',
        display: 'flex',
        flexWrap: 'wrap',
        gap: 'var(--space-4)',
        alignItems: 'center',
        justifyContent: 'space-between',
      }}>
        {/* Search Form inside Catalog */}
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: 'var(--space-2)', flex: 1, minWidth: '280px', maxWidth: '540px' }}>
          <div style={{ position: 'relative', width: '100%' }}>
            <span style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', opacity: 0.6 }}>🔍</span>
            <input
              type="text"
              placeholder={aiMode ? "Ask AI (e.g. 'comfortable wireless running headphones')..." : "Search products, brands, or specs..."}
              value={searchInput}
              onChange={(e) => setSearchInput(e.target.value)}
              style={{
                width: '100%',
                padding: 'var(--space-2) var(--space-8) var(--space-2) 36px',
                borderRadius: 'var(--radius-md)',
                fontSize: 'var(--text-sm)',
              }}
            />
            {searchInput && (
              <button
                type="button"
                onClick={() => { setSearchInput(''); updateParam('q', ''); }}
                style={{
                  position: 'absolute',
                  right: '10px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  color: 'var(--text-muted)',
                  fontSize: '13px'
                }}
              >✕</button>
            )}
          </div>
          <button type="submit" className="btn btn-primary btn-sm">Search</button>
        </form>

        {/* Quick controls: AI Toggle & Sort */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-4)', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
            <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', fontWeight: 600 }}>SEARCH MODE:</span>
            <div style={{ display: 'flex', borderRadius: 'var(--radius-md)', overflow: 'hidden', border: '1px solid var(--border-default)' }}>
              <button
                onClick={() => { setAiMode(false); updateParam('ai', ''); }}
                className={!aiMode ? 'btn btn-primary btn-sm' : 'btn btn-ghost btn-sm'}
                style={{ borderRadius: 0, padding: '4px 12px', fontSize: 'var(--text-xs)' }}
              >
                Keyword
              </button>
              <button
                onClick={() => { setAiMode(true); updateParam('ai', 'true'); }}
                className={aiMode ? 'btn btn-primary btn-sm' : 'btn btn-ghost btn-sm'}
                style={{ borderRadius: 0, padding: '4px 12px', fontSize: 'var(--text-xs)' }}
              >
                🧠 AI Hybrid
              </button>
            </div>
          </div>

          {!aiMode && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-2)' }}>
              <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', fontWeight: 600 }}>SORT:</span>
              <select
                value={sortBy}
                onChange={e => updateParam('sort_by', e.target.value)}
                style={{ fontSize: 'var(--text-xs)', padding: '6px 10px', borderRadius: 'var(--radius-md)' }}
              >
                <option value="created_at">Newest</option>
                <option value="price_asc">Price: Low → High</option>
                <option value="price_desc">Price: High → Low</option>
                <option value="rating">Top Rated</option>
                <option value="title">Name A–Z</option>
              </select>
            </div>
          )}
        </div>
      </div>

      {/* ─── Active Filter Pills ───────────────────────────── */}
      {(q || category || minPrice || maxPrice) && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--space-2)',
          flexWrap: 'wrap',
          marginBottom: 'var(--space-6)',
          padding: 'var(--space-2) 0'
        }}>
          <span style={{ fontSize: 'var(--text-xs)', color: 'var(--text-muted)', fontWeight: 600 }}>Active Filters:</span>
          {category && (
            <span className="badge badge-accent" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '4px 10px' }}>
              📁 {activeCategoryName || category}
              <button
                onClick={() => updateParam('category', '')}
                style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'inherit', padding: 0 }}
                title="Remove category filter"
              >✕</button>
            </span>
          )}
          {q && (
            <span className="badge badge-accent" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '4px 10px' }}>
              🔍 "{q}"
              <button
                onClick={() => updateParam('q', '')}
                style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'inherit', padding: 0 }}
                title="Remove query filter"
              >✕</button>
            </span>
          )}
          {(minPrice || maxPrice) && (
            <span className="badge badge-accent" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', padding: '4px 10px' }}>
              💲 ${minPrice || '0'} - ${maxPrice || '∞'}
              <button
                onClick={() => { updateParam('min_price', ''); updateParam('max_price', ''); }}
                style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'inherit', padding: 0 }}
                title="Remove price filter"
              >✕</button>
            </span>
          )}
          <button
            onClick={clearAllFilters}
            className="btn btn-ghost btn-sm"
            style={{ fontSize: 'var(--text-xs)', color: 'var(--danger)', padding: '2px 8px' }}
          >
            Clear All
          </button>
        </div>
      )}

      <div style={{ display: 'flex', gap: 'var(--space-8)' }}>
        {/* ─── Sidebar Filters ────────────────────────────── */}
        <aside style={{
          width: 'var(--sidebar-width)', flexShrink: 0,
          display: 'flex', flexDirection: 'column', gap: 'var(--space-6)',
        }}>
          {/* Categories Sidebar */}
          <div className="glass-card" style={{ padding: 'var(--space-5)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-4)' }}>
              <h3 style={{ fontSize: 'var(--text-sm)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)', margin: 0 }}>
                Categories
              </h3>
              {category && (
                <button
                  onClick={() => updateParam('category', '')}
                  style={{ background: 'none', border: 'none', color: 'var(--accent-primary)', fontSize: 'var(--text-xs)', cursor: 'pointer' }}
                >
                  Reset
                </button>
              )}
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-1)' }}>
              <button
                onClick={() => updateParam('category', '')}
                style={{
                  textAlign: 'left',
                  padding: 'var(--space-2) var(--space-3)',
                  borderRadius: 'var(--radius-sm)',
                  fontSize: 'var(--text-sm)',
                  fontWeight: !category ? 600 : 400,
                  color: !category ? 'var(--accent-primary)' : 'var(--text-secondary)',
                  background: !category ? 'var(--accent-glow)' : 'transparent',
                  border: 'none',
                  cursor: 'pointer'
                }}
              >
                🌐 All Categories
              </button>

              {categories.map(cat => {
                const isSelected = category === cat.slug || category === cat.id;
                const hasActiveChild = cat.children && cat.children.some(ch => ch.slug === category || ch.id === category);
                const isExpanded = expandedCategories[cat.id] || isSelected || hasActiveChild;

                return (
                  <div key={cat.id} style={{ display: 'flex', flexDirection: 'column' }}>
                    <div style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      borderRadius: 'var(--radius-sm)',
                      background: (isSelected || hasActiveChild) ? 'var(--accent-glow)' : 'transparent',
                    }}>
                      <button
                        onClick={() => updateParam('category', cat.slug)}
                        style={{
                          flex: 1,
                          textAlign: 'left',
                          padding: 'var(--space-2) var(--space-3)',
                          borderRadius: 'var(--radius-sm)',
                          fontSize: 'var(--text-sm)',
                          fontWeight: (isSelected || hasActiveChild) ? 600 : 400,
                          color: (isSelected || hasActiveChild) ? 'var(--accent-primary)' : 'var(--text-secondary)',
                          background: 'transparent',
                          border: 'none',
                          cursor: 'pointer'
                        }}
                      >
                        {cat.icon} {cat.name}
                      </button>
                      {cat.children && cat.children.length > 0 && (
                        <button
                          onClick={() => toggleCategoryExpand(cat.id)}
                          style={{
                            background: 'none',
                            border: 'none',
                            cursor: 'pointer',
                            padding: '4px 8px',
                            color: 'var(--text-muted)',
                            fontSize: '11px',
                          }}
                          title="Toggle subcategories"
                        >
                          {isExpanded ? '▼' : '▶'}
                        </button>
                      )}
                    </div>

                    {/* Subcategories list */}
                    {isExpanded && cat.children && cat.children.length > 0 && (
                      <div style={{ paddingLeft: 'var(--space-4)', display: 'flex', flexDirection: 'column', gap: '2px', marginTop: '2px' }}>
                        {cat.children.map(child => {
                          const isChildSelected = category === child.slug || category === child.id;
                          return (
                            <button
                              key={child.id}
                              onClick={() => updateParam('category', child.slug)}
                              style={{
                                textAlign: 'left',
                                padding: '4px var(--space-3)',
                                borderRadius: 'var(--radius-sm)',
                                fontSize: 'var(--text-xs)',
                                fontWeight: isChildSelected ? 600 : 400,
                                color: isChildSelected ? 'var(--accent-primary)' : 'var(--text-muted)',
                                background: isChildSelected ? 'var(--bg-tertiary)' : 'transparent',
                                border: 'none',
                                cursor: 'pointer'
                              }}
                            >
                              • {child.name}
                            </button>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Price Filter */}
          <div className="glass-card" style={{ padding: 'var(--space-5)' }}>
            <h3 style={{ fontSize: 'var(--text-sm)', fontWeight: 600, marginBottom: 'var(--space-4)', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>
              Price Range ($)
            </h3>
            <div style={{ display: 'flex', gap: 'var(--space-2)', alignItems: 'center' }}>
              <input
                type="number"
                placeholder="Min"
                value={minPrice}
                onChange={e => updateParam('min_price', e.target.value)}
                style={{ fontSize: 'var(--text-sm)', width: '100%' }}
              />
              <span style={{ color: 'var(--text-muted)' }}>-</span>
              <input
                type="number"
                placeholder="Max"
                value={maxPrice}
                onChange={e => updateParam('max_price', e.target.value)}
                style={{ fontSize: 'var(--text-sm)', width: '100%' }}
              />
            </div>
          </div>
        </aside>

        {/* ─── Product Grid ───────────────────────────────── */}
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-6)' }}>
            <div>
              <h1 style={{ fontSize: 'clamp(1.5rem, 3vw, 2.25rem)', fontFamily: 'var(--font-serif)', fontWeight: 500, margin: 0, color: 'var(--text-primary)' }}>
                {q
                  ? (aiMode ? `AI Curation for "${q}"` : `Results for "${q}"`)
                  : (activeCategoryName ? activeCategoryName : 'The Full Collection')}
              </h1>
              {activeCategoryName && q && (
                <span style={{ fontSize: 'var(--text-xs)', color: 'var(--accent-primary)', fontWeight: 600 }}>
                  Filtered in: {activeCategoryName}
                </span>
              )}
            </div>
            <span style={{ color: 'var(--text-muted)', fontSize: 'var(--text-sm)' }}>
              {total} product{total !== 1 ? 's' : ''} found
            </span>
          </div>

          {loading ? (
            <div className="product-grid">
              {[...Array(8)].map((_, i) => (
                <div key={i} className="product-card" style={{ overflow: 'hidden' }}>
                  <div className="skeleton skeleton-image"></div>
                  <div style={{ padding: 'var(--space-4)' }}>
                    <div className="skeleton skeleton-text" style={{ width: '40%' }}></div>
                    <div className="skeleton skeleton-title"></div>
                    <div className="skeleton skeleton-text" style={{ width: '30%' }}></div>
                  </div>
                </div>
              ))}
            </div>
          ) : displayItems.length > 0 ? (
            <>
              <div className="product-grid stagger-grid">
                {displayItems.map((item) => {
                  const product = aiMode ? {
                    id: item.id,
                    title: item.title,
                    slug: item.slug,
                    short_description: item.short_description,
                    price: item.price,
                    compare_at_price: item.compare_at_price,
                    brand: item.brand,
                    avg_rating: item.avg_rating,
                    review_count: item.review_count,
                    stock_quantity: 1,
                    images: item.image_url ? [{ url: item.image_url }] : [],
                  } : item;

                  return (
                    <div key={item.id} style={{ position: 'relative' }}>
                      <ProductCard product={product} />
                      {aiMode && item.relevance_score && (
                        <div style={{
                          position: 'absolute',
                          top: 8,
                          right: 8,
                          zIndex: 10,
                          background: 'var(--accent-primary)',
                          color: 'white',
                          padding: '2px 8px',
                          borderRadius: 'var(--radius-full)',
                          fontSize: '10px',
                          fontWeight: 700,
                          fontFamily: 'var(--font-mono)',
                          boxShadow: '0 2px 8px rgba(0,0,0,0.2)'
                        }}>
                          {(item.relevance_score * 100).toFixed(0)}% match
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {/* Pagination */}
              {!aiMode && total > limit && (
                <div style={{
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  gap: 'var(--space-2)',
                  marginTop: 'var(--space-10)',
                  flexWrap: 'wrap',
                }}>
                  <button
                    disabled={page <= 1}
                    onClick={() => updateParam('page', String(page - 1))}
                    className="btn btn-secondary btn-sm"
                    style={{
                      opacity: page <= 1 ? 0.4 : 1,
                      cursor: page <= 1 ? 'not-allowed' : 'pointer',
                      fontSize: '0.75rem',
                      letterSpacing: '0.04em',
                    }}
                  >
                    ← Prev
                  </button>

                  {Array.from({ length: Math.ceil(total / limit) }, (_, i) => {
                    const pageNum = i + 1;
                    const isActive = Number(page) === pageNum;
                    return (
                      <button
                        key={pageNum}
                        onClick={() => updateParam('page', String(pageNum))}
                        className={isActive ? 'btn btn-primary btn-sm' : 'btn btn-secondary btn-sm'}
                        style={{
                          minWidth: '38px',
                          fontWeight: isActive ? 700 : 500,
                          fontSize: '0.8125rem',
                        }}
                      >
                        {pageNum}
                      </button>
                    );
                  })}

                  <button
                    disabled={page >= Math.ceil(total / limit)}
                    onClick={() => updateParam('page', String(page + 1))}
                    className="btn btn-secondary btn-sm"
                    style={{
                      opacity: page >= Math.ceil(total / limit) ? 0.4 : 1,
                      cursor: page >= Math.ceil(total / limit) ? 'not-allowed' : 'pointer',
                      fontSize: '0.75rem',
                      letterSpacing: '0.04em',
                    }}
                  >
                    Next →
                  </button>
                </div>
              )}
            </>
          ) : (
            <div className="glass-card" style={{ textAlign: 'center', padding: 'var(--space-16) var(--space-6)', color: 'var(--text-muted)' }}>
              <div style={{ fontSize: '3rem', marginBottom: 'var(--space-4)' }}>🔍</div>
              <h3 style={{ color: 'var(--text-primary)', marginBottom: 'var(--space-2)' }}>No matching products found</h3>
              <p style={{ maxWidth: '420px', margin: '0 auto var(--space-6)', fontSize: 'var(--text-sm)' }}>
                We couldn't find any products matching your criteria. Try clearing some filters or searching for general keywords like "Sony", "Apple", "Shoes", or "MacBook".
              </p>
              <button onClick={clearAllFilters} className="btn btn-primary">
                Clear All Filters
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
