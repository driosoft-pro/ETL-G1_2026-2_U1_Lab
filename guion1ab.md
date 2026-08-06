# Guion de Presentacion - Proyecto 1b: ETL Pipeline Retail Analytics

## Integrantes
1. Deyton Riascos Ortiz — Project Manager
2. Daniel David Garcia Restrepo — Product Owner
3. Samuel Izquierdo Bonilla — Development Team
4. Mauricio Taborda Gondora — Quality & Analytics

---

## ESTRUCTURA DE LA PRESENTACION

---

### PARTE 1: Introduccion (2 min)
**Integrante 1**

> Buenas tardes. Nuestro proyecto es un pipeline ETL completo para analisis de datos de retail. El objetivo es extraer, transformar y cargar datos de ventas de tres ciudades colombianas: Cali, Bogota y Medellin, para generar reportes analiticos que apoyen la toma de decisiones de negocio.

> El problema que resolvemos es consolidar datos de multiples fuentes con formatos diferentes (CSV, JSON, XML) en una unica base de datos analitica, aplicando reglas de calidad y generando metricas clave.

---

### PARTE 1.1: Contexto del Negocio (2 min)
**Integrante 2**

> **El Problema de Negocio:**
> La empresa tiene datos de ventas, inventario y productos, pero estan dispersos en hojas de calculo y sistemas diferentes. Los gerentes no pueden obtener una vista rapida y confiable del rendimiento de las tiendas para tomar decisiones oportunas.

> **Por que importa:**
> - Reduce el tiempo buscando informacion
> - Identifica rapidamente productos de bajo rendimiento
> - Permite decisiones basadas en datos
> - Facilita el seguimiento del cumplimiento de metas

> **Objetivos del Proyecto (Lab 1A):**
> 1. Centralizar informacion de ventas en una vista analitica unica
> 2. Monitorear rendimiento por region y tienda
> 3. Analizar rendimiento de categorias y productos
> 4. Evaluar cumplimiento de metas comerciales
> 5. Analizar tendencias de ventas en el tiempo
> 6. Analizar impacto de promociones en ventas

> **Preguntas Analiticas Clave:**
> - Cuales son las ventas totales por dia, semana, mes y anio?
> - Que categorias generan mayor y menor ingreso?
> - Que tiendas tienen mejor y peor rendimiento?
> - Como varian las ventas entre regiones?
> - Que tiendas cumplen o no sus metas comerciales?
> - Que impacto tienen las promociones en las ventas?

> **KPIs del Dashboard:**
> - Ingresos totales
> - Ventas por tienda/region
> - Ventas por categoria/top 10
> - Crecimiento de ventas (%)
> - Cumplimiento de metas (%)
> - Aumento de ventas por promocion

> **Requisitos Funcionales:**
> - Mostrar ventas totales por dia, semana, mes y anio
> - Mostrar rendimiento por categoria y producto
> - Visualizar ventas por region y tienda
> - Filtrar por region, tienda y periodo
> - Mostrar tendencias historicas
> - Mostrar cumplimiento de metas por tienda
> - Integrar informacion de promociones con ventas
> - Permitir descarga de reportes

> **Requisitos No Funcionales:**
> - Actualizacion diaria de informacion
> - Acceso solo para usuarios autorizados
> - Tiempo de carga menor a 5 segundos
> - Disponibilidad durante horas laborales
> - Compatible con dispositivos moviles
> - Escalable a mas tiendas y volumen de datos

> **Fuentes de Datos (Lab 1A):**
> - Sistema POS (ventas)
> - Catalogo de Productos
> - Catalogo de Tiendas
> - Sistema de Metas Comerciales
> - Sistema de Promociones

> **Historias de Usuario:**
> - Gerente Regional: "Quiero visualizar ventas de todas las tiendas de mi region para identificar rapidamente las mejores y peores."
> - Gerente de Tienda: "Quiero ver ventas por categoria para detectar que productos necesitan promocion."
> - Equipo de Marketing: "Quiero ver el impacto de las promociones en las ventas para identificar que campanas dan mejores resultados."
> - Director Comercial: "Quiero ver que tiendas cumplen sus metas para ajustar campanas publicitarias."

---

### PARTE 1.2: De Requisitos a ETL - Conexion Lab 1A y 1B (1 min)
**Integrante 3**

