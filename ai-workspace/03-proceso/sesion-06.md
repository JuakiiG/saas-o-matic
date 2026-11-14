# Sesión 06 · SPEC-04 al día con el contrato final del backend

| | |
|---|---|
| **Fecha** | 2026-11-14 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | SPEC-04 puesta al día con el contrato final del backend y **aprobada por el Tech Lead** (a las 10:22, al cerrar la primera parte, seguía en `borrador`); en esta sesión no se ha escrito código. **Paso 1**: 14 divergencias (DV-01 a DV-14) entre SPEC-04 y lo que el backend hace, sondeadas con el cliente de test y contrastadas con su `/openapi.json`; las de más peso, el `503` que la spec no nombraba, un validador de email del framework que rechazaría direcciones que el backend acepta y un `id` de ruta que, convertido en número, daría varias direcciones a un cliente. **Paso 2**: la API de divisas responde `200` con la misma forma y `access-control-allow-origin: *`, también en sábado; Angular CLI 21.2.29 (publicado el 2026-10-28) y los paquetes 21.2.26 cumplen el margen de una semana, y la 21.2.30 queda fuera. **Paso 3**: seis commits de SPEC-04 (52 requisitos, eran 41; 18 criterios, eran 15; tablas nuevas 5.6 y 5.7 y apartado 4.3) y uno aparte para ADR-001, ADR-003 y ADR-007, sin cambiar ninguna decisión; dos rectificaciones de la IA dentro de la sesión (S-03 y S-04). **Paso 4**: pasada del evaluador (Opus 5.5, comprobado en su registro), en solo lectura: **12 hallazgos, ninguno de severidad alta, 2 medios y 10 bajos**; ocho los introdujo la IA hoy. Informe intacto en `04-calidad/evaluacion-spec04-01.md` y respuesta, con una fila por hallazgo y tres casos más, en `04-calidad/respuesta-evaluacion-spec04-01.md`. **Segunda parte, desde las 10:34**: el Tech Lead revisa la sesión y decide los doce hallazgos, los casos A-01 a A-03 y las propuestas C-01 a C-05 (cambia una, C-04). Aplicado en siete commits con historial (`5830543` a `066bcc8`; SPEC-04 queda con 55 requisitos y 18 criterios, y `limitaciones-conocidas.md` gana L-06), más el apartado 4 de la respuesta (`22a6578`). **SPEC-04 pasa a `aprobada` a las 11:06** (`0ef98be`), en la spec y en el índice; el bloque del frontend deja de estar cerrado por el control de specs. **Plan del frontend presentado, sin escribir código ni crear el proyecto** (apartado 3): para darlo con evidencia la IA ensayó en una carpeta temporal fuera del repositorio las dos opciones de npm, la orden de creación y los umbrales del oráculo. Lo que más pesa del ensayo: ninguna de las dos opciones de npm revisa un fichero de bloqueo ya escrito; el CLI escribe los ficheros con CRLF en Windows, que el oráculo rechaza; y `npm audit` da 27 avisos moderados en herramientas de desarrollo, con una corrección (ESLint 10.15.0) que queda fuera del margen (regla 3 de ADR-007, a decidir). Oráculo en verde con 20 comprobaciones activas y 4 inactivas. Quedan sin aprobar las precisiones U-01 a U-05 y X-01 a X-10. **Sesión parada: el Tech Lead aprueba el plan antes de crear nada** |

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

**Segundo prompt, a las 10:34** (resumen fiel; las decisiones, fila a fila,
están en el apartado 3):

> Revisada la sesión 06. Admitidas S-01 a S-09; en S-05 se queda el filtro
> del `id`. Decisiones sobre C-01 a C-05, H-01 a H-12 y A-01 a A-03.
> Aplicarlo todo a SPEC-04, con historial, y la fila L-06 en
> `limitaciones-conocidas.md`. Un commit por grupo, con el oráculo en
> verde. Rellenar el apartado 4 de la respuesta con la decisión y el commit
> de cada fila. Después, marcar SPEC-04 como aprobada, en la spec y en el
> índice; el hook pedirá confirmación y la da el Tech Lead.
>
> Con SPEC-04 aprobada, presentar el plan del frontend, **sin escribir
> código ni crear el proyecto**: (1) cómo se aplica en npm el margen de una
> semana de ADR-007, probando las dos opciones en una carpeta temporal
> fuera del repositorio y proponiendo una; versiones exactas, sin rangos, y
> fichero de bloqueo. (2) La orden exacta con la que se crea el proyecto
> con el CLI 21.2.29, con sus opciones, y qué se quita de lo que genera.
> (3) Cómo pasa a activa cada comprobación del frontend del oráculo y cómo
> se cumplen sus umbrales, sin tocar `scripts/`. (4) Las piezas, en orden,
> cada una con sus requisitos y sus casos: lo común de `core/` (cliente de
> la API, errores por su `code`, medidas de texto, filtro del `id`, formato
> del dinero), `/meta`, panel, alta, detalle, simulador y divisas. (5) La
> presentación: sin librería de UI, *mobile-first* a 375 px, y cómo se
> organiza el CSS. (6) Como máximo tres paradas para que el Tech Lead
> revise, y en cuál abre la aplicación en el navegador por primera vez.
> (7) Qué no se puede comprobar hasta tener Playwright.
>
> **Parar con el plan**: lo aprueba el Tech Lead antes de crear nada.

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
| 10:00–10:13 | — | El commit anterior es `8516f5c` (09:59:27 según `git log`). **Paso 4**: pasada del evaluador, en solo lectura, sobre `8516f5c`. La IA no tocó el repositorio mientras trabajaba |
| 10:15 | — | Informe guardado intacto en `04-calidad/evaluacion-spec04-01.md` y comparado con el mensaje del registro del subagente: ninguna línea distinta (apartado 3) |
| 10:16 | `e03fc80` | Commit propio del informe (10:16:47 según `git log`). Oráculo en verde antes |
| 10:18 | — | La IA repite lo que afirma cada hallazgo, sin corregir nada: los doce se reproducen |
| 10:21 | `5bfa62f` | `04-calidad/respuesta-evaluacion-spec04-01.md`: una fila por hallazgo y la propuesta de la IA, **sin aplicar ninguna** (10:21:22 según `git log`). Oráculo en verde antes |
| 10:22 | *(este commit)* | Cierre de esta bitácora. **La IA para aquí**: el Tech Lead decide cada hallazgo y aprueba SPEC-04 |
| 10:34 | — | El cierre anterior es `f66c4ed` (10:24:04 según `git log`). **El Tech Lead revisa la sesión**: admite S-01 a S-09, decide C-01 a C-05, H-01 a H-12 y A-01 a A-03, manda aplicarlo todo, aprobar SPEC-04 y presentar el plan del frontend sin crear nada (apartado 3). Anotado en esta bitácora antes de empezar. Una línea en blanco que partía en dos esta tabla desde las 09:36, quitada |
| 11:30 | `5830543` a `066bcc8` | Fila escrita a las 11:30. **Correcciones decididas, aplicadas**: siete commits entre las 10:37 y las 10:52, con su hora en la tabla del apartado 3. Oráculo en verde antes de cada uno |
| 11:30 | `22a6578` | Fila escrita a las 11:30. Apartado 4 de la respuesta a la evaluación, con la decisión y el commit de cada fila (10:54:37 según `git log`). Oráculo en verde antes |
| 11:30 | `0ef98be` | Fila escrita a las 11:30. **SPEC-04 pasa a `aprobada` (2026-11-14)**, en la spec y en el índice (11:06:58 según `git log`). El oráculo, a las 11:06, en verde, con sus tres comprobaciones de specs correctas |
| 11:08–11:29 | — | Fila escrita a las 11:30. Lectura de los módulos del oráculo que ejecutan las comprobaciones del frontend (`checks_stack.py`, `checks_code.py`, `checks_trace.py`, `repo.py`). **Ensayo en una carpeta temporal fuera del repositorio**: las dos opciones de npm, la orden de creación con el CLI 21.2.29, la instalación con versiones exactas, la compilación, los tests con cobertura, ESLint y los finales de línea (apartado 3). Una orden de la IA fue denegada a las 11:12 y se rehízo sin borrar nada (X-07). `git status` del repositorio: solo esta bitácora |
| 11:30 | *(este commit)* | Plan del frontend escrito en el apartado 3 y cierre de esta bitácora. **La IA para aquí**: el Tech Lead aprueba el plan antes de crear nada |

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
| S-04 | **Error de la IA, visto antes de la evaluación.** Las reglas del *surrogate* suelto nombraban `isWellFormed()` y `toWellFormed()`. Son de ES2024; la plantilla de `tsconfig.json` del CLI 21.2.29, leída a las 09:55, compila para ES2022 sin declarar otra biblioteca. Contradecía la regla de usar la configuración por defecto del CLI. Sustituidas por una expresión regular en modo Unicode, comprobada con Node | La IA las había comprobado con Node 24, que sí las tiene, y no con lo que el proyecto compila |
| S-05 | DV-05: la alternativa al filtro era enviar el texto de la ruta tal cual y dejar que el backend responda `422`. La IA eligió el filtro porque, sin él, un `id` por encima de 2^53 − 1 llegaría redondeado al cuerpo de la proyección y del guardado, y porque evita construir una URL con un texto arbitrario. A cambio, repite en el frontend la forma del `id` | Es la decisión con más alternativas de las aplicadas; si el Tech Lead prefiere la otra, cambian 2.1, E-15, E-47 y 5.7 |
| S-06 | DV-06: la ayuda del email comprueba el máximo de 254 caracteres, que SPEC-04 no tenía, además de la `@` | Sin él, el email era el único texto del alta sin tope (L-01). El backend rechaza lo mismo con `too_long` (sondeado con 254 y 255) |
| S-07 | La fila «Depende de» de la cabecera gana las convenciones comunes del índice (ADR-006) y ADR-007 | La spec cita ahora las dos |
| S-08 | Los tres ADR se tocaron sin que el encargo los nombre: solo con datos comprobados hoy, sin cambiar ninguna decisión, y en commit aparte, como manda el encargo para lo que toque un ADR | ADR-007 decía que la fecha del CLI no estaba comprobada, y ya lo está |
| S-09 | Dos descuidos corregidos antes de su commit: el historial decía «quince filas» y son catorce, y una edición duplicó el título del apartado 4.2 | Vistos al repasar el cambio |

