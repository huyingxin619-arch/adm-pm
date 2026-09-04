#!/usr/bin/env python3
"""notify-card-send.py — 构建 AdaptiveCard type-17 payload 并通过 Octo API 发送。

由 notify-card.sh 调用，不直接使用。
"""

import json
import sys
import urllib.request

def main():
    (event_type, identifier, title, detail,
     channel_id, channel_type,
     mention_uid, mention_name,
     icon, color, action,
     api_url, bot_token) = sys.argv[1:15]

    # 构建卡片正文
    mention_str = f"@[{mention_uid}:{mention_name}]"

    # 标题行：图标 + 动作 + issue编号
    header_text = f"{icon} {action}：{identifier}"

    # 正文：需求标题 + 详情 + mention
    body_lines = [
        {"type": "TextBlock", "text": header_text, "size": "Medium", "weight": "Bolder",
         "color": color if color != "default" else "Default", "wrap": True},
        {"type": "TextBlock", "text": title, "wrap": True, "spacing": "Small"},
    ]

    if detail:
        body_lines.append(
            {"type": "TextBlock", "text": detail, "wrap": True, "spacing": "Small",
             "isSubtle": True}
        )

    # mention 行
    body_lines.append(
        {"type": "TextBlock", "text": mention_str, "wrap": True, "spacing": "Medium",
         "weight": "Bolder"}
    )

    card = {
        "type": "AdaptiveCard",
        "version": "1.5",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "body": body_lines
    }

    # plain fallback
    plain_parts = [f"{icon} {action}：{identifier}", title]
    if detail:
        plain_parts.append(detail)
    plain_parts.append(mention_str)
    plain = "\n".join(plain_parts)

    payload = {
        "type": 17,
        "profile": "octo/v1",
        "card_version": "1.5",
        "card": card,
        "plain": plain
    }

    body = json.dumps({
        "channel_id": channel_id,
        "channel_type": int(channel_type),
        "payload": payload
    }).encode()

    req = urllib.request.Request(
        f"{api_url}/v1/bot/sendMessage",
        data=body,
        headers={
            "Authorization": f"Bearer {bot_token}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
