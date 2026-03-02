import hashlib
import argparse
import os
import json
from datetime import datetime

OUTPUT_DIR = "outputs"


def current_timestamp():
    return datetime.utcnow().isoformat()


def compute_hash(file_path, algorithm):
    h = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    hash_parser = subparsers.add_parser("hash")
    hash_parser.add_argument("--file", required=True)
    hash_parser.add_argument("--algo", required=True)

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("--file", required=True)
    verify_parser.add_argument("--algo", required=True)
    verify_parser.add_argument("--hash", required=True)

    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("--dir", required=True)
    report_parser.add_argument("--algo", required=True)

    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if args.command == "hash":
        print(compute_hash(args.file, args.algo))

    elif args.command == "verify":
        computed = compute_hash(args.file, args.algo)
        if computed == args.hash:
            print("MATCH")
        else:
            print("NOT MATCH")

    elif args.command == "report":
        report = []
        for filename in os.listdir(args.dir):
            path = os.path.join(args.dir, filename)
            if os.path.isfile(path):
                report.append({
                    "filename": filename,
                    "size": os.path.getsize(path),
                    "algorithm": args.algo,
                    "hash": compute_hash(path, args.algo),
                    "timestamp": current_timestamp()
                })

        with open(os.path.join(OUTPUT_DIR, "hashes_report.json"), "w") as f:
            json.dump(report, f, indent=4)


if __name__ == "__main__":
    main()