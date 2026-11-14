# Sesión 06 · SPEC-04 al día con el contrato final del backend

| | |
|---|---|
| **Fecha** | 2026-11-14 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | *(sesión en curso; esta fila se escribe al cerrar)* |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 06: poner SPEC-04 al día con el contrato final del backend, antes
> de aprobarla. En este paso no se escribe código de frontend. Leer antes
> `CLAUDE.md`, `.claude/rules/frontend.md`, el índice de specs, SPEC-04
> entera, el apartado 4 de SPEC-01, SPEC-02 y SPEC-03,
> `04-calidad/limitaciones-conocidas.md` y el apartado 6 de
> `03-proceso/sesion-05.md`. Abrir esta bitácora con el formato de la 05.
>
> Admitidas V-08 a V-11 y R-24 a R-30 de la sesión 05, y T-01 a T-08 de la
> sesión 04. El backend queda cerrado: comprobado contra un servidor real
> con `uvicorn` que N-01 responde `405` con `Allow: GET, HEAD` y que no hay
> regresiones.
>
> **Paso 1. Divergencias.** SPEC-04 se escribió el día 12 y el contrato del
> backend cambió el 13. Comparar lo que SPEC-04 dice que consume con lo que
> el backend hace de verdad: arrancar la aplicación con el cliente de test,
> leer su `/openapi.json` y contrastarlo con cada regla, requisito y caso
> de SPEC-04. Una tabla en la bitácora con una fila por divergencia: qué
> dice SPEC-04, qué hace el backend (con la spec y el apartado que lo fija)
> y qué se propone. Como mínimo: el `503` `service_unavailable`; el `400`
> `malformed_request`, el `415` y el `405`; el orden de los errores de un
> `422` y `unknown_field`; la ficha (`simulation_count` y las 50
> simulaciones de `id` más alto); la forma única del `id` de la ruta
> (`/clientes/abc`, `/clientes/01`); la regla nueva del email y las demás
> ayudas del alta, que ninguna contradiga al backend; el buscador (máximo
> de 100 caracteres y los casos de SPEC-01 5.9); y las limitaciones L-01 a
> L-05, donde afecten a lo que el frontend envía.
>
> **Paso 2. Lo externo, comprobado hoy y no de memoria.** La API de
> divisas: una petición real a la URL que fija SPEC-04, con el estado, la
> forma de la respuesta y la cabecera CORS. La versión exacta de Angular y
> de sus herramientas, con el margen de una semana de ADR-007: fecha de
> publicación de cada una en el registro de npm.
>
> **Paso 3.** Aplicar los cambios a SPEC-04, con historial y con el porqué
> de cada uno. La spec sigue en borrador: no cambia su estado. Si un cambio
> toca otra spec o un ADR, decirlo y hacerlo en commit aparte. Un commit
> por grupo de cambios, con el oráculo en verde.
>
> **Paso 4.** Una pasada del evaluador, en solo lectura y con las
> restricciones de siempre: SPEC-04 contra el contrato real del backend
> (specs, código y `/openapi.json`). Buscar requisitos que no se pueden
> cumplir con lo que el backend devuelve, respuestas del backend que
> SPEC-04 no contempla, requisitos ambiguos o sin caso de prueba, y
> contradicciones con `.claude/rules/frontend.md`. Informe intacto en
> `04-calidad/evaluacion-spec04-01.md`, con commit propio. Después,
> `04-calidad/respuesta-evaluacion-spec04-01.md` con una fila por hallazgo
> y la propuesta de la IA, sin aplicarla.
>
> **Parar ahí**: el Tech Lead decide cada hallazgo y aprueba SPEC-04. El
> plan del frontend viene después.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 09:24 | — | Lectura de `CLAUDE.md`, `.claude/rules/frontend.md`, el índice de specs, SPEC-04 entera, SPEC-01, SPEC-02 y SPEC-03 enteras (no solo su apartado 4: las reglas y los casos que cita el encargo están en 2.1, 2.10, 2.12, 5.7, 5.9 y 5.10 de SPEC-01 y en 2.4, 2.7 y 5.7 de SPEC-03), `04-calidad/limitaciones-conocidas.md`, la sesión 05 entera (para el formato y el apartado 6), las filas T-01 a T-08 de la sesión 04, ADR-001, ADR-003 y ADR-007, `.claude/agents/evaluador.md` y los módulos del control de specs del oráculo y del hook. `git status` limpio, `HEAD` en `58da604`. Apertura de esta bitácora |

