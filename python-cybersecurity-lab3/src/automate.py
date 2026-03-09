import argparse
import subprocess
import json
import os
import sys
from collections import Counter

OUTPUT_DIR = "outputs"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--ports", required=True)
    parser.add_argument("--scrape-source", required=True)
    parser.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    python_exec = sys.executable  # IMPORTANT: use current env python

    # 1. Run scanner
    subprocess.run([
        python_exec, "src/scanner.py",
        "--host", args.host,
        "--ports", args.ports
    ])

    # 2. Generate hash report for outputs/
    subprocess.run([
        python_exec, "src/crypto_tool.py",
        "report",
        "--dir", "outputs",
        "--algo", "sha256"
    ])

    # 3. Run scraper
    subprocess.run([
        python_exec, "src/scraper.py",
        "--source", args.scrape_source,
        "--limit", str(args.limit)
    ])

    # 4. Create summary.json
    summary = {}

    # Scan summary
    with open(os.path.join(OUTPUT_DIR, "scan_results.json")) as f:
        scan_data = json.load(f)

    open_ports = [p for p in scan_data if p["status"] == "open"]
    banners = [p["banner"] for p in open_ports if p["banner"]]
    top_banners = Counter(banners).most_common(3)

    summary["scan_summary"] = {
        "open_ports_count": len(open_ports),
        "top_banners": top_banners
    }

    # Hash summary
    with open(os.path.join(OUTPUT_DIR, "hashes_report.json")) as f:
        hash_data = json.load(f)

    summary["hash_summary"] = {
        "files_hashed": len(hash_data)
    }

    # Scraper summary
    with open(os.path.join(OUTPUT_DIR, "scraped_alerts.json")) as f:
        scrape_data = json.load(f)

    latest_title = scrape_data[0]["title"] if scrape_data else None

    summary["scraper_summary"] = {
        "advisories_collected": len(scrape_data),
        "latest_title": latest_title
    }

    with open(os.path.join(OUTPUT_DIR, "summary.json"), "w") as f:
        json.dump(summary, f, indent=4)


if __name__ == "__main__":
    main()