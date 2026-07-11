import { useState, useEffect } from 'react';
import {
  Users, CheckCircle2, XCircle, Cpu, Database, Clock, Activity, Zap,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { fetchEvents } from '../api';
import type { SystemStatus, EventLog } from '../types';
import { LoadingState, EmptyState } from './ui';
import { LlmStatusBadge, formatUptime, formatTimestamp, StatusDot } from './status';

function StatCard({
  icon: Icon,
  label,
  value,
  sub,
  accent = 'text-accent',
  children,
}: {
  icon: LucideIcon;
  label: string;
  value: string | number;
  sub?: React.ReactNode;
  accent?: string;
  children?: React.ReactNode;
}) {
  return (
    <div className="glass-card-hover p-5 animate-slide-up">
      <div className="flex items-start justify-between mb-3">
        <div className="w-10 h-10 rounded-xl bg-elevated/60 border border-border flex items-center justify-center">
          <Icon size={18} className={accent} />
        </div>
      </div>
      <div className="text-sm text-primary-muted mb-1">{label}</div>
      <div className="text-2xl font-bold text-white mb-1 truncate">{value}</div>
      {sub && <div className="text-xs text-primary-secondary">{sub}</div>}
      {children}
    </div>
  );
}

export function Dashboard({
  status,
  liveEvent,
}: {
  status: SystemStatus | null;
  liveEvent: EventLog | null;
}) {
  const [events, setEvents] = useState<EventLog[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let mounted = true;
    async function load() {
      try {
        const data = await fetchEvents(30);
        if (mounted) setEvents(data.events || []);
      } catch {
        /* server might be down */
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    const interval = setInterval(load, 15000);
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, [liveEvent]);

  if (!status) {
    return <LoadingState label="جاري تحميل حالة النظام..." />;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white mb-1">لوحة التحكم</h1>
        <p className="text-sm text-primary-muted">نظرة شاملة على حضارة الوكلاء</p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <StatCard
          icon={Users}
          label="الوكلاء النشطون"
          value={status.total_agents}
          sub={`${status.specializations} تخصص · ${status.external_agents} خارجي`}
          accent="text-accent"
        />
        <StatCard
          icon={CheckCircle2}
          label="المهام المكتملة"
          value={status.tasks_completed}
          sub={
            <>
              <XCircle size={12} className="inline ml-1 text-error" />
              {status.tasks_failed} فشلت
            </>
          }
          accent="text-success"
        />
        <StatCard
          icon={Cpu}
          label="نموذج LLM"
          value={status.llm_configured ? status.llm_model.split('/').pop() || status.llm_model : 'غير مهيأ'}
          accent="text-accent"
        >
          <div className="mt-2">
            <LlmStatusBadge configured={status.llm_configured} model={status.llm_model} />
          </div>
        </StatCard>
        <StatCard
          icon={Database}
          label="قاعدة البيانات"
          value={status.supabase_configured ? 'Supabase' : 'في الذاكرة'}
          sub={
            status.tasks_in_db !== null
              ? `${status.tasks_in_db} مهمة محفوظة`
              : `${status.tasks_in_memory} في الذاكرة`
          }
          accent="text-accent"
        />
        <StatCard
          icon={Clock}
          label="مدة التشغيل"
          value={formatUptime(status.uptime_s)}
          accent="text-warning"
        >
          <div className="mt-2">
            <span className="badge-success">
              <span className="w-2 h-2 rounded-full bg-success dot-pulse" />
              يعمل
            </span>
          </div>
        </StatCard>
        <StatCard
          icon={Activity}
          label="آخر حدث"
          value={liveEvent ? liveEvent.event_type : 'في انتظار...'}
          sub={liveEvent?.event_data?.agent ? `الوكيل: ${String(liveEvent.event_data.agent)}` : '\u00A0'}
          accent="text-accent"
        >
          {liveEvent && (
            <div className="mt-2 flex items-center gap-1.5 text-xs text-accent">
              <Zap size={12} className="animate-pulse" />
              <span>مباشر</span>
            </div>
          )}
        </StatCard>
      </div>

      {/* Events log */}
      <div className="glass-card p-5">
        <div className="flex items-center gap-2 mb-4">
          <Activity size={18} className="text-accent" />
          <h2 className="font-semibold text-white">سجل الأحداث المباشر</h2>
          <span className="w-2 h-2 rounded-full bg-success dot-pulse mr-auto" />
        </div>

        {loading ? (
          <LoadingState label="جاري تحميل الأحداث..." />
        ) : events.length === 0 ? (
          <EmptyState icon={Activity} label="لا توجد أحداث بعد" sublabel="الأحداث ستظهر هنا فور نشاط الوكلاء" />
        ) : (
          <div className="space-y-2 max-h-[400px] overflow-y-auto">
            {events.map((ev, i) => (
              <div
                key={ev.id || `${ev.created_at}-${i}`}
                className="flex items-start gap-3 p-3 rounded-xl bg-elevated/30 border border-border/50 hover:border-border transition-colors animate-slide-up"
              >
                <div className="mt-1">
                  <StatusDot
                    status={
                      ev.event_type === 'task_completed'
                        ? 'completed'
                        : ev.event_type === 'chat_completed'
                          ? 'completed'
                          : 'queued'
                    }
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-sm font-semibold text-accent font-mono">{ev.event_type}</span>
                  </div>
                  <div className="text-xs text-primary-secondary truncate mt-0.5">
                    {ev.event_data ? JSON.stringify(ev.event_data).slice(0, 120) : ''}
                  </div>
                  <div className="text-xs text-primary-muted mt-0.5">
                    {formatTimestamp(ev.created_at)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
