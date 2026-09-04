#!/usr/bin/env python3
"""notify-card-send.py — 升级版 AdaptiveCard 通知卡片。

参考 Multica 状态助手设计，适配 Loop 7 种状态 + 新评论/新子任务：
- 彩色状态头横幅（Container style 分区）
- 五步进度条（待规划→待办→进行中→审核中→已完成）
- 执行人 + 提需人双列
- 详情色块
- 底部「打开 Issue →」按钮
"""

import json
import os
import subprocess
import sys
import urllib.request

LOOP_URL_PREFIX = os.environ.get(
    "LOOP_ISSUE_URL_PREFIX",
    "https://im.deepminer.com.cn/fleet/adm-81pn/issues/"
)

# 五步进度条
STEPS = ["待规划", "待办", "进行中", "审核中", "已完成"]

# 事件类型 → 进度条当前步骤索引（-1 = 不显示进度条）
EVENT_STEP = {
    "backlog": 0, "todo": 1, "in_progress": 2,
    "in_review": 3, "done": 4,
    "blocked": 2,       # 受阻时卡在进行中
    "cancelled": -1,    # 取消不显示进度条
    "new_comment": -1,  # 评论不显示进度条（issue 真实状态未知）
    "new_child": -1,
}

# 事件 → 主题配置
# style: Container style | color: TextBlock color | icon: emoji
THEME = {
    "backlog":     {"icon": "📋", "label": "进入待规划", "sub": "新任务已创建，待确认要不要做",       "style": "emphasis",  "color": "Default"},
    "todo":        {"icon": "📝", "label": "进入待办",   "sub": "已确认要做，还没人动",              "style": "emphasis",  "color": "Accent"},
    "in_progress": {"icon": "🔧", "label": "开始执行",   "sub": "任务进行中，有人在干活",            "style": "emphasis",  "color": "Accent"},
    "in_review":   {"icon": "🔍", "label": "提交验收",   "sub": "研发已交付，等产品验收",            "style": "good",      "color": "Good"},
    "done":        {"icon": "✅", "label": "任务完成",   "sub": "验收通过，任务真正闭环",            "style": "good",      "color": "Good"},
    "blocked":     {"icon": "🚫", "label": "任务受阻",   "sub": "任务有阻塞，等待处理",              "style": "attention", "color": "Attention"},
    "cancelled":   {"icon": "❌", "label": "任务取消",   "sub": "任务已取消，不再跟进",              "style": "emphasis",  "color": "Default"},
    "new_comment": {"icon": "💬", "label": "有新评论",   "sub": "有人在 issue 下留言",               "style": "warning",   "color": "Warning"},
    "new_child":   {"icon": "🪓", "label": "拆分子任务", "sub": "已拆分子任务，可在父需求中跟进",     "style": "warning",   "color": "Warning"},
}

# 进度条节点 emoji
def step_dot(i, current, event_type):
    if event_type == "blocked" and i == current:
        return "🔴"
    if event_type == "cancelled":
        return "❌" if i == 0 else "⚪"
    if i < current:
        return "✅"
    if i == current:
        return ["⚪", "🔵", "🔷", "🟠", "✅"][i] if 0 <= i < 5 else "🔹"
    return "⚪"


def build_progress_bar(current, event_type):
    """五步进度条：ColumnSet + emoji 圆点 + 连线"""
    cols = []
    for i, name in enumerate(STEPS):
        is_cur = (i == current)
        dot = step_dot(i, current, event_type)
        wt = "Bolder" if is_cur else "Default"
        subtle = not is_cur

        cols.append({
            "type": "Column", "width": "stretch",
            "items": [
                {"type": "TextBlock", "text": dot,
                 "horizontalAlignment": "Center", "size": "Medium", "spacing": "None"},
                {"type": "TextBlock", "text": name,
                 "horizontalAlignment": "Center", "size": "Small",
                 "weight": wt, "isSubtle": subtle, "spacing": "None"}
            ]
        })
        if i < len(STEPS) - 1:
            cols.append({
                "type": "Column", "width": "auto",
                "items": [{"type": "TextBlock", "text": "—",
                           "color": "Good" if i < current else "Default",
                           "isSubtle": i >= current,
                           "spacing": "None", "horizontalAlignment": "Center"}]
            })
    return {"type": "ColumnSet", "columns": cols, "spacing": "Small"}


