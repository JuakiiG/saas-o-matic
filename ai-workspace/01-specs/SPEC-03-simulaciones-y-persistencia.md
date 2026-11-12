# SPEC-03 · Simulaciones y persistencia

| | |
|---|---|
| **Estado** | `borrador` (2026-11-12) |
| **Requisitos** | R-05 y la parte de backend de R-11 |
| **Supuestos** | A6, A7, A9, A13, A14 y A18 (`decidido`) · A3 (`pendiente de confirmar`) |
| **Depende de** | SPEC-01 (cliente) y SPEC-02 (cálculo), las dos en `borrador` |
| **Bloqueos para aprobarla** | A3 sin respuesta (con fecha límite) · SPEC-01 y SPEC-02 sin aprobar |

## 1. Objetivo

Definir cómo se registra una simulación de consumo de un cliente, qué se
guarda de su cálculo, cómo se consulta el historial y qué reglas cumple la
base de datos.

**Dentro**: `POST /simulations`, el historial dentro de
`GET /customers/{id}`, las tablas y sus restricciones, la creación de la base
de datos.

**Fuera**: la tarifa y el impuesto (SPEC-02), los datos y la validación del
cliente (SPEC-01), la presentación del historial y la divisa (SPEC-04),
edición y borrado (A18).

## 2. Reglas de negocio

### 2.1 Datos de una simulación

| Campo | Quién lo pone | Regla |
|---|---|---|
| `customer_id` | Petición | Cliente existente |
| `active_users` | Petición | Entero de 0 a 100.000 (A7) |
| `storage_gb` | Petición | Almacenamiento contratado, en GB. Entero de 0 a 1.000.000 |
| `estimated_api_calls` | Petición | Llamadas a la API estimadas al mes. Entero de 0 a 1.000.000.000 |
| Cálculo | Sistema | El resultado completo de la función de SPEC-02 para `active_users` y el país del cliente |
| `id`, `created_at` | Sistema | Entero positivo; fecha y hora UTC en ISO 8601 con precisión de segundos |

`storage_gb` y `estimated_api_calls` se validan y se guardan, pero **no
intervienen en el importe** (A3).

### 2.2 Qué se guarda del cálculo

Se guarda **todo lo que devuelve el cálculo**, no solo el total: coste base,
tipo impositivo aplicado, impuesto, total y el desglose de los tres tramos
(límites, precio por usuario, usuarios y subtotal de cada uno).

*Por qué*: A4 ya exige guardar el tipo aplicado para que una simulación
antigua siga mostrando lo que se calculó entonces. El mismo argumento vale
para la tarifa: si un precio o un límite de tramo cambia, un desglose
recalculado dejaría de sumar el coste base guardado.

Una simulación guardada **nunca se recalcula**: el historial lee los importes
guardados.

### 2.3 Un solo cálculo

`POST /simulations` llama a la misma función del dominio que
`POST /pricing/quote` (SPEC-02/E-08). La petición no puede aportar importes,
tipo impositivo ni país.

### 2.4 Historial

- Se obtiene dentro de `GET /customers/{id}`, como dice A13 («ficha del
  cliente con su historial»). No hay un endpoint de simulaciones aparte.
- Orden: **solo por `id` descendente**, la última guardada primero. *Por
  qué*: el `id` refleja el orden real de inserción; la fecha puede empatar o
  desajustarse si cambia el reloj.
- Se devuelven **como máximo las 50 de `id` más alto**, junto con el número
  total de simulaciones del cliente.

### 2.5 Inmutabilidad

Las simulaciones no se modifican ni se eliminan (A18). La API no ofrece
ninguna operación para ello y la base de datos impide borrar un cliente que
tiene simulaciones.

### 2.6 Persistencia

**Tablas** (los tipos son los de SQLite; el DDL definitivo irá en
`02-arquitectura/` cuando se apruebe esta spec):

`customers` — campos de SPEC-01.

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | INTEGER | Clave primaria |
| `company_name` | TEXT | No nulo |
| `company_name_search` | TEXT | No nulo. Forma de búsqueda (SPEC-01/E-33) |
| `tax_id` | TEXT | No nulo. Normalizado |
| `contact_email` | TEXT | No nulo |
| `country` | TEXT | No nulo |
| `plan` | TEXT | No nulo |
| `created_at` | TEXT | No nulo |
| — | — | `UNIQUE (country, tax_id)` (SPEC-01/E-19) |

