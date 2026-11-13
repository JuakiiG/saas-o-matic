# SPEC-03 · Simulaciones y persistencia

| | |
|---|---|
| **Estado** | `aprobada` (2026-11-13) |
| **Requisitos** | R-05 y la parte de backend de R-11 |
| **Supuestos** | A3, A4, A6, A7, A9, A13, A14, A16 y A18 (`decidido`). A3, confirmado por la respuesta del 2026-11-13; A4, solo en parte: la lista de países es decisión propia |
| **Depende de** | SPEC-01 (cliente) y SPEC-02 (cálculo), las dos aprobadas el 2026-11-13 |
| **Bloqueos para aprobarla** | Ninguno desde el 2026-11-13: A3 y A4 decididos (apartado 9) y aprobación a la vez que SPEC-01 y SPEC-02, las tres del bloque backend (índice de specs) |

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
| `customer_id` | Petición | Entero de 1 a 9223372036854775807, de un cliente existente |
| `active_users` | Petición | Entero de 0 a 100.000 (A7) |
| `storage_gb` | Petición | Almacenamiento contratado, en GB. Entero de 0 a 1.000.000 |
| `estimated_api_calls` | Petición | Llamadas a la API estimadas al mes. Entero de 0 a 1.000.000.000 |
| Cálculo | Sistema | El resultado completo de la función de SPEC-02 para `active_users` y el país del cliente |
| `id`, `created_at` | Sistema | Entero de 1 a 9223372036854775807; fecha y hora UTC en ISO 8601 con precisión de segundos (`2026-11-12T15:00:00Z`) |

`storage_gb` y `estimated_api_calls` se validan y se guardan, pero **no
intervienen en el importe** (A3).

### 2.2 Qué se guarda del cálculo

Se guarda **todo lo que devuelve el cálculo**, no solo el total: país con
el que se calculó, coste base, tipo impositivo aplicado, impuesto, total y el
desglose de los tres tramos (límites, precio por usuario, usuarios y subtotal
de cada uno).

*Por qué*: A4 ya exige guardar el tipo aplicado para que una simulación
antigua siga mostrando lo que se calculó entonces. El mismo argumento vale
para la tarifa: si un precio o un límite de tramo cambia, un desglose
recalculado dejaría de sumar el coste base guardado.

Una simulación guardada **nunca se recalcula**: el historial lee solo lo
guardado en la simulación, incluido su `country`, sin consultar el país del
cliente ni las constantes del dominio.

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

**Tablas** (los tipos son los de SQLite). El DDL vive en el backend, en un
`schema.sql` versionado que se aplica al arrancar (ADR-004); se escribe con
el esqueleto del backend. `02-arquitectura/` muestra el modelo y enlaza a
ese fichero; no guarda una segunda copia del DDL.

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
| `created_at` | TEXT | No nulo. UTC, ISO 8601, precisión de segundos |
| — | — | `UNIQUE (country, tax_id)` (SPEC-01/E-19) |

`simulations`

| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | INTEGER | Clave primaria |
| `customer_id` | INTEGER | No nulo. Clave foránea a `customers(id)`, sin borrado en cascada |
| `active_users` | INTEGER | No nulo. `>= 0` |
| `storage_gb` | INTEGER | No nulo. `>= 0` |
| `estimated_api_calls` | INTEGER | No nulo. `>= 0` |
| `country` | TEXT | No nulo. País del cliente en el momento del cálculo |
| `base_cents` | INTEGER | No nulo. `>= 0` |
| `tax_rate_bp` | INTEGER | No nulo. `>= 0` |
| `tax_cents` | INTEGER | No nulo. `>= 0` |
| `total_cents` | INTEGER | No nulo. `= base_cents + tax_cents` |
| `created_at` | TEXT | No nulo. UTC, ISO 8601, precisión de segundos |
| — | — | Índice `idx_simulations_customer_id` sobre `customer_id` |

`simulation_tiers` — tres filas por simulación.

