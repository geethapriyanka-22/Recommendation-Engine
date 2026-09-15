/**
 * Activity Tracker for NovaMart Personalized Recommendations
 * 
 * Persists recent client interactions (viewed, carted, purchased)
 * in localStorage so that recommendations adapt dynamically across sessions.
 */

const STORAGE_KEY = 'novamart_user_activity_v1';

export function trackProductInteraction(type, productId) {
  if (!productId) return;
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    const data = raw ? JSON.parse(raw) : { views: [], cart: [], purchases: [] };

    if (type === 'view') {
      data.views = [productId, ...(data.views || []).filter(id => id !== productId)].slice(0, 12);
    } else if (type === 'cart') {
      data.cart = [productId, ...(data.cart || []).filter(id => id !== productId)].slice(0, 12);
    } else if (type === 'purchase') {
      const ids = Array.isArray(productId) ? productId : [productId];
      data.purchases = [...ids, ...(data.purchases || []).filter(id => !ids.includes(id))].slice(0, 12);
    }

    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (err) {
    console.warn('Could not record product interaction:', err);
  }
}

export function getInteractionPayload() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const data = JSON.parse(raw);
    
    // Purchases prioritized, then Cart items, then Views
    const combined = [
      ...(data.purchases || []),
      ...(data.cart || []),
      ...(data.views || []),
    ];
    // De-duplicate preserving priority order
    return Array.from(new Set(combined));
  } catch (err) {
    return [];
  }
}
