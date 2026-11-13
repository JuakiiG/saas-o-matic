# Sesión 05 · Correcciones de la evaluación independiente del backend

| | |
|---|---|
| **Fecha** | 2026-11-13 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | El Tech Lead decidió los hallazgos de la evaluación independiente del backend (H-01 a H-14 y A-01; H-15 quedó sin nombrar) y la IA los aplicó, uno o un grupo por commit y con el oráculo en verde antes de cada uno. **Corregidos en el código**: un `id` de ruta de miles de dígitos (`422`), un surrogate suelto en el cuerpo (`400`, una sola regla en el guarda), el cuerpo como UTF-8 estricto, un `q` con U+0000 (lista vacía, decidido en el dominio y sin condición en el SQL), el email con cualquier separador Unicode, `/redoc` y `/docs/oauth2-redirect` desactivadas y un tipo concreto en lugar de `Any`. **Solo specs, tests o documentación**: la regla del parámetro de consulta desconocido (H-03), CORS (H-10), los comentarios de los tests escritos después del código (H-13), la prueba de las sentencias (H-14) y las limitaciones L-04 (ampliada) y L-05 (nueva: H-04 no se implementa). El informe de la primera evaluación recupera su U+00A0 y la respuesta lleva la decisión y el commit de cada fila y la tabla de sondas de antes y después. 731 tests del backend (eran 639), `domain/` al 100 %, 92 de 92 ramas y oráculo en verde con 20 comprobaciones activas y 4 inactivas. **Segunda pasada del evaluador** (Opus 5.5, comprobado en su registro), en solo lectura: 12 hallazgos corregidos, 3 conformes a lo decidido y 1 sin veredicto posible (H-13); ninguna regresión; **tres hallazgos nuevos sin corregir**: N-01 (medio: un método no admitido sobre `/docs` o `/openapi.json` responde `500`; ya ocurría antes de esta sesión), N-02 y N-03 (bajos). Tres requisitos siguen en `NO CUMPLE` por las limitaciones aceptadas L-04 y L-05. Quedan sin aprobar las precisiones R-01 a R-23 y V-08 a V-11. Sesión parada: el Tech Lead decide N-01 a N-03, H-15 y las precisiones. **Añadido a las 20:25**: el Tech Lead revisó las correcciones y la segunda pasada a las 20:06; admitió R-01 a R-23 y dice haber comprobado las sondas con un servidor real, sin regresiones. Decidió los hallazgos nuevos y la IA los aplicó, uno por commit: **N-01 corregido** (un método no admitido sobre `/docs` o `/openapi.json` responde `405` con `Allow: GET, HEAD`, con las seis filas vistas en rojo antes), **N-02** (ningún `Any` sin comentario en su línea, comprobado con una búsqueda), **N-03** (las specs citan L-04 y L-05, y SPEC-03 5.7 gana seis filas), **H-15** (L-01 se mantiene, con la medida y el cierre previsto en el proxy inverso) y una fila con su test para un `q` que solo lleva una marca diacrítica. Respuesta en `04-calidad/respuesta-evaluacion-backend-02.md`. 741 tests del backend, `domain/` al 100 %, 96 de 96 ramas y oráculo en verde con 20 comprobaciones activas y 4 inactivas. **No hay tercera pasada del evaluador**, por decisión del Tech Lead: estas cinco correcciones no tienen comprobación independiente ni prueba con servidor real. Tres requisitos siguen en `NO CUMPLE` en sus casos límite por L-04 y L-05, que ahora las specs citan. Quedan sin aprobar V-08 a V-11 y R-24 a R-30. Sesión parada |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 05: correcciones de la evaluación independiente del backend. Leer
> antes `CLAUDE.md`, `.claude/rules/backend.md`, el índice de specs,
> `04-calidad/evaluacion-backend-01.md`,
> `04-calidad/respuesta-evaluacion-backend-01.md` y los apartados 5 y 6 de
> `03-proceso/sesion-04.md`. Abrir esta bitácora con el formato de la 04.
>
> Admitidas B-01 a B-04 y V-04 a V-07. El Tech Lead decide cada hallazgo
> (tabla del apartado 3).
>
> El informe: en H-08, línea 255, el ejemplo del evaluador llevaba un U+00A0
> entre la `a` y la `b` y se guardó como espacio corriente; es la única
> diferencia con su mensaje. Restaurarlo y comprobar que el fichero tiene
> exactamente un U+00A0. Si la herramienta de edición no lo conserva, con un
> script de una línea y declarándolo: excepción a n4 solo para ese carácter.
> Commit propio. Corregir el apartado 3 de la respuesta: comprobado en el
> registro del subagente que era el evaluador y que respondió con Opus 5.5.
>
> Cómo: rojo visto antes del código en cada corrección; un commit por
> hallazgo o por grupo; oráculo en verde en cada uno. Rellenar el apartado 4
> de la respuesta con la decisión y el commit de cada fila.
>
> Al terminar, repetir las sondas del apartado 2 de la respuesta y añadir la
> tabla de antes y después. Después, lanzar otra vez el evaluador, en solo
> lectura y con las mismas restricciones, solo para comprobar que cada
> hallazgo corregido lo está de verdad y buscar regresiones. Informe intacto
> en `04-calidad/evaluacion-backend-02.md`, con commit propio. Cerrar la
> bitácora de la sesión 05 y **parar**.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 18:43 | — | Lectura de `CLAUDE.md`, `.claude/rules/backend.md`, el índice de specs, el informe, la respuesta, los apartados 5 y 6 de la sesión 04 (y la cabecera, la cronología y las tablas de la revisión del backend, para el formato), `04-calidad/limitaciones-conocidas.md`, los apartados de SPEC-01 que cambian y el código afectado de `backend/app/`. `git status` limpio, `HEAD` en `68ae670` |
| 18:46 | — | Registro del subagente evaluador de la sesión 04, leído por la IA con un script de solo lectura fuera del repositorio (apartado 3). Apertura de esta bitácora |
| 19:30 | `e71196f` a `eb0a27f` | Fila escrita a las 19:43; el detalle y las horas de cada paso están en las tablas del apartado 3, escritas en su momento. Informe con su U+00A0: `e71196f` (18:48:52 según `git log`). Apartado 3 de la respuesta: `ca85f85` (18:50:19). H-01: `33eeb83` (18:52:39). H-02 y A-01: `1b7fdd9` (18:56:47). H-07: `1e0f839` (18:59:47). H-04: `b345bc7` (19:01:28). H-03: `2e0913f` (19:03:20). H-05 y H-11: `758b880` (19:07:06). H-06: `c223520` (19:08:30). H-08: `861c6ca` (19:11:25). H-09: `a52cae5` (19:13:51). H-10: `b5411f8` (19:16:16). H-12: `b579de3` (19:19:29). H-13: `e8194d3` (19:22:20). H-14: `edbbb08` (19:24:59). Respuesta con el apartado 4 y las sondas: `5e9c7ef` (19:28:16; sustituye por enmienda a `cff0c0a`). Bitácora hasta ahí: `eb0a27f` (19:30:16). Oráculo en verde antes de cada uno |
| 19:31–19:39 | — | Segunda pasada del evaluador, en solo lectura, sobre `eb0a27f`. La IA no tocó el repositorio mientras trabajaba |
| 19:41 | `99aeec2` | Informe guardado intacto en `04-calidad/evaluacion-backend-02.md` y commit propio (19:41:49 según `git log`). Oráculo en verde antes |
| 19:43 | *(este commit)* | Comprobados por la IA los tres hallazgos nuevos, sin corregir ninguno (apartado 3). Cierre de esta bitácora. **La IA para aquí**: N-01, N-02 y N-03 esperan la decisión del Tech Lead |
| 20:06 | — | El cierre anterior es `99e01a7` (19:45:28 según `git log`). El Tech Lead revisa las correcciones y la segunda pasada: admite R-01 a R-23 y decide N-01, N-02, N-03, H-15 y un caso sin fila (apartado 3). Anotado en esta bitácora antes de empezar |
| 20:25 | `b5c468d` a `68ef17f` y *(este commit)* | Fila escrita a las 20:25; el detalle y las horas están en la tabla «Correcciones tras la revisión» del apartado 3. N-01: `b5c468d` (20:10:17). N-02: `7cc5858` (20:13:11). N-03: `040eba3` (20:15:43). H-15: `aef612a` (20:18:24). `q` con solo U+0301: `bd7d269` (20:22:13). Respuesta a la segunda pasada: `68ef17f` (20:24:58). Oráculo en verde antes de cada uno. Este commit solo cierra la bitácora. **La IA para aquí**; no hay tercera pasada del evaluador, por decisión del Tech Lead |
| 20:28 | *(este commit, enmendado)* | **Enmienda** (norma n3): el cierre se hizo como `5777b9a` (20:27:43 según `git log`), era el último commit y no hay nada subido. La fila «Resultado» decía «bloque backend cerrado; lo siguiente es aprobar SPEC-04», una conclusión de la IA que el Tech Lead no ha dicho. Quitada; el resto no cambia |