### Paso 4 · Pasada del evaluador (10:00–10:21)

| Hora | Qué |
|---|---|
| 10:00 | Lanzado el subagente `evaluador` con el árbol limpio en `8516f5c`. Encargo: SPEC-04 contra el contrato real del backend (las specs, el código y el `/openapi.json`, que debía obtener él arrancando la aplicación), buscando lo que pide el encargo de la sesión: requisitos que no se pueden cumplir, respuestas que SPEC-04 no contempla, requisitos ambiguos o sin caso de prueba y contradicciones con `.claude/rules/frontend.md`. Restricciones de siempre: solo lectura, no leer `03-proceso/` ni `04-calidad/` ni la historia de git, rutas relativas, decir en la cabecera qué modelo es y nombrar los caracteres invisibles por su código. Dos añadidas: no hacer peticiones a internet y poner la base de datos de sus sondeos fuera del repositorio. **La IA no le dio ninguna conclusión propia**: ni las divergencias, ni lo que cambió hoy, ni las precisiones. Como no puede abrir `limitaciones-conocidas.md`, el encargo le resume L-01 a L-05 en una frase cada una |
| 10:00–10:13 | La IA no tocó el repositorio |
| 10:13 | Informe recibido. `git status --short` vacío, `HEAD` en `8516f5c`, ningún `stash` y `backend/data/` sin crear: el evaluador no cambió nada |
| 10:14 | Informe escrito con `Write`, quitando solo la sangría de dos espacios que añade la herramienta. **Comparado con el mensaje que consta en el registro del subagente** (script de solo lectura fuera del repositorio): 184 líneas y 15.150 caracteres los dos, **ninguna línea distinta**, y el mensaje no trae ningún carácter de control ni separador que no sea el espacio y el salto de línea. En el mismo registro: tipo de agente `evaluador` y modelo `claude-opus-5-5` en sus 66 respuestas |
| 10:16 | Oráculo en verde. Commit propio del informe: `e03fc80` (10:16:47) |
| 10:18 | La IA repite lo que afirma cada hallazgo, con el cliente de test, con Node y leyendo el paquete de Angular, sin corregir nada |
| 10:21 | Respuesta escrita, con una fila por hallazgo. Oráculo en verde. Commit `5bfa62f` (10:21:22) |

**Resultado del informe**: oráculo en verde, ejecutado por el evaluador.
**12 hallazgos, ninguno de severidad alta**: 2 medios (H-01, formatear un
importe en EUR obliga a usar coma flotante, contra la regla del dinero; y
H-02, cinco requisitos sin ningún caso que los demuestre) y 10 bajos.
Ningún requisito `NO CONFORME`; 5 `AMBIGUO`, 5 `SIN CASO DE PRUEBA` y 1
`NO COMPROBABLE` (la API de divisas, por encargo). De los criterios, 13
`CONFORME`, 2 `AMBIGUO` y 3 `SIN CASO DE PRUEBA`.

**De los doce, ocho los introdujo la IA hoy** al poner la spec al día
(H-03, H-04, H-06, H-07, H-08, H-10, H-11 y H-12) y cuatro estaban desde
el día 12 (H-01, H-02, H-05 y H-09). La IA está de acuerdo con todos. **No
ha corregido ninguno.**

