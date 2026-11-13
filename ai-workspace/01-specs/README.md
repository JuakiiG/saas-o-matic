# Especificaciones

Cada spec define qué debe hacer una parte del sistema antes de escribir su
código. No se programa una parte hasta que su spec está `aprobada`.

## Índice

| Spec | Ámbito | Requisitos | Supuestos de los que depende | Estado |
|---|---|---|---|---|
| [SPEC-01](SPEC-01-clientes-y-validacion-fiscal.md) | Clientes y validación fiscal | R-03, R-04, R-10, R-11 | A2, A4, A10, A11, A12, A13, A14, A18 | `aprobada` (2026-11-13) |
| [SPEC-02](SPEC-02-tarificacion-e-impuestos.md) | Tarificación e impuestos | R-06, R-07, R-12 | A2, A3, A4, A5, A6, A7, A9, A13, A14 | `aprobada` (2026-11-13) |
| [SPEC-03](SPEC-03-simulaciones-y-persistencia.md) | Simulaciones y persistencia | R-05, R-11 | A3, A4, A6, A7, A9, A13, A14, A16, A18 | `aprobada` (2026-11-13) |
| [SPEC-04](SPEC-04-frontend-y-divisas.md) | Frontend y divisas | R-09 a R-12, R-17 | A3, A6, A7, A8, A9, A12, A13, A14, A16, A17 | `borrador` (2026-11-12) |

Una spec no puede pasar a `aprobada` mientras dependa de un supuesto que no
esté `decidido` (ver [`supuestos.md`](../00-analisis/supuestos.md)).

**Supuestos consultados (A2 a A5)**: la fecha límite, el viernes 13 de
noviembre de 2026 a las 10:00, se cumplió sin respuesta, y ese día el Tech
Lead los decidió con la hipótesis ya documentada. *Por qué: una consulta sin
contestar no puede bloquear el desarrollo de forma indefinida.* La respuesta
llegó ese mismo día, más tarde: confirma A2, A3 y A5 y, de A4, solo el uso
del tipo general (la lista de países es decisión propia). **No cambia
ninguna regla y la consulta está cerrada.** El detalle está en
[`supuestos.md`](../00-analisis/supuestos.md).

## Bloques de aprobación y orden de implementación

Las specs se aprueban en dos bloques, decididos por el Tech Lead el
2026-11-12:

| Bloque | Specs | Cuándo se aprueba |
|---|---|---|
| **Backend** | SPEC-01, SPEC-02 y SPEC-03 | Las tres **a la vez**, antes de escribir código del backend. **Aprobado el 2026-11-13** |
| **Frontend** | SPEC-04 | Aparte, después del bloque backend y antes de empezar el frontend |

*Por qué un bloque*: las tres specs del backend se necesitan entre sí.
SPEC-01 usa la constante de países de SPEC-02 y devuelve en la ficha el
historial que define SPEC-03; SPEC-03 guarda el cálculo de SPEC-02 para un
cliente de SPEC-01, y contiene los requisitos de los errores genéricos, de
CORS y del esquema que usan todos los endpoints. Aprobarlas una a una
obligaría a implementar una spec a medias o a escribir código de otra sin
aprobar.

**Orden de implementación del bloque backend**:

1. **Lo común**: errores genéricos (convenciones de este índice y
   SPEC-03/E-29), CORS (SPEC-03/E-24 a E-26, E-30 y E-31), `GET /health`
   (SPEC-03/E-27 y E-28) y el esquema de la base de datos (SPEC-03, 2.6).
2. **SPEC-02**: tarifa, impuesto y `POST /pricing/quote`.
3. **SPEC-01**: clientes y validación fiscal.
4. **SPEC-03**: simulaciones e historial.

## Ciclo de vida

| Estado | Significado |
|---|---|
| `borrador` | Redactada por la IA; se puede discutir y cambiar. No autoriza a programar |
| `aprobada` (fecha) | Firmada por el Tech Lead. Autoriza a programar esa parte |

Un cambio en una spec aprobada se anota en su historial, con fecha y motivo,
y vuelve a pasar por aprobación.

## Formato de los requisitos (EARS)

Cada requisito es una sola frase comprobable, con identificador propio
(`SPEC-02/E-03`), y sigue uno de estos patrones:

