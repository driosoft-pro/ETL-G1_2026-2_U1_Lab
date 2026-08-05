# Guion de Presentacion - Proyecto 1b: ETL Pipeline Retail Analytics

## Integrantes
1. Integrante 1
2. Integrante 2
3. Integrante 3
4. Integrante 4

---

## ESTRUCTURA DE LA PRESENTACION

### Parte 1: Introduccion (2 min)
**Integrante 1**

> Buenas tardes. Nuestro proyecto es un pipeline ETL completo para analisis de datos de retail. El objetivo es extraer, transformar y cargar datos de ventas de tres ciudades colombianas: Cali, Bogota y Medellin, para generar reportes analiticos que apoyen la toma de decisiones de negocio.

> El problema que resolvemos es consolidar datos de multiples fuentes con formatos diferentes (CSV, JSON, XML) en una unica base de datos analitica, aplicando reglas de calidad y generando metricas clave.

---

### Parte 2: Arquitectura del Sistema (2 min)
**Integrante 2**

> Nuestro sistema esta compuesto por 6 modulos principales:

- **extract.py** - Lee datos de CSV, JSON y XML, unificando el esquema
- **profiling.py** - Analiza calidad de datos: nulos, duplicados, invalidos
- **clean.py** - Limpia y estandariza: fechas, duplicados, case normalization
- **transform.py** - Genera metricas: ventas brutas, descuentos, ventas netas
- **validate.py** - Verifica integridad: IDs unicos, FK, formulas
- **load.py** - Exporta a CSV y carga en SQLite

> La base de datos tiene 5 tablas: sales_analytics, products, stores, promotions, monthly_targets.

---

### Parte 3: Proceso ETL (3 min)
**Integrante 3**

**EXTRACT:**
> Extraemos 763 registros de ventas de 3 fuentes:
> - CSV (Cali): 241 filas
> - JSON (Bogota): 281 filas
> - XML (Medellin): 241 filas
> Ademas de 4 tablas de referencia: productos, tiendas, promociones, metas mensuales.

**CLEAN:**
> Limpiamos los datos eliminando:
> - 3 registros duplicados
> - 2 cantidades invalidas
> - 1 precio invalido
> - 2 precios nulos
> Resultado: 755 registros validos de 763 originales.

**TRANSFORM:**
> Calculamos metricas clave:
> - gross_sales = cantidad x precio unitario
> - discount_amount = ventas brutas x porcentaje descuento
> - net_sales = ventas brutas - descuento
> - month, week, day_name para analisis temporal

---

### Parte 4: Base de Datos y Consultas (2 min)
**Integrante 4**

> Cargamos toda la informacion en SQLite con 5 tablas:
> - sales_analytics: 239 registros (consulta consolidada)
> - products: 15 productos
> - stores: 3 tiendas
> - promotions: 6 promociones
> - monthly_targets: 9 metas mensuales

> Ejecutamos 6 consultas analiticas:
> 1. Top productos por ventas netas
> 2. Rendimiento mensual vs metas
> 3. Analisis regional
> 4. Ventas por region
> 5. Ventas por categoria
> 6. Cumplimiento de objetivos

---

### Parte 5: Visualizacion y Analisis (2 min)
**Integrante 1**

> Presentamos 4 graficas clave de analisis de negocio:

> 1. **Top 10 productos + Distribucion por categoria** - Identificamos los productos estrella y su contribucion por categoria.

> 2. **Cumplimiento de metas + Heatmap de ingresos** - Visualizamos que tiendas y meses cumplieron objetivos, y la relacion categoria-tienda.

> 3. **Tendencia mensual** - Mostramos la evolucion de ingresos y unidades vendidas en el tiempo.

> Estas graficas permiten identificar oportunidades de mejora y areas de exito.

---

### Parte 6: Calidad y Pruebas (1 min)
**Integrante 2**

> Contamos con 50 pruebas automatizadas:
> - test_extract: 9 pruebas
> - test_profiling: 13 pruebas
> - test_clean: 10 pruebas
> - test_transform: 8 pruebas
> - test_validate: 7 pruebas
> - test_load: 5 pruebas

> Todas pasan al 100%, verificando integridad de datos y funcionalidad del pipeline.

---

### Parte 7: Conclusiones (1 min)
**Integrante 3**

> Conclusiones:
> - Pipeline ETL completo y funcional
> - Datos de 3 ciudades consolidados exitosamente
> - Calidad de datos verificada con 50 pruebas
> - Metricas de negocio calculadas automaticamente
> - Visualizaciones para toma de decisiones

> Tecnologias utilizadas: Python, Pandas, SQLite, Matplotlib, Seaborn, Pytest.

---

### Parte 8: Demostracion en Vivo (3 min)
**Integrante 4**

> Ahora mostraremos el notebook interactivo ejecutandose en tiempo real...

> [Abrir main.ipynb y ejecutar celda por celda]

---

## TIEMPO TOTAL ESTIMADO: 15 minutos

| Parte | Tema | Tiempo | Responsable |
|-------|------|--------|-------------|
| 1 | Introduccion | 2 min | Integrante 1 |
| 2 | Arquitectura | 2 min | Integrante 2 |
| 3 | Proceso ETL | 3 min | Integrante 3 |
| 4 | BD y Consultas | 2 min | Integrante 4 |
| 5 | Visualizacion | 2 min | Integrante 1 |
| 6 | Calidad y Pruebas | 1 min | Integrante 2 |
| 7 | Conclusiones | 1 min | Integrante 3 |
| 8 | Demo en Vivo | 3 min | Integrante 4 |

---

## PREGUNTAS FRECUENTES

**P: Por que usaron SQLite y no PostgreSQL?**
R: SQLite es ideal para este proyecto por su simplicidad, no requiere servidor y es portatil. Para produccion se migraria a PostgreSQL.

**P: Cuantos registros se perdieron en la limpieza?**
R: 8 registros de 763 (1.05%). Fueron por duplicados, valores invalidos y nulos.

**P: Como manejan las fechas de diferentes formatos?**
R: Usamos un parser multicapa que intenta 3 formatos: YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY.

**P: Es escalable este pipeline?**
R: Si. Los modulos estan desacoplados y se puede adaptar a nuevas fuentes de datos facilmente.