Precisiones de la IA sobre el paso 4, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| U-01 | El informe no da veredicto a E-42 ni a E-43: su tabla tiene 50 filas de requisitos y 39 `CONFORME`, y su resumen dice 52 y 41. Además, las filas sin caso de prueba remiten a «H-04» y el hallazgo que las describe es el H-02. El informe se queda como llegó (casos A-02 y A-03 de la respuesta) | Intacto quiere decir también con sus errores |
| U-02 | El encargo al evaluador lo redactó la IA, incluido el resumen de L-01 a L-05. El texto completo consta en el registro del subagente | Un resumen mal hecho podría haberle orientado |
| U-03 | La respuesta trae tres casos que no son hallazgos numerados del informe (A-01 a A-03). A-01 (CA-18 no puede comprobarse como está escrito) lo dice el propio evaluador en su apartado 4 | Para que no se pierda por no llevar número |
| U-04 | Las recomendaciones de H-01 (formatear el EUR por partes, solo con enteros) y de H-12 (decide el texto, no el número) las ha comprobado la IA con Node, no en un navegador ni con TypeScript | Son las dos que más cambian cómo se implementa |
| U-05 | El evaluador comprobó por su cuenta varias afirmaciones que la IA había escrito hoy en SPEC-04 (el validador de email de Angular, el *target* ES2022 del CLI, la expresión regular del *surrogate* y la codificación de `q`) y las da por ciertas. Una no lo era: que U+FFFD no coincide con ningún cliente (H-03) | La IA la escribió sin sondearla |

### Revisión de la sesión por el Tech Lead (10:34)

**Admitidas S-01 a S-09.** En S-05 se queda el filtro del `id`. El mensaje
no nombra U-01 a U-05, que siguen sin aprobar.

| # | Decisión del Tech Lead | Frente a la propuesta de la IA |
|---|---|---|
| C-01 | **Aceptada como limitación conocida L-06.** Redactada como lo que es: JavaScript no representa exactos los enteros por encima de 2^53 − 1, así que el frontend no abre un cliente con un `id` mayor; solo existiría insertado a mano | Aprobada, con la redacción fijada por él |
| C-02 | Sí: la nota cuando llegan 20 resultados | Aprobada |
| C-03 | Sí: un mensaje propio para el listado inicial vacío, con el acceso al alta. Por qué: es lo primero que se ve con la base de datos recién creada | Aprobada |
| C-04 | Si un código de país o de plan no está en `/meta`, se muestra el código **tal como llega, sin marca**. Se ajusta E-35 | **Cambiada.** La IA recomendaba mostrarlo marcado como no reconocido |
| C-05 | Sí: el aviso tras un `timeout` al guardar | Aprobada |
| H-01 | La recomendada: el EUR se formatea solo con enteros, y la regla del dinero no cambia | Aprobada |
| H-02, H-03, H-04, H-05, H-07, H-08, H-10 y H-11 | De acuerdo con la propuesta | Aprobadas |
| H-06 | La recomendada: se quita la rama del `422` | Aprobada |
| H-09 | (1) El tipo de cambio, con los decimales que trae, hasta 6. (2) Los importes de cuatro cifras, como los da `es-ES`, con su fila en 5.1. (3) Los rótulos de tramo propuestos | Aprobadas las tres recomendaciones |
| H-12 | **Decide el texto.** El campo es de texto con `inputmode="numeric"`, no un control numérico del navegador | Aprobada, fijando él el tipo de campo |
| A-01 | De acuerdo: se parte el criterio | Aprobada |
| A-02 | Vale con CA-16; no se pide nada más al evaluador | La IA lo dejaba a su decisión |
| A-03 | Nada que tocar | — |

Cómo: todo a SPEC-04, con historial, y la fila L-06 en
`limitaciones-conocidas.md`; un commit por grupo, con el oráculo en verde;
el apartado 4 de la respuesta, con la decisión y el commit de cada fila.
Después, SPEC-04 pasa a aprobada en la spec y en el índice (el hook pedirá
confirmación y la da él). Con ella aprobada, el plan del frontend, **sin
escribir código ni crear el proyecto**, en siete puntos; la IA para con el
plan.

### Correcciones decididas, aplicadas (10:37–10:54)

Horas de `git log --format=%ci`. Oráculo en verde antes de cada commit.
Todos los de SPEC-04 llevan su fila de historial.

| Hora | Commit | Decisiones | Qué cambia |
|---|---|---|---|
| 10:37:24 | `5830543` | H-01, H-05, H-09 | 2.6: el EUR se formatea solo con enteros, el tipo de cambio con hasta 6 decimales y los importes de cuatro cifras como los da `es-ES`; 2.8: rótulos de tramo; dos filas y dos tablas en 5.1; CA-01, CA-02 y CA-08 |
| 10:39:26 | `c682749` | H-02, A-01 | Cuatro filas nuevas en 5.3, 5.4 y 5.5; CA-18 se parte y CA-14 cita E-52 |
| 10:41:25 | `9de261a` | C-01 | Fila L-06 en `limitaciones-conocidas.md`; SPEC-04 la cita en 2.1, 4.3, 5.7 y el apartado 9 |
| 10:43:43 | `a7e00e5` | H-06, H-07, H-11 | Se quita la rama del `422` del cliente; la forma del `id` dice «el primero distinto de `0`»; la remisión de 5.7 a SPEC-01 5.10 |
| 10:46:03 | `bba612c` | H-03, H-04, H-08, C-02, C-03 | Buscador (cancelar al superar el límite, frase de U+FFFD, fila de 4.1) y panel (nota de los 20 y listado inicial vacío): E-53 y E-54 nuevos, cinco filas en 5.3 |
| 10:47:57 | `32393b1` | H-10, C-04 | Un código que `/meta` no trae se muestra tal como llega, sin marca (2.1, E-35, 5.3, CA-07); D-13 recoge el *surrogate* |
| 10:52:56 | `066bcc8` | H-12, C-05 | En el simulador decide el texto escrito y los campos son de texto con `inputmode="numeric"` (2.5, E-22, E-36, 5.5); aviso tras agotar la espera al guardar: E-55 nuevo, una fila en 5.5 y CA-08 |
| 10:54:37 | `22a6578` | — | Apartado 4 de `respuesta-evaluacion-spec04-01.md`: decisión y commit de cada fila |

### Aprobación de SPEC-04 (11:06)

Commit `0ef98be` (11:06:58). Seis ediciones: en la spec, el estado de la
cabecera, la fila de bloqueos, el apartado 9 y una fila de historial; en el
índice, la fila de SPEC-04 y la tabla de bloques. Tres de ellas llevan la
palabra que dispara el hook (el estado de la cabecera, la fila del índice y
la fila de historial). A las 11:06 el oráculo da por correctas sus tres
comprobaciones de specs: ningún fichero de código sin su bloque aprobado,
el estado de cada spec coincide con el índice y ninguna spec aprobada
depende de un supuesto sin decidir.

### Ensayo fuera del repositorio para el plan (11:08–11:29)

Todo en una carpeta temporal del sistema, fuera del repositorio. Node
24.18.0, npm 11.16.0, fecha de corte `2026-11-07T00:00:00Z` (la de la tabla
de ADR-001). **Nada del ensayo entra en el repositorio.**

**Las dos opciones de npm** (11:08 a 11:12 y 11:27):

