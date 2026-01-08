#!/usr/bin/env python3
"""
LinkedIn Video Generator with Runway + Cartesia

Generates AI videos for LinkedIn posts with optional voice narration.
Supports A/B testing: video+voice vs video+text-only vs text-only.

Usage:
    python scripts/generate_video.py --post EC-004 --style pain-point
    python scripts/generate_video.py --post EC-004 --style pain-point --voice
    python scripts/generate_video.py --post EC-004 --style text-overlay --no-voice
    python scripts/generate_video.py --list-styles
    python scripts/generate_video.py --list-voices
"""

import os
import sys
import json
import asyncio
import argparse
import subprocess
import base64
from pathlib import Path
from datetime import datetime
from typing import Optional, List

import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
POSTS_DIR = PROJECT_ROOT / "posts"
VIDEOS_DIR = PROJECT_ROOT / "videos" / "runway"
PROMPTS_DIR = VIDEOS_DIR / "prompts"

# API Keys
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
CARTESIA_VOICE_ID = os.getenv("CARTESIA_VOICE_ID", "a0e99841-438c-4a64-b679-ae501e7d6091")
CARTESIA_SPEED = float(os.getenv("CARTESIA_SPEED", "1.0"))

# API URLs
RUNWAY_API_URL = "https://api.runwayml.com/v1"
CARTESIA_API_URL = "https://api.cartesia.ai"


# ========================================
# Video Style Templates (Load from JSON)
# ========================================

def load_video_styles() -> dict:
    """Load video styles from JSON files in prompts/ directory."""
    styles = {}
    for json_file in PROMPTS_DIR.glob("*.json"):
        try:
            with open(json_file) as f:
                style_data = json.load(f)
                style_name = style_data.get("style", json_file.stem)
                styles[style_name] = style_data
        except Exception as e:
            print(f"⚠️  Failed to load {json_file}: {e}")

    # Fallback to hardcoded if no JSON files found
    if not styles:
        styles = {
            "abstract": {
                "name": "Abstract Motion",
                "template": "Abstract motion graphics: {key_phrase}. Flowing electrical current, HVAC airflow patterns. Blue, orange, copper palette. 8 seconds, cinematic.",
                "best_for": ["attention hooks"],
                "duration": 8,
                "voice_script": "short"
            },
            "pain-point": {
                "name": "Pain Point Illustration",
                "template": "Dramatic visualization: {pain_point}. Electrical contractor or HVAC tech stressed, service van in background. Dark to hope transition. 8 seconds, cinematic.",
                "best_for": ["emotional connection"],
                "duration": 8,
                "voice_script": "full"
            },
            "text-overlay": {
                "name": "Text Overlay",
                "template": "Kinetic typography: '{key_words}'. Bold font, blurred service van background. Blue and orange. 8 seconds.",
                "best_for": ["message reinforcement"],
                "duration": 8,
                "voice_script": "key_phrase"
            },
            "before-after": {
                "name": "Before-After Transformation",
                "template": "Split screen: Left stressed trade pro, right organized with tablet. Smooth morph. 8 seconds.",
                "best_for": ["solution reveal"],
                "duration": 8,
                "voice_script": "full"
            }
        }
    return styles

# Load styles at module import
VIDEO_STYLES = load_video_styles()


# ========================================
# Post Reader
# ========================================

def find_post_file(post_id: str) -> Optional[Path]:
    """Find the post file by ID across all folders."""
    # Search patterns
    patterns = [
        f"**/{post_id}.md",
        f"**/{post_id.lower()}.md",
        f"**/{post_id.upper()}.md",
    ]

    for pattern in patterns:
        matches = list(POSTS_DIR.glob(pattern))
        if matches:
            return matches[0]

    return None


