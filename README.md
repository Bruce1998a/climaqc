# ClimaQC

**ClimaQC** es un paquete en Python (en español) para series **diarias**:

- Validación del CSV (fecha/valor, separador, fechas).
- EDA (exploratorio).
- Detección de atípicos con **Isolation Forest** (marca, **no borra**).
- Relleno de faltantes con un enfoque **MICE-like** (IterativeImputer).
- Climatología mensual para periodos base de **30 años** (1981–2010, 1991–2020, etc.).
- Gráficas: medias mensuales y boxplot por trimestre.

## Instalación (modo desarrollo)
```bash
pip install -e .
```

## Formato esperado del CSV del usuario
- Columna fecha: `fecha` (o la que indiques con `date_col`)
- Columna valor: `valor` (o la que indiques con `value_col`)
- Separador: coma `,` o punto y coma `;` (parámetro `sep`)

## Pipeline diario (CSV -> CSV)
```python
from climaqc import run_daily_pipeline

out = run_daily_pipeline(
    input_csv="mi_serie.csv",
    output_csv="salidas/mi_serie_qc.csv",
    sep=";",
    date_col="fecha",
    value_col="valor",
    variable="precipitacion_diaria",
    contamination=0.01,
    mice_iter=20,
    dayfirst=False
)

print(out["eda"])
```

El CSV de salida incluye:
- `fecha`, `valor`, `atipico_isoforest`, `score_isoforest`, `valor_mice`, `qc_flag`

## Datos demo incluidos
```python
from climaqc import load_demo
df = load_demo("precipitacion_diaria")
print(df.head())
```

## Climatología mensual (>=30 años)
```python
from climaqc import read_series_csv
from climaqc.climate.climatology import monthly_climatology, plot_monthly_means, plot_boxplot_quarterly

df = read_series_csv("salidas/mi_serie_qc.csv", sep=",", date_col="fecha", value_col="valor_mice")

clim = monthly_climatology(
    df,
    date_col="fecha",
    value_col="valor_mice",
    baseline=("1991-01-01","2020-12-31"),
    agg="sum"  # 'sum' para precipitación, 'mean' para temperatura
)

plot_monthly_means(clim, "salidas/climatologia_mensual.png", title="Climatología 1991-2020")
plot_boxplot_quarterly(df, "salidas/boxplot_trimestres.png", value_col="valor_mice")
```

## Subir a GitHub (rápido)
```bash
git init
git add .
git commit -m "Primer release de ClimaQC"
git branch -M main
git remote add origin <TU_REPO_GITHUB>
git push -u origin main
```