| Prueba | `before=2026-11-07T00:00:00Z` | `min-release-age=7` |
|---|---|---|
| Un rango (`prettier@3`; sin ninguna opción resuelve a 3.10.1) | 3.9.10 | 3.9.10 |
| Una versión exacta posterior al corte (`prettier@3.10.0`) | Falla con `ETARGET`: «No matching version found … with a date before 7/11/2026, 1:00:00» | Falla con `ETARGET`, con el corte en «7/11/2026, 11:09:36»: siete días antes del momento de ejecutarlo |
| Una etiqueta (`@playwright/test@latest`) | 1.65.0, no la 1.65.1 | No probado |
| `typescript-eslint@8` (la 8.72.2 es del 2026-11-09) | 8.72.1 | 8.72.1 |
| `npm ci` con un fichero de bloqueo que trae una versión posterior al corte (3.10.1), con la opción en `.npmrc` | **La instala sin avisar** | **La instala sin avisar** |
| `npm install` sin argumentos, con ese mismo fichero de bloqueo | **La instala sin avisar** | **La instala sin avisar** |
| `npm install` sin fichero de bloqueo, con la 3.10.1 exacta en `package.json` | Falla con `ETARGET` | No probado |
| `npm exec` del CLI 21.2.30 (del 2026-11-12) | Falla con `ETARGET` | No probado |
| `npm ci` cuando `package.json` y el fichero de bloqueo no cuadran | Falla con `EUSAGE`, sin instalar (no depende de la opción) | — |

**El proyecto de ensayo** (11:13 a 11:29), creado con la orden del punto 2
del plan y desechable:

| Qué | Resultado |
|---|---|
| `ng new` con el CLI 21.2.29, resuelto con `before` | 23 ficheros. `package.json` con rangos (`^21.2.0`, `~7.8.0`…) y `"packageManager": "npm@11.16.0"`. **Todos los ficheros de texto, con CRLF** |
| `npm install` con `before` en `.npmrc`, sobre los rangos del CLI | Resuelve a las versiones de la tabla del paso 2: Angular 21.2.26, CLI y `@angular/build` 21.2.29, `rxjs` 7.8.2, `tslib` 2.9.1, `typescript` 5.9.3, `vitest` 4.1.12, `jsdom` 28.1.0, `prettier` 3.9.10 |
| Añadidos con versión exacta: `eslint` 10.14.0, `@eslint/js` 10.0.1, `angular-eslint` 21.4.0, `typescript-eslint` 8.72.1, `@vitest/coverage-v8` 4.1.12 y `@playwright/test` 1.65.0 | Instalan sin conflictos de dependencias entre sí. `@eslint/js` no lo trae ESLint 10 y hace falta para sus reglas recomendadas; su última versión es la 10.0.1, del 2026-02-06 |
| Fecha de publicación de **cada** entrada del fichero de bloqueo, consultada en el registro con un script de solo lectura | 652 versiones de 620 paquetes: **ninguna posterior al corte**. La más reciente, `tough-cookie` 6.1.0, del 2026-11-06 a las 17:26 UTC |
| Scripts de instalación | npm 11.16.0 no los ejecuta sin aprobarlos y avisa de cuatro pendientes (`esbuild`, `lmdb`, `msgpackr-extract` y `@parcel/watcher`). **Sin aprobar ninguno**, `ng build` y `ng test` funcionan |
| `ng build` (tal como lo genera el CLI) | Correcto: 214,34 kB iniciales. `tsconfig.json` trae `strict`, `strictTemplates` y `target` ES2022 |
| `ng test --no-watch` | 2 tests del CLI, correctos, con Vitest 4.1.12 y jsdom |
| Cobertura: una configuración `ci` del *target* `test` con `coverage`, `coverageInclude` de `src/app/**/*.ts` y `coverageThresholds` de 80 en líneas | Con ficheros sin test añadidos a propósito: «Coverage for lines (4%) does not meet global threshold (80%)» y código de salida 1. **Los ficheros que ningún test importa cuentan**, al 0 % |
| ESLint con `max-lines-per-function` 40, `max-params` 5, las reglas recomendadas y la de `OnPush` | Señala, con código de salida 1: una función de 42 líneas, una de 6 parámetros, un `any`, un import de `features/` desde `core/` y el componente que genera el CLI, que no es `OnPush` |
| La misma regla de 40 líneas en un `.spec.ts` | **Señala el `describe`**: once tests de tres líneas hacen una función de 45 |
| «Una feature no importa de otra» con `no-restricted-imports` | El primer patrón de la IA no lo detectaba (X-09). Con una expresión regular sí, y deja pasar `../../core/` y los imports de la propia carpeta; exige que las carpetas de `features/` no tengan subcarpetas |
| Finales de línea, con el `.gitattributes` del repositorio en un repositorio de ensayo | `git ls-files --eol` da 16 ficheros `w/crlf`, que es lo que el oráculo rechaza. `git checkout-index --force --all` no los cambia. `prettier --write` deja en LF todos los que sabe tratar; quedan `.editorconfig`, `.gitignore` y `README.md` |
| `npm audit` del árbol de ensayo | **27 avisos, todos moderados y todos en dependencias de desarrollo.** Salen de dos: `GHSA-g3hv-75wg-m249` (`minimatch` de 7.0.0 a 11.0.0, denegación de servicio; corregido en 11.0.1) y `GHSA-3g3m-2fjr-6pw4` (`glob` de 9.0.0 a 14.0.1; corregido en 14.0.2), publicados los dos el 2026-10-30. El árbol trae `minimatch` 10.2.6 y `glob` 13.0.7 porque ESLint 10.14.0, `typescript-eslint` 8.72.1 y el CLI 21.2.29 dependen de esas líneas. Lo que npm ofrece como arreglo: ESLint 10.15.0 (del 2026-11-13, **fuera del margen**); para `typescript-eslint`, ninguna versión de la línea 8 (la 8.72.2 sigue afectada); para el CLI, la línea 22 |

### Plan del frontend · propuesta de la IA, sin aprobar (11:30)

Es una propuesta: no se ha creado nada. Lo que el Tech Lead tiene que
decidir está reunido al final.

**1. El margen de una semana en npm.** Propuesta: **`before` con fecha
fija**, en un `frontend/.npmrc` versionado, junto con `save-exact=true`:

```
before=2026-11-07T00:00:00Z
save-exact=true
```

- *Por qué `before` y no `min-release-age`*: es el equivalente de
  `exclude-newer` de uv (ADR-007, opción A). La fecha queda escrita en el
  repositorio, resolver dos veces da lo mismo y adelantarla es un cambio
  que se ve en un diff, con su tabla de antes y después (regla 2).
  `min-release-age=7` cumple el margen pero es una ventana que se mueve: la
  misma orden da un árbol distinto según el día y no deja escrito con qué
  corte se resolvió.
- **Lo que ninguna de las dos hace**: revisar un fichero de bloqueo ya
  escrito. El margen actúa al resolver; después lo sostienen las versiones
  exactas de `package.json`, el `package-lock.json` versionado y que las
  instalaciones se hagan con `npm ci`, que falla si los dos no cuadran.
- Al crear el fichero de bloqueo, y cada vez que cambie, se comprueba la
  fecha de cada entrada contra el registro (el script de solo lectura del
  ensayo) y el resultado se anota en la bitácora. **El oráculo no lo
  comprueba**, y no se toca `scripts/`.
- Versiones exactas de las dependencias directas: las de la tabla del paso
  2, que son las que el ensayo ha resuelto. Nuevas, que el CLI no trae y
  piden aprobación: `eslint` 10.14.0, `@eslint/js` 10.0.1, `angular-eslint`
  21.4.0, `typescript-eslint` 8.72.1 y `@vitest/coverage-v8` 4.1.12; y
  `@playwright/test` 1.65.0 cuando llegue la fase de QA.
