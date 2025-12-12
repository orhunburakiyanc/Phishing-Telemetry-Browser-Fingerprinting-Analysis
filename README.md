# Phishing Telemetry & User Fingerprinting Analysis 🕵️‍♂️

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python)
![Framework](https://img.shields.io/badge/Framework-Flask-green?style=flat&logo=flask)
![Focus](https://img.shields.io/badge/Focus-Security%20Research-red)
![License](https://img.shields.io/badge/License-MIT-grey)

## Project Goal
This project is a **"Purple Team"** research tool designed to reverse-engineer and demonstrate the tracking techniques used in advanced phishing campaigns. 

By simulating a malicious telemetry server, it helps security professionals and awareness trainers understand:
1.  **Email Reconnaissance:** How attackers verify if an email is opened using **Tracking Pixels**.
2.  **Victim Profiling:** What data (IP, User-Agent, Device Type) is exfiltrated instantly upon a click.
3.  **Fingerprinting:** How browser configurations are used to track users across sessions.

## Technical Implementation
The project uses **Python Flask** to create a lightweight telemetry collector acting as a simulated C2 (Command & Control) endpoint.

* **1x1 Tracking Pixel:** Serves an invisible 1x1 GIF image to log interaction times and IP addresses without user interaction.
* **Header Analysis:** Parses HTTP headers to extract OS, Browser Version, and Referrer data.
* **Logging System:** structured logging of "victim" requests for forensic analysis.

## Tech Stack
* **Language:** Python 3
* **Web Framework:** Flask
* **Libraries:** `datetime`, `logging`, `io`

## Usage

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/orhunburakiyane/Phishing-Telemetry-Analysis-Tool.git](https://github.com/orhunburakiyane/Phishing-Telemetry-Analysis-Tool.git)
    cd Phishing-Telemetry-Analysis-Tool
    ```

2.  **Install dependencies:**
    *(Flask is the only requirement)*
    ```bash
    pip install flask
    ```

3.  **Run the Telemetry Server:**
    ```bash
    python app.py
    ```
    *Server will start on `http://0.0.0.0:5000`*

4.  **Test the Tracking:**
    * Open `http://localhost:5000/tracking_pixel.png` in your browser.
    * Check the terminal or `victim_logs.txt` to see the captured footprint.

## ⚠️ Legal & Ethical Disclaimer
**For Educational and Research Purposes Only.**
This tool is created to demonstrate web tracking risks and improve defense mechanisms. It should never be used for malicious activities, unauthorized surveillance, or on networks where you do not have explicit permission. The author assumes no liability for misuse.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.
