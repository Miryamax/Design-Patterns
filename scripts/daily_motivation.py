#!/usr/bin/env python3
"""
Daily motivation email sender.
Fetches a random small item from the EMM Jira backlog and sends a motivational
email to the configured recipient.

Required env vars:
  JIRA_EMAIL         - Atlassian account email (e.g. you@etoro.com)
  JIRA_API_TOKEN     - Atlassian API token
  GMAIL_SENDER       - Gmail address used to send the email
  GMAIL_APP_PASSWORD - Gmail app password for that address
  RECIPIENT_EMAIL    - Destination email address
"""

import os
import random
import smtplib
import sys
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

# ── configuration ─────────────────────────────────────────────────────────────

JIRA_BASE = "https://etoro-jira.atlassian.net"
JIRA_PROJECT = "EMM"
JIRA_BOARD_URL = "https://etoro-jira.atlassian.net/jira/software/c/projects/EMM/boards/513/backlog"

MOTIVATIONAL_MESSAGE = """המציאות של יהודי בעולם היא יקרה וחשובה מאוד מאוד. גם בלי שיעשה כלום לקיום שלו בעולם יש משמעות אדירה. בעצם העובדה שיהודי חי, הוא ממלא תפקיד גדול ועושה לבורא נחת רוח עצומה.

ועכשיו בשפת הייטק:
אני לא חייבת לאהוב את הסביבה כדי לצמוח ממנה. כל יום שאני מעמיקה את הידע שלי, בונה השפעה ומחזקת את היכולות שלי - אני מתקדמת לכיוון שאני רוצה להיות בו. המטרה שלי היא לא להיות העובדת הכי מתוסכלת בחדר. המטרה שלי היא להיות האדם שאליו פונים כשצריך להבין, להוביל ולפתור בעיות.

ועכשיו לתכלס:
- ב-Code Review: להילחם רק על מה שבאמת חשוב.
- להתמקד במה שבשליטתי, לא במה שמעצבן אותי.
- לנצל זמני אוויר ללמידה ולהעמקה במערכת.
- להבין עוד חלק אחד במערכת בכל יום.
- להשאיר כל דבר קצת יותר טוב ממה שמצאתי אותו.
- למדוד את היום לפי מה שלמדתי והשפעתי, לא לפי איכות הניהול."""

# ── helpers ───────────────────────────────────────────────────────────────────


def fetch_backlog_issues(email: str, token: str) -> list[dict]:
    """Return open backlog stories/tasks from the EMM project."""
    jql = (
        f"project = {JIRA_PROJECT} "
        "AND sprint is EMPTY "
        "AND statusCategory != Done "
        "AND issuetype in (Story, Task, Bug) "
        "ORDER BY created DESC"
    )
    url = f"{JIRA_BASE}/rest/api/3/search"
    params = {
        "jql": jql,
        "maxResults": 100,
        "fields": "summary,issuetype,priority,labels,story_points,customfield_10016,status",
    }
    resp = requests.get(url, params=params, auth=(email, token), timeout=15)
    resp.raise_for_status()
    return resp.json().get("issues", [])


def pick_small_issue(issues: list[dict]) -> dict | None:
    """Pick a random issue, preferring lightweight ones (small SP, certain keywords)."""
    if not issues:
        return None

    small_keywords = ["get api", "create api", "read", "fetch", "display", "ui", "fix", "cleanup", "rename", "add", "update", "remove", "migrate"]

    def is_small(issue: dict) -> bool:
        f = issue.get("fields", {})
        summary = f.get("summary", "").lower()
        sp = f.get("customfield_10016")  # story points
        if sp is not None and sp <= 3:
            return True
        if any(kw in summary for kw in small_keywords):
            return True
        return False

    small = [i for i in issues if is_small(i)]
    pool = small if small else issues
    return random.choice(pool)


