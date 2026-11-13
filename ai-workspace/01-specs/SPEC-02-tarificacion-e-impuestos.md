# SPEC-02 · Tarificación e impuestos

| | |
|---|---|
| **Estado** | `aprobada` (2026-11-13) |
| **Requisitos** | R-06, R-07 y la parte de cálculo de R-12 |
| **Supuestos** | A6, A7, A9, A13 y A14 (`decidido`) · A2, A3, A4 y A5 (`decidido (sin confirmación externa)`, 2026-11-13) |
| **Bloqueos para aprobarla** | Ninguno desde el 2026-11-13: A2, A3, A4 y A5 decididos sin confirmación externa (apartado 8) y aprobación a la vez que SPEC-01 y SPEC-03, las tres del bloque backend (índice de specs) |

## 1. Objetivo

Definir cómo se calcula el importe mensual de una suscripción a partir del
número de usuarios y del país del cliente, y el endpoint que devuelve ese
cálculo sin guardarlo.

**Dentro**: tarifa por tramos, impuesto, redondeo, desglose,
`POST /pricing/quote` y la constante de países admitidos con sus tipos
(2.2), que es la única del sistema.

**Fuera**: guardar simulaciones (SPEC-03), alta de clientes (SPEC-01, que
usa esa constante), conversión de divisa (SPEC-04).

## 2. Reglas de negocio

### 2.1 Tarifa

| Tramo | Usuarios | Precio por usuario |
|---|---|---|
| 1 | del 1 al 10 | 10,00 € (`1000`) |
| 2 | del 11 al 50 | 8,00 € (`800`) |
| 3 | del 51 en adelante | 5,00 € (`500`) |

La tarifa es **acumulativa**: cada usuario se cobra al precio del tramo en el
que cae, no todos al precio del último tramo alcanzado.

```
base(n) = 1000 · min(n, 10)
        +  800 · min(max(n − 10, 0), 40)
        +  500 · max(n − 50, 0)                     (céntimos)
```

### 2.2 Impuesto y total

```
impuesto = redondeo(base · tipo_bp / 10000)
total    = base + impuesto
```

- El tipo es el del país del cliente, en puntos básicos, tomado de la
  **constante de países** del dominio:

| Código | Nombre | Tipo (bp) |
|---|---|---|
| `ES` | España | 2100 |
| `PT` | Portugal | 2300 |
| `FR` | Francia | 2000 |
| `DE` | Alemania | 1900 |
| `IT` | Italia | 2200 |
| `NL` | Países Bajos | 2100 |
| `IE` | Irlanda | 2300 |
| `BE` | Bélgica | 2100 |
| `GB` | Reino Unido | 2000 |

  Es la **única** lista de países del sistema: cada entrada lleva el
  código, el nombre y el tipo. Los valores son los de A4, decidido sin
  confirmación externa el 2026-11-13. Esta spec es la dueña de los tipos;
  SPEC-01 usa la misma constante para validar el país del alta y para
  `GET /meta`, y no mantiene una lista aparte.
- El impuesto se calcula **una vez, sobre el coste base total**, no tramo a
  tramo.
- `redondeo` es al céntimo más próximo, con el medio céntimo hacia arriba. En
  enteros: `(base · tipo_bp + 5000) // 10000`.

Con precios en euros enteros y tipos en porcentajes enteros, como los
actuales, `base · tipo_bp` es siempre múltiplo de 10000 y el redondeo no
llega a actuar. La regla cubre tarifas o tipos futuros con decimales.

### 2.3 Dónde vive

La tarifa y los tipos impositivos son datos constantes del dominio
(`backend/app/domain/`), no filas de la base de datos. El cálculo es una
función pura: mismos datos de entrada, mismo resultado, sin entrada/salida.
`POST /pricing/quote` y `POST /simulations` llaman a esa misma función (A9).

## 3. Requisitos (EARS)

### Cálculo

