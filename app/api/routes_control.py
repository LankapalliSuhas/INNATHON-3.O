from fastapi import APIRouter
from app.schemas import ControlCommand
import app.state as state

router = APIRouter()


@router.get("/control")
def get_control_state():
    return state.control_state


@router.post("/control")
def set_control_state(cmd: ControlCommand):
    state.control_state["relay1"] = cmd.relay1
    state.control_state["relay2"] = cmd.relay2
    state.control_state["buzzer"] = cmd.buzzer

    return {
        "status": "ok",
        "control_state": state.control_state
    }