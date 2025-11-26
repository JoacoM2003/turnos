export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('es-AR', {
    style: 'currency',
    currency: 'ARS',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('es-AR', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(date);
};

export const formatDateOnly = (dateString: string): string => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('es-AR', {
    dateStyle: 'medium',
  }).format(date);
};

export const formatTime = (timeString: string): string => {
  // timeString viene como "HH:MM:SS" o "HH:MM"
  const parts = timeString.split(':');
  return `${parts[0]}:${parts[1]}`;
};