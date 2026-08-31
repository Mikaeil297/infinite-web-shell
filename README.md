# infinite-web-shell

**Created by:** [mikaeil297](https://github.com/mikaeil297)

An infinite loop between two GitHub Actions workflows that triggers each other every 6 hours, cancels the previous run, and starts a **password-protected web shell** inside the runner using Flask + ngrok.

## 🔐 Default Login
- **Username:** `admin`
- **Password:** `admin123`

*(You can override these by adding `WEB_USER` and `WEB_PASS` to your GitHub Secrets.)*

## ⚠️ Security Warning
This project is for **educational purposes only**. Even with a password, never expose this to the public for long periods. Use it in private repositories.

## 🚀 How It Works
- **Workflow A** runs at `00:00` and `12:00` UTC.
- **Workflow B** runs at `06:00` and `18:00` UTC.
- Each run starts a web server on port `8080` and tunnels it via ngrok.
- `concurrency` with `cancel-in-progress: true` stops the previous run instantly.
- Only the run triggered by the **schedule (cron)** calls the other workflow.

## 📂 Project Structure
```

.github/workflows/
├── a.yml
└── b.yml
web_shell.py
README.md

```

## 🛠 Prerequisites
1. A **public repository** (to avoid GitHub's free minute limits for private repos).
2. A free [ngrok](https://ngrok.com) account to get your **authtoken**.
3. Add the ngrok token as a secret:
   - Go to `Settings` → `Secrets and variables` → `Actions`.
   - Name: `NGROK_AUTH_TOKEN` → Value: *your ngrok token*.

## 🧪 How to Run

### Option 1: Automatic (Wait for the Cron)
1. Push all the files to your repository.
2. Go to the **Actions** tab.
3. Wait for the scheduled times (00:00, 06:00, 12:00, 18:00 UTC). The loop will start automatically.

### Option 2: Manual Test
1. Go to the **Actions** tab.
2. Select **Workflow A** and click **Run workflow**.
3. Select **Workflow B** and click **Run workflow** (a few minutes later).
   *(Note: Manual runs will NOT trigger the other workflow because of the `if: github.event_name == 'schedule'` condition.)*

## 👀 Accessing the Web Shell
1. Open the running workflow log.
2. Find the line that says:
```

✅ Web Shell URL: https://xxxx.ngrok.io

```
3. Open the URL in your browser.
4. Enter the username (`admin`) and password (`admin123`).
5. Type your shell commands (e.g., `ls -la`, `whoami`) and click **Execute**.

## 🛑 Stopping the Loop
To stop the infinite loop:
- Delete or comment out the `schedule` section in `a.yml` and `b.yml`, OR
- Disable the workflows in the Actions tab, OR
- Archive/Delete the repository.

---
**Author:** mikaeil297
