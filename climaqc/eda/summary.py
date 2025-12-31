"""Exploración (EDA) para series diarias."""

from __future__ import annotations
import pandas as pd


def eda_summary(
    df: pd.DataFrame,
    date_col: str = "fecha",
    value_col: str = "valor",
    percentiles: tuple[int, ...] = (0, 1, 5, 10, 25, 50, 75, 90, 95, 99, 100),
) -> dict:
    """Resumen exploratorio básico para series diarias.

    Esta función:
    - Convierte la columna de fecha a datetime
    - Valida fechas
    - Calcula estadísticos descriptivos y disponibilidad
    """

    df = df.copy()

    # 🔒 Convertir fecha a datetime (obligatorio)
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # Validar fechas
    if df[date_col].isna().any():
        raise ValueError(
            f"La columna '{date_col}' contiene fechas no válidas. "
            "Revise el formato antes de ejecutar el EDA."
        )

    s = df[value_col]
    out = {}

    out["fecha_inicio"] = df[date_col].min().date().isoformat()
    out["fecha_fin"] = df[date_col].max().date().isoformat()
    out["n_filas"] = int(len(df))
    out["n_faltantes_valor"] = int(s.isna().sum())
    out["n_fechas_unicas"] = int(df[date_col].nunique())

    # Estadísticos y percentiles
    desc = s.describe(
        percentiles=[p / 100 for p in percentiles if 0 < p < 100],
        include="all"
    )

    out["estadisticos"] = {
        k: (None if pd.isna(v) else float(v))
        for k, v in desc.to_dict().items()
    }

    # Disponibilidad por año
    by_year = (
        df.assign(anio=df[date_col].dt.year)
          .groupby("anio")[value_col]
          .apply(lambda x: x.notna().sum())
    )
    out["disponibilidad_por_anio"] = by_year.to_dict()

    # Asimetría y curtosis
    try:
        out["skew"] = float(s.dropna().skew())
        out["kurtosis"] = float(s.dropna().kurtosis())
    except Exception:
        out["skew"] = None
        out["kurtosis"] = None

    return out


def add_time_features(df: pd.DataFrame, date_col: str = "fecha") -> pd.DataFrame:
    """Agrega variables temporales útiles para QC e imputación."""

    out = df.copy()

    # 🔒 Asegurar datetime también aquí
    out[date_col] = pd.to_datetime(out[date_col], errors="coerce")

    if out[date_col].isna().any():
        raise ValueError(
            f"La columna '{date_col}' contiene fechas no válidas. "
            "No se pueden generar variables temporales."
        )

    out["anio"] = out[date_col].dt.year
    out["mes"] = out[date_col].dt.month
    out["dia"] = out[date_col].dt.day
    out["doy"] = out[date_col].dt.dayofyear
    out["dow"] = out[date_col].dt.dayofweek

    return out