def main():
    (event_type, identifier, title, detail,
     channel_id, channel_type,
     mention_uid, mention_name,
     _icon, _color, _action,
     api_url, bot_token, assignee) = sys.argv[1:16]

    mention_str = f"@[{mention_uid}:{mention_name}]"
    issue_url = f"{LOOP_URL_PREFIX}{identifier}"

    t = THEME.get(event_type, THEME["done"])
    step_idx = EVENT_STEP.get(event_type, -1)

    # ── 头横幅 ──
    banner = {
        "type": "Container",
        "style": t["style"],
        "items": [{
            "type": "ColumnSet",
            "columns": [
                {"type": "Column", "width": "stretch", "items": [
                    {"type": "TextBlock",
                     "text": f"{t['icon']} {t['label']}",
                     "weight": "Bolder", "size": "Medium",
                     "color": t["color"], "spacing": "None"},
                    {"type": "TextBlock",
                     "text": t["sub"],
                     "size": "Small", "isSubtle": True, "spacing": "None"}
                ]},
                {"type": "Column", "width": "auto", "verticalAlign": "center", "items": [
                    {"type": "TextBlock",
                     "text": identifier,
                     "size": "Small", "weight": "Bolder", "isSubtle": True}
                ]}
            ]
        }]
    }

    # ── 标题（可点击） ──
    title_block = {
        "type": "TextBlock",
        "text": f"[{title}]({issue_url})",
        "weight": "Bolder", "size": "Medium",
        "wrap": True, "spacing": "Medium"
    }

    body = [banner, title_block]

    # ── 进度条 ──
    if step_idx >= 0:
        body.append(build_progress_bar(step_idx, event_type))

    # ── 双列：执行人 + 提需人 ──
    body.append({
        "type": "ColumnSet",
        "spacing": "Small",
        "columns": [
            {"type": "Column", "width": "stretch", "items": [
                {"type": "FactSet", "facts": [
                    {"title": "执行人", "value": assignee or "未指派"}
                ], "spacing": "None"}
            ]},
            {"type": "Column", "width": "stretch", "items": [
                {"type": "FactSet", "facts": [
                    {"title": "提需人", "value": mention_name or "—"}
                ], "spacing": "None"}
            ]}
        ]
    })

    # ── 详情色块 ──
    if detail:
        body.append({
            "type": "Container",
            "style": t["style"] if t["style"] != "default" else "default",
            "spacing": "Small",
            "separator": True,
            "items": [
                {"type": "TextBlock", "text": detail,
                 "wrap": True, "spacing": "None", "isSubtle": True,
                 "color": t["color"] if t["color"] != "Default" else "Default"}
            ]
        })

    # ── 底部按钮 ──
    actions = [{
        "type": "Action.OpenUrl",
        "title": "打开 Issue →",
        "url": issue_url
    }]

    card = {
        "type": "AdaptiveCard",
        "version": "1.5",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "body": body,
        "actions": actions
    }

    # plain fallback
    plain_parts = [f"{t['icon']} {t['label']}：{identifier}", title, t["sub"]]
    if detail:
        plain_parts.append(detail)
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
        headers={"Authorization": f"Bearer {bot_token}", "Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
            print(f"CARD_SENT: {result.get('message_id', 'unknown')}", file=sys.stderr)
    except Exception as e:
        print(f'ERROR: card send failed: {e}', file=sys.stderr)
        sys.exit(1)

    # mention（纯文本 @人，走 openclaw CLI）
    target = channel_id if int(channel_type) == 1 else f"group:{channel_id}"
    mention_msg = f"{mention_str} 【{identifier}】{t['label']}：{title}"
    cli_cmd = [
        "openclaw", "message", "send", "--channel", "octo",
        "--account", "adm_pm_bot", "--target", target, "--message", mention_msg
    ]
    env = os.environ.copy()
    env["PATH"] = "/Users/adm/.nvm/versions/node/v24.19.0/bin:" + env.get("PATH", "")
    try:
        r = subprocess.run(cli_cmd, capture_output=True, text=True, timeout=60, env=env)
        if r.returncode == 0:
            print(f"MENTION_SENT: {(r.stdout or '').strip()}", file=sys.stderr)
        else:
            print(f"WARN: mention rc={r.returncode}", file=sys.stderr)
    except Exception as e:
        print(f"WARN: mention: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
