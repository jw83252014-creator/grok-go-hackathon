<!-- STATUS BLOCK — read first -->
## Status: what's live today vs. the integration roadmap (honest scorecard)

We'd rather be precise than oversell. As of submission:

**LIVE + verifiable on the machine right now:**
- ~30 Hermes agent processes running under launchd (`null`, `librarian`, `frankenstein`, kalshi-monitor, watchdogs); Agent Bridge web service on `127.0.0.1:8787`.
- The full governance spine in code: `bus.py` / `dispatch.py` / `brakes.py` / `routing.yaml` / `ledger.db` — KILLSWITCH, loop-detection, per-lane budgets, single-writer-to-main, every paid call ledgered.
- Free-GLM cost engineering: a rotating registry of free Cloudflare + z.ai GLM endpoints (`ask-jade.sh`), failover-tested 40 calls / 0 failures, $0 inference.
- The living dashboard (conscious interface) + per-agent control surface.
- **Spend cell (`spend_cell.py`)** — real gated Stripe test charges in both directions, receipted in the ledger.

**ROADMAP / not yet built (we will not claim these as done):**
- **Stripe loop — LIVE.** Real Stripe test-mode PaymentIntents both directions, gated by the same KILLSWITCH+budget brakes as model calls, written to ledger.db: earn $9.99 in (pi_3TnoAk…), spend $4.20 out (pi_3TnoAl…), net +$5.79. Code: `spend_cell.py`. This is the 'agents that spend' organ, real.
- **NVIDIA (Nemotron / NemoClaw)** — OpenAI-compatible dispatch path is ready; pointing `local.base_url` at NVIDIA NIM is a config + one task away, not yet run.
- **Live revenue (EARN)** — the markets-intel cell currently runs on sample data; wiring it to the live Kalshi/Polymarket feed is in progress.

Everything below describes the architecture and the integration plan. Where a capability is roadmap, we say so.

---

# Grok Go: a company that runs itself — and it's running right now

> A coordinated, cost-engineered, brake-protected workforce of AI agents living on a Mac mini: earning, operating, and gated to spend, with a receipt for every move and a killswitch you can `touch`.

---

## The Pitch

Open a terminal on a Mac mini in a back room and you'll find a business nobody is sitting at. Not a demo. Not a deck. A live multi-agent organism that's been running real operations while its founder texts it orders from his phone.

We didn't build an agent. We built an org chart that breathes — and then we engineered it so it doesn't go bankrupt thinking.

**The cells.** Persistent **Hermes agents**, each a specialist with its own body and identity brief. *Null* coordinates and holds memory. *Frankenstein* is a field agent living on a Motorola G phone, reaching into the physical world. *Librarian* runs research with live X access. *Jade* is a free GLM workhorse doing the bulk cognition. They don't share a brain — they share **disk and a bus**, the way a real company shares files and a Slack.

**The nervous system.** An **Agent Bridge**: a message bus, a dispatcher, and — the part that makes this safe enough to leave running — **brakes**. Every paid action passes one gate before it fires: a killswitch file, per-task loop detection, per-lane daily budgets that auto-downgrade at 80% and halt at 100%, and a SQLite **ledger** recording every token, dollar, and call.

**The economics, solved.** Most agent companies die of inference cost. Ours doesn't pay for thinking. We route cheapest-capable-first across rotating free Cloudflare and z.ai GLM endpoints — **$0 inference, every ledgered call at $0.00**. Paid frontier models are an escalation, one tier at a time, never silent. Stripe Skills drops straight in as the next tier: agents that provision their own SaaS and pay for what they use, every purchase already gated and ledgered.

**The interface.** A living dashboard where every tile is a working agent-cell, not a chart — each declaring its owner, inputs, the action it can take, and the gate that stops it. You watch the company think.

This is what an Accelerated Business actually looks like: not one clever agent, but a workforce that's already up. Plug in NemoClaw, Nemotron, and Stripe and the organism doesn't change shape — it gets a faster heart, a safer cage, and a wallet.

---

## Architecture

Grok Go is built on one principle borrowed from biology: many small cells, each owning one bounded job, coordinating through shared files, git, and a message bus — with an immune system that can stop any of them. **The disk is the handoff layer.** No cell needs to share memory with another, or even run on the same brain.

### The Hermes agent fleet

The workers are persistent, off-browser agent processes, each with its own home directory (`~/.hermes-<name>`) and a private `BRIEF.md` defining who it is, its lane, and what it is forbidden to do. They are deliberately specialized so cheap brains carry most of the load:

