"""
Healthcare Data Analysis Script
--------------------------------
This script uses Polars (a fast DataFrame library) to analyze hospital CSV data.
It loads and displays basic statistics about hospitals and physicians.
"""

import polars as pl

# ============================================================================
# CONFIGURATION: Define paths to CSV data files
# ============================================================================
HOSPITAL_DATA_PATH = "data/hospitals.csv"
PHYSICIAN_DATA_PATH = "data/physicians.csv"

# ============================================================================
# LOAD AND ANALYZE HOSPITAL DATA
# ============================================================================
# Read hospital CSV file into a Polars DataFrame
data_hospitals = pl.read_csv(HOSPITAL_DATA_PATH)

# Display hospital data statistics
print("=" * 60)
print("HOSPITAL DATA ANALYSIS")
print("=" * 60)
print(f"Dataset shape (rows, columns): {data_hospitals.shape}")
print("\nFirst 5 rows:")
print(data_hospitals.head())

# ============================================================================
# LOAD AND ANALYZE PHYSICIAN DATA
# ============================================================================
# Read physician CSV file into a Polars DataFrame
data_physicians = pl.read_csv(PHYSICIAN_DATA_PATH)

# Display physician data statistics
print("\n" + "=" * 60)
print("PHYSICIAN DATA ANALYSIS")
print("=" * 60)
print(f"Dataset shape (rows, columns): {data_physicians.shape}")
print("\nFirst 5 rows:")
print(data_physicians.head())
print("=" * 60)