## 3. Revisiones y decisiones del Tech Lead

### Decisión de cada hallazgo (18:42, en el encargo)

Admitidas B-01 a B-04 y V-04 a V-07 (precisiones de la sesión 04).

La columna «Frente a la propuesta de la IA» compara con
`04-calidad/respuesta-evaluacion-backend-01.md`, apartado 1.

| Hallazgo | Decisión del Tech Lead | Frente a la propuesta de la IA |
|---|---|---|
| H-01 | Un entero bien escrito en la ruta, por largo que sea, responde `422` con `out_of_range`. Tests con 4301 y 20000 dígitos, y con signo negativo. Fila en SPEC-01 5.10, con historial | Aprobada; añade los 20000 dígitos y el signo negativo |
| H-02 y A-01 | **Una sola regla, en el guarda**: un cuerpo con un surrogate suelto, en un valor o en un nombre de campo, responde `400` `malformed_request`. Por qué: A-01 afecta a los tres `POST` (también a `/simulations`) y en los endpoints con modelo falla en otro punto que en el alta, así que la regla por campo exigiría tres arreglos; RFC 8259 §8.2 dice que ese texto no representa caracteres Unicode. Se escribe en la fila del `400` del índice, con historial. Tests en los tres `POST`, con el surrogate en un valor y en una clave; un emoji válido sigue dando `201` | **Cambiada.** La IA recomendaba `invalid_characters` por campo en `company_name` y `contact_email`, y daba el `400` en el guarda como alternativa. No vale porque deja fuera A-01 y obliga a tres arreglos |
| H-03 | La opción recomendada: la regla se escribe en «Errores de validación» del índice. Sin cambio de código | Aprobada |
| H-04 | **No se implementa. Limitación conocida L-05**: un entero JSON de más de 4300 dígitos se trata como cuerpo mal formado. Por qué: ese límite es una protección de Python contra denegación de servicio, y cambiarlo obliga a sustituir la lectura del cuerpo que hace FastAPI. Un test fija 4300 dígitos en `422` y 4301 en `400`, anotado como escrito después del código | **Rechazada.** La IA proponía leer los enteros de forma que uno desmesurado llegara a la validación; la limitación era su alternativa |
| H-05 y H-11 | Juntos: un `q` con U+0000 devuelve la lista vacía, sin cambio en el contrato. Por qué: ningún nombre ni identificador guardado puede contenerlo, así que no coincide con nada; hoy SQLite corta el patrón. La decisión la toma el dominio, y con ella sale del SQL la condición `? <> ''`. Filas en SPEC-01 5.9 (`%00`, `a%00` y `%00a`), con historial | **H-05, cambiada**: la IA recomendaba un `422` con `invalid_characters` en `q` para las categorías `Cc` y `Cf`; se elige su alternativa sin tocar el contrato. H-11, aprobada |
| H-06 | Se mantiene L-04; se amplía su texto con la consecuencia | Aprobada |
| H-07 | El cuerpo se lee como UTF-8 estricto: UTF-16 y UTF-32, con BOM o sin él, y UTF-8 con BOM responden `400`. Frase en el índice, con historial | Aprobada |
| H-08 | **La alternativa estricta**: un email con cualquier separador Unicode (categorías `Zs`, `Zl` y `Zp`) responde `invalid_email`. Por qué: un espacio de no separación llega al copiar y pegar un correo, y guardado así no sirve. SPEC-01 2.1 y filas en 5.7, con historial | **Cambiada.** La IA recomendaba solo escribir en la spec que «espacio» es U+0020 |
| H-09 | Se conservan `/docs` y `/openapi.json`; se desactivan `/redoc` y `/docs/oauth2-redirect`, que pasan a `404` `not_found`. Por qué: quien revise la prueba abrirá `/docs`; `/redoc` lo duplica y no hay OAuth. El índice dice que `/docs` y `/openapi.json` existen, que no son endpoints de negocio y que no aplican la regla del parámetro desconocido. Se apunta para el README que `/docs` carga recursos de un servidor externo | **Cambiada.** La IA recomendaba desactivar también `/docs`; conservarlo era su alternativa |
| H-10 | De acuerdo | Aprobada |
| H-12 | De acuerdo, con un tipo concreto para la fila. Se anota en `CLAUDE.md` que el oráculo no comprueba esa regla; no se toca `scripts/` | Aprobada, eligiendo el tipo concreto y no el comentario |
| H-13 | De acuerdo: el mismo comentario en los demás tests escritos después del código | Aprobada |
| H-14 | De acuerdo | Aprobada |
| H-15 | **El encargo no lo nombra.** La IA no hace nada con él: sigue como L-01, sin la medida que proponía añadir | Sin decisión |

### El registro del subagente evaluador (18:45)

El Tech Lead dice haber comprobado en el registro del subagente que era el
evaluador y que respondió con Opus 5.5, y que la única diferencia entre su
mensaje y el informe guardado es el U+00A0 de la línea 255.

La IA lo ha comprobado también, con un script de solo lectura fuera del
repositorio que lee el registro de la sesión 04 (carpeta de registros de
Claude Code, fuera del repo):

| Qué | Resultado |
|---|---|
| Tipo de agente (fichero de metadatos del subagente) | `evaluador` |
| Instrucciones de sistema de la petición | El texto de `.claude/agents/evaluador.md` |
| Modelo de cada respuesta | `claude-opus-5-5` en las 60 respuestas del registro |
| Mensaje del informe frente al fichero guardado | 302 líneas los dos y 23.096 caracteres los dos. **Una sola línea distinta, la 255**: el mensaje lleva un U+00A0 entre la `a` y la `b`; el fichero, un U+0020. El mensaje tiene exactamente un U+00A0 |

Un dato que la IA no sabe interpretar: el fichero de metadatos trae además
un campo `pickedEffortModel` con el valor `claude-fable-5-2`. El modelo que
consta en cada respuesta es `claude-opus-5-5`.