- No se aprueba ningún script de instalación: el ensayo compila y pasa los
  tests sin ellos.
- **Regla 3 de ADR-007**: los 27 avisos de `npm audit`. Recomendación:
  quedarse dentro del margen con ESLint 10.14.0 y dejarlos anotados. Son
  de gravedad moderada, afectan solo a herramientas de desarrollo que
  procesan los patrones de la configuración del propio proyecto y nada de
  eso llega al navegador; la excepción (ESLint 10.15.0, publicado ayer)
  quitaría una parte y dejaría los de `typescript-eslint` y el CLI. Se
  vuelve a mirar al adelantar la fecha. Decide el Tech Lead.
- Al aprobarse, ADR-007 y ADR-001 recogen el mecanismo y las versiones, en
  un commit de documentación anterior al del proyecto.

**2. La orden de creación**, desde la raíz del repositorio:

```
NG_CLI_ANALYTICS=false npm exec --before=2026-11-07T00:00:00Z --yes --package=@angular/cli@21.2.29 -- ng new frontend --skip-git --skip-install --package-manager=npm --style=css --ssr=false --zoneless --ai-config=none --interactive=false
```

| Opción | Por qué |
|---|---|
| `npm exec --before=… --package=@angular/cli@21.2.29` | Es el `npx @angular/cli@21.2.29` de ADR-001 con el margen aplicado también al propio CLI y a lo que arrastra. Probado: con la 21.2.30 falla |
| `NG_CLI_ANALYTICS=false` | El CLI no pregunta por la telemetría ni la envía |
| `--skip-git` | Ya hay repositorio; el CLI no crea otro ni hace un commit |
| `--skip-install` | El CLI escribe rangos e instalaría sin el margen. Antes se fijan las versiones y se añade `.npmrc` |
| `--style=css`, `--ssr=false` | Sin preprocesador ni renderizado en servidor: menos dependencias y nada que la spec pida |
| `--zoneless` | Es el valor por defecto del CLI 21 y encaja con `OnPush` y signals; se escribe para que conste |
| `--ai-config=none` | El CLI ofrece escribir ficheros de instrucciones para herramientas de IA; el repositorio ya tiene los suyos |
| `--interactive=false` | Ninguna pregunta: la orden da lo mismo cada vez |

Se dejan los valores por defecto del CLI: rutas, componentes *standalone*,
modo estricto, Vitest con jsdom, prefijo `app` y nombres de fichero del
estilo de 2025 (`app.ts`).

Qué se quita o se cambia de lo que genera, en el mismo commit:

| Fichero | Qué | Por qué |
|---|---|---|
| `.vscode/` (4 ficheros) | Se quita | El `.gitignore` de la raíz ya ignora `.vscode/`, y `mcp.json` lanza `npx -y @angular/cli mcp` sin versión fijada |
| `README.md` | Se quita | Texto del CLI en inglés; la documentación va en el `README.md` de la raíz |
| `.gitignore` | Se quita | Repite el de la raíz, que ya cubre `node_modules/`, `dist/`, `coverage/` y `.angular/` |
| `public/favicon.ico` y su enlace en `index.html` | Se quita | Es el logotipo de Angular: material de terceros |
| `src/app/app.html` | Se sustituye por la del armazón | Trae 344 líneas de página de bienvenida; el oráculo admite 120 |
| `src/app/app.spec.ts` | Se reescribe, y es el primer test en rojo | Prueba la página de bienvenida |
| `package.json` | Rangos por versiones exactas; scripts `lint` y `test:ci` | ADR-007 y el oráculo |
| `angular.json` | `cli.analytics` a `false`; configuración `ci` del *target* `test` | Telemetría y cobertura |
| `src/index.html` | `lang="es"` y el título | Textos en español |
| Todos | Pasan a LF: `prettier --write` y, para `.editorconfig`, la herramienta de edición | El CLI escribe CRLF en Windows y el oráculo lo rechaza |

Se añaden: `.npmrc`, `eslint.config.js` y, con el generador del CLI
(`ng generate environments`), los ficheros de entorno con la URL del
backend y la de la API de divisas (SPEC-04, 2.9). Después, `npm install`
una vez, para escribir `package-lock.json`, y la comprobación de fechas.

**3. Las comprobaciones del oráculo.** Las cuatro están inactivas solo
porque no existe `frontend/package.json`. En cuanto exista, el oráculo
ejecuta en `frontend/`, en cada pasada, `npm run lint`, `npm run build` y
`npm run test:ci`. Consecuencia: **el commit que crea `package.json` tiene
que traer ya los tres scripts y pasarlos**; el armazón no se puede partir
en «crear el proyecto» y «añadir ESLint» sin un oráculo en rojo entre los
dos. Sin `node_modules` (`npm ci`) las tres fallan: en rojo, no en
silencio.

| Comprobación | Script | Cómo se cumple |
|---|---|---|
| ESLint, con los límites de tamaño | `"lint": "eslint . --max-warnings 0"` | `eslint.config.js` con las reglas recomendadas de ESLint, `typescript-eslint` y `angular-eslint` (incluidas las de accesibilidad de plantillas) y, además: `max-lines-per-function` 40, `max-params` 5, `OnPush` obligatorio, plantilla dentro del `.ts` de 30 líneas como máximo (`component-max-inline-declarations`) y las fronteras entre `core/`, `shared/` y `features/`. El `any` lo señala la regla recomendada. Todo probado en el ensayo salvo la regla de la plantilla, que solo se ha visto que existe |
| Compilación en modo estricto | `"build": "ng build"` | El `tsconfig.json` del CLI, sin tocar: `strict` y `strictTemplates` |
| Tests con el 80 % de líneas | `"test:ci": "ng test --configuration ci"` | La configuración `ci` del ensayo. Cada pieza llega con sus tests (TDD), y el armazón, con los suyos: con la cobertura contando todo `src/app`, el primer test tiene que usar la configuración y las rutas de la aplicación o no llega al 80 % |
| Playwright: principio a fin y 375 px | `"e2e": "playwright test"` | Sigue inactiva mientras no se pase `--e2e` («fase de QA»). El script, `@playwright/test`, el navegador que descarga y `playwright.config.ts` entran en esa fase, no antes |

Lo que ya está activo y empieza a tener ficheros que mirar: las 250 líneas
por fichero y las 120 por plantilla `.html`, las reglas silenciadas sin
motivo, los tests saltados o en solitario, los CRLF y el control de specs
(abierto desde las 11:06).

Lo que el oráculo **no** comprueba del frontend: que cada test cite su
requisito (la comprobación de trazabilidad es solo del backend; se propone
citar `SPEC-04/E-nn` en el nombre de cada `describe` y que lo mire el
evaluador), que el dinero no pase por coma flotante y que las plantillas
no tengan lógica.

Al crear el armazón hay que poner al día el apartado «Qué comprueba hoy el
oráculo» de `CLAUDE.md`, que da por inactivos los límites de TypeScript.