| Patrón | Forma |
|---|---|
| Ubicuo | «El sistema deberá…» |
| Por evento | «Cuando *ocurre algo*, el sistema deberá…» |
| Por estado | «Mientras *se da una condición*, el sistema deberá…» |
| Comportamiento no deseado | «Si *ocurre algo indebido*, entonces el sistema deberá…» |

Los criterios de aceptación (`CA-xx`) dicen cómo se demuestra que los
requisitos se cumplen. Cada test cita el requisito que comprueba.

## Convenciones comunes de la API

Valen para todas las specs, que solo detallan lo que les es propio. Las
alternativas y el motivo de cada una están en
[ADR-006](../02-arquitectura/ADR-006-convenciones-transversales-de-la-api.md).

- **Formato**: JSON, con nombres de campo en inglés y `snake_case`.
- **Dinero**: enteros en céntimos de euro, en campos acabados en `_cents`.
  Nunca decimales (A6).
- **Tipos impositivos**: enteros en puntos básicos, en campos acabados en
  `_bp` (21 % = `2100`).
- **Campos desconocidos**: una petición con un campo no documentado se
  rechaza; no se ignora en silencio.
- **Identificadores**: todo `id`, vaya en la ruta o en el cuerpo, es un
  entero de 1 a 9223372036854775807, el máximo de `INTEGER` en SQLite. Fuera
  de ese rango, `422` con el código de campo `out_of_range`; si no es un
  entero, `not_an_integer`. **En la ruta, un `id` tiene una sola forma**: es
  un entero si es `0` o un signo menos opcional seguido de dígitos ASCII
  (`0` a `9`) sin ceros a la izquierda. Todo lo demás es `not_an_integer`:
  `1.0`, `+1`, `01`, `1_0` o un espacio delante o detrás. Después se aplica
  el rango: `0` y los negativos dan `out_of_range`. *Por qué: un cliente,
  una dirección.*
- **Fechas con hora**: UTC, ISO 8601 y precisión de segundos
  (`2026-11-12T14:30:00Z`).
- **Errores**: `application/problem+json` (RFC 9457) con esta forma (A14):

  ```json
  {
    "type": "about:blank",
    "title": "Unprocessable Content",
    "status": 422,
    "code": "validation_error",
    "detail": "La petición contiene datos no válidos.",
    "errors": [
      {
        "field": "active_users",
        "code": "out_of_range",
        "message": "Debe estar entre 0 y 100000."
      }
    ]
  }
  ```

  `code` es estable y forma parte del contrato; `detail` y `message` son
  texto en español para mostrar y pueden cambiar. `errors` solo aparece en
  los errores de validación.

- **Errores de validación**: un solo error por campo, el primero que falle,
  y `errors` en el orden de los campos del contrato. `field` es el nombre
  del campo del cuerpo, `id` para el identificador de la ruta y el nombre
  del parámetro para los de consulta. Además:
  - Los campos del cuerpo que no están en el contrato (`unknown_field`) van
    **después** de los del contrato, por orden alfabético de su nombre
    (SPEC-01, 2.12), comparando por punto de código: las mayúsculas van
    antes que las minúsculas. Los parámetros de consulta no documentados
    van en el orden en que llegan en la petición.
  - Un **cuerpo ausente equivale a `{}`**: un `missing` por cada campo
    obligatorio.
  - Una validación que falla **sin tener un código en el contrato** es un
    fallo nuestro: `500` `internal_error`, registrado. Nunca se responde
    con el formato de error del framework ni con un código que no esté en
    la spec.
