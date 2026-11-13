# Sesión 05 · Correcciones de la evaluación independiente del backend

| | |
|---|---|
| **Fecha** | 2026-11-13 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | *En curso.* Se rellena al cerrar la sesión |

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

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git rev-parse --short HEAD` (18:43) | Limpio, `68ae670` |

## 5. No verificado

*Se rellena durante la sesión.*

## 6. Tareas pendientes

*Se rellena durante la sesión.*
