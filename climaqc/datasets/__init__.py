"""Datos demo incluidos en el paquete."""

from importlib import resources
import pandas as pd

_MAP = {
    "precipitacion_diaria": "demo_precipitacion_diaria.csv",
    "temperatura_media_diaria": "demo_temperatura_media_diaria.csv",
    "tmin_diaria": "demo_tmin_diaria.csv",
    "tmax_diaria": "demo_tmax_diaria.csv",
}

def load_demo(nombre: str) -> pd.DataFrame:
    """Carga un dataset demo incluido en el paquete.

    NOTA
    ----
    Los archivos demo están separados por punto y coma (;).

    Parámetros
    ----------
    nombre : str
        Uno de: 'precipitacion_diaria', 'temperatura_media_diaria',
        'tmin_diaria', 'tmax_diaria'.

    Retorna
    -------
    pandas.DataFrame
        DataFrame con columnas correctamente separadas (fecha, valor).
    """
    nombre = nombre.strip().lower()
    if nombre not in _MAP:
        raise ValueError(
            f"Dataset demo desconocido: {nombre}. "
            f"Opciones: {list(_MAP.keys())}"
        )

    fname = _MAP[nombre]
    with resources.files(__package__).joinpath(fname).open("rb") as f:
        return pd.read_csv(f, sep=";")
