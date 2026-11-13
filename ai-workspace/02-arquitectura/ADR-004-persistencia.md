# ADR-004 · Persistencia: tres tablas, foto completa del cálculo y sin migraciones

| | |
|---|---|
| **Estado** | `aceptado` (2026-11-12) |
| **Decide** | Tech Lead |
| **Requisitos** | R-05, R-11 |
| **Supuestos** | A4, A6, A18 |
| **Specs** | SPEC-03 (D-02, D-06, D-07) |
| **Relacionado** | ADR-001 (acceso a SQLite con `sqlite3`) |

## Contexto

`POST /simulations` debe **persistir el cálculo** (R-05) y la ficha del
cliente debe mostrar el historial de simulaciones guardadas (R-11). Las
simulaciones no se modifican ni se eliminan (A18).

ADR-001 ya decidió usar el módulo `sqlite3` de la biblioteca estándar con
SQL parametrizado. Quedaban tres preguntas con alternativas:

1. Qué se guarda de un cálculo.
2. Qué reglas comprueba la propia base de datos.
3. Cómo se crea y cómo evoluciona el esquema.

## 1. Qué se guarda del cálculo

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **Foto completa**: en `simulations`, el país, la base, el tipo, el impuesto y el total; en `simulation_tiers`, una fila por tramo con sus límites, su precio, sus usuarios y su subtotal | La simulación guardada conserva todo lo que se calculó y se explica sola; cada dato tiene su tipo y sus restricciones | Una tabla más y tres filas más por simulación; hay que guardar en una transacción |
| B | Solo los totales; el desglose se recalcula al mostrar | Una tabla menos | Si cambia un precio o un límite de tramo, el desglose recalculado deja de sumar la base guardada |
| C | Totales en columnas y el desglose como texto JSON en una columna | Una tabla menos y la foto completa | La base de datos no puede comprobar nada de ese texto; el JSON se convierte en un segundo contrato |
| D | Solo los totales, sin desglose en el historial | La opción más simple | Se pierde el porqué del importe |

**Decisión: opción A.**

*Por qué*: A4 ya exige guardar el tipo impositivo aplicado para que una
simulación antigua siga mostrando lo que se calculó entonces. El mismo
argumento vale para la tarifa y para el país: el historial debe leer **solo
lo guardado**, sin recalcular y sin consultar el país del cliente ni las
constantes del dominio. Por eso `simulations` guarda también `country`.

## 2. Qué comprueba la base de datos

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **Solo invariantes**: claves foráneas, unicidad, valores no negativos y sumas que cuadran (`total = base + impuesto`, `subtotal = precio × usuarios`, posición 1, 2 o 3) | Impide lo que nunca puede ser cierto, sin duplicar reglas de negocio | Un máximo de negocio mal validado en la API no lo frenaría la base de datos |
| B | Repetir también los máximos de negocio (100.000 usuarios, etc.) | Segunda barrera | Dos sitios que mantener; cambiar un máximo exigiría migrar el esquema |
| C | Ninguna restricción más allá de las claves | Esquema mínimo | Un fallo de programación podría guardar importes incoherentes sin que nada lo detecte |

**Decisión: opción A.**

*Por qué*: un máximo de negocio puede cambiar sin migrar datos; una suma
que no cuadra es siempre un error. Las reglas de negocio viven en el
dominio (`CLAUDE.md`); la base de datos guarda lo que el dominio calculó y
no calcula nada.

## 3. Creación y evolución del esquema

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **Un `schema.sql` versionado, aplicado al arrancar con `CREATE TABLE IF NOT EXISTS`** | Ninguna dependencia; levantar el proyecto en local no exige ningún paso previo (R-18) | No hay historial de cambios de esquema: un cambio posterior a tener datos habría que hacerlo a mano |
| B | Una herramienta de migraciones | Evolución ordenada del esquema | Una dependencia nueva y un paso más para un esquema que nace completo y sin datos que conservar |

**Decisión: opción A.**

*Por qué*: es lo más pequeño que cumple. El esquema se define entero antes
de escribir código y la herramienta solo se ejecuta en local.

## Resultado

Tres tablas, definidas en SPEC-03 (2.6):

