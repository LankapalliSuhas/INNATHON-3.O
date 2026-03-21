class Settings:
    APP_NAME = "VoltWise Backend"
    DEFAULT_MONTHLY_BUDGET = 100.0
    DEFAULT_TARIFF = "demo_dc"
    AUTO_MODE_ENABLED = True

    # Thresholds for alerts / auto control
    OVERCURRENT_THRESHOLD_A = 1.5
    OVERPOWER_THRESHOLD_W = 25.0

    # Demo slab config (can later replace with real Telangana slab)
    # Format: (upper_limit_kwh, rate_per_unit)
    TARIFF_SLABS = [
        (50, 5.0),
        (100, 6.0),
        (999999, 8.0)
    ]


settings = Settings()