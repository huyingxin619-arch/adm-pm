#!/bin/bash
# issue-poll.sh — 全量事件轮询：状态变更+新评论+指派人变更+新建子任务
# 输出：JSON 事件数组 | NO_CHANGES | FIRST_RUN | ERROR

set -euo pipefail

WORKSPACE_DIR="$HOME/.openclaw-adm_pm/workspace-pm"
STATE_DIR="$WORKSPACE_DIR/state"
mkdir -p "$STATE_DIR"

# Use nvm octo-cli (v0.19.0) instead of old homebrew octo-daemon (v1.1.0)
export PATH="/Users/adm/.nvm/versions/node/v24.19.0/bin:$PATH"
export OCTO_BOT_ID="27xvrdnfc6ld216a898_bot"
export OCTO_WORKSPACE_ID="1b1dd00c-1be9-4ceb-bddc-53280567820d"

exec python3 "$WORKSPACE_DIR/scripts/issue_poll.py" "$STATE_DIR"
