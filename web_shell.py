import subprocess
import os
from flask import Flask, request, render_template_string, session, redirect, url_for
from functools import wraps
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Credentials from environment variables (never hardcode!)
USERNAME = os.environ.get('WEB_USER', 'admin')
PASSWORD = os.environ.get('WEB_PASS', 'admin123')
PORT = int(os.environ.get('PORT', 8080))

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Web Shell Login</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        }
        h2 {
            text-align: center;
            color: #333;
            margin-top: 0;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        input {
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        button {
            padding: 12px;
            margin: 20px 0 0 0;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #5568d3;
        }
        .error {
            color: #e74c3c;
            text-align: center;
            margin: 10px 0;
            padding: 10px;
            background: #fadbd8;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2>Lock Icon Web Shell Login</h2>
        <p style="text-align: center; color: #777;">Created by Mikaeil297</p>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required autofocus>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
"""

SHELL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Web Shell</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            background: #1e1e1e;
            color: #e0e0e0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #333;
        }
        h1 {
            font-size: 24px;
            color: #4CAF50;
        }
        .logout-btn {
            background: #e74c3c;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            text-decoration: none;
            transition: background 0.3s;
        }
        .logout-btn:hover {
            background: #c0392b;
        }
        .input-section {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            background: #2d2d2d;
            border: 1px solid #444;
            color: #e0e0e0;
            border-radius: 4px;
            font-family: inherit;
            font-size: 14px;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #4CAF50;
            box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.1);
        }
        button {
            padding: 12px 24px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            transition: background 0.3s;
        }
        button:hover {
            background: #45a049;
        }
        .output {
            background: #1e1e1e;
            border: 1px solid #333;
            border-radius: 4px;
            padding: 15px;
            height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-size: 13px;
            line-height: 1.5;
        }
        .output::-webkit-scrollbar {
            width: 8px;
        }
        .output::-webkit-scrollbar-track {
            background: #2d2d2d;
        }
        .output::-webkit-scrollbar-thumb {
            background: #4CAF50;
            border-radius: 4px;
        }
        .success {
            color: #4CAF50;
        }
        .error {
            color: #e74c3c;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Computer Icon Web Shell</h1>
            <a href="/logout" class="logout-btn">Logout</a>
        </header>
        
        <div class="input-section">
            <form method="POST" style="display: flex; gap: 10px; width: 100%;">
                <input type="text" name="cmd" placeholder="Enter command (e.g., ls -la, pwd, whoami)" required autofocus>
                <button type="submit">Execute</button>
            </form>
        </div>
        
        <div class="output" id="output">{{ output }}</div>
    </div>
</body>
</html>
"""

def login_required(func):
    """Decorator to require login for routes"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login"""
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            logger.info(f"User logged in: {username}")
            return redirect(url_for('index'))
        else:
            error = 'X Invalid username or password!'
            logger.warning(f"Failed login attempt with username: {username}")
    
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/logout')
def logout():
    """Handle logout"""
    session.pop('logged_in', None)
    logger.info("User logged out")
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """Main shell interface"""
    output = "<span class='success'>Check mark Logged in! Ready to execute commands...</span>"
    
    if request.method == 'POST':
        cmd = request.form.get('cmd', '').strip()
        
        if not cmd:
            output = "<span class='error'>X Please enter a command!</span>"
        else:
            try:
                # Execute command with timeout for safety
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30  # 30 second timeout
                )
                
                if result.stdout:
                    output = f"<span class='success'>$ {cmd}</span>\n{result.stdout}"
                elif result.stderr:
                    output = f"<span class='success'>$ {cmd}</span>\n<span class='error'>{result.stderr}</span>"
                else:
                    output = f"<span class='success'>$ {cmd}\nCheck mark Command executed successfully (no output)</span>"
                
                logger.info(f"Command executed: {cmd}")
            
            except subprocess.TimeoutExpired:
                output = "<span class='error'>X Command timed out (max 30 seconds)!</span>"
                logger.warning(f"Command timeout: {cmd}")
            
            except Exception as e:
                output = f"<span class='error'>X Error: {str(e)}</span>"
                logger.error(f"Command error: {cmd} - {str(e)}")
    
    return render_template_string(SHELL_TEMPLATE, output=output)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return redirect(url_for('login')), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return "<h1>500 - Internal Server Error</h1>", 500

if __name__ == '__main__':
    logger.info(f"Starting Web Shell on port {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)