**4. Las piezas, en orden.** Una tarea, un test en rojo visto antes, un
commit, con el oráculo en verde.

| # | Pieza | Dónde | Requisitos | Casos y criterios |
|---|---|---|---|---|
| 0 | Armazón: proyecto, configuración, cabecera con el nombre y el enlace al panel, página «no encontrada» | raíz de `frontend/`, `app` | E-34 | 2.1; CA-11 (se completa al llegar cada vista) |
| 1a | Medidas de texto: longitud en puntos de código, recorte solo de U+0020, *surrogate* suelto | `core/` | E-41, E-45 y la medida de E-50 | Filas de longitud y recorte de 5.4 y de 5.3 |
| 1b | Filtro del `id` de la ruta | `core/` | E-47 y la parte de forma de E-15 | 5.7; CA-17 |
| 1c | Formato: EUR solo con enteros, porcentajes, rótulos de tramo, fechas. Un único *pipe* de importes | `core/` y `shared/` | E-28 y el formato de E-29; 2.8 | 5.1 entera; CA-01 |
| 1d | Errores por su `code`: clasificación (`network_error`, `timeout`, `service_unavailable`, por `code`, inesperado) y reparto de un `422` por campos | `core/` | E-11, E-42, E-43 y el reparto de E-09 y E-48 | 5.6; CA-06 y CA-16 |
| 1e | Cliente de la API: clientes, proyección y simulaciones; tres estados, 10 s de espera, solo `GET` y `POST`, sin cabeceras propias, `q` y cuerpos como dice 4.3 | `core/` | E-32, E-33, E-51, E-52 y los cuerpos de E-46 y E-49 | 5.6 y las URL de 5.3 y 5.7; CA-10, CA-16 y CA-18 |
| 2 | `/meta`: una petición al arrancar, en memoria, nombres de país y plan, el código tal cual si falta, «Reintentar» | `core/` | E-39, E-35, E-40 y la fuente de E-05 | Filas de `/meta` de 5.3 y 5.5 |
| 3 | Panel y buscador | `features/panel` | E-01 a E-04, E-50, E-51, E-53, E-54 | 5.3 entera; CA-04 |
| 4 | Alta | `features/alta` | E-05 a E-10, E-41, E-44 a E-46 | 5.4 entera; CA-05 |
| 5 | Detalle | `features/detalle` | E-12 a E-15, E-47 | 5.7 y la lista de CA-07; CA-07 y CA-17 |
| 6 | Simulador, en EUR | `features/simulador` | E-17 a E-25, E-36 a E-38, E-48, E-49, E-55 | 5.5 menos sus dos filas de divisa, y 5.7; CA-08 y CA-17 |
| 7 | Divisas: servicio, selector en la cabecera y conversión para mostrar | `core/` y `app` | E-26, E-27, E-29, E-30, E-31 | 5.2 entera, la conversión de 5.1 y las filas de divisa de 5.5; CA-02, CA-03 y CA-09, y se cierra CA-08 |
| 8 | Cierre: los recorridos completos | tests | E-31, E-34, E-52 | CA-09, CA-11 y CA-18 |

E-06 y E-19 (nada de reglas de negocio en el navegador) no son una pieza:
los comprueba el evaluador al cerrar (CA-12). E-16, CA-13, CA-14 y CA-15
son de la fase de QA.

**5. La presentación.**

- Sin librería de UI, sin *framework* de CSS y sin preprocesador: CSS con
  propiedades personalizadas. Fuente del sistema y ningún icono ni recurso
  de terceros; solo tema claro.
- **Tres niveles.** (1) `src/styles.css` importa cuatro ficheros pequeños
  de `src/styles/`: las propiedades (colores, escala de espacios, radios,
  tamaños de letra, anillo de foco), la base (reinicio mínimo, tipografía,
  enlaces), los controles de formulario y botones, y nada más. (2) Los
  patrones que se repiten son componentes de `shared/` con su propio CSS:
  el bloque de estado (cargando, error con «Reintentar», vacío), el campo
  con su etiqueta y su error, y la tarjeta. (3) El `.css` de cada vista
  solo coloca: no define colores ni tamaños, usa las propiedades.
- ***Mobile-first***: lo que se escribe sin *media query* es la vista de
  375 px, en una columna. Un único punto de corte, `min-width: 48rem`,
  que da el ancho máximo del contenido y las dos columnas del detalle y
  del simulador. Medidas en `rem`, sin anchos fijos; los textos largos
  (un nombre de 200 caracteres, un email de 254) se parten con
  `overflow-wrap: anywhere`; listas de tarjetas en lugar de tablas;
  controles de al menos 44 px de alto y letra de 16 px en los campos.
- Accesibilidad: HTML semántico, un `h1` por vista, etiquetas, errores
  enlazados a su campo, avisos en regiones vivas, foco visible y respeto
  de `prefers-reduced-motion`.
- El presupuesto de estilos por componente del CLI (aviso a 4 kB, error a
  8 kB) se deja como está.

**6. Las tres paradas.**

| Parada | Después de | Qué revisa el Tech Lead |
|---|---|---|
| 1 | Las piezas 0 a 3: armazón, lo común de `core/`, `/meta` y el panel | La configuración entera (versiones, fichero de bloqueo, reglas de ESLint), la estructura y las funciones puras con sus tablas de casos. **Aquí abre la aplicación en el navegador por primera vez**, con el backend real |
| 2 | Las piezas 4 a 6: alta, detalle y simulador en EUR | El flujo completo, de dar de alta un cliente a ver su simulación guardada |
| 3 | Las piezas 7 y 8: divisas y cierre | El selector de divisa con la API pública real y el frontend completo, antes de la fase de QA (Playwright, evaluador y README) |

*Por qué el navegador en la parada 1 y no antes ni después*: el panel es
la primera vista que habla con el backend, así que es el primer momento en
que el navegador enseña lo que ningún test dice (el CORS real, `/meta`
real, el aspecto a 375 px). Y corregir la base visual cuesta entonces una
vista, no cuatro.

**7. Lo que no se puede comprobar hasta tener Playwright.**

- **El desplazamiento horizontal a 375 px** (E-16, CA-13): jsdom no
  calcula la disposición de la página.
- **El recorrido de principio a fin contra el backend real** (CA-14) y,
  con él, **el CORS de verdad** (E-52): que la comprobación previa pasa
  con las cabeceras que ponen el navegador y Angular. Los tests usan las
  utilidades de `HttpClient` y no envían nada.
- **El formato de `Intl` en un navegador**: los tests corren en Node, que
  comparte motor de JavaScript con Chromium pero no tiene por qué llevar
  los mismos datos de idioma. Firefox y Safari no se comprueban ni con
  Playwright si solo se instala Chromium.
- **La fila de 5.5 de la fecha del tipo con un desfase horario negativo**:
  Playwright puede fijar la zona horaria; al evaluador no le funcionó
  cambiarla con Node en Windows y la IA no lo ha intentado.
- Lo que hace un campo real con un texto pegado muy largo o con un
  *surrogate* suelto, la navegación con teclado y el foco, la carga
  diferida de las rutas en la compilación real, y los tiempos reales
  (300 ms, 200 ms, 10 s): los tests usan temporizadores simulados.
