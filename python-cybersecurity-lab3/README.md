# Lab 3 – Python for Cybersecurity

Name: Syifa Nur Nabila   
Course: Python for Cyber Security  

---

## Overview

This project demonstrates core cybersecurity concepts using Python:

- Socket Programming (Port scanning + Banner grabbing)
- Cryptography (Hashing and integrity verification)
- Web Scraping (Collecting vulnerability information from NVD)
- Automation (End-to-end workflow with logging)

All programs run locally using Python 3.x.

---

## Setup Instructions

1. Create virtual environment:
```
python -m venv env
```
2. Activate environment (Windows):
```
env\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
---

## How to Run Each Part

### Part A – Port Scanner

```
python src/scanner.py --host 127.0.0.1 --ports 1-100
```
Example:
python src/scanner.py --host 127.0.0.1 --ports 20-80

Output:
outputs/scan_results.json


---

### Part B – Cryptography (Hashing)

Generate hash report:
```
python src/crypto_tool.py report --dir outputs --algo sha256
```
Verify file integrity:

python src/crypto_tool.py verify --file outputs/scan_results.json --algo sha256 --hash <expected_hash>

Output:
outputs/hashes_report.json


---

### Part C – Web Scraping

Scrape vulnerability data from NVD:
```
python src/scraper.py --source nvd --limit 5
```
Output:
outputs/scraped_alerts.json

Note:
- Scraping follows responsible crawling practices.
- A delay (time.sleep) is implemented.
- Only public data is collected.


---

### Part D – Automation (Full Pipeline)

Run full workflow:
```
python src/automate.py --host 127.0.0.1 --ports 1-200 --scrape-source nvd --limit 5
```
This will:
1. Run port scanner
2. Generate hash report
3. Run scraper
4. Create summary.json
5. Log activity in outputs/run.log

Output files:
- scan_results.json
- hashes_report.json
- scraped_alerts.json
- summary.json
- run.log

---

## Folder Structure
```
Syifa Nur Nabila_2023071017_Assignment/
│
├── README.md
├── requirements.txt
│
├── src/
│   ├── scanner.py
│   ├── crypto_tool.py
│   ├── scraper.py
│   ├── automate.py
│
└── outputs/
    ├── scan_results.json
    ├── hashes_report.json
    ├── scraped_alerts.json
    ├── summary.json
    └── run.log
```