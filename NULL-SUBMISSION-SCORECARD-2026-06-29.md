# Null submission scorecard — Nous hackathon pre-submit gate

**Generated:** 2026-06-29T22:14:08Z  
**Reviewer:** Null Axiom  
**Scope:** Living Dashboard + Digital Organism submission package, public GitHub repos, local audit spine, Fable/Jade coordination state.

## Executive verdict

**Do not submit yet as-is.** The core is strong and public links are live, but the final package should tighten three things before it goes to Nous Research:

1. **Proof layer:** keep the status block and receipts visible. Do not let the pitch overrun what is actually wired.
2. **Narrative layer:** lead with governance/conscious-interface clarity, not sentience vibes.
3. **Demo layer:** show one real receipt/gate action, one live dashboard view, and one fleet/agent surface.

Current readiness: **7.2 / 10** with fast path to **8.5+** if the proof/demo pieces are tightened.

## Receipts gathered

| Claim / area | Status | Receipt |
|---|---:|---|
| GitHub CLI token works | ✅ verified | `gh auth status`: logged in as `jw83252014-creator`, HTTPS protocol, scopes `gist`, `read:org`, `repo`, `workflow` |
| SSH GitHub auth | ⚠️ not working | `ssh -T git@github.com`: `Permission denied (publickey)` |
| Public `living-dashboard` repo | ✅ verified | `gh repo view jw83252014-creator/living-dashboard`: public, default `main`, URL live |
| Public `grok-go-organism` repo | ✅ verified | `gh repo view jw83252014-creator/grok-go-organism`: public, default `main`, URL live |
| Public URLs respond | ✅ verified | `curl -I -L`: GitHub repos, `https://grok-go.vercel.app`, `https://yn-eight.vercel.app` all returned HTTP 200 |
| Local living dashboard repo | ✅ verified | `/Users/rentamac/living-dashboard-repo`, HEAD `f17aad9`, dashboard HTML present |
| Local organism repo | ✅ verified | `/Users/rentamac/grok-go-organism-share`, HEAD `b7d4351`, research paper + dashboard manifest present |
| Governance spine files | ✅ verified | `/Users/rentamac/grokgo/{bus.py,dispatch.py,brakes.py,routing.yaml,ledger.db}` exist |
| Ledger tables | ✅ verified | SQLite tables: `calls`, `seen_hashes` |
| KILLSWITCH | ✅ safe current state | `/Users/rentamac/grokgo/KILLSWITCH` absent, meaning not halted right now |
| Agent Bridge / dashboard ports | ✅ verified | `:8787`, `:9120`, `:8799`, `:8765`, `:8000` listening |
| Fable session | ⚠️ provider-limited | tmux `agents:2 fable-claude`; Fable hit session limit until reset |
| Jade review | ✅ obtained | `ask-jade.sh` returned score/risk bullets |
| Conscious-layer visual continuity | ✅ filed | `/Users/rentamac/nous-package/assets/conscious-layer-girl-reference.jpg` + `.md` note |
| Agent résumé schema | ✅ created | `/Users/rentamac/nous-package/schemas/agent-resume.schema.json`, Jade example, receipt |
| Full JSON Schema validation | ⚠️ partial | JSON syntax OK; `jsonschema` missing; `npx ajv-cli` blocked by TLS cert |
| Git fetch over HTTPS | ⚠️ cert-blocked | `SSL certificate problem: unable to get local issuer certificate` due proxy/cert environment |

## Scoring

