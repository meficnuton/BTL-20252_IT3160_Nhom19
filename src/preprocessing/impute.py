from __future__ import annotations

from typing import Dict, List, Optional

import pandas as pd

from .base import Transformer


class MedianImputer(Transformer):
    def __init__(self, columns: List[str]) -> None:
        super().__init__()
        self.columns = columns
        self.medians_: Dict[str, Optional[float]] = {}

    def fit(self, df: pd.DataFrame) -> "MedianImputer":
        for col in self.columns:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found in input DataFrame.")
            series = df[col]
            if series.dropna().empty:
                self.medians_[col] = None
            else:
                self.medians_[col] = float(series.median())

        self._fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self._fitted:
            raise RuntimeError("MedianImputer must be fit before calling transform.")

        missing_cols = [c for c in self.columns if c not in df.columns]
        if missing_cols:
            raise ValueError(
                f"Input DataFrame is missing columns: {', '.join(missing_cols)}"
            )

        out = df.copy()
        for col in self.columns:
            fill_value = self.medians_.get(col)
            if fill_value is not None:
                out[col] = out[col].fillna(fill_value)
        return out


class ModeImputer(Transformer):
    def __init__(self, columns: List[str]) -> None:
        super().__init__()
        self.columns = columns
        self.modes_: Dict[str, Optional[object]] = {}

    def fit(self, df: pd.DataFrame) -> "ModeImputer":
        for col in self.columns:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found in input DataFrame.")
            series = df[col]
            if series.dropna().empty:
                self.modes_[col] = None
            else:
                mode_series = series.mode(dropna=True)
                self.modes_[col] = mode_series.iloc[0] if not mode_series.empty else None

        self._fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if not self._fitted:
            raise RuntimeError("ModeImputer must be fit before calling transform.")

        missing_cols = [c for c in self.columns if c not in df.columns]
        if missing_cols:
            raise ValueError(
                f"Input DataFrame is missing columns: {', '.join(missing_cols)}"
            )

        out = df.copy()
        for col in self.columns:
            fill_value = self.modes_.get(col)
            if fill_value is not None:
                out[col] = out[col].fillna(fill_value)
        return out
