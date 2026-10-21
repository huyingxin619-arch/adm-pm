#!/bin/bash
# issue-poll.sh — 全量事件轮询：状态变更+新评论+指派人变更+新建子任务
# 输出：JSON 事件数组 | NO_CHANGES | FIRST_RUN | ERROR

set -euo pipefail

WORKSPACE_DIR="$HOME/.openclaw-adm_pm/workspace-pm"
STATE_DIR="$WORKSPACE_DIR/state"
mkdir -p "$STATE_DIR"

# Use bot token + adm workspace for Loop API access
export OCTO_TOKEN="bf_be3721af90eecfe33b649bb478b84ff1"
export OCTO_WORKSPACE_ID="1b1dd00c-1be9-4ceb-bddc-53280567820d"

exec python3 "$WORKSPACE_DIR/scripts/issue_poll.py" "$STATE_DIR"
