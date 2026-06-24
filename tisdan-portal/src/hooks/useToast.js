import { useState } from 'react'

export function useToast() {
  const [toast, setToast] = useState(null)
  const show = (msg, type = 'success') => setToast({ msg, type })
  const hide = () => setToast(null)
  return { toast, show, hide }
}
