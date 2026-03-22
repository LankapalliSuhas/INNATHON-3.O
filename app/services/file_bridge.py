import os
import json


FRONTEND_OUTPUT_DIR = "data/frontend_output"
FRONTEND_LIVE_FILE = os.path.join(FRONTEND_OUTPUT_DIR, "latest_frontend_payload.json")


def write_frontend_payload(payload: dict):
    os.makedirs(FRONTEND_OUTPUT_DIR, exist_ok=True)

    with open(FRONTEND_LIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)