### El informe y el apartado 3 de la respuesta (18:47–18:50)

| Hora | Qué |
|---|---|
| 18:47 | **La herramienta de edición no conserva el U+00A0.** La IA lo intentó con `Edit`: el carácter que escribe la IA llega como un espacio corriente, la herramienta respondió que el texto nuevo era igual al viejo y el fichero no cambió (comprobado: seguía con cero U+00A0). **Excepción a n4, declarada, solo para ese carácter**: una orden de una línea de Python (`python -c`) que sustituye en la línea 255 el U+0020 que hay entre la `a` y la `b` por U+00A0, tras comprobar que el texto a sustituir aparece una sola vez. Resultado: el fichero tiene **exactamente un U+00A0**, el diff es de una línea y, comparado otra vez con el mensaje del registro, **ninguna línea es distinta** |
| 18:48 | Oráculo en verde (20 correctas, 0 con fallo, 4 inactivas). Commit propio del informe: `e71196f` (18:48:52 según `git log`) |
| 18:50 | Apartado 3 de la respuesta corregido: las dos frases que decían «la IA no puede asegurar» y «no tiene otra forma de comprobar» quedan tachadas, con lo comprobado al lado. Oráculo en verde. Commit `ca85f85` (18:50:19) |

### Correcciones (desde las 18:50)

Orden de cada una: la spec, el test, el test ejecutado y su rojo a la vista,
el código, el verde y el oráculo. Cada commit, con el oráculo en verde
(20 correctas, 0 con fallo, 4 inactivas) justo antes.

| Hora | Hallazgo | Rojo visto antes del código | Qué se hizo | Verde, oráculo y commit |
|---|---|---|---|---|
| 18:52 | H-01 | 18:50: **3 en rojo por aserción** (`assert 500 == 422`; en el log, `UntranslatedValidationError: id: int_parsing_size`): 4301 nueves, 20000 nueves y signo menos con 4301 nueves. La fila de 4300 nueves, añadida como frontera, ya pasaba | SPEC-01 5.10: tres filas, una nota y el historial. `app/api/validation.py`: el tipo de error `int_parsing_size` se traduce a `out_of_range` | `49 passed` en el fichero; oráculo en verde a las 18:52. Commit `33eeb83` (18:52:39) |
| 18:56 | H-02 y A-01 | 18:53: **11 en rojo por aserción**: `500 == 400` en el nombre y el email del alta y en un nombre de campo con surrogate de los tres `POST`; `422 == 400` en un valor de `/pricing/quote` y de `/simulations` (hoy `not_an_integer`) y en los casos anidados. **Los 4 del emoji pasaron**: fijan lo que «sigue» valiendo y no pueden estar en rojo. En su lugar, **mutación a las 18:55**: con un guarda que rechaza todo lo que no es ASCII fallan los 4; deshecha | Índice de specs: fila del `400`, párrafo «El texto del cuerpo» e historial. `app/api/request_guard.py`: tras leer el JSON, el guarda comprueba que todo el texto leído puede escribirse en UTF-8. Fichero de tests nuevo, `tests/integration/test_body_text.py`, contra los tres `POST` reales, comprobando además que no se guarda nada | `15 passed` en el fichero; oráculo en verde a las 18:56. Commit `1b7fdd9` (18:56:47) |
| 18:59 | H-07 | 18:57: **22 en rojo por aserción** (`200 == 400` y `201 == 400`): los tres `POST` con siete codificaciones (UTF-16 y UTF-32 con BOM, sin él en los dos órdenes de bytes, y UTF-8 con BOM) y un cuerpo en UTF-16 cuyo `Content-Type` lo declara | Índice de specs: fila del `400`, primera frase de «El texto del cuerpo» e historial. `app/api/request_guard.py`: el guarda decodifica el cuerpo como UTF-8 estricto antes de leer el JSON, y el alta lee el cuerpo con esa misma función | `37 passed` en el fichero; oráculo en verde a las 18:59, con 88 de 88 ramas. Commit `1e0f839` (18:59:47) |
| 19:01 | H-04 | **No hay rojo, por decisión**: no se implementa, y el test fija el comportamiento que hay. Pasó a la primera a las 19:00 y lleva el comentario de escrito después del código. Sin mutación: fija un límite de Python, no una línea de la aplicación | `tests/integration/test_body_text.py`: en `POST /pricing/quote`, 4300 dígitos responden `422` con `active_users: out_of_range` y 4301 responden `400` `malformed_request`. Limitación **L-05** en `04-calidad/limitaciones-conocidas.md` | `2 passed`; oráculo en verde a las 19:01. Commit `b345bc7` (19:01:28) |
| 19:03 | H-03 | **No hay rojo**: sin cambio de código. El test nuevo, el de la ruta, pasó a la primera a las 19:01 y lleva el comentario | Índice de specs: regla nueva en «Errores de validación» e historial. Un test más en `test_customers_read.py` (`GET /customers/abc?x=1` responde solo `x: unknown_field`); el del cuerpo ya existía desde W-15 | Oráculo en verde a las 19:03. Commit `2e0913f` (19:03:20) |
| 19:07 | H-05 y H-11 | 19:04: **15 en rojo. Doce por aserción**: las ocho filas del dominio (`CustomerSearch(…, tax_id='') == CustomerSearch(…, tax_id=None)` y las de U+0000), las tres filas nuevas de 5.9 (`%00` devolvía los siete clientes, `a%00` devolvía el 2 y el 3, `%00a` los siete) y la del repositorio que demuestra que la condición ya no está en el SQL (`[] == ['B12345674']`). **Tres no fallan por aserción** sino con `AttributeError: 'NoneType' object has no attribute 'replace'`, dentro del código probado: el repositorio aún no admitía una forma sin texto (R-10) | SPEC-01: dos puntos en 2.10, tres filas en 5.9 e historial. `app/domain/customers.py`: `customer_search` devuelve «nada que comparar» (`None`) para el identificador cuando su forma normalizada queda vacía, y para las dos formas cuando el texto lleva U+0000. `app/repositories/customers.py`: la sentencia pierde `? <> ''` y pasa de cuatro parámetros a tres; una forma sin texto llega como nulo, y `LIKE` con un patrón nulo no coincide con ninguna fila | `147 passed` en los tres ficheros; oráculo en verde a las 19:06, con 92 de 92 ramas. Commit `758b880` (19:07:06) |
| 19:08 | H-06 | No aplica: solo documentación | `04-calidad/limitaciones-conocidas.md`: L-04 dice la consecuencia (solo se valida el último `q`) y que se mantiene | Oráculo en verde a las 19:08. Commit `c223520` (19:08:30) |
| 19:11 | H-08 | 19:09: **28 en rojo por aserción**: en el dominio, `[] == [('contact_email', 'invalid_email')]` en las cinco filas nuevas de 5.7 y en 18 de los 19 separadores Unicode (todos menos U+0020, que ya se rechazaba); en la API, `201 == 422` en las cinco filas | SPEC-01: regla del email en 2.1, punto nuevo en 2.12, cinco filas en 5.7 e historial. `app/domain/customers.py`: el email no admite ningún carácter de las categorías `Zs`, `Zl` o `Zp`. Tests: las cinco filas en la tabla compartida por el dominio y la API, y un test unitario que recorre todos los caracteres de las tres categorías, delante y detrás de la `@` | `187 passed` en los dos ficheros; oráculo en verde a las 19:11. Commit `861c6ca` (19:11:25) |
| 19:13 | H-09 | 19:12: **3 en rojo por aserción**: `200 == 404` en `/redoc` y en `/docs/oauth2-redirect`, y la página de `/docs` todavía nombraba la redirección de OAuth. Los otros 3 pasaron a la primera y llevan el comentario: `/docs?x=1` y `/openapi.json?x=1` responden `200`, y el documento OpenAPI no lista ninguna de esas rutas | Índice de specs: punto «Documentación generada», excepción en la fila del parámetro desconocido e historial. `app/main.py`: `redoc_url=None` y `swagger_ui_oauth2_redirect_url=None`. Fichero de tests nuevo, `tests/integration/test_generated_docs.py` | `6 passed`; oráculo en verde a las 19:13. Commit `a52cae5` (19:13:51) |
| 19:16 | H-10 | **No hay rojo**: sin cambio de código; las dos aserciones nuevas pasaron a la primera. **Mutación a las 19:14**: con una cabecera admitida de más (`X-Mutation`) fallan los dos tests de la comprobación admitida, que con la aserción anterior habrían pasado, y los cuatro de las rechazadas; deshecha | SPEC-03: 2.7, la fila de la comprobación admitida de 5.6 e historial. Tests: `test_cors.py` y `test_real_endpoints.py` comparan el valor entero de `access-control-allow-headers`, en vez de mirar solo que `content-type` esté | Oráculo en verde a las 19:16. Commit `b5411f8` (19:16:16) |
| 19:19 | H-12 | **No hay rojo**: no cambia el comportamiento. Los tests del historial que ya había, sin tocar, pasan (`729 passed` en todo el backend a las 19:18); `ruff` y `mypy --strict`, sin avisos | `app/repositories/simulations.py`: cada fila de la consulta del historial se convierte, al salir de la base de datos, en un tipo propio (las columnas de la simulación y su tramo, o ninguno); ya no hay ningún `Any` en el fichero. `CLAUDE.md`, «Estilo común»: el oráculo no comprueba el uso de `Any` sin comentario. `scripts/` sin tocar (solo leído, para saber qué comprueba) | Oráculo en verde a las 19:19. Commit `b579de3` (19:19:29) |
| 19:22 | H-13 | No aplica: solo comentarios | El comentario de «escrito después del código» en: los tres tests de `test_customers_repository.py` y los tres de `test_customer_errors.py` (Y-12), las dos líneas de los límites del `id` en el OpenAPI (Z-04), los tres tests de las siete filas de CORS con endpoints reales (b2) y, con su propia redacción, los cinco tests de 5.7 y CA-09 de `test_real_endpoints.py` (M-07: 20 de sus 27 casos pasaron antes del código). También los de esta sesión que no pudieron verse en rojo (los del emoji y la fila de 4300 nueves) | Oráculo en verde a las 19:22. Commit `e8194d3` (19:22:20) |
| 19:24 | H-14 | **No hay rojo**: son tests de código que ya existía; pasaron a la primera a las 19:23 y llevan el comentario. **Mutación a las 19:23**, una por sentencia, escribiendo el valor dentro del SQL: fallan los dos tests nuevos (un dígito dentro de la sentencia del alta; `[(), ()] == [(12,), (12,)]` en las dos lecturas); deshechas, y `git status` solo mostraba el fichero de tests | `tests/integration/test_customers_search_sql.py`: el alta de un cliente con valores que cambiarían la sentencia si se escribieran en ella, y la lectura de un cliente y de su país con un `id` de dos cifras; en los tres casos, ningún dígito ni comilla en la sentencia y los valores en los parámetros | Oráculo en verde a las 19:24. Commit `edbbb08` (19:24:59) |

