# Proyecto integrador: PIB y mercado laboral del Tolima (2007–2025)

**Asignatura:** Fundamentos de Integración y Transformación de Datos  
**Modalidad:** Proyecto individual
**Área:** Economía y analítica de datos  
**Tecnologías:** Python, pandas y openpyxl  
**Cobertura:** Departamento del Tolima, Colombia · Datos anuales · 2007–2025

## 1. Descripción del proyecto

Este repositorio contiene un proceso ETL (*extracción, transformación y carga/exportación*) desarrollado en Python para integrar información económica y laboral del departamento del Tolima. Utiliza datos del Departamento Administrativo Nacional de Estadística (DANE) procedentes de dos publicaciones: las Cuentas Nacionales Departamentales y la Gran Encuesta Integrada de Hogares (GEIH).

**Objetivo:** construir una base anual integrada y verificable que permita describir la evolución del producto interno bruto (PIB) real, la ocupación y la desocupación del Tolima entre 2007 y 2025.

**Pregunta orientadora:** ¿Cómo evolucionaron el PIB real y los indicadores del mercado laboral del Tolima entre 2007 y 2025, y qué relaciones descriptivas pueden observarse entre ellos?

El análisis es **descriptivo**: las coincidencias entre variables no permiten establecer por sí solas relaciones causales.

## 2. Estructura del repositorio

