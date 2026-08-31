import subprocess
import os
from flask import Flask, request, render_template_string, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Read credentials from Secrets or use defaults
USERNAME = os.environ.get('WEB_USER', 'admin')
PASSWORD = os.environ.get('WEB_PASS', 'admin123')

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>Web Shell Login</title></head>
<body style="font-family: sans-serif; text-align: center; padding-top: 100px;">
    <h2>🔐 Login - Created by mikaeil297</h2>
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

SHELL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>GitHub Web Shell</title></head>
<body style="font-family: sans-serif; padding: 20px;">
    <h2>💻 Web Shell - Created by mikaeil297</h2>
    <p><a href="/logout" style="color: red;">Logout</a></p>
    <form method="POST">
        <input type="text" name="cmd" placeholder="Enter command (e.g. ls -la)" style="width: 70%; padding: 5px;">
        <button type="submit">Execute</button>
    </form>
    <pre style="background: #f0f0f0; padding: 15px; border-radius: 5px; margin-top: 20px; white-space: pre-wrap;">{{ output }}</pre>
</body>
</html>
"""

def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = '❌ Invalid username or password!'
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    output = "✅ Logged in! Waiting for your command..."
    if request.method == 'POST':
        cmd = request.form.get('cmd', '')
        if cmd:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                output = result.stdout if result.stdout else result.stderr
                if not output:
                    output = "✔️ Command executed successfully with no output."
            except Exception as e:
                output = f"❌ Error: {e}"
    return render_template_string(SHELL_TEMPLATE, output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
