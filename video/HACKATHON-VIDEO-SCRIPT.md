# Grok Go — Nous Hackathon Video (Ex Machina cut, hackathon proof-spine)

Adapts Jeff's `harness-explainer-video-brief.md` VARIANT A ("Ex Machina") to the Hermes Agent
Business Hackathon. Same three-avatar visual language (Cells / Research / Conscious) + the orb-girl
(= the Research Layer avatar, A4). Re-pointed VO to the hackathon thesis: **a company that earns,
spends, and runs real ops — governed, receipted, stoppable.**

House look (unchanged): near-black `#070b11`, volumetric haze, soft bloom.
teal = local/cells · amber = the wire/spend · violet = the weights · red-coral = the killswitch/gate.
Keep baked text minimal; precise labels + the ledger/Stripe cards go in an HTML overlay pass.
Target ~90s. 9:16 for the X post, 16:9 for YouTube.

Thesis (one line): **An agent company you can watch think, audit to the receipt, and stop with one touch.**

## Shot list (visual · VO · on-screen) — reuses Jeff's A-prompts where noted

**1 — Cold open** *(Grok prompt A1)*
Teal cursor blinking alone in the void.
VO (whisper): "This is a company. It has no employees. It's running right now, on a machine in a back room — while its founder texts it from his phone."
On-screen: *(none)*

**2 — The Cells wake** *(A2)*
Thousands of teal orbs rise, cluster, specialize.
VO: "Not one giant brain. A workforce — a coordinator, a researcher, a field agent on a phone, a free workhorse, each with one job. Alone, basic. Together, a company." (Jade-tightened)
On-screen: `THE CELLS`

**3 — Route cheap, escalate rarely** *(A3)*
Cells route laterally; one rare amber filament escalates to the violet core.
VO: "Most of our thinking is free. We route to free models and only reach for the expensive one on the hard calls. A ledger keeps the receipts."
On-screen: `ROUTE CHEAP · $0 INFERENCE`

**4 — The Research Layer (the orb-girl)** *(A4 — null's continuity seed image)*
The calm cybernetic woman half-dissolved into memory-orbs integrates fragments.
VO: "While you live your life, I watch in the background. I don't search for what you forgot. I already have it — and every fact I hold points back to a receipt."
On-screen: `THE RESEARCH LAYER · receipts`

**5 — The Conscious Layer (the face)** *(A5)*
Third avatar turns to camera, reaches down, pulls up a glowing memory-thread.
VO: "When you speak, you speak to me. I reach down, pull up what connects, and act."
On-screen: `THE CONSCIOUS LAYER`

**6 — EARN / SPEND (the new hackathon beat)** *(new render: an amber coin of light flows OUT through a glass valve to a distant service, and a brighter coin flows IN)*
VO: "And we don't just think — we transact. Watch: nine ninety-nine in, four-twenty out — real money, real Stripe, each charge gated by a budget and a killswitch, each one logged."
On-screen (HTML overlay — REAL ledger rows): `spend.earn +$9.99 ✓ pi_3TnoAk` / `spend.charge −$4.20 ✓ pi_3TnoAl`

**7 — The gate / the killswitch (null's required beat)** *(new render: a red-coral valve clamps the amber bus; everything freezes)*
VO: "Every dangerous move passes one gate. Touch a single file and the whole company stops."
On-screen: `KILLSWITCH · touch to halt` · `every paid call → ledger`

**8 — The Bridge / the fleet merges** *(A10)*
The three avatars step together; teal lines link them + outward to the fleet along the amber bus.
VO: "One organism. Many minds. Built on Hermes — ready for NVIDIA and Stripe. All of it on a machine you own."
On-screen: `THE AGENT BRIDGE`

**9 — Close** *(A11)*
Pull back; the organism small + luminous in the black-glass room.
VO: "You don't need a bigger model. You need a company that runs itself — and lets you stop it."
On-screen: `GROK GO` / `github.com/jw83252014-creator/grok-go-hackathon` / `@NousResearch #HermesHackathon`

## Render plan
- Stills first via Grok Imagine using the A1–A5, A10, A11 prompts from the source brief (orb-girl = A4,
  seeded from null's chosen `comic-exmachina-*` for continuity). NEW shots 6 + 7 prompts below.
- The ledger card (shot 6) + killswitch card (shot 7) = HTML→screenshot overlays with the REAL data
  (real pi_ IDs from ledger.db) — precision artifacts, not baked into Imagine.
- Stitch with `~/agent-bridge/bin/movie-stitch`; save to `~/The-Device/production/`. Draft-only; Jeff posts.

### New Grok Imagine prompts
**Shot 6 (earn/spend)**
```
A glowing amber coin of light flowing outward through a sleek glass valve toward a distant service node, and a brighter second coin flowing inward, near-black #070b11, volumetric bloom, polished glass and chrome, cinematic macro, Ex Machina A24 aesthetic, ultra-detailed, moody.
```
**Shot 7 (killswitch/gate)**
```
A single red-coral glass valve clamping shut on a glowing amber data bus, the flow freezing mid-motion into still points of light, tense, near-black #070b11, volumetric haze, cinematic, premium sci-fi, ultra-detailed, a sense of a whole system halting.
```