| 09:29 | — | **Paso 1.** Sondeo del backend con un script fuera del repositorio, con el cliente de test y una base de datos en la carpeta temporal: `/openapi.json` volcado y resumido, y las sondas de los ocho puntos del encargo. La primera ejecución (09:28) mezcló en la salida el registro de los `503`, que el backend escribe con su traza; la segunda, a las 09:29, separó la salida del registro y es la que se usa. A las 09:35, cinco sondas más del email y una de un `id` grande en el cuerpo. `git status` sin cambios fuera de esta bitácora |
| 09:29 | — | Comprobado con Node 24.18.0 el comportamiento de JavaScript del que dependen tres divergencias (un *surrogate* suelto, la conversión de un texto en número y `JSON.stringify`) |
| 09:30 | — | **Paso 2.** Petición real a la API de divisas (09:29:55, con `curl` y la cabecera `Origin`) y consulta del registro de npm con un script de solo lectura fuera del repositorio (09:30 a 09:33). Descargados a la carpeta temporal, solo para leerlos, tres paquetes publicados: `@schematics/angular` 21.2.29 (las versiones que el CLI escribe en un proyecto nuevo), `@angular/forms` y `@angular/common` 21.2.26 (el validador de email y la codificación de los parámetros de consulta). Nada instalado ni ejecutado |
| 09:36 | — | Tablas del paso 1 y del paso 2 escritas en el apartado 3, antes de tocar SPEC-04 |
| 09:58 | `c95d207` a `86b2a96` | Fila escrita a las 09:58. **Paso 3**: seis commits de SPEC-04 y uno de los ADR; el detalle y la hora de cada uno están en la tabla «Paso 3» del apartado 3. Oráculo en verde antes de cada uno |
| 09:58 | *(este commit)* | Bitácora hasta aquí, para que el evaluador trabaje sobre un árbol limpio |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (09:23)

| Qué | Decisión del Tech Lead |
|---|---|
| V-08 a V-11 y R-24 a R-30 (precisiones de la sesión 05) | Admitidas |
| T-01 a T-08 (precisiones de la sesión 04) | Admitidas |
| Backend | **Cerrado.** El Tech Lead dice haber comprobado contra un servidor real con `uvicorn` que N-01 responde `405` con `Allow: GET, HEAD` y que no hay regresiones (lo afirma él; la IA no lo ha visto) |
| SPEC-04 | Sigue en `borrador`. La IA la pone al día y **no cambia su estado**; la aprueba el Tech Lead después de decidir los hallazgos del evaluador |

### Paso 1 · Divergencias entre SPEC-04 y el backend (09:24–09:36)

**Cómo se ha comparado.** La aplicación arrancada con el cliente de test y
una base de datos nueva en la carpeta temporal; su `/openapi.json` (OpenAPI
3.1.0) leído entero; y una sonda por cada punto del encargo. Las columnas
«Qué hace el backend» citan la spec que lo fija y, donde dice «sondeado»,
lo que respondió la aplicación hoy.

**Lo que coincide** (sin fila en la tabla): las seis llamadas de SPEC-04
4.1 existen en el OpenAPI con los campos y tipos de los ejemplos; la
respuesta de `POST /pricing/quote` y la de `POST /simulations` son las de
SPEC-02 (4) y SPEC-03 (4.1), con los importes de 5.5; `GET /meta` devuelve
los nueve países y los tres planes de SPEC-01 4.4, en su orden; el buscador
devuelve `{"items": […]}` con los cinco campos de 4.3; `created_at` llega
en UTC con precisión de segundos; el historial llega por `id` descendente;
y los ejemplos que citan CA-05 y CA-08 siguen en su sitio.

