import { useState, useEffect, useCallback } from 'react';
import { LayoutDashboard, MessageSquare, Layers, Users, ListChecks, Cpu, Github } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { fetchSystemStatus, createEventSource } from '../api';
import type { SystemStatus, EventLog } from '../types';
import { Spinner } from './ui';

export type TabId = 'dashboard' | 'chat' | 'specializations' | 'agents' | 'tasks';

const TABS: { id: TabId; label: string; icon: LucideIcon }[] = [
  { id: 'dashboard', label: 'لوحة التحكم', icon: LayoutDashboard },
  { id: 'chat', label: 'المحادثة', icon: MessageSquare },
  { id: 'specializations', label: 'التخصصات', icon: Layers },
  { id: 'agents', label: 'الوكلاء', icon: Users },
  { id: 'tasks', label: 'المهام', icon: ListChecks },
];

export function AppShell({
  children,
  onNavigate,
  activeTab,
}: {
  children: (props: { status: SystemStatus | null; liveEvent: EventLog | null }) => React.ReactNode;
  onNavigate: (tab: TabId) => void;
  activeTab: TabId;
}) {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [liveEvent, setLiveEvent] = useState<EventLog | null>(null);
  const [statusError, setStatusError] = useState(false);

  const refreshStatus = useCallback(async () => {
    try {
      const s = await fetchSystemStatus();
      setStatus(s);
      setStatusError(false);
    } catch {
      setStatusError(true);
    }
  }, []);

  useEffect(() => {
    refreshStatus();
    const interval = setInterval(refreshStatus, 10000);

    let es: EventSource | null = null;
    try {
      es = createEventSource();
      es.onmessage = (e) => {
        try {
          const data = JSON.parse(e.data) as EventLog;
          if (data.event_type !== 'heartbeat') {
            setLiveEvent(data);
            if (data.event_type === 'task_completed' || data.event_type === 'task_created') {
              refreshStatus();
            }
          }
        } catch {
          /* ignore malformed events */
        }
      };
      es.onerror = () => {};
    } catch {
      /* SSE not available */
    }

    return () => {
      clearInterval(interval);
      es?.close();
    };
  }, [refreshStatus]);

  return (
    <div className="min-h-screen flex flex-col lg:flex-row">
      {/* Sidebar (desktop) / Top bar (mobile) */}
      <aside className="lg:w-64 lg:min-h-screen bg-base/90 backdrop-blur-xl border-l border-border flex flex-col sticky top-0 z-50 lg:fixed lg:right-0">
        {/* Brand */}
        <div className="p-5 flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-accent to-blue-600 flex items-center justify-center shadow-[0_0_20px_rgba(0,212,255,0.3)] animate-pulse-glow">
            <Cpu size={22} className="text-white" />
          </div>
          <div>
            <div className="font-bold text-base text-white leading-tight">AGOS Civilization</div>
            <div className="text-xs text-primary-muted">v3.0 · حضارة الوكلاء</div>
          </div>
        </div>

        {/* Status indicator */}
        <div className="px-5 pb-3">
          {status ? (
            <div className="flex items-center gap-2 text-xs">
              <span className="w-2 h-2 rounded-full bg-success dot-pulse" />
              <span className="text-primary-secondary">النظام يعمل</span>
              <span className="text-primary-muted mr-auto">{status.total_agents} وكيل</span>
            </div>
          ) : statusError ? (
            <div className="flex items-center gap-2 text-xs text-error">
              <span className="w-2 h-2 rounded-full bg-error" />
              <span>غير متصل بالخادم</span>
            </div>
          ) : (
            <div className="flex items-center gap-2 text-xs text-primary-muted">
              <Spinner size={14} />
              <span>جاري الاتصال...</span>
            </div>
          )}
        </div>

        {/* Nav */}
        <nav className="flex-1 px-3 py-2 flex lg:flex-col gap-1 overflow-x-auto lg:overflow-x-hidden">
          {TABS.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => onNavigate(tab.id)}
                className={`nav-tab whitespace-nowrap ${activeTab === tab.id ? 'nav-tab-active' : ''}`}
              >
                <Icon size={18} />
                {tab.label}
              </button>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="p-4 border-t border-border hidden lg:block">
          <a
            href="https://github.com/noos-prog/All-hand"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-xs text-primary-muted hover:text-accent transition-colors"
          >
            <Github size={16} />
            المستودع
          </a>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 lg:mr-64 p-4 lg:p-8 max-w-full overflow-hidden">
        <div className="max-w-6xl mx-auto animate-fade-in">{children({ status, liveEvent })}</div>
      </main>
    </div>
  );
}
