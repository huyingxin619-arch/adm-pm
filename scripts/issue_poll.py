#!/usr/bin/env python3
"""Loop issue 全量事件轮询：状态变更 / 新评论 / 指派人变更 / 新建子任务。

输出：JSON 事件数组 | NO_CHANGES | FIRST_RUN | ERROR
状态文件：state/issue-snapshot-v2.json + state/issue-comments-state.json
"""

import json
import os
import subprocess
import sys

STATE_DIR = sys.argv[1]
SNAPSHOT_FILE = os.path.join(STATE_DIR, "issue-snapshot-v2.json")
COMMENTS_FILE = os.path.join(STATE_DIR, "issue-comments-state.json")

# 跳过的系统/测试 issue（不触发事件）
SKIP_IDENTS = {"ADM-3"}


def run(cmd, timeout=15):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if r.returncode == 0:
            return r.stdout
    except Exception:
        pass
    return None


def comment_count(issue_id):
    out = run(["octo-daemon", "issue", "comment", "list", issue_id, "--output", "json"])
    if not out:
        return None, None
    try:
        comments = json.loads(out)
        if not isinstance(comments, list):
            return 0, None
        latest = None
        if comments:
            c = comments[-1]
            body = (c.get("body") or c.get("content") or "")[:150]
            author = c.get("creator_name") or c.get("creator_id") or ""
            latest = {"body": body, "author": author}
        return len(comments), latest
    except Exception:
        return None, None


def main():
    out = run(["octo-daemon", "issue", "list", "--output", "json"], timeout=30)
    if not out:
        print("ERROR: octo-daemon issue list failed")
        return 1

    data = json.loads(out)
    issues = data.get("issues", [])

    current = {}
    for i in issues:
        ident = i["identifier"]
        current[ident] = {
            "id": i["id"],
            "status": i["status"],
            "assignee_id": i.get("assignee_id") or "",
            "assignee_type": i.get("assignee_type") or "",
            "updated_at": i["updated_at"],
            "title": i["title"],
            "parent_issue_id": i.get("parent_issue_id"),
        }

    id_to_ident = {v["id"]: k for k, v in current.items()}

    # ===== 首次运行：只建快照，不触发事件 =====
    if not os.path.exists(SNAPSHOT_FILE):
        with open(SNAPSHOT_FILE, "w") as f:
            json.dump(current, f, ensure_ascii=False, indent=2)

        counts = {}
        for ident, info in current.items():
            if info["status"] in ("done", "cancelled") or ident in SKIP_IDENTS:
                counts[ident] = -1  # -1 = 不跟踪
                continue
            n, _ = comment_count(info["id"])
            counts[ident] = n if n is not None else 0
        with open(COMMENTS_FILE, "w") as f:
            json.dump(counts, f)

        print("FIRST_RUN")
        return 0

    with open(SNAPSHOT_FILE) as f:
        old = json.load(f)
    with open(COMMENTS_FILE) as f:
        old_counts = json.load(f)

    events = []

    for ident in sorted(current):
        if ident in SKIP_IDENTS:
            continue
        new = current[ident]
        prev = old.get(ident)

        # --- 新建子任务 ---
        if prev is None:
            if new["parent_issue_id"]:
                parent_ident = id_to_ident.get(new["parent_issue_id"], "")
                events.append({
                    "type": "new_child",
                    "identifier": ident,
                    "title": new["title"],
                    "parent": parent_ident,
                    "status": new["status"],
                    "updated_at": new["updated_at"],
                })
            continue

        # --- 状态变更 ---
        if prev["status"] != new["status"]:
            ev = {
                "type": "status_change",
                "identifier": ident,
                "title": new["title"],
                "old_status": prev["status"],
                "new_status": new["status"],
                "updated_at": new["updated_at"],
            }
            if new["parent_issue_id"]:
                ev["parent"] = id_to_ident.get(new["parent_issue_id"], "")
            events.append(ev)

        # --- 指派人变更 ---
        if prev.get("assignee_id") != new.get("assignee_id"):
            events.append({
                "type": "assignee_change",
                "identifier": ident,
                "title": new["title"],
                "old_assignee": prev.get("assignee_id", ""),
                "new_assignee": new.get("assignee_id", ""),
                "updated_at": new["updated_at"],
            })

        # --- updated_at 变化但状态/指派人都没变（来回变化被快照抵消）---
        # 说明中间有动作，需要通知提需人关注
        prev_updated = prev.get("updated_at", "")
        if prev_updated != new["updated_at"] and prev["status"] == new["status"] and prev.get("assignee_id") == new.get("assignee_id"):
            events.append({
                "type": "updated",
                "identifier": ident,
                "title": new["title"],
                "status": new["status"],
                "updated_at": new["updated_at"],
            })

        # --- 新评论 ---
        if new["status"] in ("done", "cancelled"):
            old_counts[ident] = -1
        else:
            prev_count = old_counts.get(ident, 0)
            if prev_count >= 0:
                n, latest = comment_count(new["id"])
                if n is not None:
                    if n > prev_count and latest:
                        ev = {
                            "type": "new_comment",
                            "identifier": ident,
                            "title": new["title"],
                            "comment_preview": latest["body"],
                            "commenter": latest["author"],
                            "updated_at": new["updated_at"],
                        }
                        if new["parent_issue_id"]:
                            ev["parent"] = id_to_ident.get(new["parent_issue_id"], "")
                        events.append(ev)
                    old_counts[ident] = n

    # 保存新快照
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)
    with open(COMMENTS_FILE, "w") as f:
        json.dump(old_counts, f)

    if events:
        print(json.dumps(events, ensure_ascii=False, indent=2))
    else:
        print("NO_CHANGES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
