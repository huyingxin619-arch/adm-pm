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

    # 构建卡片正文 — 卡片不放 mention，mention 由紧随其后的纯文本消息负责
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

    # 发第二条：纯文本 mention（卡片里 @人不生效，分两条才可靠）
    text_body = json.dumps({
        "channel_id": channel_id,
        "channel_type": int(channel_type),
        "payload": {"type": 1, "content": mention_str}
    }).encode()

    text_req = urllib.request.Request(
        f"{api_url}/v1/bot/sendMessage",
        data=text_body,
        headers={
            "Authorization": f"Bearer {bot_token}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(text_req, timeout=10) as resp:
            result = json.loads(resp.read())
            print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        # mention 消息失败不影响卡片已发送的事实
        print(f'WARN: mention text failed: {e}', file=sys.stderr)

if __name__ == "__main__":
    main()
