from calendar import monthrange
from datetime import datetime
from app.services.billing import slab_bill


def predict_month_end(units_so_far: float, timestamp: int):
    dt = datetime.fromtimestamp(timestamp)
    day = max(dt.day, 1)
    days_in_month = monthrange(dt.year, dt.month)[1]

    avg_daily = units_so_far / day
    predicted_units = avg_daily * days_in_month
    predicted_bill = slab_bill(predicted_units)

    # Eco mode assumption = 20% reduction
    eco_units = predicted_units * 0.8
    eco_bill = slab_bill(eco_units)

    return {
        "predicted_month_units": round(predicted_units, 4),
        "predicted_month_bill": round(predicted_bill, 2),
        "eco_mode_predicted_bill": round(eco_bill, 2),
        "potential_savings": round(predicted_bill - eco_bill, 2)
    }