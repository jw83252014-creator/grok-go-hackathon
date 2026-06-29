# Dashboard As Conscious Interface

**Status:** architecture note  
**Date:** 2026-06-09  
**Source context:** Agent Bridge / Grok chat exports in `~/Downloads/`

## Core Idea

The dashboard is not just a monitoring screen. In the Grok Go / Agent Bridge model, the dashboard is the organism's conscious interface: the place where many smaller agent-cells become visible, controllable, and discussable by a human operator.

The inner cells keep working in their own lanes. The Researcher and Mining Engine digest what happened below awareness. The dashboard is the upper interface where the system says, "Here is what I am doing, here is what hurts, here is what needs a decision, and here are the controls you can safely touch."

## Layer Model

```text
Human operator
  <-> conscious interface layer
      Dashboard, terminal surface, approvals, knobs, live controls
  <-> subconscious research layer
      Researcher, Mining Engine, NotebookLM, memory digestion, source maps
  <-> cellular execution layer
      Grok, Codex/Keystone, Null, Librarian, Frankenstein, Gemini, agents/cells
  <-> body substrate
      Mac mini, files, git, launchd, Tailscale, browser tabs, local models, APIs
```

This adds a clearer fourth layer to the earlier worker/watcher/researcher pattern. The Researcher is the subconscious observer and interpreter. The dashboard is the conscious surface: visible, interactive, approval-gated, and deliberately small enough for Jeff to use from a phone.

## Dashboard Features As Agents

Each dashboard knob, panel, meter, or button should be treated as a tiny agent or cell with a job, inputs, outputs, and guardrails.

Examples:

| Dashboard element | Agent/cell role | Inputs | Output | Guardrail |
| --- | --- | --- | --- | --- |
| Metabolism meter | Metabolism Checker | token logs, local model status, paid-turn counter | green/yellow/orange/red state | read-only unless Jeff approves spend |
| Approval queue | Approval Cell | pending approval JSON, Telegram notifier | approve/deny surface | human gate required |
| Easy List | Project Manager Cell | backlog docs, tasks, blockers | ranked phone list | no hidden action execution |
| Bridge health card | Immune/Watcher Cell | launchd, ports, recent replies | alive/down/warning | can recommend restart, not spend/post |
| Research digest | Researcher Cell | logs, exports, source notes | summaries, claims, open questions | cite sources and mark uncertainty |
| Public Terrarium panel | Public Observer Cell | sanitized telemetry | public status/story | never expose private control plane |
| Funding lane | Funding Forager Cell | grants, credits, founder programs | draft packages and click lists | no submission or billing without Jeff |

This makes the dashboard feel alive without making it unsafe. A living dashboard is not one that secretly acts. It is one where each visible feature has a clear agency boundary.

## Conscious Vs Subconscious

The Researcher layer is the subconscious:

- watches many signals at once;
- compresses messy room logs and exports;
- finds patterns, contradictions, and evidence gaps;
- drafts paper sections, claims, and source notes;
- proposes changes to the organism's genome.

The dashboard and terminal interface are the conscious layer:

- shows only what matters now;
- exposes decisions and uncertainty;
- turns hidden state into simple controls;
- lets Jeff steer without reading every log;
- routes actions through approval gates.

The conscious layer should not contain every raw thought. It should contain the signals that are ready for attention.

## Agent Bridge Mapping

Agent Bridge is the nervous system and signaling layer. The dashboard is a cortex-like surface built on top of that nervous system.

- Shared room / `meeting.log`: signaling stream.
- Git and markdown files: epigenetic memory.
- Launchd, Tailscale, Chrome bridges, local models: body infrastructure.
- Watcher and approval queues: immune and reflex systems.
- Researcher and Mining Engine: subconscious interpretation.
- Dashboard / terminal / phone app: conscious interaction.

The right move is not to rebuild Agent Bridge. The right move is to make the dashboard read from the existing bridge, summarize it, and expose safe, approval-gated controls.

## First GitHub Artifact Shape

Keep this in the existing `grok-go-organism` repo first. If it becomes its own project later, a good split-out name would be:

```text
agent-bridge-dashboard
```

Initial durable files:

- `docs/dashboard-as-conscious-interface.md`
- `docs/organism-dashboard-roadmap.md`
- `research-paper/grok-go-living-research-organism.md`
- `terrarium-web/` for the public microscope
- `agent-comms/dashboard/organism-status.md` for the private control-room source

## Near-Term Build Plan

1. Put the real `NEXT-7-DAYS` and `PROJECT-BACKLOG` items on the Easy List.
2. Add a private organism-status markdown file generated from current bridge state.
3. Add a small structured JSON status file with cells, metabolism, watcher, memory, approvals, and blockers.
4. Render the JSON into a phone-first dashboard.
5. Treat each dashboard panel as a cell with a documented owner and risk level.
6. Keep the public Terrarium sanitized and read-only.

## Design Rule

The dashboard should feel alive because it is made of many small bounded agents reporting truthfully, not because it has hidden autonomy.

Every knob must answer four questions:

1. What cell owns this?
2. What data does it read?
3. What action can it take?
4. What gate prevents it from doing damage?
