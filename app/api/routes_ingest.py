from fastapi import APIRouter
from app.schemas import TelemetryInput
from app.services.processor import process_telemetry
from app.services.storage import append_telemetry
import app.state as state

router = APIRouter()


@router.post("/ingest")
def ingest_telemetry(payload: TelemetryInput):
    state.latest_raw_telemetry = payload.model_dump()

    frontend_payload = process_telemetry(payload)
    state.latest_frontend_payload = frontend_payload

    append_telemetry(payload)

    # sync recommended buzzer state into control state
    state.control_state["buzzer"] = frontend_payload["control"]["buzzer_should_be_on"]

    return {
        "status": "ok",
        "message": "Telemetry processed",
        "frontend_payload": frontend_payload
    }