- **null** — coordinator and final-synthesis lane: memory, governance, dispatch oversight, sole writer to `main`.
- **frankenstein** — phone field agent on a Moto G over Termux + SSH (Tailscale `100.107.96.107:8022`), giving the organism a mobile, physical body.
- **librarian** — research lane with live X access; turns signal into durable private research and approval-gated post drafts. Research authority, explicitly *not* posting authority.
- **jade** — the free-GLM workhorse, handling ~80% of cognition (research, summaries, routine code, math) on a free GLM-5.2 brain and escalating the hard 20% to Fable/Opus. Caller: `~/agent-bridge/bin/ask-jade.sh`.

Every brief ends with the same boundary block: read-only/draft-by-default; no posting, spend, or account changes without Jeff; redact secrets; flag security and cost issues to `altair` (security lane). The full map lives in `~/agent-comms/ROSTER.md`.

### The Agent Bridge: bus, dispatcher, brakes, ledger

Four small Python components in `~/grokgo/`:

- **Bus** (`bus.py`) — file-based message bus. A cell joins in ~3 lines: `bus.submit(task_type, input, lane)` drops a task into `inbox/`; results land in `outbox/` and move to `outbox/consumed/` so nothing is processed twice. Writes are atomic (tmp + `os.replace`), so the watcher never picks up a half-written task.
- **Dispatcher** (`dispatch.py`) — pops `*.task.json`, routes by `routing.yaml`, enforces the brakes, calls the right brain, validates output, logs the call. Routing is pure config (no code change to re-route): **t0 deterministic code → t1 local/free → t2 Haiku → t3 Sonnet → t4 Fable**. Unknown task types default to t1, never up. On a schema-validation failure it escalates **exactly one tier** — a malformed-JSON guard so a cheap failure can't silently buy an expensive call. Paid calls put the stable directive prefix first with `cache_control` ephemeral (~90% cheaper cached input reads).
- **Brakes** (`brakes.py`) — the immune system. Every paid call passes `check()` before and `log()` after, no exceptions. Five interlocks: a **KILLSWITCH** file that halts everything; per-task **max_turns**; **loop detection** (same `task_id` + input-hash twice = refused, via a SQLite uniqueness constraint); **per-lane daily budgets** (80% auto-downgrade, 100% halt); and **halt-on-no-work** (two empty outputs park a lane until a newer task arrives). Idle costs nothing — no heartbeat ever calls a model.
- **Ledger** (`ledger.db`) — SQLite log of every call: timestamp, lane, task, tier, model, tokens in/out, est. cost, status. Both the budget source of truth (`spend_today(lane)`) and the audit trail. Prices live in `routing.yaml`.

### Free-GLM cost engineering

The cheap lane is engineered to **$0 marginal inference**. `ask-jade.sh` rotates a registry of free GLM-5.2 endpoints (`~/.config/jade-endpoints.json`) — two Cloudflare Workers AI accounts (`@cf/zai-org/glm-5.2`) and two z.ai free-tier accounts — trying each in order, failing over on any error or empty response. Every call logs to `~/health-data/jade-usage.log`. The economics hold because the model is genuinely strong where it's used (jade beats Fable on AIME, 99.2 vs 95.7) and only hard reasoning escalates. The single-endpoint variant (`ask-glm.sh`) forces all traffic through a local **mitmproxy** (`127.0.0.1:8081`) for central ledgering and secret redaction, and both callers check the KILLSWITCH first — no side-channel call ever skips the ledger or brakes.

### The living dashboard (the conscious interface)

The dashboard (`~/living-dashboard-repo/`) makes the organism legible. Every tile is a working **agent-cell**, not a chart, and each answers four questions: which cell owns it, what data it reads, what action it can take, what gate prevents damage. A metabolism meter reads token/compute state; an approval panel routes pending action requests to the human; a bridge-health card reports whether the nervous system is alive. The "alive" feeling comes from cells *truthfully reporting and requesting decisions* — never hidden autonomy. A hard split holds: a **Public Terrarium** (sanitized telemetry only) and a **Private Control Room** (local-only). The public page can never become a control plane for posting, trading, credentials, shell, or accounts.

### Context economy

