import {
  corsHeaders, SPECIALIZATIONS, callLLM, generateTaskId,
  getSupabase, logEvent, upsertAgentStats,
} from "../_shared/agos.ts";

const ROUTER_SYSTEM = (
  "You are the dispatcher of an AI agent civilization with these specializations: "
  + Object.keys(SPECIALIZATIONS).join(", ")
  + ". Given a user command (in any language, including Arabic), reply with ONLY the single "
  + "best specialization name from the list, nothing else."
);

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  try {
    const { message } = await req.json();
    if (!message || typeof message !== "string") {
      return new Response(JSON.stringify({ error: "message is required" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const supabase = getSupabase();
    const started = Date.now();

    // Route to best specialization via LLM
    let spec = "communicator";
    const routeResult = await callLLM(ROUTER_SYSTEM, message, 20);
    if (routeResult.ok) {
      const candidate = routeResult.content.trim().toLowerCase().replace(/-/g, "_");
      for (const name of Object.keys(SPECIALIZATIONS)) {
        if (candidate.includes(name)) {
          spec = name;
          break;
        }
      }
    }

    // Pick an agent (deterministic round-robin based on task count)
    const agentName = `${spec}_${String(Math.floor(Math.random() * 3) + 1).padStart(4, "0")}`;
    const system = SPECIALIZATIONS[spec];

    // Execute the task via LLM
    const llmResult = await callLLM(system, message);

    const elapsed = (Date.now() - started) / 1000;
    const ok = llmResult.ok;

    const result = {
      ok,
      agent: agentName,
      specialization: spec,
      elapsed_s: Math.round(elapsed * 100) / 100,
      result: {
        answer: llmResult.ok ? llmResult.content : null,
        llm_error: llmResult.ok ? undefined : llmResult.error,
        model: llmResult.model,
      },
    };

    // Persist task
    const taskId = generateTaskId();
    await supabase.from("agos_tasks").insert({
      task_id: taskId,
      specialization: spec,
      prompt: message.slice(0, 500),
      status: ok ? "completed" : "failed",
      agent_name: agentName,
      result: result,
      elapsed_s: result.elapsed_s,
      finished_at: new Date().toISOString(),
    });

    // Update agent stats
    const { data: existingStats } = await supabase
      .from("agos_agent_stats")
      .select("*")
      .eq("agent_name", agentName)
      .maybeSingle();

    const prev = existingStats || { tasks_completed: 0, tasks_failed: 0, total_time_s: 0 };
    await upsertAgentStats(
      supabase,
      agentName,
      spec,
      prev.tasks_completed + (ok ? 1 : 0),
      prev.tasks_failed + (ok ? 0 : 1),
      prev.total_time_s + elapsed,
    );

    // Log event
    await logEvent(supabase, "chat_completed", {
      task_id: taskId,
      agent: agentName,
      specialization: spec,
      ok,
    });

    return new Response(JSON.stringify({
      task_id: taskId,
      routed_to: spec,
      agent: agentName,
      outcome: result,
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
