from pathlib import Path
import pandas as pd


def cargar_excel(ruta_archivo, columnas_requeridas):
    """
    Lee un archivo Excel y verifica su estructura.

    Parámetros:
        ruta_archivo: ubicación del archivo Excel.
        columnas_requeridas: columnas obligatorias.

    Retorna:
        DataFrame con los datos originales.
    """

    ruta_archivo = Path(ruta_archivo)

    # Verificar existencia del archivo
    if not ruta_archivo.is_file():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta_archivo}"
        )

    # Leer el Excel
    datos = pd.read_excel(ruta_archivo)

    # Comprobar que no esté vacío
    if datos.empty:
        raise ValueError(
            f"El archivo está vacío: {ruta_archivo.name}"
        )

    # Verificar columnas obligatorias
    faltantes = set(columnas_requeridas) - set(datos.columns)

    if faltantes:
        raise ValueError(
            f"Faltan columnas en {ruta_archivo.name}: "
            f"{sorted(faltantes)}"
        )

    return datos


def explorar_fuente(nombre, datos):
    """
    Presenta el perfil inicial de una fuente,
    sin modificar sus datos originales.
    """
    print("\n" + "=" * 60)
    print(f"EXPLORACIÓN INICIAL: {nombre}")
    print("=" * 60)

    print(f"Dimensiones: {datos.shape}")
    print(f"Columnas: {datos.columns.tolist()}")

    print("\nTipos de datos:")
    print(datos.dtypes.to_string())

    print("\nValores faltantes por columna:")
    print(datos.isna().sum().to_string())

    print("\nPrimeros cinco registros:")
    print(datos.head().to_string(index=False))


def comparar_fuentes_iniciales(pib, mercado_laboral):
    """
    Construye una comparación estructural de las
    dos fuentes antes de su limpieza.
    """
    comparacion = pd.DataFrame([
        {
            "archivo": "pib_departamental.xlsx",
            "variable_clave": "año_id",
            "registros": len(pib),
            "columnas": pib.shape[1],
            "valores_faltantes": int(pib.isna().sum().sum()),
            "anios_unicos": pib["año_id"].nunique()
        },
        {
            "archivo": "mercado_laboral_tolima.xlsx",
            "variable_clave": "id_año",
            "registros": len(mercado_laboral),
            "columnas": mercado_laboral.shape[1],
            "valores_faltantes": int(
                mercado_laboral.isna().sum().sum()
            ),
            "anios_unicos": mercado_laboral["id_año"].nunique()
        }
    ])

    print("\nTABLA COMPARATIVA INICIAL DE FUENTES")
    print(comparacion.to_string(index=False))

    return comparacion


def documentar_fuentes():
    """
    Documenta la procedencia de los datos utilizados
    durante la etapa de extracción del proyecto ETL.
    """

    fuentes = [
        {
            "archivo": "pib_departamental.xlsx",
            "entidad": "DANE",
            "publicacion": "Cuentas Nacionales Departamentales",
            "anexo_original": "anex-PIBDep-TotalDep-2025pr.xlsx",
            "periodo": "2007-2025",
            "preparacion": "Selección y organización de los datos del Tolima",
            "pagina_oficial": (
                "https://www.dane.gov.co/files/operaciones/PIB/"
                "anex-PIBDep-TotalDep-2025pr.xlsx"
                )
        },
        {
            "archivo": "mercado_laboral_tolima.xlsx",
            "entidad": "DANE",
            "publicacion": "Gran Encuesta Integrada de Hogares (GEIH)",
            "anexo_original": "anex-GEIHDepartamentos-2025.xls",
            "periodo": "2007-2025",
            "preparacion": "Selección y organización de los datos del Tolima",
            "pagina_oficial": (
                "https://www.dane.gov.co/files/operaciones/GEIH/"
                "anex-GEIHDepartamentos-2025.xls"
            )
        }
    ]

    print("\nDOCUMENTACIÓN DE LAS FUENTES DE INFORMACIÓN")

    for fuente in fuentes:
        print("\nArchivo preparado:", fuente["archivo"])
        print("Entidad:", fuente["entidad"])
        print("Publicación:", fuente["publicacion"])
        print("Anexo original:", fuente["anexo_original"])
        print("Período:", fuente["periodo"])
        print("Preparación:", fuente["preparacion"])
        print("Página oficial:", fuente["pagina_oficial"])

    return fuentes