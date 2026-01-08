# Video Generation Workflow

Quick reference for creating LinkedIn videos with CEO/CTO.

---

## 1. Pick a Post

```bash
# See available posts
ls posts/week1/
```

Available:
- `EC-001` - Electrical: Material Cost Overruns
- `HV-001` - HVAC: Labor Burden
- `PL-001` - Plumbing: Admin Burden

---

## 2. Pick a Style

```bash
# See available styles
python scripts/generate_video.py --list-styles
```

| Style | Best For |
|-------|----------|
| `pain-point` | Emotional connection, show the problem |
| `text-overlay` | Key stats, impactful words |
| `abstract` | Attention hooks, motion graphics |
| `before-after` | Transformation, solution reveal |

---

## 3. Generate Videos

### A/B Test (Both Versions)
```bash
python scripts/generate_video.py --post EC-001 --style pain-point --both
```

### Voice Only
```bash
python scripts/generate_video.py --post HV-001 --style text-overlay --voice
```

### Silent Only
```bash
python scripts/generate_video.py --post PL-001 --style abstract --no-voice
```

---

## 4. Find Your Videos

```bash
ls videos/runway/final/
```

Videos saved as:
- `{POST}_{STYLE}_{TIMESTAMP}_voice.mp4`
- `{POST}_{STYLE}_{TIMESTAMP}_silent.mp4`

---

## 5. Post & Track

### Posting Schedule
| Day | Version | Why |
|-----|---------|-----|
| Mon | A (Voice) | Peak engagement |
| Wed | B (Silent) | Comparison |
| Fri | C (Text only) | Control |

### Update Tracker
```bash
python scripts/build_tracker.py
open tracking/linkedin_engagement_tracker.xlsx
```

---

## Quick Commands Reference

```bash
# Setup (first time)
source venv/bin/activate
pip install -r requirements.txt

# List styles
python scripts/generate_video.py --list-styles

# List voices (if Cartesia configured)
python scripts/generate_video.py --list-voices

# Generate A/B test videos
python scripts/generate_video.py --post EC-001 --style pain-point --both

# Rebuild tracker
python scripts/build_tracker.py
```

---

## API Keys Needed

Add to `.env`:
```
RUNWAY_API_KEY=your_key
CARTESIA_API_KEY=your_key
```

Get keys:
- Runway: https://app.runwayml.com/settings/api-keys
- Cartesia: https://cartesia.ai (you already have one!)