| Columna | Tipo | Restricciones |
|---|---|---|
| `simulation_id` | INTEGER | No nulo. Clave foránea a `simulations(id)` |
| `position` | INTEGER | No nulo. 1, 2 o 3 |
| `from_users` | INTEGER | No nulo. `>= 1` |
| `to_users` | INTEGER | Nulo en el último tramo. `to_users IS NULL OR to_users >= from_users` |
| `unit_price_cents` | INTEGER | No nulo. `>= 0` |
| `users` | INTEGER | No nulo. `>= 0` |
| `subtotal_cents` | INTEGER | No nulo. `= unit_price_cents * users` |
| — | — | Clave primaria `(simulation_id, position)` |

**Reglas**:

- **Todo importe es `INTEGER` en céntimos**; ningún `REAL` en el esquema
  (A6).
- **Las tres tablas son `STRICT`**: la base de datos rechaza un valor que no
  es del tipo de su columna, como `10.5` en `base_cents` o `'abc'` en
  `active_users`. Un valor que SQLite convierte sin pérdida (el real `15.0`
  o el texto `'15'`) se guarda como el entero `15`. *Por qué: en SQLite el
  tipo declarado es solo una afinidad; sin `STRICT`, una columna `INTEGER`
  guarda `10.5` como real, y un importe con decimales nunca puede ser
  cierto (E-19, A6).* Exige SQLite 3.37.0 o posterior (ADR-004).
- **`simulations` tiene un índice sobre `customer_id`**, creado con
  `CREATE INDEX IF NOT EXISTS` junto a las tablas. *Por qué: la ficha
  cuenta y lee las simulaciones de un cliente en cada petición, y SQLite no
  crea un índice para una clave foránea; sin él, cada ficha recorre la
  tabla entera.* Una base de datos que ya existe lo recibe en el siguiente
  arranque.
- Cada conexión ejecuta `PRAGMA foreign_keys = ON` (ADR-001).
- La simulación y sus tres tramos se guardan en **una sola transacción**: o
  se guardan las cuatro filas o ninguna.
- Los límites superiores (100.000 usuarios, etc.) los valida la API; la base
  de datos solo impide lo que nunca puede ser cierto (valores de otro tipo,
  negativos, sumas que no cuadran, referencias rotas). *Por qué: un máximo de negocio puede
  cambiar sin migrar datos; una suma que no cuadra es siempre un error.*
- Las reglas de negocio no viven en SQL: la base de datos guarda lo que el
  dominio calculó y no calcula nada.
- Toda sentencia recibe sus valores como parámetros.
- El fichero de la base de datos se crea al arrancar si no existe, con
  sentencias `CREATE TABLE IF NOT EXISTS`. Su ruta se configura con la
  variable de entorno `DATABASE_PATH`, cuyo valor por defecto es
  `backend/data/saas-o-matic.db`, relativo a la raíz del repositorio; git
  lo ignora (`*.db` en `.gitignore`). Si el directorio no existe, se crea.
  No hay herramienta de migraciones.

Las alternativas y las consecuencias de estas decisiones (tres tablas, foto
completa del cálculo, sin migraciones) están en ADR-004.

### 2.7 Operación del backend

**CORS** (A16). El backend solo admite peticiones de navegador desde los
orígenes de la variable de entorno `CORS_ORIGINS`, una lista separada por
comas cuyo valor por defecto es `http://localhost:4200`, el origen del
frontend en local. A una petición con un `Origin` de la lista se le responde
con `access-control-allow-origin` igual a ese origen; a cualquier otra, sin
esa cabecera. Nunca se responde con `*`. Los métodos admitidos son `GET` y
`POST`, y la cabecera admitida, `content-type`, además de las que la norma
CORS admite siempre (`accept`, `accept-language` y `content-language`), que
el middleware estándar anuncia junto a ella: `access-control-allow-headers`
vale `Accept, Accept-Language, Content-Language, Content-Type`. Ese valor
exacto lo fija un test con la versión fijada del framework.

