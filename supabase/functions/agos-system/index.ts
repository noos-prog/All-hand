import {
  corsHeaders, SPECIALIZATIONS, SPECIALIZATION_ICONS, SPECIALIZATION_TOOLS,
  getSupabase,
} from "../_shared/agos.ts";

const AGENTS_PER_SPEC = 3;

interface AgentSnapshot {
  id: number;
  name: string;
  specialization: string;
  status: string;
  stats: { tasks_completed: number; tasks_failed: number; total_time_s: number };
}

function buildAgentRoster(statsMap: Map<string, { tasks_completed: number; tasks_failed: number; total_time_s: number }>) {
  const agents: AgentSnapshot[] = [];
  let id = 0;
  for (const spec of Object.keys(SPECIALIZATIONS)) {
    for (let i = 0; i < AGENTS_PER_SPEC; i++) {
      const name = `${spec}_${String(i + 1).padStart(4, "0")}`;
      const s = statsMap.get(name) || { tasks_completed: 0, tasks_failed: 0, total_time_s: 0 };
      agents.push({
        id,
        name,
        specialization: spec,
        status: s.tasks_completed > 0 ? "idle" : "idle",
        stats: s,
      });
      id++;
    }
  }
  return agents;
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  const supabase = getSupabase();
  const url = new URL(req.url);
  const endpoint = url.searchParams.get("endpoint") || url.pathname.split("/").pop() || "";

  try {
    // /api/system/status
    if (endpoint === "status") {
      const { data: stats } = await supabase.from("agos_agent_stats").select("*");
      const { count: taskCount } = await supabase.from("agos_tasks").select("*", { count: "exact", head: true });
      const { data: extAgents } = await supabase.from("agos_external_agents").select("*");

      const statsMap = new Map<string, { tasks_completed: number; tasks_failed: number; total_time_s: number }>();
      let totalCompleted = 0;
      let totalFailed = 0;
      for (const s of stats || []) {
        statsMap.set(s.agent_name, {
          tasks_completed: s.tasks_completed,
          tasks_failed: s.tasks_failed,
          total_time_s: s.total_time_s,
        });
        totalCompleted += s.tasks_completed;
        totalFailed += s.tasks_failed;
      }

      const agents = buildAgentRoster(statsMap);
      const apiKeyConfigured = !!Deno.env.get("OPENROUTER_API_KEY");

      return new Response(JSON.stringify({
        status: "healthy",
        uptime_s: 0,
        llm_configured: apiKeyConfigured,
        llm_model: Deno.env.get("LLM_MODEL") || "meta-llama/llama-3.3-70b-instruct:free",
        supabase_configured: true,
        specializations: Object.keys(SPECIALIZATIONS).length,
        total_agents: agents.length,
        external_agents: extAgents?.length || 0,
        tasks_completed: totalCompleted,
        tasks_failed: totalFailed,
        tasks_in_memory: 0,
        tasks_in_db: taskCount || 0,
      }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // /api/specializations
    if (endpoint === "specializations") {
      const specs = Object.entries(SPECIALIZATIONS).map(([name, prompt]) => ({
        name,
        description: prompt.split(".")[0],
        agents: AGENTS_PER_SPEC,
        icon: SPECIALIZATION_ICONS[name] || "robot",
        tool: SPECIALIZATION_TOOLS[name] || null,
      }));
      return new Response(JSON.stringify({ specializations: specs }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // /api/agents
    if (endpoint === "agents") {
      const filter = url.searchParams.get("specialization");
      const { data: stats } = await supabase.from("agos_agent_stats").select("*");
      const { data: extAgents } = await supabase.from("agos_external_agents").select("*");

      const statsMap = new Map<string, { tasks_completed: number; tasks_failed: number; total_time_s: number }>();
      for (const s of stats || []) {
        statsMap.set(s.agent_name, {
          tasks_completed: s.tasks_completed,
          tasks_failed: s.tasks_failed,
          total_time_s: s.total_time_s,
        });
      }

      let agents = buildAgentRoster(statsMap);

      // Add external agents
      for (const ext of extAgents || []) {
        agents.push({
          id: 10000 + Math.floor(Math.random() * 1000),
          name: ext.name,
          specialization: "external",
          status: "idle",
          stats: { tasks_completed: 0, tasks_failed: 0, total_time_s: 0 },
        });
      }

      if (filter) {
        agents = agents.filter((a) => a.specialization === filter);
      }

      return new Response(JSON.stringify({ count: agents.length, agents }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // /api/events
    if (endpoint === "events") {
      const limit = Math.min(parseInt(url.searchParams.get("limit") || "50"), 200);
      const { data, error } = await supabase
        .from("agos_events")
        .select("*")
        .order("created_at", { ascending: false })
        .limit(limit);

      if (error) throw error;
      return new Response(JSON.stringify({ count: data.length, events: data }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // /api/agents/external — register
    if (endpoint === "register_external" && req.method === "POST") {
      const { name, url: agentUrl, model, api_key } = await req.json();
      if (!name || !agentUrl) {
        return new Response(JSON.stringify({ error: "name and url are required" }), {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
      const { data, error } = await supabase
        .from("agos_external_agents")
        .insert({ name, url: agentUrl, model: model || "", api_key: api_key || "" })
        .select("*")
        .maybeSingle();

      if (error) {
        return new Response(JSON.stringify({ error: error.message }), {
          status: 409,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
      return new Response(JSON.stringify({ registered: data }), {
        status: 201,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // /api/agents/external — delete
    if (endpoint === "remove_external" && req.method === "POST") {
      const { name } = await req.json();
      await supabase.from("agos_external_agents").delete().eq("name", name);
      return new Response(JSON.stringify({ removed: name }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // Root — API info
    return new Response(JSON.stringify({
      name: "AGOS Agent Civilization",
      version: "4.0.0",
      status: "alive",
      specializations: Object.keys(SPECIALIZATIONS),
      endpoints: ["status", "specializations", "agents", "events", "register_external", "remove_external"],
    }), {
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
