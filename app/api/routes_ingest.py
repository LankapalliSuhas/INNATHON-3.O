from fastapi import APIRouter
from app.schemas import TelemetryInput
from app.services.processor import process_telemetry
from app.services.storage import append_telemetry
from app.services.file_bridge import write_frontend_payload
import app.state as state

router = APIRouter()


@router.post("/ingest")
def ingest_telemetry(payload: TelemetryInput):
    # Save raw telemetry in runtime memory
    state.latest_raw_telemetry = payload.model_dump()

    # Process telemetry into frontend-ready digital twin payload
    frontend_payload = process_telemetry(payload)

    # Save latest processed payload in runtime memory
    state.latest_frontend_payload = frontend_payload

    # Append CSV telemetry log
    append_telemetry(payload)

    # Write latest processed payload to file for frontend dev fallback
    write_frontend_payload(frontend_payload)

    # Sync recommended buzzer state into control state
    state.control_state["buzzer"] = frontend_payload["control"]["buzzer_should_be_on"]

    return {
        "status": "ok",
        "message": "Telemetry processed",
        "frontend_payload": frontend_payload
    }