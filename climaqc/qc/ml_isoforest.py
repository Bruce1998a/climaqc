"""Detección de atípicos con Isolation Forest (NO borra datos)."""

from __future__ import annotations
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from ..eda.summary import add_time_features
from ..core import flags as F

def qc_isolation_forest(
    df: pd.DataFrame,
    date_col: str = "fecha",
    value_col: str = "valor",
    contamination: float = 0.01,
    random_state: int = 42,
    use_log1p: bool = False,
    flag_col: str = "qc_flag",
    outlier_col: str = "atipico_isoforest",
    score_col: str = "score_isoforest",
) -> pd.DataFrame:
    """Marca atípicos usando Isolation Forest."""
    out = df.copy()
    if flag_col not in out.columns:
        out[flag_col] = F.OK

    tmp = add_time_features(out, date_col=date_col)
    x = tmp[[value_col, "mes", "doy"]].copy()

    if use_log1p:
        x[value_col] = np.log1p(x[value_col].clip(lower=0))

    mask_fit = x[value_col].notna()
    x_fit = x.loc[mask_fit].values

    if len(x_fit) < 10:
        out[outlier_col] = False
        out[score_col] = np.nan
        return out

    model = IsolationForest(
        n_estimators=300,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(x_fit)

    scores = np.full(len(out), np.nan, dtype=float)
    preds = np.full(len(out), False, dtype=bool)

    scores_fit = model.decision_function(x_fit)
    pred_fit = model.predict(x_fit)

    scores[mask_fit.values] = scores_fit
    preds[mask_fit.values] = (pred_fit == -1)

    out[score_col] = scores
    out[outlier_col] = preds
    out.loc[out[outlier_col] == True, flag_col] = F.SUSPECT

    return out