- **Ni con Playwright**: el teclado numérico de `inputmode="numeric"` (solo
  en un móvil real), el contraste y la llamada real a la API de divisas
  desde el navegador, que una prueba repetible no debe hacer. Eso lo ve el
  Tech Lead a mano en las paradas.

Hasta entonces, lo que se vea a mano en el navegador en las paradas es una
comprobación manual y se anota como tal.

**Lo que decide el Tech Lead con el plan:**

| # | Decisión | Recomendación de la IA |
|---|---|---|
| P-01 | Mecanismo del margen en npm | `before` con fecha fija en `frontend/.npmrc`, con `save-exact=true` |
| P-02 | Dependencias nuevas: `eslint` 10.14.0, `@eslint/js` 10.0.1, `angular-eslint` 21.4.0, `typescript-eslint` 8.72.1, `@vitest/coverage-v8` 4.1.12; `@playwright/test` 1.65.0 en la fase de QA | Aprobarlas |
| P-03 | Los 27 avisos moderados de `npm audit` (regla 3 de ADR-007) | Quedarse dentro del margen y anotarlos; alternativa, la excepción para ESLint 10.15.0, que quita solo una parte |
| P-04 | Lo que se quita de lo que genera el CLI (tabla del punto 2) | Como está en la tabla |
| P-05 | Los generadores del CLI (`ng new`, `ng generate`), `npm install` y `prettier --write` escriben en `frontend/` desde la terminal; `CLAUDE.md` pide las herramientas de edición | Admitir esos cuatro y nada más: son generadores y un formateador, como `ruff format` en el backend |
| P-06 | La regla de 40 líneas por función señala el `describe` de un `.spec.ts` | Desactivar en los `.spec.ts` solo esa regla, con su motivo escrito en la configuración y en `CLAUDE.md`; los 5 parámetros siguen. Alternativa: partir cada `describe` |
| P-07 | Comprobar el formato con `prettier --check` dentro de `npm run lint` | Sí: es el equivalente de `ruff format --check` y además detecta un CRLF. La comprobación del oráculo haría entonces más de lo que dice su nombre |
| P-08 | Carpetas de `features/` sin subcarpetas, para que ESLint pueda comprobar que una feature no importa de otra | Sí |
| P-09 | El lugar de las tres paradas y de la primera apertura en el navegador | Como en el punto 6 |

