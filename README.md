# Proyecto integrador: PIB y mercado laboral del Tolima (2007–2025)

**Asignatura:** Fundamentos de Integración y Transformación de Datos  
**Área:** Economía y analítica de datos  
**Tecnologías:** Python, pandas y openpyxl  
**Cobertura:** Tolima, Colombia · Frecuencia anual · 2007–2025

## 1. Descripción y objetivo

Este repositorio contiene un **pipeline ETL** (extracción, transformación y carga/exportación) en Python que integra dos fuentes estadísticas del Departamento Administrativo Nacional de Estadística (DANE):

- Producto interno bruto (PIB) departamental a precios constantes de 2015.
- Indicadores del mercado laboral del Tolima.

**Objetivo:** construir una base anual integrada, consistente y reproducible para describir la evolución de la actividad económica, la ocupación y la desocupación del Tolima, preservando los archivos originales y documentando las decisiones de calidad.

**Pregunta orientadora:** ¿Cómo evolucionaron el PIB real y los indicadores del mercado laboral del Tolima entre 2007 y 2025, y qué relaciones descriptivas pueden observarse entre ellos?

> **Alcance:** las comparaciones permiten un análisis descriptivo; por sí solas no demuestran relaciones causales entre el PIB y el empleo.

## 2. Contenido del repositorio

- **Código fuente:** módulos de extracción, limpieza, transformación, integración, validación y auditoría.
- **Datos originales:** dos libros Excel en `data/raw/`.
- **Datos procesados:** archivos CSV y Excel en `data/processed/`.
- **Informe académico:** documento Word en `docs/`.
- **Dependencias:** `requirements.txt`.

### Estructura de carpetas

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

La carpeta `outputs/`, si se crea, puede reservarse para salidas adicionales; el pipeline actual exporta a `data/processed/`. El entorno virtual `.venv/`, los archivos temporales de Python y la configuración local de VS Code se excluyen mediante `.gitignore`.

## 3. Guía rápida de ejecución (Windows)

**Requisitos:** Python compatible con las dependencias del proyecto y Git (o descargar el ZIP desde GitHub).

Abra **PowerShell** en la carpeta donde desee descargar el proyecto y ejecute los comandos en este orden:

```powershell
# 1. Descargar el repositorio
git clone https://github.com/StefaniaRodriguez/Proyecto_Integrador_Tolima.git

# 2. Entrar a la carpeta
cd Proyecto_Integrador_Tolima

# 3. Crear un entorno virtual
py -m venv .venv

# 4. Instalar las dependencias
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 5. Ejecutar el pipeline
.\.venv\Scripts\python.exe main.py
```

> **Nota:** no es necesario activar el entorno virtual para utilizar los comandos anteriores. Si ya está activado y la terminal muestra `(.venv)`, también puede ejecutar `python -m pip install -r requirements.txt` y `python main.py`.

Al finalizar, revise la carpeta `data/processed/`.

## 4. Instalación detallada desde cero

### Paso 1. Instalar Python

