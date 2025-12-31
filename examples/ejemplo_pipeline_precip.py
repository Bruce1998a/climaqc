from climaqc import run_daily_pipeline

out = run_daily_pipeline(
    input_csv="precipitacion.csv",
    output_csv="salidas/precipitacion_qc.csv",
    sep=",",
    date_col="fecha",
    value_col="valor",
    variable="precipitacion_diaria",
    contamination=0.01,
    mice_iter=20
)

print("EDA:", out["eda"])
print("Listo. Revisa 'salidas/precipitacion_qc.csv'")