`simulations`

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | INTEGER | Clave primaria |
| `customer_id` | INTEGER | No nulo. Clave foránea a `customers(id)`, sin borrado en cascada |
| `active_users` | INTEGER | No nulo. `>= 0` |
| `storage_gb` | INTEGER | No nulo. `>= 0` |
| `estimated_api_calls` | INTEGER | No nulo. `>= 0` |
| `base_cents` | INTEGER | No nulo. `>= 0` |
| `tax_rate_bp` | INTEGER | No nulo. `>= 0` |
| `tax_cents` | INTEGER | No nulo. `>= 0` |
| `total_cents` | INTEGER | No nulo. `= base_cents + tax_cents` |
| `created_at` | TEXT | No nulo |

`simulation_tiers` — tres filas por simulación.

| Columna | Tipo | Restricciones |
|---|---|---|
| `simulation_id` | INTEGER | No nulo. Clave foránea a `simulations(id)` |
| `position` | INTEGER | No nulo. 1, 2 o 3 |
| `from_users` | INTEGER | No nulo |
| `to_users` | INTEGER | Nulo en el último tramo |
| `unit_price_cents` | INTEGER | No nulo. `>= 0` |
| `users` | INTEGER | No nulo. `>= 0` |
| `subtotal_cents` | INTEGER | No nulo. `= unit_price_cents * users` |
| — | — | Clave primaria `(simulation_id, position)` |

**Reglas**:

- **Todo importe es `INTEGER` en céntimos**; ningún `REAL` en el esquema
  (A6).
- Cada conexión ejecuta `PRAGMA foreign_keys = ON` (ADR-001).
- La simulación y sus tres tramos se guardan en **una sola transacción**: o
  se guardan las cuatro filas o ninguna.
- Los límites superiores (100.000 usuarios, etc.) los valida la API; la base
  de datos solo impide lo que nunca puede ser cierto (negativos, sumas que
  no cuadran, referencias rotas). *Por qué: un máximo de negocio puede
  cambiar sin migrar datos; una suma que no cuadra es siempre un error.*
- Las reglas de negocio no viven en SQL: la base de datos guarda lo que el
  dominio calculó y no calcula nada.
- Toda sentencia recibe sus valores como parámetros.
- El fichero de la base de datos se crea al arrancar si no existe, con
  sentencias `CREATE TABLE IF NOT EXISTS`. Su ruta se configura con la
  variable de entorno `DATABASE_PATH`. No hay herramienta de migraciones.

## 3. Requisitos (EARS)

### `POST /simulations`

| Id | Requisito | Cubre |
|---|---|---|
| E-01 | Cuando recibe una simulación válida de un cliente existente, el sistema deberá calcular el importe, guardar la simulación con su cálculo y responder `201` con la simulación creada. | R-05 |
| E-02 | El sistema deberá calcular el importe de la simulación con la misma función del dominio que usa `POST /pricing/quote`. | A9 |
| E-03 | El sistema deberá guardar, junto con los datos de entrada, el coste base, el tipo impositivo aplicado, el impuesto, el total y el desglose de los tres tramos. | R-05, A4 |
| E-04 | El sistema deberá guardar `storage_gb` y `estimated_api_calls` sin que intervengan en ningún importe. | A3 |
| E-05 | Si `active_users`, `storage_gb` o `estimated_api_calls` no es un número entero, es negativo o supera su máximo, entonces el sistema deberá rechazar la petición sin guardar nada. | A3, A7 |
| E-06 | Si falta un campo o la petición trae un campo no documentado, incluidos importes, tipo impositivo o país, entonces el sistema deberá rechazar la petición sin guardar nada. | A14 |
| E-07 | Si la petición no supera la validación, entonces el sistema deberá responder `422` con el código `validation_error` y el detalle de cada campo. | A14 |
| E-08 | Si el cliente indicado no existe, entonces el sistema deberá responder `404` con el código `customer_not_found`. | R-05 |
| E-09 | Si la petición tiene a la vez un error de validación y un cliente inexistente, entonces el sistema deberá responder `422`. | — |
| E-10 | Si el país del cliente no tiene tipo impositivo definido, entonces el sistema deberá responder `500` con el código `tax_rate_not_defined`, sin trazas, y no guardar nada. | SPEC-02/E-10 |
| E-11 | El sistema deberá guardar la simulación y su desglose de forma atómica: si algo falla, no queda ninguna fila. | R-05 |

