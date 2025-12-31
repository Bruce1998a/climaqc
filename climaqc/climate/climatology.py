"""Climatología mensual y gráficas."""

from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt

def _check_baseline_30y(df: pd.DataFrame, date_col: str, start: str, end: str) -> pd.DataFrame:
    sub = df[(df[date_col] >= pd.to_datetime(start)) & (df[date_col] <= pd.to_datetime(end))].copy()
    if sub.empty:
        raise ValueError("El periodo base no contiene datos.")
    years = sub[date_col].dt.year.nunique()
    if years < 30:
        raise ValueError(f"El periodo base debe tener al menos 30 años con datos. Años únicos encontrados: {years}.")
    return sub

def monthly_climatology(
    df: pd.DataFrame,
    date_col: str = "fecha",
    value_col: str = "valor",
    baseline: tuple[str, str] = ("1991-01-01", "2020-12-31"),
    agg: str = "mean",
) -> pd.DataFrame:
    """Calcula climatología mensual para un periodo base (>=30 años)."""
    start, end = baseline
    sub = _check_baseline_30y(df, date_col, start, end)

    sub["mes"] = sub[date_col].dt.month

    if agg == "mean":
        clim = sub.groupby("mes")[value_col].mean()
    elif agg == "sum":
        sub["anio"] = sub[date_col].dt.year
        ym = sub.groupby(["anio", "mes"])[value_col].sum().reset_index()
        clim = ym.groupby("mes")[value_col].mean()
    else:
        raise ValueError("agg debe ser 'mean' o 'sum'.")

    return clim.reset_index().rename(columns={value_col: "climatologia"})

def plot_monthly_means(
    clim_df: pd.DataFrame,
    out_png: str,
    title: str = "Climatología mensual",
    x_col: str = "mes",
    y_col: str = "climatologia",
) -> None:
    plt.figure()
    plt.plot(clim_df[x_col], clim_df[y_col], marker="o")
    plt.xlabel("Mes")
    plt.ylabel(y_col)
    plt.title(title)
    plt.xticks(range(1, 13))
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

def plot_boxplot_quarterly(
    df: pd.DataFrame,
    out_png: str,
    date_col: str = "fecha",
    value_col: str = "valor",
    title: str = "Boxplot por trimestre",
) -> None:
    tmp = df.copy()
    tmp["trimestre"] = ((tmp[date_col].dt.month - 1) // 3) + 1
    data = [tmp.loc[tmp["trimestre"] == q, value_col].dropna().values for q in [1, 2, 3, 4]]

    plt.figure()
    plt.boxplot(data, labels=["Q1", "Q2", "Q3", "Q4"])
    plt.xlabel("Trimestre")
    plt.ylabel(value_col)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()
