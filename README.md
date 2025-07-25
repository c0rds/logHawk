# LogHawk — Log Monitoring Tool

A lightweight Bash + Python pipeline that **captures live log activity every few minutes and flags suspicious behaviour** (e.g., brute‑force attempts, HTTP 500 storms) before it becomes a full‑blown security incident.

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](#license)

---

## ✨ Key Features
- **Cron‑driven capture** — pulls recent lines from any log on a fixed schedule.
- **Pluggable pattern matching** — track a single IP, a regex, or swap in more filters.
- **Python analytics (`logHawk.py`)** — counts 404/500 spikes & noisy IPs, then drops a timestamped report to your Desktop.
- **One‑liner install** — copy two files, `chmod +x`, add one cron entry, done.
- Works out‑of‑the‑box on **Ubuntu 22.04 LTS**; easily portable to other Linux distros.

---

## 🗺️ Project Layout
loghawk/
├── logCapture.sh → Bash capture/filter script
├── logHawk.py → Python analyser
└── README.md

---

## ⚙️ Requirements
| Component | Minimum Version | Notes |
|-----------|-----------------|-------|
| **Python** | 3.8+ | Standard library only (no `pip` packages needed). |
| **GNU coreutils** | 8.x | `tail`, `grep`, `date`, `mkdir` etc. (default on most distros). |
| **Cron** | any | `cronie`, `vixie‑cron`, or systemd‐timers all work. |

---

## 🚀 Installation

```bash
# 1. Clone the repo (or copy the two scripts)
git clone https://github.com/c0rds/logHawk.git
cd logHawk

# 2. Move scripts into your PATH and mark executable
sudo install -m 755 logCapture.sh /usr/local/bin/
sudo install -m 755 logHawk.py    /usr/local/bin/

# 3. Verify they run
logCapture.sh --help  # (or simply run to test)

## 🛠️ Configuration
Both scripts are plain text—tweak paths and patterns at the top of logCapture.sh.

source_log_file="/var/log/apache2/access.log"  # default source log
destination="/home/student/Desktop/logAnalysis"  # report folder
pattern_of_interest="127\.0\.0\.1"              # grep‑style pattern
Other interesting logs to monitor (edit source_log_file accordingly)

/var/log/auth.log – failed SSH logins, sudo misuse

/var/log/syslog – kernel events, app crashes

## ⏱️ Scheduling with Cron
Edit root’s crontab (or any user that can read the log file):


# Run every 10 minutes:
*/10 * * * * /usr/local/bin/logCapture.sh
Behind the scenes logCapture.sh:

Tails the last 100 lines of access.log and appends matches to
filtered_YYYY‑MM‑DD.log inside /home/student/Desktop/logAnalysis/.

Immediately calls logHawk.py filtered_YYYY‑MM‑DD.log.

logHawk.py writes report_YYYY‑MM‑DD.txt to ~/Desktop/logHawk_analysis/
and prints its full path for easy emailing or SIEM ingestion.

## 📄 Sample Report

Number of occurrences of '404': 17
Number of occurrences of '500': 3
Sorted IP addresses (most common to least):
192.0.2.15 : 91
203.0.113.42 : 53
198.51.100.77 : 12
## 🚧 Roadmap
 Add email alert on critical findings (SMTP).

 Add alerts for critical findings.

 Parametric thresholds (--bf-threshold, --traffic-spike).

 Extend compatibility for Windows OS and Windows Task Scheduler.

🤝 Contributing
PRs and issue reports are welcome!

📜 License
Released under the MIT License — see LICENSE for full text.
Feel free to use, modify, and redistribute with attribution.

👤 Author
c0rds – cybersecurity student and enthusiast.
Say hi on GitHub or open an issue if LogHawk helps (or breaks) something!
