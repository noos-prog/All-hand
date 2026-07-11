import { useState, useEffect, useCallback } from 'react';
import { ListChecks, RefreshCw, ChevronDown, Clock, Wrench, CheckCircle2, XCircle } from 'lucide-react';
import { fetchTasks } from '../api';
import type { Task, EventLog, TaskResult, TaskStatus } from '../types';
import { getIcon, SPECIALIZATION_LABELS } from '../icons';
import { LoadingState, EmptyState } from './ui';
import { TaskStatusBadge, formatTimestamp } from './status';

const STATUS_FILTERS: { key: 'all' | TaskStatus; label: string }[] = [
  { key: 'all', label: 'الكل' },
  { key: 'completed', label: 'مكتملة' },
  { key: 'failed', label: 'فشلت' },
  { key: 'running', label: 'تعمل' },
  { key: 'queued', label: 'في الانتظار' },
];

export function Tasks({ liveEvent }: { liveEvent: EventLog | null }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | TaskStatus>('all');
  const [expanded, setExpanded] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      const data = await fetchTasks(100);
      setTasks(data.tasks || []);
    } catch {
      /* server down */
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
    const interval = setInterval(load, 10000);
    return () => clearInterval(interval);
  }, [load]);

  useEffect(() => {
    if (liveEvent && (liveEvent.event_type === 'task_completed' || liveEvent.event_type === 'task_created')) {
      void load();
    }
  }, [liveEvent, load]);

  const filtered = filter === 'all' ? tasks : tasks.filter((t) => (t.status as string) === filter);

  const counts = tasks.reduce(
    (acc, t) => {
      const s = (typeof t.status === 'string' ? t.status : 'queued') as TaskStatus;
      acc[s] = (acc[s] || 0) + 1;
      return acc;
    },
    {} as Record<TaskStatus, number>,
  );

  if (loading) {
    return <LoadingState label="جاري تحميل المهام..." />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="glass-card p-5">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div>
            <h1 className="text-xl font-bold text-white">{tasks.length} مهمة</h1>
            <div className="flex gap-2 mt-1 flex-wrap">
              <span className="badge-success text-[10px]">{counts.completed || 0} مكتملة</span>
              <span className="badge-error text-[10px]">{counts.failed || 0} فشلت</span>
              <span className="badge-info text-[10px]">{(counts.running || 0) + (counts.queued || 0)} قيد التشغيل</span>
            </div>
          </div>
          <button className="btn-ghost text-sm" onClick={() => void load()}>
            <RefreshCw size={14} className="inline ml-1" />
            تحديث
          </button>
        </div>

        <div className="flex gap-2 mt-4 flex-wrap">
          {STATUS_FILTERS.map((f) => (
            <button
              key={f.key}
              className={`text-xs px-3 py-1.5 rounded-lg transition-all ${
                filter === f.key
                  ? 'bg-accent/20 text-accent border border-accent/30'
                  : 'bg-elevated/50 text-primary-secondary hover:bg-hover'
              }`}
              onClick={() => setFilter(f.key)}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>

      {/* Task list */}
      {filtered.length === 0 ? (
        <EmptyState icon={ListChecks} label="لا توجد مهام" sublabel="المهام ستظهر هنا فور إنشائها" />
      ) : (
        <div className="space-y-3">
          {filtered.map((task) => {
            const taskId = task.task_id || task.id;
            const status = (typeof task.status === 'string' ? task.status : 'queued') as TaskStatus;
            const isExpanded = expanded === taskId;
            const Icon = getIcon(task.specialization);

            return (
              <div
                key={taskId}
                className="glass-card-hover overflow-hidden cursor-pointer animate-slide-up"
                onClick={() => setExpanded(isExpanded ? null : taskId ?? null)}
              >
                <div className="p-4 flex items-start gap-3">
                  <div className="w-9 h-9 rounded-xl bg-elevated/60 border border-border flex items-center justify-center flex-shrink-0">
                    <Icon size={16} className="text-accent" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <span className="text-sm font-semibold text-white">
                        {SPECIALIZATION_LABELS[task.specialization] || task.specialization}
                      </span>
                      {task.agent_name && (
                        <span className="badge-info text-[10px] font-mono">{task.agent_name}</span>
                      )}
                      <TaskStatusBadge status={status} />
                      <ChevronDown
                        size={16}
                        className={`text-primary-muted mr-auto transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                      />
                    </div>
                    <p className="text-sm text-primary-secondary truncate">{task.prompt}</p>
                    <div className="flex items-center gap-3 mt-1.5 text-xs text-primary-muted flex-wrap">
                      <span className="font-mono">{taskId}</span>
                      {task.elapsed_s != null && (
                        <span className="flex items-center gap-1">
                          <Clock size={10} />
                          {task.elapsed_s}s
                        </span>
                      )}
                      {task.created_at && <span>{formatTimestamp(task.created_at)}</span>}
                    </div>
                  </div>
                </div>

                {isExpanded && task.result && (
                  <TaskResultDetail result={task.result} />
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function TaskResultDetail({ result }: { result: TaskResult }) {
  const r = result.result || {};
  const answer = r.answer || r.error || null;
  const toolOutput = r.tool_output;

  return (
    <div className="px-4 pb-4 space-y-2 animate-slide-down">
      {toolOutput && (
        <div className="bg-elevated/40 rounded-xl p-3 border border-border/50">
          <div className="flex items-center gap-2 text-accent font-mono text-xs mb-2">
            <Wrench size={12} />
            أداة: {toolOutput.tool}
          </div>
          <pre className="text-xs text-primary-secondary font-mono whitespace-pre-wrap break-words max-h-40 overflow-y-auto">
            {JSON.stringify(toolOutput, null, 2).slice(0, 600)}
          </pre>
        </div>
      )}
      {answer && (
        <div className="bg-elevated/40 rounded-xl p-3 border border-border/50">
          <div className="flex items-center gap-2 mb-2">
            {result.ok ? (
              <CheckCircle2 size={14} className="text-success" />
            ) : (
              <XCircle size={14} className="text-error" />
            )}
            <span className={`text-xs font-semibold ${result.ok ? 'text-success' : 'text-error'}`}>
              {result.ok ? 'النتيجة' : 'خطأ'}
            </span>
          </div>
          <div className="text-sm text-primary whitespace-pre-wrap break-words max-h-60 overflow-y-auto">
            {answer.slice(0, 1200)}
            {answer.length > 1200 && '...'}
          </div>
        </div>
      )}
      {r.model && (
        <div className="text-xs text-primary-muted font-mono px-1">النموذج: {r.model}</div>
      )}
    </div>
  );
}
