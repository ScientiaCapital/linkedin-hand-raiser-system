# LinkedIn Hand-Raiser System

> **AI-powered LinkedIn content engine** for B2B lead generation.
> Runway video generation + Cartesia TTS + A/B testing framework.

---

## What It Does

- **AI video generation** with Runway + Cartesia voice synthesis
- **A/B testing framework** - voice vs text overlay vs text-only
- **Hand-raiser methodology** - "Comment X and I'll send you Y"
- **Excel tracker** with engagement rates and conversion metrics
- **3 vertical tracks** - Electrical, HVAC, Plumbing contractors

## Goals

Test LinkedIn posts for engagement and conversion. Find which pain points resonate with MEP contractors.

## Quick Start

```bash
cd linkedin-hand-raiser-system
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Generate A/B test videos
python scripts/generate_video.py --post EC-001 --style pain-point --both

# Build engagement tracker
python scripts/build_tracker.py
```

## Current Status

| Component | Status |
|-----------|--------|
| Project infrastructure | Complete |
| AI video generation | Working (Runway + Cartesia) |
| Excel tracker | Working |
| Post templates | 5 pain points ready |
| First posts | Scheduled |

## A/B Testing Framework

| Version | Stack | Schedule |
|---------|-------|----------|
| A | Runway video + Cartesia voice | Monday |
| B | Runway video + text overlay | Wednesday |
| C | Text only (control) | Friday |

## Pain Points Tested

1. Material Cost Overruns (copper/steel volatility)
2. Labor Burden Blindness (hidden costs)
3. Admin Time Waste (paperwork drowning)
4. Cash Flow Delays (slow invoicing)
5. Job Profitability Opacity (can't see profit)

## GTME Skills Developed

Building toward Go-To-Market Engineer through hands-on projects:

| Skill Area | What I Learned |
|------------|----------------|
| **Content marketing** | Hand-raiser methodology, hook formulas, CTAs that convert |
| **A/B testing** | Structured experiments with voice vs text vs video |
| **AI video production** | Runway text-to-video, Cartesia voice synthesis |
| **Engagement analytics** | Tracking impressions → engagement → DMs → demos → close |
| **Vertical segmentation** | Testing same message across Electrical/HVAC/Plumbing |
| **Response automation** | Personalized Loom videos within 24 hours |

## Tech Stack

Python, Runway API (video), Cartesia API (TTS), Excel tracking

## Success Metrics

| Metric | Target |
|--------|--------|
| Engagement rate | >5% |
| DM conversion | >2% |
| Video → Demo | >30% |
| Demo → Close | >25% |
