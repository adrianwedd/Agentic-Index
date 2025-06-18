#!/usr/bin/env python3
"""Monitor GitHub metrics and alert on unexpected changes."""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

import requests

STAR_DROP_THRESHOLD = int(os.getenv("STAR_DROP_THRESHOLD", "1"))
RELEASE_AGE_THRESHOLD = int(os.getenv("RELEASE_AGE_THRESHOLD", "30"))


def _headers() -> Dict[str, str]:
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def fetch_repo_data(full_name: str) -> Dict[str, int | None]:
    """Return current star count and release age for ``full_name``."""
    resp = requests.get(
        f"https://api.github.com/repos/{full_name}", headers=_headers(), timeout=10
    )
    resp.raise_for_status()
    data = resp.json()
    stars = int(data.get("stargazers_count", 0))

    rel_resp = requests.get(
        f"https://api.github.com/repos/{full_name}/releases/latest",
        headers=_headers(),
        timeout=10,
    )
    release_age = None
    if rel_resp.status_code == 200:
        ts = rel_resp.json().get("published_at")
        if ts:
            try:
                dt = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
                release_age = (
                    datetime.now(timezone.utc) - dt.replace(tzinfo=timezone.utc)
                ).days
            except Exception:
                release_age = None
    return {"stars": stars, "release_age": release_age}


def slack_alert(message: str) -> None:
    url = os.getenv("SLACK_WEBHOOK_URL")
    if not url:
        return
    try:
        requests.post(url, json={"text": message}, timeout=10)
    except Exception:
        pass


def email_alert(subject: str, message: str) -> None:
    import smtplib
    from email.message import EmailMessage

    to_addr = os.getenv("ALERT_EMAIL")
    server = os.getenv("SMTP_SERVER")
    if not (to_addr and server):
        return
    from_addr = os.getenv("FROM_EMAIL", to_addr)
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg.set_content(message)
    try:
        port = int(os.getenv("SMTP_PORT", "25"))
        user = os.getenv("SMTP_USER")
        password = os.getenv("SMTP_PASS")
        with smtplib.SMTP(server, port) as smtp:
            if user:
                smtp.starttls()
                smtp.login(user, password or "")
            smtp.send_message(msg)
    except Exception:
        pass


def load_repos(path: str) -> Iterable[dict]:
    data = json.loads(Path(path).read_text())
    return data.get("repos", data)


def check_repo(repo: dict) -> List[str]:
    actual = fetch_repo_data(repo["full_name"])
    messages = []
    expected_stars = repo.get("stargazers_count", repo.get("stars", 0))
    if actual["stars"] < expected_stars - STAR_DROP_THRESHOLD:
        messages.append(
            f"{repo['full_name']} stars {expected_stars}->{actual['stars']}"
        )
    exp_age = repo.get("release_age")
    act_age = actual.get("release_age")
    if exp_age is not None and act_age is not None:
        if act_age > exp_age + RELEASE_AGE_THRESHOLD:
            messages.append(f"{repo['full_name']} release age {exp_age}->{act_age}d")
    return messages


def main(path: str = "data/repos.json") -> int:
    repos = load_repos(path)
    alerts: List[str] = []
    for repo in repos:
        alerts.extend(check_repo(repo))
    if alerts:
        message = "\n".join(alerts)
        slack_alert(message)
        email_alert("Agentic Index metrics alert", message)
        print(message)
        return 1
    print("All metrics within expected ranges")
    return 0


if __name__ == "__main__":
    sys.exit(main(os.getenv("METRICS_FILE", "data/repos.json")))
