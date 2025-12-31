"""Lectura robusta de CSV para series diarias."""

from __future__ import annotations
import pandas as pd
from ..core.schema import validate_daily_series, coerce_dates

def read_series_csv(
    path: str,
    sep: str = ",",
    date_col: str = "fecha",
    value_col: str = "valor",
    date_format: str | None = None,
    dayfirst: bool = False,
    encoding: str | None = None,
) -> pd.DataFrame:
    """Lee un CSV del usuario y valida columnas/fechas."""
    df = pd.read_csv(path, sep=sep, encoding=encoding)
    df.columns = [c.strip() for c in df.columns]

    validate_daily_series(df, date_col=date_col, value_col=value_col)
    df = coerce_dates(df, date_col=date_col, date_format=date_format, dayfirst=dayfirst)

    df[value_col] = pd.to_numeric(df[value_col], errors="coerce")

    df = df.sort_values(date_col).drop_duplicates(subset=[date_col], keep="last").reset_index(drop=True)
    return df
