import { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, User, Cpu, Clock, AlertCircle } from 'lucide-react';
import { sendChat } from '../api';
import type { ChatMessage } from '../types';
import { getIcon, SPECIALIZATION_LABELS } from '../icons';
import { Spinner } from './ui';

const QUICK_PROMPTS = [
  'حلل أداء النظام الحالي',
  'ابحث عن أحدث تقنيات الذكاء الاصطناعي',
  'اكتب كود Python لحساب متوسط قائمة أرقام',
  'تحقق من صحة هذا JSON: {"name":"test","value":42}',
  'صمم استراتيجية لتطوير الحضارة',
];

export function Chat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEnd = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEnd.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (text?: string) => {
    const prompt = (text || input).trim();
    if (!prompt || loading) return;

    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: prompt }]);
    setLoading(true);

    try {
      const res = await sendChat(prompt);
      const answer =
        res.outcome?.result?.answer ||
        res.outcome?.result?.error ||
        'لا يوجد رد من الوكيل';
      setMessages((prev) => [
        ...prev,
        {
          role: 'agent',
          content: answer,
          agent: res.agent,
          specialization: res.routed_to,
          elapsed: res.outcome?.elapsed_s,
        },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'agent',
          content: `خطأ: ${(e as Error).message}`,
          agent: 'system',
          specialization: 'error',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      void handleSend();
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-140px)] lg:h-[calc(100vh-120px)]">
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-white mb-1">المحادثة</h1>
        <p className="text-sm text-primary-muted">تحدث مع حضارة الوكلاء — يتم التوجيه تلقائياً لأنسب تخصص</p>
      </div>

      {/* Messages */}
      <div className="flex-1 glass-card p-4 lg:p-6 overflow-y-auto mb-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center py-12 animate-fade-in">
            <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-accent/20 to-blue-600/20 border border-accent/30 flex items-center justify-center mb-4 animate-pulse-glow">
              <Sparkles size={28} className="text-accent" />
            </div>
            <div className="text-lg font-semibold text-primary-secondary mb-2">
              ابدأ محادثة مع حضارة الوكلاء
            </div>
            <div className="text-sm text-primary-muted mb-6">
              اكتب رسالتك وسيتم توجيهها تلقائياً للوكيل الأنسب
            </div>
            <div className="flex flex-wrap gap-2 justify-center max-w-2xl">
              {QUICK_PROMPTS.map((p) => (
                <button
                  key={p}
                  onClick={() => void handleSend(p)}
                  className="btn-ghost text-xs"
                  disabled={loading}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="space-y-4">
          {messages.map((msg, i) => (
            <MessageBubble key={i} msg={msg} />
          ))}

          {loading && (
            <div className="flex gap-3 animate-fade-in">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-accent to-blue-600 flex items-center justify-center flex-shrink-0">
                <Cpu size={18} className="text-white" />
              </div>
              <div className="glass-card px-4 py-3 flex items-center gap-3">
                <Spinner size={16} />
                <span className="text-sm text-primary-secondary">الوكيل يفكر...</span>
              </div>
            </div>
          )}
        </div>

        <div ref={messagesEnd} />
      </div>

      {/* Input */}
      <div className="glass-card p-3 flex items-end gap-3">
        <textarea
          className="form-input flex-1 !bg-transparent !border-transparent !ring-0 resize-none max-h-32"
          placeholder="اكتب رسالتك هنا... (Enter للإرسال، Shift+Enter لسطر جديد)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
          disabled={loading}
          style={{ height: 'auto', minHeight: '44px' }}
          onInput={(e) => {
            const el = e.currentTarget;
            el.style.height = 'auto';
            el.style.height = `${Math.min(el.scrollHeight, 128)}px`;
          }}
        />
        <button
          className="btn-primary flex-shrink-0"
          onClick={() => void handleSend()}
          disabled={loading || !input.trim()}
        >
          <Send size={16} className="inline ml-1" />
          إرسال
        </button>
      </div>
    </div>
  );
}

function MessageBubble({ msg }: { msg: ChatMessage }) {
  const isUser = msg.role === 'user';
  const isError = msg.specialization === 'error';
  const SpecIcon = msg.specialization ? getIcon(msg.specialization) : Cpu;

  return (
    <div className={`flex gap-3 animate-slide-up ${isUser ? 'flex-row-reverse' : ''}`}>
      <div
        className={`w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 ${
          isUser
            ? 'bg-elevated border border-border'
            : 'bg-gradient-to-br from-accent to-blue-600'
        }`}
      >
        {isUser ? <User size={18} className="text-primary-secondary" /> : <Cpu size={18} className="text-white" />}
      </div>
      <div className={`max-w-[80%] ${isUser ? 'items-end' : 'items-start'} flex flex-col gap-1`}>
        <div
          className={`rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap break-words ${
            isUser
              ? 'bg-gradient-to-br from-accent/15 to-blue-600/10 border border-accent/20 text-primary'
              : isError
                ? 'bg-error/10 border border-error/20 text-error'
                : 'glass-card text-primary'
          }`}
        >
          {isError && <AlertCircle size={14} className="inline ml-1 mb-0.5" />}
          {msg.content}
        </div>
        {!isUser && msg.agent && (
          <div className="flex items-center gap-2 text-xs text-primary-muted px-1">
            <SpecIcon size={12} className="text-accent" />
            <span>{SPECIALIZATION_LABELS[msg.specialization || ''] || msg.specialization}</span>
            <span>·</span>
            <span className="font-mono">{msg.agent}</span>
            {msg.elapsed != null && (
              <>
                <span>·</span>
                <Clock size={10} />
                <span>{msg.elapsed}s</span>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
