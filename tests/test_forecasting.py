import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.forecasting_model import run_forecast_pipeline

# -------------------------------
# 1. Mock historical Findex data
# -------------------------------
historical_access = pd.DataFrame({
    "year": [2011, 2014, 2017, 2021, 2024],
    "access_rate": [22.0, 26.0, 35.0, 46.0, 49.0]
})

historical_usage = pd.DataFrame({
    "year": [2011, 2014, 2017, 2021, 2024],
    "usage_rate": [3.0, 4.0, 6.0, 4.7, 9.45]
})

# -------------------------------
# 2. Event impacts from Task-3
# -------------------------------
event_impacts = {
    "Digital Payment Policy Expansion 2025": 1.5,
    "4G Tower Deployment 2025": 0.5
}

event_schedule = {
    "Digital Payment Policy Expansion 2025": [2025, 2026, 2027],
    "4G Tower Deployment 2025": [2026, 2027]
}

forecast_years = [2025, 2026, 2027]

# -------------------------------
# 3. Run ACCESS forecast
# -------------------------------
access_forecast = run_forecast_pipeline(
    historical_df=historical_access,
    year_col="year",
    value_col="access_rate",
    forecast_years=forecast_years,
    event_impacts=event_impacts,
    event_schedule=event_schedule,
    log_trend=False,
    uncertainty_width=0.15
)

print("\n=== ACCESS FORECAST ===")
print(access_forecast)

# -------------------------------
# 4. Run USAGE forecast
# -------------------------------
usage_forecast = run_forecast_pipeline(
    historical_df=historical_usage,
    year_col="year",
    value_col="usage_rate",
    forecast_years=forecast_years,
    event_impacts=event_impacts,
    event_schedule=event_schedule,
    log_trend=True,   # usage often grows non-linearly
    uncertainty_width=0.25
)

print("\n=== USAGE FORECAST ===")
print(usage_forecast)
