import type {
  SystemStatus,
  Specialization,
  AgentSnapshot,
  Task,
  EventLog,
  ChatResponse,
  ExternalAgentForm,
} from './types';

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || '';
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || '';
const FUNCTION_BASE = `${SUPABASE_URL}/functions/v1`;

class ApiError extends Error {
  constructor(message: string, public status: number) {
    super(message);
  }
}

function authHeaders(): Record<string, string> {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
    'apikey': SUPABASE_ANON_KEY,
  };
}

async function callFunction<T>(name: string, params?: Record<string, string>, options?: RequestInit): Promise<T> {
  const url = new URL(`${FUNCTION_BASE}/${name}`);
  if (params) {
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));
  }
  const res = await fetch(url.toString(), {
    ...options,
    headers: { ...authHeaders(), ...options?.headers },
  });
  const body = await res.json().catch(() => ({ error: res.statusText }));
  if (!res.ok) {
    throw new ApiError(body.error || `HTTP ${res.status}`, res.status);
  }
  return body as T;
}

export const fetchSystemStatus = () =>
  callFunction<SystemStatus>('agos-system', { endpoint: 'status' });

export const fetchSpecializations = () =>
  callFunction<{ specializations: Specialization[] }>('agos-system', { endpoint: 'specializations' });

export const fetchAgents = (spec?: string) =>
  callFunction<{ count: number; agents: AgentSnapshot[] }>(
    'agos-system',
    { endpoint: 'agents', ...(spec ? { specialization: spec } : {}) },
  );

export const fetchTasks = (limit = 50) =>
  callFunction<{ count: number; tasks: Task[]; source: string }>(
    'agos-tasks',
    { limit: String(limit) },
  );

export const getTask = (taskId: string) =>
  callFunction<Task>('agos-tasks', { task_id: taskId });

export const fetchEvents = (limit = 50) =>
  callFunction<{ count: number; events: EventLog[] }>(
    'agos-system',
    { endpoint: 'events', limit: String(limit) },
  );

export const createTask = (specialization: string, prompt: string, data?: unknown) =>
  callFunction<{ task_id: string; status: string }>('agos-tasks', undefined, {
    method: 'POST',
    body: JSON.stringify({ specialization, prompt, data }),
  });

export const sendChat = (message: string) =>
  callFunction<ChatResponse>('agos-chat', undefined, {
    method: 'POST',
    body: JSON.stringify({ message }),
  });

export const registerExternalAgent = (form: ExternalAgentForm) =>
  callFunction<{ registered: AgentSnapshot }>('agos-system', { endpoint: 'register_external' }, {
    method: 'POST',
    body: JSON.stringify({ name: form.name, url: form.url, model: form.model, api_key: form.api_key }),
  });

export const removeExternalAgent = (name: string) =>
  callFunction<{ removed: string }>('agos-system', { endpoint: 'remove_external' }, {
    method: 'POST',
    body: JSON.stringify({ name }),
  });

export { ApiError };
