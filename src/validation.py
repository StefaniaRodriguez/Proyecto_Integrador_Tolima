import pandas as pd


def validar_datos_integrados(datos):
    """
    Verifica la estructura, los años y la integridad
    del conjunto de datos integrado del Tolima.
    """
    
    if datos.shape != (19, 22):
        raise ValueError(
            f"Dimensiones inesperadas: {datos.shape}"
        )

    anios_esperados = list(range(2007, 2026))
    anios_obtenidos = datos["id_año"].tolist()

    if anios_obtenidos != anios_esperados:
        raise ValueError(
            "Los años no corresponden al periodo 2007-2025."
        )
    
    if datos["id_año"].duplicated().any():
        raise ValueError("Existen años duplicados.")
    
    columnas_esenciales = [
        "id_año",
        "pib_constante_2015",
        "poblacion_ocupada",
        "tgp",
        "to",
        "td",
        "crec_pib_real",
        "var_ocupados",
        "var_desocupados",
        "pib_por_ocupado",
        "ocupados_por_mil_pet",
        "brecha_tgp_to"
    ]

    faltantes = set(columnas_esenciales) - set(datos.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas: {sorted(faltantes)}"
        )
    
    resumen_nulos = datos.isna().sum()
    resumen_nulos = resumen_nulos[resumen_nulos > 0]

    print("VALIDACIÓN COMPLETADA")
    print("Dimensiones:", datos.shape)
    print("Años duplicados:", datos["id_año"].duplicated().sum())
    print("Total de valores faltantes:", datos.isna().sum().sum())
    print("Valores faltantes por columna:")
    print(resumen_nulos)

    return datos


def validar_tasas_laborales(datos):
    """
    Verifica que las tasas laborales estén
    dentro del intervalo de 0 a 100 %.
    Registra los resultados para la auditoría.
    """
    columnas_tasas = ["pct_pet", "tgp", "to", "td", "ts"]

    resultados = {}

    for columna in columnas_tasas:
        valores = pd.to_numeric(datos[columna], errors="raise")

        fuera_de_rango = valores.notna() & ~valores.between(0, 100)

        cantidad_invalidos = int(fuera_de_rango.sum())

        resultados[columna] = cantidad_invalidos

        if cantidad_invalidos > 0:
            raise ValueError(
                f"La columna {columna} contiene "
                f"{cantidad_invalidos} tasas fuera de rango."
            )

    print("TASAS LABORALES VALIDADAS")

    return datos, resultados


def validar_consistencia_laboral(datos):
    """
    Verifica las seis identidades contables laborales.
    Considera tolerancias por redondeo de las fuentes.
    """
    tolerancia_personas = 1
    tolerancia_tasas = 0.15

    comprobaciones = {
        "Fuerza de trabajo": (
            datos["fuerza_trabajo"]
            - (
                datos["poblacion_ocupada"]
                + datos["poblacion_desocupada"]
            ),
            tolerancia_personas
        ),
        "Población en edad de trabajar": (
            datos["pet"]
            - (
                datos["fuerza_trabajo"]
                + datos["fuera_fuerza_trabajo"]
            ),
            tolerancia_personas
        ),
        "Tasa global de participación": (
            datos["tgp"]
            - datos["fuerza_trabajo"]
            / datos["pet"].replace(0, pd.NA) * 100,
            tolerancia_tasas
        ),
        "Tasa de ocupación": (
            datos["to"]
            - datos["poblacion_ocupada"]
            / datos["pet"].replace(0, pd.NA) * 100,
            tolerancia_tasas
        ),
        "Tasa de desocupación": (
            datos["td"]
            - datos["poblacion_desocupada"]
            / datos["fuerza_trabajo"].replace(0, pd.NA) * 100,
            tolerancia_tasas
        ),
        "Porcentaje PET": (
            datos["pct_pet"]
            - datos["pet"]
            / datos["poblacion_total"].replace(0, pd.NA) * 100,
            tolerancia_tasas
        )
    }

    print("VALIDACIÓN DE CONSISTENCIA LABORAL")
    resultados = {}
    for nombre, (diferencias, tolerancia) in comprobaciones.items():
        fallos = diferencias.abs() > tolerancia
        cantidad_fallos = int(fallos.sum())

        resultados[nombre] = cantidad_fallos

        print(f"{nombre}: {cantidad_fallos} inconsistencias")
        
        if cantidad_fallos > 0:
            anios = datos.loc[fallos, "id_año"].tolist()
            print(f"  Años con inconsistencias: {anios}")

    return datos, resultados


