#!/usr/bin/env python3
"""
Daily morning motivation + random small Jira task -> Microsoft Teams notification.
Triggered by GitHub Actions cron every morning at 10:00 AM Israel time.

Required GitHub Actions secrets:
  JIRA_EMAIL        - Atlassian account email (miryamma@etoro.com)
  JIRA_API_TOKEN    - Atlassian API token from:
                      https://id.atlassian.com/manage-profile/security/api-tokens
  TEAMS_WEBHOOK_URL - Incoming webhook URL from your Teams channel
                      (Channel -> ... -> Connectors -> Incoming Webhook)
"""
import os
import json
import random
import urllib.request
import urllib.parse
import base64

MOTIVATIONAL_INTRO = (
    "המציאות של יהודי בעולם היא יקרה וחשובה מאוד מאוד. "
    "גם בלי שיעשה כלום לקיום שלו בעולם יש משמעות אדירה. "
    "בעצם העובדה שיהודי חי, הוא ממלא תפקיד גדול ועושה לבורא נחת רוח עצומה.\n\n"
    "**ועכשיו בשפת הייטק:**\n"
    "אני לא חייבת לאהוב את הסביבה כדי לצמוח ממנה. "
    "כל יום שאני מעמיקה את הידע שלי, בונה השפעה ומחזקת את היכולות שלי — "
    "אני מתקדמת לכיוון שאני רוצה להיות בו. "
    "המטרה שלי היא לא להיות העובדת הכי מתוסכלת בחדר. "
    "המטרה שלי היא להיות האדם שאליו פונים כשצריך להבין, להוביל ולפתור בעיות."
)

DAILY_TIPS = (
    "- ב-Code Review: להילחם רק על מה שבאמת חשוב\n"
    "- להתמקד במה שבשליטי, לא במה שמעצבן אותי\n"
    "- לנצל זמני אוויר ללמידה ולהעמקה במערכת\n"
    "- להבין עוד חלק אחד במערכת בכל יום\n"
    "- להשאיר כל דבר קצת יותר טוב ממה שמצאתי אותו\n"
    "- למדוד את היום לפי מה שלמדתי והשפעתי, לא לפי איכות הניהול"
)

JIRA_BASE = "https://etoro-jira.atlassian.net"


def fetch_backlog_issues(email: str, token: str) -> list:
    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
    }
    jql = (
        "project = EMM AND sprint is EMPTY "
        "AND statusCategory != Done "
        "ORDER BY created DESC"
    )
    params = urllib.parse.urlencode({
        "jql": jql,
        "fields": "summary,priority,labels,customfield_10016,issuetype,description",
        "maxResults": 100,
    })
    req = urllib.request.Request(
        f"{JIRA_BASE}/rest/api/3/search?{params}", headers=headers
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read())
    return data.get("issues", [])


def pick_small_issue(issues: list) -> dict:
    if not issues:
        return None

    def smallness_score(issue):
        fields = issue["fields"]
        score = 50
        sp = fields.get("customfield_10016")
        if sp is not None:
            score = int(sp) * 10
        labels = [l.lower() for l in (fields.get("labels") or [])]
        if any(l in ("small", "quick", "minor", "chore", "tech-debt") for l in labels):
            score -= 20
        itype = (fields.get("issuetype") or {}).get("name", "")
        if itype in ("Sub-task", "Bug", "Task"):
            score -= 10
        desc = fields.get("description") or ""
        desc_len = len(json.dumps(desc)) if isinstance(desc, dict) else len(str(desc))
        if desc_len < 300:
            score -= 15
        return score

    issues_sorted = sorted(issues, key=smallness_score)
    pool = issues_sorted[: min(10, len(issues_sorted))]
    return random.choice(pool)


def build_teams_card(issue: dict) -> dict:
    if issue:
        key = issue["key"]
        summary = issue["fields"]["summary"]
        issue_url = f"{JIRA_BASE}/browse/{key}"
        task_text = f"**[{key}]({issue_url})** — {summary}"
    else:
        task_text = "לא נמצאו פריטים בבקלוג — זמן ללמידה! \U0001f4da"
        issue_url = ""

    card = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "6264A7",
        "summary": "☀️ בוקר טוב — המוטיבציה היומית שלך",
        "sections": [
            {
                "activityTitle": "☀️ בוקר טוב",
                "activitySubtitle": "המוטיבציה היומית שלך",
                "markdown": True,
                "text": MOTIVATIONAL_INTRO,
            },
            {
                "title": "ועכשיו לתכלס:",
                "markdown": True,
                "text": DAILY_TIPS,
            },
            {
                "title": "\U0001f3af משימת היום",
                "markdown": True,
                "text": task_text,
            },
        ],
    }

    if issue_url:
        card["potentialAction"] = [
            {
                "@type": "OpenUri",
                "name": "פתח ב-Jira",
                "targets": [{"os": "default", "uri": issue_url}],
            }
        ]

    return card


def send_to_teams(webhook_url: str, card: dict) -> None:
    payload = json.dumps(card, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode()
        print(f"Teams response: {resp.status} — {body}")


def main():
    email = os.environ["JIRA_EMAIL"]
    token = os.environ["JIRA_API_TOKEN"]
    webhook_url = os.environ["TEAMS_WEBHOOK_URL"]

    print("Fetching EMM backlog from Jira...")
    issues = fetch_backlog_issues(email, token)
    print(f"Found {len(issues)} backlog issues")

    issue = pick_small_issue(issues)
    if issue:
        print(f"Selected: {issue['key']} — {issue['fields']['summary']}")
    else:
        print("No issues found, sending without task")

    card = build_teams_card(issue)
    print("Sending to Teams...")
    send_to_teams(webhook_url, card)
    print("Done!")


if __name__ == "__main__":
    main()
