# API Integration Guide

Technical documentation for Runway and Cartesia integrations.

---

## Cartesia (Voice Synthesis)

### Overview
- **Product**: Sonic-3 TTS (Text-to-Speech)
- **Latency**: ~90ms time-to-first-audio
- **Languages**: 42 supported
- **Features**: Emotional tagging, laughter generation, speed control

### Installation

```bash
pip install cartesia
```

### Authentication

```python
from cartesia import Cartesia

# Sync client
client = Cartesia(api_key=os.environ["CARTESIA_API_KEY"])

# Async client
from cartesia import AsyncCartesia
client = AsyncCartesia(api_key=os.environ["CARTESIA_API_KEY"])
```

### API Headers (for direct HTTP)

```python
headers = {
    "Authorization": f"Bearer {api_key}",
    "Cartesia-Version": "2025-04-16",
    "Content-Type": "application/json",
}
```

### Models

| Model | Description | Use Case |
|-------|-------------|----------|
| `sonic-3` | Latest stable (auto-updates) | Production |
| `sonic-3-2025-10-27` | Pinned snapshot | Version control |
| `sonic-3-latest` | Beta features | Testing only |
| `sonic-2` | Legacy (40ms latency) | Low-latency needs |

### Emotional Tagging (Sonic-3)

```python
# Add emotion tags inline with text
transcript = "I can't believe it! [laughter] That's amazing!"

# Supported tags
# [laughter] - Natural laughter
# Control via SSML tags for fine-grained emotion
```

### Voice Selection

| Voice | Style | Best For |
|-------|-------|----------|
| Katie | Stable, realistic | Voice agents |
| Kiefer | Professional | Business content |
| Tessa | Emotive | Character work |
| Kyle | Expressive | Engaging content |

Default Voice ID: `a0e99841-438c-4a64-b679-ae501e7d6091`

### TTS Request Format

```python
# POST /tts/bytes
{
    "model_id": "sonic-3",
    "transcript": "Your text here [laughter]",
    "voice": {
        "mode": "id",
        "id": "a0e99841-438c-4a64-b679-ae501e7d6091"
    },
    "output_format": {
        "container": "wav",
        "encoding": "pcm_s16le",
        "sample_rate": 44100
    },
    "language": "en"
}
```

### SDK Methods

```python
# Generate audio bytes
audio = client.tts.bytes(
    model_id="sonic-3",
    transcript="Hello world",
    voice={"mode": "id", "id": voice_id},
    output_format={"container": "wav", "sample_rate": 44100}
)

# List voices
voices = client.voices.list()

# Clone voice from audio sample
new_voice = client.voices.clone(audio_sample, name="Custom Voice")

# Mix multiple voices
mixed = client.voices.mix([voice1_id, voice2_id], weights=[0.7, 0.3])
```

### Resources

