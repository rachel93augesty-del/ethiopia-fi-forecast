# tests/test_data_analysis.py

import unittest
import os
import pandas as pd
from src.data_analysis import (
    load_dataset,
    summarize_dataset,
    temporal_coverage
    # calculate_growth_rate  # Uncomment once implemented
)

class TestDataAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load a small sample dataset for testing
        sample_data = {
            'year': [2011, 2014, 2017],
            'indicator': ['account_ownership', 'account_ownership', 'account_ownership'],
            'value': [20, 35, 50]
        }
        cls.df = pd.DataFrame(sample_data)

    def test_load_dataset(self):
        # Test loading of dataset (simulate small CSV)
        path = os.path.join(os.getcwd(), 'data', 'sample.csv')
        self.df.to_csv(path, index=False)
        df_loaded = load_dataset(path)
        self.assertIsInstance(df_loaded, pd.DataFrame)
        self.assertEqual(len(df_loaded), 3)
        os.remove(path)

    def test_summarize_dataset(self):
        summary = summarize_dataset(self.df)
        self.assertIsInstance(summary, pd.DataFrame)
        self.assertIn('indicator', summary.columns)

    def test_temporal_coverage(self):
        coverage = temporal_coverage(self.df, year_col='year', indicator_col='indicator')
        self.assertIsInstance(coverage, pd.DataFrame)
        self.assertEqual(set(coverage['year']), {2011, 2014, 2017})

    # Uncomment when calculate_growth_rate is implemented
    # def test_calculate_growth_rate(self):
    #     growth = calculate_growth_rate(self.df, column='value')
    #     self.assertEqual(list(growth), [None, 75.0, 42.857142857142854])  # Example expected growth

if __name__ == "__main__":
    unittest.main()