1. Descargue Python desde [python.org/downloads](https://www.python.org/downloads/).
2. Instale una versión compatible con `pandas` y `openpyxl` indicadas en `requirements.txt`.
3. Abra PowerShell y compruebe la instalación:

```powershell
py --version
```

Si `py` no funciona, pruebe `python --version`. La compatibilidad con versiones distintas a la utilizada en el desarrollo debe verificarse ejecutando el proyecto.

### Paso 2. Instalar Visual Studio Code (opcional)

1. Descargue [Visual Studio Code](https://code.visualstudio.com/).
2. Instale la extensión **Python** de Microsoft.
3. Abra la carpeta raíz `Proyecto_Integrador_Tolima` desde **File → Open Folder**.
4. Abra **Terminal → New Terminal**.

VS Code es recomendado, pero no indispensable; el proyecto también se puede ejecutar desde PowerShell.

### Paso 3. Instalar Git y obtener el proyecto

Descargue Git desde [git-scm.com/downloads](https://git-scm.com/downloads) y compruebe:

```powershell
git --version
```

Clone el repositorio con el comando de la sección 3. Si no desea instalar Git, abra el [repositorio](https://github.com/StefaniaRodriguez/Proyecto_Integrador_Tolima), seleccione **Code → Download ZIP**, descomprímalo y abra la carpeta que contiene `main.py`.

### Paso 4. Comprobar la carpeta de trabajo

En PowerShell, dentro de la carpeta raíz, ejecute:

```powershell
Get-Location
Get-ChildItem
```

Debe encontrar `main.py`, `requirements.txt`, `src/`, `data/` y `docs/`.

### Paso 5. Crear el entorno virtual

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe --version
```

Si desea activar el entorno, puede utilizar:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell impide la activación, puede omitirla y utilizar directamente `\.venv\Scripts\python.exe` precedido de `.` como se muestra en los comandos anteriores (`.\.venv\Scripts\python.exe`). No necesita cambiar la política de seguridad del equipo.

En VS Code puede seleccionar el intérprete mediante **Ctrl + Shift + P → Python: Select Interpreter → `.venv\Scripts\python.exe`**.

### Paso 6. Instalar y comprobar las dependencias

El archivo `requirements.txt` del proyecto declara:

```text
pandas==3.1.1
openpyxl==3.1.5
```

Instale y compruebe:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip show pandas openpyxl
```

Se necesita conexión a Internet para descargar bibliotecas no disponibles localmente. Si una versión no es compatible con el intérprete instalado, revise el mensaje de `pip` y vuelva a verificar el pipeline antes de modificar las dependencias.

### Paso 7. Verificar los archivos de entrada

Antes de ejecutar, confirme que existen estos archivos:

```text
data/raw/pib_departamental.xlsx
data/raw/mercado_laboral_tolima.xlsx
```

No cambie sus nombres ni su estructura: el código espera las columnas y rutas utilizadas en el desarrollo. El procesamiento no sobrescribe los originales.

### Paso 8. Ejecutar el programa

```powershell
.\.venv\Scripts\python.exe main.py
```

Con el entorno activado, puede utilizar `python main.py`.

La ejecución realiza lectura, inspección, limpieza, transformación, integración por año, validación, auditoría y exportación.

### Paso 9. Comprobar la salida

La ejecución documentada finaliza con una confirmación equivalente a:

```text
EXPORTACIÓN COMPLETADA CORRECTAMENTE
Registros exportados: 19
Columnas exportadas: 22
Verificación de dimensiones: CORRECTA
```

Los resultados quedan en:

| Archivo | Uso recomendado |
|---|---|
| `data/processed/tolima_pib_mercado_laboral_2007_2025.xlsx` | Consulta en Excel, hoja `Datos_Integrados` |
| `data/processed/tolima_pib_mercado_laboral_2007_2025.csv` | Análisis en Python, R, Power BI y otras herramientas |

El CSV utiliza coma como separador y codificación `utf-8-sig`. Si Excel muestra todo en una sola columna, impórtelo indicando el delimitador coma o utilice directamente el `.xlsx`.

## 5. Ejecución orientativa en macOS o Linux

Los siguientes comandos son orientativos; la ejecución documentada se realizó en Windows.

```bash
git clone https://github.com/StefaniaRodriguez/Proyecto_Integrador_Tolima.git
cd Proyecto_Integrador_Tolima
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python main.py
```

## 6. Fuentes de información

Los archivos de entrada corresponden a información del **DANE**:

| Archivo | Contenido | Llave temporal original |
|---|---|---|
| `data/raw/pib_departamental.xlsx` | PIB del Tolima a precios constantes de 2015 | `año_id` |
| `data/raw/mercado_laboral_tolima.xlsx` | Población, participación, ocupación y desocupación | `id_año` |

Ambas fuentes abarcan 2007–2025, con 19 observaciones anuales por archivo. La integración se realiza mediante el año y conserva un registro por período.

**Referencia institucional:** [Departamento Administrativo Nacional de Estadística (DANE)](https://www.dane.gov.co/).

> **Pendiente de trazabilidad documental:** añadir las URL exactas de descarga, la fecha de consulta y la versión de cada archivo original, una vez verificadas. No se presentan enlaces de descarga específicos que no hayan sido comprobados.

## 7. Funcionamiento del pipeline ETL

| Etapa | Módulo | Función |
|---|---|---|
| 1. Extracción | `src/extraction.py` | Leer los Excel y explorar columnas, tipos, dimensiones y faltantes |
| 2. Limpieza | `src/cleaning.py` | Estandarizar nombres, años, decimales y escalas poblacionales |
| 3. Transformación por fuente | `src/transformation.py` | Calcular variaciones anuales del PIB y de las poblaciones ocupada y desocupada |
| 4. Integración | `src/integration.py` | Unir ambas fuentes por año y verificar la correspondencia temporal |
| 5. Transformación integrada | `src/transformation.py` | Construir indicadores que relacionan variables económicas y laborales |
| 6. Validación | `src/validation.py` | Revisar rangos, duplicados, identidades, faltantes, atípicos e integridad del PIB |
| 7. Auditoría | `src/audit.py` | Reportar completitud, estadísticas, decisiones y comparaciones antes/después |
| 8. Exportación | `main.py` | Guardar CSV y Excel y verificar las dimensiones de los archivos generados |

`main.py` coordina la ejecución de las etapas.

## 8. Seis transformaciones analíticas

Las tareas de limpieza no se cuentan como transformaciones analíticas principales.

| N.º | Variable derivada | Definición |
|---:|---|---|
| 1 | `crec_pib_real` | Variación porcentual interanual del PIB real |
| 2 | `var_ocupados` | Variación porcentual interanual de la población ocupada |
| 3 | `var_desocupados` | Variación porcentual interanual de la población desocupada |
| 4 | `pib_por_ocupado` | PIB real dividido entre población ocupada |
| 5 | `ocupados_por_mil_pet` | Población ocupada / población en edad de trabajar × 1.000 |
| 6 | `brecha_tgp_to` | Tasa global de participación menos tasa de ocupación, en puntos porcentuales |

Las tres variaciones interanuales presentan un valor faltante en 2007, porque no hay una observación anterior en el conjunto. No se reemplazan por cero. Las unidades de `pib_por_ocupado` dependen de las unidades originales de las fuentes.

## 9. Resultados y controles de calidad

Resultados de la ejecución documentada:

| Comprobación | Resultado |
|---|---|
| Período integrado | 2007–2025 |
| Registros finales | **19** |
| Columnas finales | **22** |
| Años duplicados | 0 |
| Años sin correspondencia entre fuentes | 0 |
| Valores faltantes finales | **19** |
| Inconsistencias en indicadores derivados | 0 |
| Inconsistencias en identidades laborales verificadas | 0 |
| Valores del PIB modificados | 0 |
| Suma del PIB real antes y después | 330.295, en unidades de la fuente |
| Valores atípicos detectados con IQR | 2: población desocupada y tasa de desempleo en 2020 |
| Archivos finales | CSV y Excel, con dimensiones verificadas |

### Tratamiento de valores faltantes

De los 19 faltantes finales, **16 provienen de las fuentes** y **3 corresponden a variaciones interanuales no calculables en 2007**.

| Variable | Faltantes | Explicación |
|---|---:|---|
| `ts` | 1 | Sin dato para 2020 |
| `poblacion_subocupada` | 1 | Sin dato para 2020 |
| `fuerza_trabajo_potencial` | 14 | Sin dato para 2007–2020 |
| `crec_pib_real` | 1 | No existe año anterior a 2007 |
| `var_ocupados` | 1 | No existe año anterior a 2007 |
| `var_desocupados` | 1 | No existe año anterior a 2007 |

Los faltantes se conservan y documentan; no se inventan observaciones. Los valores atípicos de 2020 se señalan para su análisis, sin eliminarlos automáticamente.

## 10. Ejemplo de interpretación económica: 2019–2021

| Año | PIB real | Población ocupada | Tasa de desempleo |
|---:|---:|---:|---:|
| 2019 | 18.512 | 536 | 16,6 % |
| 2020 | 17.149 | 459 | 23,2 % |
| 2021 | 18.733 | 473 | 16,3 % |

Entre 2019 y 2020, el PIB real disminuyó aproximadamente **7,36 %** y la población ocupada pasó de 536 a 459, en las unidades de la fuente. La tasa de desempleo aumentó de 16,6 % a 23,2 %. En 2021, el PIB real creció aproximadamente **9,24 %** respecto de 2020.

Estos cambios son descriptivos y simultáneos; no prueban una relación causal.

## 11. Solución de problemas frecuentes

| Problema | Solución recomendada |
|---|---|
| `py` o `python` no se reconoce | Verifique la instalación de Python y vuelva a abrir la terminal. |
| `git` no se reconoce | Instale Git o descargue el proyecto como ZIP. |
| `No module named pandas` / `openpyxl` | Ejecute `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`. |
| PowerShell no permite activar `.venv` | No lo active: utilice directamente `.\.venv\Scripts\python.exe main.py`. |
| `FileNotFoundError` al buscar los Excel | Compruebe los nombres y rutas de los archivos en `data/raw/`. |
| Faltan columnas o aparecen datos incompatibles | Revise que los Excel originales conserven la estructura esperada. |
| No se encuentra `main.py` | Abra la carpeta raíz y compruebe su contenido con `Get-ChildItem`. |
| El `.docx` no se abre como texto en VS Code | Ábralo en Microsoft Word u otra aplicación compatible. |
| El CSV aparece en una sola columna | Impórtelo con delimitador coma o abra el archivo `.xlsx`. |
| No aparecen resultados en `data/processed/` | Revise si el pipeline terminó con el mensaje de exportación correcta. |

## 12. Reproducibilidad y actualización

Para repetir el análisis con las mismas fuentes, conserve los archivos de `data/raw/` y ejecute nuevamente `main.py`. El programa regenera los archivos de `data/processed/`.

Si modifica las fuentes, el período, las columnas o las reglas de transformación, debe revisar las validaciones y actualizar este README y el informe académico. Los resultados de **19 filas y 22 columnas** corresponden a la ejecución documentada con los archivos actuales.

## 13. Publicación y buenas prácticas

El repositorio incluye código, dependencias, documentación y archivos para reproducir el análisis. Antes de compartirlo, compruebe:

- [x] Pipeline ejecutado correctamente en el entorno de desarrollo.
- [x] Base integrada de 19 registros y 22 columnas.
- [x] Exportaciones CSV y Excel verificadas en dimensiones.
- [x] Dependencias declaradas en `requirements.txt`.
- [x] `.gitignore` configurado para excluir el entorno virtual y archivos temporales.
- [x] Repositorio publicado en GitHub.
- [ ] Confirmar los permisos de redistribución de los archivos originales y del informe académico.
- [ ] Probar la instalación y ejecución desde una carpeta nueva utilizando únicamente este README.
- [ ] Añadir enlaces exactos, verificados, a las fuentes estadísticas.

No publique credenciales, datos personales ni archivos temporales. El archivo `.gitignore` ayuda a excluir ciertos elementos, pero no sustituye la revisión de los archivos antes de publicarlos.

## 14. Referencias

- Departamento Administrativo Nacional de Estadística (DANE). *Cuentas nacionales departamentales y estadísticas de mercado laboral*. https://www.dane.gov.co/
- Material académico de la asignatura *Fundamentos de Integración y Transformación de Datos*: lineamientos de integración de fuentes, transformaciones, validación y trazabilidad.

**Pendiente:** completar las referencias específicas de los archivos fuente con URL oficial, fecha de consulta y versión utilizada, una vez verificadas.