### Historial

| Id | Requisito | Cubre |
|---|---|---|
| E-12 | Cuando recibe `GET /customers/{id}` de un cliente existente, el sistema deberá devolver, junto a los datos del cliente, sus simulaciones guardadas y el número total de ellas. | R-11, A13 |
| E-13 | El sistema deberá devolver las simulaciones ordenadas por `id` descendente, sin tener en cuenta `created_at`. | R-11 |
| E-14 | Mientras el cliente tiene más de 50 simulaciones, el sistema deberá devolver solo las 50 de `id` más alto. | A13 |
| E-15 | Cuando el cliente no tiene simulaciones, el sistema deberá devolver una lista vacía y un total de 0. | R-11 |
| E-16 | El sistema deberá devolver de cada simulación los importes guardados, sin recalcularlos. | A4 |
| E-17 | El sistema no deberá incluir en el historial de un cliente simulaciones de otro. | R-11 |

### Inmutabilidad y persistencia

| Id | Requisito | Cubre |
|---|---|---|
| E-18 | El sistema no deberá ofrecer ninguna operación que modifique o elimine una simulación o un cliente. | A18 |
| E-19 | El sistema deberá guardar todos los importes como enteros en céntimos y los tipos como enteros en puntos básicos. | A6 |
| E-20 | Si se intenta guardar una simulación de un cliente inexistente, o borrar un cliente con simulaciones, entonces la base de datos deberá rechazarlo. | ADR-001 |
| E-21 | Si se intenta guardar una fila con un valor negativo o cuyo total no es la suma de base e impuesto, entonces la base de datos deberá rechazarla. | A6 |
| E-22 | Cuando el backend arranca y la base de datos no existe, el sistema deberá crearla con todas sus tablas; cuando ya existe, deberá conservar sus datos. | R-05 |
| E-23 | El sistema deberá pasar a la base de datos todos los valores como parámetros de la sentencia. | — |

## 4. Contratos

### 4.1 `POST /simulations`

| Campo | Tipo | Obligatorio | Regla |
|---|---|---|---|
| `customer_id` | entero | sí | Cliente existente |
| `active_users` | entero | sí | De 0 a 100.000 |
| `storage_gb` | entero | sí | De 0 a 1.000.000 |
| `estimated_api_calls` | entero | sí | De 0 a 1.000.000.000 |

Los cuatro siguen la regla de SPEC-02: solo un número JSON entero. Se
rechazan cadenas, booleanos, `null` y números con parte decimal, incluido
`15.0`.

```json
{ "customer_id": 1, "active_users": 15, "storage_gb": 500, "estimated_api_calls": 250000 }
```

Respuesta `201`:

```json
{
  "id": 1,
  "customer_id": 1,
  "active_users": 15,
  "storage_gb": 500,
  "estimated_api_calls": 250000,
  "currency": "EUR",
  "tiers": [
    { "from_users": 1,  "to_users": 10,   "unit_price_cents": 1000, "users": 10, "subtotal_cents": 10000 },
    { "from_users": 11, "to_users": 50,   "unit_price_cents": 800,  "users": 5,  "subtotal_cents": 4000 },
    { "from_users": 51, "to_users": null, "unit_price_cents": 500,  "users": 0,  "subtotal_cents": 0 }
  ],
  "base_cents": 14000,
  "country": "ES",
  "tax_rate_bp": 2100,
  "tax_cents": 2940,
  "total_cents": 16940,
  "created_at": "2026-11-12T15:00:00Z"
}
```

Los campos del cálculo son exactamente los de `POST /pricing/quote`. No lleva
cabecera `Location`: no existe un endpoint para leer una simulación suelta.

| Estado | `code` | Cuándo | Códigos por campo |
|---|---|---|---|
| `404` | `customer_not_found` | No existe un cliente con ese `customer_id` | — |
| `422` | `validation_error` | La petición no es válida | `missing`, `not_an_integer`, `out_of_range`, `unknown_field` |
| `500` | `tax_rate_not_defined` | El país del cliente guardado no tiene tipo impositivo | — |

### 4.2 `GET /customers/{id}` (amplía SPEC-01, apartado 4.2)

A los datos del cliente se añaden dos campos:

