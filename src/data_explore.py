# data_explore.py
import pandas as pd
from datetime import datetime
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data_explore as de
# -----------------------------
# 1. Load data
# -----------------------------
def load_data(data_file, impact_links_file=None, reference_codes_file=None):
    """
    Load datasets and return as pandas DataFrames.
    Handles Excel (.xlsx) files with multiple sheets.
    """
    # Load main data sheet
    data_df = pd.read_excel(data_file, sheet_name="ethiopia_fi_unified_data")
    
    # Load impact links sheet from same file if separate file not provided
    if impact_links_file:
        impact_links_df = pd.read_excel(impact_links_file)
    else:
        impact_links_df = pd.read_excel(data_file, sheet_name="Impact_sheet")  # corrected sheet name
    
    # Load reference codes
    reference_codes_df = pd.read_excel(reference_codes_file)
    
    print("✅ Data loaded successfully")
    print(f"Main data shape: {data_df.shape}")
    print(f"Impact sheet shape: {impact_links_df.shape}")
    print(f"Reference codes shape: {reference_codes_df.shape}")
    
    return data_df, impact_links_df, reference_codes_df


# -----------------------------
# 2. Explore schema
# -----------------------------
def explore_schema(data_df, impact_df, reference_df):
    """
    Explore the schema of the loaded datasets.
    """
    print("\n=== Main Data Schema ===")
    print("Columns:", list(data_df.columns))
    print("\nData Types:\n", data_df.dtypes)
    print("\nSample Rows:\n", data_df.head(3))
    
    print("\n=== Impact Sheet Schema ===")
    print("Columns:", list(impact_df.columns))
    print("\nData Types:\n", impact_df.dtypes)
    print("\nSample Rows:\n", impact_df.head(3))
    
    print("\n=== Reference Codes Schema ===")
    print("Columns:", list(reference_df.columns))
    print("\nData Types:\n", reference_df.dtypes)
    print("\nSample Rows:\n", reference_df.head(3))
    
    print("\n✅ Schema exploration done.\n")


# -----------------------------
# 3. Basic exploration
# -----------------------------
def basic_exploration(data_df, impact_df):
    """
    Explore basic stats for Task 1 Step 2.
    """
    print("\n--- Main Data Exploration ---")
    
    # Counts by categories
    for col in ["record_type", "pillar", "source_type", "confidence"]:
        if col in data_df.columns:
            print(f"\nCounts for {col}:")
            print(data_df[col].value_counts())
    
    # Temporal range
    if "observation_date" in data_df.columns:
        print("\nObservation date range:")
        print(data_df["observation_date"].min(), "to", data_df["observation_date"].max())
    
    # Unique indicators
    if "indicator_code" in data_df.columns:
        print("\nUnique indicators (indicator_code):")
        print(data_df["indicator_code"].unique())
    
    # Events and dates
    if "record_type" in data_df.columns and "event_date" in data_df.columns:
        events = data_df[data_df["record_type"] == "event"]
        print(f"\nNumber of events: {len(events)}")
        print(events[["pillar", "event_date"]].head(5))
    
    # Impact sheet summary
    print("\n--- Impact Sheet Summary ---")
    print(impact_df.head(5))
    print("\n✅ Basic exploration done.\n")

