Proyecto integrador: PIB y mercado laboral del Tolima (2007–2025)
Asignatura: Fundamentos de Integración y Transformación de Datos
Área de estudio: Economía y analítica de datos
Tecnologías: Python, pandas y openpyxl
Cobertura: Departamento del Tolima, Colombia; datos anuales de 2007 a 2025.
1. Descripción del proyecto
Este repositorio contiene un proceso ETL (extracción, transformación y carga/exportación) desarrollado en Python para integrar dos fuentes estadísticas del DANE: el producto interno bruto (PIB) departamental a precios constantes de 2015 y los indicadores del mercado laboral del Tolima.

Objetivo: construir una base anual integrada, consistente y reproducible que permita describir la evolución de la actividad económica, la ocupación y la desocupación del Tolima entre 2007 y 2025, preservando los datos originales y documentando las decisiones de calidad.

Pregunta orientadora: ¿Cómo evolucionaron el PIB real y los indicadores del mercado laboral del Tolima entre 2007 y 2025, y qué relaciones descriptivas pueden observarse entre ellos?
Importante: los resultados permiten realizar comparaciones y análisis descriptivos; por sí solos no demuestran relaciones causales entre PIB y empleo.

2. Qué encontrará en este repositorio
- Código fuente: módulos Python para extracción, limpieza, transformación, integración, validación y auditoría.
- Datos originales: dos archivos Excel en data/raw/.
- Datos finales: una base integrada en formatos .csv y .xlsx dentro de data/processed/.
- Informe académico: documento Word en docs/.
- Dependencias: archivo requirements.txt para instalar las bibliotecas requeridas.
Estructura de carpetas
Proyecto_Integrador_Tolima/
├── data/
│   ├── raw/
│   │   ├── pib_departamental.xlsx
│   │   └── mercado_laboral_tolima.xlsx
│   └── processed/
│       ├── tolima_pib_mercado_laboral_2007_2025.csv
│       └── tolima_pib_mercado_laboral_2007_2025.xlsx
├── docs/
│   └── [informe académico en formato .docx]
├── outputs/                     # carpeta reservada para salidas adicionales
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
Nota: .venv/, __pycache__/ y .vscode/ pueden existir en el computador de quien desarrolla el proyecto, pero están excluidos del repositorio mediante .gitignore. La carpeta outputs/ está reservada; el proceso actual guarda la base final en data/processed/.
3. Guía rápida: ejecutar el proyecto en Windows
Si ya tiene Python y Git instalados, puede seguir estos pasos desde PowerShell:
# 1. Descargar el repositorio (reemplace la URL por la dirección real de GitHub)
git clone URL_DEL_REPOSITORIO

# 2. Entrar a la carpeta del proyecto
cd Proyecto_Integrador_Tolima

# 3. Crear un entorno virtual
py -m venv .venv

# 4. Instalar las bibliotecas necesarias
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# 5. Ejecutar el proyecto
.\.venv\Scripts\python.exe main.py
Al terminar, revise data/processed/. Allí estarán los archivos Excel y CSV. No copie literalmente URL_DEL_REPOSITORIO: debe reemplazarla por la URL del repositorio publicado. Si descargó un ZIP, omita git clone y abra la carpeta descomprimida.
4. Instalación detallada desde cero (Windows)
Paso 1. Instalar Python
1. Entre en el sitio oficial: https://www.python.org/downloads/.
2. Descargue e instale una versión de Python compatible con las dependencias del proyecto. El entorno de desarrollo usado en la ejecución documentada fue Python 3.15.2; no se han verificado aquí otras versiones.
3. Si el instalador ofrece la opción Add Python to PATH, actívela.
4. Abra PowerShell (puede buscarlo en el menú Inicio) y compruebe la instalación:
   py --version
   Si el comando py no está disponible, pruebe python --version. Si ninguno funciona, cierre y vuelva a abrir la terminal y compruebe la instalación de Python.
