import { Outlet, useLocation } from 'react-router-dom'
import Sidebar from './Sidebar'
import { C } from '../lib/theme'

const PAGE_TITLES = {
  '/': 'Dashboard',
  '/bookings': 'Bookings',
  '/results': 'Results',
  '/patients': 'Patients',
  '/customers': 'Customers',
  '/payments': 'Payments',
  '/tests': 'Diagnostic Tests',
  '/branches': 'Branches',
  '/users': 'Users',
  '/staff': 'Staff Management',
  '/doctors': 'Doctors',
  '/coordinators': 'Coordinators & Referrals',
  '/broadcast': 'Broadcast',
}

export default function Layout() {
  const location = useLocation()
  const title = PAGE_TITLES[location.pathname] || 'Tisdan'

  return (
    <div style={{ display: 'flex', height: '100vh', background: C.bg, overflow: 'hidden' }}>
      <Sidebar />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* Topbar */}
        <header style={{
          background: C.surface, borderBottom: `1px solid ${C.border}`,
          padding: '0 28px', height: 56, display: 'flex', alignItems: 'center',
          justifyContent: 'space-between', flexShrink: 0,
        }}>
          <h1 style={{ fontSize: 16, fontWeight: 700, color: C.text }}>{title}</h1>
          <div style={{ fontSize: 13, color: C.muted }}>
            {new Date().toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' })}
          </div>
        </header>

        {/* Page content */}
        <main style={{ flex: 1, overflowY: 'auto', padding: '24px 28px' }}>
          <Outlet />
        </main>
      </div>
    </div>
  )
}
