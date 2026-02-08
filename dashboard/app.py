# dashboard/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import Task-4 forecasting functions
from src.forecasting_model import run_forecast_pipeline  

# -------------------------
# Project Root and Data Files
# -------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
HISTORICAL_FILE = PROJECT_ROOT / "data" / "processed" / "ethiopia_fi_enriched_data.csv"
EVENTS_FILE = PROJECT_ROOT / "data" / "processed" / "ethiopia_fi_enriched_impact_links.csv"

# -------------------------
# Page Title
# -------------------------
st.set_page_config(page_title="Ethiopia Financial Inclusion Dashboard", layout="wide")
st.title("🇪🇹 Ethiopia Financial Inclusion Dashboard")
st.markdown(
    "Interactive dashboard to explore historical trends, event impacts, financial inclusion progress, and forecasts."
)

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    try:
        historical_df = pd.read_csv(HISTORICAL_FILE)
    except FileNotFoundError:
        st.error(f"❌ Data file not found: {HISTORICAL_FILE}")
        return None, None

    try:
        event_df = pd.read_csv(EVENTS_FILE)
    except FileNotFoundError:
        st.warning(f"⚠️ Event impacts file not found: {EVENTS_FILE}")
        event_df = pd.DataFrame()

    # Ensure numeric columns
    historical_df['value_numeric'] = pd.to_numeric(historical_df['value_numeric'], errors='coerce')
    historical_df['fiscal_year'] = pd.to_numeric(historical_df['fiscal_year'], errors='coerce')

    return historical_df, event_df

historical_df, event_df = load_data()
if historical_df is None:
    st.stop()  # Stop execution if essential data is missing

# -------------------------
# Sidebar: Page Selection
# -------------------------
page = st.sidebar.selectbox(
    "Select Dashboard Page",
    ["Overview", "Trends", "Forecasts", "Inclusion Projections"]
)

# -------------------------
# 1. Overview Page
# -------------------------
if page == "Overview":
    st.header("Overview of Key Metrics")

    latest_year = historical_df['fiscal_year'].max()
    latest_data = historical_df[historical_df['fiscal_year'] == latest_year]

    col1, col2, col3 = st.columns(3)
    with col1:
        acc_ownership = latest_data[latest_data['indicator'] == "Account Ownership Rate"]['value_numeric'].mean()
        st.metric("Account Ownership Rate (%)", f"{acc_ownership:.1f}")
    with col2:
        digital_usage = latest_data[latest_data['indicator'] == "Mobile Money Activity Rate"]['value_numeric'].mean()
        st.metric("Mobile Money Usage (%)", f"{digital_usage:.1f}")
    with col3:
        crossover = latest_data[latest_data['indicator'] == "P2P/ATM Crossover Ratio"]['value_numeric'].mean()
        st.metric("P2P/ATM Crossover Ratio", f"{crossover:.2f}")

    st.markdown("---")
    st.subheader("Event Impacts")
    if not event_df.empty:
        st.dataframe(event_df)
        # Download event data
        csv = event_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Event Data as CSV",
            data=csv,
            file_name='event_impacts.csv',
            mime='text/csv'
        )
    else:
        st.info("No event impacts data available.")

# -------------------------
# 2. Trends Page
# -------------------------
elif page == "Trends":
    st.header("Trends Over Time")
    indicators = historical_df['indicator'].unique()
    selected_indicator = st.selectbox("Select Indicator", indicators)

    indicator_data = historical_df[historical_df['indicator'] == selected_indicator]

    fig = px.line(
        indicator_data,
        x="fiscal_year",
        y="value_numeric",
        title=f"{selected_indicator} Over Time",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # Download button
    csv = indicator_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"Download {selected_indicator} Data as CSV",
        data=csv,
        file_name=f'{selected_indicator}_historical.csv',
        mime='text/csv'
    )

# -------------------------
# 3. Forecasts Page
# -------------------------
elif page == "Forecasts":
    st.header("Financial Inclusion Forecasts")
    st.markdown("Baseline trend, event-augmented forecast, and scenario ranges.")

    targets = {
        "access": "Account Ownership Rate",
        "usage": "Mobile Money Activity Rate"
    }

    forecast_years = [2025, 2026, 2027]
    event_impacts = {}  # replace with Task-3 outputs if available
    event_schedule = {}

    for key, indicator_name in targets.items():
        indicator_df = historical_df[historical_df['indicator'] == indicator_name]
        historical_values = (
            indicator_df.groupby('fiscal_year')['value_numeric']
            .mean()
            .reset_index()
            .rename(columns={'fiscal_year': 'year', 'value_numeric': 'value'})
        )
        if historical_values.empty:
            st.warning(f"No historical data found for {indicator_name}. Skipping forecast.")
            continue

        forecast_table = run_forecast_pipeline(
            historical_df=historical_values,
            year_col='year',
            value_col='value',
            forecast_years=forecast_years,
            event_impacts=event_impacts,
            event_schedule=event_schedule,
            log_trend=False,
            uncertainty_width=0.2
        )

        st.subheader(f"Forecast for {indicator_name}")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=forecast_table['year'],
            y=forecast_table['baseline'],
            mode='lines+markers',
            name='Baseline'
        ))
        fig.add_trace(go.Scatter(
            x=forecast_table['year'],
            y=forecast_table['optimistic'],
            mode='lines+markers',
            name='Optimistic'
        ))
        fig.add_trace(go.Scatter(
            x=forecast_table['year'],
            y=forecast_table['pessimistic'],
            mode='lines+markers',
            name='Pessimistic'
        ))
        fig.add_trace(go.Scatter(
            x=list(forecast_table['year']) + list(forecast_table['year'])[::-1],
            y=list(forecast_table['ci_upper']) + list(forecast_table['ci_lower'])[::-1],
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=True,
            name='Confidence Interval'
        ))

        st.plotly_chart(fig, use_container_width=True)

        # Download forecast table
        csv = forecast_table.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"Download {indicator_name} Forecast as CSV",
            data=csv,
            file_name=f'{indicator_name}_forecast.csv',
            mime='text/csv'
        )

# -------------------------
# 4. Inclusion Projections Page
# -------------------------
elif page == "Inclusion Projections":
    st.header("Financial Inclusion Rate Projections")
    indicator_name = "Account Ownership Rate"
    indicator_df = historical_df[historical_df['indicator'] == indicator_name]
    historical_values = (
        indicator_df.groupby('fiscal_year')['value_numeric']
        .mean()
        .reset_index()
        .rename(columns={'fiscal_year': 'year', 'value_numeric': 'value'})
    )

    forecast_years = [2025, 2026, 2027]
    forecast_table = run_forecast_pipeline(
        historical_df=historical_values,
        year_col='year',
        value_col='value',
        forecast_years=forecast_years,
        event_impacts={},
        event_schedule={},
        log_trend=False,
        uncertainty_width=0.2
    )

    scenario = st.radio("Select Scenario", ["Base", "Optimistic", "Pessimistic"])
    scenario_col = scenario.lower() if scenario != "Base" else "base"

    fig = px.line(
        forecast_table,
        x="year",
        y=scenario_col,
        title=f"{indicator_name} Forecast - {scenario} Scenario",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # Progress toward 60% target
    forecast_table["target_progress"] = forecast_table[scenario_col] / 60 * 100
    st.bar_chart(forecast_table.set_index("year")["target_progress"])

    # Download scenario forecast
    csv = forecast_table.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"Download {indicator_name} {scenario} Scenario Forecast as CSV",
        data=csv,
        file_name=f'{indicator_name}_{scenario}_forecast.csv',
        mime='text/csv'
    )
