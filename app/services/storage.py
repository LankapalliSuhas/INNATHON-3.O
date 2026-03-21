import csv
import os

LOG_FILE = "data/telemetry_log.csv"

HEADERS = [
    "device_id", "timestamp",
    "relay1", "relay2", "buzzer",
    "load1_label", "load1_type", "load1_voltage", "load1_current", "load1_power", "load1_energy",
    "load2_label", "load2_type", "load2_voltage", "load2_current", "load2_power", "load2_energy"
]


def ensure_log_file():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)


def append_telemetry(t):
    ensure_log_file()
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            t.device_id, t.timestamp,
            t.relay1, t.relay2, t.buzzer,
            t.load1.label, t.load1.type, t.load1.voltage, t.load1.current, t.load1.power, t.load1.energy,
            t.load2.label, t.load2.type, t.load2.voltage, t.load2.current, t.load2.power, t.load2.energy
        ])