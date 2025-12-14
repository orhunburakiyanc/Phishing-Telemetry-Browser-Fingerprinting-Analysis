"""
Phishing Telemetry & Fingerprinting Server
------------------------------------------
Purpose: Simulates a C2 (Command & Control) redirection server to analyze
incoming traffic, distinguish between automated bots (security scanners) and
human targets, and log interaction telemetry.

Key Features:
1. Cloudflare & Proxy IP Resolution: Correctly identifies real client IPs behind WAFs.
2. Bot Detection: Filters out known scanners (Google, Bing, Security Vendors) based on User-Agent.
3. Evasion Technique: Serves different content to Bots (Plain Text) vs Humans (HTML/JS Redirect).
"""

from flask import Flask, request, render_template_string 
import datetime
import csv
import os

app = Flask("server")

LOG_FILE = "click-logs.csv"
REDIRECT_URL = "https://www.google.com"
BOT_KEYWORDS = [
    "GoogleImageProxy", "Microsoft Defender", "SmartScreen", 
    "Cisco IronPort", "Barracuda", "Proofpoint", "bingbot", 
    "Googlebot", "Slackbot-LinkExpanding", "Twitterbot", 
    "facebookexternalhit", "Discordbot"
]

def analyze_request(req):
    user_agent = req.headers.get('User-Agent', '')
    method = req.method
    for keyword in BOT_KEYWORDS:
        if keyword.lower() in user_agent.lower():
            return f"===== BOT/SCANNER ({keyword}) ====="
    
    if method == 'HEAD':
        return "--- BOT (HEAD Request) ---" # a human needs to see the body to read the page, a HEAD request almost always implies non-human intent.
    
    return "=== HUMAN ==="

@app.route('/')
def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tracking Server</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .box {
                background: white;
                padding: 20px 30px;
                border-radius: 8px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                text-align: center;
            }
            h2 {
                margin: 0 0 10px;
            }
            .status {
                color: green;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Tracking Server</h2>
            <p class="status">● ACTIVE</p>
            <p>Use <code>/track/&lt;campaign_name&gt;</code></p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_content)


@app.route('/track/<campaign_name>')
def track_click(campaign_name):
    # Collect data        
    if request.headers.get('CF-Connecting-IP'): # creates a secure "tunnel" from my computer to the internet, gives a public link
        # A TCP connection is required to establish a Cloudflare Tunnel. 
        # Therefore, Cloudflare updates the IP address if it changes or is spoofed.
        # Cloudflare returns only one IP address, which belongs to the client that clicked the link.
        ip = request.headers.get('CF-Connecting-IP')
    elif request.headers.get('X-Forwarded-For'):
        # =============================
        # If the clicker wasn't directed via Cloudflare, client could easily manipulate the header (IP address)
        # In that case, we wouldn't know if the ip was client's real IP or not. 
        # Standard proxies append the IP to the list rather than overwriting it like Cloudflare does.
        # =============================        

        # e.g. ['88.255.12.34', ' 104.21.55.1', ' 127.0.0.1'] 
        # 0th index is the user's ip.
        ip = request.headers.get('X-Forwarded-For').split(',')[0] 
    else:
        ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    method = request.method
    
    # Perform analysis
    classification = analyze_request(request)

    # Write to log file (CSV Format)
    file_exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write headers first if file doesn't exist
        if not file_exists:
            writer.writerow(['Timestamp', 'Scenario', 'IP_Address', 'User_Agent', 'Method', 'Analysis_Result'])
        writer.writerow([timestamp, campaign_name, ip, ua, method, classification])

    # Print output to terminal
    print(f"[{timestamp}] CLICK: {campaign_name} -> {classification}")

    # If BOT, return simple text only (Save resources/Avoid detection)
    if "BOT" in classification:
        return "Scanning content..."

    # If HUMAN, show a convincing page executing JavaScript
    html_content = f"""
    <html>
    <head>
        <title>Loading...</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{ font-family: sans-serif; text-align: center; margin-top: 20%; color: #333; }}
            .loader {{ border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }}
            @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        </style>
        <script>
            console.log("Human verification: JS Active");
            setTimeout(function() {{
                window.location.href = "{REDIRECT_URL}";
            }}, 1500); // Wait 1.5 seconds and redirect
        </script>
    </head>
    <body>
        <div class="loader"></div>
        <h3>Checking secure connection...</h3>
        <p>Please wait.</p>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)