def validar_valores_positivos(datos):
    """
    Comprueba que el PIB real y las principales
    variables poblacionales sean positivos.
    """
    columnas = [
        "pib_constante_2015",
        "poblacion_total",
        "pet",
        "fuerza_trabajo",
        "poblacion_ocupada"
    ]

    print("VALIDACIÓN DE VALORES POSITIVOS")

    for columna in columnas:
        valores = pd.to_numeric(datos[columna], errors="raise")

        invalidos = valores.isna() | (valores <= 0)
        cantidad_invalidos = int(invalidos.sum())

        print(f"{columna}: {cantidad_invalidos} valores inválidos")

        if cantidad_invalidos > 0:
            anios = datos.loc[invalidos, "id_año"].tolist()
            print(f"  Años afectados: {anios}")

    return datos

def validar_indicadores_derivados(datos):
    """
    Comprueba los seis indicadores derivados
    a partir de sus variables originales.
    """
    datos_ordenados = datos.sort_values("id_año")

    indicadores_esperados = {
        "crec_pib_real": (
            datos_ordenados["pib_constante_2015"]
            .pct_change(fill_method=None) * 100
        ),
        "var_ocupados": (
            datos_ordenados["poblacion_ocupada"]
            .pct_change(fill_method=None) * 100
        ),
        "var_desocupados": (
            datos_ordenados["poblacion_desocupada"]
            .pct_change(fill_method=None) * 100
        ),
        "pib_por_ocupado": (
            datos_ordenados["pib_constante_2015"]
            / datos_ordenados["poblacion_ocupada"]
        ),
        "ocupados_por_mil_pet": (
            datos_ordenados["poblacion_ocupada"]
            / datos_ordenados["pet"] * 1000
        ),
        "brecha_tgp_to": (
            datos_ordenados["tgp"] - datos_ordenados["to"]
        )
    }

    print("VALIDACIÓN DE INDICADORES DERIVADOS")

    for columna, esperado in indicadores_esperados.items():
        observado = datos_ordenados[columna]

        diferencias = (observado - esperado).abs()
        inconsistencias = (
            diferencias.gt(0.000001).fillna(False)
            | (observado.isna() != esperado.isna())
        )

        cantidad = int(inconsistencias.sum())
        print(f"{columna}: {cantidad} inconsistencias")

        if cantidad > 0:
            anios = datos_ordenados.loc[
                inconsistencias, "id_año"
            ].tolist()
            print(f"  Años afectados: {anios}")

    return datos


def detectar_valores_atipicos(datos):
    """
    Detecta valores atípicos mediante el método IQR.
    No elimina ni modifica los registros.
    """
    columnas = [
        "pib_constante_2015",
        "poblacion_total",
        "pet",
        "fuerza_trabajo",
        "poblacion_ocupada",
        "poblacion_desocupada",
        "tgp",
        "to",
        "td"
    ]
    
    resultados = {}
    print("DETECCIÓN DE VALORES ATÍPICOS (IQR)")

    for columna in columnas:
        valores = pd.to_numeric(
            datos[columna], errors="raise"
        ).dropna()

        q1 = valores.quantile(0.25)
        q3 = valores.quantile(0.75)
        iqr = q3 - q1

        limite_inferior = q1 - 1.5 * iqr
        limite_superior = q3 + 1.5 * iqr

        atipicos = (
            (datos[columna] < limite_inferior)
            | (datos[columna] > limite_superior)
        ).fillna(False)

        cantidad = int(atipicos.sum())

        resultados[columna] = cantidad

        print(f"{columna}: {cantidad} valores atípicos")

        if cantidad > 0:
            print(
                datos.loc[
                    atipicos, ["id_año", columna]
                ].to_string(index=False)
            )

    return datos, resultados


