# LinkedIn Hand-Raiser GTME Motion

## Executive Summary

**What:** Async LinkedIn demand gen replacing cold outreach with high-intent inbound.

**How:** Post pain-point content → Prospects engage → Send 5-min Loom → Book demo.

**Why:** Cold email is dying (2% response). This flips the dynamic - they come to us.

---

## The Motion

```
Post (3x/week) → Engagement → DM → Loom Video → Demo → Close
     ↓              ↓          ↓        ↓          ↓
   ~1,000        ~5%        ~3/post   ~30%      ~25%
 impressions   engage       DM us   book demo   close
```

**Math:** 12 posts/month × 3 DMs = 36 hand-raisers × 30% = 11 demos × 25% = **2-3 closes/month**

---

## Target Audience

| Vertical | Pain Point | Post ID |
|----------|-----------|---------|
| Electrical | Material cost overruns (copper spikes) | EC-001 |
| HVAC | Labor burden blindness ("80% done" myth) | HV-001 |
| Plumbing | Admin time waste (timecard chasing) | PL-001 |

**ICP:** 10-100 employees, $2M-$50M revenue, using QuickBooks

---

## What's Ready

### Content
- 3 LinkedIn posts (Mon/Wed/Fri) - copy approved, ready to schedule
- Response scripts for comments and DMs
- Objection handlers for common pushbacks

### Loom Scripts
- `EC-loom-material-costs.md` - Electrical vertical (5 min)
- `HV-loom-labor-burden.md` - HVAC vertical (5 min)
- `PL-loom-admin-burden.md` - Plumbing vertical (5 min)

### Tooling
- Excel tracker with auto-calculated metrics
- CLI tool for posting (`python scripts/post.py`)
- 8am M/W/F reminder system installed

---

## Loom Recording Requirements

**Who should record:** Someone who can demo Coperniq + talk to contractors naturally.

**What you need:**
1. Coperniq demo environment with sample data
2. Loom account (free tier works)
3. 15 minutes per video (5 min recording + takes)

**Script location:** `videos/scripts/`

Each script has:
- Word-for-word talk track
- Screen navigation instructions
- Pre-recording checklist

---

## Time Investment

| Activity | Weekly Time |
|----------|-------------|
| Post creation/scheduling | 30 min |
| Engagement monitoring (2x/day) | 100 min |
| Video responses | 60 min |
| Weekly review | 15 min |
| **Total** | **~3.5 hrs/week** |

---

## Success Metrics

| Week | Focus | Success Criteria |
|------|-------|------------------|
| 1 | Baseline | 3 posts live, tracking engagement |
| 2 | Identify winner | Which vertical/pain point performs best |
| 3 | First demos | Hand-raisers converting to demos |
| 4 | Full review | CAC calculation, scale or pivot |

**Target CAC:** <$300/customer (vs $3,000 cold email)

---

## Recommendation

1. **Tim posts content** - Already has CLI tool + reminders set up
2. **[CEO/CTO] records Looms** - Better for credibility with contractor owners
3. **Tim sends videos + books demos** - Handles DM flow

This splits the work and puts the right face on the videos.

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/ScientiaCapital/linkedin-hand-raiser-system.git

# View Loom scripts
cat videos/scripts/EC-loom-material-costs.md

# Test the posting CLI
source venv/bin/activate
python scripts/post.py --list
```

---

## Files Reference

| File | Purpose |
|------|---------|
| `posts/week1/*.md` | Post copy to paste in LinkedIn |
| `posts/response-scripts.md` | DM reply templates |
| `videos/scripts/*.md` | Loom recording scripts |
| `tracking/linkedin_engagement_tracker.xlsx` | Performance tracking |
| `docs/weekly_workflow.md` | Day-by-day process |

---

**Repo:** https://github.com/ScientiaCapital/linkedin-hand-raiser-system

**Owner:** Tim Kipper, Sr BDR @ Coperniq