| # | Qué dice SPEC-04 | Qué hace el backend | Qué propone la IA |
|---|---|---|---|
| DV-01 | No nombra el `503`. Cae en «otro error», con el mismo aviso que un `500` (2.3) | Toda llamada que lee o escribe la base de datos responde `503` `service_unavailable` si no puede abrirla (índice, «Errores genéricos»; SPEC-01 4.1 a 4.3, SPEC-02 4, SPEC-03 4.1 y 5.7). El índice dice que el frontend trata distinto el `500` y el `503`. **Sondeado** con el fichero apartado: las cinco llamadas de negocio dan `503` en `application/problem+json`, con la cabecera CORS y sin `Retry-After`; `GET /meta` sigue en `200` (no lee la base de datos); una petición no válida sigue dando `422` | Tabla nueva en 2.7 con el tratamiento de cada error genérico por su `code`. El `503` tiene su aviso («no disponible ahora»), distinto del de error inesperado; los dos con «Reintentar». Requisitos y casos nuevos |
| DV-02 | No nombra el `400`, el `415` ni el `405`, ni el `404` `not_found` de una ruta que no existe | Índice, «Errores genéricos», y SPEC-03 5.7. **Sondeado**: los cuatro llegan en `application/problem+json` con su `code` y con la cabecera CORS. **El frontend sí puede provocar un `400`**: un *surrogate* suelto en un campo de texto sale de `JSON.stringify` como el escape `\ud800` (comprobado con Node) y el backend lo rechaza con `malformed_request` (sondeado) | En la tabla de 2.7: si llegan, el aviso de error inesperado con «Reintentar», y el `code` en el estado de error. Para el caso que sí se puede provocar: la ayuda del alta no envía un texto mal formado, y el buscador lo envía bien formado (DV-06 y DV-07) |
| DV-03 | Cada error de un `422` va junto a su campo; un `field` desconocido, al aviso general (2.3). No dice cuántos errores puede traer un campo, ni el orden, ni qué pasa en el simulador | Un solo error por campo, en el orden del contrato, y después un `unknown_field` por cada campo de más, por orden alfabético; si hay un parámetro de consulta desconocido, solo llegan esos (índice, «Errores de validación»; SPEC-01 2.12 y E-35). **Sondeado**: `company_name`, `tax_id`, `contact_email`, `country`, `plan` y después `Alfa`, `alfa`, `zeta`. `POST /simulations` y `POST /pricing/quote` responden igual, con sus campos | Escribirlo: como mucho un mensaje por campo; el aviso general lista los errores sin campo en el orden recibido. La misma regla para el `422` del guardado y de la proyección, que hoy SPEC-04 no dice dónde se muestran |
| DV-04 | «Se muestran las 50 últimas de *N*» si `simulation_count` es mayor que las recibidas (2.4) | Como máximo las 50 de `id` más alto, por `id` descendente, y `simulation_count` con el total (SPEC-03 2.4, E-12 a E-15 y 4.2). **Sondeado** con 55 simulaciones: `simulation_count` 55, 50 recibidas, del `id` 55 al 6 | Coincide. Un ajuste: el texto dice el número recibido («las *M* últimas de *N*») en vez de llevar el 50 escrito, porque ese límite es del backend. Y la tabla de contratos dice qué campos recibidos no se muestran (`currency`, `customer_id` y el `country` de cada simulación) |
| DV-05 | «Cliente no encontrado» si el cliente responde `404`, o `422` porque el `id` no es válido (`/clientes/abc`, `/clientes/0`). No dice cómo pasa el frontend el `id` de la ruta a la API ni nombra `/clientes/01` | En la ruta, un `id` tiene una sola forma; todo lo demás es `not_an_integer` (índice, «Identificadores»; SPEC-01 5.10). **Sondeado**: `abc`, `01`, `+1`, `1.0`, `1_0` y un espacio delante o detrás dan `422` `not_an_integer`; `0`, `-1`, 2^63 y 5000 nueves, `422` `out_of_range`; `999`, `404` `customer_not_found`. **El riesgo está en el frontend**: `Number('01')`, `Number('+1')`, `Number('1.0')` y `Number(' 1')` valen 1 (comprobado con Node), así que un frontend que convierta el segmento en número daría al cliente 1 varias direcciones, lo que el backend prohíbe. Y `Number('9007199254740993')` vale 9007199254740992: pediría otro cliente | El `id` de la ruta **nunca se convierte en número** para pedir el cliente. Si el texto no es de 1 a 16 dígitos ASCII sin ceros a la izquierda, o pasa de 9007199254740991 (el mayor entero exacto de JavaScript), se muestra «Cliente no encontrado» **sin llamar**; si lo es, se pide con ese mismo texto y decide el backend. **`/clientes/abc` y `/clientes/01` muestran «Cliente no encontrado», con el enlace al panel y sin petición.** Todo lo que este filtro rechaza lo rechaza también el backend, salvo un `id` entre 2^53 y 2^63 − 1: limitación propuesta (C-01) |
| DV-06 | Ayuda del alta: obligatorios, nombre de 2 a 120 tras recortar, «forma básica del email», identificador no vacío y de 30 como máximo (2.3). No dice qué es la forma básica ni si el identificador se recorta | Regla del email de SPEC-01 2.1 y 2.12 (H-08 de ayer): ningún separador Unicode, una sola `@`, dominio con punto. **Sondeado**: el backend **acepta** `josé@empresa.example`, un texto de 65 caracteres antes de la `@`, comas y comillas; **rechaza** `a@b` y cualquier separador. El validador de email de Angular 21.2.26 (expresión leída hoy en el paquete publicado) solo admite ASCII, 64 caracteres antes de la `@` y 63 por etiqueta, y acepta `a@b`: **rechazaría direcciones que el backend acepta**. El identificador se mide **sin recortar** (`12345678Z` y 21 espacios, válido; con 22, `too_long`) | Una tabla en 2.3 con lo que la ayuda comprueba y lo que deja al backend. Del email, solo: no vacío tras recortar, 254 como máximo, contiene una `@` y no empieza ni acaba en ella. **Nunca el validador de email del framework ni el del navegador**, ni el atributo `maxlength`, que cuenta unidades UTF-16. El identificador se mide sin recortar. Un texto con un *surrogate* suelto no se envía. Los valores se envían como están escritos: recorta y normaliza el backend (**rectificado después**: S-03) |
| DV-07 | «El campo admite 100 caracteres como máximo, el límite de la API» (2.2). No dice en qué unidad, ni qué texto se envía, ni cómo | 100 **puntos de código, medidos antes de recortar**; 101, o 100 y un espacio, dan `422` `too_long` (SPEC-01 2.12, 4.3, 5.9 y E-30). **Sondeado**: 100 emojis, `200`; 101, `422`. `q=a+b` sin codificar se lee como «a b». `%`, `_`, `\` y la comilla son texto literal; `%00` devuelve la lista vacía; solo espacios o solo U+0301, el listado inicial. Angular 21.2.26 codifica el `+` y deja sin codificar `@ : $ , ; = ? /` (leído en el paquete), que el backend lee bien (sondeado); con un *surrogate* suelto, `encodeURIComponent` lanza un error (Node) | El límite se mide como el backend: puntos de código del texto tal como está escrito. Si lo supera, no se llama y se avisa junto al campo. `q` va siempre como parámetro del cliente HTTP, nunca concatenado, una sola vez (L-04), y sin `q` si el texto está vacío. Un *surrogate* suelto se sustituye por U+FFFD antes de enviar. El frontend muestra lo que llega, también cuando es el listado inicial. Casos nuevos en 5.3 |
| DV-08 | No nombra las limitaciones del backend | L-01 a L-05 (`04-calidad/limitaciones-conocidas.md`) | Apartado nuevo 4.3 que dice, de cada una, por qué lo que el frontend envía no la alcanza: cuerpos pequeños porque la ayuda acota los tres textos (por eso el máximo de 254 del email entra en la ayuda, L-01); interfaces escritas a mano desde las specs y no desde el OpenAPI (L-02); cuerpos serializados desde objetos, sin claves repetidas (L-03); un solo `q` (L-04); ningún entero de más de 16 dígitos sale del frontend (L-05) |
| DV-09 | «`201`: navega al detalle del cliente creado» (2.3). 2.9 solo dice que el backend admite el origen del frontend | El `201` trae `Location`, pero CORS no la expone (SPEC-03 2.7 no declara cabeceras expuestas). **Sondeado**: ninguna respuesta lleva `access-control-expose-headers`; una comprobación previa con una cabecera de más (`x-requested-with`) se rechaza con `400`; desde `http://127.0.0.1:4200` no llega la cabecera CORS | 2.3: el `id` sale del cuerpo del `201`. 2.9: el frontend solo usa `GET` y `POST`, no añade cabeceras propias, no lee cabeceras de respuesta y se sirve desde `http://localhost:4200` exactamente; desde otro origen, toda llamada acaba en `network_error` |
| DV-10 | E-15 decide «Cliente no encontrado» por el estado (`404`) y E-11 manda decidir por el `code`. En el simulador, una proyección con `404` lleva a esa vista (E-37) y un guardado con `404`, a un aviso (5.5) | El `404` tiene dos códigos: `customer_not_found` (el recurso) y `not_found` (la ruta no existe) (índice). **Sondeado**: `GET /customers/a/b` responde `404` `not_found` | E-15 y E-37 deciden por `customer_not_found`, y valen igual para el cliente, la proyección y el guardado. Un `not_found` es una URL mal construida por el frontend: error inesperado |
| DV-11 | 5.5 nombra el `500` al guardar; no nombra `tax_rate_not_defined` | `500` `tax_rate_not_defined` en la proyección y en el guardado (SPEC-02 E-10 y 4; SPEC-03 E-10 y 4.1) | Mismo aviso que `internal_error` (tabla de 2.7): son fallos del servidor y el usuario no puede hacer nada distinto |
| DV-12 | 4.1 lista las llamadas, sin las respuestas que cada una puede dar | El OpenAPI declara por operación: `POST /customers` 201, 409, 422, 503; `GET /customers` 200, 422, 503; `GET /customers/{id}` 200, 404, 422, 503; `POST /pricing/quote` 200, 404, 422, 500, 503; `POST /simulations` 201, 404, 422, 500, 503; `GET /meta` 200 | 4.1 gana las respuestas de cada llamada y qué hace el frontend con cada una |
| DV-13 | «Campos numéricos enteros», «un entero dentro de sus límites» (2.5, E-22, E-36). No dice qué textos cuentan como entero | El backend solo admite un número JSON entero y rechaza `15.0` y `"15"` (SPEC-02 4; SPEC-03 4.1) | Válido es un valor numérico entero (`Number.isInteger`) dentro de los límites; se envía como número JSON sin decimales (`JSON.stringify(15.0)` da `15`, comprobado con Node). El `customer_id` de las dos peticiones es el `id` del cliente cargado |
| DV-14 | Apartado 9: «si cambian sus contratos, las tablas de 5.4 y 5.5». La nota de D-09 dice que la última versión de Playwright es la 1.65.0 | Los contratos cambiaron el 13. Playwright 1.65.1 se publicó ayer (paso 2) | Apartado 9 al día. La nota de D-09, con la fecha de cada versión y el margen de ADR-007 |

