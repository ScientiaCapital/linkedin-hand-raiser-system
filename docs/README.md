# LinkedIn Hand-Raiser System

**GTME for B2B SaaS.** AI-generated videos + voice narration for LinkedIn. Built with Claude Code in one session.

---

## What It Does

Turn LinkedIn posts into an A/B testing machine:

| Version | Stack |
|---------|-------|
| **A** | Runway video + Cartesia voice |
| **B** | Runway video + text overlay |
| **C** | Text only (control) |

Post → Track → Learn → Iterate.

---

## The Tech

```
Runway Gen-3      → AI video generation
Cartesia Sonic-2  → Voice narration
Python + openpyxl → Engagement tracking
Claude Code       → Built it all
```

---

## Quick Start

```bash
# Generate both versions for A/B testing
python scripts/generate_video.py --post EC-001 --style pain-point --both

# Rebuild Excel tracker with video analytics
python scripts/build_tracker.py
```

---

## Dashboard Tracks

- Video type performance (Runway vs Loom vs None)
- Style effectiveness (Abstract vs Pain Point vs Text)
- Cost per engagement, engagement lift
- Full conversion funnel

---

## Why

Cold outreach is dead. Make prospects come to you.

1. Post pain-point content → They self-identify
2. Send AI video → Stand out instantly
3. Book demo → They're already warm

---

*More details in [PROJECT_CONTEXT.md](./PROJECT_CONTEXT.md)*