```json
{
  "id": 1,
  "company_name": "Ejemplo Uno SL",
  "tax_id": "B12345674",
  "contact_email": "compras@ejemplo-uno.example",
  "country": "ES",
  "plan": "professional",
  "created_at": "2026-11-12T14:30:00Z",
  "simulation_count": 2,
  "simulations": [
    { "id": 2, "customer_id": 1, "active_users": 51, "…": "…", "total_cents": 51425, "created_at": "2026-11-12T15:05:00Z" },
    { "id": 1, "customer_id": 1, "active_users": 15, "…": "…", "total_cents": 16940, "created_at": "2026-11-12T15:00:00Z" }
  ]
}
```

Cada elemento de `simulations` tiene exactamente la forma de la respuesta de
4.1 (aquí abreviada con `…`). `simulation_count` es el total del cliente,
aunque `simulations` traiga solo 50. Los errores son los de SPEC-01.

### 4.3 Métodos no admitidos

`PUT`, `PATCH` y `DELETE` sobre `/customers`, `/customers/{id}` y
`/simulations` responden `405` en `application/problem+json` con el código
`method_not_allowed`.

## 5. Casos de prueba

Los importes salen de las tablas 5.1 y 5.2 de SPEC-02, ya verificadas.

### 5.1 Simulaciones válidas

| Cliente | `active_users` | `storage_gb` | `estimated_api_calls` | Base | Tipo (bp) | Impuesto | Total | Qué demuestra |
|---|---|---|---|---|---|---|---|---|
| `ES` | 15 | 500 | 250000 | 14000 | 2100 | 2940 | 16940 | Ejemplo del encargo |
| `ES` | 15 | 0 | 0 | 14000 | 2100 | 2940 | 16940 | Almacenamiento y llamadas a cero; mismo importe |
| `ES` | 15 | 1000000 | 1000000000 | 14000 | 2100 | 2940 | 16940 | Máximos; mismo importe (A3) |
| `ES` | 0 | 500 | 250000 | 0 | 2100 | 0 | 0 | Cero usuarios se guarda, con importe 0 |
| `ES` | 51 | 500 | 250000 | 42500 | 2100 | 8925 | 51425 | Los tres tramos con usuarios |
| `ES` | 100000 | 500 | 250000 | 50017000 | 2100 | 10503570 | 60520570 | Máximo de usuarios |
| `DE` | 15 | 500 | 250000 | 14000 | 1900 | 2660 | 16660 | El tipo sale del país del cliente |

### 5.2 Peticiones no válidas

Las filas de `active_users` de SPEC-02 (tabla 5.4) valen aquí sin cambios. Se
añaden:

| Campo | Valor | Resultado | Código por campo |
|---|---|---|---|
| `storage_gb` | `-1` | `422` | `out_of_range` |
| `storage_gb` | `1000001` | `422` | `out_of_range` |
| `storage_gb` | `500.5`, `500.0`, `"500"`, `true`, `null` | `422` | `not_an_integer` |
| `storage_gb` | ausente | `422` | `missing` |
| `estimated_api_calls` | `-1` | `422` | `out_of_range` |
| `estimated_api_calls` | `1000000001` | `422` | `out_of_range` |
| `estimated_api_calls` | `1.5`, `"1000"`, `true`, `null` | `422` | `not_an_integer` |
| `estimated_api_calls` | ausente | `422` | `missing` |
| `customer_id` | `"1"`, `1.0`, `null` | `422` | `not_an_integer` |
| `customer_id` | `0`, `-1` | `422` | `out_of_range` |
| `customer_id` | ausente | `422` | `missing` |
| adicional | `total_cents`, `tax_rate_bp`, `country` o `created_at` | `422` | `unknown_field` |
| varios | `storage_gb` = `-1` y `estimated_api_calls` ausente | `422` | los dos errores, cada uno en su campo |
| `customer_id` | `999` (no existe), resto válido | `404` | — |
| `customer_id` y `active_users` | `999` y `-1` | `422` | `out_of_range`: gana la validación |

En todas, el número de simulaciones guardadas no cambia.

### 5.3 Historial

Datos de partida: cliente 1 (`ES`) y cliente 2 (`DE`), y estas simulaciones
guardadas en este orden.

| `id` | Cliente | `active_users` | `created_at` | Total |
|---|---|---|---|---|
| 1 | 1 | 15 | `…T15:00:00Z` | 16940 |
| 2 | 2 | 15 | `…T15:01:00Z` | 16660 |
| 3 | 1 | 51 | `…T15:05:00Z` | 51425 |
| 4 | 1 | 0 | `…T15:05:00Z` | 0 |
| 5 | 1 | 10 | `…T14:00:00Z` | 12100 |