def validar_integridad_pib(datos_integrados, pib_original):
    """
    Verifica que los valores del PIB real no hayan
    cambiado durante la integración y transformación.
    """
    comparacion = datos_integrados[
        ["id_año", "pib_constante_2015"]
    ].merge(
        pib_original[["año_id", "pib_constante_2015"]],
        left_on="id_año",
        right_on="año_id",
        how="outer",
        validate="one_to_one",
        indicator=True,
        suffixes=("_final", "_original")
    )

    diferencias = (
        comparacion["pib_constante_2015_final"]
        != comparacion["pib_constante_2015_original"]
    )

    inconsistencias = (
        diferencias.fillna(True)
        | (comparacion["_merge"] != "both")
    )

    cantidad = int(inconsistencias.sum())

    print("VALIDACIÓN DE INTEGRIDAD DEL PIB")
    print(f"Valores de PIB modificados: {cantidad}")

    if cantidad > 0:
        print(
            comparacion.loc[
                inconsistencias,
                ["id_año", "pib_constante_2015_final",
                 "pib_constante_2015_original"]
            ].to_string(index=False)
        )

    resultados = {
        "valores_pib_modificados": cantidad
    }

    return datos_integrados, resultados


def validar_cobertura_temporal(pib, mercado_laboral):
    """
    Compara los años disponibles en ambas fuentes.
    Identifica años exclusivos de cada conjunto.
    No modifica los datos.
    """
    anios_pib = set(pib["año_id"].dropna())
    anios_laboral = set(mercado_laboral["id_año"].dropna())

    solo_pib = sorted(anios_pib - anios_laboral)
    solo_laboral = sorted(anios_laboral - anios_pib)
    comunes = sorted(anios_pib & anios_laboral)

    print("\nVALIDACIÓN DE COBERTURA TEMPORAL")
    print(f"Años disponibles en PIB: {len(anios_pib)}")
    print(f"Años disponibles en mercado laboral: {len(anios_laboral)}")
    print(f"Años comunes: {len(comunes)}")
    print(f"Años del PIB sin mercado laboral: {solo_pib}")
    print(f"Años del mercado laboral sin PIB: {solo_laboral}")

    return {
        "anios_comunes": comunes,
        "solo_pib": solo_pib,
        "solo_laboral": solo_laboral
    }


def validar_poblaciones_no_negativas(datos):
    """
    Verifica que las variables poblacionales adicionales
    no contengan valores negativos.
    Conserva los valores faltantes.
    """
    columnas = [
        "poblacion_desocupada",
        "fuera_fuerza_trabajo",
        "poblacion_subocupada",
        "fuerza_trabajo_potencial"
    ]

    resultados = {}

    print("\nVALIDACIÓN DE POBLACIONES NO NEGATIVAS")

    for columna in columnas:
        valores = pd.to_numeric(
            datos[columna], errors="raise"
        )

        negativos = valores.notna() & (valores < 0)
        cantidad = int(negativos.sum())

        resultados[columna] = cantidad

        print(f"{columna}: {cantidad} valores negativos")

        if cantidad > 0:
            anios = datos.loc[negativos, "id_año"].tolist()
            raise ValueError(
                f"La columna {columna} contiene valores "
                f"negativos en los años: {anios}"
            )

    return datos, resultados


def validar_reglas_indicadores(datos):
    """
    Verifica reglas adicionales de los indicadores
    económicos y laborales derivados.
    No modifica los datos.
    """
    reglas = {
        "PIB por ocupado positivo": (
            datos["pib_por_ocupado"] <= 0
        ),
        "Ocupados por mil PET entre 0 y 1000": (
            ~datos["ocupados_por_mil_pet"].between(0, 1000)
        ),
        "Brecha TGP-TO no negativa": (
            datos["brecha_tgp_to"] < 0
        ),
        "Crecimiento PIB real no inferior a -100 %": (
            datos["crec_pib_real"] < -100
        ),
        "Variación de ocupados no inferior a -100 %": (
            datos["var_ocupados"] < -100
        ),
        "Variación de desocupados no inferior a -100 %": (
            datos["var_desocupados"] < -100
        )
    }

    resultados = {}

    print("\nVALIDACIÓN DE REGLAS ADICIONALES")

    for nombre, condicion in reglas.items():
        cantidad = int(condicion.fillna(False).sum())
        resultados[nombre] = cantidad

        print(f"{nombre}: {cantidad} incumplimientos")

        if cantidad > 0:
            raise ValueError(
                f"La regla '{nombre}' presenta "
                f"{cantidad} incumplimientos."
            )

    return datos, resultados