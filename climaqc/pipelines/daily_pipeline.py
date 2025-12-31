"""Pipeline diario: lectura -> EDA -> atípicos (Isolation Forest) -> imputación (MICE) -> export."""

from __future__ import annotations
import os
from ..io.readers import read_series_csv
from ..eda.summary import eda_summary
from ..qc.ml_isoforest import qc_isolation_forest
from ..impute.mice import impute_mice

def run_daily_pipeline(
    input_csv: str,
    output_csv: str,
    sep: str = ",",
    date_col: str = "fecha",
    value_col: str = "valor",
    date_format: str | None = None,
    dayfirst: bool = False,
    variable: str = "precipitacion_diaria",
    contamination: float = 0.01,
    mice_iter: int = 20,
    encoding: str | None = None,
    use_log1p: bool | None = None,
) -> dict:
    """Ejecuta el flujo diario y exporta un CSV final."""
    df = read_series_csv(
        input_csv,
        sep=sep,
        date_col=date_col,
        value_col=value_col,
        date_format=date_format,
        dayfirst=dayfirst,
        encoding=encoding
    )

    eda = eda_summary(df, date_col=date_col, value_col=value_col)

    if use_log1p is None:
        use_log1p = ("precip" in variable.lower()) or ("precipit" in variable.lower())

    df_qc = qc_isolation_forest(
        df,
        date_col=date_col,
        value_col=value_col,
        contamination=contamination,
        use_log1p=use_log1p
    )

    df_imp = impute_mice(
        df_qc,
        date_col=date_col,
        value_col=value_col,
        n_iter=mice_iter
    )

    out_cols = [date_col, value_col, "atipico_isoforest", "score_isoforest", "valor_mice", "qc_flag"]
    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)
    df_imp[out_cols].to_csv(output_csv, index=False)

    return {"data": df_imp[out_cols].copy(), "eda": eda}