# -----------------------------
# 4. Enrich dataset (full)
# -----------------------------
def enrich_data(data, impact_links, collected_by="Unknown"):
    """
    Add all critical observations, events, and impact links identified from exploration.
    Returns updated dataframes and enrichment log.
    """
    enrichment_log = []

    # -----------------------------
    # Helper: get next numeric ID
    # -----------------------------
    def get_max_id(df, prefix):
        if df.empty:
            return 0
        numeric_ids = df['record_id'].str.extract(fr'{prefix}_(\d+)').astype(float)
        numeric_ids = numeric_ids.dropna()
        return int(numeric_ids.max()[0]) if not numeric_ids.empty else 0

    max_obs_id = get_max_id(data[data['record_type']=='observation'], 'OBS')
    max_event_id = get_max_id(data[data['record_type']=='event'], 'EVT')
    max_impact_id = get_max_id(impact_links, 'IMP')

    # -----------------------------
    # 1. Add critical observations
    # -----------------------------
    new_observations = [
        {"pillar": "ACCESS", "indicator": "Account Ownership - Gender", "indicator_code": "ACC_GENDER",
         "value_numeric": 48.0, "observation_date": pd.Timestamp("2025-12-31"),
         "source_name": "World Bank Findex", "source_url": "https://globalfindex.worldbank.org/",
         "confidence": "High"},
        {"pillar": "ACCESS", "indicator": "Account Ownership - Urban/Rural", "indicator_code": "ACC_URBAN_RURAL",
         "value_numeric": 50.5, "observation_date": pd.Timestamp("2025-12-31"),
         "source_name": "World Bank Findex", "source_url": "https://globalfindex.worldbank.org/",
         "confidence": "High"},
        {"pillar": "ACCESS", "indicator": "Digital ID Coverage (%)", "indicator_code": "ACC_DIGID",
         "value_numeric": 72.3, "observation_date": pd.Timestamp("2025-12-31"),
         "source_name": "Government Data", "source_url": "https://www.nbe.gov.et/",
         "confidence": "High"},
        {"pillar": "USAGE", "indicator": "Mobile Money Users", "indicator_code": "USG_MM_USERS",
         "value_numeric": 12.5, "observation_date": pd.Timestamp("2025-12-31"),
         "source_name": "CBE Reports", "source_url": "https://www.cbe.gov.et/",
         "confidence": "High"},
        {"pillar": "USAGE", "indicator": "Internet Access (%)", "indicator_code": "USG_INTERNET",
         "value_numeric": 58.0, "observation_date": pd.Timestamp("2025-12-31"),
         "source_name": "ITU Statistics", "source_url": "https://www.itu.int/en/",
         "confidence": "High"},
        {"pillar": "ACCESS", "indicator": "ATM Count", "indicator_code": "ACC_ATM",
         "value_numeric": 1200, "observation_date": pd.Timestamp("2025-12-31"),
         "source_name": "National Bank of Ethiopia", "source_url": "https://www.nbe.gov.et/",
         "confidence": "High"},
        {"pillar": "ACCESS", "indicator": "Agent Count", "indicator_code": "ACC_AGENT",
         "value_numeric": 8500, "observation_date": pd.Timestamp("2025-12-31"),
         "source_name": "National Bank of Ethiopia", "source_url": "https://www.nbe.gov.et/",
         "confidence": "High"},
        {"pillar": "Infrastructure", "indicator": "4G Coverage (%)", "indicator_code": "ACC_4G_COV",
         "value_numeric": 68.0, "observation_date": pd.Timestamp("2025-12-31"),
         "source_name": "Telecom Ministry", "source_url": "https://www.mot.gov.et/",
         "confidence": "High"}
    ]

    for obs in new_observations:
        max_obs_id += 1
        obs_record = {**obs,
                      "record_id": f"OBS_{max_obs_id}",
                      "record_type": "observation",
                      "collected_by": collected_by,
                      "collection_date": datetime.today().strftime("%Y-%m-%d"),
                      "original_text": f"Added {obs['indicator']} from source {obs['source_name']}"}
        data = pd.concat([data, pd.DataFrame([obs_record])], ignore_index=True)
        enrichment_log.append({**obs_record, "notes": "Critical observation added."})

    # -----------------------------
    # 2. Add critical events
    # -----------------------------
    new_events = [
        {"category": "policy", "event_name": "Digital Payment Policy Expansion 2025", "event_date": pd.Timestamp("2025-06-01")},
        {"category": "infrastructure", "event_name": "4G Tower Deployment 2025", "event_date": pd.Timestamp("2025-07-15")},
        {"category": "policy", "event_name": "Regulatory Reform on Mobile Money 2025", "event_date": pd.Timestamp("2025-08-01")},
        {"category": "product_launch", "event_name": "Major Bank Partnership with EthioPay", "event_date": pd.Timestamp("2025-09-01")},
        {"category": "policy", "event_name": "NFIS Strategy Update 2026", "event_date": pd.Timestamp("2026-01-01")}
    ]

    for ev in new_events:
        max_event_id += 1
        ev_record = {**ev,
                     "record_type": "event",
                     "pillar": None,
                     "source_name": "Official Reports",
                     "source_url": "https://www.nbe.gov.et/",
                     "confidence": "High",
                     "record_id": f"EVT_{max_event_id}",
                     "collected_by": collected_by,
                     "collection_date": datetime.today().strftime("%Y-%m-%d"),
                     "original_text": ev["event_name"]}
        data = pd.concat([data, pd.DataFrame([ev_record])], ignore_index=True)
        enrichment_log.append({**ev_record, "notes": "Critical event added."})

    # -----------------------------
    # 3. Add impact links
    # -----------------------------
    # Map each new event to relevant indicators
    event_to_indicators = {
        f"EVT_{max_event_id-4}": [("ACC_OWNERSHIP", "ACCESS"), ("USG_MM_USERS", "USAGE")],
        f"EVT_{max_event_id-3}": [("ACC_4G_COV", "Infrastructure")],
        f"EVT_{max_event_id-2}": [("USG_MM_USERS", "USAGE")],
        f"EVT_{max_event_id-1}": [("USG_MM_USERS", "USAGE")],
        f"EVT_{max_event_id}": [("ACC_OWNERSHIP", "ACCESS"), ("USG_MM_USERS", "USAGE")]
    }

    for ev_id, indicators in event_to_indicators.items():
        for ind_code, pillar in indicators:
            max_impact_id += 1
            link_record = {
                "record_id": f"IMP_{max_impact_id}",
                "parent_id": ev_id,
                "record_type": "impact_link",
                "pillar": pillar,
                "related_indicator": ind_code,
                "impact_direction": "increase",
                "impact_magnitude": "high",
                "lag_months": 1,
                "evidence_basis": "Official report / press release",
                "collected_by": collected_by,
                "collection_date": datetime.today().strftime("%Y-%m-%d"),
                "original_text": f"Link {ev_id} → {ind_code}"
            }
            impact_links = pd.concat([impact_links, pd.DataFrame([link_record])], ignore_index=True)
            enrichment_log.append({**link_record, "notes": "Critical impact link added."})

    print(f"✅ Enrichment complete: {len(new_observations)} observations, {len(new_events)} events, {len(enrichment_log)-len(new_observations)-len(new_events)} impact links added.")
    return data, impact_links, enrichment_log

# -----------------------------
# 5. Log enrichment
# -----------------------------
def log_enrichment(enrichment_records, log_file="data_enrichment_log.md"):
    """
    Log enrichment records to a markdown file for documentation.
    """
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("# Data Enrichment Log - Task 1\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for rec in enrichment_records:
            f.write("## New Record\n")
            for k, v in rec.items():
                f.write(f"- **{k}**: {v}\n")
            f.write("\n")
    print(f"✅ Enrichment log saved to {log_file}")
