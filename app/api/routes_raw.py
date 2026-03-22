from fastapi import APIRouter
from app import state

router = APIRouter()

@router.get("/raw")
def get_raw():
    if state.latest_raw is None:
        return {"status": "waiting", "message": "No ESP32 data yet"}
    return state.latest_raw