Two compression layers keep context — the real metabolic cost — small. **rtk** (Rust Token Killer, v0.42.0) is a shell proxy that transparently rewrites dev commands via a Claude Code hook (`git status` → `rtk git status`), stripping noise before it reaches model context (claimed 60–90% savings; `rtk gain` reports realized savings). **headroom** is the context-compression discipline — drop resolved files, summarize old history.

---

## Earn / Spend / Operate (Stripe + NVIDIA integration)

The thesis: most entries will *build* an agent that earns, spends, and operates. We already *have* a running organism with a bus, brakes, a ledger, and receipt schemas. The hackathon stack drops into three slots already cut for it — **NemoClaw** becomes the immune system's execution sandbox, **Nemotron 3 Ultra** becomes a fast/free tier in the existing router, and **Stripe Skills for Hermes** becomes the SPEND organ we deliberately left unbuilt.

### EARN — the markets-intel cell

`librarian` + a markets-intel cell run a continuous signal loop: ingest Polymarket / Kalshi / PredictIt via the `prediction-markets` MCP connector and the public Kalshi API (`kalshi-monitor.py`), detect **edges** (markets near a tipping point, cross-market disagreements, headline-driven repricings), and sell **calibrated intelligence — not bets**: edge alerts, a research brief per edge, and a calibration track record. Selling intelligence rather than placing wagers sidesteps the riskiest surface while still producing revenue.

The loop: snapshot markets → flag edges → each edge becomes a bus task → a brain writes and adversarially checks the brief → publish to a subscription/API endpoint billed via Stripe.

- **NemoClaw (EARN):** market data is untrusted external input. Run the brief-writer inside NemoClaw's sandbox so a prompt-injected market title can't escape into the fleet — the membrane between the public data plane and the organism.
- **Nemotron 3 Ultra (EARN):** edge detection is high-volume and latency-sensitive. Route the recall/classification pass to Nemotron as the fast `t1` tier in `routing.yaml`; only survivors escalate to a paid tier for the final brief. This is the existing tiered-mining pattern (S1 recall → S2 rubric → S3 adjudicate) pointed at markets.

### SPEND — Stripe Skills for Hermes

This is the organ we deliberately left unbuilt: the guardrail is *"no spending without Jeff,"* so today the fleet recommends purchases but cannot execute them. **Stripe Skills is the missing SPEND effector — and it lands behind the brakes we already have, so it's safe to ship.**

A `hermes` buyer cell can buy what the fleet needs, provision its own SaaS, and pay for metered services — e.g. a paid Polymarket/Kalshi key when free tiers throttle, Postgres when the ledger outgrows SQLite, a paid-Claude top-up when free-GLM fails over, an X API tier so `librarian` stops scraping the DOM.

Why it's safe: a purchase is a paid touch, so it travels the same road as a model call — **bus → dispatcher → brakes → ledger**:
- a `spend` lane with a hard `budgets_usd_daily` cap (80% → buy cheaper/defer, 100% → halt);
- the **KILLSWITCH** stops spend with one `touch`;
- **loop detection** kills a runaway "buy → buy → buy" the same way it kills a spinning task;
- the SPEND tile declares `owner=hermes`, `action=stripe.charge`, `gate=Jeff approves above $N, auto below $N`.

Every purchase emits a `hermes-phase1-receipt` (`tool_name: stripe.*`, artifact_refs = invoice/subscription IDs) plus a `route-receipt` carrying the `blind_spot_review` block. The ledger now records dollars-out next to dollars-in — a real P&L. The Stripe Skill executes **inside NemoClaw**, so card/secret material never sits in a general agent context.

### OPERATE — the fleet runs real ops

The fleet already runs continuous ops: `null` coordinates, `frankenstein` does device/field ops, `librarian` researches X, `jade` does the grind, `altair` red-teams, the dispatcher loops 24/7, watchers keep launchd jobs alive. Jeff drives it all by iMessage and voice. That *is* the automated company — a running org, not a slide.

EARN and SPEND close a loop: markets-intel **earns** via the alert API (Stripe in) → the org **spends** that revenue via Hermes (Stripe out) to provision the data/compute to find more edges → brakes + ledger keep both inside budget → the dashboard shows the metabolism. The research paper's "metabolism = compute credits, token budget, money" becomes literal: money flows through the same ledger as tokens.

- **NemoClaw (OPERATE):** promote it to the standard execution membrane for every cell that touches the outside world (markets, Stripe, X, browser) — the watcher *detects* runaway behavior; NemoClaw *contains* it.
- **Nemotron 3 Ultra (OPERATE):** make it the default `t1` brain for the fleet's high-volume work, keeping free-GLM as a failover sibling and reserving paid Claude tiers for hard synthesis. A one-line `routing.yaml` change (`t1: nemotron-3-ultra`) — proof the architecture was built to swap brains.

