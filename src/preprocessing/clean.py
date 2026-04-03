from __future__ import annotations

import pandas as pd


def _standardize_columns(columns: list[str]) -> list[str]:
    standardized = []
    for col in columns:
        new_col = col.strip().lower().replace(" ", "_").replace("-", "_")
        standardized.append(new_col)
    return standardized


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = _standardize_columns(list(out.columns))

    if "date" in out.columns:
        parsed = pd.to_datetime(out["date"], errors="coerce")
        out["sale_year"] = parsed.dt.year
        out["sale_month"] = parsed.dt.month
        out = out.drop(columns=["date"])

    if "statezip" in out.columns:
        parts = (
            out["statezip"]
            .astype("string")
            .str.strip()
            .str.split(" ", n=1, expand=True)
        )
        out["state"] = parts[0].str.upper()
        out["zip"] = parts[1].astype("string")
        out = out.drop(columns=["statezip"])
    elif "zip" in out.columns:
        out["zip"] = out["zip"].astype("string")

    for col in ["street", "country"]:
        if col in out.columns:
            out = out.drop(columns=[col])

    numeric_cols = [
        "price",
        "bedrooms",
        "bathrooms",
        "sqft_living",
        "sqft_lot",
        "floors",
        "sqft_above",
        "sqft_basement",
        "yr_built",
        "yr_renovated",
        "sale_year",
        "sale_month",
    ]
    for col in numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    if "price" in out.columns:
        mask = out["price"].le(0).fillna(False)
        out.loc[mask, "price"] = pd.NA

    if "bedrooms" in out.columns:
        mask = out["bedrooms"].le(0).fillna(False)
        out.loc[mask, "bedrooms"] = pd.NA

    if "bathrooms" in out.columns:
        mask = out["bathrooms"].le(0).fillna(False)
        out.loc[mask, "bathrooms"] = pd.NA

    if "yr_renovated" in out.columns:
        yr_renovated = out["yr_renovated"]
        mask_positive = yr_renovated.gt(0).fillna(False)
        mask_invalid = pd.Series(False, index=out.index)
        if "yr_built" in out.columns:
            mask_invalid |= (mask_positive & yr_renovated.lt(out["yr_built"]))
        if "sale_year" in out.columns:
            mask_invalid |= (mask_positive & yr_renovated.gt(out["sale_year"]))
        mask_invalid = mask_invalid.fillna(False)
        out.loc[mask_invalid, "yr_renovated"] = pd.NA

    if "price" in out.columns:
        out = out[out["price"].notna()].copy()

    return out
