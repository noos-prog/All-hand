import { useState, useEffect } from 'react'
import { fetchAgents, fetchSpecializations, registerExternalAgent, removeExternalAgent } from '../api.js'

export default function Agents() {
  const [agents, setAgents] = useState([])
  const [specs, setSpecs] = useState([])
  const [filter, setFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [formData, setFormData] = useState({ name: '', url: '', model: '', api_key: '' })

  const load = async () => {
    try {
      const [agentsData, specsData] = await Promise.all([
        fetchAgents(),
        fetchSpecializations(),
      ])
      setAgents(agentsData.agents || [])
      setSpecs(specsData.specializations || [])
    } catch (e) {
      console.error('agents error', e)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
    const interval = setInterval(load, 20000)
    return () => clearInterval(interval)
  }, [])

  const handleRegister = async () => {
    if (!formData.name.trim() || !formData.url.trim()) return
    try {
      await registerExternalAgent(formData.name, formData.url, formData.model, formData.api_key)
      setShowModal(false)
      setFormData({ name: '', url: '', model: '', api_key: '' })
      load()
    } catch (e) {
      alert('خطأ: ' + e.message)
    }
  }

  const handleRemove = async (name) => {
    if (!confirm(`حذف الوكيل "${name}"?`)) return
    try {
      await removeExternalAgent(name)
      load()
    } catch (e) {
      alert('خطأ: ' + e.message)
    }
  }

  const filtered = filter ? agents.filter((a) => a.specialization === filter) : agents
  const specGroups = {}
  filtered.forEach((a) => {
    if (!specGroups[a.specialization]) specGroups[a.specialization] = []
    specGroups[a.specialization].push(a)
  })

  if (loading) {
    return <div className="loading"><div className="spinner" /> جاري تحميل الوكلاء...</div>
  }

  return (
    <div>
      <div className="card" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <div className="card-title" style={{ marginBottom: '4px' }}>{agents.length} وكيل نشط</div>
            <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
              {specs.length} تخصص · {agents.filter((a) => a.specialization === 'external').length} وكلاء خارجيون
            </div>
          </div>
          <button className="btn btn-primary" onClick={() => setShowModal(true)}>
            + إضافة وكيل خارجي
          </button>
        </div>

        <div style={{ display: 'flex', gap: '8px', marginTop: '16px', flexWrap: 'wrap' }}>
          <button
            className={`btn ${filter === '' ? 'btn-primary' : 'btn-ghost'}`}
            style={{ fontSize: '13px' }}
            onClick={() => setFilter('')}
          >
            الكل
          </button>
          {specs.map((s) => (
            <button
              key={s.name}
              className={`btn ${filter === s.name ? 'btn-primary' : 'btn-ghost'}`}
              style={{ fontSize: '13px' }}
              onClick={() => setFilter(s.name)}
            >
              {s.name}
            </button>
          ))}
        </div>
      </div>

      {Object.keys(specGroups).map((specName) => (
        <div key={specName} style={{ marginBottom: '24px' }}>
          <div className="card-title" style={{ marginBottom: '12px' }}>
            {specName}
            <span className="badge badge-info" style={{ marginRight: '8px' }}>
              {specGroups[specName].length}
            </span>
          </div>
          <div className="agent-list">
            {specGroups[specName].map((agent) => (
              <div key={agent.name} className="agent-card">
                <div className="agent-name">{agent.name}</div>
                <div className="agent-spec">
                  {agent.specialization === 'external' && (
                    <span className="badge badge-warning" style={{ marginRight: '6px' }}>
                      خارجي
                    </span>
                  )}
                  {agent.status === 'idle' ? 'خامل' : agent.status === 'working' ? 'يعمل' : agent.status}
                </div>
                <div className="agent-stats">
                  <div className="agent-stat">
                    <span className="agent-stat-label">مكتملة</span>
                    <span className="agent-stat-value success">{agent.stats?.tasks_completed || 0}</span>
                  </div>
                  <div className="agent-stat">
                    <span className="agent-stat-label">فشلت</span>
                    <span className="agent-stat-value error">{agent.stats?.tasks_failed || 0}</span>
                  </div>
                  <div className="agent-stat">
                    <span className="agent-stat-label">الوقت</span>
                    <span className="agent-stat-value">
                      {(agent.stats?.total_time_s || 0).toFixed(1)}s
                    </span>
                  </div>
                </div>
                {agent.specialization === 'external' && (
                  <button
                    className="btn btn-danger"
                    style={{ marginTop: '12px', fontSize: '12px', padding: '4px 10px' }}
                    onClick={() => handleRemove(agent.name)}
                  >
                    حذف
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>
      ))}

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-title">إضافة وكيل خارجي</div>
            <div style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '16px' }}>
              أي وكيل يدعم OpenAI-compatible API (Ollama, LM Studio, vLLM...)
            </div>
            <div className="form-group">
              <label className="form-label">الاسم</label>
              <input
                className="form-input"
                placeholder="my-ollama"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">URL (endpoint)</label>
              <input
                className="form-input"
                placeholder="http://localhost:11434/v1/chat/completions"
                value={formData.url}
                onChange={(e) => setFormData({ ...formData, url: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">النموذج (اختياري)</label>
              <input
                className="form-input"
                placeholder="llama3"
                value={formData.model}
                onChange={(e) => setFormData({ ...formData, model: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label className="form-label">API Key (اختياري)</label>
              <input
                className="form-input"
                type="password"
                placeholder="sk-..."
                value={formData.api_key}
                onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
              />
            </div>
            <div className="modal-actions">
              <button className="btn btn-ghost" onClick={() => setShowModal(false)}>إلغاء</button>
              <button className="btn btn-primary" onClick={handleRegister}>إضافة</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
