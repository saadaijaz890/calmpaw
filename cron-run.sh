#!/usr/bin/env bash
# Auto-content generation script for cron
# Generates 3 new articles and updates sitemap
set -e

cd "$(dirname "$0")"

# Load API key from project .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

echo "=== Content Agent Cron Run ==="
echo "Date: $(date)"
echo "Working dir: $(pwd)"

# Generate 3 new articles
python3 content-agent.py --count 3 2>&1

# Update sitemap + blog index
python3 seo-tools.py 2>&1

echo "=== Done ==="