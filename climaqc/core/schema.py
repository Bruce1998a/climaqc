"""Validación de esquema y parseo de fechas."""

from __future__ import annotations
import pandas as pd

def validate_daily_series(
    df: pd.DataFrame,
    date_col: str = "fecha",
    value_col: str = "valor",
) -> None:
    """Valida que el DataFrame tenga columnas mínimas requeridas."""
    cols = set(df.columns)
    if date_col not in cols:
        raise ValueError(f"No se encontró la columna de fecha '{date_col}'. Columnas disponibles: {list(df.columns)}")
    if value_col not in cols:
        raise ValueError(f"No se encontró la columna de valor '{value_col}'. Columnas disponibles: {list(df.columns)}")

def coerce_dates(
    df: pd.DataFrame,
    date_col: str = "fecha",
    date_format: str | None = None,
    dayfirst: bool = False,
) -> pd.DataFrame:
    """Convierte la columna de fecha a datetime."""
    out = df.copy()
    if date_format:
        out[date_col] = pd.to_datetime(out[date_col], format=date_format, errors="coerce")
    else:
        out[date_col] = pd.to_datetime(out[date_col], errors="coerce", dayfirst=dayfirst, infer_datetime_format=True)

    n_bad = int(out[date_col].isna().sum())
    if n_bad > 0:
        raise ValueError(
            f"Se encontraron {n_bad} fechas no interpretables en '{date_col}'. "
            f"Sugerencia: revisa el formato o pasa date_format=..., dayfirst=True/False."
        )
    return out
