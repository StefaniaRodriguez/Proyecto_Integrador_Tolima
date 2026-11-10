import pandas as pd


def generar_reporte_completitud(datos):
    """
    Resume la cantidad, porcentaje y completitud
    de cada columna del dataset final.
    """
    total_filas = len(datos)

    reporte = pd.DataFrame({
        "variable": datos.columns,
        "valores_faltantes": datos.isna().sum().values,
        "porcentaje_faltantes": (
            datos.isna().mean().values * 100
        ),
        "porcentaje_completitud": (
            datos.notna().mean().values * 100
        )
    })

    reporte["porcentaje_faltantes"] = (
        reporte["porcentaje_faltantes"].round(2)
    )

    reporte["porcentaje_completitud"] = (
        reporte["porcentaje_completitud"].round(2)
    )

    print("\nREPORTE DE COMPLETITUD")
    print(f"Registros analizados: {total_filas}")
    print(reporte.to_string(index=False))

    return reporte


def generar_estadisticas_descriptivas(datos):
    """
    Genera estadísticas descriptivas de las
    variables numéricas del dataset final.
    """
    variables_numericas = datos.select_dtypes(
        include="number"
    ).drop(columns=["id_año"], errors="ignore")

    estadisticas = variables_numericas.agg([
        "count",
        "mean",
        "median",
        "std",
        "min",
        "max"
    ]).T

    estadisticas = estadisticas.rename(columns={
        "count": "observaciones",
        "mean": "media",
        "median": "mediana",
        "std": "desviacion_estandar",
        "min": "minimo",
        "max": "maximo"
    })

    estadisticas = estadisticas.round(2)

    print("\nESTADÍSTICAS DESCRIPTIVAS")
    print(estadisticas.to_string())

    return estadisticas


def generar_matriz_calidad(
    datos,
    reporte_completitud,
    resultado_integridad_pib,
    resultado_consistencia,
    resultado_validez,
    resultado_atipicos
):
    """
    Resume las dimensiones de calidad verificadas
    durante el procesamiento del dataset.
    """
    total_faltantes = int(
        reporte_completitud["valores_faltantes"].sum()
    )

    matriz = pd.DataFrame([
        {
            "dimension": "Completitud",
            "criterio": "Identificación de valores faltantes",
            "resultado": f"{total_faltantes} faltantes",
            "tratamiento": "Conservar faltantes justificados"
        },
        {
            "dimension": "Unicidad",
            "criterio": "Un registro por año",
            "resultado": (
                f"{datos['id_año'].duplicated().sum()} duplicados"
            ),
            "tratamiento": "Mantener llave temporal única"
        },
        {
            "dimension": "Validez",
            "criterio": "Cinco tasas laborales entre 0 y 100 %",
            "resultado": (f"{sum(resultado_validez.values())} " "valores fuera de rango"),
            "tratamiento": "Conservar valores válidos"
        },
        {
            "dimension": "Consistencia",
            "criterio": "Seis identidades contables laborales",
            "resultado": (f"{sum(resultado_consistencia.values())} " "inconsistencias"),
            "tratamiento": "Respetar tolerancias por redondeo"    
        },
        {
            "dimension": "Integridad",
            "criterio": "Conservación del PIB original",
            "resultado": (f"{resultado_integridad_pib['valores_pib_modificados']} " "valores modificados"),
            "tratamiento": "No modificar los valores originales"
        },
        {
            "dimension": "Valores atípicos",
            "criterio": "Detección mediante IQR",
            "resultado": (f"{sum(resultado_atipicos.values())} " "valores atípicos detectados"),
            "tratamiento": "Conservar observaciones justificadas"
        }
    ])

    print("\nMATRIZ DE CALIDAD DE DATOS")
    print(matriz.to_string(index=False))

    return matriz

