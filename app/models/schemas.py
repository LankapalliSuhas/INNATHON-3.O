from pydantic import BaseModel

class LoadData(BaseModel):
    label: str
    type: str
    voltage: float
    current: float
    power: float
    energy: float

class TelemetryPayload(BaseModel):
    device_id: str
    timestamp: int
    relay1: bool
    relay2: bool
    buzzer: bool
    load1: LoadData
    load2: LoadData