La cabecera acompaña a **cualquier respuesta** a un origen admitido,
también a las de error y, en particular, al `500`. *Por qué*: sin ella el
navegador oculta la respuesta al frontend, que vería un `network_error` en
lugar de `internal_error`.

**Comprobación previa (`OPTIONS`).** La atiende el middleware de CORS, no
las rutas, y queda **fuera de la regla del `405`** (4.3). Es la petición
`OPTIONS` que el navegador envía por su cuenta, con las cabeceras `Origin`
y `Access-Control-Request-Method`, antes de un `POST` con cuerpo JSON:

- **Admitida** (origen, método y cabecera admitidos): `200`, con las
  cabeceras CORS que admiten ese origen, los métodos y `content-type`.
- **Rechazada** (por el origen, por el método o por la cabecera): la
  respuesta es **la estándar del middleware de CORS del framework, sin
  código a medida**. Lo único que esta spec exige de ella es que, si el
  origen no está admitido, **no lleve `access-control-allow-origin`**. Su
  estado y sus cabeceras exactos los fija un test con la versión fijada
  del framework, para que un cambio de versión no pase inadvertido. Se
  espera un `400`; **no está verificado**.

La comprobación previa rechazada es una **excepción documentada a
`application/problem+json`** (A14): no lleva el cuerpo de error de la API.
*Por qué*: esa respuesta la consume el navegador, no el frontend, que nunca
llega a leerla.

**Un `OPTIONS` que no es una comprobación previa** (sin `Origin` o sin
`Access-Control-Request-Method`) no lo atiende el middleware: llega a las
rutas y responde `405` `method_not_allowed`, como cualquier otro método no
admitido (4.3).

**`GET /health`** (A13). Comprueba que el backend está levantado y que la
base de datos responde a una consulta trivial. No lee ni escribe datos de
negocio.

**Errores genéricos.** La tabla de códigos está en las convenciones comunes
del índice y vale para todos los endpoints. Aquí están su requisito y sus
casos de prueba, para que no queden sin demostrar.

## 3. Requisitos (EARS)

### `POST /simulations`

| Id | Requisito | Cubre |
|---|---|---|
| E-01 | Cuando recibe una simulación válida de un cliente existente, el sistema deberá calcular el importe, guardar la simulación con su cálculo y responder `201` con la simulación creada. | R-05 |
| E-02 | El sistema deberá calcular el importe de la simulación con la misma función del dominio que usa `POST /pricing/quote`. | A9 |
| E-03 | El sistema deberá guardar, junto con los datos de entrada, el país con el que se calculó, el coste base, el tipo impositivo aplicado, el impuesto, el total y el desglose de los tres tramos. | R-05, A4 |
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
| E-16 | El sistema deberá devolver de cada simulación los importes y el país (`country`) guardados con ella, sin recalcular los importes ni consultar el país actual del cliente. | A4 |
| E-17 | El sistema no deberá incluir en el historial de un cliente simulaciones de otro. | R-11 |

### Inmutabilidad y persistencia

| Id | Requisito | Cubre |
|---|---|---|
| E-18 | El sistema no deberá ofrecer ninguna operación que modifique o elimine una simulación o un cliente. | A18 |
| E-19 | El sistema deberá guardar todos los importes como enteros en céntimos y los tipos como enteros en puntos básicos. | A6 |
| E-20 | Si se intenta guardar una simulación de un cliente inexistente, o borrar un cliente con simulaciones, entonces la base de datos deberá rechazarlo. | ADR-001 |
| E-21 | Si se intenta guardar una fila con un valor que no es del tipo de su columna (un importe con decimales, un texto en una columna entera), una fila con un valor negativo, una simulación cuyo total no es la suma de base e impuesto, un tramo cuyo subtotal no es el precio por los usuarios, un tramo con una posición distinta de 1, 2 o 3, un tramo repetido, un tramo cuyo límite inferior es menor que 1 o un tramo cuyo límite superior es menor que el inferior, entonces la base de datos deberá rechazarlo. | A6 |
| E-22 | Cuando el backend arranca y la base de datos no existe, el sistema deberá crearla con todas sus tablas; cuando ya existe, deberá conservar sus datos. | R-05 |
| E-32 | Mientras `DATABASE_PATH` no está definida, el sistema deberá usar la ruta `backend/data/saas-o-matic.db`. | R-18 |
| E-23 | El sistema deberá pasar a la base de datos todos los valores como parámetros de la sentencia. | — |

