from fastapi import APIRouter
import app.state as state

router = APIRouter()


@router.get("/frontend")
def get_frontend_payload():
    if not state.latest_frontend_payload:
        return {"message": "No telemetry yet"}
    return state.latest_frontend_payload