| Id | Requisito | Cubre |
|---|---|---|
| E-01 | El sistema deberá calcular el coste base mensual como la suma, tramo a tramo, del número de usuarios que caen en cada tramo por el precio de ese tramo. | R-06 |
| E-02 | Cuando el número de usuarios es 0, el sistema deberá devolver un coste base, un impuesto y un total de 0. | R-06, A7 |
| E-03 | El sistema deberá calcular el impuesto aplicando al coste base total el tipo del país del cliente, redondeado al céntimo más próximo con el medio céntimo hacia arriba. | R-07, A6 |
| E-04 | El sistema deberá calcular el total como la suma del coste base y el impuesto. | R-07 |
| E-05 | El sistema deberá expresar todos los importes como enteros en céntimos de euro y no usar aritmética de coma flotante en ningún paso del cálculo. | A6 |
| E-06 | El sistema deberá devolver, junto con los importes, el desglose de los tres tramos (usuarios y subtotal de cada uno, también cuando son 0) y el tipo impositivo aplicado. | R-12 |
| E-07 | El sistema deberá obtener el tipo impositivo únicamente del país del cliente guardado; la petición no puede aportar ni el tipo ni ningún importe. | R-07 |
| E-08 | El sistema deberá usar la misma función de cálculo para la proyección sin guardar y para la simulación guardada. | A9 |

### Validación de la entrada

| Id | Requisito | Cubre |
|---|---|---|
| E-09 | Si el número de usuarios no es un número entero, es negativo o supera 100.000, entonces el sistema deberá rechazar la petición sin calcular nada. | A7 |
| E-10 | Si el país del cliente no tiene un tipo impositivo definido, entonces el sistema deberá responder `500` con el código `tax_rate_not_defined`, sin trazas ni detalles internos, en lugar de aplicar un 0 %. | A4 |
| E-15 | Si `customer_id` no es un número entero de 1 a 9223372036854775807, entonces el sistema deberá rechazar la petición sin consultar la base de datos. | A14 |

E-10 describe un fallo interno, no un error de quien llama: SPEC-01 solo
admitirá en el alta países de la tabla de A4, así que un cliente guardado con
un país sin tipo indica datos incoherentes. Por eso es un `500` y no un `4xx`.

### `POST /pricing/quote`

| Id | Requisito | Cubre |
|---|---|---|
| E-11 | Cuando recibe una petición válida, el sistema deberá responder `200` con el cálculo completo. | R-12, A9 |
| E-12 | El sistema deberá atender `POST /pricing/quote` sin crear ni modificar ningún dato guardado. | A9 |
| E-13 | Si el cliente indicado no existe, entonces el sistema deberá responder `404` con el código `customer_not_found`. | — |
| E-14 | Si la petición no supera la validación (E-09, E-15, campo ausente, tipo incorrecto o campo desconocido), entonces el sistema deberá responder `422` con el código `validation_error` y el detalle de cada campo. | A14 |

## 4. Contrato de `POST /pricing/quote`

### Petición

| Campo | Tipo | Obligatorio | Regla |
|---|---|---|---|
| `customer_id` | entero | sí | De 1 a 9223372036854775807, y de un cliente existente |
| `active_users` | entero | sí | De 0 a 100.000 |

En los dos campos se acepta solo un número JSON entero. Se rechazan cadenas (`"15"`),
booleanos, `null` y números con parte decimal, incluido `15.0`.

```json
{ "customer_id": 1, "active_users": 15 }
```

### Respuesta `200`

```json
{
  "currency": "EUR",
  "active_users": 15,
  "tiers": [
    { "from_users": 1,  "to_users": 10,   "unit_price_cents": 1000, "users": 10, "subtotal_cents": 10000 },
    { "from_users": 11, "to_users": 50,   "unit_price_cents": 800,  "users": 5,  "subtotal_cents": 4000 },
    { "from_users": 51, "to_users": null, "unit_price_cents": 500,  "users": 0,  "subtotal_cents": 0 }
  ],
  "base_cents": 14000,
  "country": "ES",
  "tax_rate_bp": 2100,
  "tax_cents": 2940,
  "total_cents": 16940
}
```

`tiers` lleva siempre los tres tramos, en orden. `to_users` es `null` en el
último, que no tiene límite superior.