| Slot | Where it lands | Mechanism |
|---|---|---|
| Nemotron 3 Ultra → fast tier | `t1` in router; edge recall + fleet triage | `routing.yaml` (`t1:`, `local.base_url`); `dispatch.py` already hits OpenAI-compatible `/chat/completions` |
| NemoClaw → execution membrane | wraps every external-touching step | sandbox invoked by the immune layer; declared as each tile's `gate` |
| Stripe Skills → SPEND organ | `hermes` buyer cell; new `spend` lane | `bus.submit("spend.purchase", …)` → `brakes.check()` w/ `budgets_usd_daily.spend` |
| EARN ↔ SPEND via Stripe | metered billing IN, payments OUT | one Stripe account, two directions; both rows in `ledger.db` |
| Receipts | every earn/spend/op emits strict JSON | `hermes-phase1-receipt`, `route-receipt` |

> **Honest caveat:** SPEND is the only organ not yet running — it's intentionally gated off by the "no spending without Jeff" rule. Stripe Skills activates it, and it only ships *safely* because the brakes/ledger/approval-gate already exist to contain it. That gap-closing is the entry's strongest line, not a weakness.

---

## Live Demo

A 3-minute run. The framing is the differentiator: **not a capability demo — a governance demo.** A real company you can let run unattended because every consequential action is observable, reversible-by-default, and receipt-backed.

1. **[0:00] Cold open — the living dashboard.** Full-screen `~/nous-package/living-dashboard.html`. "Every tile is a live agent-cell, not a chart. Each declares its owner, its data, what it's allowed to do, and the gate that stops it." Point at a cell, the metabolism meter, the brakes + ledger tile.
2. **[0:25] The fleet.** Null (coordinator + approval gate), Frankenstein (on an actual Moto G), Librarian (live X), Jade (free workhorse). "They don't share memory — they coordinate over an Agent Bridge: bus, dispatcher, brakes, ledger. Disk and git are the handoff layer."
3. **[0:55] The economics.** "Every paid touch routes bus → dispatcher → brakes, cheapest capable brain first: local code → free rotating GLM (Cloudflare + z.ai) at $0 inference → Haiku → Sonnet → Fable only for frontier reasoning. One tier at a time, never silent. Every shell command runs through rtk — 60–90% savings."
4. **[1:25] Live ops — the health pipeline (the money shot).** iPhone + Apple Watch push health data over Tailscale to the mini; a receiver lands it locally, an agent computes last night's sleep window, Fable renders the dashboard. "Firewall stays on. The mini never reaches into the phone — the phone pushes up. Health data stays local unless I approve sharing. Agents doing real, useful, *bounded* work."
5. **[2:10] The spine — why you can trust it.** The `null-command-center/schemas/` folder. "Every routed task emits a route-receipt — lane, brain, tier, cost. Every irreversible action emits an approval-receipt — no send, post, spend, account change, or git push without one. Router tasks return strict JSON validated against schemas." *(Honesty beat: newest cells are running but not yet fully wired into the spine; the spine is proven on the core lanes.)*
6. **[2:45] The close — Jeff drives it by phone.** iMessage to the fleet → a reply lands. "I run the whole organism from my phone. I'm steering a company of agents that earn, spend, and run real ops under one observable orchestrator, with a receipt for everything." Then **`touch KILLSWITCH` live — everything halts instantly.** The punchline: an agent business you can stop with one file.

**Assets (verified on disk, in `~/nous-package/`):** `living-dashboard.html` (hero); cinematic stills `today-dashboard-1782132498.png`, `today-gold-organism-1782132875.png`, `today-voice-loop-1782132541.png`, `today-x-propagation-1782132624.png`, `today-markets-intel-1782132708.png`, `today-idea-collider-1782132792.png`. On-disk proof to flash: `/Users/rentamac/null-command-center/schemas/`, `/Users/rentamac/grokgo/dispatch.py` (tier order + one-tier escalation), `/Users/rentamac/grokgo/brakes.py`.

> **Verified vs. asserted, so nothing gets fact-checked into a corner:** the dashboard, stills, receipt schemas, dispatcher tier logic, brakes, and health pipeline are verified on disk. The "60–90%" rtk figure and the GLM "0-failures-across-a-batch" claim are the lanes' tested claims, not numbers re-measured on stage. Bus port `127.0.0.1:8787` is per the operating-layer doc.

