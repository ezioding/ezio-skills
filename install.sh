#!/usr/bin/env sh
# Skill installation script for ezio-skills repository
# Usage: ./install.sh <skill-name>

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_NAME="$1"

# Skill registry mapping
SKILL_DIR="skills/$SKILL_NAME"

# Validate skill name
if [ -z "$SKILL_NAME" ]; then
    echo "❌ Error: Skill name is required"
    echo "Usage: $0 <skill-name>"
    exit 1
fi

# Check if skill exists
if [ ! -d "$SKILL_DIR" ]; then
    echo "❌ Error: Skill '$SKILL_NAME' not found"
    echo "Available skills:"
    ls -1 skills/
    exit 1
fi

# Determine Claude skills directory
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"

# Create directory if needed
mkdir -p "$CLAUDE_SKILLS_DIR"

# Copy skill directory
echo "📦 Installing $SKILL_NAME..."
cp -r "$SKILL_DIR" "$CLAUDE_SKILLS_DIR/"

echo "✅ Installed! You can now use: $SKILL_NAME"
