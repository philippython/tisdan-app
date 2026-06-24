import { useState, useEffect } from 'react'
import { useApi } from '../hooks/useApi'
import { useToast } from '../hooks/useToast'
import { Card, Tabs, Field, Btn, Toast, Table, Spinner } from '../components/ui'
import { fmtDate } from '../lib/theme'

export default function Broadcast() {
  const { request } = useApi()
  const { toast, show, hide } = useToast()
  const [tab, setTab] = useState('general')
  const [genList, setGenList] = useState([])
  const [perList, setPerList] = useState([])
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [genForm, setGenForm] = useState({ title: '', message: '' })
  const [perForm, setPerForm] = useState({ user_id: '', message: '' })

  const loadAll = async () => {
    try {
      const [g, p] = await Promise.all([
        request('GET', '/broadcasts/general/'),
        request('GET', '/broadcasts/personal/'),
      ])
      setGenList([...g].reverse())
      setPerList([...p].reverse())
    } catch (e) { show(e.message, 'error') }
    setLoading(false)
  }

  useEffect(() => { loadAll() }, [])

  const sendGeneral = async (e) => {
    e.preventDefault()
    setSending(true)
    try {
      await request('POST', '/broadcasts/general/', genForm)
      show('📢 General broadcast queued for all customers')
      setGenForm({ title: '', message: '' })
      loadAll()
    } catch (ex) { show(ex.message, 'error') }
    setSending(false)
  }

  const sendPersonal = async (e) => {
    e.preventDefault()
    setSending(true)
    try {
      await request('POST', '/broadcasts/personal/', perForm)
      show('💬 Personal message sent')
      setPerForm({ user_id: '', message: '' })
      loadAll()
    } catch (ex) { show(ex.message, 'error') }
    setSending(false)
  }

  const genColumns = [
    { key: 'title', label: 'Title' },
    { key: 'message', label: 'Message', render: v => v?.slice(0, 90) + (v?.length > 90 ? '…' : '') },
    { key: 'created_at', label: 'Sent At', render: v => fmtDate(v) },
  ]

  const perColumns = [
    { key: 'user_id', label: 'User ID', render: v => <code style={{ fontSize: 11 }}>{v?.slice(0, 8)}…</code> },
    { key: 'message', label: 'Message', render: v => v?.slice(0, 90) + (v?.length > 90 ? '…' : '') },
    { key: 'created_at', label: 'Sent At', render: v => fmtDate(v) },
  ]

  return (
    <>
      {toast && <Toast msg={toast.msg} type={toast.type} onClose={hide} />}

      <Tabs
        tabs={[
          { id: 'general', label: '📢 General Broadcast' },
          { id: 'personal', label: '💬 Personal Message' },
        ]}
        active={tab}
        onChange={setTab}
      />

      {tab === 'general' ? (
        <>
          <Card style={{ marginBottom: 20 }}>
            <h3 style={{ fontSize: 15, fontWeight: 700, marginBottom: 6 }}>Send to All Customers</h3>
            <p style={{ fontSize: 13, color: '#64748b', marginBottom: 18 }}>
              This message will be sent via WhatsApp to every customer in the system.
            </p>
            <form onSubmit={sendGeneral}>
              <Field label='Title' name='title' value={genForm.title} onChange={e => setGenForm(f => ({ ...f, title: e.target.value }))} required placeholder='e.g. New test available' />
              <Field label='Message' name='message' value={genForm.message} onChange={e => setGenForm(f => ({ ...f, message: e.target.value }))} required rows={4} placeholder='Your message to all customers…' />
              <Btn type='submit' disabled={sending}>{sending ? 'Sending…' : 'Send Broadcast'}</Btn>
            </form>
          </Card>

          <Card>
            <h3 style={{ fontSize: 15, fontWeight: 700, marginBottom: 16 }}>Broadcast History</h3>
            {loading ? <Spinner /> : <Table columns={genColumns} rows={genList} canEdit={false} canDelete={false} />}
          </Card>
        </>
      ) : (
        <>
          <Card style={{ marginBottom: 20 }}>
            <h3 style={{ fontSize: 15, fontWeight: 700, marginBottom: 6 }}>Send to a Specific Customer</h3>
            <p style={{ fontSize: 13, color: '#64748b', marginBottom: 18 }}>
              Send a targeted WhatsApp message to one customer using their User ID.
            </p>
            <form onSubmit={sendPersonal}>
              <Field label='Customer User ID' name='user_id' value={perForm.user_id} onChange={e => setPerForm(f => ({ ...f, user_id: e.target.value }))} required placeholder='UUID of the user' />
              <Field label='Message' name='message' value={perForm.message} onChange={e => setPerForm(f => ({ ...f, message: e.target.value }))} required rows={4} placeholder='Your message to this customer…' />
              <Btn type='submit' disabled={sending}>{sending ? 'Sending…' : 'Send Message'}</Btn>
            </form>
          </Card>

          <Card>
            <h3 style={{ fontSize: 15, fontWeight: 700, marginBottom: 16 }}>Personal Message History</h3>
            {loading ? <Spinner /> : <Table columns={perColumns} rows={perList} canEdit={false} canDelete={false} />}
          </Card>
        </>
      )}
    </>
  )
}
