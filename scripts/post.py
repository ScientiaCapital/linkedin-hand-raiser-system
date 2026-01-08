#!/usr/bin/env python3
"""
LinkedIn Post Scheduler CLI
Copies today's scheduled post to clipboard and opens LinkedIn.

Usage:
    python scripts/post.py              # Auto-detect day, use today's post
    python scripts/post.py monday       # Force specific day
    python scripts/post.py EC-001       # Use specific post ID
    python scripts/post.py --list       # Show all scheduled posts
"""

import json
import os
import re
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

try:
    import pyperclip
except ImportError:
    print("❌ pyperclip not installed. Run: pip install pyperclip")
    sys.exit(1)


# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
POSTS_DIR = PROJECT_ROOT / "posts"
SCHEDULE_FILE = POSTS_DIR / "schedule.json"
LINKEDIN_URL = "https://www.linkedin.com/feed/"


def load_schedule():
    """Load the posting schedule from JSON."""
    if not SCHEDULE_FILE.exists():
        print(f"❌ Schedule file not found: {SCHEDULE_FILE}")
        sys.exit(1)

    with open(SCHEDULE_FILE, "r") as f:
        return json.load(f)


def get_current_week():
    """Get current week number (1-4, cycling)."""
    week_num = datetime.now().isocalendar()[1] % 4
    return f"week{week_num if week_num > 0 else 4}"


def get_today():
    """Get today's day name (lowercase)."""
    return datetime.now().strftime("%A").lower()


def extract_post_content(filepath):
    """Extract the post copy from a markdown file.

    Looks for content between ``` markers after '## Post Copy'.
    """
    if not filepath.exists():
        print(f"❌ Post file not found: {filepath}")
        sys.exit(1)

    content = filepath.read_text()

    # Find content between ``` markers in the Post Copy section
    pattern = r"## Post Copy\s*```\s*(.*?)\s*```"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(1).strip()

    # Fallback: look for any ``` block
    pattern = r"```\s*(.*?)\s*```"
    match = re.search(pattern, content, re.DOTALL)

    if match:
        return match.group(1).strip()

    print(f"❌ Could not extract post content from: {filepath}")
    sys.exit(1)


def extract_post_title(filepath):
    """Extract post title/ID from the markdown file."""
    content = filepath.read_text()

    # Look for first heading
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    return filepath.stem


def find_post_by_id(post_id, schedule):
    """Find a post file by its ID (e.g., EC-001)."""
    post_id_upper = post_id.upper()

    for week, days in schedule.items():
        for day, filepath in days.items():
            if post_id_upper in filepath.upper():
                return POSTS_DIR / filepath

    # Try direct file search
    for md_file in POSTS_DIR.rglob("*.md"):
        if post_id_upper in md_file.stem.upper():
            return md_file

    return None


def list_scheduled_posts(schedule):
    """Print all scheduled posts."""
    print("\n📅 Scheduled Posts:\n")

    for week, days in schedule.items():
        print(f"  {week.upper()}:")
        for day, filepath in days.items():
            full_path = POSTS_DIR / filepath
            if full_path.exists():
                title = extract_post_title(full_path)
                print(f"    {day.capitalize():12} → {title}")
            else:
                print(f"    {day.capitalize():12} → {filepath} (NOT FOUND)")
        print()


def main():
    schedule = load_schedule()

    # Handle --list flag
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_scheduled_posts(schedule)
        return

    # Determine which post to use
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        # Check if it's a day name
        if arg in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
            day = arg
            week = get_current_week()
        else:
            # Assume it's a post ID
            post_file = find_post_by_id(sys.argv[1], schedule)
            if not post_file:
                print(f"❌ Post not found: {sys.argv[1]}")
                print("   Try: python scripts/post.py --list")
                sys.exit(1)

            post_content = extract_post_content(post_file)
            post_title = extract_post_title(post_file)

            print(f"\n📝 Loading post: {post_title}")
            pyperclip.copy(post_content)
            print("📋 Copied to clipboard!")
            print("🌐 Opening LinkedIn...")
            webbrowser.open(LINKEDIN_URL)
            print("\n✅ Ready! Click 'Start a post' and paste (Cmd+V)\n")
            return
    else:
        day = get_today()
        week = get_current_week()

    print(f"\n📅 Today is {day.capitalize()}")

    # Get the scheduled post for today
    week_schedule = schedule.get(week, schedule.get("default", {}))

    if day not in week_schedule:
        print(f"⏸️  No post scheduled for {day.capitalize()}")
        print("   Posting days: Monday, Wednesday, Friday")
        print("   Or run: python scripts/post.py EC-001")
        return

    post_path = POSTS_DIR / week_schedule[day]
    post_content = extract_post_content(post_path)
    post_title = extract_post_title(post_path)

    print(f"📝 Loading post: {post_title}")

    # Copy to clipboard
    pyperclip.copy(post_content)
    print("📋 Copied to clipboard!")

    # Open LinkedIn
    print("🌐 Opening LinkedIn...")
    webbrowser.open(LINKEDIN_URL)

    print("\n✅ Ready! Click 'Start a post' and paste (Cmd+V)\n")


if __name__ == "__main__":
    main()