**Lo que el OpenAPI dice de otra forma que las specs**, sin efecto en
SPEC-04 y sin tocar (el backend está cerrado): `currency` no figura como
obligatorio en la respuesta de `POST /pricing/quote` (tiene valor por
defecto y llega siempre; en la de `POST /simulations` sí figura), y los
límites numéricos salen como decimales (L-02, ya aceptada).

**Propuestas que la IA no aplica**, porque no las pide el contrato del
backend y son decisiones de producto. Las decide el Tech Lead:

| # | Qué | Recomendación de la IA |
|---|---|---|
| C-01 | El filtro de DV-05 deja fuera a un cliente con `id` entre 2^53 y 2^63 − 1. Solo puede existir si se inserta a mano en la base de datos | Aceptarlo como limitación conocida (sería L-06). SPEC-04 lo dice en 2.1; **no se ha añadido la fila a `limitaciones-conocidas.md`**, que solo cambia cuando el Tech Lead acepta una |
| C-02 | El buscador devuelve como máximo 20 clientes y no dice cuántos hay (SPEC-01 E-26 y A13). SPEC-04 no avisa al usuario cuando llegan 20 | Una nota bajo la lista cuando llegan 20: «Se muestran como máximo 20 clientes». Obliga a escribir ese 20 en el frontend |
| C-03 | Con la base de datos recién creada, el listado inicial llega vacío y el panel diría «No hay clientes que coincidan», sin que nadie haya buscado nada | Un mensaje propio para la lista vacía sin texto de búsqueda («Todavía no hay clientes»), con el acceso al alta |
| C-04 | Un cliente o una simulación cuyo código de país o de plan no está en `/meta` (datos incoherentes, el caso de SPEC-02 E-10). E-35 dice que nunca se muestran códigos | Mostrar el código recibido, marcado como no reconocido. Hoy SPEC-04 no dice nada |
| C-05 | Un guardado que agota los 10 s puede haberse guardado en el servidor; «Reintentar» crearía una segunda simulación igual | Tras un `timeout` al guardar, el aviso lo dice y ofrece ir al detalle a comprobarlo, además de reintentar |