Paso 2. Instalar Visual Studio Code (recomendado)
1. Descargue Visual Studio Code desde https://code.visualstudio.com/.
2. Instálelo y ábralo.
3. En Extensions (Extensiones), busque e instale la extensión Python publicada por Microsoft.
4. VS Code facilita editar y ejecutar el proyecto, pero no es obligatorio: también puede utilizar PowerShell.
Paso 3. Instalar Git (para clonar el repositorio)
1. Descargue Git desde https://git-scm.com/downloads.
2. Instálelo y abra una nueva ventana de PowerShell.
3. Verifique la instalación:
   git --version
   Si no desea instalar Git, puede descargar el repositorio como ZIP desde GitHub: Code → Download ZIP y descomprimirlo. En ese caso, continúe desde el paso 4.
Paso 4. Descargar el proyecto
Opción A: con Git
1. En GitHub, abra la página del repositorio.
2. Pulse Code y copie la dirección HTTPS.
3. En PowerShell, vaya a la carpeta donde desea guardarlo. Por ejemplo:
   cd "$HOME\Documents"
4. Clone el repositorio (reemplace la URL de ejemplo por la real):
   git clone URL_DEL_REPOSITORIO
   cd Proyecto_Integrador_Tolima
Opción B: sin Git
1. En GitHub, pulse Code → Download ZIP.
2. Descomprima el ZIP en una carpeta de su computador.
3. Abra la carpeta descomprimida que contiene main.py, requirements.txt y src/.
Paso 5. Abrir correctamente la carpeta en VS Code
1. En VS Code, seleccione File → Open Folder (Archivo → Abrir carpeta).
2. Elija la carpeta raíz Proyecto_Integrador_Tolima, no la carpeta src/ ni data/.
3. Compruebe que a la izquierda aparezcan main.py, requirements.txt, src/, data/ y docs/.
4. Abra Terminal → New Terminal (Terminal → Nuevo terminal).
5. La terminal debe estar ubicada en la carpeta raíz del proyecto. Para comprobarlo, ejecute:
   Get-Location
   Get-ChildItem
   Get-ChildItem debe mostrar main.py y requirements.txt. Si no aparecen, cambie a la carpeta correcta antes de continuar.
Paso 6. Crear el entorno virtual
Desde la carpeta que contiene main.py, ejecute:
py -m venv .venv
Este comando crea una carpeta local .venv/ para mantener las bibliotecas del proyecto separadas de otras instalaciones de Python. No es necesario subir .venv/ a GitHub: cada persona crea la suya.

Forma recomendada, sin activar el entorno virtual: puede ejecutar directamente el Python ubicado dentro de .venv/, evitando problemas con las políticas de ejecución de PowerShell:
.\.venv\Scripts\python.exe --version
Forma alternativa, activando el entorno:
.\.venv\Scripts\Activate.ps1
Si funciona, la terminal mostrará (.venv). En ese caso, los comandos posteriores se pueden ejecutar con python en lugar de \.venv\Scripts\python.exe. Si PowerShell bloquea la activación, no necesita cambiar la seguridad del equipo: utilice la forma recomendada sin activar.

En VS Code, si se solicita seleccionar intérprete: presione Ctrl + Shift + P, busque Python: Select Interpreter y elija el Python ubicado en .venv\Scripts\python.exe.
Paso 7. Instalar las dependencias
El proyecto utiliza las versiones indicadas en requirements.txt:
pandas==3.1.1
openpyxl==3.1.5
Instálelas con:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Para comprobar que quedaron instaladas:
.\.venv\Scripts\python.exe -m pip show pandas openpyxl
Si activó el entorno virtual, los comandos equivalentes son:
python -m pip install -r requirements.txt
python -m pip show pandas openpyxl
Nota: la instalación requiere acceso a Internet para descargar las dependencias, salvo que ya estén disponibles localmente. Si una versión exacta no está disponible para su versión de Python, revise el mensaje de pip; no cambie versiones sin volver a probar el proyecto.
Paso 8. Verificar los archivos de entrada
Antes de ejecutar, compruebe que existen estos dos archivos con exactamente estos nombres:
data/raw/pib_departamental.xlsx
data/raw/mercado_laboral_tolima.xlsx
No los cambie de nombre ni de carpeta: main.py los busca en esas rutas. Los libros deben conservar la estructura de columnas esperada por el código. La ejecución no sobrescribe los originales.
Paso 9. Ejecutar el programa
Con el entorno virtual sin activar:
.\.venv\Scripts\python.exe main.py
Si el entorno ya está activado y ve (.venv) en la terminal:
python main.py
Qué ocurre al ejecutar: el programa lee los dos Excel, inspecciona su estructura, limpia variables, calcula indicadores, integra los datos por año, ejecuta validaciones, presenta reportes de auditoría y exporta la tabla final en CSV y Excel.