### Sondas repetidas y apartado 4 de la respuesta (19:25–19:28)

| Hora | Qué |
|---|---|
| 19:26 | Las sondas del apartado 2 de la respuesta, repetidas con un script fuera del repositorio sobre `edbbb08`, con el cliente de test y una base de datos en el directorio temporal. Las dos primeras ejecuciones (19:25) se cortaron a medias por dos errores del propio script al escribir un surrogate (en un rótulo y en el escape del emoji); la tercera, a las 19:26, terminó. **Todas dan lo esperado**; la tabla de antes y después está en el apartado 5 de la respuesta. `git status` sin cambios tras ejecutarlas |
| 19:28 | Respuesta: apartado 4 con la decisión y el commit de cada hallazgo, apartado 5 con la tabla y cabecera puesta al día. Oráculo en verde. Commit `cff0c0a` (19:28:02) |
| 19:28 | **Enmienda** (norma n3): `cff0c0a` era el último commit y no hay remoto al que se haya subido nada. La fila de H-14 de la tabla decía «tres de seis» sentencias y «las seis», un recuento que no es exacto (el alta de una simulación son dos sentencias). Corregida para decir qué casos cubre la prueba. El commit pasa a ser **`5e9c7ef`** (19:28:16) |

Precisiones de la IA sobre las correcciones, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| R-01 | H-01: el mensaje del error nuevo es «Está fuera del rango admitido.», sin los límites. Además de las tres filas pedidas, un test fija los 4300 nueves (el último tamaño que la biblioteca lee como número), que ya daba `out_of_range` | Ese error de la biblioteca no trae los límites, y el módulo que traduce no sabe de qué campo es. El texto no es parte del contrato |
| R-02 | H-02 y A-01: la regla está escrita para **cualquier petición con cuerpo**, no solo para los tres `POST`, y a cualquier profundidad (un surrogate dentro de una lista o de un objeto anidado). Tests añadidos sin que el encargo los pida: la segunda mitad de una pareja sola, las dos mitades en orden inverso y los casos anidados | El guarda actúa antes de buscar la ruta y no sabe de campos; un surrogate anidado en un campo desconocido acabaría igual en el `422` que no se puede escribir |
| R-03 | H-02 y A-01: cómo lo comprueba el guarda. Vuelve a escribir en UTF-8 lo que ha leído; si no se puede, hay un surrogate suelto. El lector de JSON de Python ya une una pareja bien formada en un solo carácter, así que lo único que no se puede escribir es uno suelto. Cuesta recorrer el cuerpo una segunda vez | Es la misma operación que fallaba después (guardar o responder), hecha antes |
| R-04 | H-02 y A-01: un emoji en el nombre de un campo desconocido de `/pricing/quote` y `/simulations` responde `422` `unknown_field`, no `400`; hay un test, que pasó a la primera (cubierto por la mutación de las 18:55) | En esos dos endpoints no hay ningún campo de texto donde un emoji pueda dar `201`; es la forma de ver ahí que la regla no rechaza de más |
| R-05 | H-07: el parámetro `charset` del `Content-Type` no cambia cómo se lee el cuerpo: `application/json; charset=utf-16` con un cuerpo en UTF-16 responde `400`. Hay un test | La convención ya admitía `Content-Type` con parámetros; la decisión dice que el cuerpo es UTF-8 y no habla del parámetro |
| R-06 | H-07: el alta de clientes leía el cuerpo por segunda vez con el lector de JSON y bytes; ahora usa la misma función que el guarda. Para no dejar una rama defensiva que ningún test puede recorrer, el tipo del resultado se afirma con `cast`, con su comentario | Una sola lectura del cuerpo, igual en los dos sitios |
| R-07 | H-03: **la IA escribió primero un «por qué» inventado** («una petición con un parámetro que el contrato no conoce está mal dirigida entera») y lo sustituyó antes del commit por el que consta: es lo que el backend hace desde SPEC-02, la alternativa obligaba a fijar el orden entre los dos grupos de errores y el Tech Lead lo mantuvo | El encargo no da un porqué para H-03, y la IA no debe atribuir uno |
| R-08 | H-03: test añadido sin que el encargo lo pida, para el caso de la ruta | La regla escrita nombra la ruta y el cuerpo, y solo el cuerpo tenía test |
| R-09 | H-05 y H-11: **cuatro filas de un test que ya existía cambian de valor esperado**, de `""` a `None` (`tests/unit/test_customers.py`, el test de `customer_search` que el Tech Lead pidió en r4). No se relaja: sigue comparando el resultado entero. Se cambió antes que el código y se vio en rojo. Está marcado con un comentario en el test | La decisión de H-11 cambia lo que devuelve el dominio: «no hay identificador que comparar» deja de ser una cadena vacía que el SQL interpretaba. **Si el Tech Lead prefiere otra representación que no toque esas filas, se cambia** |
| R-10 | H-05 y H-11: tres tests del repositorio no dieron un rojo por aserción, sino un `AttributeError` del código probado. No es un fallo de importación, pero tampoco lo que pide la norma del flujo 2 | El repositorio no admitía todavía una forma sin texto y reventaba antes de llegar a la aserción. La IA no escribió un paso intermedio artificial solo para convertirlo en aserción |
| R-11 | H-05 y H-11: la sentencia sigue ejecutándose con un `q` que lleva U+0000 (con los dos patrones nulos), en vez de devolver la lista vacía sin consultar | Así la base de datos apartada sigue respondiendo `503` también para ese `q`, como para cualquier otro, y hay una sola sentencia |
| R-12 | H-05 y H-11: un test nuevo le da al repositorio, a mano, un identificador vacío y comprueba que entonces coincide con todos los clientes | Es la prueba de que la condición salió del SQL: el dominio nunca entrega esa forma. Antes del cambio devolvía la lista vacía |
| R-13 | H-05: la regla está escrita en SPEC-01 2.10, además de las filas de 5.9 que pedía el encargo | Tres filas de una tabla sin una regla de la que cuelguen no dicen por qué |
| R-14 | H-08: un separador en el email da `invalid_email` y no `invalid_characters`, y se comprueba al final del orden de 2.12, después de `too_long`. Un espacio de no separación en un extremo no se recorta (solo U+0020) y da `invalid_email`. Escrito en 2.12 | El encargo dice el código; el orden sale de que es parte de la forma del email. El recorte no cambia: 2.12 lo define con U+0020 |
| R-15 | `app/domain/customers.py` tiene ahora 234 líneas, de 250 | Aviso: la próxima regla del alta o del buscador obligará a dividirlo por responsabilidad |
| R-16 | H-09: además de lo pedido, un test comprueba que la página de `/docs` ya no nombra la redirección de OAuth y otro que el OpenAPI no lista `/docs`, `/redoc` ni `/openapi.json` | Lo primero es la consecuencia visible de quitar la ruta; lo segundo, que el contrato sigue describiendo solo los endpoints de negocio |
| R-17 | H-09: la frase «la página de `/docs` carga sus scripts y estilos de un servidor externo» está en el índice de specs, además de apuntada para el README | El encargo pide apuntarlo para el README; quien lea el contrato también debe saberlo |
| R-18 | H-10: el valor exacto se fija en los dos tests de la comprobación admitida (el de la ruta de prueba y el de `OPTIONS /customers`), con una sola constante compartida con las rechazadas. Es una aserción más estricta que la que había | La anterior (`content-type` está en la cabecera) habría dejado pasar una cabecera admitida de más, como mostró la mutación |
| R-19 | H-12: la conversión de la fila al tipo nuevo se hace en una función que recibe el cursor de `sqlite3` y lee de él, y por eso `sqlite3` se importa ahora también en el repositorio de simulaciones (solo para el tipo del cursor) | Recibir las filas ya leídas obligaba a anotarlas con `Any`, que es lo que se quería quitar. `sqlite3` solo puede importarse en `repositories/`, y ahí está |
| R-20 | H-12: la nota de `CLAUDE.md` lleva un «por qué» escrito por la IA: «un `Any` sin comentario pasó el oráculo y lo encontró el evaluador (H-12)» | Es el hecho que motiva la nota, no una regla nueva |
| R-21 | H-13: en M-07 la bitácora dice cuántos casos pasaron antes del código (20 de 27), no cuáles. El comentario lo dice así, sobre los cinco tests, sin señalar casos concretos | La IA no puede saber hoy cuáles fueron sin reconstruirlo, y la bitácora no se reconstruye |
| R-22 | H-14: el alta de prueba usa valores que el dominio no dejaría pasar (comillas y `DROP TABLE` en el nombre, el email, el identificador y el plan) | El repositorio guarda lo que recibe; son los valores que cambiarían la sentencia si se escribieran en ella |
| R-23 | Sondas: un surrogate suelto en `tax_id`, `country` o `plan`, que antes respondía `422` con el código de su campo, responde ahora `400` | Consecuencia de poner la regla en el guarda, que actúa antes que la validación de cualquier campo. Está en la tabla de la respuesta |

