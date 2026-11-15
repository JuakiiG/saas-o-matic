# Respuesta a la segunda evaluación independiente del frontend

| | |
|---|---|
| **Fecha** | 2026-11-15 |
| **Responde a** | [`evaluacion-frontend-02.md`](evaluacion-frontend-02.md), que no se modifica |
| **Decide** | Tech Lead. **Sin decidir**: la columna «Qué propone la IA» es una propuesta. **No se ha aplicado nada** |
| **Escribe** | IA (Claude Code) |
| **Estado del código** | El informe evaluó el repositorio en `7f8c974`, con el árbol limpio y los diez cambios de la parada 2 aplicados |

Procedimiento: el informe del evaluador no se modifica; se responde a cada
hallazgo. Antes de responder, la IA ha repetido por su cuenta, solo leyendo
y ejecutando, lo que afirman los hallazgos (apartado 2). **Los nueve se
reproducen.** Lo que la IA no ha repetido está en el apartado 5.

Resumen de la respuesta:

- **El encargo era acotado** (decisión B-03 del Tech Lead): CA-04, CA-05,
  CA-08 y CA-16 fila a fila, el contrato del backend contra el frontend y
  los cambios de hoy.
- **Las 109 filas de 5.3 a 5.6 tienen test** (24, 40, 29 y 16; la IA ha
  contado las mismas). **Los cuatro criterios salen `NO CUMPLE`**, donde la
  primera evaluación decía «CUMPLE (muestreo)»: no por un comportamiento
  que falle, sino porque varios tests no comprueban todo lo que el criterio
  pide al pie de la letra (el cuerpo de cada envío, la URL de cada
  búsqueda, que haya «Reintentar»). Son tests de la sesión 07.
- **El contrato**: ninguna diferencia entre las specs, el backend real y
  `core/models.ts`, ni en lo que el frontend hace con cada código.
- **Los diez cambios de hoy**: los diez se sostienen. Tres dejan un fleco
  que es hallazgo: N-01 (la regla de H-05 sin test), N-06 (la página «no
  encontrada» sin título) y N-07 (qué es «una fecha»).
- **De acuerdo con los nueve hallazgos.** En desacuerdo, ninguno.
- **Dos ya los había dicho la IA** antes de la evaluación: N-01 (precisión
  AE-11 de la bitácora) y N-06 (AE-08).
- **Uno es de comportamiento y corrige a la IA**: N-07. La regla que la IA
  escribió hoy en 2.8 no es cierta para cualquier texto, y la precisión
  AE-11 decía que la fijaban dos tests cuando es uno (fila C-04).
- **Seis son huecos de tests de la sesión 07**: N-02, N-03, N-04, N-05,
  N-08 y N-09.
- **Cinco casos más**, que salen de leer el informe: filas C-01 a C-05
  (apartado 3). El más importante: **al menos quince números de línea del
  informe son erróneos** (C-01).

## 1. Respuesta por hallazgo