La terminal muestra distintos reportes; es normal que la salida sea extensa. La confirmación importante está al final:
EXPORTACIÓN COMPLETADA CORRECTAMENTE
Registros exportados: 19
Columnas exportadas: 22
Archivo CSV: ...\data\processed\tolima_pib_mercado_laboral_2007_2025.csv
Archivo Excel: ...\data\processed\tolima_pib_mercado_laboral_2007_2025.xlsx
Verificación de dimensiones: CORRECTA
Las rutas concretas dependen de la ubicación donde haya guardado el proyecto. Si aparece un error en lugar de este mensaje, consulte la sección de solución de problemas.
Paso 10. Abrir y comprobar los resultados
Entre a la carpeta data/processed/ y abra:
Archivo	Uso recomendado
tolima_pib_mercado_laboral_2007_2025.xlsx	Consultar la base final en Excel; hoja Datos_Integrados.
tolima_pib_mercado_laboral_2007_2025.csv	Utilizar la base en Python, R, Power BI u otras herramientas de análisis.


En la ejecución documentada, ambos archivos contienen 19 registros y 22 columnas. El código comprueba que los archivos exportados conservan las dimensiones de la tabla en memoria. Los archivos se actualizan cada vez que se ejecuta correctamente main.py.

El CSV utiliza coma como separador y codificación UTF-8 con BOM (utf-8-sig). Si Excel abre el CSV en una sola columna, utilice su opción de importación de texto/CSV e indique el delimitador coma. Para consultar directamente los resultados en Excel, es más sencillo abrir el archivo .xlsx.
5. Ejecución en macOS o Linux (orientación)
Estos comandos son una guía de instalación equivalente, pero la ejecución documentada del proyecto se realizó en Windows:
# Clonar (sustituir por la URL real)
git clone URL_DEL_REPOSITORIO
cd Proyecto_Integrador_Tolima

# Crear el entorno virtual
python3 -m venv .venv

# Instalar dependencias
./.venv/bin/python -m pip install -r requirements.txt

# Ejecutar
./.venv/bin/python main.py
La disponibilidad de versiones de Python y bibliotecas depende del sistema. En macOS/Linux puede utilizar VS Code de la misma forma, seleccionando el intérprete .venv/bin/python.
6. Fuentes de información y alcance
Las fuentes de origen corresponden al Departamento Administrativo Nacional de Estadística (DANE), organizadas en los siguientes archivos de entrada:
Archivo	Información	Llave temporal
data/raw/pib_departamental.xlsx	PIB del Tolima a precios constantes de 2015	año_id
data/raw/mercado_laboral_tolima.xlsx	Indicadores de población, participación, ocupación y desocupación	id_año


Ambas fuentes abarcan 2007–2025 y contienen 19 registros anuales cada una. La integración se realiza mediante el año y conserva un registro por período. Los archivos originales no se sobrescriben.

