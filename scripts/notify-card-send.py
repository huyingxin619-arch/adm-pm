#!/usr/bin/env python3
"""notify-card-send.py — 方案A：纯白底+彩色文字行，无色块分段。

结构：
- 第一行：emoji + 状态名（彩色文字）+ 副标题
- 第二行：[编号] 标题（可点击链接）
- 第三行：五步进度条（所有模板保留）
- 第四行：执行人 + 提需人
- 第五行：详情（separator 分隔，无色块）
- 底部：打开 Issue → 按钮
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

STEPS = ["待规划", "待办", "进行中", "审核中", "已完成"]

EVENT_STEP = {
    "backlog": 0, "todo": 1, "in_progress": 2,
    "in_review": 3, "done": 4,
    "blocked": 2, "cancelled": 1,
    "new_comment": -1, "new_child": -1,
}

# 主题：颜色统一——进度条节点色 = 卡片文字色
THEME = {
    "backlog":     {"icon": "📋", "label": "进入待规划", "sub": "新任务已创建，待确认要不要做",       "color": "Default"},
    "todo":        {"icon": "📝", "label": "进入待办",   "sub": "已确认要做，还没人动",              "color": "Accent"},
    "in_progress": {"icon": "🔧", "label": "开始执行",   "sub": "任务进行中，有人在干活",            "color": "Accent"},
    "in_review":   {"icon": "🔍", "label": "提交验收",   "sub": "研发已交付，等产品验收",            "color": "Warning"},  # 橙色，跟进度条统一
    "done":        {"icon": "✅", "label": "任务完成",   "sub": "验收通过，任务真正闭环",            "color": "Good"},
    "blocked":     {"icon": "🚫", "label": "任务受阻",   "sub": "任务有阻塞，等待处理",              "color": "Attention"},
    "cancelled":   {"icon": "❌", "label": "任务取消",   "sub": "任务已取消，不再跟进",              "color": "Default"},
    "new_comment": {"icon": "💬", "label": "有新评论",   "sub": "有人在 issue 下留言",               "color": "Warning"},
    "new_child":   {"icon": "🪓", "label": "拆分子任务", "sub": "已拆分子任务，可在父需求中跟进",     "color": "Warning"},
}


def step_dot(i, current, event_type):
    if event_type == "blocked" and i == current:
        return "🔴"
    if event_type == "cancelled":
        if i < current:
            return "✅"
        if i == current:
            return "❌"
        return "⚪"
    if i < current:
        return "✅"
    if i == current:
        return ["⚪", "🔵", "🔷", "🟠", "✅"][i] if 0 <= i < 5 else "🔹"
    return "⚪"


def build_progress_bar(current, event_type):
    cols = []
    for i, name in enumerate(STEPS):
        is_cur = (i == current)
        dot = step_dot(i, current, event_type)
        wt = "Bolder" if is_cur else "Default"
        cols.append({
            "type": "Column", "width": "stretch",
            "items": [
                {"type": "TextBlock", "text": dot,
                 "horizontalAlignment": "Center", "size": "Medium", "spacing": "None"},
                {"type": "TextBlock", "text": name,
                 "horizontalAlignment": "Center", "size": "Small",
                 "weight": wt, "isSubtle": not is_cur, "spacing": "None"}
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

    # 新评论/新子任务：如果传了第17个参数作为 current_step，用它
    if len(sys.argv) > 16 and sys.argv[16].isdigit():
        step_idx = int(sys.argv[16])

    body = [
        # 状态头行（纯文字着色，无色块）
        {"type": "TextBlock",
         "text": f"{t['icon']} {t['label']}",
         "weight": "Bolder", "size": "Medium",
         "color": t["color"], "spacing": "None"},
        {"type": "TextBlock",
         "text": t["sub"],
         "size": "Small", "isSubtle": True, "spacing": "None"},
        # 标题行：[编号] 标题（可点击）
        {"type": "TextBlock",
         "text": f"[{identifier}] {title}",
         "weight": "Bolder", "size": "Medium",
         "wrap": True, "spacing": "Medium",
         "color": t["color"] if t["color"] != "Default" else "Default"},
    ]

    # 进度条（所有模板都保留）
    if step_idx >= 0:
        body.append(build_progress_bar(step_idx, event_type))

    # 双列：执行人 + 提需人
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

    # 详情（无色块，用 separator 分隔）
    if detail:
        body.append({
            "type": "TextBlock",
            "text": detail,
            "wrap": True, "spacing": "Medium", "isSubtle": True,
            "separator": True
        })

    # 底部按钮
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

    plain_parts = [f"{t['icon']} {t['label']}：{identifier}", title, t["sub"]]
    if detail:
        plain_parts.append(detail)
    plain_parts.append(issue_url)
    plain = "\n".join(plain_parts)

    payload = {
        "type": 17, "profile": "octo/v1", "card_version": "1.5",
        "card": card, "plain": plain
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

    # mention
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
