def build_digital_twin(raw: dict, loads: list, system_health: int):
    relay1_state = "ON" if raw["relay1"] else "OFF"
    relay2_state = "ON" if raw["relay2"] else "OFF"
    buzzer_state = "ON" if raw["buzzer"] else "OFF"

    device_state = "ACTIVE"
    if not raw["relay1"] and not raw["relay2"]:
        device_state = "IDLE"

    components = []
    for idx, load in enumerate(loads, start=1):
        components.append({
            "id": f"load{idx}",
            "label": load["label"],
            "type": load["type"],
            "state": "ON" if load["power_w"] > 0 else "OFF",
            "voltage_v": load["voltage_v"],
            "current_a": load["current_a"],
            "power_w": load["power_w"],
            "energy_kwh": load["energy_kwh"],
        })

    return {
        "device_state": device_state,
        "relay1_state": relay1_state,
        "relay2_state": relay2_state,
        "buzzer_state": buzzer_state,
        "system_health": system_health,
        "components": components
    }