| Hallazgo | Grav. | ¿De acuerdo? | Qué propone la IA | Qué habría que tocar |
|---|---|---|---|---|
| N-01 · «Sin Reintentar» del `409` y del aviso general de un `422` no lo fija ningún test de vista | media | **Sí.** Es lo que la IA anotó en AE-11 al aplicar H-05, y el evaluador lo extiende: tampoco los tests de vista del aviso general de un `422` (`alta.spec.ts:415`, `simulador.spec.ts:561` y `:707`) miran que falte el botón. Solo lo fija `core/api-error.spec.ts:169`, en la función | Añadir las aserciones: en el alta, que el aviso del `409` y el del `422` con un campo desconocido no traen el botón; en el simulador, lo mismo en la proyección y en el guardado. Nacen en verde: una mutación en cada sitio (`retryable: true` en `alta.ts` y en `api-error.ts`) | `alta.spec.ts` y `simulador.spec.ts`. Código, ninguno |
| N-02 · El reintento del guardado no demuestra que se envía «lo que el formulario tiene en ese momento» | media | **Sí.** `simulador.spec.ts:664` no cambia nada entre el fallo y el reintento y espera el mismo cuerpo. El alta sí lo prueba (`alta.spec.ts:543`); en el simulador la IA no escribió el caso equivalente | Un test nuevo en el simulador: guardar, `500`, cambiar el almacenamiento, «Reintentar», y el cuerpo lleva el valor nuevo. Nace en verde: mutación que reenvíe lo que se envió la primera vez | `simulador.spec.ts` |
| N-03 · CA-05 y CA-08 piden el cuerpo de cada envío y muchas filas no lo miran; faltan las opciones desactivadas de los desplegables y el «0 todavía» | baja | **Sí en el hecho.** Matiz: en esos tests el envío sale de la misma función de ayuda, con los mismos valores válidos cuyo cuerpo ya comprueba otro test; lo que cada fila prueba es la respuesta. Pero el criterio dice «de cada fila que se envía», y eso no se cumple | **Lo decide el Tech Lead.** **Recomendada**: cumplir el criterio como está escrito: la aserción del cuerpo en los ocho tests del alta y en los siete del simulador que el informe lista, un test de las dos opciones desactivadas («Elige un país», «Elige un plan», que se ven al abrir y no se pueden elegir) y, en la fila de los 200 ms, contar cero peticiones antes. Nacen en verde: mutaciones por grupo. **Alternativa**: precisar CA-05 y CA-08 para que pidan el cuerpo donde lo enviado es lo que la fila prueba; es menos trabajo y deja el criterio más débil | `alta.spec.ts` y `simulador.spec.ts`; con la alternativa, SPEC-04 (CA-05 y CA-08) con historial |
| N-04 · CA-04 pide «el parámetro `q` y la URL de cada una»; siete filas no miran la URL y dos tampoco `q`; el test de «volver al panel» no puede fallar | baja | **Sí.** Lo más serio es lo último: `panel.spec.ts:304` destruye y crea el panel, pero quien pide `/meta` es `app.config.ts`, no el panel, así que el test pasaría con cualquier código. **Es un test que no prueba nada**, escrito por la IA en la sesión 07 | Añadir la URL (y `q`) en las siete filas y «Reintentar» en `:260`. Para la fila 14, **un test de verdad en `app.journeys.spec.ts`**: del panel al detalle y vuelta al panel, con una sola petición a `/meta` en todo el recorrido. Qué hacer con `:304` **lo decide el Tech Lead** (regla 3: un test no se borra sin su decisión): la IA propone sustituirlo por el del recorrido | `panel.spec.ts` y `app.journeys.spec.ts` |
| N-05 · En el nivel 2 de CA-16, tres casos no comprueban «Reintentar» y el guardado no tiene caso de falta de conexión | baja | **Sí** | La aserción del botón en `panel.spec.ts:464` y `:473` y en `simulador.spec.ts:489`, y un caso nuevo de falta de conexión al guardar. Nacen en verde: mutación | `panel.spec.ts` y `simulador.spec.ts` |
| N-06 · La página «no encontrada» conserva el título de la vista anterior | baja | **Sí.** Es la consecuencia que la IA anotó en AE-08 al aplicar H-03, con la pregunta al Tech Lead | **Lo decide el Tech Lead**, porque es un texto nuevo: `title` en la quinta ruta. La IA propone «Página no encontrada · SaaS-O-Matic», que es el `h1` de esa página. E-57 y 2.1 pasan a decir cinco vistas, y el test, en rojo antes | `app.routes.ts`, `app.routes.spec.ts` y SPEC-04 (2.1, E-57, CA-11, historial) |
| N-07 · «Un `created_at` que no se puede leer como fecha se muestra como llega» depende de lo que acepte `Date`, que lee como fecha textos que no lo son | baja | **Sí. Reproducido** con Node 24: `Ejemplo 7` da el 30 de junio de 2001; `1`, el 31 de diciembre de 2000; `12/11/2026`, el 10 de diciembre. Solo `ayer` da «no es fecha», y es el único caso del test. **La frase que la IA escribió hoy en 2.8 (H-05) describe mal el código**: para esos textos se muestra una fecha inventada. Solo ocurriría con un dato corrupto, porque el backend siempre envía `2026-11-12T15:05:00Z` | **Lo decide el Tech Lead.** **Recomendada**: que `formatDateTime` acepte solo la forma del contrato (fecha, `T`, hora y zona) y muestre como llega todo lo demás, sin pasarlo por `Date`; 2.8 diría «que no tiene la forma del contrato». Test en rojo antes, con los tres textos. **Alternativa**: no tocar el código y que 2.8 diga lo que hace hoy; deja a la vista una fecha falsa en un caso que no debería darse | `core/format.ts`, `core/format.spec.ts` y SPEC-04 (2.8, historial) |
| N-08 · Ningún test fija el `role="alert"` de los mensajes de campo del simulador, que 2.7 nombra desde hoy | baja | **Sí.** La IA escribió la regla en 2.7 (H-04) y solo puso tests en el alta, que era lo que cambiaba | Un test en el simulador: con un texto no válido, el mensaje del campo lleva `role="alert"`, y el campo lo señala. Nace en verde: mutación (quitar el `role`) | `simulador.spec.ts` |
| N-09 · Dos filas de 5.5 se cumplen fuera del test del simulador: la de la zona horaria, en Playwright, y «la simulación nueva es la primera», en CA-14 | baja | **Sí en el hecho.** No falta ninguna prueba: es la redacción de CA-08, que dice que los tests del simulador «reproducen cada fila» | Precisar CA-08: esas dos filas las reproducen `e2e/rate-date.spec.ts` y la prueba de CA-14. Con historial | SPEC-04 (CA-08, historial) |