### Operación del backend

| Id | Requisito | Cubre |
|---|---|---|
| E-24 | Cuando recibe una petición con una cabecera `Origin` incluida en `CORS_ORIGINS`, el sistema deberá responder con `access-control-allow-origin` igual a ese origen, también cuando la respuesta es un error, incluido el `500`. | A16 |
| E-25 | Si la cabecera `Origin` de una petición no está en `CORS_ORIGINS`, entonces el sistema deberá responder sin la cabecera `access-control-allow-origin`. | A16 |
| E-26 | Mientras `CORS_ORIGINS` no está definida, el sistema deberá admitir únicamente el origen `http://localhost:4200`. | A16 |
| E-27 | Cuando recibe `GET /health` y la base de datos responde, el sistema deberá responder `200` con `{"status":"ok"}`. | A13 |
| E-28 | Si recibe `GET /health` y la base de datos no responde, entonces el sistema deberá responder `503` con el código `service_unavailable`, sin trazas ni detalles internos. | A13 |
| E-29 | Si una petición a cualquier endpoint incurre en uno de los errores genéricos de las convenciones comunes, entonces el sistema deberá responder en `application/problem+json` con el estado y el `code` de esa tabla, sin trazas ni detalles internos; si incurre en varios a la vez, deberá responder con el de mayor precedencia: `415`, después `400` y después `422`. | A14 |
| E-30 | Cuando recibe una comprobación previa `OPTIONS` con un `Origin` incluido en `CORS_ORIGINS`, el sistema deberá responder `200` con las cabeceras CORS que admiten ese origen, en lugar de `405`. | A16 |
| E-31 | Si recibe una comprobación previa `OPTIONS` con un `Origin` que no está en `CORS_ORIGINS`, entonces el sistema deberá rechazarla con la respuesta estándar del middleware de CORS, que no deberá llevar la cabecera `access-control-allow-origin`. | A16 |
| E-33 | Si recibe un `OPTIONS` que no es una comprobación previa, entonces el sistema deberá responder `405` con el código `method_not_allowed`. | A14 |

## 4. Contratos

### 4.1 `POST /simulations`

| Campo | Tipo | Obligatorio | Regla |
|---|---|---|---|
| `customer_id` | entero | sí | De 1 a 9223372036854775807, y de un cliente existente |
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
| `503` | `service_unavailable` | La base de datos no puede abrirse o consultarse (error genérico de las convenciones comunes) | — |

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

Cualquier método que una ruta no admite responde `405` en
`application/problem+json` con el código `method_not_allowed`. Es la
convención común del índice; aquí interesa porque es lo que hace comprobable
A18: `PUT`, `PATCH` y `DELETE` sobre `/customers`, `/customers/{id}` y
`/simulations`, y también `GET /simulations`, que no existe.

**Excepción**: la comprobación previa de CORS, que es un `OPTIONS` con
`Origin` y `Access-Control-Request-Method`. La atiende el middleware antes
de llegar a las rutas y no responde `405` (2.7). Cualquier otro `OPTIONS`
sí responde `405`.

### 4.4 `GET /health`

Respuesta `200`:

```json
{ "status": "ok" }
```

| Estado | `code` | Cuándo |
|---|---|---|
| `503` | `service_unavailable` | La base de datos no responde |

