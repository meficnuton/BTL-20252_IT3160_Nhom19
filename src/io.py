from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Optional

import pandas as pd


def ensure_parent_dir(path: Path) -> None:
    """Create parent directories if they do not exist."""
    path.parent.mkdir(parents=True, exist_ok=True)


def load_csv(path: Path, *, usecols: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(path, usecols=usecols)


def save_csv(df: pd.DataFrame, path: Path, *, index: bool = False) -> None:
    """Save a DataFrame to CSV, creating parent dirs if needed."""
    ensure_parent_dir(path)
    df.to_csv(path, index=index)


def load_json(path: Path) -> Any:
    """Load a JSON file and return the parsed object."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(obj: Any, path: Path, *, indent: int = 2) -> None:
    """Save an object to JSON, creating parent dirs if needed."""
    ensure_parent_dir(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, indent=indent)
