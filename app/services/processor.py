from app.config import settings
from app.services.billing import slab_bill, current_slab
from app.services.digital_twin import build_digital_twin

def process_telemetry(raw: dict) -> dict:
    load1 = raw["load1"]
    load2 = raw["load2"]

    loads = [
        {
            "id": "load1",
            "label": load1["label"],
            "type": load1["type"],
            "voltage_v": round(load1["voltage"], 2),
            "current_a": round(load1["current"], 3),
            "power_w": round(load1["power"], 2),
            "energy_kwh": round(load1["energy"], 6),
            "relay": raw["relay1"],
            "status": "ON" if raw["relay1"] and load1["power"] > 0 else "OFF"
        },
        {
            "id": "load2",
            "label": load2["label"],
            "type": load2["type"],
            "voltage_v": round(load2["voltage"], 2),
            "current_a": round(load2["current"], 3),
            "power_w": round(load2["power"], 2),
            "energy_kwh": round(load2["energy"], 6),
            "relay": raw["relay2"],
            "status": "ON" if raw["relay2"] and load2["power"] > 0 else "OFF"
        }
    ]

    total_power_w = round(load1["power"] + load2["power"], 2)
    total_energy_kwh = round(load1["energy"] + load2["energy"], 6)
    active_loads = sum(1 for x in loads if x["status"] == "ON")

    current_bill = slab_bill(total_energy_kwh)
    predicted_bill = round(current_bill * settings.PREDICTION_DAYS, 2)

    slab = current_slab(total_energy_kwh)

    used_percent = round((current_bill / settings.DEFAULT_MONTHLY_BUDGET) * 100, 2) if settings.DEFAULT_MONTHLY_BUDGET > 0 else 0

    if used_percent < 70:
        budget_status = "SAFE"
    elif used_percent < 100:
        budget_status = "WARNING"
    else:
        budget_status = "OVER"

    eco_score = max(0, 100 - int(total_power_w * 2))
    system_health = 100 if not raw["buzzer"] else 70

    recommendations = []
    if total_power_w > 15:
        recommendations.append("High power usage detected. Consider turning off one load.")
    if raw["buzzer"]:
        recommendations.append("Alert active. Check overload or unsafe condition.")
    if not recommendations:
        recommendations.append("System operating normally.")

    digital_twin = build_digital_twin(raw, loads, system_health)

    return {
        "status": "live",
        "summary": {
            "device_id": raw["device_id"],
            "timestamp": raw["timestamp"],
            "total_power_w": total_power_w,
            "total_energy_kwh": total_energy_kwh,
            "active_loads": active_loads,
            "relay1": raw["relay1"],
            "relay2": raw["relay2"],
            "buzzer": raw["buzzer"]
        },
        "loads": loads,
        "billing": {
            "current_bill_inr": current_bill,
            "predicted_bill_inr": predicted_bill,
            "current_slab": slab["current_slab"],
            "next_slab": slab["next_slab"]
        },
        "budget": {
            "monthly_budget_inr": settings.DEFAULT_MONTHLY_BUDGET,
            "used_percent": used_percent,
            "status": budget_status
        },
        "insights": {
            "eco_score": eco_score,
            "system_health": system_health,
            "recommendations": recommendations
        },
        "digital_twin": digital_twin
    }