Precisiones de la IA sobre la segunda parte de la sesión, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| X-01 | **`015` es válido en el simulador y vale 15** (2.5 y una fila de 5.5). Lo decidió la IA al redactar «solo dígitos ASCII»; el Tech Lead dijo que decide el texto y no habló de los ceros a la izquierda. El `id` de la ruta sí los rechaza | Es una regla que la IA ha puesto, no una que se le haya dictado |
| X-02 | En 5.5 la IA añadió como textos no válidos `+15` y `1 5` en usuarios, y `2.0` y `1e2` en almacenamiento | Salen de la misma regla, pero no estaban en la propuesta decidida |
| X-03 | C-05: la spec no fija el texto literal del aviso, solo lo que dice y lo que ofrece. El requisito nuevo es E-55 | El texto lo fijará la implementación |
| X-04 | La respuesta a H-06 decía que habría que tocar CA-17 y no hizo falta: remite a las filas de 5.7, que sí cambiaron. Consta en el apartado 4 de la respuesta | La propuesta y lo hecho no coinciden en eso |
| X-05 | La IA no ve el diálogo del hook. Entre el commit anterior (10:54:37) y el oráculo de la aprobación (11:06:42) pasaron doce minutos y las ediciones se aplicaron; no puede afirmar más | La confirmación la da el Tech Lead y solo él sabe qué vio |
| X-06 | **El ensayo fue más allá de lo que pedía el punto 1.** El encargo pedía probar las dos opciones de npm en una carpeta temporal; la IA, además, creó allí un proyecto desechable con `ng new`, lo instaló, lo compiló y probó ESLint y la cobertura, para dar la orden del punto 2 y los umbrales del punto 3 con evidencia y no de leer plantillas. En el repositorio no se ha creado nada | El encargo decía «sin crear el proyecto»; que un ensayo fuera del repositorio lo respeta es la lectura de la IA |
| X-07 | A las 11:12 una orden de la IA fue denegada: borraba carpetas del ensayo con `rm -rf` y escribía un `.npmrc` con una redirección. La rehízo con una carpeta por caso y la herramienta de escritura, sin borrar nada | Una denegación es una corrección |
| X-08 | De `min-release-age` no se probaron la etiqueta, `npm exec` ni el árbol completo | La propuesta es `before`; la comparación no es simétrica |
| X-09 | El primer patrón de ESLint de la IA para «una feature no importa de otra» no detectaba el caso. Corregido en el ensayo con una expresión regular | Sin el caso de prueba habría llegado al plan una regla que no comprueba nada |
| X-10 | Los avisos de seguridad no se han leído enteros: título, rango afectado, gravedad y fecha, de `npm audit` y de la base de avisos de GitHub | Para decidir P-03 puede hacer falta leerlos |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git rev-parse --short HEAD` (09:24) | Limpio, `58da604` |
| Contrato real del backend | Script fuera del repositorio, con el cliente de test y una base de datos en la carpeta temporal: `/openapi.json` y las sondas de los ocho puntos del encargo (09:29 y 09:35) | Seis operaciones de negocio con los campos de las specs; resultados, en la tabla del paso 1 |
| Comportamiento de JavaScript | `node -e`, con Node 24.18.0 (09:29, 09:55 y 10:17) | Un *surrogate* suelto sale de `JSON.stringify` como escape y hace fallar `encodeURIComponent`; `Number('01')` vale 1; por encima de 2^53 − 1 se redondea; la expresión regular en modo Unicode distingue un *surrogate* suelto de un emoji |
| API de divisas | `curl` con la cabecera `Origin`, a la `v2`, a su comprobación previa, a una divisa inexistente y a la `v1` (09:29:55) | `200`, lista de tres objetos y `access-control-allow-origin: *`; tabla del paso 2 |
| Versiones y fechas de npm | Script de solo lectura contra el registro (09:30 a 09:33) | Tabla del paso 2 |
| Paquetes publicados de Angular | Descargados a la carpeta temporal y leídos, sin instalar (09:31 y 09:34): plantillas del CLI 21.2.29, `@angular/forms` y `@angular/common` 21.2.26 | Rangos que escribe el CLI, runner por defecto, *target* ES2022, expresión del validador de email y codificación de los parámetros de consulta |
| Oráculo antes de cada commit | `uv run scripts/check.py`, 11 veces entre las 09:40 y las 10:22 | Siempre código de salida 0: 20 correctas, 0 con fallo y 4 inactivas (las del frontend) |
| Caracteres invisibles en SPEC-04 | Recorrido del fichero con Python (09:46) | Ninguno. Solo dos caracteres fuera de lo corriente, los dos a propósito y visibles: U+1D538 y U+0661 |
| Numeración de SPEC-04 | Recuento con `grep` (09:52) | 52 requisitos, de E-01 a E-52, sin repetidos; 18 criterios |
| Que el evaluador no tocó nada | `git status --short`, `git rev-parse --short HEAD`, `git stash list` y `ls backend/data` (10:13) | Vacío, `8516f5c`, ningún `stash` y la carpeta no existe |
| Informe, intacto | Comparación con el mensaje del registro del subagente (10:15) | 184 líneas y 15.150 caracteres; ninguna línea distinta |
| Los doce hallazgos | Cliente de test, Node y lectura del paquete de Angular (10:17 y 10:18) | Se reproducen todos; tabla del apartado 2 de la respuesta |
| Oráculo antes de cada commit de la segunda parte | `uv run scripts/check.py`, antes de los nueve commits de las 10:37 a las 11:06 y antes del cierre | Siempre código de salida 0: 20 correctas, 0 con fallo y 4 inactivas |
| Numeración de SPEC-04 tras las correcciones | Recuento con `grep` (11:28) | 55 requisitos, de E-01 a E-55; 18 criterios |
| Control de specs tras la aprobación | Las tres comprobaciones de specs del oráculo (11:06) | Correctas |
| Cómo ejecuta el oráculo las comprobaciones del frontend | Lectura de `scripts/oracle/checks_stack.py`, `checks_code.py`, `checks_trace.py` y `repo.py` (11:07) | Tres scripts de npm en cuanto existe `frontend/package.json`; el cuarto, solo con `--e2e` |
| Las dos opciones de npm | Ensayo en una carpeta temporal fuera del repositorio (11:08 a 11:12 y 11:27) | Tabla del apartado 3 |
| La orden de creación, la instalación, la compilación, los tests, la cobertura, ESLint y los finales de línea | Proyecto de ensayo en la misma carpeta temporal (11:13 a 11:24) | Tabla del apartado 3 |
| Fechas de publicación del árbol entero | Script de solo lectura contra el registro de npm, sobre el fichero de bloqueo del ensayo (11:17 y 11:21) | 652 versiones, ninguna posterior al corte |
| Avisos de seguridad del árbol de ensayo | `npm audit` y la base de avisos de GitHub (11:28 y 11:29) | 27 moderados, de dos avisos de origen, todos en dependencias de desarrollo |
| Que el ensayo no tocó el repositorio | `git status --short` y `ls frontend` (11:28) | Solo esta bitácora modificada; `frontend/` no existe |

## 5. No verificado

Actualizado a las 11:30, al cerrar la segunda parte. Lo que el cierre de las
10:22 daba por no verificado y ya lo está se dice en cada punto.

- **Nada del frontend en el repositorio**: no existe. Desde las 11:13 hay
  un proyecto de ensayo, desechable y fuera del repositorio, que compila y
  pasa los dos tests que trae el CLI con Node 24.18.0; no tiene ni una
  línea de la aplicación. Lo que SPEC-04 dice de Angular sigue saliendo de
  leer sus paquetes publicados.
- **Del plan, sin probar**: `ng serve`; `ng generate environments`; quitar
  `public/` y que la compilación siga funcionando; la regla de ESLint de
  la plantilla dentro del `.ts`; `prettier --check` sobre el proyecto
  entero; todo lo de Playwright; y cualquier cosa fuera de Windows (en
  macOS y Linux el CLI no debería escribir CRLF, y no se ha visto).
- **Las opciones de npm**: probadas hoy. De `min-release-age` faltan tres
  casos (X-08). Que `npm ci` se use siempre para instalar es una
  disciplina: nada lo obliga.
- **Los avisos de seguridad**: `npm audit` sobre el árbol de ensayo, que
  lleva también Playwright. No se han leído enteros (X-10), y no se ha
  probado forzar las versiones corregidas de `minimatch` y `glob`.
- **Las correcciones aplicadas a SPEC-04** no han pasado por el evaluador:
  el Tech Lead dijo que no hacía falta pedirle nada más. Las de H-01 y
  H-12 siguen probadas solo como fragmentos sueltos, con Node.
- **Nada en un navegador real**: ni la llamada a la API de divisas, ni CORS
  contra el backend, ni cómo trata un campo de texto un *surrogate* suelto
  o un texto muy largo. Lo de JavaScript está visto con Node 24.
- Nada con un servidor real (`uvicorn`): las sondas de hoy son con el
  cliente de test. Que N-01 responde `405` con un servidor real lo afirma
  el Tech Lead en el encargo; la IA no lo ha visto.
- La API de divisas en festivos, su límite de peticiones y que los tres
  tipos traigan siempre la misma fecha. En fin de semana, solo se ha visto
  este sábado.
- Lo que declaran las bibliotecas de tipos de TypeScript sobre
  `Intl.NumberFormat` (H-01): lo afirma el evaluador; la IA no lo ha leído.
- La fila de 5.5 de la fecha del tipo con un desfase horario negativo: ni
  el evaluador ni la IA la han comprobado.
- E-42 y E-43 no tienen veredicto independiente: el informe no les da fila
  (U-01). El Tech Lead lo da por bueno con CA-16 (A-02).
- Lo que hizo el hook: la IA no ve su diálogo. Hasta la aprobación evitó
  escribir la palabra que lo dispara; en la aprobación la escribió en tres
  ediciones, y se aplicaron (X-05).
- Nada fuera de Windows.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Decidir cada hallazgo de la evaluación de SPEC-04 y las propuestas C-01 a C-05, admitir S-01 a S-09 y aprobar SPEC-04~~ | Hecho por el Tech Lead a las 10:34 y a las 11:06 |
| **Aprobar o cambiar el plan del frontend** (apartado 3): las decisiones P-01 a P-09. Las que más pesan: P-01 (mecanismo del margen en npm), P-03 (los 27 avisos de `npm audit` y la regla 3 de ADR-007), P-05 (qué puede escribir en `frontend/` desde la terminal) y P-06 (la regla de 40 líneas en los `.spec.ts`) | A decidir por el Tech Lead, **antes de crear nada** |
| Aprobar o cambiar las precisiones U-01 a U-05 y X-01 a X-10. La que más pesa es X-01 (`015` válido en el simulador): si no vale, cambia SPEC-04, que ya está aprobada | A decidir por el Tech Lead |
| Llevar a ADR-007 y a ADR-001 el mecanismo de npm y las versiones exactas, y poner al día en `CLAUDE.md` «Qué comprueba hoy el oráculo» | Con el plan aprobado; lo primero, en commit de documentación; lo segundo, con el armazón |
| El oráculo no comprueba las fechas del fichero de bloqueo de npm ni la trazabilidad de los tests del frontend. Cambiarlo es tocar `scripts/` | A decidir por el Tech Lead |
| La carpeta temporal del ensayo sigue en disco, fuera del repositorio; la IA no borra nada | Se puede borrar a mano; el sistema la limpia sola |
| Pendientes heredados que esta sesión no toca: documentar en el README que `/docs` carga recursos de un servidor externo, llevar las limitaciones al README, el límite de tamaño del cuerpo en el proxy inverso (L-01), `app/domain/customers.py` en 234 líneas de 250 (R-15), la base de datos creada antes de `9ec6866` (P-03) y documentar la estructura del backend en `02-arquitectura/README.md` | A decidir por el Tech Lead |
