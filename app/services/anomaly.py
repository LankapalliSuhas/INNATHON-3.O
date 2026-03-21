from app.config import settings


def detect_anomalies(load1_power: float, load2_power: float, load1_current: float, load2_current: float):
    alerts = []

    if load1_current > settings.OVERCURRENT_THRESHOLD_A:
        alerts.append("Load 1 overcurrent detected")

    if load2_current > settings.OVERCURRENT_THRESHOLD_A:
        alerts.append("Load 2 overcurrent detected")

    if load1_power > settings.OVERPOWER_THRESHOLD_W:
        alerts.append("Load 1 overpower detected")

    if load2_power > settings.OVERPOWER_THRESHOLD_W:
        alerts.append("Load 2 overpower detected")

    if not alerts:
        return {
            "level": "INFO",
            "message": "System normal"
        }

    return {
        "level": "WARNING",
        "message": "; ".join(alerts)
    }