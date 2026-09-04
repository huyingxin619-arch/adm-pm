#!/bin/bash
# notify-card.sh — 发送升级版卡片通知给提需人
#
# 用法: notify-card.sh <event_type> <identifier> <title> <detail> <channel_id> <channel_type> <mention_uid> <mention_name> [assignee_name]
#
# event_type: backlog | todo | in_progress | in_review | done | blocked | cancelled | new_comment | new_child
# channel_type: 1=DM, 2=Group
#
# 配色（AdaptiveCard Container style）:
#   good(绿)       = 审核中/已完成
#   attention(红)  = 受阻
#   warning(黄)    = 新评论/新子任务
#   emphasis(灰蓝) = 待规划/待办/进行中/已取消

set -euo pipefail

if [ "$#" -lt 8 ]; then
  echo "USAGE: notify-card.sh <event_type> <identifier> <title> <detail> <channel_id> <channel_type> <mention_uid> <mention_name> [assignee_name]" >&2
  exit 1
fi

EVENT_TYPE="$1"
IDENTIFIER="$2"
TITLE="$3"
DETAIL="$4"
CHANNEL_ID="$5"
CHANNEL_TYPE="$6"
MENTION_UID="$7"
MENTION_NAME="$8"
ASSIGNEE="${9:-未指派}"

# 从 openclaw 配置读取 bot token
BOT_TOKEN=$(python3 -c "
import json, os
c = json.load(open(os.path.expanduser('~/.openclaw-adm_pm/openclaw.json')))
print(c['channels']['octo']['accounts']['adm_pm_bot']['botToken'])
")

API_URL="https://im.deepminer.com.cn/api"

# 事件类型 → 图标/颜色/动作文案（传给 python 脚本，python 里有完整 THEME 配置）
case "$EVENT_TYPE" in
  backlog)       ICON="📋"; COLOR="default";   ACTION="进入待规划" ;;
  todo)          ICON="📝"; COLOR="accent";    ACTION="进入待办" ;;
  in_progress)   ICON="🔧"; COLOR="accent";    ACTION="开始执行" ;;
  in_review)     ICON="🔍"; COLOR="good";      ACTION="提交验收" ;;
  done)          ICON="✅"; COLOR="good";      ACTION="任务完成" ;;
  blocked)       ICON="🚫"; COLOR="attention"; ACTION="任务受阻" ;;
  cancelled)     ICON="❌"; COLOR="attention"; ACTION="任务取消" ;;
  new_comment)   ICON="💬"; COLOR="warning";   ACTION="有新评论" ;;
  new_child)     ICON="🪓"; COLOR="warning";   ACTION="拆分子任务" ;;
  *)             ICON="📢"; COLOR="default";   ACTION="有更新" ;;
esac

python3 "$HOME/.openclaw-adm_pm/workspace-pm/scripts/notify-card-send.py" \
  "$EVENT_TYPE" "$IDENTIFIER" "$TITLE" "$DETAIL" \
  "$CHANNEL_ID" "$CHANNEL_TYPE" \
  "$MENTION_UID" "$MENTION_NAME" \
  "$ICON" "$COLOR" "$ACTION" \
  "$API_URL" "$BOT_TOKEN" "$ASSIGNEE"