La 3 y la 4 tienen la misma fecha. La 5 se guardó la última pero con una
fecha anterior a todas, como si el reloj se hubiera atrasado; el test la
inserta con esa fecha de forma directa.

| Consulta | `simulation_count` | `id` en `simulations`, en orden | Qué demuestra |
|---|---|---|---|
| `GET /customers/1` | 4 | 5, 4, 3, 1 | Orden por `id` descendente: la 5 va primera aunque su fecha sea la más antigua, y el empate de fecha de la 3 y la 4 no influye; no aparece la del cliente 2 |
| `GET /customers/2` | 1 | 2 | Solo las suyas |
| Cliente sin simulaciones | 0 | — | Lista vacía, no ausente |
| Cliente con 55 simulaciones | 55 | las 50 de `id` más alto | Límite de 50 y total real |

### 5.4 Los importes guardados no se recalculan

| Paso | Resultado esperado |
|---|---|
| Guardar una simulación de 15 usuarios para un cliente `ES` | Total 16940, tipo 2100 |
| Sustituir en el test el tipo de `ES` por 1000 y el precio del tramo 1 por 2000 | — |
| `GET /customers/{id}` | La simulación sigue mostrando base 14000, tipo 2100, impuesto 2940, total 16940 y el mismo desglose |
| Guardar otra simulación de 15 usuarios | Usa los valores sustituidos: base 24000, tipo 1000, impuesto 2400, total 26400 |

### 5.5 Restricciones de la base de datos (inserciones directas)

| Inserción directa | Resultado |
|---|---|
| Simulación con `customer_id` inexistente | Rechazada por la clave foránea |
| Borrado de un cliente con simulaciones | Rechazado por la clave foránea |
| Simulación con `active_users` = −1 | Rechazada |
| Simulación con `total_cents` ≠ `base_cents + tax_cents` | Rechazada |
| Tramo con `subtotal_cents` ≠ `unit_price_cents * users` | Rechazado |
| Cuarto tramo (`position` = 4) o tramo repetido | Rechazado |

## 6. Criterios de aceptación

| Id | Criterio | Requisitos |
|---|---|---|
| CA-01 | Un test de integración envía el ejemplo de 4.1 y obtiene `201` y el cuerpo del ejemplo (salvo `id` y `created_at`). | E-01, E-03 |
| CA-02 | Un test de integración parametrizado reproduce cada fila de 5.1 y comprueba los importes en la respuesta y en las filas guardadas. | E-01, E-03, E-04 |
| CA-03 | Para cada fila de 5.1, los campos del cálculo de `POST /simulations` son idénticos a la respuesta de `POST /pricing/quote` con el mismo cliente y los mismos usuarios (cierra SPEC-02/CA-08). | E-02 |
| CA-04 | Tests de integración reproducen cada fila de 5.2 y las de SPEC-02 5.4, comprobando el estado, el `code`, el código por campo y que no se ha guardado nada. | E-05 a E-09 |
| CA-05 | Un test guarda directamente un cliente con un país sin tipo, llama a `POST /simulations` y obtiene el `500` con `tax_rate_not_defined`, sin trazas y sin ninguna simulación guardada. | E-10 |
| CA-06 | Un test provoca un fallo al guardar el segundo tramo y comprueba que no queda ninguna fila de esa simulación en ninguna de las dos tablas. | E-11 |
| CA-07 | Tests de integración reproducen cada fila de 5.3, comprobando `simulation_count`, los `id` y su orden. | E-12 a E-15, E-17 |
| CA-08 | Un test de integración reproduce los pasos de 5.4. | E-16 |
| CA-09 | Un test comprueba que `PUT`, `PATCH` y `DELETE` sobre las tres rutas de 4.3 devuelven `405` con `method_not_allowed`, y que los datos no cambian. | E-18 |
| CA-10 | Un test lee el esquema de la base de datos creada y comprueba que ninguna columna es `REAL` y que todas las acabadas en `_cents` o `_bp` son `INTEGER`. | E-19 |
| CA-11 | Tests reproducen cada fila de 5.5 sobre una conexión abierta como la de la aplicación. | E-20, E-21 |
| CA-12 | Un test arranca la aplicación con una ruta de base de datos inexistente y comprueba que se crea con las tres tablas; la arranca de nuevo y comprueba que los datos guardados siguen ahí. | E-22 |
| CA-13 | Un test sustituye la conexión por una que registra las sentencias y comprueba que ningún valor de la petición aparece en el SQL ejecutado, solo en sus parámetros. | E-23 |
| CA-14 | El OpenAPI generado declara para `POST /simulations` y `GET /customers/{id}` los campos, tipos y códigos de estado del apartado 4. | E-01, E-12 |

