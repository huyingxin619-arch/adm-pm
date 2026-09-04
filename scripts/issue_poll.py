#!/usr/bin/env python3
"""Loop issue 全量事件轮询：状态变更 / 新评论 / 评论编辑 / 评论删除 / 指派人变更 / 新建子任务 / updated_at变化。

输出：JSON 事件数组 | NO_CHANGES / FIRST_RUN / ERROR
状态文件：state/issue-snapshot-v2.json + state/issue-comments-state.json
"""

import hashlib
import json
import os
import subprocess
import sys
import time

STATE_DIR = sys.argv[1]
SNAPSHOT_FILE = os.path.join(STATE_DIR, "issue-snapshot-v2.json")
COMMENTS_FILE = os.path.join(STATE_DIR, "issue-comments-state.json")
HEARTBEAT_FILE = os.path.join(STATE_DIR, "poll-heartbeat.txt")


def write_heartbeat():
    try:
        with open(HEARTBEAT_FILE, "w") as f:
            f.write(str(int(time.time())))
    except Exception:
        pass


def make_event_id(ev):
    """生成事件唯一 ID：类型+issue+关键字段的 hash，用于通知去重。"""
    key_fields = [
        ev.get("type", ""),
        ev.get("identifier", ""),
        ev.get("new_status", ""),
        ev.get("old_status", ""),
        ev.get("new_assignee", ""),
        ev.get("updated_at", ""),
        ev.get("comment_preview", ""),
    ]
    raw = "|".join(key_fields)
    return hashlib.md5(raw.encode()).hexdigest()[:16]

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


def fetch_comments(issue_id):
    """拉取 issue 的全部评论，返回 [{id, body, author}] 列表或 None。"""
    out = run(["octo-daemon", "issue", "comment", "list", issue_id, "--output", "json"])
    if not out:
        return None
    try:
        comments = json.loads(out)
        if not isinstance(comments, list):
            return []
        result = []
        for c in comments:
            cid = c.get("id") or c.get("comment_id") or ""
            body = (c.get("body") or c.get("content") or "")[:150]
            author = c.get("creator_name") or c.get("creator_id") or ""
            result.append({"id": cid, "body": body, "author": author})
        return result
    except Exception:
        return None


def diff_comments(old_list, new_list):
    """比较评论列表，返回事件列表。"""
    events = []
    old_map = {c["id"]: c for c in old_list if c["id"]}
    new_map = {c["id"]: c for c in new_list if c["id"]}

    # 新评论
    for c in new_list:
        if c["id"] and c["id"] not in old_map:
            events.append({
                "type": "new_comment",
                "comment_preview": c["body"],
                "commenter": c["author"],
            })

    # 评论删除
    for cid, c in old_map.items():
        if cid not in new_map:
            events.append({
                "type": "comment_deleted",
                "comment_preview": c["body"],
                "commenter": c["author"],
            })

    # 评论编辑（同ID但body变化）
    for cid, c in new_map.items():
        if cid in old_map and old_map[cid]["body"] != c["body"]:
            events.append({
                "type": "comment_edited",
                "comment_preview": c["body"],
                "commenter": c["author"],
            })

    return events


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

        # 评论状态：{ident: [{id, body, author}]}
        comments_state = {}
        for ident, info in current.items():
            if info["status"] in ("done", "cancelled") or ident in SKIP_IDENTS:
                comments_state[ident] = None  # None = 不跟踪
                continue
            comments = fetch_comments(info["id"])
            comments_state[ident] = comments if comments is not None else []
        with open(COMMENTS_FILE, "w") as f:
            json.dump(comments_state, f, ensure_ascii=False)

        write_heartbeat()
        print("FIRST_RUN")
        return 0

    with open(SNAPSHOT_FILE) as f:
        old = json.load(f)
    with open(COMMENTS_FILE) as f:
        old_comments = json.load(f)

    events = []

    # 初始化新评论状态
    new_comments = {}

    for ident in sorted(current):
        if ident in SKIP_IDENTS:
            new_comments[ident] = None
            continue
        new = current[ident]
        prev = old.get(ident)

        # --- 新建子任务 ---
        if prev is None:
            new_comments[ident] = None
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
        prev_updated = prev.get("updated_at", "")
        if prev_updated != new["updated_at"] and prev["status"] == new["status"] and prev.get("assignee_id") == new.get("assignee_id"):
            events.append({
                "type": "updated",
                "identifier": ident,
                "title": new["title"],
                "status": new["status"],
                "updated_at": new["updated_at"],
            })

        # --- 评论变更（新增/编辑/删除）---
        if new["status"] in ("done", "cancelled"):
            new_comments[ident] = None
        else:
            current_comments = fetch_comments(new["id"])
            if current_comments is None:
                current_comments = []

            prev_comments = old_comments.get(ident)
            if prev_comments is None:
                # 之前不跟踪（比如从done切回来），建快照不触发
                new_comments[ident] = current_comments
            else:
                comment_events = diff_comments(prev_comments, current_comments)
                for ce in comment_events:
                    ev = {
                        "type": ce["type"],
                        "identifier": ident,
                        "title": new["title"],
                        "comment_preview": ce["comment_preview"],
                        "commenter": ce["commenter"],
                        "updated_at": new["updated_at"],
                    }
                    if new["parent_issue_id"]:
                        ev["parent"] = id_to_ident.get(new["parent_issue_id"], "")
                    events.append(ev)
                new_comments[ident] = current_comments

    # 保存新快照
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)
    with open(COMMENTS_FILE, "w") as f:
        json.dump(new_comments, f, ensure_ascii=False)

    write_heartbeat()

    if events:
        for ev in events:
            ev["event_id"] = make_event_id(ev)
        print(json.dumps(events, ensure_ascii=False, indent=2))
    else:
        print("NO_CHANGES")
    return 0


if __name__ == "__main__":
    sys.exit(main())