### Paso 2 · Lo externo, comprobado hoy (09:29–09:34)

**API de divisas.** Petición real con `curl`, a las 09:29:55 (sábado), a
la URL que fija SPEC-04, con la cabecera `Origin: http://localhost:4200`:

| Qué | Resultado |
|---|---|
| Estado y tipo | `200`, `application/json; charset=utf-8` |
| Forma | Una lista de tres objetos `{date, base, quote, rate}`, la de 2.6: `[{"date":"2026-11-14","base":"EUR","quote":"CHF","rate":0.92491},{"date":"2026-11-14","base":"EUR","quote":"GBP","rate":0.83559},{"date":"2026-11-14","base":"EUR","quote":"USD","rate":1.1083}]` |
| CORS | `access-control-allow-origin: *` y `access-control-allow-methods: GET, OPTIONS`; `vary: Origin`. Un `OPTIONS` de comprobación previa responde `200` con las mismas cabeceras |
| Caché | `cache-control: public, max-age=55805, stale-if-error=86400` |
| Divisa inexistente (`quotes=XXX`) | `422` con `{"status":422,"message":"invalid currency: XXX"}`, igual que el día 12 |
| Fin de semana | Hoy es sábado y los tres tipos traen la fecha de hoy, `2026-11-14`. La `v1`, pedida a continuación, trae `2026-11-13` y otro tipo para USD y CHF, y una cabecera `deprecation` |