### Segunda pasada del evaluador (19:31–19:43)

| Hora | Qué |
|---|---|
| 19:30 | Antes de lanzarlo, leído en el registro de la sesión 04 el encargo que recibió entonces, para repetir sus restricciones a la letra |
| 19:31 | Lanzado el subagente `evaluador` con el árbol limpio en `eb0a27f`. Encargo: solo comprobar que cada hallazgo corregido lo está de verdad y buscar regresiones. Mismas restricciones: solo lectura, no leer `03-proceso/` ni `04-calidad/` ni la historia de git, rutas relativas y decir en la cabecera qué modelo es. Como no puede leer su primer informe, el encargo le da cada hallazgo como se describió y lo que decidió el Tech Lead. **La IA no le dio ninguna conclusión propia** sobre si están corregidos, ni cómo se corrigieron, ni las precisiones R-01 a R-23. Una condición nueva: nombrar los caracteres invisibles por su código y no escribirlos, para que no se repita lo del U+00A0 |
| 19:31–19:39 | La IA no tocó el repositorio |
| 19:39 | Informe recibido. `git status --short` vacío, `HEAD` en `eb0a27f` y ningún `stash`: el evaluador no cambió nada versionado |
| 19:40 | Informe escrito con `Write` en `04-calidad/evaluacion-backend-02.md`, quitando solo la sangría de dos espacios que añade la herramienta. **Comparado con el mensaje que consta en el registro del subagente** (script de solo lectura fuera del repositorio): 106 líneas y 15.197 caracteres los dos, **ninguna línea distinta**, y el mensaje no trae ningún carácter de control ni separador que no sea el espacio y el salto de línea. En el mismo registro: tipo de agente `evaluador` y modelo `claude-opus-5-5` en sus 75 respuestas |
| 19:41 | Oráculo en verde. Commit propio del informe: `99aeec2` (19:41:49) |
| 19:42 | La IA comprueba los tres hallazgos nuevos, sin corregir nada. Una primera orden de sondeo fue **denegada** por el modo de permisos (era larga y llevaba un borrado en la carpeta temporal); la IA la dividió en pasos sin borrado |

