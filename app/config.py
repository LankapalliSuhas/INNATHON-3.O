from pydantic import BaseModel
from typing import ClassVar

class Settings(BaseModel):
    DEFAULT_MONTHLY_BUDGET: float = 500.0
    PREDICTION_DAYS: int = 30

    TARIFF_SLABS: ClassVar[list[tuple[int, float]]] = [
        (50, 5.0),
        (100, 6.0),
        (999999, 8.0),
    ]

settings = Settings()