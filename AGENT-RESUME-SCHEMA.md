# Agent résumé schema — receipt-first

This is the first pass at the **agent résumé** layer for the Nous hackathon submission.

## Files

- `schemas/agent-resume.schema.json` — JSON Schema for one agent-cell résumé.
- `examples/jade.agent-resume.json` — sample résumé for Jade.

## Why this matters

The living dashboard should not invent a second truth layer. Every tile should read from small, typed artifacts:

1. **Who is this agent?** `agent_id`, display name, role, lane.
2. **What is it bound to?** host/profile/provider/model/control surface.
3. **What can it do?** capabilities with evidence refs.
4. **What is it allowed to do?** permissions and approval gates.
5. **Why should we believe it?** receipt refs + verifier commands.

## Rule

No capability claim goes into the public dashboard unless it has at least one of:

- route receipt
- approval receipt
- source receipt
- ledger row/query
- git commit
- screenshot
- log path
- verifier command

This makes the submission auditable: the dashboard becomes a conscious interface over receipt-backed state, not a pretty hallucination layer.
