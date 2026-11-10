from pathlib import Path
from src.extraction import (
    cargar_excel,
    explorar_fuente,
    comparar_fuentes_iniciales
)
from src.cleaning import (
    limpiar_columnas,
    limpiar_anios,
    convertir_tasas_numericas,
    normalizar_escalas_poblacionales
)
from src.transformation import (
    transformar_pib,
    transformar_mercado_laboral,
    transformar_datos_integrados
)
from src.integration import integrar_datos
from src.validation import (
    validar_datos_integrados,
    validar_tasas_laborales,
    validar_consistencia_laboral,
    validar_valores_positivos,
    validar_indicadores_derivados,
    detectar_valores_atipicos,
    validar_integridad_pib,
    validar_cobertura_temporal,
    validar_poblaciones_no_negativas,
    validar_reglas_indicadores
)
from src.audit import (
    generar_reporte_completitud,
    generar_estadisticas_descriptivas,
    generar_matriz_calidad,
    comparar_antes_despues,
    analizar_periodo_2019_2021,
    comparar_calidad_antes_despues,
    diagnosticar_faltantes_laborales,
    generar_matriz_decisiones_faltantes,
    comparar_tratamiento_faltantes,
    comparar_calidad_global,
    documentar_transformaciones
)

def main():
    ruta_proyecto = Path(__file__).resolve().parent
    ruta_raw = ruta_proyecto / "data" / "raw"

    pib = cargar_excel(
        ruta_raw / "pib_departamental.xlsx",
        ["año_id", "pib_departamento", "pib_constante_2015"]
    )

    mercado_laboral = cargar_excel(
        ruta_raw / "mercado_laboral_tolima.xlsx",
        ["id_año", "mer_departamento", "tgp", "to", "td"]
    )

    explorar_fuente(
        "PIB departamental",
        pib
    )

    explorar_fuente(
        "Mercado laboral del Tolima",
        mercado_laboral
    )

    comparacion_fuentes = comparar_fuentes_iniciales(
        pib,
        mercado_laboral
    )


    print("EXTRACCIÓN COMPLETADA")
    print(f"PIB: {pib.shape[0]} filas y {pib.shape[1]} columnas")
    print(
            f"Mercado laboral: {mercado_laboral.shape[0]} filas "
            f"y {mercado_laboral.shape[1]} columnas"
        )

    pib = limpiar_columnas(pib)
    pib = limpiar_anios(pib, "año_id")

    mercado_laboral = limpiar_columnas(mercado_laboral)
    mercado_laboral = limpiar_anios(mercado_laboral, "id_año")
    mercado_laboral = convertir_tasas_numericas(mercado_laboral)
    
    resultado_cobertura = validar_cobertura_temporal(pib, mercado_laboral)

    pib_base = pib.copy(deep=True)
    mercado_laboral_base = mercado_laboral.copy(deep=True)

    print("LIMPIEZA COMPLETADA")

    pib = transformar_pib(pib)

    mercado_laboral = transformar_mercado_laboral(mercado_laboral)

    print("TRANSFORMACIÓN COMPLETADA")
    print("Indicadores del PIB:")
    print(pib[["año_id", "crec_pib_real"]].tail())

    print("Indicadores del mercado laboral:")
    print(
        mercado_laboral[
            ["id_año", "var_ocupados", "var_desocupados"]
        ].tail()
    )

    datos_integrados = integrar_datos(mercado_laboral, pib)

    datos_antes_normalizacion = datos_integrados.copy(deep=True)

    datos_integrados = normalizar_escalas_poblacionales(datos_integrados)
    comparacion_transformaciones = comparar_antes_despues(
    datos_antes_normalizacion,
    datos_integrados
)
    print("ESCALAS POBLACIONALES NORMALIZADAS")

    datos_antes_indicadores = datos_integrados.copy(deep=True)

    datos_integrados = transformar_datos_integrados(datos_integrados)

    tabla_transformaciones = documentar_transformaciones()

    comparacion_calidad = comparar_calidad_antes_despues(datos_antes_indicadores, datos_integrados)
    
    print("TIPOS DE DATOS INTEGRADOS:")
    print(
        datos_integrados[
            ["id_año", "td", "tgp", "to", "poblacion_ocupada"]
        ].dtypes
    )

    print("INTEGRACIÓN COMPLETADA")
    print(
        f"Datos integrados: {datos_integrados.shape[0]} filas "
        f"y {datos_integrados.shape[1]} columnas"
    )

    print("Años integrados:")
    print(datos_integrados["id_año"].tolist())

    print("Primeros registros integrados:")
    print(
        datos_integrados[
            ["id_año", "pib_constante_2015", "td"]
        ].head()
    )

    datos_integrados = validar_datos_integrados(datos_integrados)
    datos_integrados, resultado_reglas = validar_reglas_indicadores(datos_integrados)
    datos_integrados, resultado_validez = validar_tasas_laborales(datos_integrados)
    datos_integrados, resultado_consistencia = validar_consistencia_laboral(datos_integrados)
    datos_integrados = validar_valores_positivos(datos_integrados)
    datos_integrados, resultado_poblaciones = validar_poblaciones_no_negativas(datos_integrados)
    datos_integrados = validar_indicadores_derivados(datos_integrados)
    datos_integrados, resultado_atipicos = detectar_valores_atipicos(datos_integrados)
    datos_integrados, resultado_integridad_pib = validar_integridad_pib(datos_integrados, pib)

    reporte_completitud = generar_reporte_completitud(datos_integrados)

    diagnostico_faltantes = diagnosticar_faltantes_laborales(datos_integrados)

    matriz_decisiones_faltantes = generar_matriz_decisiones_faltantes(diagnostico_faltantes)

    comparacion_faltantes = comparar_tratamiento_faltantes(datos_integrados)

    estadisticas_descriptivas = generar_estadisticas_descriptivas(datos_integrados)

    matriz_calidad = generar_matriz_calidad(
    datos_integrados,
    reporte_completitud,
    resultado_integridad_pib,
    resultado_consistencia,
    resultado_validez,
    resultado_atipicos
)

    comparacion_2019_2021 = analizar_periodo_2019_2021(datos_integrados)

    comparacion_global = comparar_calidad_global(
        mercado_laboral_base,
        pib_base,
        datos_integrados
    )

    ruta_processed = ruta_proyecto / "data" / "processed"
    ruta_processed.mkdir(parents=True, exist_ok=True)

    archivo_csv = ruta_processed / "tolima_pib_mercado_laboral_2007_2025.csv"
    archivo_excel = ruta_processed / "tolima_pib_mercado_laboral_2007_2025.xlsx"

    # Exportar los datos integrados a CSV
    datos_integrados.to_csv(
        archivo_csv,
        index=False,
        encoding="utf-8-sig",
        sep=","
    )

    # Exportar los mismos datos a Excel
    datos_integrados.to_excel(
        archivo_excel,
        index=False,
        engine="openpyxl",
        sheet_name="Datos_Integrados"
    )

    import pandas as pd

    datos_csv = pd.read_csv(archivo_csv)
    datos_excel = pd.read_excel(archivo_excel)

    if datos_csv.shape != datos_integrados.shape:
        raise ValueError("El CSV no conserva las dimensiones de la tabla final.")

    if datos_excel.shape != datos_integrados.shape:
        raise ValueError("El Excel no conserva las dimensiones de la tabla final.")

    print("\n" + "=" * 55)
    print("EXPORTACIÓN COMPLETADA CORRECTAMENTE")
    print("=" * 55)
    print(f"Registros exportados: {datos_integrados.shape[0]}")
    print(f"Columnas exportadas: {datos_integrados.shape[1]}")
    print(f"Archivo CSV: {archivo_csv}")
    print(f"Archivo Excel: {archivo_excel}")
    print("Verificación de dimensiones: CORRECTA")
    print("=" * 55)

if __name__ == "__main__":
    main()