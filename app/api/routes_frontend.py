from fastapi import APIRouter
import app.state as state

router = APIRouter()


@router.get("/frontend")
def get_frontend_payload():
    """
    Main endpoint for frontend developer.
    Returns processed digital twin payload.
    """
    if not state.latest_frontend_payload:
        return {"message": "No telemetry yet"}
    return state.latest_frontend_payload


@router.get("/raw")
def get_raw_payload():
    """
    Debug endpoint for backend/hardware testing.
    Returns latest raw ESP32 telemetry.
    """
    if not state.latest_raw_telemetry:
        return {"message": "No raw telemetry yet"}
    return state.latest_raw_telemetry