def read_post(post_id: str) -> dict:
    """Read post content and extract key elements."""
    post_path = find_post_file(post_id)

    if not post_path:
        # Return sample data if post not found
        print(f"⚠️  Post {post_id} not found, using sample content")
        return {
            "id": post_id,
            "content": "Material costs up 40% this year. Most contractors are bleeding money without knowing it.",
            "pain_point": "Material Cost Overruns",
            "key_phrase": "Material costs up 40%",
            "key_words": "MATERIAL COSTS UP 40%",
            "vertical": post_id[:2].upper()
        }

    content = post_path.read_text()

    # Extract metadata from markdown frontmatter if present
    pain_point = "Business Pain"
    vertical = post_id[:2].upper()

    # Simple extraction of first sentence/key phrase
    lines = [l.strip() for l in content.split('\n') if l.strip() and not l.startswith('#')]
    first_line = lines[0] if lines else content[:100]

    return {
        "id": post_id,
        "content": content,
        "pain_point": pain_point,
        "key_phrase": first_line[:100],
        "key_words": first_line[:50].upper(),
        "vertical": vertical
    }


# ========================================
# Cartesia Voice Client
# ========================================

class CartesiaClient:
    """Client for Cartesia TTS API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = CARTESIA_API_URL

    async def synthesize(
        self,
        text: str,
        voice_id: str = CARTESIA_VOICE_ID,
        speed: float = CARTESIA_SPEED,
    ) -> bytes:
        """Synthesize text to audio."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/tts/bytes",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Cartesia-Version": "2025-04-16",
                    "Content-Type": "application/json",
                },
                json={
                    "model_id": "sonic-3",  # Latest model with emotional tagging
                    "transcript": text,
                    "voice": {
                        "mode": "id",
                        "id": voice_id,
                    },
                    "language": "en",
                    "output_format": {
                        "container": "wav",
                        "encoding": "pcm_s16le",
                        "sample_rate": 44100,
                    },
                }
            )

            if response.status_code != 200:
                raise Exception(f"Cartesia error: {response.text}")

            return response.content

    async def list_voices(self) -> list:
        """List available voices."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/voices",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Cartesia-Version": "2025-04-16"
                }
            )
            return response.json()


# ========================================
# Runway Video Client
# ========================================

class RunwayClient:
    """Client for Runway ML API.

    Docs: https://docs.dev.runwayml.com/api/
    Models: gen4_turbo, gen3a_turbo, veo3.1
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.dev.runwayml.com"

    async def generate_video(
        self,
        prompt: str,
        duration: int = 4,
        ratio: str = "1280:720"
    ) -> dict:
        """Generate video from text prompt.

        Args:
            prompt: Text description (up to 1000 chars)
            duration: 4, 6, or 8 seconds
            ratio: "1280:720", "720:1280", "1080:1920", "1920:1080"

        Returns:
            dict with task_id for polling status
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/v1/text_to_video",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "X-Runway-Version": "2024-11-06",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "veo3.1_fast",  # Veo 3.1 Fast (quick generation)
                    "promptText": prompt[:1000],
                    "ratio": ratio,
                    "duration": duration,
                }
            )

            if response.status_code not in [200, 201]:
                print(f"⚠️  Runway API error: {response.text}")
                return {"status": "error", "error": response.text}

            result = response.json()
            task_id = result.get('id')
            print(f"🎬 Runway task started: {task_id}")

            # Poll for completion
            print("⏳ Waiting for video generation...")
            for attempt in range(60):  # Max 5 minutes
                await asyncio.sleep(5)
                status_response = await client.get(
                    f"{self.base_url}/v1/tasks/{task_id}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "X-Runway-Version": "2024-11-06",
                    }
                )
                status_data = status_response.json()
                status = status_data.get('status', 'UNKNOWN')

                if status == 'SUCCEEDED':
                    print(f"✅ Video generated!")
                    return status_data
                elif status == 'FAILED':
                    print(f"❌ Generation failed: {status_data.get('error', 'Unknown error')}")
                    return {"status": "error", "error": status_data.get('error')}
                elif status in ['PENDING', 'RUNNING']:
                    print(f"   Status: {status} ({attempt * 5}s elapsed)")
                else:
                    print(f"   Status: {status}")

            return {"status": "error", "error": "Timeout waiting for video"}

    async def get_task_status(self, task_id: str) -> dict:
        """Check status of video generation task."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/v1/tasks/{task_id}",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "X-Runway-Version": "2024-11-06",
                }
            )
            return response.json()

    async def image_to_video(
        self,
        image_path: str,
        prompt: str,
        duration: int = 10,
        ratio: str = "1280:720"
    ) -> dict:
        """Generate video from image (for chaining/extending).

        Uses the last frame of a previous video to create smooth continuation.

        Args:
            image_path: Path to PNG/JPG image (or data URI)
            prompt: Motion description
            duration: 2-10 seconds
            ratio: Aspect ratio

        Returns:
            dict with video URL
        """
        # Convert image to data URI if it's a file path
        if image_path.startswith("data:"):
            image_data = image_path
        else:
            with open(image_path, "rb") as f:
                img_bytes = f.read()
            ext = Path(image_path).suffix.lower()
            mime = "image/png" if ext == ".png" else "image/jpeg"
            b64 = base64.b64encode(img_bytes).decode()
            image_data = f"data:{mime};base64,{b64}"

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/v1/image_to_video",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "X-Runway-Version": "2024-11-06",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gen4_turbo",  # Better for image-to-video
                    "promptImage": image_data,
                    "position": "first",  # Use image as opening frame
                    "promptText": prompt[:1000],
                    "ratio": ratio,
                    "duration": min(duration, 10),  # Max 10s for image-to-video
                }
            )

            if response.status_code not in [200, 201]:
                return {"status": "error", "error": response.text}

            result = response.json()
            task_id = result.get('id')
            print(f"🎬 Image-to-video task started: {task_id}")

            # Poll for completion
            for attempt in range(60):
                await asyncio.sleep(5)
                status_response = await client.get(
                    f"{self.base_url}/v1/tasks/{task_id}",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "X-Runway-Version": "2024-11-06",
                    }
                )
                status_data = status_response.json()
                status = status_data.get('status', 'UNKNOWN')

                if status == 'SUCCEEDED':
                    print(f"✅ Continuation clip generated!")
                    return status_data
                elif status == 'FAILED':
                    return {"status": "error", "error": status_data.get('error')}
                elif status in ['PENDING', 'RUNNING']:
                    print(f"   Extending: {status} ({attempt * 5}s)")

            return {"status": "error", "error": "Timeout"}


