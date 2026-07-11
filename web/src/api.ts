import type {
  SystemStatus,
  Specialization,
  AgentSnapshot,
  Task,
  EventLog,
  ChatResponse,
  ExternalAgentForm,
} from './types';

const API_BASE = import.meta.env.VITE_API_BASE || '';

class ApiError extends Error {
  constructor(message: string, public status: number) {
    super(message);
  }
}

async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new ApiError(err.detail || `HTTP ${res.status}`, res.status);
  }
  return res.json() as Promise<T>;
}

export const fetchSystemStatus = () =>
  api<SystemStatus>('/api/system/status');

export const fetchSpecializations = () =>
  api<{ specializations: Specialization[] }>('/api/specializations');

export const fetchAgents = (spec?: string) =>
  api<{ count: number; agents: AgentSnapshot[] }>(
    `/api/agents${spec ? `?specialization=${spec}` : ''}`,
  );

export const fetchTasks = (limit = 50) =>
  api<{ count: number; tasks: Task[]; source: string }>(
    `/api/tasks?limit=${limit}`,
  );

export const fetchEvents = (limit = 50) =>
  api<{ count: number; events: EventLog[] }>(
    `/api/events?limit=${limit}`,
  );

export const createTask = (specialization: string, prompt: string, data?: unknown) =>
  api<{ task_id: string; status: string }>('/api/tasks', {
    method: 'POST',
    body: JSON.stringify({ specialization, prompt, data }),
  });

export const sendChat = (message: string) =>
  api<ChatResponse>('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message }),
  });

export const registerExternalAgent = (form: ExternalAgentForm) =>
  api<{ registered: AgentSnapshot }>('/api/agents/external', {
    method: 'POST',
    body: JSON.stringify({
      name: form.name,
      url: form.url,
      model: form.model,
      api_key: form.api_key,
    }),
  });

export const removeExternalAgent = (name: string) =>
  api<{ removed: string }>(`/api/agents/external/${name}`, {
    method: 'DELETE',
  });

export function createEventSource(): EventSource {
  return new EventSource(`${API_BASE}/api/events/stream`);
}

export { ApiError };
