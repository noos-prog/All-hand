import type { TaskStatus, AgentStatus } from '../types';

export function StatusDot({ status }: { status: TaskStatus | AgentStatus }) {
  const colors: Record<string, string> = {
    completed: 'bg-[#00e676]',
    idle: 'bg-[#00e676]',
    failed: 'bg-[#ff5252]',
    running: 'bg-[#00d4ff]',
    working: 'bg-[#00d4ff]',
    queued: 'bg-[#ffab40]',
    stopped: 'bg-[#5c6b8a]',
  };
  const pulsing = status === 'running' || status === 'working' || status === 'queued';
  return (
    <span
      className={`inline-block w-2 h-2 rounded-full ${colors[status] || 'bg-[#5c6b8a]'} ${
        pulsing ? 'dot-pulse' : ''
      }`}
    />
  );
}

export function TaskStatusBadge({ status }: { status: TaskStatus }) {
  const config: Record<TaskStatus, { label: string; cls: string }> = {
    completed: { label: 'مكتملة', cls: 'badge-success' },
    failed: { label: 'فشلت', cls: 'badge-error' },
    running: { label: 'تعمل', cls: 'badge-info' },
    queued: { label: 'في الانتظار', cls: 'badge-warning' },
  };
  const { label, cls } = config[status] || config.queued;
  return (
    <span className={cls}>
      <StatusDot status={status} />
      {label}
    </span>
  );
}

export function AgentStatusBadge({ status }: { status: AgentStatus }) {
  const config: Record<AgentStatus, { label: string; cls: string }> = {
    idle: { label: 'خامل', cls: 'badge-success' },
    working: { label: 'يعمل', cls: 'badge-info' },
    stopped: { label: 'متوقف', cls: 'badge-warning' },
  };
  const { label, cls } = config[status] || config.idle;
  return (
    <span className={cls}>
      <StatusDot status={status} />
      {label}
    </span>
  );
}

export function LlmStatusBadge({ configured, model }: { configured: boolean; model: string }) {
  if (configured) {
    return (
      <span className="badge-success">
        <span className="w-2 h-2 rounded-full bg-[#00e676] dot-pulse" />
        {model}
      </span>
    );
  }
  return (
    <span className="badge-warning">
      <span className="w-2 h-2 rounded-full bg-[#ffab40]" />
      يحتاج مفتاح API
    </span>
  );
}

export function formatUptime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `${h}س ${m}د ${s}ث`;
}

export function formatTimestamp(ts: string | number): string {
  const date = typeof ts === 'number' ? new Date(ts * 1000) : new Date(ts);
  return date.toLocaleString('ar-EG', { hour: '2-digit', minute: '2-digit', day: 'numeric', month: 'short' });
}
