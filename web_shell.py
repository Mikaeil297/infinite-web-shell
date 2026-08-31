import subprocess
import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head><title>GitHub Actions Web Shell</title></head>
<body>
    <h2>💻 GitHub Actions Web Shell</h2>
    <form method="POST">
        <input type="text" name="cmd" placeholder="e.g. ls -la" style="width:70%;">
        <button type="submit">Execute</button>
    </form>
    <pre style="background:#f4f4f4; padding:10px; border-radius:5px;">{{ output }}</pre>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    output = "Awaiting your command..."
    if request.method == 'POST':
        cmd = request.form.get('cmd', '')
        if cmd:
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
                output = result.stdout if result.stdout else result.stderr
                if not output:
                    output = "✔️ Command executed with no output."
            except Exception as e:
                output = f"❌ Error: {e}"
    return render_template_string(HTML_TEMPLATE, output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