# ========================================
# Video Generator
# ========================================

class LinkedInVideoGenerator:
    """Generates LinkedIn videos with Runway + Cartesia."""

    def __init__(self):
        self.runway = RunwayClient(RUNWAY_API_KEY) if RUNWAY_API_KEY else None
        self.cartesia = CartesiaClient(CARTESIA_API_KEY) if CARTESIA_API_KEY else None

        # Ensure output directories exist
        VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        (VIDEOS_DIR / "audio").mkdir(exist_ok=True)
        (VIDEOS_DIR / "final").mkdir(exist_ok=True)

    def generate_prompt(self, post: dict, style: str) -> str:
        """Generate Runway prompt from post content and style."""
        if style not in VIDEO_STYLES:
            raise ValueError(f"Unknown style: {style}. Options: {list(VIDEO_STYLES.keys())}")

        template = VIDEO_STYLES[style]["template"]

        return template.format(
            key_phrase=post["key_phrase"],
            pain_point=post["pain_point"],
            key_words=post["key_words"],
        )

    def get_voice_script(self, post: dict, style: str) -> str:
        """Get the appropriate voice script based on style.

        Uses Cartesia Sonic-3 emotional tagging for expressive delivery.
        Supported tags: [laughter], and SSML for fine-grained control.
        """
        script_type = VIDEO_STYLES[style].get("voice_script", "short")

        if script_type == "full":
            # Use first paragraph or 200 chars
            content = post["content"]
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            text = paragraphs[0][:200] if paragraphs else content[:200]
        elif script_type == "key_phrase":
            text = post["key_phrase"]
        else:  # short
            text = post["key_phrase"][:80]

        # Add emotional delivery based on style
        if style == "pain-point":
            # More dramatic delivery for pain point content
            return f"{text}... Sound familiar?"
        elif style == "before-after":
            # Hopeful transition
            return f"{text} But it doesn't have to be this way."
        else:
            return text

    async def generate_voice(self, text: str, output_path: Path) -> Path:
        """Generate voice audio using Cartesia."""
        if not self.cartesia:
            raise ValueError("Cartesia API key not configured")

        print(f"🎤 Generating voice: {text[:50]}...")
        audio_data = await self.cartesia.synthesize(text)

        output_path.write_bytes(audio_data)
        print(f"✅ Audio saved: {output_path}")

        return output_path

    async def generate_video(self, prompt: str, output_path: Path) -> Path:
        """Generate video using Runway."""
        if not self.runway or not RUNWAY_API_KEY:
            # Demo mode - create placeholder
            print("⚠️  DEMO MODE: Runway API key not configured")
            print(f"   Would generate video with prompt:")
            print(f"   \"{prompt[:100]}...\"")
            print(f"   📁 Placeholder saved to: {output_path}")

            output_path.write_text(f"""DEMO MODE - Runway Video Placeholder
=====================================
This file represents where your AI video would be saved.

PROMPT THAT WOULD BE SENT TO RUNWAY:
{prompt}

TO ENABLE REAL VIDEO GENERATION:
1. Get API key from: https://app.runwayml.com/settings/api-keys
2. Add to .env: RUNWAY_API_KEY=your_key_here
3. Re-run this command

Generated: {datetime.now().isoformat()}
""")
            return output_path

        result = await self.runway.generate_video(prompt)

        # Check for errors
        if result.get("status") == "error":
            print(f"❌ Video generation failed: {result.get('error', 'Unknown error')}")
            output_path.write_text(f"ERROR: {result.get('error', 'Unknown error')}\nPrompt: {prompt}")
            return output_path

        # Download the video from the output URL
        video_url = result.get("output", [None])[0]
        if video_url:
            print(f"📥 Downloading video from: {video_url[:50]}...")
            async with httpx.AsyncClient(timeout=120.0) as client:
                video_response = await client.get(video_url)
                if video_response.status_code == 200:
                    # Change extension to .mp4
                    output_path = output_path.with_suffix('.mp4')
                    output_path.write_bytes(video_response.content)
                    print(f"✅ Video saved: {output_path} ({len(video_response.content):,} bytes)")
                else:
                    print(f"⚠️  Failed to download video: {video_response.status_code}")
                    output_path.write_text(f"Download failed\nURL: {video_url}")
        else:
            print(f"⚠️  No video URL in response")
            output_path.write_text(f"No video URL\nResponse: {json.dumps(result, indent=2)}")

        return output_path

    def merge_video_audio(self, video_path: Path, audio_path: Path, output_path: Path) -> Path:
        """Merge video and audio using ffmpeg."""
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Merged video+audio: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  ffmpeg merge failed: {e.stderr.decode()}")
            import shutil
            shutil.copy(video_path, output_path)
        except FileNotFoundError:
            print("⚠️  ffmpeg not found. Install with: brew install ffmpeg")
            import shutil
            shutil.copy(video_path, output_path)

        return output_path

    def extract_last_frame(self, video_path: Path) -> Path:
        """Extract the last frame from a video for chaining."""
        output_path = video_path.with_suffix('.png')

        cmd = [
            "ffmpeg", "-y",
            "-sseof", "-0.5",  # Start 0.5s before end
            "-i", str(video_path),
            "-frames:v", "1",  # Just one frame
            "-q:v", "2",  # High quality
            str(output_path)
        ]

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"📸 Extracted last frame: {output_path}")
            return output_path
        except Exception as e:
            print(f"⚠️  Frame extraction failed: {e}")
            return None

    def concat_videos_crossfade(
        self,
        video_paths: List[Path],
        output_path: Path,
        crossfade_duration: float = 0.5
    ) -> Path:
        """Concatenate videos with crossfade transitions."""
        if len(video_paths) == 1:
            import shutil
            shutil.copy(video_paths[0], output_path)
            return output_path

        # Build ffmpeg filter for crossfade
        # For 2 clips: [0:v][1:v]xfade=transition=fade:duration=0.5:offset=X[v]
        filter_parts = []
        current_offset = 0

        for i in range(len(video_paths) - 1):
            # Get video duration (approximate 8s per clip)
            clip_duration = 8
            offset = current_offset + clip_duration - crossfade_duration

            if i == 0:
                filter_parts.append(
                    f"[0:v][1:v]xfade=transition=fade:duration={crossfade_duration}:offset={offset}[v{i}]"
                )
            else:
                filter_parts.append(
                    f"[v{i-1}][{i+1}:v]xfade=transition=fade:duration={crossfade_duration}:offset={offset}[v{i}]"
                )
            current_offset = offset

        # Build command
        cmd = ["ffmpeg", "-y"]
        for vp in video_paths:
            cmd.extend(["-i", str(vp)])

        if len(video_paths) == 2:
            filter_complex = f"[0:v][1:v]xfade=transition=fade:duration={crossfade_duration}:offset=7.5[v]"
            cmd.extend(["-filter_complex", filter_complex, "-map", "[v]"])
        else:
            # For 3+ clips, use concat demuxer instead (simpler)
            list_file = output_path.with_suffix('.txt')
            with open(list_file, 'w') as f:
                for vp in video_paths:
                    f.write(f"file '{vp}'\n")
            cmd = [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(list_file), "-c", "copy", str(output_path)
            ]

        cmd.extend(["-c:v", "libx264", "-preset", "fast", str(output_path)])

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✅ Videos concatenated with crossfade: {output_path}")
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Concat failed: {e.stderr.decode()[:200]}")
            # Fallback: just use first video
            import shutil
            shutil.copy(video_paths[0], output_path)
            return output_path

    async def generate_chained_video(
        self,
        prompts: List[str],
        output_path: Path,
        duration_per_clip: int = 8
    ) -> Path:
        """Generate a longer video by chaining multiple clips.

        Uses the Last Keyframe Method:
        1. Generate first clip with text-to-video
        2. Extract last frame
        3. Generate continuation with image-to-video
        4. Repeat until all prompts used
        5. Concatenate with crossfade

        Args:
            prompts: List of prompts for each segment
            output_path: Final output path
            duration_per_clip: Duration per clip (max 8 for text, 10 for image)

        Returns:
            Path to final concatenated video
        """
        if not self.runway:
            print("⚠️  Runway not configured for chaining")
            return output_path

        clip_paths = []
        temp_dir = VIDEOS_DIR / "temp"
        temp_dir.mkdir(exist_ok=True)

        print(f"\n🔗 Chaining {len(prompts)} clips for ~{len(prompts) * duration_per_clip}s video\n")

        for i, prompt in enumerate(prompts):
            print(f"\n📹 Generating clip {i+1}/{len(prompts)}...")
            clip_path = temp_dir / f"clip_{i:02d}.mp4"

            if i == 0:
                # First clip: text-to-video
                result = await self.runway.generate_video(prompt, duration=duration_per_clip)
            else:
                # Subsequent clips: image-to-video from last frame
                last_frame = self.extract_last_frame(clip_paths[-1])
                if last_frame and last_frame.exists():
                    result = await self.runway.image_to_video(
                        str(last_frame), prompt, duration=min(duration_per_clip, 10)
                    )
                else:
                    # Fallback to text-to-video
                    result = await self.runway.generate_video(prompt, duration=duration_per_clip)

            # Download and save clip
            if result.get("status") != "error":
                video_url = result.get("output", [None])[0]
                if video_url:
                    async with httpx.AsyncClient(timeout=120.0) as client:
                        video_response = await client.get(video_url)
                        if video_response.status_code == 200:
                            clip_path.write_bytes(video_response.content)
                            clip_paths.append(clip_path)
                            print(f"   ✅ Clip {i+1} saved")
                        else:
                            print(f"   ⚠️  Failed to download clip {i+1}")
            else:
                print(f"   ⚠️  Clip {i+1} failed: {result.get('error', 'Unknown')}")

        # Concatenate all clips
        if clip_paths:
            return self.concat_videos_crossfade(clip_paths, output_path)
        else:
            print("⚠️  No clips generated")
            return output_path

    async def generate(
        self,
        post_id: str,
        style: str,
        with_voice: bool = False,
        chain_clips: int = 1,
        duration: int = 8,
    ) -> dict:
        """Generate video for a post.

        Args:
            post_id: Post ID (e.g., "EC-004")
            style: Video style (abstract, pain-point, text-overlay, before-after)
            with_voice: Whether to add Cartesia voice narration
            chain_clips: Number of clips to chain (1 = single, 2+ = chained)
            duration: Duration per clip in seconds

        Returns:
            dict with paths and metadata
        """
        total_duration = chain_clips * duration
        print(f"\n{'='*50}")
        print(f"🎬 Generating video for {post_id}")
        print(f"   Style: {style}")
        print(f"   Duration: ~{total_duration}s ({chain_clips} clip{'s' if chain_clips > 1 else ''} × {duration}s)")
        print(f"   Voice: {'Yes' if with_voice else 'No'}")
        print(f"{'='*50}\n")

        # Read post content
        post = read_post(post_id)
        print(f"📝 Post content: {post['key_phrase'][:60]}...")

        # Generate prompt
        prompt = self.generate_prompt(post, style)
        print(f"\n🎯 Runway prompt:\n{prompt}\n")

        # Output paths
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"{post_id}_{style}_{timestamp}"

        video_raw_path = VIDEOS_DIR / f"{base_name}_raw.mp4"
        audio_path = VIDEOS_DIR / "audio" / f"{base_name}.wav"

        suffix = "_voice" if with_voice else "_silent"
        final_path = VIDEOS_DIR / "final" / f"{base_name}{suffix}.mp4"

        # Generate video (single or chained)
        if chain_clips > 1:
            # Generate multiple prompts for chaining
            chain_prompts = [prompt]
            # Add continuation prompts
            for i in range(1, chain_clips):
                continuation = f"Continue smoothly: {post['key_phrase']}. Same visual style, same lighting. Slow camera movement. {duration} seconds."
                chain_prompts.append(continuation)

            await self.generate_chained_video(chain_prompts, video_raw_path, duration_per_clip=duration)
        else:
            await self.generate_video(prompt, video_raw_path)

        # Generate voice if requested
        if with_voice:
            if self.cartesia and CARTESIA_API_KEY:
                voice_script = self.get_voice_script(post, style)
                await self.generate_voice(voice_script, audio_path)
                self.merge_video_audio(video_raw_path, audio_path, final_path)
            else:
                print("⚠️  DEMO MODE: Cartesia API key not configured")
                print(f"   Would generate voice for: \"{self.get_voice_script(post, style)[:60]}...\"")
                import shutil
                shutil.copy(video_raw_path, final_path)
        else:
            # Just copy video to final location
            import shutil
            shutil.copy(video_raw_path, final_path)
            print(f"✅ Video saved: {final_path}")

        result = {
            "post_id": post_id,
            "style": style,
            "with_voice": with_voice,
            "video_path": str(final_path),
            "prompt": prompt,
            "timestamp": timestamp,
            "cost_estimate": 2.50 if style == "pain-point" else 1.75,
        }

        print(f"\n✅ Generation complete!")
        print(f"   📁 Output: {final_path}")
        print(f"   💰 Est. cost: ${result['cost_estimate']:.2f}")

        return result


