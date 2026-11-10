import pandas as pd


def integrar_datos(mercado_laboral, pib):
    """
    Integra el mercado laboral y el PIB del Tolima
    utilizando el año como llave temporal.
    """

    mercado = mercado_laboral.copy()
    producto = pib.copy()

    datos_integrados = pd.merge(
        mercado,
        producto,
        left_on="id_año",
        right_on="año_id",
        how="left",
        validate="one_to_one",
        indicator=True
    )

    sin_pib = datos_integrados["_merge"] != "both"

    if sin_pib.any():
        anios_faltantes = datos_integrados.loc[
            sin_pib, "id_año"
        ].tolist()

        raise ValueError(
            f"No se encontró PIB para los años: {anios_faltantes}"
        )

    datos_integrados = datos_integrados.drop(
        columns=["_merge", "año_id", "pib_departamento"]
    )

    datos_integrados = datos_integrados.rename(
        columns={"mer_departamento": "departamento"}
    )

    return datos_integrados