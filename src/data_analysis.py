# src/data_analysis.py

"""
data_analysis.py
================
Functions for Task 2: Exploratory Data Analysis (EDA) of financial inclusion in Ethiopia.
Includes dataset loading, summarization, temporal coverage, and growth rate calculation.
"""

import pandas as pd
import numpy as np


# 1. Load dataset
def load_dataset(path: str) -> pd.DataFrame:
    """
    Load CSV dataset into a pandas DataFrame.
    
    Args:
        path (str): Path to CSV file.
    
    Returns:
        pd.DataFrame: Loaded dataset.
    """
    df = pd.read_csv(path)
    return df


# 2. Summarize dataset

def summarize_dataset(df, col_name):
    """
    Summarize a single column of the DataFrame.
    """
    summary = df.groupby(col_name).size().reset_index(name="count")
    return summary



# 3. Temporal coverage
def temporal_coverage(df: pd.DataFrame, year_col: str = 'year', indicator_col: str = 'indicator') -> pd.DataFrame:
    """
    Calculate temporal coverage: which years have data for which indicators.
    
    Args:
        df (pd.DataFrame): Input dataset.
        year_col (str): Column name for years.
        indicator_col (str): Column name for indicators.
    
    Returns:
        pd.DataFrame: Coverage with columns [year_col, indicator_col, 'count'].
    """
    if year_col not in df.columns or indicator_col not in df.columns:
        raise KeyError(f"Dataset must contain '{year_col}' and '{indicator_col}' columns")
    
    coverage = df.groupby([year_col, indicator_col]).size().reset_index(name='count')
    return coverage


# 4. Calculate growth rate between consecutive years
def calculate_growth_rate(df: pd.DataFrame, year_col: str = 'year', value_col: str = 'value') -> pd.DataFrame:
    """
    Calculate year-over-year growth rate for a numeric column.
    
    Args:
        df (pd.DataFrame): Input dataset with 'year' and numeric column.
        year_col (str): Column name for years.
        value_col (str): Column name to calculate growth rate on.
    
    Returns:
        pd.DataFrame: Original DataFrame with additional 'growth_rate' column.
    """
    if year_col not in df.columns or value_col not in df.columns:
        raise KeyError(f"Dataset must contain '{year_col}' and '{value_col}' columns")
    
    df = df.sort_values(by=year_col).copy()
    df['growth_rate'] = df[value_col].pct_change() * 100  # percent
    return df


# 5. Gender gap analysis helper
def gender_gap(df: pd.DataFrame, value_col: str = 'value') -> pd.DataFrame:
    """
    Calculate gender gap (male vs female) for a numeric column.
    
    Args:
        df (pd.DataFrame): Input dataset with 'gender' and value column.
        value_col (str): Column to calculate gap on.
    
    Returns:
        pd.DataFrame: Aggregated by gender with mean values.
    """
    if 'gender' not in df.columns or value_col not in df.columns:
        raise KeyError("Dataset must contain 'gender' and value columns")
    
    gap_df = df.groupby('gender')[value_col].mean().reset_index()
    return gap_df
