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
    params = urllib.parse.urlencode({
        "jql": jql,
        "fields": "summary,issuetype,priority,labels,customfield_10016",
        "maxResults": 100,
    })
    url = f"{JIRA_BASE}/rest/api/3/search?{params}"
    req = urllib.request.Request(url, headers={
        "Authorization": jira_auth_header(),
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())["issues"]


def pick_small(issues: list[dict]) -> dict:
    # Prefer sub-tasks and tasks over stories/epics — they are typically smaller.
    # EMM project uses "Sub-Dev" as its sub-task type.
    for type_names in [["Task", "Sub-task", "Sub-Dev", "Bug"], ["Story"]]:
        pool = [i for i in issues if i["fields"]["issuetype"]["name"] in type_names]
        if pool:
            return random.choice(pool)
    return random.choice(issues)


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
