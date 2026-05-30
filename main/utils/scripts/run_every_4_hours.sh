#!/bin/bash
# run_every_4_hours.sh

#STATE_FILE="$HOME/last_run_script_date.txt"   # File that stores the last run timestamp
STATE_FILE="/Users/sanchitnath/Downloads/self_healing_locator/main/utils/last_run_script_date.txt"   # File that stores the last run timestamp
NOW=$(date +%s)                               # Current time in Unix timestamp (seconds since epoch)
echo "Script invoked. PID: $$"
echo "now = $NOW"

# Check last run
if [ -f "$STATE_FILE" ]; then                 # If the file exists
    LAST_RUN=$(cat "$STATE_FILE")             # Read the last run timestamp from the file
    echo "last run = $LAST_RUN"
    HOURS_PASSED=$(( (NOW - LAST_RUN) / 3600 ))       # Calculate difference in days [DIFF=$(( (NOW - LAST_RUN) / 86400 )) ]
    echo "diff = $HOURS_PASSED hours"
    if [ "$HOURS_PASSED" -lt 4 ]; then                # only run if less than 4 hours have passed since last run
        REMAINDER=$(( HOURS_PASSED % 4 ))
        echo "Skipping: as last run was only $REMAINDER hours ago"
        exit 0                                # Exit (skip the rest of the script)
    fi
fi

# Run your script
echo "========== Script run_every_4_hours running at $(date) =========="
/Users/sanchitnath/Downloads/update_upgrade.expect || {
    echo "Error: update_upgrade.expect failed!"
    exit 1
}

# Update last run timestamp
echo "$NOW" > "$STATE_FILE"