def comparar_antes_despues(antes, despues):
    """
    Compara los datos antes y después de normalizar
    las escalas poblacionales, sin modificarlos.
    """
    columnas = ["poblacion_total", "pet"]

    comparacion = antes[["id_año"] + columnas].merge(
        despues[["id_año"] + columnas],
        on="id_año",
        how="outer",
        validate="one_to_one",
        suffixes=("_antes", "_despues"),
        indicator=True
    )

    if not comparacion["_merge"].eq("both").all():
        raise ValueError(
            "Los años no coinciden antes y después de la normalización."
        )

    comparacion = comparacion.drop(columns="_merge")

    print("\nCOMPARACIÓN ANTES Y DESPUÉS DE LA NORMALIZACIÓN")

    for columna in columnas:
        comparacion[f"cambio_{columna}"] = (
            comparacion[f"{columna}_despues"]
            - comparacion[f"{columna}_antes"]
        )

        cantidad = int(
            comparacion[f"cambio_{columna}"].fillna(0).ne(0).sum()
        )

        print(f"{columna}: {cantidad} registros modificados")

    print(comparacion.to_string(index=False))

    columnas_comunes = [
        columna for columna in antes.columns
        if columna in despues.columns
        and columna not in ["id_año"] + columnas
    ]

    otros_cambios = 0

    for columna in columnas_comunes:
        originales = antes.set_index("id_año")[columna]
        normalizados = despues.set_index("id_año")[columna]

        if not originales.equals(normalizados):
            otros_cambios += 1
            print(f"Revisar cambios adicionales en: {columna}")

    print(f"Otras columnas modificadas: {otros_cambios}")

    return comparacion


def analizar_periodo_2019_2021(datos):
    """
    Compara indicadores económicos y laborales
    del Tolima entre 2019 y 2021.
    No modifica los datos originales.
    """
    columnas = [
        "id_año",
        "pib_constante_2015",
        "crec_pib_real",
        "poblacion_ocupada",
        "poblacion_desocupada",
        "tgp",
        "to",
        "td"
    ]

    comparacion = datos.loc[
        datos["id_año"].isin([2019, 2020, 2021]),
        columnas
    ].copy()

    comparacion = comparacion.sort_values("id_año")

    if comparacion["id_año"].tolist() != [2019, 2020, 2021]:
        raise ValueError(
            "Faltan años necesarios para el análisis 2019-2021."
        )

    print("\nANÁLISIS ECONÓMICO Y LABORAL 2019-2021")
    print(comparacion.to_string(index=False))

    return comparacion


def comparar_calidad_antes_despues(antes, despues):
    """
    Compara la calidad del conjunto integrado antes y
    después de incorporar los indicadores derivados.
    No modifica los datos.
    """
    indicadores_anuales = [
        "crec_pib_real",
        "var_ocupados",
        "var_desocupados"
    ]

    faltantes_antes = int(antes.isna().sum().sum())
    faltantes_despues = int(despues.isna().sum().sum())

    faltantes_derivados = int(
        despues[indicadores_anuales].isna().sum().sum()
    )

    comparacion = pd.DataFrame({
        "Indicador": [
            "Registros",
            "Columnas",
            "Años duplicados",
            "Valores faltantes",
            "Valores faltantes derivados",
            "Suma del PIB real"
        ],
        "Antes": [
            len(antes),
            antes.shape[1],
            int(antes["id_año"].duplicated().sum()),
            faltantes_antes,
            int(antes[indicadores_anuales].isna().sum().sum()),
            antes["pib_constante_2015"].sum()
        ],
        "Después": [
            len(despues),
            despues.shape[1],
            int(despues["id_año"].duplicated().sum()),
            faltantes_despues,
            faltantes_derivados,
            despues["pib_constante_2015"].sum()
        ]
    })

    print("\nCOMPARACIÓN GENERAL DE CALIDAD ANTES Y DESPUÉS")
    print(comparacion.to_string(index=False))

    if len(antes) != len(despues):
        raise ValueError("Se modificó la cantidad de registros.")

    if not antes["id_año"].equals(despues["id_año"]):
        raise ValueError("Se modificó la secuencia de años.")

    if antes["pib_constante_2015"].sum() != despues["pib_constante_2015"].sum():
        raise ValueError("Se modificó la suma del PIB real.")

    indicadores_nuevos = [
        columna for columna in despues.columns
        if columna not in antes.columns
    ]

    faltantes_nuevos = int(
        despues[indicadores_nuevos].isna().sum().sum()
    )

    if faltantes_despues - faltantes_antes != faltantes_nuevos:
        raise ValueError(
            "Los faltantes adicionales no corresponden "
            "a las columnas incorporadas."
        )

    print("COMPARACIÓN GENERAL DE CALIDAD VALIDADA")

    return comparacion


