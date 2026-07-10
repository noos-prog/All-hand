import { useState, useEffect } from 'react'
import { fetchSpecializations, createTask } from '../api.js'

const ICONS = {
  'chart-line': '📊', 'plug': '🔌', 'building': '🏗️', 'hammer': '🔨',
  'code': '💻', 'comments': '💬', 'calculator': '🧮', 'database': '🗄️',
  'palette': '🎨', 'graduation-cap': '🎓', 'edit': '✏️', 'monitor-heart': '📈',
  'network-wired': '🌐', 'search': '🔍', 'check-double': '✔️', 'seedling': '🌱',
  'chess': '♟️', 'syringe': '💉', 'vial': '🧪', 'shield-check': '🛡️',
  'robot': '🤖',
}

export default function Specializations() {
  const [specs, setSpecs] = useState([])
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState(null)
  const [prompt, setPrompt] = useState('')
  const [taskData, setTaskData] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [result, setResult] = useState(null)

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchSpecializations()
        setSpecs(data.specializations || [])
      } catch (e) {
        console.error('specs error', e)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const handleSubmit = async () => {
    if (!selected || !prompt.trim()) return
    setSubmitting(true)
    setResult(null)
    try {
      let data = null
      if (taskData.trim()) {
        try { data = JSON.parse(taskData) } catch { data = taskData }
      }
      const res = await createTask(selected, prompt, data)
      setResult({ ok: true, task_id: res.task_id, status: res.status })
    } catch (e) {
      setResult({ ok: false, error: e.message })
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return <div className="loading"><div className="spinner" /> جاري تحميل التخصصات...</div>
  }

  if (selected) {
    const spec = specs.find((s) => s.name === selected)
    return (
      <div>
        <div className="card" style={{ marginBottom: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
            <div className="spec-icon" style={{ marginBottom: 0 }}>
              {ICONS[spec?.icon] || '🤖'}
            </div>
            <div>
              <div className="spec-name">{spec?.name}</div>
              <div className="spec-desc" style={{ margin: 0 }}>{spec?.description}</div>
            </div>
            <button className="btn btn-ghost" style={{ marginRight: 'auto' }} onClick={() => { setSelected(null); setResult(null) }}>
              رجوع
            </button>
          </div>

          {spec?.tool && (
            <div className="badge badge-info" style={{ marginBottom: '12px' }}>
              أداة: {spec.tool}
            </div>
          )}

          <div className="form-group">
            <label className="form-label">المهمة / الطلب</label>
            <textarea
              className="form-input"
              placeholder="اكتب ما تريد من الوكيل القيام به..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={3}
            />
          </div>

          {(selected === 'data_processor' || selected === 'validator' || selected === 'test_runner') && (
            <div className="form-group">
              <label className="form-label">
                {selected === 'test_runner' ? 'كود Python لتنفيذه' : 'البيانات (JSON أو أرقام)'}
              </label>
              <textarea
                className="form-input"
                placeholder={selected === 'test_runner' ? 'print("Hello")' : '{"key": "value"} أو [1, 2, 3]'}
                value={taskData}
                onChange={(e) => setTaskData(e.target.value)}
                rows={4}
              />
            </div>
          )}

          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <button className="btn btn-primary" onClick={handleSubmit} disabled={submitting || !prompt.trim()}>
              {submitting ? 'جاري الإرسال...' : 'إرسال المهمة'}
            </button>
            {result && (
              <div>
                {result.ok ? (
                  <span className="badge badge-success">تم الإرسال: {result.task_id}</span>
                ) : (
                  <span className="badge badge-error">خطأ: {result.error}</span>
                )}
              </div>
            )}
          </div>
          <div style={{ marginTop: '12px', fontSize: '13px', color: 'var(--text-muted)' }}>
            يمكنك تتبع المهمة في تبويب "المهام"
          </div>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="card" style={{ marginBottom: '24px' }}>
        <div className="card-title">20 تخصص · {specs.length} وكيل متاح</div>
        <div style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
          كل تخصص يحتوي على وكلاء حقيقيين يعملون بنماذج LLM وأدوات فعلية. اختر تخصصاً لإرسال مهمة.
        </div>
      </div>

      <div className="spec-grid">
        {specs.map((spec) => (
          <div key={spec.name} className="spec-card" onClick={() => setSelected(spec.name)}>
            <div className="spec-icon">{ICONS[spec.icon] || '🤖'}</div>
            <div className="spec-name">{spec.name}</div>
            <div className="spec-desc">{spec.description}</div>
            <div className="spec-meta">
              <span>{spec.agents} وكيل</span>
              {spec.tool && <span className="spec-tool">⚙ {spec.tool}</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