- **Errores genéricos**: valen para todos los endpoints, van en
  `application/problem+json` y cada uno tiene su `code` estable:

  | Situación | Estado | `code` |
  |---|---|---|
  | El cuerpo no es JSON válido o no es un objeto JSON (una lista, `null`, un número) | `400` | `malformed_request` |
  | La petición lleva cuerpo y su `Content-Type` no es `application/json`. Con parámetros, como `application/json; charset=utf-8`, es válido | `415` | `unsupported_media_type` |
  | La ruta no existe | `404` | `not_found` |
  | La ruta existe pero no admite ese método (salvo `OPTIONS`, ver más abajo) | `405` | `method_not_allowed` |
  | La petición trae un parámetro de consulta no documentado | `422` | `validation_error`, con el código de campo `unknown_field` |
  | Error inesperado | `500` | `internal_error`, sin trazas ni detalles internos |
  | La base de datos no puede abrirse o consultarse | `503` | `service_unavailable`, sin trazas ni detalles internos |

  El `503` vale para **cualquier endpoint** que lea o escriba en la base de
  datos, igual que para `GET /health` (SPEC-03, E-28). Solo cubre el fallo
  de conexión o de consulta: un error de integridad (una clave repetida,
  una referencia rota) no es un `503`. La validación va antes: una petición
  no válida responde `422` sin consultar la base de datos. *Por qué: el
  `500` dice «fallo nuestro» y el `503` «no disponible ahora», y el
  frontend los trata distinto.*

  `not_found` es el de una ruta inexistente; un recurso que no existe en una
  ruta válida tiene su propio código (`customer_not_found`). El requisito y
  los casos de prueba de estos errores están en SPEC-03, «Operación del
  backend».

  **Precedencia**: si una misma petición incurre en varios, se responde
  solo con uno, en este orden: `415`, después `400` y después `422`. Así,
  un cuerpo con un `Content-Type` no admitido da `415` aunque además esté
  mal formado, y un cuerpo mal formado da `400` aunque la petición traiga
  también un parámetro de consulta desconocido.

- **Excepción a `application/problem+json`: la comprobación previa de
  CORS.** El `OPTIONS` que el navegador envía antes de un `POST` lo atiende
  el middleware de CORS y queda fuera de la regla del `405`: si la admite
  responde `200` con sus cabeceras CORS, y si la rechaza responde con su
  respuesta estándar, sin el cuerpo de error de la API y, cuando el origen
  no está admitido, sin `access-control-allow-origin`. *Por qué*: esa
  respuesta la consume el navegador, no el frontend. Un `OPTIONS` que no
  es una comprobación previa responde `405`, como cualquier otro método no
  admitido. El detalle está en SPEC-03 (2.7).

## Historial de las convenciones

Cambios de las convenciones comunes desde que el bloque backend tiene el
visto bueno del Tech Lead (2026-11-13). Los anteriores están en el historial
de cada spec.

| Fecha | Cambio |
|---|---|
| 2026-11-13 | Decisión del Tech Lead al revisar SPEC-02: cualquier endpoint que no pueda abrir o consultar la base de datos responde `503` `service_unavailable`, igual que `GET /health`; no vale para un error de integridad. Fila nueva en la tabla de errores genéricos. Motivo: hasta ahora una petición válida a `POST /pricing/quote` con la base de datos inaccesible respondía `500` `internal_error`, y el frontend trata distinto «fallo nuestro» y «no disponible ahora». El porqué, en ADR-006 |
| 2026-11-13 | Decisión del Tech Lead al revisar SPEC-02: tres reglas que la IA había aplicado al implementar y que ninguna spec decía pasan a estar escritas en «Errores de validación»: el cuerpo ausente equivale a `{}`; una validación sin código en el contrato es un `500` registrado; los campos desconocidos van después de los del contrato, en el orden de la petición. Motivo: una regla que solo está en el código no es parte del contrato |
| 2026-11-13 | Corrección decidida por el Tech Lead: los campos desconocidos del cuerpo van por **orden alfabético** de su nombre, no por el orden de la petición. Motivo: la regla escrita ese mismo día contradecía SPEC-01 (2.12), que ya decía «por orden alfabético»; la IA la había propuesto sin haber leído ese apartado. Los parámetros de consulta no documentados siguen en el orden de la petición |
| 2026-11-13 | Decisión del Tech Lead al revisar SPEC-01: en la ruta, un `id` tiene una sola forma (`0`, o un signo menos opcional y dígitos ASCII sin ceros a la izquierda); todo lo demás es `not_an_integer`, y el rango se aplica después. Regla nueva en «Identificadores». Motivo: un cliente, una dirección; hasta ahora `1.0`, `+1` y `01` devolvían el cliente 1 y `1_0` se leía como 10, porque lo decidía la biblioteca de validación |