## 2. Lo que la IA ha comprobado

Todo en solo lectura; ningún fichero del repositorio ha cambiado por estas
comprobaciones.

| Qué | Cómo | Resultado |
|---|---|---|
| El informe guardado es el del evaluador | Comparación del fichero con el mensaje que consta en el registro del subagente, con el mismo script de la primera vez (14:13:47) | **Idénticos**: 362 líneas y 34.340 caracteres los dos, ninguna línea distinta. **Ningún carácter invisible** ni de control en el mensaje: esta vez los nombró todos por su código |
| Qué agente y qué modelo respondió | Fichero de metadatos y registro del subagente | Tipo de agente `evaluador`. Las 96 respuestas del registro llevan el modelo `claude-opus-5-5` |
| Qué ejecutó | Recuento de sus llamadas en el registro | 45 órdenes de terminal y 12 lecturas de fichero. Ninguna herramienta de escritura: no la tiene. Trabajó de 14:00:55 a 14:08:44 según su cabecera |
| Estado tras el evaluador | `git status --short`, `netstat` y la carpeta temporal (14:11:32) | Árbol limpio en `7f8c974`; nada escucha en el 8000, el 4200, el 18765 (el puerto de su backend) ni en ningún 80xx; ninguna carpeta `saas-o-matic-e2e-*` |
| Cuántas filas tienen las cuatro tablas | Recuento de las líneas de tabla de 5.3 a 5.6 de SPEC-04 | 24, 40, 29 y 16, sin la cabecera: las que dice el informe |
| N-01 | Lectura de `alta.spec.ts:471` | No mira el botón. La búsqueda de la sesión (AE-11) ya había dado solo `api-error.spec.ts:169` |
| N-02 | Lectura de `simulador.spec.ts:664-684` | Como dice el informe |
| N-03, una muestra | Lectura de `alta.spec.ts:471`, `simulador.spec.ts:379` y `:544`, y búsqueda de «Elige» en `alta.spec.ts` | Sin aserción del cuerpo; ninguna aparición de «Elige»; `:379` no cuenta peticiones antes de los 200 ms |
| N-04 | Lectura de `panel.spec.ts:147`, `:179`, `:191` y `:304`, y búsqueda de quién llama a `MetaStore.load()` | Como dice el informe. Solo lo llama `app.config.ts:25` |
| N-05 | Lectura de `panel.spec.ts:464` y `:473` y de `simulador.spec.ts:489` | Solo comprueban el texto del aviso |
| N-07 | `new Date(…)` con Node 24.18.0 para cinco textos, y lectura de `format.spec.ts:60-90` | `Ejemplo 7`, `1` y `12/11/2026` dan una fecha; `ayer`, no. El test de `:64` es el único de `formatDateTime`; el de `:80` es de `formatRateDate` |
| N-08 | Búsqueda de `role` en `simulador.spec.ts` | Cinco apariciones, ninguna sobre un mensaje de campo |
| Los números de línea del informe | Longitud de cada fichero citado y búsqueda de lo citado, en las referencias a ficheros que no son los tests de la parte A | Quince referencias apuntan a líneas que no existen o no son esas (fila C-01). Las demás que la IA ha mirado son correctas, entre ellas `customer-loader.ts:37`, `alta.ts:55-59`, `api-error.ts:114-119`, `format.ts:75-79`, `detalle.spec.ts:336`, `simulador.spec.ts:783`, `alta.spec.ts:589` y `:606`, y las de `_router-chunk.mjs` |