El `503` va en `application/problem+json`, como el resto de errores.

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
| `customer_id` | `0`, `-1`, `9223372036854775808` (2^63) | `422` | `out_of_range` |
| `customer_id` | `9223372036854775807` (no existe), resto válido | `404` | — |
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
| Cambiar directamente en la base de datos el país del cliente a `DE` | — |
| `GET /customers/{id}` | Las dos simulaciones siguen mostrando `country` `ES`: se lee de la simulación, no del cliente |

### 5.5 Restricciones de la base de datos (inserciones directas)

| Inserción directa | Resultado |
|---|---|
| Simulación con `customer_id` inexistente | Rechazada por la clave foránea |
| Borrado de un cliente con simulaciones | Rechazado por la clave foránea |
| Simulación con `active_users` = −1 | Rechazada |
| Simulación con `total_cents` ≠ `base_cents + tax_cents` | Rechazada |
| Tramo con `subtotal_cents` ≠ `unit_price_cents * users` | Rechazado |
| Cuarto tramo (`position` = 4) o tramo repetido | Rechazado |
| Tramo con `from_users` = 0 o `from_users` = −1 | Rechazado |
| Tramo con `to_users` menor que `from_users` (11 y 10) | Rechazado |
| Tramo con `to_users` igual a `from_users`, o con `to_users` nulo | Aceptado |
| Simulación con `base_cents` = 14000.5 y un total que cuadra (16940.5) | Rechazada por el tipo |
| Simulación con `active_users` = `'abc'` | Rechazada por el tipo |
| Tramo con `unit_price_cents` = 10.5 y un subtotal que cuadra (105) | Rechazado por el tipo |
| Tramo con `users` = `'many'`, precio 0 y subtotal 0 | Rechazado por el tipo |

### 5.6 Operación del backend

| Petición | Configuración | Resultado |
|---|---|---|
| `GET /meta` con `Origin: http://localhost:4200` | `CORS_ORIGINS` sin definir | `200` con `access-control-allow-origin: http://localhost:4200` |
| `GET /meta` con `Origin: http://otro.example` | `CORS_ORIGINS` sin definir | Respuesta sin `access-control-allow-origin` |
| `GET /meta` con `Origin: http://localhost:4200` | `CORS_ORIGINS=http://a.example,http://b.example` | Respuesta sin `access-control-allow-origin` |
| `GET /meta` con `Origin: http://b.example` | `CORS_ORIGINS=http://a.example,http://b.example` | `access-control-allow-origin: http://b.example` |
| `OPTIONS /customers` de comprobación previa, con `Origin: http://localhost:4200`, `Access-Control-Request-Method: POST` y `Access-Control-Request-Headers: content-type` | `CORS_ORIGINS` sin definir | `200`, no `405`, con `access-control-allow-origin: http://localhost:4200`, `POST` en `access-control-allow-methods` y `access-control-allow-headers: Accept, Accept-Language, Content-Language, Content-Type` (`content-type` y las que la norma CORS admite siempre) |
| La misma comprobación previa, con `Origin: http://otro.example` | `CORS_ORIGINS` sin definir | Rechazo estándar del middleware, sin `access-control-allow-origin`; el test compara el estado y todas las cabeceras con los valores fijados al implementar. No se exige `application/problem+json` |
| La misma comprobación previa, con `Origin: http://localhost:4200` y `Access-Control-Request-Method: DELETE` | `CORS_ORIGINS` sin definir | Rechazo estándar del middleware; el test compara el estado y todas las cabeceras con los valores fijados al implementar |
| Una petición con `Origin: http://localhost:4200` que provoca un fallo inesperado (como el de 5.7) | `CORS_ORIGINS` sin definir | `500` `internal_error` con `access-control-allow-origin: http://localhost:4200` |
| `GET /health` | Base de datos accesible | `200` `{"status":"ok"}` |
| `GET /health` | Base de datos inaccesible | `503` `service_unavailable`, sin trazas |

### 5.7 Errores genéricos

