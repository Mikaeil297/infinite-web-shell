# infinite-web-shell

**Created by:** [mikaeil297](https://github.com/mikaeil297)

An infinite loop between two GitHub Actions workflows (A and B) that trigger each other every 6 hours, cancel the previous run, and start a **password-protected web shell**.

## 🛑 Stopping the Loop (Workflow C)

- Go to the **Actions** tab.
- Select **Workflow C - Stopper**.
- Click **Run workflow**.
- In the `confirm` field, type exactly: `stop`
- Click **Run workflow** again.
- Workflow C will:
  1. Send a `stop` signal to **A** and **B**.
  2. The next time A or B runs, they will exit immediately.
  3. Workflow C cancels its own run.
- The infinite loop is now completely stopped.

## 🔐 Default Login
- **Username:** `admin`
- **Password:** `admin123`

## ⚠️ Security Warning
This project is for **educational purposes only**. Use in private repositories.

## 📂 Project Structure
```

.github/workflows/
├── a.yml
├── b.yml
└── c.yml
web_shell.py
README.md

```

## 🚀 How It Works
- A and B run every 6 hours (cron).
- Each starts a web shell and calls the other (if triggered by schedule).
- C stops everything when you trigger it manually.

---
**Author:** mikaeil297
```

---

📌 How to Use Workflow C to Stop Everything

1. Go to your repository on GitHub.
2. Click the Actions tab.
3. On the left sidebar, click Workflow C - Stopper.
4. Click the Run workflow dropdown button.
5. In the confirm field, type exactly: stop
6. Click the Run workflow button.
7. Workflow C will:
   · Send a stop signal to both A and B.
   · Cancel its own run.
8. The next scheduled runs of A and B will see the stop signal and exit immediately.
9. The infinite loop is completely broken.

---

✅ Summary of All 3 Workflows

Workflow Purpose
A Runs at 00:00 & 12:00 – starts web shell – triggers B
B Runs at 06:00 & 18:00 – starts web shell – triggers A
C Manual trigger – stops A and B – then self-destructs

---