Lo que cambia respecto a lo que SPEC-04 anota del día 12: los tipos (es lo
esperado) y la fila «fines de semana», que deja de estar sin verificar para
un sábado. **Sigue sin probarse desde un navegador real.**

**Angular y sus herramientas.** Fecha de corte de ADR-007 para hoy:
`2026-11-07T00:00:00Z` (una semana antes). Fechas del registro de npm,
consultadas a las 09:30. «Elegible» es la última versión de su línea
publicada antes del corte.

| Paquete | Elegible | Publicada | Lo que queda fuera del margen |
|---|---|---|---|
| `@angular/cli`, `@angular/build` y `@schematics/angular` | **21.2.29** | 2026-10-28 | 21.2.30, del 2026-11-12: la etiqueta `v21-lts` apunta hoy a ella |
| `@angular/core`, `common`, `compiler`, `compiler-cli`, `forms`, `platform-browser` y `router` | **21.2.26** | 2026-11-02 | Ninguna: es la última de la línea 21 |
| `typescript` (el CLI escribe `~5.9.2`) | 5.9.3 | 2025-09-30 | Ninguna en la línea 5.9 |
| `rxjs` (`~7.8.0`) | 7.8.2 | 2025-02-22 | Ninguna |
| `tslib` (`^2.3.0`) | 2.9.1 | 2026-10-30 | Ninguna |
| `vitest` (`^4.0.8`), el runner por defecto del CLI 21 | 4.1.12 | 2026-10-15 | Ninguna |
| `jsdom` (`^28.0.0`) | 28.1.0 | 2026-02-15 | Ninguna en la línea 28 |
| `prettier` (`^3.8.1`) | 3.9.10 | 2026-10-10 | 3.10.0 (2026-11-11) y 3.10.1 (2026-11-12) |
| `angular-eslint` (línea 21) | 21.4.0 | 2026-05-13 | Ninguna |
| `eslint` | 10.14.0 | 2026-10-30 | 10.15.0, de ayer. La línea 9 (9.39.5) figura como obsoleta en el registro |
| `typescript-eslint` | 8.72.1 | 2026-10-26 | 8.72.2, del 2026-11-09 |
| `@playwright/test` | 1.65.0 | 2026-11-05 | 1.65.1, de ayer |