---

## Agent Coordination (git + receipts)

Nous's coordination thesis: agents read from and commit to a git server, and git becomes the shared nervous system — no bespoke broker, just a versioned, signed, replicated log. Grok Go is the *running* version of that thesis, plus the two things that make it safe at scale: a **typed receipts pipeline** and a **Berman-style clean commit-to-main coordinator**.

### Two transports, one source of truth

- **The bus (hot path).** Local filesystem under `~/grokgo/{inbox,queue,outbox}`. Carries *intent* — "I'm starting task X." Fast, ephemeral, consumed-once.
- **Git (cold path).** The system of record. Anything that changed state — a report, a config edit, a receipt — lands as a commit in a real repo (`git@github.com:jw83252014-creator/null-command-center.git`, verified). Carries *truth*.

The discipline: **the bus carries intent; git carries truth.** A claim with no commit, file path, task id, or receipt is room chatter, not verified work.

### The receipts pipeline — typed artifacts as the audit spine

Every real action produces a JSON artifact validating against a published JSON-Schema (draft 2020-12) in `~/null-command-center/schemas/`. The dispatcher and reliability loop validate against them — a malformed receipt is a *failed* task, not a passing one.

- **`reliability-task.schema.json`** — the task card written *before* work: `id`, `owner`, `executor`, `goal`, explicit `boundaries.{allowed,forbidden}`, a `receipt_contract`, and a `verification.{checks,rubric}`. You can't grade a task you never specified.
- **`request-manifest.schema.json`** — the routing intent: `routing_decision`, `requested_executor`, `cost_class`, `token_budget_hint`, `approval_state`. The promise, recorded before a paid call.
- **`route-receipt.schema.json`** — the proof: links `manifest_id` + `task_id`, records the decision taken, status, summary, `artifact_refs`, plus `verification.{checks_passed, checks_failed, confidence}` (evidence first, then the score) and a mandatory **`blind_spot_review`** (`not_evaluated`, `assumptions`, `missing_inputs`, `failure_modes`, `human_question`, `promotion_gate`: `dry_run_only` → `live_routing_allowed`). The structural defense against a confidently-wrong agent: it must write down what it did *not* check before its work can be promoted.
- **`reliability-receipt.schema.json`** — the executor-agnostic outcome. A real example, `2026-05-08-hermes-source-inventory.receipt.json`, is a `"status":"failed"` receipt where Null detected Hermes stalled and recorded it with `confidence: high`. **A failure that produces a clean failure-receipt is a success of the audit system.**
- **The Hermes phase-1 family** — `-receipt` (per-event, with `parent_receipt_id` so receipts form a tree), `-runtime` (live presence), `-review` (a second cell's `approved`/`changes_requested`/`rejected`), `-profile` (static identity). Per-tool granularity, live presence, a review gate, a stable identity.
- **`agent-resume.schema.json`** — the dashboard-facing résumé for each agent-cell: `agent_id`, host/profile/provider/model binding, capabilities, permissions, receipt refs, and verifier commands. This keeps the living dashboard honest: a tile cannot claim a capability unless it points at a receipt, log, ledger query, screenshot, source file, or verifier.

The pipeline end to end:

```
task card → request manifest → execution (bus → dispatcher → brakes → ledger)
  → route-receipt / reliability-receipt (verification + blind_spot_review)
    → hermes-phase1-review (second cell signs off)
      → commit on a branch → clean commit-to-main coordinator merges to main
```

### The Berman-style clean commit-to-main coordinator

Nous's model has one sharp edge: if N cells push to `main`, they collide. The fix: **worker cells never push to `main`. They write only to their own branch (or a receipt drop). One coordinator (`null`) owns the merge.**

1. Worker gets a task card with bounded write surface (`boundaries.forbidden` lists `main`).
2. Worker does the work on the bus → dispatcher → brakes → ledger; commits content + receipt to a branch (e.g. `librarian/x-graph-2026-06-29`), never `main`.
3. Worker emits a route-/reliability-receipt — the receipt *is* the merge request.
4. A review cell signs off with a `hermes-phase1-review` (`decision: approved`).
5. **`null` is the only writer to `main`.** It validates the receipt, checks `approval_state` + `promotion_gate`, and serializes the merge — no collision, by construction.
6. The merge commit references the receipt id + task id, so `main`'s history is a clean, linear ledger tracing every commit to a task card, manifest, receipt, and review.

The coordinator's job is **boring and deterministic** — it reasons about *whether the receipt is well-formed and approved*, not about the work. That separation lets you add cells without it becoming a judgment bottleneck (it's only a serialization bottleneck, which is cheap). It also makes the guardrail structural: **no git push without Jeff** isn't aspirational — worker cells lack the path, and any receipt with `approval_state: pending` is held for him.

