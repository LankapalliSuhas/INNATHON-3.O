from fastapi import APIRouter
from app.models.schemas import TelemetryPayload
from app.services.processor import process_telemetry
from app import state

router = APIRouter()

@router.post("/ingest")
def ingest(payload: TelemetryPayload):
    raw = payload.model_dump()
    frontend = process_telemetry(raw)

    state.latest_raw = raw
    state.latest_frontend = frontend

    state.history.append({
        "timestamp": frontend["timestamp"],
        "total_power_w": frontend["summary"]["total_power_w"],
        "current_bill_inr": frontend["billing"]["current_bill_inr"],
    })

    if len(state.history) > state.MAX_HISTORY:
        state.history.pop(0)

    state.latest_frontend["history"] = state.history

    return {
        "status": "ok",
        "message": "Telemetry received",
        "frontend_ready": True
    }