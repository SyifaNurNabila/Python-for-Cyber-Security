import logging
import os
from datetime import datetime

OUTPUT_DIR = "outputs"

def setup_logging():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    log_file = os.path.join(OUTPUT_DIR, "run.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def current_timestamp():
    return datetime.utcnow().isoformat()