## 7. Decisiones de diseño

Aprobadas las diez por el Tech Lead el 2026-11-12, con un cambio: el
historial se ordena solo por `id` descendente (2.4), no por fecha como
proponía la IA.

| Id | Decisión | Aprobado | Alternativa descartada y coste |
|---|---|---|---|
| D-01 | **Dónde va el historial** (pendiente de SPEC-01/D-13) | Dentro de `GET /customers/{id}`, que es lo que dice A13 | `GET /customers/{id}/simulations`: respuestas más pequeñas, pero es un endpoint que A13 no recoge y obliga a cambiar ese supuesto |
| D-02 | **Guardar el desglose por tramos** | Sí, en la tabla `simulation_tiers`: la simulación guardada conserva todo lo que se calculó | No guardarlo y no mostrarlo en el historial (menos código, pero se pierde el porqué del importe), o guardarlo como texto JSON en una columna (una tabla menos, pero sin restricciones comprobables) |
| D-03 | **Unidades y nombres** | `storage_gb` en GB y `estimated_api_calls` en llamadas al mes. El encargo no da unidades | Otras unidades; solo cambian los nombres y los máximos |
| D-04 | **Máximos** | 1.000.000 GB y 1.000.000.000 de llamadas. Son inventados: A3 solo pide «un máximo razonable» | Otros valores. Los dos caben en un entero exacto de JavaScript |
| D-05 | **Límite del historial** | Las 50 más recientes más `simulation_count` | Sin límite: más simple, pero una respuesta que crece sin tope, justo lo que A13 evitó en el buscador |
| D-06 | **Restricciones `CHECK` en la base de datos** | Solo invariantes (no negativos, sumas que cuadran); los máximos de negocio, en la API | Repetir también los máximos en SQL: dos sitios que mantener |
| D-07 | **Creación del esquema** | `CREATE TABLE IF NOT EXISTS` al arrancar, sin herramienta de migraciones | Una herramienta de migraciones es una dependencia nueva para un esquema que nace completo |
| D-08 | **`405` con `method_not_allowed`** | Especificarlo y probarlo, para que A18 sea comprobable | No especificarlo y dejar el comportamiento por defecto del framework |
| D-09 | **Sin `Location` en el `201`** | No hay endpoint para una simulación suelta | Añadir `GET /simulations/{id}`: no lo pide ninguna vista |
| D-10 | **Variable `DATABASE_PATH`** | Nombre de la variable de entorno con la ruta del fichero | Otro nombre |

## 8. Cambios que provoca en otras specs

No se han aplicado: se aplican cuando se apruebe esta spec.

| Spec | Cambio |
|---|---|
| SPEC-01, 4.2 | La ficha deja de ser «el mismo objeto que devuelve el alta»: añade `simulation_count` y `simulations` |
| SPEC-01, CA-06 | La comparación entre el alta y la ficha debe excluir esos dos campos |
| SPEC-01, D-13 | Queda resuelta por D-01 de esta spec |
| SPEC-02, CA-08 | Queda cubierto por CA-03 de esta spec |

## 9. Pendiente antes de aprobar

| Asunto | Qué cambiaría en esta spec |
|---|---|
| A3 · almacenamiento y API | Si tuvieran precio, entrarían en el cálculo (SPEC-02) y habría que guardar su importe |
| SPEC-01 y SPEC-02 | Si cambian los campos del cliente o del cálculo, cambian las tablas de 2.6 y los ejemplos |

La fecha límite de A3 es la del índice de specs: viernes 13 de noviembre de
2026 a las 10:00.

## Historial

| Fecha | Cambio |
|---|---|
| 2026-11-12 | Primer borrador |
| 2026-11-12 | Revisión del Tech Lead: aprobadas D-01 a D-10; el historial se ordena solo por `id` descendente (2.4, E-13 y tabla 5.3, con una fila nueva de fecha atrasada) |
