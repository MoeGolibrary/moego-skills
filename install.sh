#!/usr/bin/env bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Config
REPO_URL="https://github.com/MoeGolibrary/moego-skills.git"
INSTALL_DIR="$HOME/.claude/plugins/moego-skills"
BIN_DIR="$HOME/.local/bin"

echo -e "${GREEN}🚀 Installing MoeGo Skills...${NC}"

# Check git
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: git is not installed${NC}"
    exit 1
fi

# Create directories
mkdir -p "$BIN_DIR"
mkdir -p "$(dirname "$INSTALL_DIR")"

# Clone or update
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}Updating existing installation...${NC}"
    cd "$INSTALL_DIR"
    git pull --ff-only
else
    echo -e "${YELLOW}Cloning repository...${NC}"
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# Install CLI command
if [ -f "$INSTALL_DIR/bin/moego-skills" ]; then
    chmod +x "$INSTALL_DIR/bin/moego-skills"
    ln -sf "$INSTALL_DIR/bin/moego-skills" "$BIN_DIR/moego-skills"
fi

# Check PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}⚠️  Add this to your shell profile (.bashrc/.zshrc):${NC}"
    echo -e "   export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# Setup Claude Code adapter
CLAUDE_SKILLS_DIR="$HOME/.claude/skills"
mkdir -p "$CLAUDE_SKILLS_DIR"

# Create symlinks for skills
for skill_dir in "$INSTALL_DIR/skills/"*/; do
    skill_name=$(basename "$skill_dir")
    if [ -f "$skill_dir/skill.md" ]; then
        ln -sf "$skill_dir/skill.md" "$CLAUDE_SKILLS_DIR/$skill_name.md"
    fi
done

echo -e "${GREEN}✅ MoeGo Skills installed successfully!${NC}"
echo ""
echo "Available commands:"
echo "  moego-skills update  - Update all skills"
echo "  moego-skills list    - List installed skills"
echo "  moego-skills help    - Show help"
echo ""
echo "Installed skills:"
ls -1 "$INSTALL_DIR/skills/" 2>/dev/null | while read skill; do
    echo "  - $skill"
done
