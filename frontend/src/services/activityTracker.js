/**
 * Activity Tracker for NovaMart Multi-Channel Personalized Recommendations
 * 
 * Persists client interactions:
 * - Searches (explicit intent queries)
 * - Wishlist (high affinity saves)
 * - Cart (purchase consideration)
 * - Purchases (strongest conversion signal)
 * - Views (recent product exploration)
 * 
 * Dispatches 'novamart_activity_updated' custom event so UI and recommendations
 * update dynamically across pages without requiring manual page reloads.
 */

const STORAGE_KEY = 'novamart_user_activity_v2';

function getActivityData() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : { views: [], searches: [], wishlist: [], cart: [], purchases: [] };
  } catch (err) {
    return { views: [], searches: [], wishlist: [], cart: [], purchases: [] };
  }
}

function saveActivityData(data) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    window.dispatchEvent(new CustomEvent('novamart_activity_updated'));
  } catch (err) {
    console.warn('Could not save activity data:', err);
  }
}

export function trackProductInteraction(type, productId) {
  if (!productId) return;
  const data = getActivityData();

  if (type === 'view') {
    data.views = [productId, ...(data.views || []).filter(id => id !== productId)].slice(0, 16);
  } else if (type === 'cart') {
    data.cart = [productId, ...(data.cart || []).filter(id => id !== productId)].slice(0, 16);
  } else if (type === 'purchase') {
    const ids = Array.isArray(productId) ? productId : [productId];
    data.purchases = [...ids, ...(data.purchases || []).filter(id => !ids.includes(id))].slice(0, 16);
  }

  saveActivityData(data);
}

export function trackSearch(query) {
  if (!query || typeof query !== 'string') return;
  const trimmed = query.trim();
  if (trimmed.length < 2) return;

  const data = getActivityData();
  data.searches = [
    trimmed,
    ...(data.searches || []).filter(q => q.toLowerCase() !== trimmed.toLowerCase())
  ].slice(0, 8);

  saveActivityData(data);
}

export function toggleWishlist(productId) {
  if (!productId) return false;
  const data = getActivityData();
  const list = data.wishlist || [];
  const exists = list.includes(productId);

  if (exists) {
    data.wishlist = list.filter(id => id !== productId);
  } else {
    data.wishlist = [productId, ...list].slice(0, 30);
  }

  saveActivityData(data);
  return !exists;
}

export function isWishlisted(productId) {
  if (!productId) return false;
  const data = getActivityData();
  return (data.wishlist || []).includes(productId);
}

export function getWishlist() {
  const data = getActivityData();
  return data.wishlist || [];
}

export const getWishlistIds = getWishlist;

export function getRecentlyViewedIds() {
  const data = getActivityData();
  return data.views || [];
}

export function clearRecentlyViewed() {
  const data = getActivityData();
  data.views = [];
  saveActivityData(data);
}

export function getInteractionPayload() {
  const data = getActivityData();
  
  // Purchases prioritized, then Wishlist, then Cart, then Views
  const combined = [
    ...(data.purchases || []),
    ...(data.wishlist || []),
    ...(data.cart || []),
    ...(data.views || []),
  ];
  // De-duplicate preserving priority order
  return Array.from(new Set(combined));
}

export function getRecentSearchesPayload() {
  const data = getActivityData();
  return data.searches || [];
}
