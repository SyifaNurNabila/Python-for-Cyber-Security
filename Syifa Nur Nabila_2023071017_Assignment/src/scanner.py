import socket
import argparse
import json
import os
import time
from common import setup_logging, current_timestamp, OUTPUT_DIR
import logging

DEFAULT_HOST = "127.0.0.1"
TIMEOUT = 0.3
def parse_ports(port_str):
    ports = []
    if "-" in port_str:
        start, end = port_str.split("-")
        ports = list(range(int(start), int(end) + 1))
    else:
        ports = [int(p) for p in port_str.split(",")]
    return ports


def scan_port(host, port):
    result = {
        "port": port,
        "status": None,
        "timestamp": current_timestamp(),
        "banner": None,
        "latency_ms": None
    }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(TIMEOUT)

    start = time.time()
    try:
        s.connect((host, port))
        latency = (time.time() - start) * 1000
        result["latency_ms"] = round(latency, 2)
        result["status"] = "open"

        # Banner grabbing
        if port == 80:
            s.sendall(b"GET / HTTP/1.0\r\n\r\n")
        if port != 443:
            try:
                banner = s.recv(1024)
                result["banner"] = banner.decode(errors="ignore").strip()
            except:
                pass

    except socket.timeout:
        result["status"] = "filtered/timeout"
    except:
        result["status"] = "closed"
    finally:
        s.close()

    return result


def main():
    setup_logging()

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--ports", required=True)

    args = parser.parse_args()
    host = args.host
    ports = parse_ports(args.ports)

    logging.info(f"Scanning {host} on ports {ports}")

    results = [scan_port(host, p) for p in ports]

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(OUTPUT_DIR, "scan_results.json")

    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)

    logging.info("Scan complete.")


if __name__ == "__main__":
    main()