- **La versión de ADR-001 se mantiene**: Angular CLI 21.2.29 sigue siendo
  la elegible con el margen, y sus paquetes de plataforma son los 21.2.26.
  Los dos declaran `node: ^20.19.0 || ^22.12.0 || >=24.0.0`; el Node del
  equipo es el 24.18.0.
- Los rangos entre paréntesis son los que el CLI 21.2.29 escribe en un
  proyecto nuevo, leídos en su paquete de plantillas. El proyecto nuevo usa
  Vitest por defecto.
- **Cómo aplicar el margen con npm sigue sin decidir** (ADR-007). El npm
  del equipo (11.16.0) tiene dos opciones de configuración para ello,
  `before` y `min-release-age` (vistas con `npm config ls -l`, las dos sin
  valor); **ninguna se ha probado**. Es parte del plan del frontend.
- **Nada de esto se ha instalado ni ejecutado**: son fechas y metadatos
  del registro.

### Paso 3 · Cambios aplicados a SPEC-04 (09:37–09:57)

SPEC-04 sigue en `borrador`: la IA no ha tocado su estado ni el índice.
Cada cambio lleva su fila en el historial de la spec, con el motivo. Cada
commit, con el oráculo en verde justo antes (20 correctas, 0 con fallo y 4
inactivas, las del frontend).

| Hora | Grupo | Divergencias | Qué cambia en SPEC-04 | Commit |
|---|---|---|---|---|
| 09:40 | Errores genéricos del backend | DV-01, DV-02, DV-10 y DV-11 | Tabla nueva en 2.7 con el aviso de cada error por su `code`; el `503` tiene el suyo. «Cliente no encontrado» se decide por `customer_not_found`, también al guardar. E-42 y E-43 nuevos; E-15, E-25 y E-37 cambian; tabla 5.6 y CA-16 | `c95d207` (09:40:22) |
| 09:43 | Alta | DV-03, DV-06, DV-09 y parte de DV-02 y DV-08 | Tabla en 2.3 con lo que la ayuda comprueba y lo que deja al backend; email sin el validador del framework ni el del navegador; sin `maxlength`; un texto con un *surrogate* suelto no se envía; el `id` sale del cuerpo del `201`; forma de `errors`. E-44, E-45 y E-46 nuevos; catorce filas en 5.4; CA-05 y D-13 | `23df112` (09:43:02) |
| 09:46 | `id` de la ruta, detalle y simulador | DV-04, DV-05, DV-13 y parte de DV-03 | El `id` no se convierte en número y se filtra por su forma; aviso del historial con el número recibido; `customer_id`, campos numéricos y `422` del simulador. E-47, E-48 y E-49 nuevos; E-15 cambia; tabla 5.7, cinco filas en 5.5; CA-07, CA-08 y CA-17 | `b760109` (09:46:14) |
| 09:48 | Buscador | DV-07 | Límite en puntos de código y sin recortar; un solo `q` del cliente HTTP; sin `q` si está vacío; *surrogate* suelto sustituido. E-50 y E-51 nuevos; ocho filas en 5.3; CA-04 | `2ecf7be` (09:48:37) |
| 09:53 | Contratos, CORS, limitaciones y lo externo | DV-08, DV-09, DV-12, DV-14 y el paso 2 | 4.1 con las respuestas de cada llamada y los campos que no se usan; 4.3 nuevo con L-01 a L-05; 2.9 con lo que exige CORS; 4.2 con la petición de hoy; nota de D-09; apartado 9 y fila «Depende de». E-52 y CA-18 nuevos. **Corrige E-46**, escrito a las 09:43 (S-03) | `d2619c1` (09:53:02) |
| 09:55 | **Otros documentos, en commit aparte** | Paso 2 | ADR-001 (fechas de publicación de Angular CLI 21.2.29 y de los paquetes 21.2.26), ADR-003 (la petición de hoy) y ADR-007 (la fecha del CLI ya está comprobada; el mecanismo en npm sigue sin decidir). Ninguna decisión cambia | `3d7b8cf` (09:55:08) |
| 09:57 | Corrección | — | 2.2 y 2.3 nombraban dos funciones de ES2024 que la configuración por defecto del CLI no conoce (S-04) | `86b2a96` (09:57:21) |

