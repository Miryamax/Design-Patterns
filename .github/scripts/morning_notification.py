#!/usr/bin/env python3
"""
Daily morning notification script.
Fetches a random small EMM Jira backlog item and posts to a Teams channel.

Required environment variables:
  JIRA_EMAIL        - Atlassian account email
  JIRA_API_TOKEN    - Jira API token (generate at https://id.atlassian.com/manage-profile/security/api-tokens)
  TEAMS_WEBHOOK_URL - Incoming webhook URL for your Teams channel
"""

import requests
import random
import os
import sys
from datetime import date
from base64 import b64encode

JIRA_BASE = "https://etoro-jira.atlassian.net"

MOTIVATION = """המציאות של יהודי בעולם היא יקרה וחשובה מאוד מאוד. גם בלי שיעשה כלום לקיומו בעולם יש משמעות אדירה. בעצם העובדה שיהודי חי, הוא ממלא תפקיד גדול ועושה לבורא נחת רוח עצומה.

ועכשיו בשפת הייטק:
אני לא חייבת לאהוב את הסביבה כדי לצמוח ממנה. כל יום שאני מעמיקה את הידע שלי, בונה השפעה ומחזקת את היכולות שלי - אני מתקדמת לכיוון שאני רוצה להיות בו. המטרה שלי היא לא להיות העובדת הכי מתוסכלת בחדר. המטרה שלי היא להיות האדם שאליו פונים כשצריך להבין, להוביל ולפתור בעיות.

ועכשיו לתכלס:
• ב-Code Review: להילחם רק על מה שבאמת חשוב.
• להתמקד במה שבשליטי, לא במה שמעצבן אותי.
• לנצל זמני אוויר ללמידה ולהעמקה במערכת.
• להבין עוד חלק אחד במערכת בכל יום.
• להשאיר כל דבר קצת יותר טוב ממה שמצאתי אותו.
• למדוד את היום לפי מה שלמדתי והשפעתי, לא לפי איכות הניהול."""


def fetch_backlog(email: str, token: str) -> list:
    auth = b64encode(f"{email}:{token}".encode()).decode()
    jql = (
        "project = EMM "
        "AND sprint not in openSprints() "
        "AND sprint not in closedSprints() "
        "AND statusCategory != Done "
        "ORDER BY created DESC"
    )
    r = requests.get(
        f"{JIRA_BASE}/rest/api/3/search",
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/json"},
        params={"jql": jql, "maxResults": 50,
                "fields": "summary,priority,labels,issuetype,customfield_10016"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json().get("issues", [])


def pick_small_issue(issues: list) -> dict | None:
    light_kw = ["fix", "add", "update", "cleanup", "refactor", "rename",
                "test", "doc", "label", "log", "typo", "minor", "ops:"]
    heavy_kw = ["spike", "epic", "migration", "architecture"]
    light = [
        i for i in issues
        if any(k in i["fields"]["summary"].lower() for k in light_kw)
        and not any(k in i["fields"]["summary"].lower() for k in heavy_kw)
    ]
    pool = light if light else issues
    return random.choice(pool) if pool else None


def build_teams_card(task: dict | None) -> dict:
    today = date.today().strftime("%A, %d/%m/%Y")

    if task:
        key = task["key"]
        summary = task["fields"]["summary"]
        prio = (task["fields"].get("priority") or {}).get("name", "")
        url = f"{JIRA_BASE}/browse/{key}"
        task_text = f"[{key}]({url}) — {summary}" + (f"  _(Priority: {prio})_" if prio else "")
    else:
        task_text = "No backlog items found today."

    return {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "6B48FF",
        "summary": f"Good morning ☀️ — {today}",
        "sections": [
            {
                "activityTitle": f"☀️ Good morning — {today}",
                "activitySubtitle": "Daily Reminder",
                "activityText": MOTIVATION,
            },
            {
                "activityTitle": "\U0001f4cb Today's Jira task",
                "activityText": task_text,
            },
        ],
    }


def main():
    jira_email = os.environ["JIRA_EMAIL"]
    jira_token = os.environ["JIRA_API_TOKEN"]
    teams_url  = os.environ["TEAMS_WEBHOOK_URL"]

    issues = fetch_backlog(jira_email, jira_token)
    task   = pick_small_issue(issues)
    card   = build_teams_card(task)

    resp = requests.post(teams_url, json=card, timeout=10)
    print(f"Teams response: {resp.status_code}")
    if resp.text:
        print(resp.text[:300])
    sys.exit(0 if resp.ok else 1)


if __name__ == "__main__":
    main()
