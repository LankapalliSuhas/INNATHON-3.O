import time
from app.config import settings
from app.services.billing import slab_bill, current_slab
from app.services.prediction import predict_month_end
from app.services.budget import budget_analysis
from app.services.recommendations import generate_recommendations
from app.services.eco_score import calculate_eco_score
from app.services.anomaly import detect_anomalies


def normalize_timestamp(ts: int) -> int:
    """
    If ESP32 sends an invalid/non-unix timestamp (like millis()/1000 since boot),
    replace it with server unix time.
    """
    if ts < 1700000000:
        return int(time.time())
    return ts


def process_telemetry(t):
    # Normalize timestamp for real backend logic
    safe_timestamp = normalize_timestamp(t.timestamp)

    # Per-load status
    load1_status = "ON" if t.relay1 and t.load1.power > 0.1 else "OFF"
    load2_status = "ON" if t.relay2 and t.load2.power > 0.1 else "OFF"

    # Total values
    total_power = round(max(t.load1.power, 0) + max(t.load2.power, 0), 4)
    total_voltage_avg = round((max(t.load1.voltage, 0) + max(t.load2.voltage, 0)) / 2, 4)

    # Energy is assumed cumulative kWh from ESP32
    units_month = round(max(t.load1.energy, 0) + max(t.load2.energy, 0), 6)

    # Billing
    current_bill = slab_bill(units_month)
    slab_info = current_slab(units_month)
    effective_rate = round(current_bill / units_month, 4) if units_month > 0 else 5.0

    # Prediction
    pred = predict_month_end(units_month, safe_timestamp)

    # Budget
    budget = budget_analysis(
        current_bill=current_bill,
        units_so_far=units_month,
        monthly_budget=settings.DEFAULT_MONTHLY_BUDGET,
        timestamp=safe_timestamp
    )

    # Eco score
    eco_score, eco_badge = calculate_eco_score(
        total_power=total_power,
        budget_status=budget["budget_status"],
        predicted_bill=pred["predicted_month_bill"],
        monthly_budget=budget["monthly_budget"]
    )

    # Alerts
    alerts = detect_anomalies(
        t.load1.power, t.load2.power,
        t.load1.current, t.load2.current
    )

    # Recommendations
    recommendations = generate_recommendations(
        total_power=total_power,
        budget_status=budget["budget_status"],
        predicted_bill=pred["predicted_month_bill"],
        monthly_budget=budget["monthly_budget"],
        units_to_next_slab=slab_info["units_to_next_slab"]
    )

    # Auto control suggestions
    buzzer_should_be_on = alerts["level"] != "INFO"

    recommended_action_load1 = "KEEP_ON"
    recommended_action_load2 = "KEEP_ON"

    if budget["budget_status"] == "RISK" or total_power > settings.OVERPOWER_THRESHOLD_W:
        # Prefer shedding second load first
        recommended_action_load2 = "TURN_OFF"

    # ===== DIGITAL TWIN BLOCK =====
    digital_twin = {
        "board_status": "ACTIVE",
        "last_sync": safe_timestamp,
        "components": {
            "load1": {
                "name": t.load1.label,
                "type": t.load1.type,
                "visual_state": load1_status,
                "relay_linked": t.relay1
            },
            "load2": {
                "name": t.load2.label,
                "type": t.load2.type,
                "visual_state": load2_status,
                "relay_linked": t.relay2
            },
            "relay1": {
                "name": "Relay 1",
                "state": "ON" if t.relay1 else "OFF"
            },
            "relay2": {
                "name": "Relay 2",
                "state": "ON" if t.relay2 else "OFF"
            },
            "buzzer": {
                "name": "Buzzer",
                "state": "ON" if t.buzzer else "OFF",
                "recommended_state": "ON" if buzzer_should_be_on else "OFF"
            }
        },
        "twin_metrics": {
            "total_power": total_power,
            "total_voltage_avg": total_voltage_avg,
            "system_health": "HEALTHY" if alerts["level"] == "INFO" else "ATTENTION"
        }
    }

    # ===== FINAL FRONTEND PAYLOAD =====
    frontend_payload = {
        "device_id": t.device_id,
        "timestamp": safe_timestamp,
        "live": {
            "total_voltage_avg": total_voltage_avg,
            "total_power": total_power,
            "relay1": t.relay1,
            "relay2": t.relay2,
            "buzzer": t.buzzer
        },
        "loads": {
            "load1": {
                "label": t.load1.label,
                "type": t.load1.type,
                "voltage": round(max(t.load1.voltage, 0), 3),
                "current": round(max(t.load1.current, 0), 3),
                "power": round(max(t.load1.power, 0), 3),
                "energy_kwh": round(max(t.load1.energy, 0), 6),
                "status": load1_status
            },
            "load2": {
                "label": t.load2.label,
                "type": t.load2.type,
                "voltage": round(max(t.load2.voltage, 0), 3),
                "current": round(max(t.load2.current, 0), 3),
                "power": round(max(t.load2.power, 0), 3),
                "energy_kwh": round(max(t.load2.energy, 0), 6),
                "status": load2_status
            }
        },
        "billing": {
            "units_month": units_month,
            "current_bill": current_bill,
            "effective_rate": effective_rate,
            "current_slab": slab_info["current_slab"],
            "next_slab": slab_info["next_slab"],
            "units_to_next_slab": slab_info["units_to_next_slab"]
        },
        "prediction": pred,
        "budget": budget,
        "insights": {
            "peak_window": "Learning...",
            "peak_avg_power": total_power,
            "eco_score": eco_score,
            "eco_badge": eco_badge
        },
        "recommendations": recommendations,
        "alerts": alerts,
        "control": {
            "auto_mode_enabled": settings.AUTO_MODE_ENABLED,
            "recommended_action_load1": recommended_action_load1,
            "recommended_action_load2": recommended_action_load2,
            "buzzer_should_be_on": buzzer_should_be_on
        },
        "digital_twin": digital_twin
    }

    return frontend_payload