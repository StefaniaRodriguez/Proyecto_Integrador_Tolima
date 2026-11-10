import pandas as pd

def limpiar_columnas(datos):
    """
    Estandariza los nombres de las columnas
    sin modificar los valores originales.
    """

    datos_limpios = datos.copy()

    datos_limpios.columns = (
        datos_limpios.columns
        .str.strip()
    )

    if datos_limpios.columns.duplicated().any():
        raise ValueError(
            "Se encontraron nombres de columnas duplicados."
        )

    return datos_limpios


def limpiar_anios(datos, columna_anio):
    """
    Verifica y organiza la columna temporal
    utilizada para integrar las fuentes.
    """

    datos_limpios = datos.copy()

    if columna_anio not in datos_limpios.columns:
        raise ValueError(
            f"No existe la columna: {columna_anio}"
        )

    import pandas as pd

    anios = pd.to_numeric(
        datos_limpios[columna_anio],
        errors="raise"
    )

    if anios.isna().any() or (anios % 1 != 0).any():
        raise ValueError("Se encontraron años inválidos.")

    datos_limpios[columna_anio] = anios.astype(int)

    if datos_limpios[columna_anio].duplicated().any():
        raise ValueError("Se encontraron años duplicados.")

    datos_limpios = datos_limpios.sort_values(
        by=columna_anio
    ).reset_index(drop=True)

    return datos_limpios


def convertir_tasas_numericas(datos):
    """
    Convierte las tasas laborales de texto
    con coma decimal a valores numéricos.
    """

    datos_limpios = datos.copy()

    columnas_tasas = ["pct_pet", "tgp", "to", "td", "ts"]

    for columna in columnas_tasas:
        if columna not in datos_limpios.columns:
            raise ValueError(
                f"No existe la columna: {columna}"
            )

        valores = (
            datos_limpios[columna]
            .astype("string")
            .str.strip()
            .str.replace(",", ".", regex=False)
        )

        datos_limpios[columna] = pd.to_numeric(
            valores,
            errors="raise"
        )

    return datos_limpios


def normalizar_escalas_poblacionales(datos):
    """
    Estandariza las escalas poblacionales
    siguiendo el notebook original.
    """
    datos_normalizados = datos.copy()

    datos_normalizados["poblacion_total"] = (
        datos_normalizados["poblacion_total"] * 1000
    )

    condicion_pet = datos_normalizados["id_año"] >= 2015

    datos_normalizados.loc[condicion_pet, "pet"] = (
        datos_normalizados.loc[condicion_pet, "pet"] * 1000
    )

    return datos_normalizados