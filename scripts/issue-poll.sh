#!/bin/bash
# issue-poll.sh — 全量事件轮询：状态变更+新评论+指派人变更+新建子任务
# 输出：JSON 事件数组 | NO_CHANGES | FIRST_RUN | ERROR

set -euo pipefail

WORKSPACE_DIR="$HOME/.openclaw-adm_pm/workspace-pm"
STATE_DIR="$WORKSPACE_DIR/state"
mkdir -p "$STATE_DIR"

exec python3 "$WORKSPACE_DIR/scripts/issue_poll.py" "$STATE_DIR"
