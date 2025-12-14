# Phishing Telemetry & Evasion Analysis Framework

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Framework](https://img.shields.io/badge/Framework-Flask-green?style=flat&logo=flask)
![Focus](https://img.shields.io/badge/Focus-Traffic%20Distribution-red)

## Project Goal
This project is a **"Purple Team"** research tool designed to analyze **Traffic Distribution Systems (TDS)** and **Cloaking Techniques** used in advanced phishing campaigns. 

Unlike simple tracking pixels, this server implements **active filtering** to distinguish between security scanners (Bots) and real victims (Humans). It demonstrates how attackers bypass automated analysis by serving different content based on the visitor's profile.

## Key Features (Implemented in `server.py`)

### 1. Advanced Bot & Scanner Detection
The system analyzes `User-Agent` strings to identify known security crawlers and sandboxes, including:
* **Security Vendors:** Microsoft Defender, Barracuda, Proofpoint, Cisco IronPort.
* **Crawlers:** Googlebot, Bingbot, Slackbot, Twitterbot.
* **Method Analysis:** Automatically flags `HEAD` requests as non-human traffic.

### 2. Evasion & Cloaking Logic
Implements conditional response logic to evade detection:
* **For Bots:** Returns a harmless plain text response (`"Scanning content..."`) to avoid raising alarms in security gateways.
* **For Humans:** Serves an HTML page with a **JavaScript-based redirect** timer, simulating a legitimate verification process before redirecting to the target.

### 3. True IP Resolution (Proxy Aware)
Designed to work behind WAFs and Reverse Proxies. It correctly resolves the **Origin IP** of the client by prioritizing:
* `CF-Connecting-IP` (Cloudflare Support)
* `X-Forwarded-For` (Standard Proxy)
* `Remote_Addr` (Direct Connection)

### 4. Forensic Logging
Telemetry data is recorded in a structured **CSV format** (`click-logs.csv`) for post-incident analysis, capturing:
* Timestamp & Scenario Name
* Victim IP & User-Agent
* Request Method
* Classification Result (Human vs. Bot)

## Tech Stack
* **Language:** Python 3
* **Web Framework:** Flask
* **Techniques:** Server-Side Filtering, Header Analysis, CSV Logging

## Usage

1.  **Clone and Install:**
    ```bash
    git clone [https://github.com/orhunburakiyane/Phishing-Telemetry-Analysis-Tool.git](https://github.com/orhunburakiyane/Phishing-Telemetry-Analysis-Tool.git)
    pip install flask
    ```

2.  **Run the Server:**
    ```bash
    python server.py
    ```

3.  **Simulate a Campaign:**
    * **Test as Human:** Open browser to `http://localhost:5000/track/test-campaign`
    * **Test as Bot:** Use curl: `curl -A "Googlebot" http://localhost:5000/track/test-campaign`
    * Check `click-logs.csv` to see the different classifications.

## ⚠️ Legal & Ethical Disclaimer
**For Educational and Research Purposes Only.**
This tool is created to demonstrate evasion techniques used by threat actors to improve detection rules (Blue Team) and awareness training. It should never be used for malicious activities.
