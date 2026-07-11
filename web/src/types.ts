export type AgentStatus = 'idle' | 'working' | 'stopped';

export interface AgentStats {
  tasks_completed: number;
  tasks_failed: number;
  total_time_s: number;
}

export interface AgentSnapshot {
  id: number;
  name: string;
  specialization: string;
  status: AgentStatus;
  stats: AgentStats;
}

export interface SystemStatus {
  status: string;
  uptime_s: number;
  llm_configured: boolean;
  llm_model: string;
  supabase_configured: boolean;
  specializations: number;
  total_agents: number;
  external_agents: number;
  tasks_completed: number;
  tasks_failed: number;
  tasks_in_memory: number;
  tasks_in_db: number | null;
}

export interface Specialization {
  name: string;
  description: string;
  agents: number;
  icon: string;
  tool: string | null;
}

export type TaskStatus = 'queued' | 'running' | 'completed' | 'failed';

export interface ToolOutput {
  tool: string;
  sources?: Array<{ title: string; snippet: string; url: string }>;
  statistics?: Record<string, number | string>;
  execution?: { exit_code: number; stdout: string; stderr: string; passed: boolean };
  validation?: { valid: boolean; error?: string; type?: string; keys?: string[] };
  metrics?: Record<string, number | string>;
}

export interface TaskResult {
  ok: boolean;
  agent: string;
  specialization: string;
  elapsed_s: number;
  result: {
    answer?: string | null;
    tool_output?: ToolOutput;
    llm_error?: string;
    model?: string;
    error?: string;
  };
}

export interface Task {
  id: string;
  specialization: string;
  prompt: string;
  status: TaskStatus;
  created_at: number;
  finished_at?: number;
  result?: TaskResult | null;
  agent?: string;
  agent_name?: string;
  task_id?: string;
  elapsed_s?: number;
}

export interface EventLog {
  id?: number;
  event_type: string;
  event_data: Record<string, unknown>;
  created_at: string | number;
}

export interface ChatResponse {
  task_id: string;
  routed_to: string;
  agent: string;
  outcome: TaskResult;
}

export interface ChatMessage {
  role: 'user' | 'agent';
  content: string;
  agent?: string;
  specialization?: string;
  elapsed?: number;
}

export interface ExternalAgentForm {
  name: string;
  url: string;
  model: string;
  api_key: string;
}