### Errores

| Estado | `code` | Cuándo | Códigos por campo |
|---|---|---|---|
| `404` | `customer_not_found` | No existe un cliente con ese `customer_id` | — |
| `422` | `validation_error` | La petición no es válida | `missing`, `not_an_integer`, `out_of_range`, `unknown_field` |
| `500` | `tax_rate_not_defined` | El país del cliente guardado no tiene tipo impositivo (fallo interno, E-10) | — |

Si la petición tiene a la vez un error de validación y un cliente
inexistente, gana la validación (`422`): no se consulta la base de datos con
una petición mal formada.

## 5. Casos de prueba

### 5.1 Coste base y total con el tipo de España (21 %)

Importes en céntimos. Cada fila es un caso de test.

| Usuarios | Por qué este caso | Tramo 1 | Tramo 2 | Tramo 3 | Base | Impuesto | Total |
|---|---|---|---|---|---|---|---|
| 0 | Mínimo: sin usuarios | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | Primer usuario | 1000 | 0 | 0 | 1000 | 210 | 1210 |
| 10 | Último del tramo 1 | 10000 | 0 | 0 | 10000 | 2100 | 12100 |
| 11 | Primero del tramo 2 | 10000 | 800 | 0 | 10800 | 2268 | 13068 |
| 15 | Ejemplo del encargo: 140 € | 10000 | 4000 | 0 | 14000 | 2940 | 16940 |
| 50 | Último del tramo 2 | 10000 | 32000 | 0 | 42000 | 8820 | 50820 |
| 51 | Primero del tramo 3 | 10000 | 32000 | 500 | 42500 | 8925 | 51425 |
| 100 | Tramo 3 con varios usuarios | 10000 | 32000 | 25000 | 67000 | 14070 | 81070 |
| 20000 | Por encima del máximo del control deslizante de la interfaz (SPEC-04, 5.5) | 10000 | 32000 | 9975000 | 10017000 | 2103570 | 12120570 |
| 100000 | Máximo admitido | 10000 | 32000 | 49975000 | 50017000 | 10503570 | 60520570 |

### 5.2 Mismo coste base, distinto país (15 usuarios, base 14000)

| País | Tipo (bp) | Impuesto | Total |
|---|---|---|---|
| DE | 1900 | 2660 | 16660 |
| FR, GB | 2000 | 2800 | 16800 |
| ES, NL, BE | 2100 | 2940 | 16940 |
| IT | 2200 | 3080 | 17080 |
| PT, IE | 2300 | 3220 | 17220 |

Los tipos son los de A4, decidido sin confirmación externa el 2026-11-13.
Si la tabla cambia, cambian estas filas.

### 5.3 Redondeo (casos sintéticos sobre la función del impuesto)

Ninguna combinación real de tarifa y tipo produce fracciones de céntimo, así
que el redondeo se prueba directamente con bases y tipos inventados.

| Base | Tipo (bp) | Valor exacto | Impuesto | Qué demuestra |
|---|---|---|---|---|
| 14000 | 0 | 0 | 0 | Tipo del 0 % |
| 0 | 2100 | 0 | 0 | Base 0 |
| 10 | 2100 | 2,1 | 2 | Por debajo de medio: hacia abajo |
| 49 | 100 | 0,49 | 0 | Justo por debajo de medio |
| 50 | 100 | 0,5 | 1 | Medio exacto: hacia arriba |
| 250 | 100 | 2,5 | 3 | Medio exacto con parte entera par: 3 y no 2, descarta el redondeo «al par» |
| 999 | 2150 | 214,785 | 215 | Por encima de medio, con un tipo con decimales |
| 1005 | 2100 | 211,05 | 211 | Fracción pequeña con un tipo real |

### 5.4 Entradas no válidas de `active_users`

