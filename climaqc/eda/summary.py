"""Exploración (EDA) para series diarias."""

from __future__ import annotations
import pandas as pd

def eda_summary(
    df: pd.DataFrame,
    date_col: str = "fecha",
    value_col: str = "valor",
    percentiles: tuple[int, ...] = (0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100),
) -> dict:
    """Resumen exploratorio básico."""
    s = df[value_col]
    out = {}
    out["fecha_inicio"] = str(df[date_col].min().date()) if len(df) else None
    out["fecha_fin"] = str(df[date_col].max().date()) if len(df) else None
    out["n_filas"] = int(len(df))
    out["n_faltantes_valor"] = int(s.isna().sum())
    out["n_fechas_unicas"] = int(df[date_col].nunique())

    desc = s.describe(percentiles=[p/100 for p in percentiles if 0 < p < 100], include="all")
    out["estadisticos"] = {k: (None if pd.isna(v) else float(v)) for k, v in desc.to_dict().items()}

    by_year = df.assign(anio=df[date_col].dt.year).groupby("anio")[value_col].apply(lambda x: x.notna().sum())
    out["disponibilidad_por_anio"] = by_year.to_dict()

    try:
        out["skew"] = float(s.dropna().skew())
        out["kurtosis"] = float(s.dropna().kurtosis())
    except Exception:
        out["skew"] = None
        out["kurtosis"] = None

    return out

def add_time_features(df: pd.DataFrame, date_col: str = "fecha") -> pd.DataFrame:
    """Agrega variables temporales útiles para QC/Imputación."""
    out = df.copy()
    out["anio"] = out[date_col].dt.year
    out["mes"] = out[date_col].dt.month
    out["dia"] = out[date_col].dt.day
    out["doy"] = out[date_col].dt.dayofyear
    out["dow"] = out[date_col].dt.dayofweek
    return out
