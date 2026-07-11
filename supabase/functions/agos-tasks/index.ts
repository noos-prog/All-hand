import {
  corsHeaders, SPECIALIZATIONS, callLLM, generateTaskId,
  getSupabase, logEvent, upsertAgentStats,
} from "../_shared/agos.ts";

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 200, headers: corsHeaders });
  }

  const supabase = getSupabase();
  const url = new URL(req.url);
  const path = url.searchParams.get("task_id");

  try {
    // GET /api/tasks?limit=N — list tasks
    if (req.method === "GET" && !path) {
      const limit = Math.min(parseInt(url.searchParams.get("limit") || "50"), 200);
      const { data, error } = await supabase
        .from("agos_tasks")
        .select("*")
        .order("created_at", { ascending: false })
        .limit(limit);

      if (error) throw error;
      return new Response(JSON.stringify({ count: data.length, tasks: data, source: "database" }), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // GET /api/tasks?task_id=XXX — get single task
    if (req.method === "GET" && path) {
      const { data, error } = await supabase
        .from("agos_tasks")
        .select("*")
        .eq("task_id", path)
        .maybeSingle();

      if (error) throw error;
      if (!data) {
        return new Response(JSON.stringify({ error: "task not found" }), {
          status: 404,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }
      return new Response(JSON.stringify(data), {
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // POST /api/tasks — create and execute a task
    if (req.method === "POST") {
      const { specialization, prompt, data: taskData } = await req.json();

      if (!specialization || !prompt) {
        return new Response(JSON.stringify({ error: "specialization and prompt are required" }), {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }

      if (!(specialization in SPECIALIZATIONS) && specialization !== "external") {
        return new Response(JSON.stringify({
          error: `Unknown specialization '${specialization}'. Valid: ${Object.keys(SPECIALIZATIONS).join(", ")} + ['external']`,
        }), {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" },
        });
      }

      const taskId = generateTaskId();
      const started = Date.now();

      // Insert task as queued
      await supabase.from("agos_tasks").insert({
        task_id: taskId,
        specialization,
        prompt: prompt.slice(0, 500),
        status: "queued",
      });

      await logEvent(supabase, "task_created", { task_id: taskId, specialization });

      // Pick agent
      const agentName = `${specialization}_${String(Math.floor(Math.random() * 3) + 1).padStart(4, "0")}`;

      // Update to running
      await supabase.from("agos_tasks")
        .update({ status: "running", agent_name: agentName })
        .eq("task_id", taskId);

      // Execute via LLM
      let enrichedPrompt = prompt;
      const toolOutput: Record<string, unknown> | null = null;

      // Tool: validate_json
      if (specialization === "validator" && typeof taskData === "string" && taskData.trim()) {
        try {
          const parsed = JSON.parse(taskData);
          const validation = {
            valid: true,
            type: Array.isArray(parsed) ? "array" : typeof parsed,
            keys: typeof parsed === "object" && !Array.isArray(parsed) ? Object.keys(parsed) : null,
          };
          enrichedPrompt += `\n\nReal JSON validation result:\n${JSON.stringify(validation)}`;
        } catch (e) {
          enrichedPrompt += `\n\nReal JSON validation result: {"valid":false,"error":"${e.message}"}`
        }
      }

      // Tool: compute_statistics
      if (specialization === "data_processor" && taskData != null) {
        const nums: number[] = [];
        const extract = (v: unknown) => {
          if (typeof v === "number") nums.push(v);
          else if (Array.isArray(v)) v.forEach(extract);
          else if (typeof v === "object" && v !== null) Object.values(v).forEach(extract);
          else if (typeof v === "string") {
            const n = parseFloat(v);
            if (!isNaN(n)) nums.push(n);
          }
        };
        extract(taskData);
        if (nums.length > 0) {
          const stats = {
            count: nums.length,
            sum: nums.reduce((a, b) => a + b, 0),
            mean: nums.reduce((a, b) => a + b, 0) / nums.length,
            min: Math.min(...nums),
            max: Math.max(...nums),
          };
          enrichedPrompt += `\n\nComputed real statistics on the provided data:\n${JSON.stringify(stats)}`;
        }
      }

      const system = SPECIALIZATIONS[specialization] || "You are a helpful agent.";
      const llmResult = await callLLM(system, enrichedPrompt);
      const elapsed = (Date.now() - started) / 1000;
      const ok = llmResult.ok;

      const result = {
        ok,
        agent: agentName,
        specialization,
        elapsed_s: Math.round(elapsed * 100) / 100,
        result: {
          answer: llmResult.ok ? llmResult.content : null,
          tool_output: toolOutput,
          llm_error: llmResult.ok ? undefined : llmResult.error,
          model: llmResult.model,
        },
      };

      // Update task with result
      await supabase.from("agos_tasks")
        .update({
          status: ok ? "completed" : "failed",
          agent_name: agentName,
          result: result,
          elapsed_s: result.elapsed_s,
          finished_at: new Date().toISOString(),
        })
        .eq("task_id", taskId);

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
        specialization,
        prev.tasks_completed + (ok ? 1 : 0),
        prev.tasks_failed + (ok ? 0 : 1),
        prev.total_time_s + elapsed,
      );

      await logEvent(supabase, "task_completed", {
        task_id: taskId,
        agent: agentName,
        specialization,
        ok,
        elapsed_s: result.elapsed_s,
      });

      return new Response(JSON.stringify({ task_id: taskId, status: ok ? "completed" : "failed" }), {
        status: 202,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});
