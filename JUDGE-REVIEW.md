I have a complete, evidence-backed adversarial picture. Final verdict.

---

# JUDGE REVIEW — Grok Go

**SCORE: 6.4 / 10** (Strong infra, fatal gaps against this hackathon's stated criteria.)

The architecture is real and unusually well-engineered. But judged *adversarially against the four criteria — earn/spend/run REAL ops, automated company, Hermes, Stripe + NVIDIA — the submission's prose massively overstates what's on disk. Three of the four required integrations are vapor, and the "running right now" claim does not survive `ps aux`.

## What I verified (the good)

- `bus.py / dispatch.py / brakes.py / routing.yaml / ledger.db` all exist and the code is coherent, not hand-wavy. The dispatcher genuinely routes by config, validates JSON, escalates exactly one tier on schema-fail (dispatch.py:162-166), and the brakes implement all five interlocks for real — KILLSWITCH check (brakes.py:69), loop-detection via a SQLite `PRIMARY KEY (task_id, input_hash)` uniqueness constraint (brakes.py:38-42, 96-104), 80% downgrade / 100% halt budget math (brakes.py:85-92), and halt-on-no-work parking (brakes.py:124-135). This is the strongest part and it is not faked.
- The Hermes fleet is genuinely live: `launchctl list` shows ~30 `com.agentbridge.*` jobs running (null-agent PID 71708, librarian-agent 26608, kalshi-monitor, frankenstein-watchdog, etc.), and the Agent Bridge web service is actually listening on `127.0.0.1:8787` (PID 6014). The org-chart-of-agents thing is real.
- Schemas + the failure-receipt (`2026-05-08-hermes-source-inventory.receipt.json`, status `failed`) exist on disk as claimed.

## 3 strongest points

1. **The brakes/ledger/governance spine is real, novel, and demoable.** "An agent business you can stop with `touch KILLSWITCH`" is a genuine differentiator and the code backs it. The receipts-as-merge-request + single-writer-to-`main` coordinator design is the most credible "safe to leave running" story a judge will see.
2. **The cost engineering is real and on-disk.** Tiered routing config, $0 t1, free-GLM endpoint rotation (`jade-endpoints.json` has 4 real endpoints), KILLSWITCH-checked callers (`ask-jade.sh`, `ask-glm.sh`, `ask-zai.sh`). Ledger shows 36 real calls all at $0.00.
3. **The Hermes fleet genuinely runs as persistent off-browser processes** under launchd — this is the hardest part to fake and it's real.

## 3 biggest weaknesses (harsh)

1. **STRIPE INTEGRATION DOES NOT EXIST.** Zero Stripe code. The only on-disk artifacts are `proposals/stripe-drafts/creator-course-payment-link.draft.json` and a planning doc — drafts, not integration. The submission spends a third of its length describing SPEND, then admits in a "caveat" that it's "the one organ we deliberately left unbuilt." Reframing an unbuilt required deliverable as a *strength* ("that gap-closing is the entry's strongest line") is the single most exploitable line in the submission. A judge reads it as: **the Stripe criterion is unmet.**
2. **NVIDIA INTEGRATION DOES NOT EXIST.** `grep -rE "nemotron|nemoclaw"` hits nothing but a vendored `node_modules` and a map file in an unrelated `openclaude` spike. There is no Nemotron in `routing.yaml` (t1 is `openai/gpt-4o-mini` pointed at `models.github.ai`), no NemoClaw sandbox anywhere. Every NVIDIA claim is future-tense ("becomes," "drops into," "a one-line change"). **Criterion unmet.**
3. **"It's running right now" is false for the part that matters, and EARN is fake data.** `ps aux` shows **no `dispatch.py` process** — the orchestrator the whole pitch rests on is not running. The ledger's last call is **2026-06-13, 16 days stale** as of judging, all in one `mining` lane from a single test batch (`keepkill-*`). The "EARN / markets-intel" cell ships **hardcoded demo data** (markets_intel_cell.py:19-31, literal Anthropic-IPO numbers Fable pasted in) — no live pull, no edge detection on real data, no subscription, no billing, **no revenue path of any kind**. The real Kalshi poller (`kalshi-monitor.py`) exists but only fires phone notifications; it earns nothing. So "agents that EARN" is unmet, and "running right now" is contradicted by your own process table.

Minor but will get caught on stage: routing.yaml prices carry a self-flagged `PLACEHOLDER` on Fable; `t4: claude-fable-5` is a suspended/simulated model per your own memory; jade config says `glm-4.7-flash` on z.ai but the prose claims `GLM-5.2`; the "jade beats Fable on AIME 99.2 vs 95.7" stat appears nowhere on disk.

## Punch-list for the final hours (priority order)

1. **Ship the smallest real Stripe loop or the entry fails a criterion.** A single live Stripe **Payment Link** + webhook that writes one `dollars-in` row into `ledger.db`, and one `bus.submit("spend.purchase",…)` path that creates a real Stripe test-mode charge gated by `brakes.check()` and writing a `dollars-out` row. Even test-mode, one real charge each direction converts "deliberately unbuilt" into "demonstrated." This is your highest-leverage hour.
2. **Get ONE real NVIDIA call into the ledger.** Point `local.base_url` at NVIDIA NIM / build.nvidia.com (Nemotron), run one task through the existing `call_local` path so the ledger shows a `nemotron` row. dispatch.py already speaks OpenAI-compatible `/chat/completions` — this is genuinely a config + one task. Do it so the claim is past-tense.
3. **Start the dispatcher and generate fresh ledger rows TODAY.** `python3 dispatch.py --loop` under launchd, push 3-4 real tasks through it so `MAX(ts)` in the ledger is judging-day, not 06-13. Right now your strongest asset (the live org) has a 16-day-cold heart.
4. **Make EARN produce one real artifact.** Wire `markets_intel_cell.record()` to actual `kalshi-monitor.py` output instead of the hardcoded Anthropic block, and rehearse it. A judge who opens that file sees fabricated demo data behind a "we already EARN" claim — that's a credibility kill.
5. **Pre-empt the fact-check.** Fix the GLM-5.2-vs-4.7-flash mismatch, remove or source the AIME stat, and replace `claude-fable-5` in the live demo path with a model that actually answers (vega/Opus) so `touch KILLSWITCH` halts something a judge can see was alive.
6. **Cut or soften the "deliberately unbuilt is our strongest line" framing.** Against criteria that explicitly require Stripe + NVIDIA, that sentence invites the exact deduction that sinks you. Reframe as "shipped a minimal live loop in both directions; here's the receipt."

Bottom line: you built a better *governance and cost* substrate than most teams will, and the live Hermes fleet is impressive — but on the literal scorecard you are currently 1.5 of 4 criteria met (Hermes: yes; automated-company: partial; Stripe: no; NVIDIA: no; real earn: no). Two small real integrations in the next hours move this from a 6.4 to a defensible 8.