Referencias institucionales generales:
- DANE: https://www.dane.gov.co/
- Estadísticas de cuentas nacionales departamentales y mercado laboral del DANE.
Trazabilidad de las fuentes: antes de la publicación académica definitiva, se deben añadir las direcciones exactas de descarga y, cuando corresponda, la fecha de consulta y versión de cada conjunto original. No se incluyen enlaces directos no verificados.
7. Funcionamiento del pipeline ETL
La ejecución está centralizada en main.py y sigue este orden:
1. Extracción (src/extraction.py): carga los dos archivos Excel, revisa columnas, tipos, dimensiones y valores faltantes.
2. Limpieza (src/cleaning.py): estandariza nombres de columnas y años, convierte tasas expresadas con coma decimal y normaliza escalas poblacionales.
3. Transformación por fuente (src/transformation.py): calcula el crecimiento anual del PIB real y las variaciones anuales de ocupados y desocupados.
4. Integración (src/integration.py): combina las dos fuentes por año y comprueba la correspondencia de los períodos.
5. Transformación integrada (src/transformation.py): calcula indicadores que relacionan variables económicas y laborales.
6. Validación (src/validation.py): revisa cobertura temporal, rangos, duplicados, identidades laborales, valores positivos, indicadores derivados, atípicos e integridad del PIB.
7. Auditoría (src/audit.py): genera diagnósticos de completitud, estadísticas descriptivas, matrices de calidad, decisiones sobre faltantes y comparaciones antes/después.
8. Exportación (main.py): escribe la base final a CSV y Excel y vuelve a leer ambos archivos para verificar sus dimensiones.
Responsabilidades de los archivos
Archivo	Responsabilidad principal
main.py	Coordinar todas las etapas y exportar resultados.
src/extraction.py	Lectura y exploración de las fuentes.
src/cleaning.py	Limpieza y normalización de formatos y escalas.
src/transformation.py	Cálculo de indicadores analíticos.
src/integration.py	Unión de las fuentes mediante el año.
src/validation.py	Controles de integridad y consistencia.
src/audit.py	Diagnósticos, reportes y trazabilidad de decisiones.


8. Las seis transformaciones analíticas
Las operaciones de limpieza no se contabilizan como las seis transformaciones analíticas principales.
N.º	Indicador	Definición
1	crec_pib_real	Variación porcentual interanual del PIB real.
2	var_ocupados	Variación porcentual interanual de la población ocupada.
3	var_desocupados	Variación porcentual interanual de la población desocupada.
4	pib_por_ocupado	PIB real dividido entre población ocupada.
5	ocupados_por_mil_pet	Población ocupada / población en edad de trabajar × 1.000.
6	brecha_tgp_to	Tasa global de participación menos tasa de ocupación, en puntos porcentuales.


Los tres indicadores de variación anual presentan un valor faltante en 2007 porque no existe un año anterior dentro del conjunto de datos. No se reemplazan por cero ni se imputan arbitrariamente. Las unidades de pib_por_ocupado dependen de las unidades originales de PIB y ocupación.
9. Resultados y controles de calidad
En la ejecución documentada del pipeline se obtuvieron los siguientes resultados:
Comprobación	Resultado
Período integrado	2007–2025
Registros finales	19
Columnas finales	22
Años duplicados	0
Años sin correspondencia entre fuentes	0
Valores faltantes finales	19
Inconsistencias en indicadores derivados	0
Inconsistencias en identidades laborales verificadas	0
Valores del PIB modificados	0
Suma del PIB real antes y después	330.295 (en las unidades de la fuente)
Valores atípicos detectados mediante IQR	2: población desocupada y tasa de desempleo en 2020
Archivos finales	CSV y Excel, ambos verificados en dimensiones


Tratamiento de valores faltantes
De los 19 valores faltantes finales, 16 provienen de las fuentes y 3 corresponden a variaciones interanuales no calculables en 2007:
Variable	Faltantes	Explicación
ts	1	Sin dato para 2020.
poblacion_subocupada	1	Sin dato para 2020.
fuerza_trabajo_potencial	14	Sin dato para 2007–2020.
crec_pib_real	1	No existe dato del año anterior a 2007.
var_ocupados	1	No existe dato del año anterior a 2007.
var_desocupados	1	No existe dato del año anterior a 2007.


Los faltantes se conservan y documentan; no se inventan observaciones. Los valores atípicos de 2020 se identifican para su análisis, pero no se eliminan automáticamente.
10. Ejemplo de interpretación económica (2019–2021)
Año	PIB real	Población ocupada	Tasa de desempleo
2019	18.512	536	16,6 %
2020	17.149	459	23,2 %
2021	18.733	473	16,3 %


