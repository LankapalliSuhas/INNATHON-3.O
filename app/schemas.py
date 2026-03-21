from pydantic import BaseModel
from typing import List


class LoadInput(BaseModel):
    label: str
    type: str
    voltage: float
    current: float
    power: float
    energy: float  # MUST be cumulative kWh


class TelemetryInput(BaseModel):
    device_id: str
    timestamp: int
    relay1: bool
    relay2: bool
    buzzer: bool
    load1: LoadInput
    load2: LoadInput


class ControlCommand(BaseModel):
    relay1: bool
    relay2: bool
    buzzer: bool


class FrontendResponse(BaseModel):
    device_id: str
    timestamp: int
    live: dict
    loads: dict
    billing: dict
    prediction: dict
    budget: dict
    insights: dict
    recommendations: List[str]
    alerts: dict
    control: dict
    digital_twin: dict