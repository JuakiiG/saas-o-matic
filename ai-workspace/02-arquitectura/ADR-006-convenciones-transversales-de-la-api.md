# ADR-006 · Convenciones transversales de la API

| | |
|---|---|
| **Estado** | `aceptado` (2026-11-12) |
| **Decide** | Tech Lead |
| **Requisitos** | R-03, R-05, R-07, R-10, R-11 |
| **Supuestos** | A4, A6, A13, A14 |
| **Specs** | Las cuatro. El detalle normativo está en el índice de specs («Convenciones comunes de la API»), SPEC-01 (2.12, 4.2), SPEC-02 (2.2) y SPEC-03 (2.4, 2.7, D-01) |
| **Relacionado** | ADR-001 (FastAPI y SQLite) · ADR-004 (persistencia) |

## Contexto

Cinco decisiones afectan a más de una spec y se tomaron en las propias
specs o al responder a las evaluaciones independientes, sin un ADR. El
criterio del índice de arquitectura pide uno para toda decisión que afecte
a la arquitectura o a más de una spec. Este ADR las reúne, con sus
alternativas y su motivo.

No repite las reglas: **las specs siguen siendo la fuente normativa**. Aquí
queda el porqué.

Queda fuera el bloque de aprobación de las specs del backend: es proceso,
no arquitectura, y vive en el índice de specs. También la representación
del dinero (céntimos enteros y puntos básicos), que es el supuesto A6 y una
regla de `CLAUDE.md`.

## 1. Formato de los errores

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **`application/problem+json` (RFC 9457) con un `code` estable en inglés**, un `detail` en español y, en los errores de validación, una lista `errors` con `field`, `code` y `message` | Es un estándar; un solo formato para todos los errores; el frontend decide por el código y el texto puede cambiar | Hay que sustituir el formato de error por defecto del framework, también en los errores que el framework genera solo (`404`, `405`, `422`) |
| B | El formato de error por defecto del framework | Ningún código que escribir | No lleva código estable; su forma depende de la versión del framework; los errores de validación exponen detalles internos del validador |
| C | Un sobre propio (`{"error": {...}}`) | Libertad total | Inventa lo que ya resuelve un estándar |

**Decisión: opción A**, con estas reglas (índice de specs y SPEC-01, 2.12):

- Un solo error por campo, el primero que falle, y `errors` en el orden de
  los campos del contrato.
- Los errores genéricos tienen también su `code`: `malformed_request`
  (`400`), `unsupported_media_type` (`415`), `not_found` (`404`),
  `method_not_allowed` (`405`), `validation_error` con `unknown_field`
  (`422`) e `internal_error` (`500`), sin trazas. Si coinciden varios, la
  precedencia es `415`, `400`, `422`.
- Una petición con un campo o un parámetro no documentado se rechaza.
- **Única excepción**: la respuesta con que el middleware de CORS rechaza
  una comprobación previa, que es la estándar del framework.

*Por qué*: el frontend tiene que tratar cada error sin depender del texto
(`CLAUDE.md`), y los errores que nadie especifica acaban inventándose al
implementar; fue el hallazgo H-03 de la primera evaluación. La excepción de
CORS existe porque esa respuesta la consume el navegador, no el frontend, y
no justifica código a medida.

## 2. Identificadores

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **Entero de 1 a 9223372036854775807**, asignado por SQLite; fuera de rango, `422` `out_of_range` | Es la clave natural de SQLite; ordena por inserción, que es lo que usa el historial; corto en las rutas | Enumerable: se puede adivinar el identificador de otro cliente. Por encima de 2^53 no cabe exacto en un `number` de JavaScript |
| B | UUID | No enumerable | Sin orden de inserción; más largo; SQLite no lo genera solo |
| C | Entero sin límite declarado | Nada que especificar | Un valor mayor que el máximo de SQLite provocaría un error interno en lugar de un `422` |

**Decisión: opción A.** *Por qué*: sin autenticación (A16) y en una
herramienta interna, que un identificador sea enumerable no expone nada que
no sea ya accesible. El máximo es el de `INTEGER` en SQLite, y declararlo
convierte un posible `500` en un `422` (hallazgo H-04). El límite de 2^53
de JavaScript se acepta: es inalcanzable con el uso previsto.

