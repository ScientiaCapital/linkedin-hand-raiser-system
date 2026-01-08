# LinkedIn Hand-Raiser System

Async demand gen for Coperniq. Post → Engage → Video → Demo.

## The System

**Target:** MEP+E contractors (Electrical, HVAC, Plumbing)

**Method:** Hand-raiser posts surface high-intent prospects. They comment/DM. You send a 5-min Loom. They book a demo.

**Why it works:** No cold outreach. They come to you.

---

## Quick Commands

```bash
# Post to LinkedIn (copies to clipboard, opens browser)
source venv/bin/activate
python scripts/post.py              # Today's scheduled post
python scripts/post.py EC-001       # Specific post

# Rebuild Excel tracker
python scripts/build_tracker.py
```

---

## Project Structure

```
├── posts/
│   ├── week1/                 # Post copy by week
│   ├── response-scripts.md    # Reply templates
│   └── schedule.json          # Posting schedule
├── videos/
│   └── loom_script_template.md
├── tracking/
│   └── linkedin_engagement_tracker.xlsx
└── scripts/
    ├── post.py                # CLI poster
    └── build_tracker.py       # Excel generator
```

---

## Workflow

| When | Action |
|------|--------|
| Mon/Wed/Fri 8am | `python scripts/post.py` → paste → post |
| Same day | Reply to comments, DM video to hand-raisers |
| Daily | Update Excel tracker with engagement data |

---

## Metrics

| Stage | Target |
|-------|--------|
| Engagement Rate | >5% |
| DM Conversion | >2% |
| Video → Demo | >30% |
| Demo → Close | >25% |