| Petición | Resultado |
|---|---|
| `POST /customers` con el cuerpo `{"company_name":` (JSON cortado) | `400` `malformed_request` |
| `POST /simulations` con el cuerpo `[1, 2]`, `null` o `15` | `400` `malformed_request` |
| `POST /pricing/quote` con `Content-Type: text/plain` | `415` `unsupported_media_type` |
| `POST /pricing/quote` con `Content-Type: application/json; charset=utf-8` y un cuerpo válido | `200`: `application/json` con parámetros es válido |
| `POST /simulations?debug=1` con `Content-Type: text/plain` y el cuerpo `{"customer_id":` | `415`: gana al `400` y al `422` |
| `POST /simulations?debug=1` con `Content-Type: application/json` y el cuerpo `{"customer_id":` | `400` `malformed_request`: gana al `422` |
| `GET /clientes` o `GET /customers/1/extra` | `404` `not_found` |
| `GET /simulations`, `POST /customers/1`, `DELETE /meta` | `405` `method_not_allowed` |
| `OPTIONS /customers` sin `Origin`, y `OPTIONS /customers` con `Origin: http://localhost:4200` pero sin `Access-Control-Request-Method` | `405` `method_not_allowed`: no es una comprobación previa |
| `POST /simulations?debug=1` con un cuerpo válido | `422` `validation_error`, con `unknown_field` en el campo `debug`; no se guarda nada |
| Un fallo inesperado, provocado en el test con un repositorio que lanza una excepción | `500` `internal_error`; el cuerpo no contiene trazas, nombres de ficheros ni el texto de la excepción |
| Una petición válida a un endpoint que lee o escribe la base de datos (`POST /customers`, `GET /customers/1`, `GET /customers?q=alfa`, `POST /pricing/quote`, `POST /simulations`), con el fichero de la base de datos apartado | `503` `service_unavailable`, sin trazas; el fichero no se vuelve a crear |

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
| CA-09 | Un test comprueba que `PUT`, `PATCH` y `DELETE` sobre las tres rutas de 4.3, y `GET /simulations`, devuelven `405` con `method_not_allowed`, y que los datos no cambian. | E-18 |
| CA-10 | Un test lee el esquema de la base de datos creada y comprueba que ninguna columna es `REAL` y que todas las acabadas en `_cents` o `_bp` son `INTEGER`. | E-19 |
| CA-11 | Tests reproducen cada fila de 5.5 sobre una conexión abierta como la de la aplicación. | E-20, E-21 |
| CA-12 | Un test arranca la aplicación con una ruta de base de datos inexistente y comprueba que se crea con las tres tablas; la arranca de nuevo y comprueba que los datos guardados siguen ahí. Otro test comprueba que, sin `DATABASE_PATH`, la configuración da la ruta `backend/data/saas-o-matic.db`, sin llegar a crear el fichero. | E-22, E-32 |
| CA-13 | Un test sustituye la conexión por una que registra las sentencias y comprueba que ningún valor de la petición aparece en el SQL ejecutado, solo en sus parámetros. | E-23 |
| CA-14 | El OpenAPI generado declara para `POST /simulations`, `GET /customers/{id}` y `GET /health` los campos, tipos y códigos de estado del apartado 4. | E-01, E-12, E-27 |
| CA-15 | Tests de integración reproducen las ocho filas de CORS de 5.6 (las cuatro de `GET /meta`, las tres comprobaciones previas y el `500`), arrancando la aplicación con cada valor de `CORS_ORIGINS`. En las dos comprobaciones previas rechazadas, el test compara el estado y el conjunto completo de cabeceras con valores escritos en el propio test. | E-24, E-25, E-26, E-30, E-31 |
| CA-16 | Tests de integración reproducen las dos filas de `GET /health` de 5.6; la base de datos inaccesible se simula con una conexión que falla. El cuerpo del `503` no contiene trazas ni rutas de ficheros. | E-27, E-28 |
| CA-17 | Tests de integración reproducen cada fila de 5.7, comprobando el estado, el `Content-Type` `application/problem+json` y el `code`. | E-29, E-33 |

