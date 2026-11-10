import pandas as pd


def transformar_pib(pib):
    """
    Calcula el crecimiento anual del PIB real
    del Tolima a precios constantes de 2015.
    """

    pib_transformado = pib.copy()

    pib_transformado = pib_transformado.sort_values(
        by="año_id"
    ).reset_index(drop=True)

    pib_transformado["crec_pib_real"] = (
        pib_transformado["pib_constante_2015"]
        .pct_change(fill_method=None) * 100
    )

    return pib_transformado


def transformar_mercado_laboral(mercado_laboral):
    """
    Calcula las variaciones porcentuales anuales
    de la población ocupada y desocupada.
    """

    mercado_transformado = mercado_laboral.copy()

    mercado_transformado = mercado_transformado.sort_values(
        by="id_año"
    ).reset_index(drop=True)

    mercado_transformado["var_ocupados"] = (
        mercado_transformado["poblacion_ocupada"]
        .pct_change(fill_method=None) * 100
    )

    mercado_transformado["var_desocupados"] = (
        mercado_transformado["poblacion_desocupada"]
        .pct_change(fill_method=None) * 100
    )

    return mercado_transformado


def transformar_datos_integrados(datos_integrados):
    """
    Calcula indicadores económicos combinando
    el PIB real y el mercado laboral del Tolima.
    """

    datos_transformados = datos_integrados.copy()

    datos_transformados["pib_por_ocupado"] = (
        datos_transformados["pib_constante_2015"]
        / datos_transformados["poblacion_ocupada"].replace(0, pd.NA)
    )

    datos_transformados["ocupados_por_mil_pet"] = (
        datos_transformados["poblacion_ocupada"]
        / datos_transformados["pet"].replace(0, pd.NA)
    ) * 1000

    datos_transformados["brecha_tgp_to"] = (
        datos_transformados["tgp"]
        - datos_transformados["to"]
    )

    return datos_transformados