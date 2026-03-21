from app.config import settings


def slab_bill(units_kwh: float) -> float:
    remaining = units_kwh
    bill = 0.0
    prev_limit = 0.0

    for limit, rate in settings.TARIFF_SLABS:
        slab_units = min(remaining, limit - prev_limit)
        if slab_units > 0:
            bill += slab_units * rate
            remaining -= slab_units
        prev_limit = limit
        if remaining <= 0:
            break

    return round(bill, 2)


def current_slab(units_kwh: float):
    prev_limit = 0.0

    for i, (limit, rate) in enumerate(settings.TARIFF_SLABS):
        if units_kwh <= limit:
            next_slab = None
            if i + 1 < len(settings.TARIFF_SLABS):
                next_limit = settings.TARIFF_SLABS[i + 1][0]
                next_slab = f"{int(limit + 1)}-{int(next_limit)}"

            return {
                "current_slab": f"{int(prev_limit)}-{int(limit)}",
                "rate": rate,
                "next_slab": next_slab,
                "units_to_next_slab": None if next_slab is None else round(limit - units_kwh, 4)
            }

        prev_limit = limit

    return {
        "current_slab": "100+",
        "rate": settings.TARIFF_SLABS[-1][1],
        "next_slab": None,
        "units_to_next_slab": None
    }