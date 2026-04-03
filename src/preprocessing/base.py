from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self

import pandas as pd


class Transformer(ABC):
    def __init__(self) -> None:
        self._fitted = False

    @abstractmethod
    def fit(self, df: pd.DataFrame) -> Self:
        """Learn parameters from the DataFrame and return self."""

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform the DataFrame using learned parameters."""

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Fit to the DataFrame, then transform it."""
        self.fit(df)
        return self.transform(df)
