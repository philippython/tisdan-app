import { useCallback } from 'react'
import { apiFetch } from '../lib/api'

export function useApi() {
  const request = useCallback((method, path, body = null) => {
    return apiFetch(method, path, body)
  }, [])

  return { request }
}