## 7. Decisiones de diseño

Aprobadas las diez por el Tech Lead el 2026-11-12, con un cambio: el
historial se ordena solo por `id` descendente (2.4), no por fecha como
proponía la IA. D-02, D-06 y D-07 se registran además como ADR-004, y D-01,
que cambia el contrato de SPEC-01, en ADR-006. El criterio de qué decisiones llevan ADR está en `02-arquitectura/README.md`.

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
| D-10 | **Variable `DATABASE_PATH`** | Nombre de la variable de entorno con la ruta del fichero. Valor por defecto, fijado por el Tech Lead tras la segunda evaluación (N-13): `backend/data/saas-o-matic.db` | Otro nombre |

## 8. Cambios que provoca en otras specs

**Aplicados el 2026-11-12** por decisión del Tech Lead, tras la evaluación
independiente (H-01): con todo en borrador, mantener destinos incoherentes
no tiene sentido.

| Spec | Cambio | Estado |
|---|---|---|
| SPEC-01, 4.2 | La ficha añade `simulation_count` y `simulations` a los campos del alta | Aplicado |
| SPEC-01, CA-06 | La comparación entre el alta y la ficha excluye esos dos campos | Aplicado |
| SPEC-01, D-13 | Queda resuelta por D-01 de esta spec | Aplicado |
| SPEC-02, CA-08 | Remite a CA-03 de esta spec | Aplicado |

## 9. Pendiente antes de aprobar

**Nada pendiente desde el 2026-11-13.** El Tech Lead decidió A3 y A4 al
cumplirse la fecha límite, y la respuesta a la consulta llegó ese mismo
día, más tarde, sin cambiar ninguna regla de esta spec. La consulta está
cerrada (`supuestos.md`).

| Supuesto | Qué dice la respuesta | Efecto en esta spec |
|---|---|---|
| A3 · almacenamiento y API | No se tarifican; basta con registrarlos y mostrarlos en la simulación, sin coste | Ninguno: se guardan sin intervenir en ningún importe (E-04). Que se validen y sus máximos (D-04) siguen siendo decisión propia |
| A4 · países y tipos | Basta con el tipo general de IVA del país del cliente. No menciona qué países se admiten | Ninguno. Guardar el tipo con cada simulación sigue siendo decisión propia |

SPEC-01 y SPEC-02 forman con esta el bloque backend. Si cambian los campos
del cliente o del cálculo, cambian las tablas de 2.6 y los ejemplos.

## Historial