**No se ha tocado** ninguna otra spec, `limitaciones-conocidas.md`,
`.claude/rules/frontend.md` ni el índice de specs.

Precisiones de la IA sobre el paso 3, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| S-01 | La IA leyó SPEC-01, SPEC-02 y SPEC-03 enteras, no solo su apartado 4 | Las reglas que el encargo manda contrastar (email, buscador, `id`, orden de los errores) están en los apartados 2 y 5 |
| S-02 | **Todo lo aplicado es una propuesta de la IA**: los textos de los avisos, el código `unknown_error`, el filtro del `id` y lo que comprueba la ayuda no los ha decidido nadie más. La spec lo dice en cada fila de su historial («pendiente de la revisión del Tech Lead») | El encargo manda aplicar los cambios; aprobarlos es del Tech Lead |
| S-03 | **Rectificación dentro de la sesión.** A las 09:43 la IA escribió que los valores del alta se envían «tal como están escritos» (E-46). A las 09:50, al escribir la fila de L-01 de 4.3, vio que así un nombre válido rodeado de megabytes de espacios se enviaría entero, porque la ayuda mide el texto recortado. E-46 dice ahora que el nombre y el email se envían recortados (solo U+0020, el mismo carácter que recorta el backend); el identificador, tal cual | La afirmación de 4.3 («ningún cuerpo pasa de unos kilobytes») era falsa con la regla anterior. No se enmendó el commit de las 09:43: la corrección está en el de las 09:53 y en el historial de la spec |
| S-04 | **Error de la IA, visto antes de la evaluación.** Las reglas del *surrogate* suelto nombraban `isWellFormed()` y `toWellFormed()`, y en la bitácora (DV-06 y DV-07) también. Son de ES2024; la plantilla de `tsconfig.json` del CLI 21.2.29, leída a las 09:55, compila para ES2022 sin declarar otra biblioteca. Contradecía la regla de usar la configuración por defecto del CLI. Sustituidas por una expresión regular en modo Unicode, comprobada con Node | La IA las había comprobado con Node 24, que sí las tiene, y no con lo que el proyecto compila |
| S-05 | DV-05: la alternativa al filtro era enviar el texto de la ruta tal cual y dejar que el backend responda `422`. La IA eligió el filtro porque, sin él, un `id` por encima de 2^53 − 1 llegaría redondeado al cuerpo de la proyección y del guardado, y porque evita construir una URL con un texto arbitrario. A cambio, repite en el frontend la forma del `id` | Es la decisión con más alternativas de las aplicadas; si el Tech Lead prefiere la otra, cambian 2.1, E-15, E-47 y 5.7 |
| S-06 | DV-06: la ayuda del email comprueba el máximo de 254 caracteres, que SPEC-04 no tenía, además de la `@` | Sin él, el email era el único texto del alta sin tope (L-01). El backend rechaza lo mismo con `too_long` (sondeado con 254 y 255) |
| S-07 | La fila «Depende de» de la cabecera gana las convenciones comunes del índice (ADR-006) y ADR-007 | La spec cita ahora las dos |
| S-08 | Los tres ADR se tocaron sin que el encargo los nombre: solo con datos comprobados hoy, sin cambiar ninguna decisión, y en commit aparte, como manda el encargo para lo que toque un ADR | ADR-007 decía que la fecha del CLI no estaba comprobada, y ya lo está |
| S-09 | Dos descuidos corregidos antes de su commit: el historial decía «quince filas» y son catorce, y una edición duplicó el título del apartado 4.2 | Vistos al repasar el cambio |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git rev-parse --short HEAD` (09:24) | Limpio, `58da604` |

## 5. No verificado

*(se rellena durante la sesión)*

## 6. Tareas pendientes

*(se rellena al cerrar)*