```text
Proyecto_Integrador_Tolima/
├── data/
│   ├── raw/
│   │   ├── pib_departamental.xlsx
│   │   └── mercado_laboral_tolima.xlsx
│   └── processed/
│       ├── tolima_pib_mercado_laboral_2007_2025.csv
│       └── tolima_pib_mercado_laboral_2007_2025.xlsx
├── docs/
│   └── Informe_Integrador_PIB_Mercado_Laboral_Tolima.docx
├── src/
│   ├── extraction.py
│   ├── cleaning.py
│   ├── transformation.py
│   ├── integration.py
│   ├── validation.py
│   └── audit.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

- **`main.py`:** coordina la ejecución del proceso y la exportación de resultados.
- **`src/`:** contiene los módulos de extracción, limpieza, transformación, integración, validación y auditoría.
- **`data/raw/`:** contiene los dos Excel **preparados para el ETL** a partir de los anexos oficiales del DANE; no son copias sin modificar de los anexos originales.
- **`data/processed/`:** almacena los archivos integrados que genera el programa.
- **`docs/`:** contiene el informe académico.
- **`requirements.txt`:** especifica las bibliotecas de Python necesarias.

La carpeta `.venv/` se genera localmente al crear el entorno virtual y está excluida del repositorio mediante `.gitignore`. Las dependencias necesarias para ejecutar el proyecto están especificadas en `requirements.txt`.

## 3. Requisitos previos

Para reproducir el proyecto en **Windows**, se necesita:

1. **Python**, con una versión compatible con las dependencias de `requirements.txt`. Puede descargarse desde [python.org](https://www.python.org/downloads/).
2. **Conexión a Internet** durante la instalación de las bibliotecas, si no están disponibles localmente.
3. **Git** para clonar el repositorio, o bien descargarlo como archivo ZIP desde GitHub.
4. Los archivos de entrada incluidos en `data/raw/` del repositorio.

Los comandos siguientes están preparados para la terminal de Windows (PowerShell). Puede abrirla directamente o desde **Terminal → Nueva terminal** en [Visual Studio Code](https://code.visualstudio.com/). Visual Studio Code es opcional.

Para comprobar las herramientas instaladas, abra la terminal y ejecute:

```powershell
py --version
git --version
```

Si `py` no está disponible, compruebe la instalación con `python --version`. Si no tiene Git, puede usar la descarga ZIP descrita a continuación.

## 4. Instalación y ejecución en Windows

### Paso 1. Obtener el proyecto

En la terminal, ubíquese en la carpeta donde desea guardar el repositorio y ejecute:

```powershell
git clone https://github.com/StefaniaRodriguez/Proyecto_Integrador_Tolima.git
cd Proyecto_Integrador_Tolima
```

**Alternativa sin Git:** entre al [repositorio de GitHub](https://github.com/StefaniaRodriguez/Proyecto_Integrador_Tolima), seleccione **Code → Download ZIP**, descomprima el archivo y abra en la terminal la carpeta que contiene `main.py`.

### Paso 2. Identificar los archivos de entrada

El repositorio incluye los siguientes archivos de entrada, preparados a partir de las publicaciones oficiales del DANE:

```text
data/raw/pib_departamental.xlsx
data/raw/mercado_laboral_tolima.xlsx
```

Para visualizar los archivos desde la terminal:

```powershell
Get-ChildItem
Get-ChildItem data/raw
```

Estos son los archivos que lee el programa. Su procedencia, selección de variables y preparación se documentan en la sección 6.

### Paso 3. Crear el entorno virtual

Desde la carpeta raíz del proyecto:

```powershell
py -m venv .venv
```

No es necesario activar el entorno virtual: los siguientes comandos utilizan directamente su intérprete de Python.

### Paso 4. Instalar las dependencias

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

El archivo `requirements.txt` del proyecto declara las siguientes versiones:

```text
pandas==3.1.1
openpyxl==3.1.5
```

Para comprobar que están instaladas:

```powershell
.\.venv\Scripts\python.exe -m pip show pandas openpyxl
```

### Paso 5. Ejecutar el proceso ETL

```powershell
.\.venv\Scripts\python.exe main.py
```

El programa muestra en la terminal la documentación de las fuentes, el diagnóstico inicial, las transformaciones, las validaciones y la exportación de resultados.

### Paso 6. Comprobar los resultados

Una ejecución correcta con los archivos documentados termina con un mensaje equivalente a:

```text
EXPORTACIÓN COMPLETADA CORRECTAMENTE
Registros exportados: 19
Columnas exportadas: 22
Verificación de dimensiones: CORRECTA
```

Los resultados se guardan en:

| Archivo | Utilidad |
|---|---|
| `data/processed/tolima_pib_mercado_laboral_2007_2025.xlsx` | Consulta en Excel; hoja `Datos_Integrados` |
| `data/processed/tolima_pib_mercado_laboral_2007_2025.csv` | Análisis en Python, R, Power BI u otras herramientas |

El CSV utiliza **coma** como delimitador y codificación **`utf-8-sig`**. Si Excel lo muestra en una sola columna, impórtelo especificando el delimitador coma o abra el archivo `.xlsx`.

## 5. Funcionamiento del proceso ETL

| Etapa | Módulo | Actividad |
|---|---|---|
| Extracción y diagnóstico inicial | `src/extraction.py` | Lee los Excel, identifica columnas, tipos de datos, dimensiones y faltantes, y documenta su procedencia. |
| Limpieza | `src/cleaning.py` | Estandariza nombres, años, separadores decimales y escalas poblacionales. |
| Transformaciones por fuente | `src/transformation.py` | Calcula variaciones interanuales del PIB y de las poblaciones ocupada y desocupada. |
| Integración | `src/integration.py` | Une las dos fuentes mediante el año y comprueba la cobertura temporal. |
| Transformaciones integradas | `src/transformation.py` | Calcula indicadores que relacionan las variables económicas y laborales. |
| Validación | `src/validation.py` | Revisa rangos, duplicados, consistencia laboral, indicadores derivados e integridad del PIB. |
| Auditoría | `src/audit.py` | Presenta diagnósticos de completitud, valores atípicos y comparaciones antes/después. |
| Exportación | `main.py` | Genera los archivos CSV y Excel y verifica sus dimensiones. |

### Indicadores analíticos calculados

| Indicador | Variable | Cálculo o interpretación |
|---|---|---|
| Crecimiento anual del PIB real | `crec_pib_real` | Variación porcentual del PIB real respecto al año anterior. |
| Variación anual de ocupados | `var_ocupados` | Variación porcentual de la población ocupada. |
| Variación anual de desocupados | `var_desocupados` | Variación porcentual de la población desocupada. |
| PIB real por ocupado | `pib_por_ocupado` | PIB real dividido entre población ocupada. |
| Ocupados por cada mil PET | `ocupados_por_mil_pet` | Población ocupada / población en edad de trabajar × 1.000. |
| Brecha entre TGP y TO | `brecha_tgp_to` | Diferencia entre la tasa global de participación y la tasa de ocupación, en puntos porcentuales. |

Las tres variaciones interanuales presentan un valor faltante en **2007**, porque el conjunto de datos no incluye el año anterior. Las unidades del PIB por ocupado dependen de las unidades de las fuentes integradas.

## 6. Fuentes de información y trazabilidad

Las fuentes estadísticas utilizadas pertenecen al **Departamento Administrativo Nacional de Estadística (DANE)**. Los archivos de entrada fueron preparados seleccionando el departamento del Tolima, el período **2007–2025** y las variables necesarias para el análisis.

### Fuente 1. PIB departamental

- **Entidad:** DANE.
- **Publicación:** Cuentas Nacionales Departamentales.
- **Anexo oficial:** `anex-PIBDep-TotalDep-2025pr.xlsx`.
- **Hoja de origen:** `Cuadro 2`.
- **Información seleccionada:** PIB departamental del Tolima en volumen, con año de referencia 2015.
- **Período utilizado:** 2007–2025.
- **Archivo preparado para el ETL:** `data/raw/pib_departamental.xlsx`.
- **[Página institucional de la publicación](https://www.dane.gov.co/index.php/estadisticas-por-tema/cuentas-nacionales/cuentas-nacionales-departamentales)**.
- **[Descarga directa del anexo oficial](https://www.dane.gov.co/files/operaciones/PIB/anex-PIBDep-TotalDep-2025pr.xlsx)**.
- **Fecha de consulta:** 28 de agosto de 2026.

La publicación identifica **2024 como provisional (`2024p`)** y **2025 como preliminar (`2025pr`)**.

### Fuente 2. Mercado laboral departamental

- **Entidad:** DANE.
- **Publicación:** Gran Encuesta Integrada de Hogares (GEIH), mercado laboral por departamentos.
- **Anexo oficial:** `anex-GEIHDepartamentos-2025.xls`.
- **Hoja de origen:** `Departamentos anual`, bloque correspondiente al Tolima.
- **Información seleccionada:** indicadores anuales de población, participación, ocupación y desocupación.
- **Período utilizado:** 2007–2025.
- **Archivo preparado para el ETL:** `data/raw/mercado_laboral_tolima.xlsx`.
- **[Página institucional de la publicación](https://www.dane.gov.co/index.php/estadisticas-por-tema/mercado-laboral/mercado-laboral-por-departamentos)**.
- **[Descarga directa del anexo oficial](https://www.dane.gov.co/files/operaciones/GEIH/anex-GEIHDepartamentos-2025.xls)**.
- **Fecha de consulta:** 28 de agosto de 2026.

### Preparación de las entradas

Los anexos oficiales contienen más información que la utilizada por este proyecto. Para construir los archivos de `data/raw/` se seleccionaron los registros anuales del Tolima y se organizaron las variables con los nombres y el redondeo empleados por el ETL.

| Archivo preparado | Dimensiones iniciales | Llave temporal |
|---|---:|---|
| `pib_departamental.xlsx` | 19 filas × 3 columnas | `año_id` |
| `mercado_laboral_tolima.xlsx` | 19 filas × 15 columnas | `id_año` |

En la preparación del archivo laboral, los valores cero registrados en el anexo oficial para las variables de subocupación de **2020** se representaron como faltantes en la entrada preparada. Esta decisión se conserva y documenta durante el ETL, sin sustituirlos por cifras estimadas. La variable `fuerza_trabajo_potencial` presenta valores faltantes para **2007–2020** en la entrada preparada.

El pipeline utiliza los dos archivos Excel preparados incluidos en `data/raw/`. Los enlaces a los anexos oficiales permiten consultar la procedencia de las cifras; la descarga y la selección inicial de datos de esos anexos no forman parte de la ejecución automatizada.

## 7. Resultados y calidad de los datos

Con los archivos de entrada documentados, la ejecución comprobada produjo:

| Verificación | Resultado |
|---|---|
| Cobertura temporal | 2007–2025 |
| Registros integrados | 19 |
| Columnas finales | 22 |
| Años duplicados | 0 |
| Años sin correspondencia entre fuentes | 0 |
| Valores faltantes finales | 19 |
| Inconsistencias en indicadores derivados | 0 |
| Inconsistencias en identidades laborales verificadas | 0 |
| Valores del PIB modificados durante la integración | 0 |
| Suma del PIB real antes y después | 330.295, en unidades de la fuente |
| Valores atípicos señalados por IQR | 2: población desocupada y tasa de desempleo en 2020 |
| Archivos exportados | CSV y Excel, ambos con 19 filas y 22 columnas |

### Valores faltantes

Los **19 valores faltantes finales** se distribuyen así:

| Variable | Cantidad | Motivo documentado |
|---|---:|---|
| `ts` | 1 | Valor de 2020 tratado como no disponible en el archivo preparado. |
| `poblacion_subocupada` | 1 | Valor de 2020 tratado como no disponible en el archivo preparado. |
| `fuerza_trabajo_potencial` | 14 | Sin valores en el archivo preparado para 2007–2020. |
| `crec_pib_real` | 1 | No existe un año anterior a 2007 para calcular la variación. |
| `var_ocupados` | 1 | No existe un año anterior a 2007 para calcular la variación. |
| `var_desocupados` | 1 | No existe un año anterior a 2007 para calcular la variación. |

Los **16 faltantes iniciales de los archivos preparados** se conservan; los **3 restantes** aparecen al calcular las variaciones interanuales de 2007. No se imputan valores ni se eliminan automáticamente las observaciones atípicas.

### Ejemplo de lectura de los resultados: 2019–2021

| Año | PIB real | Población ocupada | Tasa de desempleo |
|---:|---:|---:|---:|
| 2019 | 18.512 | 536 | 16,6 % |
| 2020 | 17.149 | 459 | 23,2 % |
| 2021 | 18.733 | 473 | 16,3 % |

Entre 2019 y 2020, el PIB real disminuyó aproximadamente **7,36 %** y la población ocupada pasó de **536 a 459**, en las unidades utilizadas por la fuente. La tasa de desempleo aumentó de **16,6 % a 23,2 %**. En 2021, el PIB real creció aproximadamente **9,24 %** frente a 2020. Estas observaciones no demuestran causalidad.

Para el análisis metodológico completo, consulte el informe disponible en `docs/`.

## 8. Solución de problemas frecuentes

| Situación | Qué hacer |
|---|---|
| `py` no se reconoce | Compruebe que Python esté instalado; pruebe `python --version`. |
| `git` no se reconoce | Instale Git o descargue el repositorio como ZIP. |
| `No module named pandas` o `openpyxl` | Instale las dependencias con `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`. |
| La terminal bloquea la activación de `.venv` | No es necesario activarlo: ejecute `.\.venv\Scripts\python.exe main.py`. |
| `FileNotFoundError` | Ejecute el programa desde la carpeta raíz del repositorio y verifique que los dos Excel estén en `data/raw/`. |
| Error por columnas faltantes o datos incompatibles | Verifique que los archivos de `data/raw/` no hayan sido modificados. |
| No se encuentra `main.py` | Abra la carpeta raíz del repositorio y compruébelo con `Get-ChildItem`. |
| El CSV se abre en una sola columna | Impórtelo con delimitador coma o abra el `.xlsx`. |
| No se generan archivos en `data/processed/` | Revise el error mostrado en la terminal; la exportación solo se confirma al terminar correctamente el proceso. |

## 9. Reproducibilidad y alcance

Para repetir el análisis con las mismas entradas, ejecute nuevamente `main.py` desde la carpeta raíz. El programa genera los resultados en `data/processed/` y comprueba las dimensiones de los archivos exportados.

Con las entradas incluidas en el repositorio, el resultado esperado es una base integrada de **19 registros y 22 columnas**, correspondiente al período 2007–2025.

La ejecución documentada se realizó en **Windows**. La compatibilidad con otros sistemas operativos no se ha verificado en este proyecto.

## 10. Referencias

- Departamento Administrativo Nacional de Estadística (DANE). (2025). *Cuentas Nacionales Departamentales: anexo PIB departamental 2025pr* [Archivo Excel]. Consultado el 28 de agosto de 2026. https://www.dane.gov.co/files/operaciones/PIB/anex-PIBDep-TotalDep-2025pr.xlsx
- Departamento Administrativo Nacional de Estadística (DANE). (2025). *Gran Encuesta Integrada de Hogares: anexo de mercado laboral por departamentos, 2025* [Archivo Excel]. Consultado el 28 de agosto de 2026. https://www.dane.gov.co/files/operaciones/GEIH/anex-GEIHDepartamentos-2025.xls