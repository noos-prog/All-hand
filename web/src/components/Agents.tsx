import { useState, useEffect, useCallback } from 'react';
import { Plus, Trash2, Users, X, ExternalLink } from 'lucide-react';
import { fetchAgents, fetchSpecializations, registerExternalAgent, removeExternalAgent } from '../api';
import type { AgentSnapshot, Specialization, ExternalAgentForm } from '../types';
import { getIcon, SPECIALIZATION_LABELS } from '../icons';
import { LoadingState, EmptyState } from './ui';
import { AgentStatusBadge } from './status';

export function Agents() {
  const [agents, setAgents] = useState<AgentSnapshot[]>([]);
  const [specs, setSpecs] = useState<Specialization[]>([]);
  const [filter, setFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState<ExternalAgentForm>({ name: '', url: '', model: '', api_key: '' });
  const [formError, setFormError] = useState('');

  const load = useCallback(async () => {
    try {
      const [agentsData, specsData] = await Promise.all([fetchAgents(), fetchSpecializations()]);
      setAgents(agentsData.agents || []);
      setSpecs(specsData.specializations || []);
    } catch { /* server down */ }
    finally { setLoading(false); }
  }, []);

  useEffect(() => {
    void load();
    const interval = setInterval(load, 20000);
    return () => clearInterval(interval);
  }, [load]);

  const handleRegister = async () => {
    if (!formData.name.trim() || !formData.url.trim()) {
      setFormError('الاسم والـ URL مطلوبان');
      return;
    }
    try {
      await registerExternalAgent(formData);
      setShowModal(false);
      setFormData({ name: '', url: '', model: '', api_key: '' });
      setFormError('');
      void load();
    } catch (e) {
      setFormError((e as Error).message);
    }
  };

  const handleRemove = async (name: string) => {
    if (!confirm(`حذف الوكيل "${name}"؟`)) return;
    try { await removeExternalAgent(name); void load(); } catch { /* ignore */ }
  };

  const filtered = filter ? agents.filter((a) => a.specialization === filter) : agents;
  const specGroups: Record<string, AgentSnapshot[]> = {};
  filtered.forEach((a) => {
    if (!specGroups[a.specialization]) specGroups[a.specialization] = [];
    specGroups[a.specialization].push(a);
  });

  if (loading) return <LoadingState label="جاري تحميل الوكلاء..." />;
  if (agents.length === 0) return <EmptyState icon={Users} label="لا يوجد وكلاء" sublabel="لم يتم تحميل الوكلاء من الخادم" />;

  return (
    <div className="space-y-6">
      <div className="glass-card p-5">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div>
            <h1 className="text-xl font-bold text-white">{agents.length} وكيل نشط</h1>
            <p className="text-xs text-[#5c6b8a] mt-0.5">
              {specs.length} تخصص · {agents.filter((a) => a.specialization === 'external').length} وكلاء خارجيون
            </p>
          </div>
          <button className="btn-primary text-sm" onClick={() => setShowModal(true)}>
            <Plus size={16} className="inline ml-1" />
            إضافة وكيل خارجي
          </button>
        </div>

        <div className="flex gap-2 mt-4 flex-wrap">
          <button
            className={`text-xs px-3 py-1.5 rounded-lg transition-all ${filter === '' ? 'bg-[#00d4ff]/20 text-[#00d4ff] border border-[#00d4ff]/30' : 'bg-[#1a2236]/50 text-[#9ba8c4] hover:bg-[#232d44]'}`}
            onClick={() => setFilter('')}
          >
            الكل
          </button>
          {specs.map((s) => (
            <button
              key={s.name}
              className={`text-xs px-3 py-1.5 rounded-lg transition-all ${filter === s.name ? 'bg-[#00d4ff]/20 text-[#00d4ff] border border-[#00d4ff]/30' : 'bg-[#1a2236]/50 text-[#9ba8c4] hover:bg-[#232d44]'}`}
              onClick={() => setFilter(s.name)}
            >
              {SPECIALIZATION_LABELS[s.name] || s.name}
            </button>
          ))}
        </div>
      </div>

      {Object.entries(specGroups).map(([specName, specAgents]) => {
        const Icon = getIcon(specName);
        return (
          <div key={specName}>
            <div className="flex items-center gap-2 mb-3">
              <Icon size={18} className="text-[#00d4ff]" />
              <h2 className="font-bold text-white">{SPECIALIZATION_LABELS[specName] || specName}</h2>
              <span className="badge-info text-[10px]">{specAgents.length}</span>
              <span className="text-xs text-[#5c6b8a] font-mono mr-auto">{specName}</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
              {specAgents.map((agent) => (
                <AgentCard key={agent.name} agent={agent} isExternal={agent.specialization === 'external'} onRemove={() => void handleRemove(agent.name)} />
              ))}
            </div>
          </div>
        );
      })}

      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm" onClick={() => setShowModal(false)}>
          <div className="glass-card p-6 w-full max-w-md" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-bold text-white">إضافة وكيل خارجي</h2>
              <button onClick={() => setShowModal(false)} className="text-[#5c6b8a] hover:text-[#e8ecf4] transition-colors">
                <X size={20} />
              </button>
            </div>
            <p className="text-xs text-[#5c6b8a] mb-4 flex items-center gap-1">
              <ExternalLink size={12} />
              أي وكيل يدعم OpenAI-compatible API (Ollama, LM Studio, vLLM...)
            </p>

            <div className="space-y-3">
              <div>
                <label className="block text-sm font-semibold text-[#9ba8c4] mb-1.5">الاسم</label>
                <input className="form-input" placeholder="my-ollama" value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
              </div>
              <div>
                <label className="block text-sm font-semibold text-[#9ba8c4] mb-1.5">URL</label>
                <input className="form-input font-mono text-sm" placeholder="http://localhost:11434/v1/chat/completions" value={formData.url} onChange={(e) => setFormData({ ...formData, url: e.target.value })} />
              </div>
              <div>
                <label className="block text-sm font-semibold text-[#9ba8c4] mb-1.5">النموذج (اختياري)</label>
                <input className="form-input font-mono text-sm" placeholder="llama3" value={formData.model} onChange={(e) => setFormData({ ...formData, model: e.target.value })} />
              </div>
              <div>
                <label className="block text-sm font-semibold text-[#9ba8c4] mb-1.5">API Key (اختياري)</label>
                <input className="form-input font-mono text-sm" type="password" placeholder="sk-..." value={formData.api_key} onChange={(e) => setFormData({ ...formData, api_key: e.target.value })} />
              </div>

              {formError && <div className="text-sm text-[#ff5252] bg-[#ff5252]/10 border border-[#ff5252]/20 rounded-lg px-3 py-2">{formError}</div>}

              <div className="flex gap-3 pt-2">
                <button className="btn-ghost flex-1" onClick={() => setShowModal(false)}>إلغاء</button>
                <button className="btn-primary flex-1" onClick={() => void handleRegister()}>إضافة</button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function AgentCard({ agent, isExternal, onRemove }: { agent: AgentSnapshot; isExternal: boolean; onRemove: () => void }) {
  return (
    <div className="glass-card-hover p-4 group">
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="font-mono text-sm font-bold text-white">{agent.name}</div>
          {isExternal && <span className="badge-warning text-[10px] mt-1">خارجي</span>}
        </div>
        <AgentStatusBadge status={agent.status} />
      </div>

      <div className="grid grid-cols-3 gap-2 text-center">
        <div className="bg-[#1a2236]/30 rounded-lg py-2">
          <div className="text-[10px] text-[#5c6b8a]">مكتملة</div>
          <div className="text-sm font-bold text-[#00e676]">{agent.stats?.tasks_completed || 0}</div>
        </div>
        <div className="bg-[#1a2236]/30 rounded-lg py-2">
          <div className="text-[10px] text-[#5c6b8a]">فشلت</div>
          <div className="text-sm font-bold text-[#ff5252]">{agent.stats?.tasks_failed || 0}</div>
        </div>
        <div className="bg-[#1a2236]/30 rounded-lg py-2">
          <div className="text-[10px] text-[#5c6b8a]">الوقت</div>
          <div className="text-sm font-bold text-[#00d4ff]">{(agent.stats?.total_time_s || 0).toFixed(1)}s</div>
        </div>
      </div>

      {isExternal && (
        <button className="btn-danger w-full mt-3 text-xs" onClick={onRemove}>
          <Trash2 size={12} className="inline ml-1" />
          حذف
        </button>
      )}
    </div>
  );
}
