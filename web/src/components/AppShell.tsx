import { useState, useEffect, useCallback } from 'react';
import { LayoutDashboard, MessageSquare, Layers, Users, ListChecks, Cpu, Github, AlertCircle } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { fetchSystemStatus } from '../api';
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

interface AppShellProps {
  activeTab: TabId;
  onNavigate: (tab: TabId) => void;
  children: (props: { status: SystemStatus | null; liveEvent: EventLog | null }) => React.ReactNode;
}

export function AppShell({ activeTab, onNavigate, children }: AppShellProps) {
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
    void refreshStatus();
    const interval = setInterval(refreshStatus, 10000);
    return () => clearInterval(interval);
  }, [refreshStatus]);

  // Poll events for live updates (SSE not available with edge functions, use polling)
  useEffect(() => {
    let lastEventId = 0;
    const pollEvents = async () => {
      try {
        const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || '';
        const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || '';
        const res = await fetch(
          `${SUPABASE_URL}/rest/v1/agos_events?order=id.desc&limit=1`,
          {
            headers: {
              'apikey': SUPABASE_ANON_KEY,
              'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
            },
          },
        );
        if (res.ok) {
          const data = await res.json();
          if (data.length > 0 && data[0].id > lastEventId) {
            lastEventId = data[0].id;
            setLiveEvent(data[0]);
            if (data[0].event_type === 'task_completed' || data[0].event_type === 'task_created') {
              void refreshStatus();
            }
          }
        }
      } catch {
        /* ignore */
      }
    };
    void pollEvents();
    const interval = setInterval(pollEvents, 5000);
    return () => clearInterval(interval);
  }, [refreshStatus]);

  return (
    <div className="min-h-screen flex flex-col lg:flex-row">
      {/* Sidebar */}
      <aside className="lg:w-64 lg:min-h-screen bg-[#0a0e1a]/90 backdrop-blur-xl border-l border-[#2a3550] flex flex-col sticky top-0 z-50 lg:fixed lg:right-0">
        <div className="p-5 flex items-center gap-3">
          <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-[#00d4ff] to-blue-600 flex items-center justify-center shadow-[0_0_20px_rgba(0,212,255,0.3)]">
            <Cpu size={22} className="text-white" />
          </div>
          <div>
            <div className="font-bold text-base text-white leading-tight">AGOS Civilization</div>
            <div className="text-xs text-[#5c6b8a]">v4.0 · حضارة الوكلاء</div>
          </div>
        </div>

        <div className="px-5 pb-3">
          {status ? (
            <div className="flex items-center gap-2 text-xs">
              <span className="w-2 h-2 rounded-full bg-[#00e676] dot-pulse" />
              <span className="text-[#9ba8c4]">النظام يعمل</span>
              <span className="text-[#5c6b8a] mr-auto">{status.total_agents} وكيل</span>
            </div>
          ) : statusError ? (
            <div className="flex items-center gap-2 text-xs text-[#ff5252]">
              <AlertCircle size={12} />
              <span>غير متصل بالخادم</span>
            </div>
          ) : (
            <div className="flex items-center gap-2 text-xs text-[#5c6b8a]">
              <Spinner size={14} />
              <span>جاري الاتصال...</span>
            </div>
          )}
        </div>

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

        <div className="p-4 border-t border-[#2a3550] hidden lg:block">
          <a
            href="https://github.com/noos-prog/All-hand"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 text-xs text-[#5c6b8a] hover:text-[#00d4ff] transition-colors"
          >
            <Github size={16} />
            المستودع
          </a>
        </div>
      </aside>

      <main className="flex-1 lg:mr-64 p-4 lg:p-8 max-w-full overflow-hidden">
        <div className="max-w-6xl mx-auto animate-fade-in">{children({ status, liveEvent })}</div>
      </main>
    </div>
  );
}
