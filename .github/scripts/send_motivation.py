#!/usr/bin/env python3
"""
Daily morning motivation sender.
Fetches a random small item from the EMM Jira backlog and sends it
together with a fixed motivational message to a Teams channel.

Required environment variables:
  JIRA_EMAIL        - Jira account email (e.g. you@company.com)
  JIRA_TOKEN        - Jira API token  (https://id.atlassian.com/manage-profile/security/api-tokens)
  TEAMS_WEBHOOK_URL - Teams incoming-webhook URL
"""

import base64
import json
import os
import random
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

JIRA_BASE = "https://etoro-jira.atlassian.net"
JIRA_PROJECT = "EMM"
ISRAEL_TZ = timezone(timedelta(hours=3))  # IDT (UTC+3); IST (winter) is UTC+2

MOTIVATIONAL = """\
המציאות של יהודי בעולם היא יקרה וחשובה מאוד מאוד. גם בלי שיעשה כלום לקיום שלו בעולם יש משמעות אדירה. בעצם העובדה שיהודי חי, הוא ממלא תפקיד גדול ועושה לבורא נחת רוח עצומה.

**ועכשיו בשפת הייטק:**
אני לא חייבת לאהוב את הסביבה כדי לצמוח ממנה. כל יום שאני מעמיקה את הידע שלי, בונה השפעה ומחזקת את היכולות שלי - אני מתקדמת לכיוון שאני רוצה להיות בו. המטרה שלי היא לא להיות העובדת הכי מתוסכלת בחדר. המטרה שלי היא להיות האדם שאליו פונים כשצריך להבין, להוביל ולפתור בעיות.

**ועכשיו לתכלס:**
- ב-Code Review: להילחם רק על מה שבאמת חשוב.
- להתמקד במה שבשליטתי, לא במה שמעצבן אותי.
- לנצל זמני אוויר ללמידה ולהעמקה במערכת.
- להבין עוד חלק אחד במערכת בכל יום.
- להשאיר כל דבר קצת יותר טוב ממה שמצאתי אותו.
- למדוד את היום לפי מה שלמדתי והשפעתי, לא לפי איכות הניהול.\
"""


def jira_auth_header() -> str:
    email = os.environ["JIRA_EMAIL"]
    token = os.environ["JIRA_TOKEN"]
    return "Basic " + base64.b64encode(f"{email}:{token}".encode()).decode()


def fetch_backlog() -> list[dict]:
    jql = (
        f"project = {JIRA_PROJECT} "
        "AND sprint is EMPTY "
        "AND statusCategory != Done "
        "ORDER BY created DESC"
    )
    url = f"{JIRA_BASE}/rest/api/3/search/jql"
    body = json.dumps({
        "jql": jql,
        "fields": ["summary", "issuetype", "priority", "labels", "customfield_10016", "customfield_10028"],
        "maxResults": 100,
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": jira_auth_header(),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }, method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())["issues"]


_SMALL_SIGNALS = [
    "get api", "add ", "define ", "create ", "update ", "fix ", "rename ",
    "mapping", "config", "constant", "label", "cleanup", "typo", "missing",
]
_LARGE_SIGNALS = [
    "epic", "migration", "refactor", "redesign", "architecture", "phase ",
    "implement all", "apply to all", "all controllers", "all flows", "all screens",
]


def _smallness_score(issue: dict) -> float:
    fields = issue["fields"]
    summary = fields.get("summary", "").lower()
    itype = fields.get("issuetype", {}).get("name", "")
    sp = fields.get("customfield_10016") or fields.get("customfield_10028")

    score = {"Task": 3, "Sub-task": 3, "Bug": 2, "Story": 1}.get(itype, 0)
    score -= {"Epic": 10}.get(itype, 0)

    if sp is not None:
        score += 5 if sp <= 2 else (2 if sp <= 3 else -3)

    for kw in _SMALL_SIGNALS:
        if kw in summary:
            score += 1
    for kw in _LARGE_SIGNALS:
        if kw in summary:
            score -= 2

    return score


def pick_small(issues: list[dict]) -> dict:
    scored = sorted(issues, key=_smallness_score, reverse=True)
    # Randomly pick from top 20 % or top 5, whichever is larger, to avoid
    # the same issue appearing every day.
    pool_size = max(5, len(scored) // 5)
    return random.choice(scored[:pool_size])


def build_teams_card(issue: dict) -> dict:
    key = issue["key"]
    summary = issue["fields"]["summary"]
    issue_type = issue["fields"]["issuetype"]["name"]
    priority = (issue["fields"].get("priority") or {}).get("name", "—")
    jira_url = f"{JIRA_BASE}/browse/{key}"
    today = datetime.now(ISRAEL_TZ).strftime("%A, %d %B %Y")

    return {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0078D4",
        "summary": "☀️ בוקר טוב — הנעת היום",
        "sections": [
            {
                "activityTitle": f"☀️ בוקר טוב — {today}",
                "text": MOTIVATIONAL,
            },
            {
                "activityTitle": "📌 המשימה של היום",
                "activitySubtitle": "נבחרה אקראית מה-Backlog של EMM",
                "facts": [
                    {"name": "Jira", "value": f"[{key}]({jira_url})"},
                    {"name": "כותרת", "value": summary},
                    {"name": "סוג", "value": issue_type},
                    {"name": "עדיפות", "value": priority},
                ],
                "potentialAction": [
                    {
                        "@type": "OpenUri",
                        "name": f"פתח {key} ב-Jira",
                        "targets": [{"os": "default", "uri": jira_url}],
                    }
                ],
            },
        ],
    }


def send_to_teams(card: dict) -> None:
    webhook_url = os.environ["TEAMS_WEBHOOK_URL"]
    payload = json.dumps(card, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode()
        print(f"Teams response: {resp.status} — {body}")


def main() -> None:
    print("Fetching EMM backlog …")
    issues = fetch_backlog()
    print(f"Found {len(issues)} open backlog issues")

    if not issues:
        print("No backlog issues found — skipping notification.", file=sys.stderr)
        sys.exit(1)

    issue = pick_small(issues)
    key = issue["key"]
    summary = issue["fields"]["summary"]
    print(f"Selected: [{key}] {summary}")

    card = build_teams_card(issue)
    send_to_teams(card)
    print(f"✓ Notification sent for [{key}] {summary}")


if __name__ == "__main__":
    main()