## 3. Fechas con hora

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **UTC, ISO 8601, precisión de segundos** (`2026-11-12T14:30:00Z`), en la API y en la base de datos | Sin ambigüedad de zona; legible; se compara igual como texto que como fecha; SQLite lo guarda en `TEXT` | El frontend tiene que convertir a la zona del navegador para mostrar |
| B | Hora local con desfase | Se lee tal cual | Dos formas de escribir el mismo instante; el desfase del servidor no significa nada para quien lo lee |
| C | Marca de tiempo numérica | Compacta | Ilegible en la base de datos y en las respuestas |
| D | Precisión de milisegundos | Más resolución | Ninguna regla la necesita, y dos representaciones con distinta precisión acaban sin compararse bien |

**Decisión: opción A.** *Por qué*: la fecha solo se muestra. El orden del
historial no depende de ella: va por `id`, que refleja el orden real de
inserción aunque el reloj cambie (SPEC-03, 2.4). La fecha del tipo de
cambio es otra cosa, una fecha sin hora que viene de un tercero, y no sigue
esta regla (SPEC-04, 2.6).

## 4. Constante única de países

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **Una sola constante en el dominio**, con el código, el nombre y el tipo impositivo de cada país. La define SPEC-02; SPEC-01 la usa para validar el alta y para `GET /meta` | Un país admitido en el alta tiene siempre tipo impositivo; un solo sitio que cambiar | SPEC-01 depende de SPEC-02 |
| B | Dos listas: países admitidos en SPEC-01 y tipos en SPEC-02 | Cada spec es dueña de lo suyo | Pueden divergir: un país admitido sin tipo es un `500` al calcular |
| C | Una tabla en la base de datos | Editable sin desplegar | Es una regla de negocio fuera del dominio; nadie ha pedido editarla; habría que sembrarla |

**Decisión: opción A.** *Por qué*: el error que se quiere hacer imposible
es un cliente guardado con un país sin tipo impositivo. Con una sola
constante solo puede ocurrir manipulando la base de datos, y aun así está
previsto (SPEC-02, E-10). La dependencia de SPEC-01 respecto de SPEC-02 es
una de las razones por las que las specs del backend se aprueban en bloque.

## 5. El historial va dentro de la ficha del cliente

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **`GET /customers/{id}` devuelve los datos del cliente, `simulation_count` y `simulations`** (las 50 de `id` más alto) | Es lo que dice A13; la vista de detalle hace una sola petición y tiene un solo estado de carga y de error | El contrato de la ficha, que es de SPEC-01, lo completa SPEC-03; la respuesta es mayor |
| B | Un endpoint aparte, `GET /customers/{id}/simulations` | Respuestas más pequeñas; cada spec con su endpoint | Un endpoint que A13 no recoge; dos peticiones y dos estados para una sola vista |
| C | Historial sin límite | Más simple | Una respuesta que crece sin tope, lo que A13 evitó en el buscador |

**Decisión: opción A**, con el límite de 50 y el total aparte (SPEC-03,
D-01 y D-05). *Por qué*: el supuesto A13 ya describía la ficha «con su
historial», y la vista que la consume es una sola. El coste es que una
misma respuesta se define entre dos specs; se trata diciendo en SPEC-01
(4.2) dónde está cada parte y aprobando las dos specs a la vez.

## Consecuencias

A favor:

- El frontend trata todos los errores del backend con el mismo código.
- Las reglas que valen para todos los endpoints están escritas una vez, en
  el índice de specs, y probadas una vez (SPEC-03, 5.7).

En contra, y cómo se trata:

| Consecuencia | Tratamiento |
|---|---|
| Hay que sustituir los errores por defecto del framework | Un único punto de traducción en la capa `api/` (`.claude/rules/backend.md`) y un test por cada error genérico (SPEC-03, CA-17) |
| SPEC-01 depende de SPEC-02 y de SPEC-03 | Las tres se aprueban en bloque y se implementan en un orden fijado (índice de specs) |
| Identificadores enumerables | Aceptado mientras no haya autenticación (A16) |
| Las convenciones viven en el índice y su motivo aquí | El índice enlaza a este ADR |

## No verificado

- Que el framework permita, sin más código que ese punto de traducción,
  todos los estados y códigos de los errores genéricos, la precedencia
  `415` > `400` > `422` y las cabeceras CORS en un `500`.
- El estado y las cabeceras exactos con que el middleware de CORS rechaza
  una comprobación previa. Los fija un test al implementar.

## Cuándo habría que revisarla

- Si se añadiera autenticación o la herramienta dejara de ser interna: los
  identificadores enumerables (punto 2).
- Si la lista de países tuviera que cambiar sin desplegar: la opción C del
  punto 4.
- Si el historial creciera hasta necesitar paginación: la opción B del
  punto 5.
