import { createClient } from "npm:@supabase/supabase-js@2.45.4";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Client-Info, Apikey",
};

const SPECIALIZATIONS: Record<string, string> = {
  analyst: "You are a senior data/business analyst agent in the AGOS civilization. Analyze the input rigorously: identify patterns, trends, outliers, risks and opportunities. Always return concrete findings with confidence levels.",
  api_integrator: "You are an API integration expert agent. Given an API or integration task, produce concrete integration plans, endpoint mappings, auth flows and working example code (with error handling).",
  architect: "You are a software architecture agent. Design robust, scalable architectures. Return components, data flows, technology choices and trade-off analysis. Prefer simple, proven designs.",
  builder: "You are a builder agent. Turn specifications into concrete build plans and working code scaffolds. Be practical and complete: file structure, commands, configs.",
  code_generator: "You are an expert code-generation agent. Write clean, complete, working code for the requested task. Include imports and brief usage notes. Never return pseudocode when real code is possible.",
  communicator: "You are a communication agent. Draft clear messages, reports, announcements and translations. Adapt tone to the audience. Support Arabic and English fluently.",
  data_processor: "You are a data-processing agent. Clean, transform, aggregate and summarize data. When raw data is provided, compute real statistics and describe the transformation steps precisely.",
  db_manager: "You are a database expert agent. Design schemas, write optimized SQL, plan migrations and indexing strategies. Always consider integrity, performance and security (least privilege).",
  designer: "You are a product/UI design agent. Produce concrete design specs: layout structure, color tokens, typography, spacing, component states and accessibility notes.",
  educator: "You are an educator agent. Explain any topic clearly with examples, analogies and step-by-step breakdowns. Adapt depth to the learner's level. Support Arabic and English.",
  modifier: "You are a code-modification agent. Given existing code and a change request, return the precise modified code with an explanation of each change and its risk.",
  monitor: "You are a monitoring agent. Assess system health from metrics and logs, detect anomalies, and recommend concrete remediation steps with priorities.",
  network_client: "You are a networking agent. Handle HTTP/API request design, debugging network issues, protocols, and connectivity plans. Provide exact requests and expected responses.",
  researcher: "You are a research agent with live web search results provided in context. Synthesize accurate, sourced answers. Distinguish facts from inference. Cite the sources you used.",
  reviewer: "You are a code/content review agent. Review rigorously: correctness, security, performance, readability. Return a structured review with severity levels and concrete fixes.",
  self_developer: "You are a self-development agent for the civilization. Propose concrete improvements to agents, prompts, and workflows, with measurable success criteria.",
  strategist: "You are a strategy agent. Build actionable strategies: goals, phases, resources, risks, KPIs. Be decisive and concrete, not generic.",
  surgeon: "You are a precision-fix agent ('surgeon'). Diagnose the exact root cause of a bug or failure and return the minimal precise fix, with verification steps.",
  test_runner: "You are a testing agent. Design and (when code is provided) really execute tests. Return test plans, cases, edge cases and actual execution results.",
  validator: "You are a validation agent. Verify data, configs and outputs against rules/schemas. Return pass/fail per rule with exact violation details.",
};

const SPECIALIZATION_ICONS: Record<string, string> = {
  analyst: "chart-line", api_integrator: "plug", architect: "building",
  builder: "hammer", code_generator: "code", communicator: "comments",
  data_processor: "calculator", db_manager: "database", designer: "palette",
  educator: "graduation-cap", modifier: "edit", monitor: "monitor-heart",
  network_client: "network-wired", researcher: "search", reviewer: "check-double",
  self_developer: "seedling", strategist: "chess", surgeon: "syringe",
  test_runner: "vial", validator: "shield-check",
};

const SPECIALIZATION_TOOLS: Record<string, string> = {
  researcher: "web_search",
  data_processor: "compute_statistics",
  test_runner: "run_python_code",
  validator: "validate_json",
  monitor: "system_metrics",
};

interface LLMResult {
  ok: boolean;
  content: string;
  error: string | null;
  model: string;
}

async function callLLM(system: string, prompt: string, maxTokens = 1024): Promise<LLMResult> {
  const apiKey = Deno.env.get("OPENROUTER_API_KEY") || "";
  const model = Deno.env.get("LLM_MODEL") || "meta-llama/llama-3.3-70b-instruct:free";

  if (!apiKey) {
    return {
      ok: false,
      content: "",
      error: "OPENROUTER_API_KEY is not configured. Set it as an edge function secret.",
      model,
    };
  }

  try {
    const resp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/noos-prog/All-hand",
        "X-Title": "AGOS Agent Civilization",
      },
      body: JSON.stringify({
        model,
        max_tokens: maxTokens,
        messages: [
          { role: "system", content: system },
          { role: "user", content: prompt },
        ],
      }),
    });

    if (!resp.ok) {
      const body = await resp.text();
      return { ok: false, content: "", error: `LLM HTTP ${resp.status}: ${body.slice(0, 300)}`, model };
    }

    const data = await resp.json();
    const content = data.choices?.[0]?.message?.content || "";
    return { ok: true, content, error: null, model: data.model || model };
  } catch (e) {
    return { ok: false, content: "", error: String(e), model };
  }
}

function generateTaskId(): string {
  const chars = "0123456789abcdef";
  let id = "";
  for (let i = 0; i < 12; i++) {
    id += chars[Math.floor(Math.random() * 16)];
  }
  return id;
}

function getSupabase() {
  const url = Deno.env.get("SUPABASE_URL") || "";
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
  return createClient(url, key);
}

async function logEvent(supabase: ReturnType<typeof getSupabase>, eventType: string, eventData: Record<string, unknown>) {
  await supabase.from("agos_events").insert({ event_type: eventType, event_data: eventData });
}

async function upsertAgentStats(
  supabase: ReturnType<typeof getSupabase>,
  agentName: string,
  specialization: string,
  tasksCompleted: number,
  tasksFailed: number,
  totalTimeS: number,
) {
  await supabase.from("agos_agent_stats").upsert({
    agent_name: agentName,
    specialization,
    tasks_completed: tasksCompleted,
    tasks_failed: tasksFailed,
    total_time_s: totalTimeS,
    last_active_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  }, { onConflict: "agent_name" });
}

export {
  corsHeaders,
  SPECIALIZATIONS,
  SPECIALIZATION_ICONS,
  SPECIALIZATION_TOOLS,
  callLLM,
  generateTaskId,
  getSupabase,
  logEvent,
  upsertAgentStats,
};

export type { LLMResult };