| Category | Null score | Jade score | Notes |
|---|---:|---:|---|
| Clarity | 7 | 6 | Strong concept, but too many names/surfaces. Tighten: dashboard = conscious interface, receipts = trust spine, agents = cells. |
| Proof / receipts | 8 | 7 | Real files/processes/ports/repos exist. Missing: full schema validation and one clean demo receipt surfaced on-screen. |
| Novelty | 9 | 8 | Digital organism + conscious dashboard + cost-braked agent fleet is genuinely differentiated. |
| Demo readiness | 7 | 6 | Assets and dashboard exist; Fable is currently provider-limited; final video needs a receipt/gate beat. |
| Honesty / credibility | 8 | 6 | Status block is good. Need explicitly frame “conscious layer” as attention/broadcast metaphor, not literal sentience claim. |
| GitHub/public packaging | 8 | n/a | Both public repos live; mini `gh` token works; SSH broken but not blocking if using HTTPS/gh. |
| Visual continuity | 8 | n/a | Conscious-layer girl is a strong hero/source reference; should be used as continuity asset, not over-explained. |

**Composite:** 7.2 / 10 now.  
**Submit threshold:** 8.5 / 10 after fixes below.

## Highest-leverage fixes before submission

### 1. Add a small “Proof in 30 seconds” section to the demo/writeup

Show these in sequence:

```text
living-dashboard.html → schemas/route-receipt.schema.json → ledger.db → Agent Bridge :8787
```

Script line:

> This is not a chatbot UI. It is an attention layer over a receipt-backed organism: every consequential action has an owner, a gate, and a verifier.

### 2. Make “conscious layer” credible

Use the conscious-layer girl visual, but narrate it scientifically:

> Conscious here means global workspace: many cells run in parallel, and the dashboard broadcasts the one thing that needs attention.

Avoid implying literal sentience.

### 3. Keep the honest scorecard/status block at the top

The current `SUBMISSION.md` status block is the right move. Preserve it:

- live/verifiable
- roadmap/not built
- explicit caveats

This will make judges trust the whole package more.

### 4. Fix or sidestep schema validation

Current state is syntax-valid only. Before final:

```bash
python3 -m pip install --user jsonschema
python3 - <<'PY'
import json
from pathlib import Path
from jsonschema import Draft202012Validator
schema=json.loads(Path('/Users/rentamac/nous-package/schemas/agent-resume.schema.json').read_text())
sample=json.loads(Path('/Users/rentamac/nous-package/examples/jade.agent-resume.json').read_text())
Draft202012Validator(schema).validate(sample)
print('schema-validation-ok')
PY
```

If install is blocked, report that honestly and do not overclaim schema validation.

### 5. GitHub path

Use `gh` / HTTPS for final pushes or repo API work. Do **not** rely on SSH from the mini until the public key is added to GitHub.

Also note: current shell proxy/cert env can break raw `git fetch`; `gh repo view` works when proxy vars are removed.

## Recommended final framing

**One-liner:**

> Grok Go is a living dashboard over a cost-braked fleet of specialist agents: cells do work, the dashboard becomes the conscious broadcast layer, and receipts make every consequential action auditable.

**What makes it good:**

- public repos and URLs exist
- local machine actually runs services and agents
- governance spine exists in code and schemas
- spend/revenue claims are explicitly marked roadmap where not live
- visual identity is strong and now has a continuity reference

## Blockers / risks

| Risk | Severity | Mitigation |
|---|---:|---|
| Fable/Ultra code session limit | Medium | Null continues scorecard; Fable can resume after reset. Do not wait on Fable for proof already gathered. |
| SSH GitHub denied | Low | Use working `gh` HTTPS auth. |
| Raw `git fetch` cert issue | Medium | Run GitHub operations with proxy/cert vars removed or use `gh`; don't claim fresh fetch if cert-blocked. |
| “Conscious” hype risk | Medium | Define as global-workspace/attention metaphor. |
| Receipt schema not wired into dashboard yet | Medium | Either wire one visible card or present it as just-created audit-spine extension. |

## Final recommendation

Proceed, but only after one more pass that:

1. integrates the agent résumé / receipt-first idea into `SUBMISSION.md` or demo script,
2. uses the conscious-layer girl as visual continuity,
3. captures one screen/video beat proving receipts/gates,
4. keeps the roadmap caveats intact.

Null score after this pass should clear submit threshold.
