export const C = {
  bg: '#f8f9fb',
  surface: '#ffffff',
  sidebar: '#0f1c2e',
  sidebarActive: '#2563eb',
  accent: '#2563eb',
  accentLight: '#dbeafe',
  text: '#1e293b',
  muted: '#64748b',
  border: '#e2e8f0',
  danger: '#ef4444',
  success: '#10b981',
  warn: '#f59e0b',
  purple: '#8b5cf6',
}

export const statusColor = {
  PENDING: C.warn,
  CONFIRMED: C.accent,
  CANCELLED: C.danger,
  COMPLETED: C.success,
  RELEASED: C.success,
  FAILED: C.danger,
  ADMIN: C.accent,
  STAFF: C.purple,
  DOCTOR: C.success,
  COORDINATOR: C.warn,
  CLIENT: C.muted,
}

export const fmtDate = (d) => d ? new Date(d).toLocaleString() : '—'
export const fmtShort = (d) => d ? new Date(d).toLocaleDateString() : '—'
export const truncate = (s, n = 60) => s && s.length > n ? s.slice(0, n) + '…' : (s || '—')
export const shortId = (id) => id ? id.slice(0, 8) + '…' : '—'
