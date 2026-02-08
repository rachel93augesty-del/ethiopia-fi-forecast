# ============================================================
# Event Impact Modeling Module
# Task 3 – Ethiopia Financial Inclusion Forecast
# ============================================================

import pandas as pd
import numpy as np

# ============================================================
# 1. Load Processed Data
# ============================================================

def load_processed_data(impact_links_path, enriched_data_path):
    """
    Loads processed impact links and enriched indicator/event data.

    Returns:
    - events_df
    - indicators_df
    - impact_links_df
    """

    impact_links_df = pd.read_csv(impact_links_path)
    enriched_df = pd.read_csv(enriched_data_path)

    # Extract events
    events_df = (
        enriched_df[["record_id", "event_name", "event_date"]]
        .dropna(subset=["event_name"])
        .drop_duplicates()
        .rename(columns={"record_id": "parent_id"})
    )

    # Indicators time series
    indicators_df = enriched_df[
        ["indicator_code", "observation_date", "value_numeric"]
    ].dropna()

    return events_df, indicators_df, impact_links_df


# ============================================================
# 2. Prepare Impact Links (clean + enrich)
# ============================================================

def prepare_impact_links(impact_links_df, events_df):
    """
    Joins impact links with events and standardizes direction/magnitude.
    """

    df = impact_links_df.merge(
        events_df,
        on="parent_id",
        how="left"
    )

    # Direction to numeric sign
    df["direction_sign"] = df["impact_direction"].map(
        {"positive": 1, "negative": -1}
    ).fillna(1)

    # Final effect size
    df["effect"] = (
        df["direction_sign"]
        * df["impact_magnitude"].fillna(0)
    )

    df["lag_months"] = df["lag_months"].fillna(0).astype(int)

    return df


# ============================================================
# 3. Build Event–Indicator Association Matrix
# ============================================================

def build_association_matrix(impact_links_prepared):
    """
    Rows: Events
    Columns: Indicators
    Values: Estimated effect
    """

    matrix = (
        impact_links_prepared
        .pivot_table(
            index="event_name",
            columns="indicator_code",
            values="effect",
            aggfunc="sum",
            fill_value=0
        )
    )

    return matrix


# ============================================================
# 4. Apply Event Impacts Over Time
# ============================================================

def apply_event_impacts_over_time(
    indicators_df,
    impact_links_prepared,
    start_year=2015,
    end_year=2024
):
    """
    Simulates indicator evolution with event impacts.
    """

    years = list(range(start_year, end_year + 1))
    results = {}

    for indicator in indicators_df["indicator_code"].unique():
        base_series = (
            indicators_df[indicators_df["indicator_code"] == indicator]
            .groupby(indicators_df["observation_date"].str[:4])
            ["value_numeric"]
            .mean()
        )

        series = pd.Series(index=years, dtype=float)

        for year in years:
            series[year] = base_series.get(str(year), np.nan)

            impacts = impact_links_prepared[
                (impact_links_prepared["indicator_code"] == indicator)
            ]

            for _, row in impacts.iterrows():
                event_year = pd.to_datetime(row["event_date"]).year
                lagged_year = event_year + (row["lag_months"] // 12)

                if lagged_year == year:
                    series[year] += row["effect"]

        results[indicator] = series

    return pd.DataFrame(results)


# ============================================================
# 5. Validate Against Observed Data
# ============================================================

def validate_against_observed(simulated_df, indicators_df):
    """
    Compares simulated vs observed indicator values.
    """

    observed = (
        indicators_df
        .assign(year=indicators_df["observation_date"].str[:4].astype(int))
        .groupby(["indicator_code", "year"])["value_numeric"]
        .mean()
        .unstack(0)
    )

    comparison = simulated_df.subtract(observed, fill_value=0)

    return comparison


# ============================================================
# 6. Confidence Classification
# ============================================================

def classify_confidence(impact_links_prepared):
    """
    Assigns confidence labels to impact estimates.
    """

    def label(row):
        if row["confidence"] >= 0.8:
            return "High"
        elif row["confidence"] >= 0.5:
            return "Medium"
        else:
            return "Low"

    impact_links_prepared["confidence_level"] = impact_links_prepared.apply(
        label, axis=1
    )

    return impact_links_prepared


# ============================================================
# 7. Documentation Helper
# ============================================================

def methodology_notes():
    """
    Returns text describing modeling assumptions.
    """

    return {
        "functional_form": "Additive linear impact with lag",
        "assumptions": [
            "Event effects are additive",
            "Lag captured in months",
            "Comparable-country evidence used where local data missing"
        ],
        "limitations": [
            "No interaction effects",
            "No saturation constraints",
            "Annual aggregation smooths shocks"
        ]
    }
