import sys
import os
import pytest
import pandas as pd

# -----------------------------
# Ensure src folder is on Python path
# -----------------------------
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import data_explore as de

# -----------------------------
# Paths to test files
# -----------------------------
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'ethiopia_fi_unified_data.xlsx')
REFERENCE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'reference_codes.xlsx')

# -----------------------------
# Fixtures
# -----------------------------
@pytest.fixture
def load_dataframes():
    data_df, impact_df, reference_df = de.load_data(
        DATA_FILE,
        reference_codes_file=REFERENCE_FILE
    )
    return data_df, impact_df, reference_df

# -----------------------------
# Tests
# -----------------------------
def test_load_data(load_dataframes):
    data_df, impact_df, reference_df = load_dataframes
    # Check shapes
    assert data_df.shape[0] > 0
    assert impact_df.shape[0] > 0
    assert reference_df.shape[0] > 0
    # Check some columns exist in main data
    for col in ['record_type', 'pillar', 'indicator', 'indicator_code']:
        assert col in data_df.columns
    # Check columns in impact links
    for col in ['record_id', 'parent_id', 'pillar', 'related_indicator']:
        assert col in impact_df.columns
    # Check columns in reference codes (fixed)
    for col in ['field', 'code', 'description', 'applies_to']:
        assert col in reference_df.columns

def test_basic_exploration(load_dataframes, capsys):
    data_df, impact_df, _ = load_dataframes
    # Just run function, capture stdout
    de.basic_exploration(data_df, impact_df)
    captured = capsys.readouterr()
    assert "Main Data Exploration" in captured.out
    assert "Impact Sheet Summary" in captured.out

def test_enrich_data(load_dataframes):
    data_df, impact_df, _ = load_dataframes
    original_data_rows = data_df.shape[0]
    original_impact_rows = impact_df.shape[0]

    # Enrich
    data_df, impact_df, log = de.enrich_data(data_df, impact_df)

    # Checks
    assert len(log) > 0
    assert data_df.shape[0] > original_data_rows
    assert impact_df.shape[0] > original_impact_rows
    # Check enrichment log structure
    for rec in log:
        assert 'notes' in rec
        assert 'record_type' in rec or 'parent_id' in rec
