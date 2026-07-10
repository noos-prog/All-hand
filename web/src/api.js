const API_BASE = import.meta.env.VITE_API_BASE || '';

async function api(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export const fetchSystemStatus = () => api('/api/system/status');
export const fetchSpecializations = () => api('/api/specializations');
export const fetchAgents = (spec) => api(`/api/agents${spec ? `?specialization=${spec}` : ''}`);
export const fetchTasks = (limit = 50) => api(`/api/tasks?limit=${limit}`);
export const fetchEvents = (limit = 50) => api(`/api/events?limit=${limit}`);
export const createTask = (specialization, prompt, data) =>
  api('/api/tasks', { method: 'POST', body: JSON.stringify({ specialization, prompt, data }) });
export const sendChat = (message) =>
  api('/api/chat', { method: 'POST', body: JSON.stringify({ message }) });
export const registerExternalAgent = (name, url, model, apiKey) =>
  api('/api/agents/external', { method: 'POST', body: JSON.stringify({ name, url, model, api_key: apiKey }) });
export const removeExternalAgent = (name) =>
  api(`/api/agents/external/${name}`, { method: 'DELETE' });

export function createEventSource() {
  return new EventSource(`${API_BASE}/api/events/stream`);
}
