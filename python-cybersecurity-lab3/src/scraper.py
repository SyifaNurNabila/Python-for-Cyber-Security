import requests
import argparse
import json
import os
from datetime import datetime, UTC

OUTPUT_DIR = "outputs"


def scrape_nvd(limit):
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "resultsPerPage": limit
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    results = []

    vulnerabilities = data.get("vulnerabilities", [])

    for item in vulnerabilities[:limit]:
        cve = item.get("cve", {})
        cve_id = cve.get("id")

        descriptions = cve.get("descriptions", [])
        description_text = None
        for desc in descriptions:
            if desc.get("lang") == "en":
                description_text = desc.get("value")
                break

        results.append({
            "title": cve_id,
            "description": description_text,
            "date_scraped": datetime.now(UTC).isoformat(),
            "url": f"https://nvd.nist.gov/vuln/detail/{cve_id}"
        })

    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if args.source == "nvd":
        data = scrape_nvd(args.limit)
    else:
        print("Unsupported source")
        return

    with open(os.path.join(OUTPUT_DIR, "scraped_alerts.json"), "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()