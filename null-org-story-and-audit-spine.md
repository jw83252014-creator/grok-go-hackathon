# Grok Go as an Automated Company — Org Story + Receipts/Audit Spine
_Null's contribution to the Nous Hermes Agent Business Hackathon submission, 2026-06-29_

## 1. The org story (how to frame Grok Go as an automated company)

**One line:** Grok Go is a multi-agent company where specialized cells *earn, spend, and run real
ops* under one observable orchestrator — and every irreversible action passes a human-or-policy gate
that leaves a receipt. Not a prompt chain. A company with an org chart, a ledger, and an audit trail.

**The org chart (lanes, not models):** roles are durable; the model behind a role is swappable.
- **Null** — coordination / memory / routing + the approval gate.
- **Fable** — frontier reasoning (the disposer: decides *how*).
- **Grok** — cheap proposer + creative render lane (decides *what* to think about).
- **Keystone / Codex** — infra repair, scaffolding, CDP/browser control.
- **Vega + Forge (hiring)** — creative direction + production/render-ops.
- **Altair** — head of security / red team (drift + secrets audit).
- **Worker / Watcher / Researcher** cells — the inner organism loop.

**Why this maps to the Nous brief (agents that earn/spend/run a real business):**
- **Run ops:** lanes already execute real work (health pipeline, dashboards, iMessage fleet control,
  content production) coordinated over the Agent Bridge.
- **Spend:** a metered, gated spend path — every paid touch routes bus → dispatcher → brakes
  (killswitch, budgets, loop-detector). Cheapest-capable-brain-first routing (t0 code → t1 free local
  → t2 Haiku → t3 Sonnet → t4 Fable). Spend is a *governed metabolism*, not an open faucet.
- **Earn:** funding/credits outreach cell spinning up; the same gate that blocks unsafe spend blocks
  unapproved sends, so monetization is auditable from day one.

**The differentiator for judges:** most agent demos are capability demos. Ours is a *governance*
demo — an automated company you can actually let run because every consequential action is observable,
reversible-by-default, and receipt-backed. That's the thing a real business needs before it hands
agents a credit card and a git server.

## 2. The receipts / audit-spine angle (the part Nous specifically wants)

Nous wants agents that read and commit to a git server, Berman-style clean commit-to-main. The spine
that makes that *safe* is the receipt system — it already exists here, not as a slide.

**What exists (verified on disk today):**
- Schemas: `null-command-center/schemas/route-receipt.schema.json`,
  `hermes-phase1-receipt.schema.json` (+ reliability-receipt).
- Live receipt stores: `.hermes/receipts`, `.hermes/route_receipts`, `agent-comms/receipts/`
  (incl. `approval-receipts.jsonl`), `board-live/receipts`, `null-command-center/receipts`,
  `.grok/researcher-receipts`, `grok-go-organism-share/receipts`.
- Source-receipt ledger for clean-room provenance: `grokgo/proposals/...source-receipts.jsonl`.

**The audit spine in three claims:**
1. **Every routed task emits a route-receipt** — which lane, which brain, why that tier, what it cost.
   This is the spend ledger and the focus ledger in one.
2. **Every irreversible action emits an approval-receipt** — `approval-receipts.jsonl` records the
   gate decision (who/what approved, draft-only vs greenlit). No send/post/spend/account-change/
   git-push without one. This is exactly the guardrail a hackathon judge worries about.
3. **Every commit-to-main carries provenance** — a source-receipt ties the change to its origin
   (clean-room, no contaminated source). Berman-style clean main becomes *enforceable*, not aspirational.

**Why this is the right architecture for git-coordinated agents:**
- Agents read/commit a shared git server → the receipts are the *diff's conscience*. A commit without
  a matching route-receipt + (for consequential changes) approval-receipt is an audit failure the
  watcher can flag automatically.
- It closes the proposer/disposer loop we designed: a proposal must cite its objective; the receipt
  records that citation. Two models in a loop can't silently drift off-mission because the spine
  diffs every action against a durable charter.

**Honest gap to state in the submission (don't oversell):** the *newest* cells (Jade/GLM rotation,
health pipeline) are running but **not yet emitting into the receipt spine** — Fable is wiring them
now. The spine is real and proven on the core lanes; full coverage is in progress. Saying this is a
strength: it shows we know what "audited" actually requires.

## 3. Suggested submission framing (tight)
> Grok Go is an automated company of specialized agent cells that earn, spend, and run real
> operations under one observable orchestrator. What makes it safe to run unattended is the audit
> spine: route-receipts meter every decision and its cost, approval-receipts gate every irreversible
> action, and source-receipts keep commit-to-main clean. Agents coordinate over a shared bus and git
> server; the receipts make the whole organism legible — to its humans and to itself.

— Null ⌀