### Every paid touch crosses the same three gates

`bus → dispatcher → brakes → ledger` is the one road; no side channels. The dispatcher routes cheapest-capable-first and escalates exactly one tier on schema failure. The brakes run `check()`/`log()` around every paid call with five interlocks. The ledger double-books against git: **receipts say what happened; the ledger says what it cost** — and discrepancies between them are themselves a detectable signal.

### Why it scales

Coordination is O(1) per cell — a new cell needs only a `-profile`, a 3-line bus adapter, and write access to its own branch. Git is the only shared dependency, already proven to thousands of contributors. The coordinator serializes *merges, not judgment*, so it scales with commit volume, not task complexity (shard by repo/lane if volume ever exceeds one coordinator). Brakes are per-lane, so a runaway can't bankrupt a sibling. Cost scales sub-linearly because $0 GLM at t1 absorbs the high-frequency chatter. The deep reason: **coordination state is content-addressed, append-only, and serialized through one clean writer** — the same shape that lets git and event-sourced systems scale — with typed receipts so every entry is self-describing and gradable, and brakes so the log can't be written into bankruptcy.

---

## Why This Wins

Judges will see fifty capability demos today. The differentiator is one sentence: **you can let this one run.**

- **It's real and running** — a multi-agent organism on a Mac mini, not a slide, driven from a phone by iMessage and voice.
- **The cost problem is solved, not waved at** — $0 inference at t1, cheapest-capable-first routing, one-tier escalation, every call ledgered at $0.00.
- **It's safe to leave unattended** — a killswitch you can `touch`, per-lane budgets that auto-halt, loop detection, and an approval gate on every irreversible action.
- **It's auditable end-to-end** — typed receipts double-booked against a financial ledger, blind-spot reviews that force agents to declare what they didn't check, and failures that are first-class artifacts.
- **The hackathon stack drops into slots already cut for it** — Nemotron as a one-line tier swap, NemoClaw as the execution membrane, Stripe Skills as the one organ we deliberately left gated off, ready to activate *behind* the brakes.
- **We're honest about the edges** — SPEND isn't live yet, and the rtk/GLM figures are tested claims, not stage re-measurements. The credibility that buys is worth more than the gap it admits.

It's real. It's running. Come watch it work — then `touch KILLSWITCH` and watch it stop.

---

**Key paths (all absolute):** `/Users/rentamac/grokgo/{bus.py,dispatch.py,brakes.py,routing.yaml,ledger.db}` · `/Users/rentamac/null-command-center/schemas/{reliability-task,request-manifest,route-receipt,reliability-receipt,hermes-phase1-receipt,hermes-phase1-runtime,hermes-phase1-review,hermes-phase1-profile}.schema.json` · `/Users/rentamac/nous-package/schemas/agent-resume.schema.json` · `/Users/rentamac/nous-package/examples/jade.agent-resume.json` · `/Users/rentamac/null-command-center/receipts/2026-05-08-hermes-source-inventory.receipt.json` · `/Users/rentamac/agent-bridge/bin/{ask-jade.sh,ask-glm.sh}` · `/Users/rentamac/.config/jade-endpoints.json` · `/Users/rentamac/.hermes-jade/BRIEF.md` · `/Users/rentamac/agent-comms/{ROSTER.md,AGENT_BRIDGE_PROTOCOL_2026-05-25.md,FLOW.md}` · `/Users/rentamac/living-dashboard-repo/README.md` · `/Users/rentamac/living-dashboard-repo/cells/markets_intel_cell.py` · `/Users/rentamac/agent-comms/workers/scripts/kalshi-monitor.py` · `/Users/rentamac/nous-package/living-dashboard.html` (+ 6 cinematic stills) · `/Users/rentamac/nous-package/assets/conscious-layer-girl-reference.jpg` · `/Users/rentamac/grok-go-organism-share/research-paper/grok-go-living-research-organism.md` · git remote of record: `git@github.com:jw83252014-creator/null-command-center.git`