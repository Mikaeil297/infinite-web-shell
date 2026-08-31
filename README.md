# Web Shell - Remote Command Execution Interface

A lightweight, web-based shell interface for remote command execution with authentication and ngrok integration for public access.

**Created by:** [@Mikaeil297](https://github.com/Mikaeil297)

---

## Features

- **Authentication**: Username and password protected access
- **Web Interface**: Clean, modern terminal-like user interface
- **Real-time Execution**: Execute system commands instantly
- **Security**: Session-based authentication with timeout protection (30 seconds per command)
- **Portable**: Runs on any system with Python 3.7+
- **ngrok Integration**: Public access via ngrok tunnel (GitHub Actions ready)
- **Dependency Management**: Clean requirements.txt for easy setup
- **Error Handling**: Comprehensive error messages and logging
- **Customizable**: Environment variables for credentials and port configuration

---

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- ngrok account (optional, for public access via GitHub Actions)
- Git (for cloning the repository)

---

## Quick Start

### Step 1: Clone the Repository

```bash
git clone https://github.com/Mikaeil297/infinite-web-shell.git
cd infinite-web-shell
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python web_shell.py
```

Default login credentials:
- **Username:** admin
- **Password:** admin123

Access the application at: **http://localhost:8080**

---

## Custom Configuration

### Using Environment Variables

#### On Linux/macOS:

```bash
export WEB_USER=myusername
export WEB_PASS=mysecurepassword
export PORT=8080
python web_shell.py
```

#### On Windows:

```cmd
set WEB_USER=myusername
set WEB_PASS=mysecurepassword
set PORT=8080
python web_shell.py
```

### Using .env File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your configuration:
   ```env
   WEB_USER=myusername
   WEB_PASS=mysecurepassword
   PORT=8080
   NGROK_TOKEN=your_ngrok_token
   ```

3. Load the environment and run:
   ```bash
   # On Linux/macOS
   source .env
   python web_shell.py
   
   # On Windows (PowerShell)
   ./.env
   python web_shell.py
   ```

---

## Public Access with ngrok

### Automatic Deployment (GitHub Actions)

The repository includes a GitHub Actions workflow that automatically deploys the web shell with ngrok.

**Setup Instructions:**

1. Go to your repository: **Settings → Secrets and variables → Actions**
2. Create a new repository secret:
   - **Name:** `NGROK_TOKEN`
   - **Value:** Your ngrok authentication token (get from [ngrok.com](https://ngrok.com))
3. Trigger the workflow:
   - Push code to the `main` branch, or
   - Go to **Actions** tab and manually run "Deploy Web Shell with ngrok"
4. Check the workflow output for the public URL

**Workflow Features:**
- Automatic ngrok v3 download
- Secure token authentication
- Cleanup on workflow completion
- Public URL generation and logging

### Manual Setup (Local Machine)

1. Download ngrok from [ngrok.com](https://ngrok.com/download)

2. Authenticate ngrok:
   ```bash
   ./ngrok config add-authtoken YOUR_NGROK_TOKEN
   ```

3. Start the web shell:
   ```bash
   python web_shell.py
   ```

4. In another terminal, start the ngrok tunnel:
   ```bash
   ./ngrok http 8080
   ```

5. ngrok will display your public URL:
   ```
   Forwarding                    https://abc-123-def-456.ngrok.io -> http://localhost:8080
   ```

---

## Usage Examples

### Basic Commands

```bash
# Print working directory
pwd

# List files and directories
ls -la

# Create a file
echo "Hello World" > test.txt

# Display file contents
cat test.txt

# Show system information
uname -a

# Check Python version
python --version

# Current user
whoami
```

### System Administration

```bash
# Process list
ps aux

# Disk usage
df -h

# Memory usage
free -h

# Network configuration
ifconfig

# Network connectivity test
ping -c 4 google.com

# Search for files
find . -name "*.py"

# View system logs
tail -f /var/log/syslog
```

### File Operations

```bash
# Copy files
cp source.txt destination.txt

# Move or rename files
mv oldname.txt newname.txt

# Remove files
rm file.txt

# Create directories
mkdir new_directory

# Change permissions
chmod 755 script.sh
```

---

## Configuration Options

### Environment Variables

| Variable | Default | Description | Example |
|----------|---------|-------------|----------|
| `WEB_USER` | `admin` | Login username | `WEB_USER=myuser` |
| `WEB_PASS` | `admin123` | Login password | `WEB_PASS=SecurePass123!` |
| `PORT` | `8080` | Server listening port | `PORT=8000` |
| `NGROK_TOKEN` | *(empty)* | ngrok authentication token | `NGROK_TOKEN=abc123xyz` |

### Command Execution Settings

- **Timeout:** 30 seconds per command (prevents hanging processes)
- **Shell:** System default shell (`/bin/sh` on Linux/macOS, `cmd.exe` on Windows)
- **Output:** Both stdout and stderr are captured and displayed
- **Error Handling:** Comprehensive error messages for debugging

---

## Security Considerations

**WARNING:** This tool executes arbitrary system commands. Handle with care!

### Security Best Practices

1. **Strong Credentials**
   - Use complex, unique passwords
   - Change default credentials immediately
   - Example: `MySecure!Pass2024`

2. **Network Security**
   - Use on private networks when possible
   - Require VPN or SSH tunnel for remote access
   - Keep firewall rules restrictive

3. **HTTPS and Encryption**
   - ngrok provides HTTPS by default
   - Enable ngrok's IP whitelist feature for additional security
   - Avoid HTTP-only connections over untrusted networks

4. **Audit and Monitoring**
   - Review logs regularly: `tail -f nohup.out`
   - Monitor command history
   - Set up alerts for suspicious activity

5. **Access Control**
   - Limit access to trusted users only
   - Disable when not in use
   - Use rate limiting if deployed publicly

### Security Warnings

- Never expose to untrusted networks without proper authentication
- Do not use default credentials in production environments
- Never share authentication tokens in version control or logs
- Do not run with `debug=True` in production
- Regularly update Python and dependencies for security patches
- Implement command filtering or restrictions for sensitive operations

---

## Troubleshooting

### Port Already in Use

**Problem:** `Address already in use` error

**Solution:**
```bash
# Find process using port 8080
lsof -i :8080  # Linux/macOS
netstat -ano | findstr :8080  # Windows

# Kill the process or use different port
kill -9 <PID>  # Linux/macOS
Set PORT=8081 && python web_shell.py  # Windows
export PORT=8081 && python web_shell.py  # Linux/macOS
```

### Connection Refused

**Problem:** Cannot connect to localhost:8080

**Solution:**
- Ensure web shell is running: `python web_shell.py`
- Check if port is correct: default is 8080
- Verify firewall settings
- Check logs for startup errors

### ngrok Authentication Failed

**Problem:** `Error: invalid authtoken`

**Solution:**
```bash
# Reset authtoken
./ngrok config add-authtoken YOUR_NEW_TOKEN

# Verify ngrok version
./ngrok --version  # Should be v3

# View ngrok logs
./ngrok http 8080 --log=stdout --log-level=debug
```

### Permission Denied

**Problem:** `Permission denied` when running ngrok

**Solution:**
```bash
# Make ngrok executable
chmod +x ngrok

# Run with proper permissions
./ngrok http 8080
```

### Command Timeout

**Problem:** "Command timed out (max 30 seconds)" message

**Solution:**
- Use commands that complete within 30 seconds
- For long-running tasks, use background execution:
  ```bash
  nohup python script.py > output.log 2>&1 &
  ```

---

## Deployment Options

### Cloud Platforms

#### Heroku

1. Create `Procfile`:
   ```
   web: python web_shell.py
   ```

2. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

#### AWS EC2

1. SSH to instance:
   ```bash
   ssh -i key.pem ec2-user@instance-ip
   ```

2. Install and run:
   ```bash
   git clone https://github.com/Mikaeil297/infinite-web-shell.git
   cd infinite-web-shell
   pip install -r requirements.txt
   nohup python web_shell.py > web_shell.log 2>&1 &
   ```

#### DigitalOcean Droplet

```bash
# SSH to droplet
ssh root@droplet-ip

# Install dependencies
apt update && apt install -y python3 python3-pip git

# Clone and run
git clone https://github.com/Mikaeil297/infinite-web-shell.git
cd infinite-web-shell
pip3 install -r requirements.txt
nohup python3 web_shell.py > web_shell.log 2>&1 &
```

#### PythonAnywhere

1. Upload files to PythonAnywhere
2. Create web app with Flask
3. Configure WSGI file to import from `web_shell.py`
4. Reload web app

### Docker (Advanced)

**Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY web_shell.py .
EXPOSE 8080
CMD ["python", "web_shell.py"]
```

**Build and run:**
```bash
docker build -t web-shell .
docker run -e WEB_USER=admin -e WEB_PASS=secure_pass -p 8080:8080 web-shell
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add your feature description'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a Pull Request with a clear description

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This tool is provided "as-is" for educational and authorized testing purposes only. Unauthorized access to computer systems is illegal. Users are responsible for:

- Ensuring they have proper authorization before using this tool
- Complying with all applicable laws and regulations
- Protecting the confidentiality and security of their systems
- Monitoring and auditing all command execution

The authors assume no liability for unauthorized or malicious use.

---

## Support and Contact

- **Report Issues:** [GitHub Issues](https://github.com/Mikaeil297/infinite-web-shell/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Mikaeil297/infinite-web-shell/discussions)
- **Author:** [@Mikaeil297](https://github.com/Mikaeil297)
- **Email:** Contact via GitHub profile

---

## Changelog

### Version 2.0.0 (Current)
- Improved security and error handling
- Added requirements.txt for dependency management
- Enhanced README with comprehensive documentation
- Fixed ngrok v2/v3 version mismatch in GitHub Actions
- Added .env.example for secure configuration
- Implemented proper logging and monitoring
- Improved web UI with better styling

### Version 1.0.0
- Initial release
- Basic web shell functionality
- Simple authentication system
- ngrok integration

---

**If you find this project useful, please consider giving it a Star!** ⭐
