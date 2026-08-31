import subprocess
import os
from flask import Flask, request, render_template_string, session, redirect, url_for, jsonify
from functools import wraps
import logging
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Credentials from environment variables (never hardcode!)
USERNAME = os.environ.get('WEB_USER', 'admin')
PASSWORD = os.environ.get('WEB_PASS', 'admin123')
PORT = int(os.environ.get('PORT', 8080))

# Command history storage
command_history = []
MAX_HISTORY = 100

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Shell - Login</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e22ce 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        
        .login-container {
            background: white;
            padding: 50px;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            width: 100%;
            max-width: 450px;
            animation: slideIn 0.5s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .logo h1 {
            font-size: 48px;
            margin-bottom: 10px;
            color: #2a5298;
        }
        
        .logo p {
            color: #666;
            font-size: 14px;
        }
        
        h2 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
        }
        
        form {
            display: flex;
            flex-direction: column;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
            font-size: 14px;
        }
        
        input {
            width: 100%;
            padding: 14px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s;
            font-family: inherit;
        }
        
        input:focus {
            outline: none;
            border-color: #2a5298;
            box-shadow: 0 0 0 4px rgba(42, 82, 152, 0.1);
            background: #f8f9ff;
        }
        
        button {
            padding: 14px;
            margin-top: 20px;
            background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(42, 82, 152, 0.3);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .error {
            color: #e74c3c;
            text-align: center;
            margin: 15px 0;
            padding: 15px;
            background: #fadbd8;
            border-radius: 8px;
            border-left: 4px solid #e74c3c;
            font-size: 14px;
        }
        
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #999;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <h1>⚡</h1>
            <p>Web Shell Terminal</p>
        </div>
        
        <h2>Login</h2>
        
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        
        <form method="POST">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" placeholder="Enter your username" required autofocus>
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter your password" required>
            </div>
            
            <button type="submit">Sign In</button>
        </form>
        
        <div class="footer">
            <p>Web Shell Terminal • Created by Mikaeil297</p>
        </div>
    </div>
</body>
</html>
"""

SHELL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Web Shell Terminal</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Fira Code', 'Courier New', monospace;
            background: #0a0e27;
            color: #e0e0e0;
            overflow: hidden;
        }
        
        .container {
            display: flex;
            flex-direction: column;
            height: 100vh;
        }
        
        header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px 30px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header-left {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .header-left h1 {
            font-size: 24px;
            color: white;
            font-weight: 700;
        }
        
        .header-right {
            display: flex;
            gap: 15px;
            align-items: center;
        }
        
        .user-info {
            font-size: 14px;
            color: rgba(255, 255, 255, 0.9);
        }
        
        .logout-btn {
            background: #e74c3c;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }
        
        .logout-btn:hover {
            background: #c0392b;
            transform: translateY(-2px);
        }
        
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .terminal-output {
            flex: 1;
            background: #0a0e27;
            border: 1px solid #1e3a5f;
            margin: 20px 30px 0 30px;
            border-radius: 10px 10px 0 0;
            overflow-y: auto;
            padding: 20px;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        
        .terminal-output::-webkit-scrollbar {
            width: 8px;
        }
        
        .terminal-output::-webkit-scrollbar-track {
            background: #1a1f3a;
            border-radius: 10px;
        }
        
        .terminal-output::-webkit-scrollbar-thumb {
            background: #2a5298;
            border-radius: 10px;
        }
        
        .terminal-output::-webkit-scrollbar-thumb:hover {
            background: #3a6bb8;
        }
        
        .input-section {
            background: #0a0e27;
            padding: 20px 30px 30px 30px;
            border: 1px solid #1e3a5f;
            margin: 0 30px 20px 30px;
            border-radius: 0 0 10px 10px;
            display: flex;
            gap: 10px;
        }
        
        .input-wrapper {
            flex: 1;
            display: flex;
            gap: 10px;
        }
        
        .prompt {
            color: #4CAF50;
            font-weight: bold;
            user-select: none;
        }
        
        input[type="text"] {
            flex: 1;
            background: #1a1f3a;
            border: 2px solid #2a5298;
            color: #e0e0e0;
            padding: 12px 15px;
            border-radius: 6px;
            font-family: inherit;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        input[type="text"]:focus {
            outline: none;
            border-color: #4CAF50;
            box-shadow: 0 0 10px rgba(76, 175, 80, 0.3);
            background: #202540;
        }
        
        .button-group {
            display: flex;
            gap: 8px;
        }
        
        button {
            padding: 12px 24px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 14px;
            transition: all 0.3s;
            font-family: inherit;
        }
        
        button:hover {
            background: #45a049;
            transform: translateY(-2px);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        button.clear-btn {
            background: #f39c12;
        }
        
        button.clear-btn:hover {
            background: #e67e22;
        }
        
        .command {
            color: #4CAF50;
            margin: 10px 0 5px 0;
        }
        
        .output {
            color: #e0e0e0;
            margin-bottom: 10px;
        }
        
        .error {
            color: #e74c3c;
        }
        
        .info {
            color: #3498db;
        }
        
        .warning {
            color: #f39c12;
        }
        
        .success {
            color: #4CAF50;
        }
        
        .timestamp {
            color: #7f8c8d;
            font-size: 12px;
        }
        
        .history-indicator {
            color: #95a5a6;
            font-size: 12px;
            margin-left: 10px;
        }
        
        .shortcut-info {
            background: #1a1f3a;
            border: 1px solid #2a5298;
            padding: 15px 30px;
            border-radius: 6px;
            font-size: 12px;
            color: #95a5a6;
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin: 0 30px 30px 30px;
        }
        
        .shortcut-info span {
            display: inline-block;
        }
        
        .shortcut-info kbd {
            background: #0a0e27;
            padding: 2px 6px;
            border-radius: 3px;
            border: 1px solid #2a5298;
            color: #4CAF50;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-left">
                <h1>⚡ Web Shell Terminal</h1>
            </div>
            <div class="header-right">
                <div class="user-info">
                    <span id="current-time"></span>
                </div>
                <a href="/logout" class="logout-btn">Logout</a>
            </div>
        </header>
        
        <div class="main-content">
            <div class="terminal-output" id="terminal-output">{{ output }}</div>
            
            <div class="input-section">
                <form method="POST" style="display: flex; width: 100%; gap: 10px;" id="command-form">
                    <div class="input-wrapper">
                        <span class="prompt">$</span>
                        <input type="text" id="cmd-input" name="cmd" placeholder="Enter your command here..." autofocus spellcheck="false">
                    </div>
                    <div class="button-group">
                        <button type="submit">Execute</button>
                        <button type="button" class="clear-btn" onclick="clearTerminal()">Clear</button>
                    </div>
                </form>
            </div>
            
            <div class="shortcut-info">
                <span><kbd>Enter</kbd> Execute</span>
                <span><kbd>↑/↓</kbd> History</span>
                <span><kbd>Ctrl+L</kbd> Clear</span>
                <span id="history-count">History: 0 commands</span>
            </div>
        </div>
    </div>
    
    <script>
        let historyIndex = -1;
        let commands = [];
        
        // Update time
        function updateTime() {
            const now = new Date();
            document.getElementById('current-time').textContent = now.toLocaleTimeString();
        }
        setInterval(updateTime, 1000);
        updateTime();
        
        // Auto-scroll to bottom
        function scrollToBottom() {
            const terminal = document.getElementById('terminal-output');
            terminal.scrollTop = terminal.scrollHeight;
        }
        
        // Clear terminal
        function clearTerminal() {
            if (confirm('Clear all output?')) {
                document.getElementById('terminal-output').innerHTML = '<span class="info">Terminal cleared</span>';
                commands = [];
                historyIndex = -1;
                updateHistoryCount();
            }
        }
        
        // Update history count
        function updateHistoryCount() {
            document.getElementById('history-count').textContent = 'History: ' + commands.length + ' commands';
        }
        
        // Keyboard shortcuts
        document.getElementById('cmd-input').addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                document.getElementById('command-form').submit();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (historyIndex < commands.length - 1) {
                    historyIndex++;
                    this.value = commands[commands.length - 1 - historyIndex];
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (historyIndex > 0) {
                    historyIndex--;
                    this.value = commands[commands.length - 1 - historyIndex];
                } else if (historyIndex === 0) {
                    historyIndex = -1;
                    this.value = '';
                }
            } else if (e.ctrlKey && e.key === 'l') {
                e.preventDefault();
                clearTerminal();
            }
        });
        
        // Store command
        document.getElementById('command-form').addEventListener('submit', function(e) {
            const cmd = document.getElementById('cmd-input').value.trim();
            if (cmd && commands[commands.length - 1] !== cmd) {
                commands.push(cmd);
                if (commands.length > 100) commands.shift();
            }
            historyIndex = -1;
            updateHistoryCount();
        });
        
        // Scroll on page load
        window.addEventListener('load', function() {
            scrollToBottom();
            updateHistoryCount();
        });
        
        // Scroll after form submission
        setTimeout(scrollToBottom, 100);
    </script>
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
            error = 'Invalid username or password!'
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
    output = '<span class="success">✓ Ready to execute commands...</span>\n'
    
    if request.method == 'POST':
        cmd = request.form.get('cmd', '').strip()
        
        if not cmd:
            output = '<span class="warning">⚠ Please enter a command!</span>'
        else:
            try:
                # Add command to history
                command_history.append({
                    'command': cmd,
                    'timestamp': datetime.now().isoformat()
                })
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                # Execute command with timeout for safety
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd=os.path.expanduser('~')
                )
                
                timestamp = datetime.now().strftime('%H:%M:%S')
                output = f'<span class="command">$ {cmd}</span>\n'
                
                if result.stdout:
                    output += f'<span class="output">{result.stdout}</span>'
                
                if result.stderr:
                    output += f'<span class="error">{result.stderr}</span>'
                
                if not result.stdout and not result.stderr:
                    output += '<span class="success">✓ Command executed successfully</span>'
                
                logger.info(f"Command executed: {cmd}")
            
            except subprocess.TimeoutExpired:
                output = '<span class="error">✗ Command timed out (max 60 seconds)!</span>'
                logger.warning(f"Command timeout: {cmd}")
            
            except FileNotFoundError as e:
                output = f'<span class="error">✗ Command not found: {str(e)}</span>'
                logger.error(f"Command not found: {cmd}")
            
            except Exception as e:
                output = f'<span class="error">✗ Error: {str(e)}</span>'
                logger.error(f"Command error: {cmd} - {str(e)}")
    
    return render_template_string(SHELL_TEMPLATE, output=output)

@app.route('/api/history')
@login_required
def get_history():
    """Get command history as JSON"""
    return jsonify(command_history)

@app.route('/api/clear-history', methods=['POST'])
@login_required
def clear_history():
    """Clear command history"""
    global command_history
    command_history = []
    logger.info("Command history cleared")
    return jsonify({'status': 'success'})

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
