#!/bin/bash
#
# LinkedIn Post Reminder
# Pops up a macOS notification at 8am Mon/Wed/Fri
#

# Get the day of week
DAY=$(date +%A)

# Only notify on posting days
if [[ "$DAY" == "Monday" || "$DAY" == "Wednesday" || "$DAY" == "Friday" ]]; then

    # Show macOS notification
    osascript -e 'display notification "Run: python scripts/post.py" with title "LinkedIn Post Time" subtitle "Click to open Terminal"'

    # Also show an alert dialog that requires clicking (harder to miss)
    osascript <<EOF
display dialog "Time to post on LinkedIn!

Run this command:
python scripts/post.py" buttons {"Open Terminal", "Skip"} default button "Open Terminal" with title "LinkedIn Hand-Raiser" with icon note
EOF

    BUTTON=$?

    # If "Open Terminal" was clicked (button 1 = exit code 0)
    if [ $BUTTON -eq 0 ]; then
        # Open Terminal and run the command
        osascript -e 'tell application "Terminal"
            activate
            do script "cd ~/tk_projects/linkedin-hand-raiser-system && source venv/bin/activate && python scripts/post.py"
        end tell'
    fi
fi