**Resultado del informe**: oráculo en verde y 731 tests, ejecutados por el
evaluador. De los 16 hallazgos: **12 `CORREGIDO`** (H-01, H-02, A-01, H-03,
H-05, H-07, H-08, H-09, H-10, H-11, H-12 y H-14), **3 `CONFORME A LO
DECIDIDO`** (H-04, H-06 y H-15) y **1 sin veredicto posible** (H-13: los
comentarios están, pero sin leer la historia no puede saber si están
todos). De los cinco requisitos que eran `NO CUMPLE`, dos pasan a `CUMPLE`
(SPEC-01/E-24 y E-25) y **tres siguen en `NO CUMPLE`, por las limitaciones
aceptadas**: SPEC-01/E-30 (L-04) y SPEC-02/E-14 y SPEC-03/E-07 (L-05).
**Ninguna regresión encontrada y tres hallazgos nuevos**: N-01, de gravedad
media, y N-02 y N-03, de gravedad baja.

Lo que la IA ha comprobado de los hallazgos nuevos. **No ha corregido
ninguno ni propone todavía nada**: el encargo acaba en el informe.

| Hallazgo | Qué dice el informe | Qué ha comprobado la IA |
|---|---|---|
| N-01 · media | Un método no admitido sobre `/docs` o `/openapi.json` (`POST`, `PUT`, `DELETE`, `OPTIONS`) responde `500` `internal_error` en vez de `405`: la función que calcula la cabecera `Allow` no encuentra la ruta en la petición. El evaluador no pudo decir si es una regresión | **Se reproduce** (19:42): las cinco peticiones del informe dan `500`; `POST /health` da `405` con `Allow: GET`. **No es una regresión**: el mismo sondeo contra el código de `bda2c65`, extraído con `git archive` a una carpeta temporal fuera del repositorio, da los mismos cinco `500`, y además `POST /redoc` daba `500` (hoy da `404`). Es un defecto anterior a esta sesión, que la primera evaluación no vio y la IA tampoco. La corrección de H-09 lo hace más visible: el índice dice ahora que esas dos rutas existen. Los tests de H-09 solo prueban `GET` |
| N-02 · baja | Quedan `Any` sin un comentario en su misma línea en `app/api/validation.py` (`_failed_fields` y `_field_error`) y en `app/api/contract.py` (`methods_of`) | **Cierto**, leído en el código: esas funciones usan `Any` y el comentario está sobre otra función del mismo fichero. No es de esta sesión: el primer informe daba esos dos ficheros por buenos («cada `Any` lleva su comentario») y el Tech Lead decidió H-12 sobre `simulations.py`. Los dos informes no miden igual |
| N-03 · baja | (1) L-04 y L-05 no aparecen en ninguna spec: quien lea solo las specs no sabe que E-30, SPEC-02/E-14 y SPEC-03/E-07 tienen esas desviaciones. (2) La tabla 5.7 de SPEC-03 no tiene filas para el surrogate suelto, UTF-16 o UTF-32, el BOM, `/redoc` ni `/docs?x=1`, así que CA-17 («cada fila de 5.7») no alcanza a los tests nuevos | **Cierto las dos cosas**, leído: las limitaciones están solo en `04-calidad/limitaciones-conocidas.md`, que el evaluador no lee, y la tabla 5.7 no ha cambiado. El encargo pedía escribir las reglas nuevas en el índice, y ahí están; no pedía filas en 5.7 ni llevar las limitaciones a las specs |

Precisiones de la IA sobre la segunda pasada, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| V-08 | Una cita del informe no cuadra: sitúa el cambio de H-09 en `backend/app/main.py:223-226`, y ese fichero tiene 85 líneas (el cambio está en las líneas 66 a 69). El informe se queda como llegó | Intacto quiere decir también con sus errores |
| V-09 | El encargo al evaluador lo redactó la IA, incluida la descripción de cada hallazgo y de cada decisión. Es un resumen del primer informe y del encargo del Tech Lead, no su texto literal | El evaluador no puede leer `04-calidad/`. Un resumen mal hecho podría haberle orientado; el texto completo del encargo consta en el registro del subagente |
| V-10 | El evaluador dice no haber ejecutado ninguna mutación (no puede modificar código): que los tests nuevos fallarían con el defecto original lo razona, no lo ve. Los rojos y las mutaciones de esta bitácora son de la IA | Límite del solo lectura, dicho en el apartado 5 de su informe |
| V-11 | Un caso que el evaluador anota sin contarlo como defecto: un `q` que solo tiene una marca diacrítica (U+0301) devuelve todos los clientes, porque su forma de búsqueda queda vacía. Es el caso Y-25 de la sesión 04 (un `q` que queda vacío sin serlo), ya admitido | Para que no se lea como algo nuevo |

### Revisión de las correcciones y de la segunda pasada por el Tech Lead (20:06)

El cierre anterior de esta bitácora es `99e01a7` (19:45:28 según `git log`).

**Correcciones revisadas.** Admitidas R-01 a R-23; en R-09 vale la
representación con `None`. El Tech Lead dice haber comprobado contra un
servidor real con `uvicorn` que las sondas de H-01 a H-14 y A-01 dan lo
decidido y que no hay regresiones (lo afirma él; la IA no lo ha visto). El
mensaje no nombra V-08 a V-11, que siguen sin aprobar.

Decisión de los hallazgos nuevos y de lo que quedaba suelto:

| # | Decisión del Tech Lead | Frente a lo que había |
|---|---|---|
| N-01 | **Se corrige.** Un método no admitido sobre `/docs` o `/openapi.json` responde `405` `method_not_allowed` con una cabecera `Allow` que diga los métodos que esa ruta admite de verdad (`HEAD` responde `200` en las dos). Por qué: el índice dice ahora que esas rutas existen, y un `500` nunca es respuesta a una petición del cliente. Confirmado por él con servidor real: `POST`, `PUT`, `DELETE` y `OPTIONS` sobre `/docs`, y `POST` y `DELETE` sobre `/openapi.json`, dan `500` con `KeyError: 'route'`. Tests en rojo antes, con esas seis filas. Una frase en «Documentación generada» del índice, con historial | La IA no había propuesto nada: el encargo anterior acababa en el informe |
| N-02 | De acuerdo. Cada `Any` que queda lleva su comentario en esa línea o un tipo concreto. Al terminar, una búsqueda comprueba que no queda ninguno sin él | — |
| N-03 | De acuerdo en las dos partes. (1) Las specs citan las limitaciones: una nota en SPEC-01 junto a E-30 hacia L-04 y una en la fila del `400` del índice hacia L-05, con historial. (2) Filas nuevas en SPEC-03 5.7 para el surrogate suelto, UTF-16 y UTF-32, el BOM, `/redoc`, `/docs?x=1` y las de N-01, con historial; los tests que ya existen citan esas filas | — |
| H-15 | Se mantiene L-01. Se añade la medida (2.000.000 y 20.000.000 de caracteres se procesan enteros) y cómo se cerraría en producción: un límite en el proxy inverso | No había llegado en el encargo anterior |
| V-11 | Un `q` que solo lleva una marca diacrítica (U+0301) devuelve el listado inicial, porque su forma de búsqueda queda vacía: es lo que dice 2.10. Se fija con una fila en SPEC-01 5.9 y un test, anotado como escrito después del código | El caso que anotó el evaluador sin contarlo como defecto |

Cómo: rojo antes del código en N-01; un commit por hallazgo; oráculo en
verde en cada uno. `04-calidad/respuesta-evaluacion-backend-02.md` con la
decisión y el commit de cada fila. **No hace falta una tercera pasada del
evaluador.** Cierre de esta bitácora con su resultado y la IA para.

