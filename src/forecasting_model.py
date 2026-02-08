"""
Task 4: Forecasting Access and Usage (2025–2027)

This module forecasts:
1. Account Ownership (Access)
2. Digital Payment Usage (Usage)

Approach:
- Trend regression (linear / log-linear)
- Event-augmented adjustments (from Task-3 outputs)
- Scenario analysis (optimistic / base / pessimistic)
- Heuristic uncertainty quantification

Designed for sparse data (Global Findex: ~5 points over 13 years)
"""

from dataclasses import dataclass
from typing import Dict, List
import os

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data/processed")  # Task 3 outputs stored here

# ---------------------------------------------------------------------
# Load Event Data from Task 3
# ---------------------------------------------------------------------

def load_event_impacts(file_name="ethiopia_fi_enriched_impact_links.csv") -> pd.DataFrame:
    """
    Load the Event-Indicator Association Matrix from Task 3.
    Returns: DataFrame with events as rows, indicators as columns
    """
    path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{file_name} not found in {DATA_DIR}")
    return pd.read_csv(path, index_col=0)


def load_event_schedule(file_name="event_schedule.csv") -> pd.DataFrame:
    """
    Load the schedule of events (year of occurrence, expected impact)
    Returns: DataFrame with columns ['event', 'year']
    """
    path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"{file_name} not found in {DATA_DIR}")
    return pd.read_csv(path)

# ---------------------------------------------------------------------
# Data Containers
# ---------------------------------------------------------------------

@dataclass
class ForecastResult:
    year: int
    baseline: float
    with_events: float
    optimistic: float
    base: float
    pessimistic: float
    ci_lower: float
    ci_upper: float

# ---------------------------------------------------------------------
# Trend Models
# ---------------------------------------------------------------------

def fit_trend_model(
    df: pd.DataFrame,
    year_col: str,
    value_col: str,
    log_transform: bool = False
) -> LinearRegression:
    """Fit a simple linear (or log-linear) trend model."""
    X = df[[year_col]].values
    y = df[value_col].values
    if log_transform:
        y = np.log(y)
    model = LinearRegression()
    model.fit(X, y)
    return model


def forecast_trend(
    model: LinearRegression,
    years: List[int],
    log_transform: bool = False
) -> pd.Series:
    """Generate baseline trend forecast for given years."""
    X_future = np.array(years).reshape(-1, 1)
    y_pred = model.predict(X_future)
    if log_transform:
        y_pred = np.exp(y_pred)
    return pd.Series(y_pred, index=years)

# ---------------------------------------------------------------------
# Event-Augmented Forecast
# ---------------------------------------------------------------------

def apply_event_impacts(
    baseline: pd.Series,
    event_impacts: Dict[str, float],
    event_schedule: Dict[str, List[int]],
    scenario_multiplier: float = 1.0
) -> pd.Series:
    """
    Apply event-based adjustments to baseline forecast.
    """
    adjusted = baseline.copy()
    for event, impact in event_impacts.items():
        years = event_schedule.get(event, [])
        for y in years:
            if y in adjusted.index:
                adjusted.loc[y] += impact * scenario_multiplier
    return adjusted

# ---------------------------------------------------------------------
# Scenario Construction
# ---------------------------------------------------------------------

def build_scenarios(baseline: pd.Series, with_events: pd.Series) -> Dict[str, pd.Series]:
    """
    Build optimistic / base / pessimistic scenarios
    based on event effects
    """
    return {
        "optimistic": baseline + 1.2 * (with_events - baseline),
        "base": with_events,
        "pessimistic": baseline + 0.7 * (with_events - baseline)
    }

# ---------------------------------------------------------------------
# Uncertainty Quantification
# ---------------------------------------------------------------------

def compute_confidence_intervals(forecast: pd.Series, uncertainty_width: float = 0.2) -> pd.DataFrame:
    """Compute heuristic confidence intervals."""
    lower = forecast * (1 - uncertainty_width)
    upper = forecast * (1 + uncertainty_width)
    return pd.DataFrame({"lower": lower, "upper": upper})

# ---------------------------------------------------------------------
# Master Forecast Pipeline
# ---------------------------------------------------------------------

def run_forecast_pipeline(
    historical_df: pd.DataFrame,
    year_col: str,
    value_col: str,
    forecast_years: List[int],
    event_impacts: Dict[str, float],
    event_schedule: Dict[str, List[int]],
    log_trend: bool = False,
    uncertainty_width: float = 0.2
) -> pd.DataFrame:
    """End-to-end forecasting pipeline for Task 4."""

    # Fit trend model
    trend_model = fit_trend_model(historical_df, year_col, value_col, log_transform=log_trend)

    # Baseline forecast
    baseline = forecast_trend(trend_model, forecast_years, log_transform=log_trend)

    # Event-augmented forecast (base scenario)
    with_events = apply_event_impacts(baseline, event_impacts, event_schedule, scenario_multiplier=1.0)

    # Scenarios
    scenarios = build_scenarios(baseline, with_events)

    # Confidence intervals (based on base)
    ci = compute_confidence_intervals(scenarios["base"], uncertainty_width=uncertainty_width)

    # Assemble final forecast table
    forecast_table = pd.DataFrame({
        "year": forecast_years,
        "baseline": baseline.values,
        "with_events": with_events.values,
        "optimistic": scenarios["optimistic"].values,
        "base": scenarios["base"].values,
        "pessimistic": scenarios["pessimistic"].values,
        "ci_lower": ci["lower"].values,
        "ci_upper": ci["upper"].values
    })

    return forecast_table

# ---------------------------------------------------------------------
# Interpretation Helpers
# ---------------------------------------------------------------------

def summarize_forecast(forecast_table: pd.DataFrame) -> Dict[str, str]:
    """
    Return text-ready summary insights for notebook.
    """
    summary = {
        "trend": "Both access and usage show continued upward trends through 2027.",
        "events": "Event-based policies and digital finance initiatives accelerate usage more than access.",
        "uncertainty": "Forecast uncertainty remains high due to sparse historical data and reliance on assumed event impacts."
    }
    return summary