| Tabla | Contenido |
|---|---|
| `customers` | Los campos de SPEC-01, más la forma de búsqueda del nombre. `UNIQUE (country, tax_id)` |
| `simulations` | Los datos de entrada y la foto del cálculo: país, base, tipo, impuesto y total |
| `simulation_tiers` | Tres filas por simulación, con el desglose |

Reglas comunes: todo importe es `INTEGER` en céntimos (A6); cada conexión
ejecuta `PRAGMA foreign_keys = ON` (ADR-001); la simulación y sus tramos se
guardan en una sola transacción; el historial se ordena por `id`
descendente, que refleja el orden real de inserción.

**Añadido el 2026-11-12**, tras la segunda evaluación independiente, sin
cambiar ninguna de las tres decisiones:

- Entre los invariantes del punto 2 están también los límites de cada
  tramo: `from_users >= 1` y `to_users IS NULL OR to_users >= from_users`
  (SPEC-03, 2.6 y E-21).
- El `schema.sql` del punto 3 vive en el backend y es la única copia del
  DDL; `02-arquitectura/README.md` muestra el modelo y enlaza a él.

**Añadido el 2026-11-13**, tras la revisión del paso 1 por el Tech Lead.
Amplía la opción A del punto 2, sin cambiar la decisión:

- Las tres tablas se crean como **`STRICT`**. *Por qué*: en SQLite el tipo
  declarado es solo una afinidad; una columna `INTEGER` aceptaba `10.5`
  (guardado como real) y `'abc'` (guardado como texto). Un importe con
  decimales nunca puede ser cierto (A6), así que es un invariante más de
  los que comprueba la base de datos.
- **Versión mínima: SQLite 3.37.0** (noviembre de 2021), la primera con
  tablas `STRICT`. La que acompaña al Python 3.12 del entorno de desarrollo
  es la 3.42.0. Con una versión anterior, el arranque falla al crear el
  esquema con un error de sintaxis; no arranca con tablas sin comprobar.
- `STRICT` convierte lo que se puede convertir sin pérdida (`15.0` y `'15'`
  se guardan como `15`) y rechaza el resto.
- `CREATE TABLE IF NOT EXISTS` no modifica una tabla que ya existe: una
  base de datos creada antes de este cambio sigue sin `STRICT` hasta que se
  borra el fichero. Es el coste ya aceptado en el punto 3 (sin migraciones).

**Añadido el 2026-11-13**, tras la revisión del backend entero por el Tech
Lead. Amplía la opción A del punto 3, sin cambiar la decisión:

- `simulations` tiene un **índice sobre `customer_id`**
  (`idx_simulations_customer_id`). *Por qué*: SQLite no crea un índice para
  una clave foránea, y la ficha de un cliente cuenta y lee sus simulaciones
  en cada petición; sin él, cada ficha recorre la tabla entera. El mismo
  índice sirve a la comprobación de la clave foránea al intentar borrar un
  cliente.
- Se crea con `CREATE INDEX IF NOT EXISTS` en el mismo `schema.sql`. A
  diferencia de `STRICT`, **sí llega a una base de datos que ya existe**:
  un índice se puede añadir a una tabla con datos, y el esquema se aplica
  en cada arranque.
- Coste: una escritura más por simulación guardada. Aceptado: se lee mucho
  más de lo que se escribe.

## Consecuencias

A favor:

- Una simulación guardada no cambia aunque cambien la tarifa, los tipos o
  el país del cliente, y se puede comprobar con un test (SPEC-03, 5.4).
- Las incoherencias las rechaza la base de datos, no solo el código.

En contra, y cómo se trata:

| Consecuencia | Tratamiento |
|---|---|
| Guardar una simulación son cuatro filas en dos tablas | Una sola transacción; un test provoca un fallo a medias y comprueba que no queda nada (SPEC-03, CA-06) |
| Leer el historial necesita unir dos tablas | Como máximo 50 simulaciones por respuesta (SPEC-03, D-05) |
| Sin migraciones, un cambio de esquema con datos es manual | Aceptado: el alcance no prevé evolución con datos reales |
| ADR-001 razonaba con «dos tablas» | Corregido en ADR-001: son tres. La decisión de usar `sqlite3` no cambia |

## Cuándo habría que revisarla

- Si la herramienta dejara de ser local o hubiera que conservar datos entre
  versiones: haría falta la opción B del punto 3.
- Si la tarifa dejara de tener tres tramos fijos: la restricción de
  posición 1, 2 o 3 tendría que cambiar.
