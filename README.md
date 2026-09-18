⚡ Nexus Latency Optimizer

**Ultimate System Debloater & Input Lag Reducer for Competitive Gaming**

Nexus Latency Optimizer is an open-source, lightweight GUI utility designed to strip away Windows bloatware, disable heavy background telemetry, and optimize your network/CPU settings for zero input lag. Built specifically for competitive titles like **CS2, Dota 2, and Valorant**, this tool applies safe registry and system-level tweaks with a single click.

🚀 Key Features

* **1:1 Mouse Aim:** Disables residual Windows mouse acceleration completely via registry for flawless tracking.
* **Zero Ping Network Tweaks:** Disables Nagle's Algorithm and removes Network Throttling limits for the lowest possible packet transmission latency.
* **CPU Core Unparking:** Forces the Ultimate Performance power plan and disables HPET/Dynamic Ticks for buttery-smooth frame times.
* **System Debloat:** Safely turns off Xbox Game Bar, Cortana, SysMain (Superfetch), and Microsoft Telemetry to free up RAM and CPU cycles.

🛠️ Installation & Usage

1. Go to the **[Releases](../../releases)** tab and download `Nexus_Optimizer.exe`.
2. Right-click the downloaded file and select **Run as Administrator** (Required for registry and system service tweaks).
3. Select the optimizations you want to apply using the toggles.
4. Click **APPLY TWEAKS**.
5. Restart your PC to let Windows apply the core changes.

## 💻 Open Source Compilation
If you prefer to compile the tool yourself from the source code:
```bash
pip install customtkinter pyinstaller
pyinstaller --noconsole --onefile main.py
Disclaimer
This tool modifies Windows Registry keys and system services to maximize gaming performance. While these tweaks are standard in the competitive scene and completely safe for anti-cheats (VAC, Vanguard, Faceit), use it at your own risk.
