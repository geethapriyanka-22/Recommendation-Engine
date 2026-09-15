export const CURRENCY_SYMBOL = '₹';

export function formatPrice(amount) {
  if (amount === null || amount === undefined || isNaN(amount)) return '₹0';
  const num = Number(amount);
  return `${CURRENCY_SYMBOL}${num.toLocaleString('en-IN', {
    maximumFractionDigits: 2,
    minimumFractionDigits: 0,
  })}`;
}

export function formatCurrency(amount) {
  return formatPrice(amount);
}