## 3. Cinco casos más

No son hallazgos del informe: salen de leerlo y de compararlo.

| # | Caso | Qué propone la IA |
|---|---|---|
| C-01 | **Al menos quince números de línea del informe son erróneos**; lo que afirman es cierto, pero no está en esa línea. `simulador.html:496`, `:512` y `:528` son las líneas 42, 58 y 74 (el fichero tiene 111); `panel.html:155` es la 19; `controls.css:56`, la 18; `playwright.config.ts:268`, la 27; `playwright.capturas.config.ts:18-21`, la 13 (tiene 14); `capturas.spec.ts:153`, la 113 (tiene 144); `meta-store.spec.ts:253`, la 104 (tiene 144); `app.routes.spec.ts:85-96` son las líneas 49 a 59 y su comentario viejo, «:45-46», está en la 8 y la 9 (tiene 74); y `alta-help.ts:203-206`, `simulador-help.ts:408-410`, `simulador-view.ts:395-401` y `projector.ts:301-302` caen fuera de ficheros de 86, 52, 95 y 101 líneas. Los de los tests que la IA ha abierto (apartado 2) y los de SPEC-04 son correctos | Ninguna: el informe no se toca. Quien siga una de esas referencias tiene aquí la línea buena de las que la IA ha localizado. **Causa probable**: son posiciones dentro de una salida con varios ficheros seguidos; `controls.css:56` es 18 más las 38 líneas de `tokens.css`. La IA no ha repasado las referencias una a una en los tests de la parte A más allá de las del apartado 2 |
| C-02 | El informe deja **tres detalles sin llevar a hallazgo**: el párrafo «Sobre CA-12 a CA-15» de SPEC-04 habla ya de CA-19 sin que su título lo diga; el `describe` de `app.routes.spec.ts` sigue citando solo E-34 y su comentario («The rows of the four views join this file as each view arrives») quedó viejo; y la comprobación del oráculo se llama «Playwright: principio a fin y 375 px», sin nombrar el contraste que ya ejecuta | Los dos primeros, una línea cada uno, si el Tech Lead quiere. El tercero está en `scripts/`, que no se toca sin que él lo mande |
| C-03 | **La parte B da su veredicto casi sin citas**: «Sí» en cada código, con pocas referencias `fichero:línea`, y el evaluador dice haber leído de las specs del backend los apartados 2.12 y 4 de SPEC-01, el 4 de SPEC-02 y el 4 de SPEC-03. No contrastó con el OpenAPI publicado (lo dice él) | Ninguna. **La IA no ha repetido la parte B** (apartado 5): su «ninguna diferencia» es la palabra del evaluador, apoyada en su sondeo del backend real |
| C-04 | **Error de la IA en la precisión AE-11** de la bitácora: decía que la regla de `created_at` la fijaban «dos tests de `format.spec.ts`». Es uno, el de `:64`; el de `:80` es de la fecha del tipo de cambio. La IA los encontró con una búsqueda y no abrió el fichero | Queda corregido en la bitácora, con una nota junto a AE-11 |
| C-05 | Las filas que el informe marca con «Sí» en la parte A (77 de las 109, contadas por la IA sobre sus tablas; las otras 32 son «Parcial») **son la lectura del evaluador**: la IA solo ha abierto tests de las marcadas como «Parcial» | Ninguna. Queda dicho en el apartado 5 |

## 4. Decisión del Tech Lead

Pendiente. Esta respuesta se entrega en la parada 3 de la sesión 08 sin
aplicar nada.

## 5. Lo que esta respuesta no demuestra

- **La parte B entera**: la IA no ha repetido la comparación del contrato
  con `core/models.ts` ni la tabla de códigos.
- **Las filas marcadas «Sí» de la parte A**: la IA no ha abierto esos
  tests.
- **N-06 y N-07 en un navegador**: salen del código del router y de Node,
  que usa el mismo motor que Chromium; la IA no arranca el frontend fuera
  de Playwright y no ha escrito una prueba, porque sería aplicar algo.
- **Que las mutaciones propuestas muerdan**: ninguna está hecha.
- **Nada con un lector de pantalla** (limitación L-10), que afecta a N-06 y
  a N-08.
- **Que no haya más**: el evaluador trabajó menos de ocho minutos sobre 109
  filas y tres specs.
