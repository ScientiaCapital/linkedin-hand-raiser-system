# LinkedIn Hand-Raiser System

## Overview
Async LinkedIn demand gen system for Coperniq using promise-based hand-raiser posts + 5-minute video responses.

**Goal:** Replace cold outreach with high-intent inbound leads from MEP+E contractors.

## System Components

### 1. Tracking (`/tracking`)
- `linkedin_engagement_tracker.xlsx` - Main performance dashboard
- Track: Post engagement, DM conversion, video→demo rates, pipeline

### 2. Posts (`/posts`)
- Draft posts before publishing
- Archive published posts with engagement data
- Template library for each vertical (Electrical, HVAC, Plumbing)

### 3. Videos (`/videos`)
- Loom script templates for responses
- Video link archive
- Demo conversion tracking

### 4. Scripts (`/scripts`)
- `build_tracker.py` - Generates Excel tracker
- Future automation scripts as needed

## Quick Start

1. **Update tracker daily** (5 min):
   - Add new post data from LinkedIn analytics
   - Log DMs/comments received
   - Track video sends + demo bookings

2. **Weekly review** (15 min, Monday 9am):
   - Review Dashboard tab
   - Identify highest-performing pain points
   - Plan next 3 posts (Mon/Wed/Fri)

3. **Video response protocol**:
   - Respond to DMs within 24 hours
   - Use Loom templates from `/videos`
   - Track in Response Tracker tab

## Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Post Engagement Rate | >5% | TBD |
| DM Conversion Rate | >2% | TBD |
| Video→Demo Rate | >30% | TBD |
| Demo→Close Rate | >25% | TBD |



---

**Last Updated:** 2025-01-07
**Owner:** Tim Kipper, Sr BDR @ Coperniq