### Correcciones tras la revisión (desde las 20:07)

Cada commit, con el oráculo en verde (20 correctas, 0 con fallo, 4
inactivas) justo antes.

| Hora | Hallazgo | Rojo visto antes del código | Qué se hizo | Verde, oráculo y commit |
|---|---|---|---|---|
| 20:10 | N-01 | 20:08: **6 en rojo por aserción** (`assert 500 == 405`; en el log, «Unexpected error in POST /docs» y las otras cinco): `POST`, `PUT`, `DELETE` y `OPTIONS /docs`, y `POST` y `DELETE /openapi.json`. Los dos tests de `HEAD` pasaron a la primera y llevan el comentario | Índice de specs: frase en «Documentación generada» e historial. `app/api/contract.py`: una petición a una ruta que no es del contrato no declara ningún método, en vez de fallar. `app/api/error_handling.py`: en ese caso, la cabecera `Allow` dice los métodos que el framework nombra para esa ruta, ordenados. Tests en `test_generated_docs.py`: las seis filas, con `Allow: GET, HEAD` y sin ningún error en el log | `79 passed` en los tres ficheros de errores genéricos; oráculo en verde a las 20:10, con 96 de 96 ramas. Commit `b5c468d` (20:10:17) |
| 20:13 | N-02 | **No hay rojo**: no cambia el comportamiento. `ruff`, `mypy --strict` y los tests (`739 passed`), en verde a las 20:12 | `app/api/validation.py`: los errores de Pydantic se anotan con el tipo que la propia biblioteca les da (`ErrorDetails`) y el fichero ya no usa `Any`. `app/api/contract.py` y `app/api/problems.py`: un alias en cada uno para lo que FastAPI tipa con `Any` (el objeto de un documento OpenAPI y el parámetro `responses`), con el comentario en la misma línea. **Búsqueda al terminar**: en el código Python de `backend/` y `scripts/` la palabra solo aparece en dos `import`, en los dos alias comentados y en dos docstrings donde es la palabra inglesa | Oráculo en verde a las 20:13. Commit `7cc5858` (20:13:11) |
| 20:15 | N-03 | No aplica: documentación y docstrings | SPEC-01: nota «Sobre E-30» hacia L-04 e historial. Índice: la fila del `400` cita L-05, e historial. SPEC-03 5.7: seis filas nuevas e historial. Cinco docstrings de `test_body_text.py` y `test_generated_docs.py` citan esas filas y CA-17; ningún test cambia | Oráculo en verde a las 20:15. Commit `040eba3` (20:15:43) |
| 20:18 | H-15 | No aplica: documentación. **Medido antes de escribirlo**, a las 20:15, con un script fuera del repositorio y el cliente de test: un `company_name` de 2.000.000 de caracteres responde `422` con `too_long` en 0,32 s y uno de 20.000.000, en 2,14 s; después no hay ningún cliente guardado | `04-calidad/limitaciones-conocidas.md`: L-01 dice la medida, que es un riesgo de denegación de servicio, y cómo se cerraría en producción (un límite en el proxy inverso) | Oráculo en verde a las 20:18. Commit `aef612a` (20:18:24) |
| 20:22 | `q` con solo U+0301 | **No hay rojo, por decisión**: el test fija lo que el código ya hace. Pasó a la primera a las 20:18 y lleva el comentario | SPEC-01 5.9: una fila e historial. Tests: uno de la API (con el `q` escrito como `%CC%81` y también como parámetro) y una fila del dominio | `167 passed` en los dos ficheros; oráculo en verde a las 20:22. Commit `bd7d269` (20:22:13) |
| 20:24 | Respuesta | — | `04-calidad/respuesta-evaluacion-backend-02.md`: una fila por hallazgo, la decisión y el commit de cada una, la búsqueda de N-02 y lo que no demuestra | Oráculo en verde a las 20:24. Commit `68ef17f` (20:24:58) |