- [Cartesia Docs](https://docs.cartesia.ai)
- [PyPI Package](https://pypi.org/project/cartesia/)
- [Sonic-3 Model](https://docs.cartesia.ai/build-with-cartesia/tts-models/latest)

---

## Runway (AI Video Generation)

### Overview
- **Product**: Gen-3 Alpha Turbo (text-to-video)
- **Speed**: Up to 7x faster than standard
- **Cost**: ~50% cheaper than Gen-3 Alpha
- **Duration**: 4, 6, or 8 seconds

### Authentication

```python
# Environment variable
RUNWAYML_API_SECRET=your_api_key

# Header format
headers = {
    "Authorization": f"Bearer {api_key}",
    "X-Runway-Version": "2024-11-06",
    "Content-Type": "application/json",
}
```

### Models

| Model | Description | Use Case |
|-------|-------------|----------|
| `gen3a_turbo` | Gen-3 Alpha Turbo | Fast, cost-effective |
| `gen4_turbo` | Gen-4 Turbo | Higher quality |
| `veo3.1` | Veo 3.1 | Alternative style |

### Endpoints

#### Text-to-Video
```
POST https://api.dev.runwayml.com/v1/text_to_video
```

```python
{
    "model": "gen3a_turbo",
    "promptText": "Your description up to 1000 chars",
    "ratio": "1280:720",
    "duration": 4
}
```

#### Image-to-Video
```
POST https://api.dev.runwayml.com/v1/image_to_video
```

```python
{
    "model": "gen4_turbo",
    "promptImage": "https://...",  # or data URI
    "promptText": "Motion description",
    "ratio": "1280:720",
    "duration": 4
}
```

#### Check Task Status
```
GET https://api.dev.runwayml.com/v1/tasks/{task_id}
```

### Supported Ratios

| Ratio | Orientation |
|-------|-------------|
| `1280:720` | Landscape (16:9) |
| `720:1280` | Portrait (9:16) |
| `1080:1920` | Portrait HD |
| `1920:1080` | Landscape HD |
| `960:960` | Square |

### Async Workflow

```python
import asyncio
import httpx

async def generate_video(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        # 1. Start task
        response = await client.post(
            "https://api.dev.runwayml.com/v1/text_to_video",
            headers={
                "Authorization": f"Bearer {api_key}",
                "X-Runway-Version": "2024-11-06",
            },
            json={
                "model": "gen3a_turbo",
                "promptText": prompt,
                "ratio": "1280:720",
                "duration": 4,
            }
        )
        task_id = response.json()["id"]

        # 2. Poll for completion
        while True:
            status = await client.get(
                f"https://api.dev.runwayml.com/v1/tasks/{task_id}",
                headers={...}
            )
            data = status.json()
            if data["status"] == "SUCCEEDED":
                return data["output"]["url"]
            elif data["status"] == "FAILED":
                raise Exception(data.get("error"))
            await asyncio.sleep(5)
```

### Resources

- [Runway API Docs](https://docs.dev.runwayml.com/api/)
- [Developer Portal](https://dev.runwayml.com/)
- [Model Guide](https://runwayml.com/api)

---

## Environment Variables

```bash
# .env file
RUNWAY_API_KEY=your_runway_key
CARTESIA_API_KEY=your_cartesia_key

# Optional
CARTESIA_VOICE_ID=a0e99841-438c-4a64-b679-ae501e7d6091
CARTESIA_SPEED=1.0
RUNWAY_COST_PER_CREDIT=0.05
```

---

## Error Handling

### Cartesia Errors

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid API key | Check CARTESIA_API_KEY |
| 400 | Invalid request | Check model_id, voice format |
| 429 | Rate limited | Implement backoff |

### Runway Errors

| Status | Meaning | Action |
|--------|---------|--------|
| 401 | Invalid API key | Check RUNWAY_API_KEY |
| 400 | Invalid prompt | Shorten to <1000 chars |
| 500 | Generation failed | Retry with simpler prompt |

---

## Video Chaining (Longer Videos)

### The Challenge
- Text-to-video: Max 8 seconds per generation
- Image-to-video: Max 10 seconds per generation
- LinkedIn optimal: 15-30 seconds for engagement

### Last Keyframe Method (Recommended)

The proper way to create longer, smooth videos:

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Generate       │     │  Extract Last   │     │  Generate       │
│  Clip 1 (10s)   │ ──► │  Frame as PNG   │ ──► │  Clip 2 (10s)   │
│  text-to-video  │     │  (finalframe)   │     │  image-to-video │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Repeat up to   │
                                               │  3x = 40s total │
                                               └─────────────────┘
```

### Step-by-Step Workflow

```python
import asyncio
from PIL import Image
import cv2

async def chain_videos(prompts: list[str], duration_per_clip: int = 10) -> list[str]:
    """Generate chained video clips using last-keyframe method."""
    video_paths = []

    # 1. Generate first clip (text-to-video)
    clip1 = await generate_text_to_video(prompts[0], duration=duration_per_clip)
    video_paths.append(clip1)

    for prompt in prompts[1:]:
        # 2. Extract last frame from previous video
        last_frame = extract_last_frame(video_paths[-1])

        # 3. Upload frame and generate continuation (image-to-video)
        clip = await generate_image_to_video(
            image_path=last_frame,
            prompt=prompt,
            duration=duration_per_clip,
            position="first"  # Use image as opening frame
        )
        video_paths.append(clip)

    return video_paths

def extract_last_frame(video_path: str) -> str:
    """Extract the last frame as PNG for continuity."""
    cap = cv2.VideoCapture(video_path)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count - 1)
    ret, frame = cap.read()
    cap.release()

    output_path = video_path.replace('.mp4', '_lastframe.png')
    cv2.imwrite(output_path, frame)
    return output_path
```

### Image-to-Video API for Chaining

```python
# POST https://api.dev.runwayml.com/v1/image_to_video
{
    "model": "gen4_turbo",        # Better for continuity
    "promptImage": "data:image/png;base64,...",  # Last frame
    "position": "first",          # CRITICAL: Use as opening frame
    "promptText": "Continue the motion smoothly...",
    "duration": 10,               # Max for image-to-video
    "ratio": "1280:720"
}
```

### Duration Limits by Model

| Model | Endpoint | Max Duration | Extensions |
|-------|----------|--------------|------------|
| `veo3.1_fast` | text-to-video | 8 seconds | N/A |
| `gen4_turbo` | image-to-video | 10 seconds | 3x = 40s |
| `gen3a_turbo` | image-to-video | 10 seconds | 3x = 40s |

### Best Practices for Smooth Transitions

1. **Consistent prompts** - Use similar visual language across clips
2. **Same color palette** - Mention colors in each prompt
3. **Stable last frame** - Pick frame from last 0.5s for stability
4. **Minimal camera movement** - At clip boundaries
5. **Same subject focus** - Don't introduce new elements at transitions

---

## Voice + Video Integration

### The Complete Workflow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Write      │    │  Generate    │    │  Generate    │    │   Merge      │
│   Script     │ ─► │  Voice       │ ─► │  Video       │ ─► │   with       │
│   (text)     │    │  (Cartesia)  │    │  (Runway)    │    │   ffmpeg     │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```

### Timing Synchronization

**Match voice duration to video duration:**

```python
import wave
import struct

def get_audio_duration(wav_path: str) -> float:
    """Get WAV file duration in seconds."""
    with wave.open(wav_path, 'rb') as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        return frames / rate

# Example: Generate 8s video to match voice
voice_duration = get_audio_duration("narration.wav")  # e.g., 7.5s
video_duration = 8  # Round up to nearest supported (4, 6, 8)
```

### ffmpeg Merge Commands

**Basic merge (voice replaces video audio):**
```bash
ffmpeg -i video.mp4 -i voice.wav -c:v copy -c:a aac \
    -map 0:v:0 -map 1:a:0 output.mp4
```

**With crossfade transition between clips:**
```bash
ffmpeg -i clip1.mp4 -i clip2.mp4 \
    -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=9.5[v]" \
    -map "[v]" -c:v libx264 output.mp4
```

**Merge multiple clips + voice:**
```bash
# 1. Concat video clips
ffmpeg -f concat -i clips.txt -c copy combined_video.mp4

# 2. Add voice track
ffmpeg -i combined_video.mp4 -i voice.wav -c:v copy -c:a aac final.mp4
```

### clips.txt format for concat:
```
file 'clip1.mp4'
file 'clip2.mp4'
file 'clip3.mp4'
```

### A/B Test Variants

| Variant | Voice | Text Overlay | Video |
|---------|-------|--------------|-------|
| A | Cartesia narration | None | Runway |
| B | None | Burned in | Runway |
| C | None | None | Runway only |

### Python Integration Example

```python
import subprocess

def merge_voice_video(video_path: str, audio_path: str, output_path: str):
    """Merge Cartesia voice with Runway video using ffmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-shortest",  # Match shorter duration
        output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path
```

### Install ffmpeg (macOS)

```bash
brew install ffmpeg
```

---

## Cost Estimates

| Service | Unit | Approximate Cost |
|---------|------|------------------|
| Cartesia Sonic-3 | per 1K chars | ~$0.01 |
| Runway Gen-3 Turbo | per 4s video | ~$0.25 |
| Runway Gen-3 Turbo | per 8s video | ~$0.50 |

---

*Last updated: 2026-01-07*