| Fecha | Cambio |
|---|---|
| 2026-11-12 | Primer borrador |
| 2026-11-12 | Revisión del Tech Lead: aprobadas D-01 a D-10; el historial se ordena solo por `id` descendente (2.4, E-13 y tabla 5.3, con una fila nueva de fecha atrasada) |
| 2026-11-12 | Correcciones de la evaluación independiente (`04-calidad/evaluacion-specs-01.md`), decididas por el Tech Lead: aplicados los cambios cruzados del apartado 8 (H-01); A4 y A16 en la cabecera (H-02); `405` para cualquier método no admitido, y el requisito E-29, la tabla 5.7 y CA-17 para los errores genéricos del índice (H-03); `customer_id` de 1 a 9223372036854775807 (H-04); nuevo apartado 2.7 «Operación del backend» con CORS y `GET /health`, E-24 a E-28, 4.4, 5.6, CA-15 y CA-16 (H-05); E-21 cubre el subtotal y la posición de los tramos (H-11); remisión a ADR-004 (H-20); columna `country` en `simulations` y precisión de `created_at` (H-23) |
| 2026-11-12 | Correcciones de la segunda evaluación independiente (`04-calidad/evaluacion-specs-02.md`), decididas por el Tech Lead: aprobación en bloque con SPEC-01 y SPEC-02 (N-01); `CHECK` de los límites de los tramos, con E-21 y tres filas en 5.5 (N-04); `OPTIONS` fuera de la regla del `405`, con E-30 y E-31, y cabeceras CORS también en el `500`, con E-24 y tres filas en 5.6 (N-05); el DDL vive en el `schema.sql` del backend (N-07); `application/json` con parámetros, precedencia `415` > `400` > `422` y valor por defecto de `DATABASE_PATH`, con E-29, E-32, tres filas en 5.7 y CA-12 (N-13); E-16 cubre el país guardado (N-17) |
| 2026-11-12 | Decisiones del Tech Lead sobre las cuestiones abiertas de la segunda respuesta: un `OPTIONS` que no es comprobación previa responde `405`, con E-33 y una fila en 5.7 (Q-01); la comprobación previa rechazada se queda con la respuesta estándar del middleware, sin código a medida, y solo se exige que no lleve `access-control-allow-origin`, con E-31, 2.7, 5.6 y CA-15 (Q-02); D-01 se registra en ADR-006 (Q-03) |
| 2026-11-13 | Decisión del Tech Lead al vencer la fecha límite sin respuesta externa: A3 y A4 pasan a `decidido (sin confirmación externa)` con la hipótesis ya documentada, sin cambios en las reglas; cabecera y apartado 9 actualizados. La consulta sigue abierta: si la respuesta llega, se aplica como cambio de esta spec |
| 2026-11-13 | Aprobación del Tech Lead: el estado pasa a `aprobada` (2026-11-13), a la vez que SPEC-01 y SPEC-02 (bloque backend) |
| 2026-11-13 | Llega la respuesta a la consulta: confirma A3 y, de A4, solo el uso del tipo general. El Tech Lead mantiene su visto bueno a esta spec. Cabecera y apartado 9 actualizados; la consulta queda cerrada. Motivo: registrar la fuente de cada supuesto. Sin cambios en reglas, requisitos, criterios ni casos |
| 2026-11-13 | Cambio pedido por el Tech Lead en la revisión del paso 1: las tres tablas pasan a ser `STRICT` (2.6), E-21 incluye el valor que no es del tipo de su columna y 5.5 gana cuatro filas. Motivo: sin `STRICT` la base de datos guardaba `10.5` en `base_cents` y `'abc'` en `active_users`, y un importe con decimales nunca puede ser cierto (E-19, A6). Versión mínima de SQLite, 3.37.0, anotada en ADR-004 |
| 2026-11-13 | Decisión del Tech Lead al revisar SPEC-01, ya implementada: fila nueva en 5.7 para el `503` `service_unavailable` de un endpoint que no es `GET /health`, y fila `503` en la tabla de errores de 4.1. Motivo: todo endpoint que lee la base de datos declara el `503` (regla de las convenciones comunes); la tabla 5.7 no tenía ese caso. E-29 y CA-17 no cambian de texto y lo cubren |
| 2026-11-13 | Decisión del Tech Lead al revisar el backend, ya implementado: índice `idx_simulations_customer_id` sobre `simulations(customer_id)`, creado con `CREATE INDEX IF NOT EXISTS` (2.6). Motivo: la ficha cuenta y lee las simulaciones de un cliente en cada petición, y una clave foránea sin índice obliga a recorrer la tabla entera. Sin cambios en requisitos ni criterios; un test comprueba que el plan de las consultas del historial usa el índice. Nota en ADR-004 |
| 2026-11-13 | Corrección de la evaluación independiente del backend (`04-calidad/evaluacion-backend-01.md`, H-10), decidida por el Tech Lead: 2.7 y la fila de la comprobación previa admitida de 5.6 dicen el valor exacto de `access-control-allow-headers` (`Accept, Accept-Language, Content-Language, Content-Type`). Sin cambio de comportamiento; E-30 y CA-15 no cambian de texto. Motivo: la spec decía «la cabecera admitida, `content-type`» y el middleware estándar anuncia además las tres que la norma CORS admite siempre; el test solo comprobaba que `content-type` estuviera |
