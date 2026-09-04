#!/bin/bash
# notify-card.sh — 发送结构化卡片通知给提需人
#
# 用法: notify-card.sh <event_type> <identifier> <title> <detail> <channel_id> <channel_type> <mention_uid> <mention_name>
#
# event_type:  in_review | done | blocked | cancelled | new_comment | new_child
# channel_type: 1=DM, 2=Group
#
# 颜色编码（提需人视角）:
#   绿色(good)      = 请验收 / 已闭环
#   红色(attention)  = 有阻塞 / 已取消
#   黄色(warning)    = 有新评论 / 拆分了子任务

set -euo pipefail

if [ "$#" -ne 8 ]; then
  echo "USAGE: notify-card.sh <event_type> <identifier> <title> <detail> <channel_id> <channel_type> <mention_uid> <mention_name>" >&2
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

# 从 openclaw 配置读取 bot token
BOT_TOKEN=$(python3 -c "
import json, os
c = json.load(open(os.path.expanduser('~/.openclaw-adm_pm/openclaw.json')))
print(c['channels']['octo']['accounts']['adm_pm_bot']['botToken'])
")

API_URL="https://im.deepminer.com.cn/api"

# 根据事件类型选择颜色、图标、动作文案
case "$EVENT_TYPE" in
  in_review)
    ICON="✅"; COLOR="good";      ACTION="请验收" ;;
  done)
    ICON="✅"; COLOR="good";      ACTION="已闭环" ;;
  blocked)
    ICON="🚫"; COLOR="attention"; ACTION="有阻塞" ;;
  cancelled)
    ICON="❌"; COLOR="attention"; ACTION="已取消" ;;
  new_comment)
    ICON="💬"; COLOR="warning";   ACTION="有新评论" ;;
  new_child)
    ICON="📋"; COLOR="warning";   ACTION="拆分了子任务" ;;
  *)
    ICON="📢"; COLOR="default";   ACTION="有更新" ;;
esac

# 用 python3 构建并发送卡片消息（避免 shell 转义地狱）
python3 "$HOME/.openclaw-adm_pm/workspace-pm/scripts/notify-card-send.py" \
  "$EVENT_TYPE" "$IDENTIFIER" "$TITLE" "$DETAIL" \
  "$CHANNEL_ID" "$CHANNEL_TYPE" \
  "$MENTION_UID" "$MENTION_NAME" \
  "$ICON" "$COLOR" "$ACTION" \
  "$API_URL" "$BOT_TOKEN"