| Valor | Resultado | Código por campo |
|---|---|---|
| `-1` | `422` | `out_of_range` |
| `100001` | `422` | `out_of_range` |
| `15.5` | `422` | `not_an_integer` |
| `15.0` | `422` | `not_an_integer` |
| `"15"` | `422` | `not_an_integer` |
| `true` | `422` | `not_an_integer` |
| `null` | `422` | `not_an_integer` |
| campo ausente | `422` | `missing` |
| campo adicional `tax_rate_bp` | `422` | `unknown_field` |

### 5.5 Valores de `customer_id`

Con `active_users` válido salvo que se indique.

| Valor | Resultado | Código por campo |
|---|---|---|
| `1` (existe) | `200` | — |
| `999` (no existe) | `404` `customer_not_found` | — |
| `9223372036854775807` (no existe) | `404` `customer_not_found` | — |
| `0` | `422` | `out_of_range` |
| `-1` | `422` | `out_of_range` |
| `9223372036854775808` (2^63) | `422` | `out_of_range` |
| `1.0`, `"1"`, `true`, `null` | `422` | `not_an_integer` |
| campo ausente | `422` | `missing` |
| `999` y `active_users` = `-1` | `422` | `out_of_range` en `active_users`: gana la validación |

## 6. Criterios de aceptación

| Id | Criterio | Requisitos |
|---|---|---|
| CA-01 | Un test unitario parametrizado del dominio reproduce cada fila de 5.1, comprobando el subtotal de cada tramo, la base, el impuesto y el total. | E-01, E-02, E-04, E-06 |
| CA-02 | Un test unitario parametrizado reproduce cada fila de 5.2 y de 5.3. | E-03 |
| CA-03 | Un test recorre todos los valores de 0 a 1000 usuarios y comprueba que `base(n+1) − base(n)` es exactamente el precio del tramo del usuario `n+1`. | E-01 |
| CA-04 | Las funciones del dominio rechazan con un error propio un número de usuarios fuera de rango y un país sin tipo definido. | E-09, E-10 |
| CA-05 | Un test de integración llama a `POST /pricing/quote` con un cliente de España y 15 usuarios, y obtiene exactamente la respuesta del apartado 4. | E-07, E-11 |
| CA-06 | Un test de integración comprueba que, tras varias llamadas a `POST /pricing/quote`, el número de simulaciones guardadas no ha cambiado. | E-12 |
| CA-07 | Tests de integración cubren cada fila de 5.4 y de 5.5, comprobando el estado, el `code` y el código por campo, no el texto. | E-13, E-14, E-15 |
| CA-08 | Para una misma entrada, los importes de `POST /pricing/quote` y los de la simulación guardada por `POST /simulations` son idénticos. Lo comprueba SPEC-03/CA-03. | E-08 |
| CA-09 | El oráculo comprueba de forma automática que `domain/` no importa nada ajeno a la biblioteca estándar, no usa `float` (ni el tipo, ni literales con decimales, ni la división `/`) y tiene el 100 % de ramas cubiertas. | E-05 |
| CA-10 | El OpenAPI generado declara para `POST /pricing/quote` los campos, tipos y códigos de estado del apartado 4. | E-11, E-13, E-14 |
| CA-11 | Un test de integración guarda directamente en la base de datos un cliente con un país sin tipo impositivo, llama a `POST /pricing/quote` y obtiene un `500` en `application/problem+json` con el código `tax_rate_not_defined`, cuyo cuerpo no contiene trazas ni nombres internos. | E-10 |

**Sobre CA-09**: la comprobación la hace `scripts/check.py`, que existe
desde el 2026-11-12. Recorre el árbol sintáctico (AST) de los módulos de
`domain/` y exige el 100 % de sentencias y ramas de `domain/` con
`coverage report --include=app/domain/* --fail-under=100`. Mientras
`domain/` no tenga código, pasa sin nada que medir: el criterio **no puede
darse por cumplido** hasta que exista el cálculo.

## 7. Decisiones de diseño

Aprobadas por el Tech Lead el 2026-11-12.

1. **La proyección se pide por `customer_id`, no por país.** Así el tipo
   impositivo sale siempre del cliente guardado y la petición es igual a la
   de `POST /simulations`. A cambio, no se puede proyectar sin un cliente
   dado de alta.
