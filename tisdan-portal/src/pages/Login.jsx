import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { C } from '../lib/theme'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const user = await login(form.email, form.password)
      navigate(user.role === 'COORDINATOR' ? '/coordinators' : '/')
    } catch (ex) {
      setError(ex.message)
    }
    setLoading(false)
  }

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center',
      justifyContent: 'center', background: C.sidebar,
    }}>
      <div style={{
        background: C.surface, borderRadius: 16, padding: '40px 36px',
        width: '100%', maxWidth: 380, boxShadow: '0 24px 64px rgba(0,0,0,.35)',
      }}>
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{ fontSize: 32, fontWeight: 800, color: C.accent, letterSpacing: '-1px' }}>Tisdan</div>
          <div style={{ color: C.muted, fontSize: 13, marginTop: 4 }}>Diagnostic Centre Portal</div>
        </div>

        {error && (
          <div style={{
            background: '#fef2f2', border: `1px solid #fecaca`, color: C.danger,
            padding: '10px 14px', borderRadius: 6, fontSize: 13, marginBottom: 18,
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: 14 }}>
            <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: C.muted, marginBottom: 5 }}>
              Email address
            </label>
            <input
              type='email' required autoFocus
              value={form.email}
              onChange={e => setForm(f => ({ ...f, email: e.target.value }))}
              placeholder='you@tisdan.com'
              style={{
                width: '100%', padding: '10px 13px', borderRadius: 7,
                border: `1px solid ${C.border}`, fontSize: 14, outline: 'none',
                background: C.bg, color: C.text,
              }}
            />
          </div>
          <div style={{ marginBottom: 22 }}>
            <label style={{ display: 'block', fontSize: 12, fontWeight: 600, color: C.muted, marginBottom: 5 }}>
              Password
            </label>
            <input
              type='password' required
              value={form.password}
              onChange={e => setForm(f => ({ ...f, password: e.target.value }))}
              placeholder='••••••••'
              style={{
                width: '100%', padding: '10px 13px', borderRadius: 7,
                border: `1px solid ${C.border}`, fontSize: 14, outline: 'none',
                background: C.bg, color: C.text,
              }}
            />
          </div>
          <button
            type='submit' disabled={loading}
            style={{
              width: '100%', padding: '11px', borderRadius: 7, border: 'none',
              background: C.accent, color: '#fff', fontSize: 14, fontWeight: 700,
              cursor: loading ? 'not-allowed' : 'pointer', opacity: loading ? 0.7 : 1,
            }}
          >
            {loading ? 'Signing in…' : 'Sign in'}
          </button>
        </form>
      </div>
    </div>
  )
}
