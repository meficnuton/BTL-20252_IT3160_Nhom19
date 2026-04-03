import pandas as pd

from src.preprocessing.clean import clean_data

def _raw_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["5/2/2014 0:00", "5/2/2014 0:00", "5/2/2014 0:00"],
            "price": [313000, 0, 500000],
            "bedrooms": [3, 0, 3],
            "bathrooms": [1.5, 2.5, 0],
            "sqft_living": [1340, 3650, 1000],
            "sqft_lot": [7912, 9050, 5000],
            "floors": [1.5, 2, 1],
            "waterfront": [0, 0, 0],
            "view": [0, 4, 0],
            "condition": [3, 5, 3],
            "sqft_above": [1340, 3370, 1000],
            "sqft_basement": [0, 280, 0],
            "yr_built": [1955, 1921, 2000],
            "yr_renovated": [2005, 0, 1990],
            "street": ["18810 Densmore Ave N", "709 W Blaine St", "123 A St"],
            "city": ["Shoreline", "Seattle", "X"],
            "statezip": ["WA 98133", "WA 98119", "WA 98000"],
            "country": ["USA", "USA", "USA"],
        }
    )


def test_date_parsing_and_drop() -> None:
    cleaned = clean_data(_raw_df())
    assert "date" not in cleaned.columns
    assert "sale_year" in cleaned.columns
    assert "sale_month" in cleaned.columns
    assert cleaned["sale_year"].iloc[0] == 2014
    assert cleaned["sale_month"].iloc[0] == 5


def test_statezip_split() -> None:
    cleaned = clean_data(_raw_df())
    assert "statezip" not in cleaned.columns
    assert "state" in cleaned.columns
    assert "zip" in cleaned.columns
    assert cleaned["state"].iloc[0] == "WA"
    assert cleaned["zip"].iloc[0] == "98133"


def test_invalids_cleaned_and_target_drop() -> None:
    cleaned = clean_data(_raw_df())
    assert len(cleaned) == 2
    assert pd.isna(cleaned.loc[cleaned["city"] == "X", "bathrooms"]).all()
    assert pd.isna(cleaned.loc[cleaned["city"] == "X", "yr_renovated"]).all()
