from fastapi import APIRouter
from app.models.schemas import TelemetryPayload
from app.services.processor import process_telemetry
from app import state
import json

router = APIRouter()

@router.post("/ingest")
def ingest(payload: TelemetryPayload):
    raw = payload.model_dump()
    frontend = process_telemetry(raw)

    # Save in RAM
    state.latest_raw = raw
    state.latest_frontend = frontend

    # Save chart history
    state.history.append({
        "timestamp": frontend["summary"]["timestamp"],
        "total_power_w": frontend["summary"]["total_power_w"],
        "current_bill_inr": frontend["billing"]["current_bill_inr"],
    })

    if len(state.history) > state.MAX_HISTORY:
        state.history.pop(0)

    state.latest_frontend["history"] = state.history

    # =========================
    # TERMINAL VISUAL CONFIRMATION
    # =========================
    print("\n" + "=" * 70)
    print("✅ ESP32 DATA RECEIVED")
    print("=" * 70)

    print("\n📥 RAW JSON FROM ESP32:")
    print(json.dumps(raw, indent=2))

    print("\n⚙️ PROCESSED FRONTEND JSON:")
    print(json.dumps(frontend, indent=2))

    print("\n📊 QUICK SUMMARY:")
    print(f"Device ID        : {frontend['summary']['device_id']}")
    print(f"Timestamp        : {frontend['summary']['timestamp']}")
    print(f"Total Power      : {frontend['summary']['total_power_w']} W")
    print(f"Total Energy     : {frontend['summary']['total_energy_kwh']} kWh")
    print(f"Current Bill     : ₹{frontend['billing']['current_bill_inr']}")
    print(f"Predicted Bill   : ₹{frontend['billing']['predicted_bill_inr']}")
    print(f"Relay1           : {'ON' if frontend['summary']['relay1'] else 'OFF'}")
    print(f"Relay2           : {'ON' if frontend['summary']['relay2'] else 'OFF'}")
    print(f"Buzzer           : {'ON' if frontend['summary']['buzzer'] else 'OFF'}")
    print("=" * 70 + "\n")

    return {
        "status": "ok",
        "message": "Telemetry received",
        "frontend_ready": True
    }