Entre 2019 y 2020, el PIB real disminuyó aproximadamente 7,36 % y la población ocupada pasó de 536 a 459 (en las unidades de la fuente). Paralelamente, la tasa de desempleo aumentó de 16,6 % a 23,2 %. En 2021, el PIB real creció aproximadamente 9,24 % respecto de 2020. Estas observaciones describen cambios simultáneos; no permiten atribuir causalidad sin análisis adicional.
11. Solución de problemas frecuentes
python o py no se reconoce
Python puede no estar instalado o no estar disponible en la terminal. Instálelo desde el sitio oficial, cierre y vuelva a abrir PowerShell y compruebe py --version o python --version.
git no se reconoce
Instale Git y reinicie la terminal. Alternativamente, descargue el proyecto mediante Code → Download ZIP desde GitHub.
No module named pandas o No module named openpyxl
Instale las dependencias con el mismo intérprete que utilizará para ejecutar el proyecto:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
PowerShell no permite activar .venv
No es obligatorio activar el entorno. Ejecute directamente:
.\.venv\Scripts\python.exe main.py
FileNotFoundError al buscar los Excel
Compruebe que está ejecutando el proyecto desde su carpeta raíz y que los archivos están en data/raw/ con los nombres exactos pib_departamental.xlsx y mercado_laboral_tolima.xlsx.
Error de columnas faltantes o datos incompatibles
Verifique que los archivos Excel originales no hayan sido reemplazados por versiones con otra estructura. El programa espera columnas específicas para PIB y mercado laboral. Consulte los mensajes de extracción y validación para identificar el problema.
main.py no se encuentra
La terminal puede estar abierta en otra carpeta. En VS Code, utilice File → Open Folder y seleccione Proyecto_Integrador_Tolima; luego abra una terminal nueva. Compruebe con Get-ChildItem que main.py está visible.
El archivo .docx no se abre como texto en VS Code
Es normal: un documento Word es un archivo binario para el editor de texto. Ábralo con Microsoft Word u otra aplicación compatible. No afecta la ejecución del programa.
El CSV se abre en una sola columna en Excel
Importe el CSV indicando coma como separador, o abra directamente el archivo .xlsx que se genera junto con él.
No aparecen los archivos en data/processed/
Revise si el programa terminó y mostró EXPORTACIÓN COMPLETADA CORRECTAMENTE. Si se interrumpió antes, lea el error en la terminal. La carpeta de salida se crea automáticamente cuando el proceso llega a la etapa de exportación.
12. Cómo reproducir o actualizar los resultados
Para repetir el análisis con los mismos archivos, conserve los Excel de data/raw/ y vuelva a ejecutar main.py. El programa regenerará los resultados de data/processed/.

Si modifica los datos de entrada, el período de cobertura, las columnas o las reglas de transformación, debe revisar las validaciones y actualizar este README y el informe académico. Los resultados de 19 filas y 22 columnas corresponden a la ejecución documentada con las fuentes actuales.
13. Publicación y uso desde GitHub
El repositorio debe contener main.py, src/, requirements.txt, .gitignore, README.md, los archivos originales necesarios para reproducir el análisis (si su redistribución está permitida), el informe académico y las salidas finales previstas para la entrega.

No se deben publicar .venv/, __pycache__/, archivos temporales de Office ni datos personales o credenciales. Estas exclusiones están contempladas en .gitignore, pero conviene revisar los archivos antes de subirlos.
Comprobación recomendada antes de compartir el enlace
- [x] Pipeline ejecutado con éxito en el entorno de desarrollo.
- [x] Datos integrados: 19 filas y 22 columnas.
- [x] Exportación a Excel y CSV verificada en dimensiones.
- [x] Dependencias declaradas en requirements.txt.
- [x] .gitignore configurado para excluir archivos temporales y entorno virtual.
- [ ] Confirmar permiso de redistribución de los archivos originales y del informe.
- [ ] Publicar el repositorio y reemplazar URL_DEL_REPOSITORIO por su enlace real en este README.
- [ ] Clonar o descargar el repositorio en una carpeta nueva y repetir la ejecución siguiendo únicamente estas instrucciones.
- [ ] Añadir enlaces de descarga exactos y verificados de las fuentes estadísticas.
14. Referencias
- Departamento Administrativo Nacional de Estadística (DANE). Información de cuentas nacionales departamentales y estadísticas de mercado laboral. https://www.dane.gov.co/.
- Material académico de la asignatura Fundamentos de Integración y Transformación de Datos. Lineamientos de integración de fuentes, transformaciones, validación y trazabilidad de datos.
Pendiente documental: completar las referencias específicas de los archivos fuente con sus enlaces oficiales de descarga, fecha de consulta y versión utilizada, una vez verificadas.