"""Relleno de datos con enfoque MICE-like (IterativeImputer)."""

from __future__ import annotations
import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor
from ..eda.summary import add_time_features
from ..core import flags as F

def impute_mice(
    df: pd.DataFrame,
    date_col: str = "fecha",
    value_col: str = "valor",
    out_col: str = "valor_mice",
    flag_col: str = "qc_flag",
    add_features: bool = True,
    n_iter: int = 20,
    random_state: int = 42,
    min_value: float | None = None,
    max_value: float | None = None,
) -> pd.DataFrame:
    """Imputa valores faltantes usando IterativeImputer (MICE-like)."""
    out = df.copy()
    if flag_col not in out.columns:
        out[flag_col] = F.OK

    tmp = add_time_features(out, date_col=date_col) if add_features else out.copy()

    cols = [value_col]
    if add_features:
        cols += ["mes", "doy", "dow"]

    X = tmp[cols].copy()
    for c in X.columns:
        X[c] = pd.to_numeric(X[c], errors="coerce")

    estimator = RandomForestRegressor(
        n_estimators=300,
        random_state=random_state,
        n_jobs=-1,
        min_samples_leaf=2
    )

    imputer = IterativeImputer(
        estimator=estimator,
        max_iter=n_iter,
        random_state=random_state,
        sample_posterior=False,
        skip_complete=True
    )

    X_imp = imputer.fit_transform(X)
    imputados = X_imp[:, 0].astype(float)

    if min_value is not None:
        imputados = np.maximum(imputados, min_value)
    if max_value is not None:
        imputados = np.minimum(imputados, max_value)

    out[out_col] = imputados

    mask_nan = out[value_col].isna()
    out.loc[mask_nan, flag_col] = F.CORRECTED

    return out
