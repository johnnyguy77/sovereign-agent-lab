"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ['search_venues', 'get_venue_details']

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "No results found- A search for venues with a minimum capacity of 300 and a vegan option returned **0 results**."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True   # True or False

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
The result didn't change, I changed the script and saved it and then re-ran the script. However it was seem as available still, maybe it is becuase I haven't hange venue_tools.py
to full and they are still in sync.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 5  # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 2   # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
MCP gives us dynamic tool discovery at runtime; the agent connects to a server and learns
what tools are available, their schemas, and parameter descriptions automatically. This means
you can add, remove, or modify tools on the server side without changing a single line of
client/agent code. It also enables interoperability: any MCP-compatible agent can connect to
any MCP-compatible tool server, making tools reusable across different agents and frameworks
rather than locked into one codebase.
"""

# ── PyNanoClaw architecture — SPECULATION QUESTION ─────────────────────────
#
# (The variable below is still called WEEK_5_ARCHITECTURE because the
# grader reads that exact name. Don't rename it — but read the updated
# prompt: the question is now about PyNanoClaw, the hybrid system the
# final assignment will have you build.)
#
# This is a forward-looking, speculative question. You have NOT yet seen
# the material that covers the planner/executor split, memory, or the
# handoff bridge in detail — that is what the final assignment (releases
# 2026-04-18) is for. The point of asking it here is to check that you
# have read PROGRESS.md and can imagine how the Week 1 pieces grow into
# PyNanoClaw.
#
# Read PROGRESS.md in the repo root. Then write at least 5 bullet points
# describing PyNanoClaw as you imagine it at final-assignment scale.
#
# Each bullet should:
#   - Name a component (e.g. "Planner", "Memory store", "Handoff bridge",
#     "Rasa MCP gateway")
#   - Say in one clause what that component does and which half of
#     PyNanoClaw it lives in (the autonomous loop, the structured agent,
#     or the shared layer between them)
#
# You are not being graded on getting the "right" architecture — there
# isn't one right answer. You are being graded on whether your description
# is coherent and whether you have thought about which Week 1 file becomes
# which PyNanoClaw component.
#
# Example of the level of detail we want:
#   - The Planner is a strong-reasoning model (e.g. Nemotron-3-Super or
#     Qwen3-Next-Thinking) that takes the raw task and produces an ordered
#     list of subgoals. It lives upstream of the ReAct loop in the
#     autonomous-loop half of PyNanoClaw, so the Executor never sees an
#     ambiguous task.

WEEK_5_ARCHITECTURE = """
- The Planner sits upstream of the ReAct loop in the autonomous-loop half. It takes the raw task like Rod's WhatsApp message and breaks it down into subgoals, find a venue, check availability, get costs, hand off to confirm the booking, generate flyer, send email. That way the Executor doesn't have to figure out the big picture itself, it just works through the list.

- The Executor is basically research_agent.py from Week 1 but now it works through the Planner's subgoals instead of trying to reason about everything at once. It still lives in the autonomous loop half as a ReAct loop but has more tools now — web search, file ops, and a handoff tool that passes things to the Rasa side when a human conversation is needed.

- The Shared MCP Tool Server is mcp_venue_server.py grown up. It sits in the shared layer between both halves and serves all the tools — venue lookups, web search, calendar, email, booking. Both the loop and the structured agent discover tools from it dynamically so neither side has to hardcode anything, which is the whole point of MCP.

- The Handoff Bridge is in the shared layer and manages routing between the two halves. So when the Executor finds a venue and needs someone to actually confirm the deposit with the pub manager, it hands off to the Rasa agent. And if the Rasa agent gets a question it cant answer with its flows it hands back to the loop for more research.

- The Structured Agent is the exercise3_rasa CALM agent but now wired into PyNanoClaw as the structured agent half. It handles the high-stakes stuff like confirming deposits and talking to the pub manager, with deterministic flows and business rule guards so it cant just improvise with someone's money. It connects to the shared MCP server for live data.

- The Persistent Memory Store lives alongside the autonomous loop so it can remember things across subgoal steps like which venues were already rejected or what prices came back. Without this everything would have to fit in one LLM context window which wouldn't scale.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
-The LangGraph ReAct agent is the right one for research. It figured out on its own to chain tool calls together, like searching for venues then checking the weather then calculating catering costs, without me telling it the order. It reasoned about what to do next based on what came back. You couldn't script that in advance because the next step depends on what the search returns.
-The Rasa CALM agent is the right one for the pub manager call, in exercise 3 it followed explicit flows with business rule guards so it couldn't just improvise. When I tried to get it to do something outside its defined flows it pushed back, which is exactly what you want when someone's confirming a deposit with real money.
- Swapping them would be wrong both ways. If you used Rasa for the research it would need predefined flows for every possible search path, which is impossible when you don't know what venues exist or what constraints will matter. And if you used the ReAct agent for the confirmation call it could hallucinate or skip a validation step there's nothing stopping it from confirming a booking without checking the budget, it would just do whatever the LLM thinks is helpful. The whole point is using the right technology for each half of the problem.
"""