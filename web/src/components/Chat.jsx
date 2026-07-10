import { useState, useRef, useEffect } from 'react'
import { sendChat } from '../api.js'

const QUICK_PROMPTS = [
  'حلل أداء النظام الحالي',
  'ابحث عن أحدث تقنيات الذكاء الاصطناعي',
  'اكتب كود Python لحساب متوسط قائمة أرقام',
  'تحقق من صحة هذا JSON: {"name":"test","value":42}',
  'صمم استراتيجية لتطوير الحضارة',
]

export default function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEnd = useRef(null)

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (text) => {
    const prompt = (text || input).trim()
    if (!prompt || loading) return

    setInput('')
    setMessages((prev) => [...prev, { role: 'user', content: prompt }])
    setLoading(true)

    try {
      const res = await sendChat(prompt)
      const answer = res.outcome?.result?.answer || res.outcome?.result?.error || 'لا يوجد رد'
      setMessages((prev) => [...prev, {
        role: 'agent',
        content: answer,
        agent: res.agent,
        specialization: res.routed_to,
        elapsed: res.outcome?.elapsed_s,
      }])
    } catch (e) {
      setMessages((prev) => [...prev, {
        role: 'agent',
        content: `خطأ: ${e.message}`,
        agent: 'system',
        specialization: 'error',
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="empty-state">
            <div className="empty-state-icon">✦</div>
            <div>ابدأ محادثة مع حضارة الوكلاء</div>
            <div style={{ marginTop: '20px', display: 'flex', flexWrap: 'wrap', gap: '8px', justifyContent: 'center' }}>
              {QUICK_PROMPTS.map((p) => (
                <button key={p} className="btn btn-ghost" style={{ fontSize: '13px' }} onClick={() => handleSend(p)}>
                  {p}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`chat-message ${msg.role}`}>
            <div className={`chat-avatar ${msg.role}`}>
              {msg.role === 'user' ? 'أنت' : 'A'}
            </div>
            <div>
              <div className="chat-bubble">{msg.content}</div>
              <div className="chat-meta">
                {msg.role === 'agent' && msg.agent && `${msg.specialization} · ${msg.agent}`}
                {msg.elapsed && ` · ${msg.elapsed}s`}
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="chat-message agent">
            <div className="chat-avatar agent">A</div>
            <div className="chat-bubble">
              <div className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }} />
              <span style={{ marginRight: '8px' }}>الوكيل يفكر...</span>
            </div>
          </div>
        )}

        <div ref={messagesEnd} />
      </div>

      <div className="chat-input-area">
        <textarea
          className="chat-input"
          placeholder="اكتب رسالتك هنا... (Enter للإرسال، Shift+Enter لسطر جديد)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          disabled={loading}
        />
        <button className="btn btn-primary" onClick={() => handleSend()} disabled={loading || !input.trim()}>
          إرسال
        </button>
      </div>
    </div>
  )
}