> **El Desafio Detras de los KPIs:**
> Muchos KPIs requieren mas de una fuente de datos. Por ejemplo:
> - **Cumplimiento de Metas:** Requiere Sistema POS + Sistema de Metas Comerciales
> - **Impacto de Promociones:** Requiere Sistema POS + Sistema de Promociones
>
> El KPI mas dificil es "Aumento de Ventas por Promocion" porque:
> - Integra ventas y promociones de diferentes sistemas
> - Cada promocion debe relacionarse con producto, tienda y fecha
> - Requiere comparar ventas antes, durante y despues de cada campana
> - Riesgo de atribucion: no confundir el efecto con estacionalidad

> **Como el ETL resuelve esto (Lab 1B):**
>
> **EXTRACT:** Recuperamos datos del Sistema POS, Catalogo de Productos, Catalogo de Tiendas, Sistema de Promociones y Sistema de Metas Comerciales.
>
> **TRANSFORM:** Limpiamos, integramos, validamos, calculamos KPIs y generamos agregaciones.
>
> **LOAD:** Almacenamos el dataset consolidado que alimentara el dashboard.

> **Trazabilidad de Requisito a Salida:**
>
> | Requisito | Fuente | Transformacion | Salida Esperada |
> |-----------|--------|----------------|-----------------|
> | Medir cumplimiento de metas | POS + Metas | Integrar ventas reales con metas y calcular % | KPI de cumplimiento por tienda y region |
> | Analizar impacto promociones | POS + Promociones | Relacionar promociones con producto, tienda, fecha | Indicadores de impacto de promociones |
> | Generar reportes | Dataset ETL consolidado | Integrar todos los datos procesados | Dataset final para dashboard y reportes |

> **Reflexion Final:**
> Construir el dashboard no es el primer paso. Antes de disenar tablas, graficas o wireframes, el equipo tuvo que entender el problema de negocio, identificar stakeholders y traducir sus necesidades en objetivos y preguntas analiticas. El dashboard es el resultado visible - el verdadero primer paso es entender el negocio y los datos necesarios.

---

### PARTE 2: Arquitectura del Sistema y Porque de cada Script (3 min)
**Integrante 2**

> Nuestro sistema esta compuesto por 7 modulos principales. Cada uno tiene un proposito especifico:

#### 2.1 extract.py - Extraccion de Datos
> **Por que existe:** Los datos vienen de 3 fuentes diferentes con formatos distintos. Este modulo unifica todo a un esquema comun.

> - Lee CSV (Cali): formato estandar, columnas en ingles
> - Lee JSON (Bogota): columnas en espanol (id_linea, fecha, sucursal, etc.), las traduce automaticamente
> - Lee XML (Medellin): estructura anidada, extrae valores con findtext()
> - Concatena todo en un unico DataFrame con 8 columnas: sale_line_id, sale_date, store_id, product_id, quantity, unit_price, promotion_code, payment_method

#### 2.2 profiling.py - Perfilamiento de Datos
> **Por que existe:** Antes de limpiar, necesitamos saber QUE hay malo en los datos. Este modulo genera un diagnostico completo.

> Calcula:
> - Cantidad de filas y columnas
> - Valores nulos por columna
> - Duplicados por sale_line_id
> - Cantidades y precios invalidos (<=0)
> - Fechas que no se pueden parsear
> - Valores distintos para campos categoricos
> - Genera un reporte en profile_report.txt

#### 2.3 clean.py - Limpieza de Datos
> **Por que existe:** Los datos sucios generan reportes incorrectos. Este modulo aplica reglas de calidad basadas en el diagnostico del profiling.

> Reglas aplicadas:
> - **Parser de fechas multicapa:** Intenta 3 formatos (YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY) y fallback a dayfirst=True. Por que? Porque cada ciudad reporta fechas en formato diferente.
> - **Case normalization:** Convierte store_id, product_id, payment_method a mayusculas. Por que? Porque "s02" y "S02" deberian ser lo mismo en la base de datos.
> - **Strip de strings:** Elimina espacios extra que puedan causar errores de match.
> - **Eliminacion de duplicados:** Solo mantiene la primera ocurrencia de cada sale_line_id.
> - **Validacion de nulos:** Elimina filas sin ID, fecha, tienda o producto.
> - **Validacion numerica:** Elimina cantidades y precios <= 0.

#### 2.4 transform.py - Transformacion e Integracion
> **Por que existe:** Los datos limpios necesitan ser enriquecidos con informacion de las tablas de referencia y metricas calculadas.

> Pasos:
> - **integrate_products:** Join con productos para obtener nombre y categoria
> - **integrate_stores:** Join con tiendas para obtener nombre, ciudad, region
> - **integrate_promotions:** Join con promociones para obtener porcentaje descuento y campana
> - **calculate_metrics:** Calcula:
>   - gross_sales = quantity x unit_price
>   - discount_amount = gross_sales x discount_pct
>   - net_sales = gross_sales - discount_amount
>   - month, week, day_name para analisis temporal
> - **integrate_targets:** Join con metas mensuales para comparar