def diagnosticar_faltantes_laborales(datos):
    """
    Identifica los años y porcentajes de valores faltantes
    en tres variables laborales del proyecto.

    No modifica ni imputa los datos.
    """
    columnas = [
        "ts",
        "poblacion_subocupada",
        "fuerza_trabajo_potencial"
    ]

    total_registros = len(datos)
    resultados = []

    print("\nDIAGNÓSTICO INDIVIDUAL DE FALTANTES LABORALES")

    for columna in columnas:
        faltantes = datos[columna].isna()

        cantidad = int(faltantes.sum())

        porcentaje = (
            cantidad / total_registros * 100
            if total_registros > 0 else 0
        )

        anios_faltantes = datos.loc[
            faltantes, "id_año"
        ].tolist()

        resultados.append({
            "variable": columna,
            "valores_faltantes": cantidad,
            "porcentaje_faltantes": round(porcentaje, 2),
            "anios_faltantes": str(anios_faltantes)
        })

        print(f"\nVariable: {columna}")
        print(f"Valores faltantes: {cantidad}")
        print(f"Porcentaje: {porcentaje:.2f}%")
        print(f"Años afectados: {anios_faltantes}")

    diagnostico = pd.DataFrame(resultados)

    print("\nRESUMEN DEL DIAGNÓSTICO")
    print(diagnostico.to_string(index=False))

    return diagnostico


def generar_matriz_decisiones_faltantes(diagnostico):
    """
    Documenta las decisiones de tratamiento de los
    valores faltantes de las variables laborales.
    No modifica ni imputa los datos.
    """
    decisiones = {
        "ts": {
            "tratamiento": "Conservar valor faltante",
            "justificacion": (
                "Dato no disponible para 2020. "
                "No se inventan valores."
            )
        },
        "poblacion_subocupada": {
            "tratamiento": "Conservar valor faltante",
            "justificacion": (
                "Dato no disponible para 2020. "
                "No se realiza imputacion."
            )
        },
        "fuerza_trabajo_potencial": {
            "tratamiento": "Conservar valores faltantes",
            "justificacion": (
                "Solo hay datos entre 2021 y 2025. "
                "No se extrapolan años anteriores."
            )
        }
    }

    matriz = diagnostico.copy()

    matriz["tratamiento"] = matriz["variable"].map(
        lambda variable: decisiones[variable]["tratamiento"]
    )

    matriz["justificacion"] = matriz["variable"].map(
        lambda variable: decisiones[variable]["justificacion"]
    )

    print("\nMATRIZ DE DECISIONES SOBRE VALORES FALTANTES")
    print(matriz.to_string(index=False))

    return matriz


def comparar_tratamiento_faltantes(datos):
    """
    Audita la estrategia de conservación de faltantes.
    Comprueba que no se alteren registros ni estadísticas.
    """
    columnas = [
        "ts",
        "poblacion_subocupada",
        "fuerza_trabajo_potencial"
    ]

    antes = datos[columnas].copy(deep=True)

    # Tratamiento adoptado: conservar los NaN.
    despues = antes.copy(deep=True)

    resultados = []

    for variable in columnas:
        resultados.append({
            "variable": variable,
            "faltantes_antes": int(antes[variable].isna().sum()),
            "faltantes_despues": int(despues[variable].isna().sum()),
            "media_antes": antes[variable].mean(),
            "media_despues": despues[variable].mean(),
            "mediana_antes": antes[variable].median(),
            "mediana_despues": despues[variable].median()
        })

    comparacion = pd.DataFrame(resultados).round(2)

    if not antes.equals(despues):
        raise ValueError(
            "El tratamiento modificó los datos originales."
        )

    if len(antes) != len(despues):
        raise ValueError(
            "El tratamiento modificó la cantidad de registros."
        )

    print("\nCOMPARACIÓN DEL TRATAMIENTO DE FALTANTES")
    print(f"Registros antes: {len(antes)}")
    print(f"Registros después: {len(despues)}")
    print(comparacion.to_string(index=False))
    print("CONSERVACIÓN DE FALTANTES VALIDADA")

    return comparacion


