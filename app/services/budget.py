from calendar import monthrange
from datetime import datetime


def budget_analysis(current_bill: float, units_so_far: float, monthly_budget: float, timestamp: int):
    dt = datetime.fromtimestamp(timestamp)
    days_in_month = monthrange(dt.year, dt.month)[1]
    remaining_days = max(days_in_month - dt.day, 1)

    remaining_budget = max(monthly_budget - current_bill, 0.0)

    effective_rate = current_bill / units_so_far if units_so_far > 0 else 5.0
    safe_daily_budget = remaining_budget / remaining_days
    safe_daily_units = safe_daily_budget / effective_rate if effective_rate > 0 else 0.0

    progress_percent = (current_bill / monthly_budget * 100) if monthly_budget > 0 else 0

    if progress_percent < 70:
        status = "SAFE"
    elif progress_percent < 90:
        status = "WARNING"
    else:
        status = "RISK"

    return {
        "monthly_budget": round(monthly_budget, 2),
        "remaining_budget": round(remaining_budget, 2),
        "safe_daily_units": round(safe_daily_units, 4),
        "budget_status": status,
        "budget_progress_percent": round(progress_percent, 2)
    }