#### 2.5 validate.py - Validacion de Datos
> **Por que existe:** Verifica que los datos transformados cumplan reglas de integridad antes de cargar.

> Validaciones:
> - Unicidad de sale_line_id (no duplicados)
> - Integridad de foreign keys (product_id y store_id existen en tablas referencia)
> - Valores positivos en quantity, unit_price, gross_sales, net_sales
> - Formula correcta: net_sales = gross_sales - discount_amount

#### 2.6 load.py - Carga de Datos
> **Por que existe:** Exporta los datos procesados a los destinos finales para su uso.

> Destinos:
> - CSV: data/processed/sales_analytics.csv
> - SQLite: 5 tablas (sales_analytics, products, stores, promotions, monthly_targets)
> - Funcion create_vanilla_database(): crea BD sin limpieza para comparar

#### 2.7 queries.py - Consultas Analiticas
> **Por que existe:** Ejecuta las 6 consultas SQL que responden preguntas de negocio.

> 6 consultas:
> 1. Top productos por ventas netas
> 2. Rendimiento mensual vs metas
> 3. Analisis regional (por region, ciudad, tienda)
> 4. Ventas totales por region
> 5. Ventas totales por categoria
> 6. Cumplimiento de objetivos

---

### PARTE 3: Proceso ETL Detallado (3 min)
**Integrante 3**

#### 3.1 Extract
> Extraemos 763 registros de ventas de 3 fuentes:
> - CSV (Cali): 241 filas - formato YYYY-MM-DD
> - JSON (Bogota): 281 filas - formato DD/MM/YYYY, columnas en espanol
> - XML (Medellin): 241 filas - formato MM-DD-YYYY, estructura anidada
>
> Ademas de 4 tablas de referencia: 15 productos, 3 tiendas, 6 promociones, 9 metas mensuales.

#### 3.2 Profile
> Diagnostico de calidad de datos:
> - Total rows: 763
> - Duplicados: 3
> - Cantidades invalidas: 2
> - Precios invalidos: 1
> - Precios nulos: 2
> - Total a limpiar: 8 registros

#### 3.3 Clean
> Reglas aplicadas:
> - Parser de fechas: 3 formatos + fallback
> - Case normalization: store_id, product_id, payment_method a MAYUSCULAS
> - Strip de strings en columnas clave
> - Eliminacion de 3 duplicados
> - Eliminacion de 5 registros con valores invalidos/nulos
>
> Resultado: 755 registros validos de 763 originales (98.95% retencion)

#### 3.4 Transform
> Join de 4 tablas de referencia + calculo de metricas:
> - 12 columnas nuevas agregadas
> - gross_sales, discount_amount, net_sales calculados
> - month, week, day_name para analisis temporal
> - Total: 755 filas con 22 columnas

#### 3.5 Validate
> 4 validaciones ejecutadas:
> - Unicidad de IDs: PASSED
> - Foreign keys: PASSED
> - Valores positivos: PASSED
> - Formulas: PASSED

#### 3.6 Load
> Carga en 2 destinos:
> - CSV: data/processed/sales_analytics.csv
> - SQLite: 5 tablas pobladas
>   - sales_analytics: 239 registros (consulta consolidada)
>   - products: 15 registros
>   - stores: 3 registros
>   - promotions: 6 registros
>   - monthly_targets: 9 registros

---

### PARTE 4: Base de Datos SQLite (2 min)
**Integrante 4**

> Nuestra base de datos tiene 5 tablas:

> **products** (15 registros):
> - product_id (PK), product_name, category, list_price, unit_cost
> - Catalogo de productos disponibles

> **stores** (3 registros):
> - store_id (PK), store_name, city, region
> - Las 3 tiendas: Cali, Bogota, Medellin

> **promotions** (6 registros):
> - promotion_code (PK), product_id (FK), start_date, end_date, discount_pct, campaign_name
> - Promociones activas con porcentaje de descuento

> **monthly_targets** (9 registros):
> - store_id (FK), month, sales_target
> - Meta de ventas por tienda y mes

> **sales_analytics** (239 registros):
> - Tabla principal con toda la informacion integrada
> - Incluye metricas calculadas y columnas derivadas

---

### PARTE 5: Notebook Interactivo - main.ipynb (3 min)
**Integrante 1**