def comparar_calidad_global(mercado_laboral, pib, datos_finales):
    """
    Compara la estructura inicial integrada de las
    dos fuentes con el dataset final del proceso ETL.
    """

    datos_iniciales = mercado_laboral.merge(
        pib[["año_id", "pib_constante_2015"]],
        left_on="id_año",
        right_on="año_id",
        how="inner",
        validate="one_to_one"
    ).drop(columns=["año_id"])

    comparacion = pd.DataFrame({
        "Indicador": [
            "Registros",
            "Columnas",
            "Años duplicados",
            "Valores faltantes",
            "Suma del PIB real"
        ],
        "Antes": [
            len(datos_iniciales),
            datos_iniciales.shape[1],
            int(datos_iniciales["id_año"].duplicated().sum()),
            int(datos_iniciales.isna().sum().sum()),
            datos_iniciales["pib_constante_2015"].sum()
        ],
        "Después": [
            len(datos_finales),
            datos_finales.shape[1],
            int(datos_finales["id_año"].duplicated().sum()),
            int(datos_finales.isna().sum().sum()),
            datos_finales["pib_constante_2015"].sum()
        ]
    })

    if len(datos_iniciales) != len(datos_finales):
        raise ValueError("Se modificó la cantidad de registros.")

    if datos_iniciales["id_año"].tolist() != datos_finales["id_año"].tolist():
        raise ValueError("Se modificó la cobertura temporal.")

    if (
        datos_iniciales["pib_constante_2015"].sum()
        != datos_finales["pib_constante_2015"].sum()
    ):
        raise ValueError("Se modificó la suma del PIB real.")

    print("\nCOMPARACIÓN GLOBAL DE CALIDAD DEL PROCESO ETL")
    print(comparacion.to_string(index=False))
    print("COMPARACIÓN GLOBAL VALIDADA")

    return comparacion


def documentar_transformaciones():
    """Documenta las transformaciones analíticas del proyecto."""

    transformaciones = pd.DataFrame([
        {
            "numero": 1,
            "transformacion": "Crecimiento anual del PIB real",
            "variable": "crec_pib_real",
            "justificacion": "Medir la variacion porcentual anual del PIB real"
        },
        {
            "numero": 2,
            "transformacion": "Variacion anual de ocupados",
            "variable": "var_ocupados",
            "justificacion": "Medir los cambios porcentuales de la ocupacion"
        },
        {
            "numero": 3,
            "transformacion": "Variacion anual de desocupados",
            "variable": "var_desocupados",
            "justificacion": "Medir los cambios porcentuales de la desocupacion"
        },
        {
            "numero": 4,
            "transformacion": "PIB real por ocupado",
            "variable": "pib_por_ocupado",
            "justificacion": "Relacionar la produccion real con los ocupados"
        },
        {
            "numero": 5,
            "transformacion": "Ocupados por cada mil PET",
            "variable": "ocupados_por_mil_pet",
            "justificacion": "Medir la proporcion de ocupados respecto a la PET"
        },
        {
            "numero": 6,
            "transformacion": "Brecha entre TGP y TO",
            "variable": "brecha_tgp_to",
            "justificacion": "Medir la diferencia entre participacion y ocupacion"
        }
    ])

    print("\nDOCUMENTACION DE LAS TRANSFORMACIONES ANALITICAS")
    print(transformaciones.to_string(index=False))

    return transformaciones