2. **El máximo de usuarios es 100.000** (A7).
3. **`15.0` se rechaza.** Un número con parte decimal no es un entero aunque
   la parte decimal sea cero; aceptar unos decimales y otros no es más
   difícil de explicar que rechazarlos todos.
4. **`tiers` devuelve siempre los tres tramos**, también los vacíos, para que
   la respuesta tenga siempre la misma forma.
5. **Si la petición es inválida y además el cliente no existe, gana el
   `422`.**
6. **Almacenamiento y llamadas a la API no entran en la petición** porque no
   tienen precio (A3). Si la respuesta a la consulta, que sigue abierta,
   dijera que sí lo tienen, esta spec se amplía con un cambio anotado en su
   historial.

## 8. Pendiente antes de aprobar

**Nada pendiente desde el 2026-11-13.** La fecha límite (viernes 13 de
noviembre de 2026, 10:00) se cumplió sin respuesta y el Tech Lead decidió
A2, A3, A4 y A5 con la hipótesis ya documentada: están en
`decidido (sin confirmación externa)`. La consulta sigue abierta: si la
respuesta llega, se aplica como cambio de esta spec, con fecha y motivo en
su historial.

| Supuesto | Qué cambiaría en esta spec si la respuesta lo contradijera |
|---|---|
| A2 · plan | Si el plan afectara al precio, habría una segunda dimensión en la tarifa |
| A3 · almacenamiento y API | Si tuvieran precio, entrarían en la petición y en el coste base |
| A4 · países y tipos | La constante de países de 2.2 y la tabla de 5.2 |
| A5 · IVA entre empresas | Si hubiera que modelarlo, el tipo dejaría de depender solo del país. Hoy se aplica siempre el tipo del país del cliente; la inversión del sujeto pasivo no se modela y es una simplificación conocida |

## Historial

| Fecha | Cambio |
|---|---|
| 2026-11-12 | Primer borrador |
| 2026-11-12 | Revisión del Tech Lead: aprobadas las decisiones de diseño y A7; E-10 responde `500` con `tax_rate_not_defined` (nueva fila de errores y CA-11); CA-09 pasa a comprobarse de forma automática; añadidos A2 a los supuestos y la fecha límite de los pendientes |
| 2026-11-12 | Correcciones de la evaluación independiente (`04-calidad/evaluacion-specs-01.md`), decididas por el Tech Lead: A13 y A14 en la cabecera (H-02); `customer_id` de 1 a 9223372036854775807, con E-15 y la tabla 5.5 (H-04); la constante única de países, con su tabla en 2.2 (H-12); CA-08 remite a SPEC-03/CA-03 (H-01) |
| 2026-11-12 | Correcciones de la segunda evaluación independiente (`04-calidad/evaluacion-specs-02.md`), decididas por el Tech Lead: aprobación en bloque con SPEC-01 y SPEC-03 (N-01); la lista de países deja de figurar como ajena a esta spec en el apartado 1 (N-02, resto de H-12); fila de 20000 usuarios en 5.1 (N-08) |
| 2026-11-13 | Decisión del Tech Lead al vencer la fecha límite sin respuesta externa: A2, A3, A4 y A5 pasan a `decidido (sin confirmación externa)` con la hipótesis ya documentada, sin cambios en las reglas; cabecera, 2.2, 5.2, decisión 6 del apartado 7 y apartado 8 actualizados. La consulta sigue abierta: si la respuesta llega, se aplica como cambio de esta spec |
| 2026-11-13 | Aprobación del Tech Lead: el estado pasa a `aprobada` (2026-11-13), a la vez que SPEC-01 y SPEC-03 (bloque backend) |
| 2026-11-13 | Corrección ordenada por el Tech Lead: la nota «Sobre CA-09» decía que `scripts/check.py` aún no existía. Existe desde el 2026-11-12; la nota dice ahora qué comprueba y que el criterio no se da por cumplido mientras `domain/` no tenga código. Motivo: la nota había quedado desfasada. Sin cambios en requisitos, criterios ni casos |