> Nuestro notebook main.ipynb es un Colab-compatible que ejecuta todo el pipeline en tiempo real. Veamos cada paso:

#### 5.1 Celda Setup
> Detecta si estamos en Colab o local. Si es Colab, monta Google Drive y configura los paths. Importa pandas y configura opciones de visualizacion.

#### 5.2 Celda Import Modules
> Importa todas las funciones de los 7 modulos: extract, profiling, clean, transform, validate, load, queries.

#### 5.3 STEP 1 - Initialize Database
> Crea la base de datos SQLite con DROP TABLE IF EXISTS para evitar problemas de esquema. Ejecuta init_database() que crea las 5 tablas con sus foreign keys e indices.

#### 5.4 STEP 2 - Extract Data
> Ejecuta extract_all() que lee los 3 archivos de transacciones y 4 de referencia. Muestra:
> - Conteo por fuente (CSV, JSON, XML)
> - Muestra de las primeras 5 filas
> - Contenido de las 4 tablas de referencia

#### 5.5 STEP 3 - Profile Data
> Ejecuta profile_dataframe() para cada dataset. Genera el reporte profile_report.txt con metricas completas. Muestra tabla resumen y metricas detalladas de transacciones.

#### 5.6 STEP 4 - Clean Data
> Ejecuta clean_transactions() y clean_references(). Muestra:
> - Antes vs despues (763 → 755)
> - Registros eliminados y原因
> - Verificacion de normalizacion (IDs en mayusculas)
> - Rango de fechas

#### 5.7 STEP 5 - Transform Data
> Ejecuta transform_all() que integra las 4 tablas de referencia y calcula metricas. Muestra columnas derivadas: gross_sales, discount_amount, net_sales, month, week, day_name.

#### 5.8 STEP 6 - Validate Data
> Ejecuta validate_all() con las 4 validaciones. Muestra si paso o fallo con detalles.

#### 5.9 STEP 7 - Load Data
> Exporta a CSV y carga en SQLite. Verifica las 5 tablas y muestra conteo de registros en cada una.

#### 5.10 STEP 8 - Analytical Queries
> Ejecuta las 6 consultas analiticas y muestra los resultados en tablas. Guarda los resultados en data/output/ como CSV.

---

### PARTE 6: Graficas de Analisis de Negocio (2 min)
**Integrante 2**

> Presentamos 4 graficas clave que responden preguntas de negocio:

#### Grafica 1: Top 10 Productos + Distribucion por Categoria
> **Que muestra:**
> - Izquierda: Barras horizontales con los 10 productos que mas generan ingresos netos
> - Derecha: Pie chart con la participacion de cada categoria en las ventas totales
>
> **Por que es importante:**
> - Identifica los productos estrella que debemos mantener en stock
> - Muestra que categorias son las mas rentables para enfocar esfuerzos de marketing
>
> **Lectura:**
> - Si un producto tiene alto ranking pero baja categoria, puede ser oportunidad de upselling
> - Si una categoria domina, considerar diversificar el portafolio

#### Grafica 2: Cumplimiento de Metas + Heatmap de Ingresos
> **Que muestra:**
> - Izquierda: Barras horizontales con el % de cumplimiento de metas por tienda y mes (verde=cumplio, rojo=no cumplio)
> - Derecha: Mapa de calor mostrando ingresos por categoria y tienda (colores mas oscuros = mas ingresos)
>
> **Por que es importante:**
> - Identifica que tiendas estan rindiendo y cuales necesitan apoyo
> - Muestra que combinaciones de categoria-tienda son mas rentables
>
> **Lectura:**
> - Las tiendas en rojo necesitan estrategias especificas
> - Las celdas oscuras del heatmap son las oportunidades de negocio

#### Grafica 3: Tendencia Mensual
> **Que muestra:**
> - Izquierda: Linea de tendencia de ingresos totales por mes con area sombreada
> - Derecha: Barras de unidades vendidas por mes
>
> **Por que es importante:**
> - Identifica patrones estacionales (meses altos vs bajos)
> - Detecta tendencias de crecimiento o declive
>
> **Lectura:**
> - Subidas repentinas pueden indicar exito de promociones
> - Caidas pueden requerir investigacion de mercado

#### Grafica 4: (Integrada en Grafica 2)
> El heatmap complementa el analisis mostrando la relacion entre tiendas y categorias.

---

### PARTE 7: Pruebas y Calidad (1 min)
**Integrante 3**

> Contamos con 50 pruebas automatizadas usando pytest:

