import { createContext, useContext, useState, useEffect } from 'react'
import { apiFetch, apiLogin, saveToken, clearToken, getToken } from '../lib/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = getToken()
    if (!token) { setLoading(false); return }
    apiFetch('GET', '/auth/me')
      .then(setUser)
      .catch(() => clearToken())
      .finally(() => setLoading(false))
  }, [])

  const login = async (email, password) => {
    const data = await apiLogin(email, password)
    saveToken(data.access_token)
    const me = await apiFetch('GET', '/auth/me', null, data.access_token)
    setUser(me)
    return me
  }

  const logout = () => {
    clearToken()
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