def build_email_html(issue: dict, today: date) -> tuple[str, str]:
    """Return (subject, html_body) for the daily email."""
    f = issue.get("fields", {})
    summary = f.get("summary", "(no summary)")
    key = issue.get("key", "")
    issue_url = f"{JIRA_BASE}/browse/{key}"
    issue_type = f.get("issuetype", {}).get("name", "Task")
    priority = (f.get("priority") or {}).get("name", "")
    sp = f.get("customfield_10016")
    sp_text = f"{int(sp)} SP" if sp else ""

    meta_parts = [p for p in [issue_type, priority, sp_text] if p]
    meta = " · ".join(meta_parts)

    subject = f"☀️ הבוקר שלך | {today.strftime('%d/%m/%Y')}"

    # Plain-text version (also used as fallback)
    msg_plain = MOTIVATIONAL_MESSAGE + f"\n\n---\n📌 המשימה של היום\n\n{key}: {summary}\n{meta}\n{issue_url}\n{JIRA_BOARD_URL}"

    # HTML version
    motivation_html = MOTIVATIONAL_MESSAGE.replace("\n\n", "</p><p dir='rtl'>").replace("\n", "<br>")
    motivation_html = f"<p dir='rtl'>{motivation_html}</p>"

    html = f"""<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <style>
    body {{ font-family: Arial, sans-serif; background: #f9f9f9; padding: 24px; }}
    .card {{ background: white; border-radius: 12px; padding: 28px 32px; max-width: 640px;
             margin: auto; box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
    h1 {{ font-size: 1.3em; color: #1a1a2e; margin-bottom: 4px; }}
    .date {{ color: #888; font-size: .9em; margin-bottom: 24px; }}
    .motivation {{ color: #2d2d2d; line-height: 1.9; font-size: 1.02em; }}
    .divider {{ border: none; border-top: 2px solid #f0f0f0; margin: 28px 0; }}
    .task-box {{ background: #f0f4ff; border-left: 4px solid #4a6cf7;
                 border-radius: 8px; padding: 16px 20px; }}
    .task-label {{ font-size: .8em; color: #666; text-transform: uppercase;
                   letter-spacing: .05em; margin-bottom: 6px; }}
    .task-title {{ font-size: 1.05em; font-weight: 600; color: #1a1a2e; }}
    .task-meta {{ font-size: .85em; color: #888; margin-top: 6px; }}
    .task-link {{ display: inline-block; margin-top: 10px; font-size: .9em;
                  color: #4a6cf7; text-decoration: none; }}
    .board-link {{ display: block; text-align: center; margin-top: 20px;
                   font-size: .85em; color: #aaa; }}
  </style>
</head>
<body>
<div class="card">
  <h1>☀️ הבוקר שלך</h1>
  <div class="date">{today.strftime('%A, %d %B %Y')}</div>

  <div class="motivation">{motivation_html}</div>

  <hr class="divider">

  <div class="task-box">
    <div class="task-label">📌 המשימה של היום</div>
    <div class="task-title">{summary}</div>
    <div class="task-meta">{key}{(' · ' + meta) if meta else ''}</div>
    <a class="task-link" href="{issue_url}">פתח ב-Jira ↗</a>
  </div>

  <a class="board-link" href="{JIRA_BOARD_URL}">צפה ב-Backlog המלא</a>
</div>
</body>
</html>"""

    return subject, html, msg_plain


def send_email(
    sender: str,
    password: str,
    recipient: str,
    subject: str,
    html_body: str,
    plain_body: str,
) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())


# ── main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    jira_email = os.environ["JIRA_EMAIL"]
    jira_token = os.environ["JIRA_API_TOKEN"]
    gmail_sender = os.environ["GMAIL_SENDER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    print("Fetching EMM backlog…")
    issues = fetch_backlog_issues(jira_email, jira_token)
    print(f"Found {len(issues)} backlog issues")

    issue = pick_small_issue(issues)
    if not issue:
        print("No backlog issues found – sending motivation only")
        issue = {"key": "", "fields": {"summary": "אין משימה היום — קדימה לבחור משהו!", "issuetype": {}, "priority": None, "customfield_10016": None}}

    key = issue.get("key", "")
    summary = issue.get("fields", {}).get("summary", "")
    print(f"Selected issue: {key} – {summary}")

    today = date.today()
    subject, html_body, plain_body = build_email_html(issue, today)

    print(f"Sending email to {recipient}…")
    send_email(gmail_sender, gmail_password, recipient, subject, html_body, plain_body)
    print("Email sent successfully!")


if __name__ == "__main__":
    main()
