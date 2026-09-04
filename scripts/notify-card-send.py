#!/usr/bin/env python3
"""notify-card-send.py — 构建 AdaptiveCard type-17 payload 并通过 Octo API 发送。

由 notify-card.sh 调用，不直接使用。
"""

import json
import os
import subprocess
import sys
import urllib.request

# Loop web UI 的 issue 详情链接前缀（Dispatcher 确认格式）
LOOP_URL_PREFIX = os.environ.get(
    "LOOP_ISSUE_URL_PREFIX",
    "https://im.deepminer.com.cn/fleet/adm-81pn/issues/"
)


def main():
    (event_type, identifier, title, detail,
     channel_id, channel_type,
     mention_uid, mention_name,
     icon, color, action,
     api_url, bot_token, assignee) = sys.argv[1:16]

    mention_str = f"@[{mention_uid}:{mention_name}]"
    issue_url = f"{LOOP_URL_PREFIX}{identifier}"

    STATUS_MAP = {
        "in_review": "🔍 待验收",
        "done": "✅ 已闭环",
        "blocked": "🚫 已阻塞",
        "cancelled": "❌ 已取消",
        "new_comment": "💬 新评论",
        "new_child": "🪓 新子任务",
    }
    current_status = STATUS_MAP.get(event_type, event_type)

    # 首行大字：图标 + 动作 + 标题（标题为 markdown 链接，点击直达 issue）
    header_text = f"{icon} {action}：[{title}]({issue_url})"

    body = [
        {
            "type": "TextBlock", "text": header_text, "size": "Medium",
            "weight": "Bolder", "color": color if color != "default" else "Default",
            "wrap": True, "spacing": "None"
        },
        {
            "type": "FactSet",
            "facts": [
                {"title": "编号", "value": identifier},
                {"title": "状态", "value": current_status},
                {"title": "指派", "value": assignee},
            ],
            "spacing": "Small",
            "separator": True
        }
    ]

    if detail:
        body.append({
            "type": "TextBlock", "text": detail,
            "wrap": True, "spacing": "Small", "isSubtle": True
        })

    ACTION_GUIDE = {
        "in_review": "👉 请到测试环境验证，确认无误后请验收",
        "done": "🎉 需求已闭环，感谢配合",
        "blocked": "⚠️ 处理中遇到阻塞，请留意后续更新或补充信息",
        "cancelled": "❌ 该需求已被取消，原因见详情",
        "new_comment": "💬 有新评论，点标题查看",
        "new_child": "🪓 已拆分子任务，在父需求中跟进",
    }
    action_hint = ACTION_GUIDE.get(event_type, "")
    if action_hint:
        body.append({
            "type": "TextBlock", "text": action_hint,
            "wrap": True, "spacing": "Medium", "weight": "Bolder",
            "color": color if color != "default" else "Default"
        })

    card = {
        "type": "AdaptiveCard",
        "version": "1.5",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "body": body
    }

    plain_parts = [f"{icon} {action}：{identifier}", title]
    if detail:
        plain_parts.append(f"详情：{detail}")
    if action_hint:
        plain_parts.append(action_hint)
    plain_parts.append(issue_url)
    plain = "\n".join(plain_parts)

    payload = {
        "type": 17,
        "profile": "octo/v1",
        "card_version": "1.5",
        "card": card,
        "plain": plain
    }

    card_body = json.dumps({
        "channel_id": channel_id,
        "channel_type": int(channel_type),
        "payload": payload
    }).encode()

    req = urllib.request.Request(
        f"{api_url}/v1/bot/sendMessage",
        data=card_body,
        headers={
            "Authorization": f"Bearer {bot_token}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            print(f"CARD_SENT: {result.get('message_id', 'unknown')}", file=sys.stderr)
    except Exception as e:
        print(f'ERROR: card send failed: {e}', file=sys.stderr)
        sys.exit(1)

    # 第二条：mention 通知，走 openclaw CLI
    target = channel_id if int(channel_type) == 1 else f"group:{channel_id}"
    # mention 消息带上关键信息，而非只 @人
    mention_msg = f"{mention_str} 【{identifier}】{action}：{title}"
    cli_cmd = [
        "openclaw", "message", "send",
        "--channel", "octo",
        "--account", "adm_pm_bot",
        "--target", target,
        "--message", mention_msg
    ]
    env = os.environ.copy()
    env["PATH"] = "/Users/adm/.nvm/versions/node/v24.19.0/bin:" + env.get("PATH", "/opt/homebrew/bin:/usr/bin:/bin")
    try:
        r = subprocess.run(cli_cmd, capture_output=True, text=True, timeout=60, env=env)
        out = (r.stdout or "").strip()
        err = (r.stderr or "").strip()
        if r.returncode != 0:
            print(f"WARN: mention CLI rc={r.returncode} stdout={out} stderr={err}", file=sys.stderr)
        else:
            # 输出关键确认信息
            print(f"MENTION_SENT: {out}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("WARN: mention CLI timeout after 60s", file=sys.stderr)
    except Exception as e:
        print(f"WARN: mention CLI exception: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
