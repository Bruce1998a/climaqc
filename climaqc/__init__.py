"""ClimaQC: Control de calidad, relleno e indicadores climatológicos para series diarias.

API rápida:
- load_demo()
- read_series_csv()
- eda_summary()
- qc_isolation_forest()
- impute_mice()
- monthly_climatology()
- run_daily_pipeline()
"""

from .datasets import load_demo
from .io.readers import read_series_csv
from .eda.summary import eda_summary
from .qc.ml_isoforest import qc_isolation_forest
from .impute.mice import impute_mice
from .climate.climatology import monthly_climatology
from .pipelines.daily_pipeline import run_daily_pipeline

__all__ = [
    "load_demo",
    "read_series_csv",
    "eda_summary",
    "qc_isolation_forest",
    "impute_mice",
    "monthly_climatology",
    "run_daily_pipeline",
]
