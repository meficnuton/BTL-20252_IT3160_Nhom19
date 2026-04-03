from pathlib import Path

# Project root (directory that contains data/, src/, etc.)
ROOT_DIR = Path(__file__).resolve().parents[1]

# Reproducibility
RANDOM_SEED = 42

# Paths
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_DATA_PATH = RAW_DIR / "rawdata.csv"
PROCESSED_CLEAN_PATH = PROCESSED_DIR / "cleaned.csv"

# Columns
TARGET_COL = "price"
DATE_COL = "date"

RAW_COLUMNS = [
    "date",
    "price",
    "bedrooms",
    "bathrooms",
    "sqft_living",
    "sqft_lot",
    "floors",
    "waterfront",
    "view",
    "condition",
    "sqft_above",
    "sqft_basement",
    "yr_built",
    "yr_renovated",
    "street",
    "city",
    "statezip",
    "country",
]

CLEAN_FEATURE_COLS = [
    "bedrooms",
    "bathrooms",
    "sqft_living",
    "sqft_lot",
    "floors",
    "waterfront",
    "view",
    "condition",
    "sqft_above",
    "sqft_basement",
    "yr_built",
    "yr_renovated",
    "city",
    "state",
    "zip",
    "sale_year",
    "sale_month",
]

FEATURE_COLS = CLEAN_FEATURE_COLS.copy()

# Treat these as categorical/string-like. Others will be numeric by default.
CATEGORICAL_COLS = [
    "city",
    "state",
    "zip",
    "waterfront",
    "view",
    "condition",
]

NUMERIC_COLS = [c for c in FEATURE_COLS if c not in CATEGORICAL_COLS]
