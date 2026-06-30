# CODEX HANDOFF — render the Grok Go hackathon video

**Goal:** produce a ~90s cinematic video for the Nous Hermes Agent Business Hackathon (deadline EOD Jun 30).
You (Codex) are the GENERATION + STITCH lane. Fable wrote the script + prompts; you make the actual frames.
**Gate:** draft-only. Nothing posts publicly. Save outputs, ping back. Jeff posts the final.

## What to do (in order)
1. **Generate 9 stills** from the prompts in `RENDER-PACKAGE-for-codex.md` (same folder).
   House style: near-black #070b11, volumetric haze, Ex Machina A24. Save as
   `~/The-Device/production/hk-shot-1.png` … `hk-shot-9.png`. 9:16 (vertical, for X).
   - Shot 4 (the orb-girl / Research Layer): seed from null's chosen `~/Pictures/Grok-Go-Visuals/comic-exmachina-*.jpg` for face/style continuity.
2. **Make 3 overlay cards** (HTML → screenshot, NOT baked into the AI frames — real data):
   - `hk-overlay-ledger.png`: `spend.earn +$9.99 ✓ pi_3TnoAk   spend.charge −$4.20 ✓ pi_3TnoAl`
   - `hk-overlay-killswitch.png`: `KILLSWITCH · touch to halt    every paid call → ledger`
   - `hk-overlay-endcard.png`: `GROK GO   github.com/jw83252014-creator/grok-go-hackathon   @NousResearch #HermesHackathon`
3. **Stitch:** `~/agent-comms/bin/movie-stitch` (ffmpeg has NO drawtext on this mini — text via Pillow/HTML overlays only). Pair each shot with its VO timing from `HACKATHON-VIDEO-SCRIPT.md`. Output → `~/The-Device/production/grok-go-hackathon.mp4`.
4. **VO (optional):** generate from the 9 VO lines in the script (any TTS you have) or leave silent for Jeff to voice.
5. **Ping back** on the Agent Bridge (`:8787`) + leave files on the dashboard. Tell Fable the paths.

## Generation lane (pick cheapest that works)
- **Grok Imagine** (Chrome/X Grok lane) — the signature look. Userscript helper: `~/agent-bridge/grok-imagine.user.js`; queue: `~/agent-bridge/imagine-queue.json`; collector: `~/agent-bridge/imagine_collector.py`.
- **Gemini image gen** (`/opt/homebrew/bin/gemini`) — needs `GEMINI_API_KEY` or `gemini` login first (currently unauthed — `gemini` then sign in, or set the key).
- Whatever image model you have native — fine, as long as the house style holds.

## Plugins / tools you may need to install
- **ffmpeg** (stitch): `brew install ffmpeg` if missing.
- **Pillow** (text overlays): `python3 -m pip install Pillow --break-system-packages`.
- **Gemini CLI auth** (if using that lane): set `GEMINI_API_KEY` in env or run `gemini` and log in.
- Grok Imagine needs the logged-in Chrome (debug :9222 already running) — the userscript drives it.

## Why this matters / the spec in one line
A cinematic proof that Grok Go is a real, governed company-as-organism: it thinks (cells), remembers with receipts (research), acts (conscious), EARNS + SPENDS real money (Stripe), and STOPS on one touch (killswitch). That's the whole pitch in 90 seconds.
