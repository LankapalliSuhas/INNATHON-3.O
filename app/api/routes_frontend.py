from fastapi import APIRouter
from app import state

router = APIRouter()

@router.get("/frontend")
def get_frontend():
    if state.latest_frontend is None:
        return {
            "status": "waiting",
            "message": "No processed data yet",
            "summary": {
                "device_id": "esp32_01",
                "timestamp": 0,
                "total_power_w": 0,
                "total_energy_kwh": 0,
                "active_loads": 0,
                "relay1": False,
                "relay2": False,
                "buzzer": False
            },
            "loads": [],
            "billing": {
                "current_bill_inr": 0,
                "predicted_bill_inr": 0,
                "current_slab": "0-50",
                "next_slab": "51-100"
            },
            "budget": {
                "monthly_budget_inr": 500,
                "used_percent": 0,
                "status": "SAFE"
            },
            "insights": {
                "eco_score": 100,
                "system_health": 100,
                "recommendations": ["Waiting for live ESP32 data"]
            },
            "digital_twin": {
                "device_state": "IDLE",
                "relay1_state": "OFF",
                "relay2_state": "OFF",
                "buzzer_state": "OFF",
                "components": []
            },
            "history": []
        }
    return state.latest_frontend