# ========================================
# CLI Interface
# ========================================

def list_styles():
    """Print available video styles."""
    print("\n📹 Available Video Styles:\n")
    for key, style in VIDEO_STYLES.items():
        print(f"  {key}")
        print(f"    Name: {style['name']}")
        print(f"    Best for: {', '.join(style['best_for'])}")
        print()


async def list_voices():
    """Print available Cartesia voices."""
    if not CARTESIA_API_KEY:
        print("⚠️  CARTESIA_API_KEY not configured")
        return

    client = CartesiaClient(CARTESIA_API_KEY)
    voices = await client.list_voices()

    print(f"\n🎤 Available Voices ({len(voices)} total):\n")
    for voice in voices[:10]:  # Show first 10
        print(f"  {voice.get('name', 'Unknown')}")
        print(f"    ID: {voice.get('id', 'N/A')}")
        print(f"    Description: {voice.get('description', 'N/A')[:60]}")
        print()


async def main():
    parser = argparse.ArgumentParser(
        description="Generate LinkedIn videos with Runway + Cartesia"
    )

    parser.add_argument("--post", help="Post ID (e.g., EC-004)")
    parser.add_argument(
        "--style",
        choices=list(VIDEO_STYLES.keys()),
        help="Video style"
    )
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Add Cartesia voice narration"
    )
    parser.add_argument(
        "--no-voice",
        action="store_true",
        help="Generate without voice (text overlay only)"
    )
    parser.add_argument(
        "--list-styles",
        action="store_true",
        help="List available video styles"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List available Cartesia voices"
    )
    parser.add_argument(
        "--both",
        action="store_true",
        help="Generate both voice and no-voice versions for A/B testing"
    )
    parser.add_argument(
        "--chain",
        type=int,
        default=1,
        metavar="N",
        help="Chain N clips together for longer video (e.g., --chain 2 for ~16s)"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=8,
        choices=[4, 6, 8],
        help="Duration per clip in seconds (default: 8)"
    )

    args = parser.parse_args()

    # Handle list commands
    if args.list_styles:
        list_styles()
        return

    if args.list_voices:
        await list_voices()
        return

    # Validate required args for generation
    if not args.post:
        parser.error("--post is required for video generation")
    if not args.style:
        parser.error("--style is required for video generation")

    # Generate video(s)
    generator = LinkedInVideoGenerator()

    if args.both:
        # Generate both versions for A/B testing
        print("🧪 A/B Test Mode: Generating both voice and silent versions\n")

        # Version A: With voice
        result_voice = await generator.generate(
            args.post, args.style, with_voice=True,
            chain_clips=args.chain, duration=args.duration
        )

        # Version B: Without voice
        result_silent = await generator.generate(
            args.post, args.style, with_voice=False,
            chain_clips=args.chain, duration=args.duration
        )

        print("\n" + "="*50)
        print("🧪 A/B TEST VIDEOS READY")
        print("="*50)
        print(f"\n📹 Version A (Voice):  {result_voice['video_path']}")
        print(f"📹 Version B (Silent): {result_silent['video_path']}")
        print(f"\n💡 Tip: Post Version A on Monday, Version B on Wednesday")
        print(f"   Compare: engagement rate, comments, DMs")

    else:
        # Single version
        with_voice = args.voice and not args.no_voice
        await generator.generate(
            args.post, args.style, with_voice=with_voice,
            chain_clips=args.chain, duration=args.duration
        )


if __name__ == "__main__":
    asyncio.run(main())
