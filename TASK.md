# Active Tasks

**Last Updated:** 2026-01-07 (End of Day - Session 2)

## ✅ Completed Today (Session 2)

### Sprint 3: AI Video Generation System

- [x] Set up Runway + Cartesia API integration
- [x] Create `scripts/generate_video.py` with full workflow
- [x] Add MEP-focused prompt templates (not generic construction)
- [x] Implement A/B testing framework (voice vs silent)
- [x] Add video chaining support (Last Keyframe Method)
- [x] Generate first 16-second chained video with voice
- [x] Document API integration in `docs/API_INTEGRATION.md`
- [x] Strengthen `.gitignore` for IP protection
- [x] Install ffmpeg for video/audio merging

### Security Sweep (End of Day)
- [x] Secrets scan - No hardcoded API keys in source
- [x] Git history scan - Clean, no exposed keys
- [x] Dependency audit - Standard packages, no vulnerabilities
- [x] Env file audit - All .env files properly gitignored

---

## ✅ Completed (Session 1)

### Sprint 1: Project Setup
- [x] Create project directory structure
- [x] Build Excel tracker with formulas
- [x] Create CLAUDE.md with Start Day Protocol
- [x] Create workflow documents (TASK, PLANNING, BACKLOG)
- [x] Initialize Git repository
- [x] Push to GitHub

### Sprint 2: Content Launch
- [x] Create Week 1 posts (EC-001, HV-001, PL-001)
- [x] Create response scripts with objection handlers
- [x] Create Loom video script template

### Sprint 2.5: Post Scheduler CLI
- [x] Create `scripts/post.py` CLI tool
- [x] Create `posts/schedule.json` config
- [x] Simplify README.md to GTME format

---

## 📋 Tomorrow's Priorities

1. **Test more video styles** - Generate abstract and text-overlay variants
2. **Create A/B test videos** - Use `--both` flag for voice/silent comparison
3. **Post first video** - Schedule EC-001 with video attachment
4. **Update Excel tracker** - Add video performance data

---

## ⏳ Pending (Next Sprint)

### [ ] Video Performance Tracking
- Track video views vs non-video posts
- Compare voice vs silent engagement
- Calculate video ROI (credits spent vs demos booked)

### [ ] LinkedIn Profile Optimization
- Update headline with clear value prop for MEP contractors
- Add "Featured" section with case study or testimonial

### [ ] Connection Building
- Add 50 Electrical contractors
- Add 50 HVAC contractors
- Add 50 Plumbing contractors

---

## 🚫 Blocked

_None currently_

---

## Video Generation Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Single 8-second video (silent)
python scripts/generate_video.py --post EC-001 --style pain-point

# Single video with voice
python scripts/generate_video.py --post EC-001 --style pain-point --voice

# A/B test (both voice + silent)
python scripts/generate_video.py --post EC-001 --style pain-point --both

# Longer video (16 seconds, chained)
python scripts/generate_video.py --post EC-001 --style pain-point --chain 2 --voice

# List available styles
python scripts/generate_video.py --list-styles
```

---

## Notes

- Videos are saved to `videos/runway/final/` (gitignored)
- Prompt templates are in `videos/runway/prompts/*.json`
- All .env files and videos are gitignored for IP protection
- ffmpeg installed via `brew install ffmpeg`
