# test_src_import.py
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))

try:
    from src.forecasting_model import run_forecast_pipeline
    print("✅ Import successful!")
except ModuleNotFoundError as e:
    print("❌ Import failed:", e)