Precisiones de la IA sobre estas correcciones, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| R-24 | N-01: en una ruta que no es del contrato, la cabecera `Allow` sale de lo que el framework dice de su propia ruta en el `405` que él mismo levanta, puesta en orden alfabético. En las rutas del contrato sigue saliendo del contrato, como antes | El framework solo nombra los métodos de la primera ruta que encaja; por eso las rutas de negocio miran el contrato. `/docs` y `/openapi.json` son una sola ruta cada una y no están en el contrato. El orden se fija porque el framework los escribe en el orden de un conjunto, que cambia entre ejecuciones |
| R-25 | N-01: además de las seis filas, dos tests comprueban que `HEAD` responde `200` y sin cuerpo en las dos rutas, y las seis filas comprueban también que no se registra ningún error | `Allow: GET, HEAD` solo es verdad si `HEAD` funciona, y un `405` no es un fallo nuestro que deba ir al log |
| R-26 | N-02: la regla y la búsqueda miran el `Any` que se escribe. Lo que una biblioteca devuelve sin tipo (las filas de `sqlite3`, el JSON leído) sigue llegando sin tipo hasta la línea que lo anota; y el `cast` del guarda (R-06) no es un `Any` | Para que «no queda ninguno» no se lea como más de lo que es |
| R-27 | N-03: la fila de `/docs?x=1` de 5.7 responde `200`, no un error: de lo que pide CA-17 solo le aplica el estado, como a la fila del `Content-Type` con parámetros que ya había. No se han añadido filas para lo que el encargo no nombra: el emoji válido, la frontera de L-05 ni el `charset` del `Content-Type` | El encargo enumera las filas |
| R-28 | N-03: la cita de L-05 está dentro de la celda de la fila del `400`, con un enlace a `04-calidad/limitaciones-conocidas.md`; la de L-04, en una nota bajo la tabla de requisitos del buscador | Donde lo pide el encargo |
| R-29 | H-15: los tiempos son de una sola ejecución, en el equipo de desarrollo y con el cliente de test | Valen como orden de magnitud; el encargo pedía que constara que se procesan enteros |
| R-30 | **Error de la IA, visto antes del commit**: en los dos tests del `q` con U+0301 escribió el carácter como escape (`́`) y la herramienta de edición lo guardó como el carácter literal, invisible. Lo vio al comprobar el fichero, lo sustituyó por `chr(0x0301)` y repasó todo el código versionado de `backend/`, `scripts/` y `CLAUDE.md`: ninguna línea con un carácter invisible literal. En `ai-workspace/` solo hay dos, los dos a propósito: el espacio de anchura cero del ejemplo de SPEC-01 5.7 y el U+00A0 del informe | Lo mismo que pasó con el U+00A0, al revés: lo que la IA escribe no siempre llega tal cual al fichero. Los caracteres invisibles se escriben por su código |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git rev-parse --short HEAD` (18:43) | Limpio, `68ae670` |
| Registro del evaluador de la sesión 04 | Script de solo lectura fuera del repositorio (18:45) | Tipo de agente `evaluador`, modelo `claude-opus-5-5` en 60 respuestas, y una sola línea distinta entre su mensaje y el informe guardado: la 255 |
| U+00A0 del informe | Recuento de caracteres con Python y nueva comparación con el registro (18:47) | Exactamente un U+00A0; ninguna línea distinta del mensaje |
| Oráculo antes de cada commit | `uv run scripts/check.py`, 19 veces entre las 18:48 y las 19:41 | Siempre código de salida 0: 20 correctas, 0 con fallo y 4 inactivas (las del frontend). Las ramas del backend pasan de 86 de 86 a 92 de 92; `domain/` sigue al 100 % |
| Tests del backend | `uv run pytest` (19:18) y el recuento del evaluador (19:37) | `729 passed` antes de H-13 y H-14; `731 passed` al final. Al empezar eran 639 |
| Mutaciones | Cambio temporal del código con `Edit`, tests y vuelta atrás: H-02 (18:55), H-10 (19:14) y H-14 (19:23) | Los tests que no pudieron verse en rojo fallan con la mutación. Tras cada una, `git status` sin restos |
| Sondas del apartado 2 de la respuesta | Script fuera del repositorio, con el cliente de test (19:26) | Todas dan lo decidido; tabla en el apartado 5 de la respuesta |
| Que el evaluador no tocó nada | `git status --short`, `git rev-parse --short HEAD` y `git stash list` (19:39) | Vacío, `eb0a27f` y ningún `stash` |
| Segundo informe, intacto | Comparación con el mensaje del registro del subagente (19:40) | 106 líneas y 15.197 caracteres; ninguna línea distinta |
| N-01 en el código actual y en el de `bda2c65` | Sondeo con el cliente de test; el código antiguo, extraído con `git archive` a una carpeta temporal (19:42) | `500` en los dos: no es una regresión |
| Oráculo antes de cada commit tras la revisión | `uv run scripts/check.py`, 7 veces entre las 20:10 y las 20:26 | Siempre código de salida 0: 20 correctas, 0 con fallo y 4 inactivas. Las ramas del backend pasan de 92 de 92 a 96 de 96 |
| Tests del backend al terminar | `uv run pytest` (20:22) | `741 passed` |
| Ningún `Any` sin comentario en su línea (N-02) | `grep` de la palabra en el código Python de `backend/` y `scripts/`, sin el entorno virtual (20:13) | Dos `import`, dos alias con el comentario en la misma línea y dos docstrings con la palabra inglesa |
| Cuerpos de 2 y 20 millones de caracteres (H-15) | Script fuera del repositorio, con el cliente de test (20:15) | `422` con `too_long` los dos, en 0,32 s y 2,14 s; ningún cliente guardado |
| Caracteres invisibles literales | Recorrido de los ficheros versionados con Python (20:20 y 20:25) | Ninguno en `backend/`, `scripts/` ni `CLAUDE.md`. En `ai-workspace/`, dos, los dos a propósito (R-30) |

## 5. No verificado

- Nada con un servidor real (`uvicorn`): todas las pruebas de la sesión, las
  de la IA y las del evaluador, son con el cliente de test.
- Que el hook pidiera confirmación al editar las specs aprobadas (el índice,
  SPEC-01 y SPEC-03): la IA no ve el diálogo. Las ediciones se aplicaron.
- Que la lista de tests escritos después del código esté completa (H-13):
  sale de lo que la bitácora de la sesión 04 anotó (r4, Y-12, Z-04, b2 y
  M-07). Un test que pasara a la primera sin anotarse no tendría comentario.
  El evaluador tampoco pudo comprobarlo.
- Cuáles de los 27 casos de M-07 pasaron antes del código: la bitácora dice
  cuántos, no cuáles (R-21).
- Que la regla del surrogate suelto no rechace ningún texto válido más allá
  de lo probado: emojis como pareja de escapes y en UTF-8, en un valor y en
  un nombre de campo.
- El coste de recorrer el cuerpo una segunda vez en el guarda (R-03): no se
  ha medido, y el cuerpo sigue sin límite de tamaño (L-01).
- `/docs` en un navegador: carga recursos de un servidor externo y nadie la
  ha abierto en esta sesión; solo se ha visto su HTML y su estado.
- Qué significa el campo `pickedEffortModel` del fichero de metadatos del
  subagente (dice `claude-fable-5-2`); el modelo de cada respuesta del
  registro es `claude-opus-5-5`.
- Que el comportamiento de `LIKE` con un patrón nulo sea el mismo en otra
  versión de SQLite: probado con la 3.42.0 del entorno.
- Nada fuera de Windows.
- Los tres requisitos que el evaluador mantiene en `NO CUMPLE`
  (SPEC-01/E-30, SPEC-02/E-14 y SPEC-03/E-07) siguen así por las
  limitaciones L-04 y L-05, aceptadas por el Tech Lead.
- ~~Los tres hallazgos nuevos (N-01, N-02 y N-03) están comprobados, no
  corregidos~~: corregidos entre las 20:07 y las 20:15, por decisión del
  Tech Lead.
- ~~Nada con un servidor real~~, en parte: el Tech Lead dice haber
  comprobado con `uvicorn` las sondas de H-01 a H-14 y A-01 y que N-01 se
  reproducía (lo afirma él). **Las cinco correcciones hechas después de su
  revisión no se han probado con un servidor real**, tampoco el `405` de
  N-01.
- **Ninguna comprobación independiente de las correcciones hechas tras la
  revisión** (N-01, N-02, N-03, H-15 y el `q` con solo U+0301): no hay
  tercera pasada del evaluador, por decisión del Tech Lead. Solo hay los
  tests y las comprobaciones de la IA sobre su propio código.
- Que la cabecera `Allow` de `/docs` y `/openapi.json` siga siendo
  `GET, HEAD` con otra versión del framework: sale de lo que el framework
  dice de sus rutas. Un test lo fija con la versión actual.
- Los tiempos de H-15: una sola ejecución, en el equipo de desarrollo.
- Cómo se comporta un proxy inverso con un límite de tamaño delante del
  backend (el cierre previsto de L-01): no hay ninguno; es una previsión.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Decidir cada hallazgo de la evaluación del backend: H-01 a H-15 y A-01~~ | Hecho a las 18:42, en el encargo, salvo H-15. Corregidos entre las 18:50 y las 19:25 |
| ~~Aprobar o cambiar B-01 a B-04 y V-04 a V-07~~ | Admitidas a las 18:42 |
| ~~Decidir N-01, N-02 y N-03~~ | Decididos a las 20:06. Hechos en `b5c468d`, `7cc5858` y `040eba3` |
| ~~H-15~~ | Decidido a las 20:06: se mantiene L-01, con la medida y el cierre previsto. Hecho en `aef612a` |
| ~~Aprobar o cambiar R-01 a R-23~~ | Admitidas a las 20:06; en R-09 vale la representación con `None` |
| Aprobar o cambiar V-08 a V-11 (la revisión de las 20:06 no las nombra) y R-24 a R-30 | A decidir por el Tech Lead |
| `app/domain/customers.py` está en 234 líneas de 250 (R-15): la próxima regla del alta o del buscador obligará a dividirlo | Cuando llegue esa regla |
| Poner un límite de tamaño del cuerpo en el proxy inverso (cierre previsto de L-01) | Si el backend se despliega en producción |
| **Documentar en el README que `/docs` carga recursos de un servidor externo** (decisión de H-09) | Al escribir el README |
| Llevar la lista de `04-calidad/limitaciones-conocidas.md` al README, ahora con L-05 | Al escribir el README |
| Pendientes heredados de la sesión 04 que esta sesión no toca: T-01 a T-08, la base de datos creada antes de `9ec6866` (P-03), documentar la estructura del backend en `02-arquitectura/README.md`, el margen de una semana en npm (ADR-007) y los heredados de la sesión 03 | A decidir por el Tech Lead |
| Aprobar SPEC-04 | Antes de empezar el frontend |
