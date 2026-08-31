# infinite-web-shell

# GitHub Actions Infinite Loop with Web Shell

This repository demonstrates an infinite loop between two workflows (`A` and `B`) that trigger each other every 6 hours, cancel the previous run, and run a web-based shell (using Flask + ngrok) inside the runner.

## 🔄 How the Loop Starts Automatically

- Workflow **A** is scheduled at `00:00` and `12:00` UTC.
- Workflow **B** is scheduled at `06:00` and `18:00` UTC.
- As soon as the first cron hits (e.g., 00:00), Workflow **A** starts.
- Because it was triggered by the schedule, it calls Workflow **B** via `workflow_dispatch`.
- Workflow **B** starts, and at its next scheduled time (06:00), it calls Workflow **A** again.
- This cycle repeats forever, with `concurrency` cancelling the previous run each time.

> **No manual intervention is needed.** Just push the files and wait for the first scheduled time.

## ⚠️ WARNING

- This web shell is **unauthenticated** – anyone with the URL can control your runner.
- Use only in **private repositories** and **never share the URL**.
- For educational purposes only. Malicious use will get your account banned.

## 🛠 Prerequisites

- A **public repository** (to avoid monthly minute limits) – if private, free minutes (2000/month) will run out in less than 2 days.
- An [ngrok account](https://ngrok.com) to get your **authtoken**.
- Add the token as a secret in your repository:
  - Go to `Settings` → `Secrets and variables` → `Actions` → `New repository secret`
  - Name: `NGROK_AUTH_TOKEN`
  - Value: your ngrok authtoken

## 📂 Files Structure

```

.github/workflows/
├── a.yml
└── b.yml
web_shell.py
README.md

```

## 📄 File Contents (see below)
```

---