> - **test_extract.py (9 pruebas):** Verifica lectura correcta de CSV, JSON, XML, esquema unificado, conteo de filas
> - **test_profiling.py (13 pruebas):** Verifica metricas de perfilamiento, reporte generado, manejo de nulos
> - **test_clean.py (10 pruebas):** Verifica limpieza, duplicados, fechas, case normalization, valores invalidos
> - **test_transform.py (8 pruebas):** Verifica joins, metricas calculadas, columnas derivadas
> - **test_validate.py (7 pruebas):** Verifica unicidad, FK, valores positivos, formulas
> - **test_load.py (5 pruebas):** Verifica exportacion CSV, carga SQLite, tablas creadas

> Todas pasan al 100%, garantizando la integridad del pipeline.

---

### PARTE 8: Conclusiones y Tecnologias (1 min)
**Integrante 4**

> **Conclusiones:**
> - Pipeline ETL completo y funcional
> - 763 registros de 3 ciudades consolidados exitosamente
> - 755 registros validos (98.95% retencion)
> - Calidad de datos verificada con 50 pruebas
> - Metricas de negocio calculadas automaticamente
> - 4 visualizaciones para toma de decisiones
> - Base de datos SQLite con 5 tablas pobladas

> **Tecnologias:**
> - Python 3.12
> - Pandas (manipulacion de datos)
> - SQLite (base de datos)
> - Matplotlib + Seaborn (visualizaciones)
> - Pytest (pruebas automatizadas)
> - Google Colab (notebook interactivo)

---

### PARTE 9: Demostracion en Vivo (3 min)
**Integrante 4**

> Ahora mostraremos el notebook interactivo ejecutandose en tiempo real...

> [Abrir main.ipynb en Colab o Jupyter]
>
> 1. Ejecutar celda de Setup
> 2. Ejecutar celda de Import Modules
> 3. Ejecutar STEP 1 - Initialize Database
> 4. Ejecutar STEP 2 - Extract Data (mostrar tablas)
> 5. Ejecutar STEP 3 - Profile Data (mostrar reporte)
> 6. Ejecutar STEP 4 - Clean Data (mostrar antes/despues)
> 7. Ejecutar STEP 5 - Transform Data (mostrar metricas)
> 8. Ejecutar STEP 6 - Validate Data (mostrar passed)
> 9. Ejecutar STEP 7 - Load Data (mostrar tablas)
> 10. Ejecutar STEP 8 - Queries (mostrar resultados)
> 11. Ejecutar STEP 9 - Charts (mostrar graficas)

---

## TIEMPO TOTAL ESTIMADO: 20 minutos

| Parte | Tema | Tiempo | Responsable |
|-------|------|--------|-------------|
| 1 | Introduccion | 2 min | Integrante 1 |
| 2 | Arquitectura y Porque de Scripts | 3 min | Integrante 2 |
| 3 | Proceso ETL Detallado | 3 min | Integrante 3 |
| 4 | Base de Datos SQLite | 2 min | Integrante 4 |
| 5 | Notebook Interactivo | 3 min | Integrante 1 |
| 6 | Graficas de Analisis | 2 min | Integrante 2 |
| 7 | Pruebas y Calidad | 1 min | Integrante 3 |
| 8 | Conclusiones | 1 min | Integrante 4 |
| 9 | Demo en Vivo | 3 min | Integrante 4 |

---

## PREGUNTAS FRECUENTES

**P: Por que usaron SQLite y no PostgreSQL?**
R: SQLite es ideal para este proyecto por su simplicidad, no requiere servidor y es portatil. Para produccion se migraria a PostgreSQL.

**P: Cuantos registros se perdieron en la limpieza?**
R: 8 registros de 763 (1.05%). Fueron por duplicados (3), valores invalidos (2) y nulos (3).

**P: Como manejan las fechas de diferentes formatos?**
R: Usamos un parser multicapa que intenta 3 formatos: YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY, con fallback a dayfirst=True.

**P: Es escalable este pipeline?**
R: Si. Los modulos estan desacoplados y se puede adaptar a nuevas fuentes de datos facilmente.

**P: Por que 4 graficas y no mas?**
R: Seleccionamos las 4 mas relevantes para decisiones de negocio: productos estrella, cumplimiento de metas, tendencia temporal y distribucion por categoria.

**P: Que pasaria si agregamos una nueva ciudad?**
R: Solo necesitariamos agregar un nuevo extractor (ej: extract_mysql.py) y mapear las columnas al esquema unificado.

**P: Como se ejecutan las pruebas?**
R: Con el comando `pytest tests/` desde la raiz del proyecto. Se ejecutan las 50 pruebas en aproximadamente 3 segundos.
