import { useState, useEffect } from 'react';
import { ArrowRight, Wrench, Send, CheckCircle2, AlertCircle, Layers } from 'lucide-react';
import { fetchSpecializations, createTask } from '../api';
import type { Specialization } from '../types';
import { getIcon, SPECIALIZATION_LABELS } from '../icons';
import { LoadingState, EmptyState } from './ui';

export function Specializations() {
  const [specs, setSpecs] = useState<Specialization[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<string | null>(null);
  const [prompt, setPrompt] = useState('');
  const [taskData, setTaskData] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<{ ok: boolean; task_id?: string; error?: string } | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchSpecializations();
        setSpecs(data.specializations || []);
      } catch { /* server down */ }
      finally { setLoading(false); }
    }
    void load();
  }, []);

  const handleSubmit = async () => {
    if (!selected || !prompt.trim()) return;
    setSubmitting(true);
    setResult(null);
    try {
      let data: unknown = null;
      if (taskData.trim()) {
        try { data = JSON.parse(taskData); } catch { data = taskData; }
      }
      const res = await createTask(selected, prompt, data);
      setResult({ ok: true, task_id: res.task_id });
      setPrompt('');
      setTaskData('');
    } catch (e) {
      setResult({ ok: false, error: (e as Error).message });
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <LoadingState label="جاري تحميل التخصصات..." />;

  if (selected) {
    const spec = specs.find((s) => s.name === selected);
    const Icon = getIcon(spec?.icon || '');
    const showDataField = selected === 'data_processor' || selected === 'validator' || selected === 'test_runner';

    return (
      <div className="space-y-4">
        <button onClick={() => { setSelected(null); setResult(null); }} className="btn-ghost text-sm">
          <ArrowRight size={16} className="inline ml-1" />
          رجوع للتخصصات
        </button>

        <div className="glass-card p-6">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-[#00d4ff]/20 to-blue-600/20 border border-[#00d4ff]/30 flex items-center justify-center">
              <Icon size={26} className="text-[#00d4ff]" />
            </div>
            <div className="flex-1">
              <h2 className="text-xl font-bold text-white">{SPECIALIZATION_LABELS[spec?.name || ''] || spec?.name}</h2>
              <p className="text-sm text-[#9ba8c4]">{spec?.description}</p>
            </div>
            {spec?.tool && (
              <span className="badge-info"><Wrench size={12} />{spec.tool}</span>
            )}
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-[#9ba8c4] mb-2">المهمة / الطلب</label>
              <textarea className="form-input" placeholder="اكتب ما تريد من الوكيل القيام به..." value={prompt} onChange={(e) => setPrompt(e.target.value)} rows={3} />
            </div>

            {showDataField && (
              <div>
                <label className="block text-sm font-semibold text-[#9ba8c4] mb-2">
                  {selected === 'test_runner' ? 'كود Python لتنفيذه' : 'البيانات (JSON أو أرقام)'}
                </label>
                <textarea
                  className="form-input font-mono text-sm"
                  placeholder={selected === 'test_runner' ? 'print("Hello World")' : '{"key": "value"} أو [1, 2, 3]'}
                  value={taskData}
                  onChange={(e) => setTaskData(e.target.value)}
                  rows={4}
                />
              </div>
            )}

            <button className="btn-primary w-full" onClick={() => void handleSubmit()} disabled={submitting || !prompt.trim()}>
              {submitting ? 'جاري الإرسال...' : <><Send size={16} className="inline ml-1" />إرسال المهمة</>}
            </button>

            {result && (
              <div className={`p-4 rounded-xl border ${
                result.ok ? 'bg-[#00e676]/10 border-[#00e676]/20 text-[#00e676]' : 'bg-[#ff5252]/10 border-[#ff5252]/20 text-[#ff5252]'
              }`}>
                <div className="flex items-center gap-2 font-semibold">
                  {result.ok ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
                  {result.ok ? `تم إنشاء المهمة: ${result.task_id}` : `خطأ: ${result.error}`}
                </div>
                {result.ok && <div className="text-xs mt-1 text-[#00e676]/70">تتبع المهمة في تبويب "المهام"</div>}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  if (specs.length === 0) {
    return <EmptyState icon={Layers} label="لا توجد تخصصات" sublabel="لم يتم تحميل التخصصات من الخادم" />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">التخصصات</h1>
        <p className="text-sm text-[#5c6b8a]">{specs.length} تخصص · اختر تخصصاً لإرسال مهمة</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {specs.map((spec) => {
          const Icon = getIcon(spec.icon);
          return (
            <button
              key={spec.name}
              onClick={() => { setSelected(spec.name); setResult(null); }}
              className="glass-card-hover p-5 text-right group"
            >
              <div className="flex items-start gap-3 mb-3">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#00d4ff]/15 to-blue-600/15 border border-[#00d4ff]/20 flex items-center justify-center group-hover:scale-110 transition-transform">
                  <Icon size={22} className="text-[#00d4ff]" />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="font-bold text-white text-sm">{SPECIALIZATION_LABELS[spec.name] || spec.name}</div>
                  <div className="text-xs text-[#5c6b8a] font-mono">{spec.name}</div>
                </div>
              </div>
              <p className="text-xs text-[#9ba8c4] mb-3 line-clamp-2 leading-relaxed">{spec.description}</p>
              <div className="flex items-center gap-2 text-xs">
                <span className="text-[#5c6b8a]">{spec.agents} وكلاء</span>
                {spec.tool && <span className="badge-info text-[10px]"><Wrench size={10} />{spec.tool}</span>}
                <ArrowRight size={14} className="text-[#00d4ff] mr-auto opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
