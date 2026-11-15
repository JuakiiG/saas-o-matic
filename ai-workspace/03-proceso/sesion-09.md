# Sesión 09 · Documentación de entrega e integración continua

| | |
|---|---|
| **Fecha** | 2026-11-15 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | **Sesión cerrada en la parada 2 (17:56): los tres cambios de la revisión de la parada 1, aplicados.** La parada 1 se aprobó a las 17:40, con AG-01 a AG-12 admitidas; el script de la trazabilidad se queda y el Tech Lead ha comprobado los tres SHA del workflow. **Tres commits**, cada uno con el oráculo en código 0 antes, con `--e2e` los dos que tocan `frontend/`: **E-16** (`426be86`), la prueba del detalle a 375 px lo cita en su título y la matriz queda en **140 de 140**; **AG-07** (`eaed046`), SPEC-04 dice que «Reintentar» de `/meta` repite solo `/meta`, sin cambiar el comportamiento, con una fila en 5.3 y un test nuevo en el panel que nace en verde y matan dos mutaciones, la primera **solo él** (1 de 566); y el **README** (`59b0a00`), con una captura y la frase del `npm ci`. El frontend acaba con **566 tests unitarios y 18 de Playwright**. **Lo que el Tech Lead tiene que conocer**: (1) **en el detalle y en el simulador pasa lo mismo que en el panel con la carga del cliente, y en el simulador también con la proyección**; está dicho en SPEC-04 (2.1) y **ningún test lo fija** (no se ha añadido); (2) la IA tocó además la frase de 2.5, que decía lo mismo sin condición (AH-02); (3) para mirarlo escribió tres tests temporales y los borró (AH-03); (4) la matriz se regeneró dos veces, porque el test nuevo cambia sus cifras (AH-04). Quedan sin aprobar AH-01 a AH-06. El guion de pruebas manuales sigue sin ejecutar y la integración continua, sin ejecutarse: la prueba en limpio y el `push` son del Tech Lead. · **Antes, parada 1 alcanzada (16:55): los cinco pasos, hechos, cada uno en su commit y con el oráculo en código 0 antes; pasada final con `--e2e` en código 0 (24 correctas).** No ha cambiado nada en `backend/` ni en `frontend/`. **Paso 1** (`4ab6986`): `04-calidad/trazabilidad.md`, generada con `uv run scripts/traceability.py`; de 140 requisitos EARS, 139 tienen algún test que los cita y **uno no, SPEC-04/E-16**, cubierto por CA-13; nada corregido. **Paso 2** (`69d2b3b`): `04-calidad/pruebas-manuales.md`, 30 pasos, con la columna de resultados vacía. **Paso 3** (`d7cb4af`): `.github/workflows/ci.yml`, en Linux y en Windows, con tres acciones fijadas por el SHA de su commit; **no se ha ejecutado ni se puede antes del `push`**. **Paso 4** (`1c0ab2e` y `8cbcc25`): el README de la raíz. **Paso 5** (`a7684a1`): `ai-workspace/README.md`. **Lo que el Tech Lead tiene que conocer**: (1) la matriz la genera un script nuevo en `scripts/`, con 21 tests, que el encargo no pedía (AG-01); (2) en SPEC-04 la cita va casi siempre en el `describe`: solo 10 de sus 57 requisitos tienen un test que los cite en su propio título, y 21 tests del frontend citan un apartado y no un requisito (AG-03 a AG-05); (3) la IA no ha ejecutado el guion en un navegador (AG-06); (4) leyendo el código para el guion: tras recargar el panel con el backend parado hacen falta dos «Reintentar», y SPEC-04 no lo dice (AG-07); (5) dos órdenes del README, las de arranque, no las ha ejecutado la IA tal cual, por la regla 8: las ejecuta Playwright (AG-08); (6) para el margen de una semana la IA consultó además la API pública de GitHub (AG-09); (7) ningún analizador ha leído la sintaxis del workflow. Quedan sin aprobar AG-01 a AG-12. · Antes, sesión abierta a las 16:14 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

**La conversación es nueva**, sin el contexto de la sesión 08: la IA llega
con lo que ha leído al empezar (`CLAUDE.md`, `README.md`,
`ai-workspace/README.md`, `04-calidad/limitaciones-conocidas.md` y la
bitácora de la sesión 08, con sus pendientes) y con sus cuatro notas de
memoria, no con lo que hizo esta mañana.

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 09: documentación de entrega e integración continua. Antes de
> nada, leer `CLAUDE.md`, `README.md`, `ai-workspace/README.md`,
> `04-calidad/limitaciones-conocidas.md` y los pendientes de
> `03-proceso/sesion-08.md`. Abrir esta bitácora con el mismo formato que
> las anteriores.
>
> Parada 4 de la sesión 08 aprobada. Admitidas AF-01 a AF-09. AF-05: bien
> hecho; los dos tests se quedan; el permiso se apoyaba en una afirmación
> que nadie había probado. AF-01: admitido; la forma exigida es la que
> escribe el backend y la spec lo dice. AF-07: admitida la falta; el commit
> depende del código de salida del oráculo, sin filtros en medio.
>
> En esta sesión no cambia el código de la aplicación. Un commit por paso.
> El oráculo sin `--e2e` antes de cada commit y una pasada final con
> `--e2e`, siempre por su código de salida. Si algo obliga a tocar
> `backend/` o `frontend/src`, parar y preguntar.
>
> **Paso 1. Trazabilidad.** `ai-workspace/README.md` promete en
> `04-calidad` una matriz de requisito a test que no existe. Crearla en
> `04-calidad/trazabilidad.md`: por cada spec, una fila por requisito EARS
> con cuántos tests lo citan y en qué ficheros, contando backend, frontend
> y Playwright. Sacarla de las citas reales de los tests, con una orden que
> quede escrita en el propio documento, y poner la fecha y el commit sobre
> el que se generó. Los requisitos sin ningún test que los cite van en una
> lista aparte, cada uno con el criterio que lo cubre o «sin cubrir». No
> arreglar ninguno: los decide el Tech Lead.
>
> **Paso 2. `04-calidad/pruebas-manuales.md`.** Un guion para que el Tech
> Lead lo ejecute a mano en unos 15 minutos, con los dos servidores
> arrancados como dirá el README. Pasos numerados, cada uno con lo que hay
> que hacer, lo que se debe ver y el requisito o criterio del que sale. La
> columna del resultado se queda vacía: la rellena él, con fecha, navegador
> y commit. Que incluya al menos: alta de un cliente, detalle, simulador,
> guardar, y la simulación nueva la primera; un alta con errores (el foco
> va al primer campo con error); un identificador fiscal no válido y un
> duplicado; otra divisa (importes, tipo y fecha) y la API de divisas sin
> conexión, con las herramientas del navegador; el backend parado (el aviso
> y «Reintentar»); una dirección que no existe y `/clientes/%31`; el título
> de la pestaña en las cinco vistas; el tabulador por el alta (se ve el
> anillo de foco, también sobre el botón «Guardar»); 375 px de ancho en las
> cuatro vistas, con las herramientas del navegador; y Ctrl+C a mitad de
> `npm run e2e` (los puertos 8000 y 4200 quedan libres y no queda carpeta
> temporal).
>
> **Paso 3. Integración continua.** `.github/workflows/ci.yml`, que ejecute
> lo mismo que se ejecuta en local: el oráculo con `--e2e`. En Linux y en
> Windows (hasta hoy el proyecto solo se ha probado en Windows: el job de
> Linux será la primera prueba fuera). `uv`, Python y Node en las versiones
> que usa el proyecto. `npm ci`. El navegador de Playwright, solo Chromium,
> con sus dependencias de sistema en Linux. Cada acción fijada por su SHA
> completo, con la versión en un comentario; decir de dónde sale cada SHA y,
> si hace falta la red para consultarlo, pedirlo antes. Permisos mínimos
> (`contents: read`), sin secretos, con tiempo máximo, en `push` y en
> `pull_request`. El oráculo lee la historia de git: comprobar qué necesita
> del checkout. No se puede ejecutar antes del `push`: decirlo en la
> bitácora. Sin insignia en el README y sin afirmar que pasa: lo verá el
> Tech Lead tras el `push` y se corrige entonces lo que falle.
>
> **Paso 4. `README.md` de la raíz**, para quien clona el repositorio y
> quiere verlo funcionar en pocos pasos. Corto: se lee en tres minutos y
> enlaza lo demás. Qué es, en tres líneas, fuera el «en desarrollo».
> Requisitos, con las versiones exactas con las que se ha probado. Arranque
> del backend y del frontend, con las órdenes exactas; se abre en
> `http://localhost:4200`, no en `127.0.0.1`, y por qué; qué pasa con la
> base de datos la primera vez. Datos para probar: un identificador fiscal
> válido de cada país admitido, sin script de datos de ejemplo. Tests y
> oráculo: las órdenes, cuántos tests hay, y que las pruebas de Playwright
> descargan Chromium una vez (origen y tamaño), usan los puertos 8000 y
> 4200 y solo funcionan en Chromium. Configuración: las variables de
> entorno que existen y su valor por defecto. Qué necesita internet: la API
> de divisas, y qué se ve si falla, y `/docs`. Límites, sin esconderlos:
> enlace a `limitaciones-conocidas.md`, sin copiar la tabla, y además: solo
> probado en Windows 11, los avisos de `npm audit` con su número de hoy,
> dos ejecuciones de Playwright a la vez se estorban, y el céntimo que
> puede bailar entre el desglose y el total en otra divisa. Cómo se ha
> hecho y por dónde leerlo: enlace a `ai-workspace/README.md`. **Reglas del
> README**: cada orden, ejecutada tal como está escrita, o decir cuál no y
> por qué; con la regla 8, los servidores de la IA van en otros puertos;
> las cifras se copian de una salida de hoy; nada de nombres de quien
> propone el reto.
>
> **Paso 5. `ai-workspace/README.md`.** El apartado «Estado», al día. Un
> recorrido de cinco minutos: qué leer primero para ver el método (una
> spec, un ADR, una bitácora, una evaluación con su respuesta y la
> trazabilidad). La fila de `04-calidad` dice lo que hay de verdad.
>
> **Parar ahí (parada 1)**: qué se ha escrito, qué órdenes del README no se
> han podido ejecutar tal cual, qué requisitos salen sin test, qué acciones
> y qué SHA usa el workflow, y qué no se ha podido comprobar. La prueba en
> limpio y el `push` los hace el Tech Lead.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 16:14 | — | Mensaje recibido a las 16:13 (primera lectura del reloj, 16:13:12). `git status` limpio; el último commit es `7845574` (2026-11-15 15:47:40), el último de la sesión 08. Lecturas del encargo hechas, y además `scripts/check.py` con los módulos del oráculo que usan git, `frontend/package.json`, `frontend/playwright.config.ts`, `backend/pyproject.toml` y `.claude/rules/frontend.md`. **`netstat` a las 16:14:12: nada escucha en el 8000, el 4200, el 8001 ni el 4201.** Existe `backend/data/saas-o-matic.db`, que es del Tech Lead (28.672 bytes, 2026-11-14 18:37): la IA no lo toca. No existe `.github/`. Apertura de esta bitácora |
| 16:25 | `f2379c4` | **Apertura de la bitácora**, 16:17:12 según `git log`, tras el oráculo sin `--e2e` de 16:15:26 a 16:17:12, código 0 (23 correctas, 1 inactiva); la salida, a un fichero, y el commit, en la misma orden, solo con ese código |
| 16:25 | — | **Paso 1, exploración** (16:18 a 16:20, solo lectura): cómo cita cada grupo de tests. El backend, en el docstring de cada función y siempre con la forma completa (`SPEC-01/E-01, SPEC-01/E-02`); el frontend, casi siempre en el título del `describe` y con listas y rangos (`SPEC-04/E-05 a E-11, E-40 a E-46`); Playwright, en el título de cada prueba. **Una búsqueda de texto no sirve**: contaría solo el primer identificador de cada lista y daría por no citados casi todos los requisitos de SPEC-04. La IA decide escribir un script (AG-01) |
| 16:25 | — | **Paso 1, el script, con TDD.** Esqueletos sin lógica y 20 tests nuevos en `scripts/tests/`; **rojo visto a las 16:20:43**: 18 fallan por aserción, 1 por un índice sobre la lista vacía que devuelve el esqueleto y 1 pasa ya (AG-02). **Verde a las 16:22:07**, los 20. Primera salida real: la matriz deja ver 21 tests del frontend sin ninguna cita; test nuevo para listarlos, **rojo por aserción a las 16:22:44** y verde a las 16:22:56 (21 tests) |
| 16:25 | — | **Paso 1, la matriz** (16:24): `uv run scripts/traceability.py`, código 0. **140 requisitos; 139 con algún test que los cita; 1 sin ninguno, SPEC-04/E-16**, que cubre CA-13. Contraste de los totales con recuentos hechos de otra forma (apartado 4). Cifras de hoy de los tres *runners* (16:23:45 a 16:24:08): 741, 565 y 18 más 4 capturas. `04-calidad/trazabilidad.md` escrito: los apartados 1 a 3, a mano; el 4, la salida de la orden, comparada byte a byte con una segunda ejecución |
| 16:32 | `4ab6986` | **Paso 1**, 16:27:29 según `git log`: `04-calidad/trazabilidad.md`, `scripts/traceability.py`, el paquete `scripts/tracematrix/` y sus dos ficheros de tests. Antes, con todo añadido, oráculo sin `--e2e` de 16:25:46 a 16:27:29, código 0: 23 correctas y 1 inactiva; los tests del oráculo y del hook pasan de 75 a 96 |
| 16:32 | — | **Paso 2, datos del guion** (16:28:37 a 16:29:39). `netstat`: nada en el 8011. Backend de la IA en `127.0.0.1:8011` con `DATABASE_PATH` en la carpeta de trabajo de la sesión, fuera del repositorio; la espera mira el PID que escucha (24632). Sondeo con un script de usar y tirar (apartado 4): el `422` de control, el de formato, el alta con `b-1234567.4`, el `409`, un alta en cada uno de los otros ocho países, las proyecciones de 10 y 15 usuarios, dos simulaciones y su orden, `/customers/%31`, la búsqueda y `/docs`. **Parado por su PID**; después, nada en el 8011, la base temporal borrada y `backend/data/saas-o-matic.db` igual (28.672 bytes, 2026-11-14 18:37) |
| 16:32 | — | **Paso 2, el guion**: `04-calidad/pruebas-manuales.md`, 30 pasos en ocho bloques, con la columna «Resultado» vacía y una tabla de fecha, navegador, sistema y commit para quien lo ejecute. Los textos, copiados de las plantillas y del código; los importes, de las respuestas del sondeo. **La IA no lo ha ejecutado en un navegador** (AG-06). Al leer el código para el paso del backend parado: tras recargar el panel sin backend hacen falta dos «Reintentar», el de `/meta` y el de la lista (AG-07). Las órdenes de PowerShell del paso 30 no se han podido ejecutar: la orden fue denegada por los permisos de la sesión (apartado 5) |
| 16:38 | `69d2b3b` | **Paso 2**, 16:34:13 según `git log`: `04-calidad/pruebas-manuales.md`. Antes, oráculo sin `--e2e` de 16:32:28 a 16:34:13, código 0: 23 correctas y 1 inactiva |
| 16:38 | — | **El paso 3 se deja para después del 4 y el 5**: necesita la red para consultar los SHA de las acciones, y el encargo manda pedirlo antes. La IA adelanta lo que no depende de la respuesta. **Los commits irán en el orden de los pasos** |
| 16:38 | — | **Paso 4, las órdenes del README, ejecutadas tal como están escritas** (apartado 4): `npm audit` (16:34:01; 27 avisos moderados); `npm ci` en `frontend/` (16:34:35 a 16:35:26, código 0; acaba con el aviso de `npm audit` y con el de cuatro paquetes con scripts de instalación sin aprobar); `npx playwright install --only-shell chromium` (16:35:37, código 0, sin nada que descargar: ya estaba) y antes la misma con `--dry-run`, para el origen y el destino; tres peticiones `HEAD` para el tamaño (16:35:58); y `uv run --locked pytest` en `backend/` (16:36:10 a 16:36:38: 741 en verde). **No ejecutadas tal cual por la IA**: `uv run --locked uvicorn --factory app.main:create_app` y `npm start`, que usan el 8000 y el 4200 (regla 8); las ejecuta Playwright, con esas mismas palabras, en cada pasada con `--e2e` (AG-08). `README.md` reescrito; sin commit todavía |
| 16:38 | — | **Paso 5**: `ai-workspace/README.md`: la fila de `04-calidad` dice lo que hay, un apartado «Recorrido de cinco minutos» con cinco documentos y el apartado «Estado» al día, con lo pendiente separado de lo hecho. Comprobado que cada cosa que el recorrido promete está en el documento enlazado (apartado 4). Sin commit todavía |
| 16:45 | — | **Paso 3, la pregunta** (16:38 a 16:42): la IA pide permiso para tres lecturas con `git ls-remote` y propone tres acciones. **El Tech Lead responde que sí, y que lea además el `action.yml` de cada una**, con dos condiciones (apartado 3): el SHA es el del commit y la versión cumple el margen de una semana |
| 16:45 | — | **Paso 3, los SHA** (16:42:40 a 16:43): `git ls-remote --tags` de los tres repositorios; la última versión de cada uno; su fecha de publicación, de la API pública de GitHub (AG-09); y, con `git fetch --depth 1` de cada SHA a una carpeta fuera del repositorio, que el objeto es un commit y su `action.yml` (tabla en el apartado 3). **Las tres etiquetas son ligeras**: no tienen línea `^{}` y su SHA ya es el del commit. Las tres versiones, anteriores al 2026-11-06 |
| 16:45 | — | **Paso 3, el workflow**: `.github/workflows/ci.yml`. Un job en matriz, Linux y Windows, que ejecuta `uv run scripts/check.py --e2e`. `fetch-depth: 0`, porque el oráculo lee toda la historia (apartado 3). **No se puede ejecutar antes del `push`** y ningún analizador ha leído su sintaxis: no hay ninguno instalado y la IA no ha descargado uno (apartado 5). Sin insignia en el README. Sin commit todavía |
| 16:55 | `d7cb4af` | **Paso 3**, 16:47:24 según `git log`: `.github/workflows/ci.yml`. Antes, oráculo sin `--e2e` de 16:45:37 a 16:47:24, código 0 |
| 16:55 | `1c0ab2e` | **Paso 4**, 16:49:12: `README.md`. Antes, oráculo sin `--e2e` de 16:47:24 a 16:49:12, código 0 |
| 16:55 | `a7684a1` | **Paso 5**, 16:50:49: `ai-workspace/README.md`. Antes, oráculo sin `--e2e` de 16:49:12 a 16:50:49, código 0. Los tres commits, en una sola orden: cada uno solo se hace si su pasada del oráculo sale con código 0, sin filtros en medio (AG-11) |
| 16:55 | — | **Pasada final con `--e2e`**, de 16:50:49 a 16:52:45, sobre `a7684a1`: **código 0, 24 correctas, 0 con fallo y 0 inactivas**. Después, nada en escucha en el 8000 ni en el 4200, ninguna carpeta `saas-o-matic-e2e-*` y `backend/data/saas-o-matic.db` igual. Es además la primera pasada completa después del `npm ci` de las 16:34 |
| 16:55 | `8cbcc25` | **Tres erratas del README**, 16:54:59, que la IA vio al releerlo ya en su commit: «país y importes»; «una sola orden» seguida de dos; y «el nombre y el email son libres», cuando el email tiene que tener forma de email. Commit aparte, sin enmendar. Antes, oráculo sin `--e2e` de 16:53:20 a 16:54:59, código 0. **Después de la pasada con `--e2e` solo han cambiado este README y esta bitácora** |
| 16:55 | *(este commit)* | Cierre de esta bitácora para la **parada 1**. La IA para aquí: el Tech Lead revisa los cinco pasos y las precisiones AG-01 a AG-12. La prueba en limpio y el `push` son suyos. La hora de este commit se ve con `git log` |
| 17:42 | — | El commit anterior es `f82184e` (16:57:20 según `git log`), tras el oráculo sin `--e2e` de 16:55:43 a 16:57:20, código 0. **El Tech Lead aprueba la parada 1** (mensaje leído a las 17:40:41): admite AG-01 a AG-12, se queda el script de la trazabilidad, ha comprobado los tres SHA contra sus etiquetas y coinciden, y manda tres cambios, un commit cada uno, con el oráculo en código 0 y con `--e2e` donde se toque `frontend/`; después, **parada 2** y cierre de la bitácora (apartado 3). `git status` limpio; nada escucha en el 8000 ni en el 4200 |
| 17:42 | — | **Cambio 1 (E-16)**, sin commit todavía. El título de la prueba del detalle de `frontend/e2e/responsive.spec.ts` acaba en `(SPEC-04/CA-13, E-16)`; `npx playwright test --list` lo enseña. Matriz regenerada a las 17:41:33: **140 de 140**; E-16 tiene un test, citado en su propio título, y en SPEC-04 son 11, no 10, los requisitos con una cita directa. `trazabilidad.md`: cabecera, apartados 2 y 3 y el apartado 4, que es la salida nueva, comparada byte a byte con otra ejecución. `ai-workspace/README.md`: «140 de 140» |
| 17:51 | `426be86` | **Cambio 1 (E-16)**, 17:45:03 según `git log`. Antes, oráculo con `--e2e` de 17:42:45 a 17:45:03, código 0: 24 correctas, 0 con fallo y 0 inactivas; puertos libres y sin carpeta temporal después |
| 17:51 | — | **Cambio 2 (AG-07), el test.** Un test nuevo en `panel.spec.ts`: `/meta` falla con un `500` y la lista con un `503`, para distinguir un aviso del otro; tras «Reintentar» de `/meta` con éxito, ninguna petición a `/customers`, el buscador a la vista y un solo aviso, el de la lista, con su «Reintentar»; al pulsarlo, una petición sin `q`, ninguna a `/meta`, y la lista con nombres. **Nace en verde** (17:45:41; 36 tests en el fichero). **Dos mutaciones**, cada una con los 566 tests. La primera, el panel repite la búsqueda cuando `/meta` se recupera de un error: **falla solo el test nuevo** (17:46:40; 1 de 566, «expected 1 to be 0» en las peticiones a `/customers`). Un primer intento, a las 17:46:08, era demasiado grueso (repetía cualquier búsqueda fallida, también con `/meta` bien) y rompía 11; se rehízo (AH-01). La segunda, el «Reintentar» de la lista reintenta `/meta`: 6 fallos, el nuevo entre ellos (17:47:10). Deshechas; `git diff` sin nada en `frontend/src` fuera del test |
| 17:51 | — | **Cambio 2, el detalle y el simulador** (17:48:20 y 17:48:54): **pasa lo mismo con el cliente, y en el simulador también con la proyección.** Visto con tres tests temporales, uno al final de `detalle.spec.ts` y dos al final de `simulador.spec.ts`, **borrados después**; los dos ficheros quedan idénticos a como estaban, comparados byte a byte con una copia hecha antes (AH-03). **Ningún test lo fija y no se ha añadido ninguno** (apartado 3) |
| 17:51 | — | **Cambio 2, los documentos.** SPEC-04: un párrafo nuevo en 2.1, la frase de 2.2, una condición en la de 2.5 (AH-02), una fila en 5.3 y su fila de historial. El paso 22 del guion ya no pide anotar: dice que hacen falta las dos pulsaciones. **La matriz, regenerada otra vez** (17:50:37), porque el test nuevo cambia sus cifras: 250 declaraciones del frontend, 566 casos y E-40 con 103; sigue en 140 de 140 (AH-04). Sin commit todavía |
| 17:51 | — | **Cambio 3 (README)**, sin commit todavía: la captura `simulador-usd-1280.png` bajo la descripción, enlazada desde `ai-workspace/04-calidad/capturas/` y sin copiar; la frase de que el oráculo necesita antes el `npm ci` del frontend; y «566 del frontend» (AH-04). La IA ha mirado la captura: el simulador con 15 usuarios en USD, con 155,95, 32,75 y 188,69 USD, que es el caso del céntimo |
| 17:56 | `eaed046` | **Cambio 2 (AG-07)**, 17:53:51 según `git log`. Antes, oráculo con `--e2e` de 17:51:52 a 17:53:51, código 0: 24 correctas, 0 con fallo y 0 inactivas, con los 566 tests del frontend. Puertos libres y sin carpeta temporal después. **Es la última pasada con `--e2e` de la sesión y el último commit que toca `frontend/`** |
| 17:56 | `59b0a00` | **Cambio 3 (README)**, 17:55:28. Antes, oráculo sin `--e2e` de 17:53:52 a 17:55:28, código 0: 23 correctas y 1 inactiva. `backend/data/saas-o-matic.db`, igual que al empezar |
| 17:56 | *(este commit)* | **Cierre de esta bitácora en la parada 2.** La IA para aquí: el Tech Lead revisa los tres cambios y las precisiones AH-01 a AH-06. La prueba en limpio y el `push` son suyos. La hora de este commit se ve con `git log` |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (16:13)

**Parada 4 de la sesión 08, aprobada. Admitidas AF-01 a AF-09.**

| Precisión | Decisión del Tech Lead |
|---|---|
| AF-05 (el test de `panel.spec.ts` que la IA no quitó) | **Bien hecho. Los dos tests se quedan.** Su permiso se apoyaba en una afirmación que nadie había probado |
| AF-01 (`formatDateTime` muestra crudo lo que no tiene la forma del contrato) | **Admitido.** La forma exigida es la que escribe el backend y la spec lo dice |
| AF-07 (un commit encadenado a un `grep`) | **Admitida la falta.** El commit depende del código de salida del oráculo, sin filtros en medio |
| AF-02, AF-03, AF-04, AF-06, AF-08 y AF-09 | Admitidas, sin comentario |

La bitácora de la sesión 08 no se toca: la aprobación queda anotada aquí,
como la de AB-01 a AB-07 quedó en la de la sesión 08.

**Reglas de esta sesión**, del encargo:

- **No cambia el código de la aplicación.** Si algo obliga a tocar
  `backend/` o `frontend/src`, la IA para y pregunta.
- **Un commit por paso**, con el oráculo sin `--e2e` antes de cada uno y
  una pasada final con `--e2e`; el commit depende del código de salida.
- **La prueba en limpio y el `push` son del Tech Lead.** La integración
  continua no se puede ejecutar antes del `push`.

### Pasos 1, 2, 4 y 5 · lo hecho

| Paso | Qué hay | Commit |
|---|---|---|
| 1 | `04-calidad/trazabilidad.md`: cómo se cuenta, lo que la matriz dice y lo que no, la lista de requisitos sin test y la matriz, que es la salida de `uv run scripts/traceability.py`. El script, el paquete `scripts/tracematrix/` (dos módulos, 265 líneas) y 21 tests | `4ab6986` |
| 2 | `04-calidad/pruebas-manuales.md`: 30 pasos en ocho bloques, con la columna «Resultado» vacía | `69d2b3b` |
| 4 | `README.md` de la raíz, reescrito | `1c0ab2e` y, con tres erratas, `8cbcc25` |
| 5 | `ai-workspace/README.md`: la fila de `04-calidad`, el recorrido de cinco minutos y el apartado «Estado» | `a7684a1` |

**Lo que sale de la matriz** (paso 1):

- **140 requisitos; 139 con algún test que los cita; 1 sin ninguno:
  SPEC-04/E-16** (el detalle sin desplazamiento horizontal a 375 px). Lo
  cubre CA-13: la prueba de Playwright del detalle cita `SPEC-04/CA-13`, y
  E-16 solo aparece en el comentario de cabecera del fichero. Ninguno queda
  «sin cubrir». **No se ha corregido nada.**
- **En SPEC-04 la cita va casi siempre en el `describe`**: solo 10 de sus
  57 requisitos tienen algún test que los cite en su propio título; 46 se
  citan solo desde un bloque. El número de la matriz dice ahí cuántos tests
  hay en bloques que nombran el requisito, no cuántos lo comprueban.
- **E-06 y E-19** solo se citan dentro de un rango; su criterio, CA-12, es
  la revisión del evaluador, no un test.
- **21 tests del frontend no citan ningún requisito**: citan un apartado de
  SPEC-04 (2.1, 2.2, 2.6, 2.7 o 2.8) que no tiene requisito EARS.
- Ninguna cita apunta a algo que no exista.

**Las órdenes del README** (paso 4), una a una:

| Orden | ¿Ejecutada tal como está escrita? |
|---|---|
| `uv run --locked uvicorn --factory app.main:create_app`, en `backend/` | **No por la IA**: usa el 8000 y la base local del Tech Lead (regla 8). La IA la ejecutó con `--port 8011` y `DATABASE_PATH` aparte. Tal cual la ejecuta Playwright en cada pasada con `--e2e`, con `DATABASE_PATH` temporal |
| `npm ci`, en `frontend/` | Sí (16:34:35), código 0 |
| `npm start`, en `frontend/` | **No por la IA**: usa el 4200 (regla 8). La ejecuta Playwright en cada pasada con `--e2e` |
| `uv run scripts/check.py` | Sí, antes de cada commit |
| `uv run scripts/check.py --e2e` | Sí, en la pasada final |
| `npx playwright install --only-shell chromium`, en `frontend/` | Sí (16:35:37), código 0, **pero sin descargar nada**: el navegador ya estaba. La descarga de verdad es la de la sesión 08 |
| `uv run --locked pytest`, en `backend/` | Sí (16:36:10): 741 en verde |
| `npm run test:ci` y `npm run e2e`, en `frontend/` | Las ejecuta el oráculo, con esas palabras; la IA no las ha lanzado sueltas |

Precisiones de la IA, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| AG-01 | **La matriz la genera un script nuevo, no una búsqueda de texto**: `scripts/traceability.py` y el paquete `scripts/tracematrix/`, con 21 tests en `scripts/tests/`. El encargo pedía «una orden»; no pedía código. No toca `backend/` ni `frontend/`. El paquete no se llama `trace` porque taparía un módulo de la biblioteca estándar | Las citas del frontend son listas y rangos (`SPEC-04/E-05 a E-11, E-40 a E-46`): una búsqueda de `SPEC-nn/E-nn` cuenta solo el primero de cada lista y daría por no citados casi todos los requisitos de SPEC-04. Si el Tech Lead no quiere el script, se quita y la matriz queda sin orden que la regenere |
| AG-02 | **De los 20 primeros tests del script, uno no se vio en rojo**: el de «un identificador sin su spec no es una cita» espera un conjunto vacío, que es justo lo que devuelve el esqueleto. Otro falló por un índice sobre la lista vacía y no por aserción. Los otros 18 y el test añadido después, por aserción. El script va en un solo commit con su documento, no en un commit por tarea | La regla 2 pide ver el rojo por aserción. Un commit por paso es lo que mandaba el encargo |
| AG-03 | **Se cuentan declaraciones de test, no casos**: 183, 249 y 14, frente a los 741, 565 y 18 más 4 que ejecutan los *runners*. Y la matriz lleva una columna que el encargo no pedía, **«En su título»**: cuántos tests citan el requisito ellos mismos y no por heredarlo de su bloque | Contar casos exige ejecutar los tres *runners* y casar su salida con los docstrings. La columna es lo que deja ver que en el frontend el número está inflado; sin ella E-40 tendría «102 tests» |
| AG-04 | **Qué es una cita lo ha decidido la IA**: `SPEC-nn/` seguido de identificadores unidos por coma, «y» o «a»; en el título o el docstring, no en un comentario; y un `(CA-05)` o un `(E-29)` sin su spec delante no cuenta. Los criterios no tienen filas | Sin una regla estricta, una mención en prosa contaría como cita. Con esta, E-16 sale sin test aunque el comentario de cabecera de `responsive.spec.ts` lo nombra |
| AG-05 | **La lectura de la matriz (apartado 2 de `trazabilidad.md`) es de la IA**, no salida del script: los 46 requisitos citados solo desde un bloque, E-06 y E-19, y los 21 tests que citan un apartado. La IA no ha comprobado test a test qué requisito comprueba cada uno | El Tech Lead tiene que saber qué parte es dato y qué parte es lectura |
| AG-06 | **La IA no ha ejecutado el guion de pruebas manuales en un navegador.** Los textos salen de las plantillas y del código; los importes, de las respuestas de un backend propio en el 8011. Lo que el guion espera del navegador (el foco, el anillo, los títulos, la barra de direcciones, las herramientas de desarrollo) sale de leer el código y las specs | Sus servidores no pueden usar el 8000 ni el 4200, y el frontend solo habla con el backend desde `http://localhost:4200` |
| AG-07 | **Al escribir el paso 22 del guion, leyendo `panel.ts` y `meta-gate.ts`: si el panel se recarga con el backend parado, hacen falta dos «Reintentar»**, el de `/meta` y después el de la lista, que también falló. SPEC-04 (2.2) dice que cuando `/meta` «se reintenta con éxito, la lista ya está y no hace falta pedirla otra vez», y eso solo es cierto si la lista no falló. No visto en pantalla. **No se ha tocado nada**: el guion pide anotarlo | Puede ser una regla que falta en la spec o un comportamiento que cambiar; lo decide el Tech Lead |
| AG-08 | **Tres frases del README no salen de haberlo visto**: que desde `http://127.0.0.1:4200` se ve «No se ha podido conectar con el servidor.» (sale de SPEC-04, 2.9); que `/docs` queda en blanco sin conexión (la IA vio que su HTML carga de `cdn.jsdelivr.net`, no la página sin red); y que la primera vez se crea `backend/data/saas-o-matic.db` (visto con otra ruta, y lo fija el test de SPEC-03/CA-12) | El encargo pide decir qué no se ha ejecutado tal cual |
| AG-09 | **Para cumplir el margen de una semana la IA usó dos accesos a la red que no había nombrado en su pregunta**: la API pública de GitHub (`api.github.com/repos/…/releases`), para la fecha de publicación de cada versión, y `git fetch --depth 1` de cada SHA, para comprobar que es un commit y leer su `action.yml` (en vez de `raw.githubusercontent.com`). Son lecturas anónimas y no envían nada del proyecto. En esta sesión la red se ha usado además para `npm audit`, `npm ci` y tres peticiones `HEAD` a `cdn.playwright.dev` | `git ls-remote` no da fechas, y las tres etiquetas son ligeras: no llevan fecha propia. El Tech Lead tiene que saber todo lo que ha salido a la red |
| AG-10 | **Decisiones del workflow que el encargo no fijaba**: Python «3.12» y no 3.12.0; `ubuntu-latest` y `windows-latest`; sin caché de uv ni de npm; `push` en cualquier rama y `pull_request`, de modo que una rama del propio repositorio con *pull request* se ejecuta dos veces; sin subir las trazas de Playwright como artefacto; 20 minutos de máximo, puestos a ojo: en local el oráculo con `--e2e` tarda dos | Cada una tiene alternativa. La de las trazas puede hacer falta: si algo falla en Linux, el oráculo solo enseña las últimas 15 líneas de la herramienta que falla |
| AG-11 | **Los commits de los pasos 3, 4 y 5 se hicieron seguidos, al final**, cada uno tras su propia pasada del oráculo, pero con los ficheros de los otros pasos ya escritos en el árbol y sin añadir. Y el README no nombra la integración continua: dice «solo se ha probado en Windows 11»; que el workflow está escrito y sin ejecutar lo dice `ai-workspace/README.md` | El paso 3 esperaba el permiso de red y la IA adelantó el 4 y el 5. Una frase sobre la integración continua en el README quedaría falsa tras su primera ejecución |
| AG-12 | **Dos órdenes de la IA fueron denegadas por los permisos de la sesión** y no se han rodeado: una de PowerShell, para probar las órdenes del paso 30 del guion, y un borrado recursivo de la carpeta de la base temporal, que se borró después fichero a fichero | Las órdenes de PowerShell y las de Linux y macOS del paso 30 quedan sin ejecutar |

### Permiso para consultar la red: pregunta de la IA y respuesta del Tech Lead (16:38–16:42)

La IA preguntó si podía leer con `git ls-remote --tags` las etiquetas de
`actions/checkout`, `actions/setup-node` y `astral-sh/setup-uv`, con tres
opciones: solo eso (la que recomendaba); eso y el `action.yml` de cada
acción; o no consultar y dejar un marcador en el sitio de cada SHA.

**El Tech Lead eligió la segunda y añadió dos condiciones**: «El SHA que se
fija es el del commit, no el del objeto de la etiqueta: en las etiquetas
anotadas es la línea que acaba en `^{}`. Y la versión cumple el margen de
una semana del proyecto.»

### Paso 3 · las acciones y sus SHA

| Acción | Versión | SHA del commit | Publicada | De dónde sale |
|---|---|---|---|---|
| `actions/checkout` | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` | 2026-07-20 | `git ls-remote --tags https://github.com/actions/checkout`, línea `refs/tags/v7.0.1`; la etiqueta `v7` apunta al mismo SHA |
| `actions/setup-node` | v7.1.0 | `949feb2413d6458794dcd2491c4babbbce0c15c1` | 2026-10-08 | `git ls-remote --tags https://github.com/actions/setup-node`, línea `refs/tags/v7.1.0`; la etiqueta `v7` apunta al mismo SHA |
| `astral-sh/setup-uv` | v10.3.3 | `68559e99cc807c1eb7e9238fd43a15bba460eec2` | 2026-10-28 | `git ls-remote --tags https://github.com/astral-sh/setup-uv`, línea `refs/tags/v10.3.3`; la API da ese mismo SHA como destino de la versión |

- **El SHA es el del commit.** Ninguna de las tres etiquetas tiene línea
  `^{}`: son ligeras. Comprobado además trayendo cada SHA con
  `git fetch --depth 1` a una carpeta vacía fuera del repositorio:
  `git cat-file -t` dice `commit` en los tres.
- **El margen de una semana** (ADR-007). Cada una es la última versión de
  su repositorio y las tres son anteriores al 2026-11-06, la fecha de
  corte más antigua del proyecto. La fecha es el `published_at` de
  `https://api.github.com/repos/<repositorio>/releases` (AG-09).
- **Los parámetros**, leídos en el `action.yml` de cada SHA y no de
  memoria: `fetch-depth` y `persist-credentials` (`checkout`); `version`,
  `python-version` y `enable-cache` (`setup-uv`); `node-version` y
  `package-manager-cache` (`setup-node`). Las tres se ejecutan con
  `node24`.

**Qué necesita el oráculo del checkout.** Leído en `scripts/oracle/`:

| Comprobación | Qué lee de git | Qué pide del checkout |
|---|---|---|
| Ningún commit con trailer de coautoría | `git log` de toda la historia de `HEAD` | **Toda la historia**: `fetch-depth: 0`. Con la profundidad por defecto, 1, saldría en verde habiendo mirado un solo commit |
| `.private/` nunca versionado | `git log --all -- .private` | Lo mismo |
| Ningún CRLF | `git ls-files --eol` | Nada: `.gitattributes` fija LF en cualquier sistema |
| Los tests del oráculo | Crean sus propios repositorios, con su `user.name` y su `user.email` | Nada: no dependen de la identidad de git de la máquina |

En un `pull_request` el checkout trae el commit de fusión que crea GitHub;
su mensaje no lleva trailer.

**Lo que el workflow fija y lo que no.** uv 0.12.13 y Node.js 24.18.0, que
trae npm 11.16.0 (comprobado en la carpeta de Node de este equipo), son
exactos. **Python es «3.12», no 3.12.0**: es lo que piden
`backend/.python-version` y `pyproject.toml`, y uv elegirá la revisión que
encuentre o descargue (AG-10). Los sistemas son `ubuntu-latest` y
`windows-latest`, que cambian con el tiempo. Sin caché, sin secretos, con
`contents: read` y 20 minutos de máximo por job.

### Revisión de la parada 1 por el Tech Lead (17:40)

**Parada 1 aprobada. Admitidas AG-01 a AG-12.**

| Precisión | Decisión del Tech Lead |
|---|---|
| AG-01 (el script de la trazabilidad) | **Se queda**: tiene tests y el oráculo los ejecuta |
| Los tres SHA del workflow | **Comprobados por el Tech Lead contra sus etiquetas: coinciden** (lo afirma él) |
| AG-03 a AG-05 (los 21 tests que citan un apartado y las citas en el `describe`) | **Se queda como está**: la matriz ya lo explica |
| AG-10 (decisiones del workflow) | **Se quedan**, sin subir trazas. Si falla en Linux, lo reproduce él en local |
| AG-11 (el README no nombra la integración continua) | **Se queda** así hasta que él la vea ejecutarse |
| AG-08 (las tres frases del README que la IA no ha visto) | Las comprueba él en la prueba en limpio |

**Tres cambios**, un commit cada uno, con el oráculo en verde por su código
de salida y con `--e2e` donde se toque `frontend/`:

| # | Cambio |
|---|---|
| 1 | **E-16.** La prueba de Playwright del detalle a 375 px cita también `SPEC-04/E-16` en su título, además de CA-13. Regenerar la matriz y poner al día sus apartados 2 y 3 y la cifra de `ai-workspace/README.md`: 140 de 140 |
| 2 | **AG-07, los dos «Reintentar» del panel. No se cambia el comportamiento**: se escribe en SPEC-04 tal como está el código, con historial. La frase de 2.2 deja de decir que «la lista ya está» sin condición: si la lista también falló, tras reintentar `/meta` con éxito se ve el aviso de la lista, con su propio «Reintentar». *Por qué*: son dos peticiones y cada aviso reintenta la suya. Una fila en 5.3 y un test en el panel que lo fije; nace en verde, así que con mutación. Mirar si en el detalle y en el simulador pasa lo mismo con la carga del cliente: si pasa, decirlo en 2.1 y decir si hay test que lo fije, **sin añadirlo**. Poner al día el paso 22 del guion |
| 3 | **README de la raíz, dos retoques.** Una captura bajo la descripción: el simulador en otra divisa a 1280 px, enlazada desde `ai-workspace/04-calidad/capturas/`, sin copiar el fichero. Y en «Tests y oráculo», una frase: el oráculo necesita antes el `npm ci` del frontend |

Después, **parada 2** y cierre de esta bitácora.

### Cambios de la revisión de la parada 1 · lo hecho (desde las 17:41)

| # | Commit | Rojo visto o mutación | Qué toca |
|---|---|---|---|
| 1 · E-16 | `426be86` | Ninguno: solo cambia el título de una prueba | `frontend/e2e/responsive.spec.ts`, `04-calidad/trazabilidad.md` y `ai-workspace/README.md` |
| 2 · AG-07 | `eaed046` | **Mutación**, dos: el panel repite la búsqueda cuando `/meta` se recupera (**la mata solo el test nuevo**, 1 de 566) y el «Reintentar» de la lista reintenta `/meta` (6 fallos, el nuevo entre ellos) | `panel.spec.ts`, SPEC-04 (2.1, 2.2, 2.5, 5.3 e historial), `04-calidad/pruebas-manuales.md`, `04-calidad/trazabilidad.md` y `ai-workspace/README.md` |
| 3 · README | `59b0a00` | — | `README.md` |

**Tests del frontend al cerrar**: 566 unitarios (eran 565: uno más, el del
panel) y 18 de Playwright, más las 4 capturas.

**Qué pasa en el detalle y en el simulador** (cambio 2). Lo mismo que en
el panel. Las dos vistas piden el cliente por su cuenta, sin esperar a
`/meta`, y «Reintentar» de `/meta` solo repite `/meta`:

| Vista | Qué falla, además de `/meta` | Tras reintentar `/meta` con éxito | Al pulsar el segundo «Reintentar» | ¿Hay test que lo fije? |
|---|---|---|---|---|
| Panel | El listado inicial | El buscador y el aviso de la lista, con su «Reintentar»; ninguna petición a `/customers` | 1 a `/customers`, sin `q`; ninguna a `/meta`; la lista | **Sí, desde hoy** (`panel.spec.ts`) |
| Detalle | El cliente | El aviso del cliente, con su «Reintentar»; ninguna petición del cliente | 1 del cliente; ninguna a `/meta`; el detalle | **No** |
| Simulador | El cliente | El aviso del cliente, con su «Reintentar»; ninguna petición del cliente ni de proyección | 1 del cliente y, al llegar, 1 de proyección; el simulador con su total | **No** |
| Simulador | La primera proyección (el cliente llegó) | El simulador con el aviso de la proyección y su «Reintentar»; ninguna petición | 1 de proyección; el total | **No** |

Lo que sí tiene test en esas dos vistas es el caso contrario: `/meta`
falla y lo demás llega (el del detalle, «should show the error of /meta
with a retry…», y el del simulador, «should ask for the customer and its
first projection all the same, and appear loaded when /meta comes back»).
**No se ha añadido ninguno.**

Precisiones de la IA sobre estos cambios, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| AH-01 | **El primer intento de la primera mutación era demasiado grueso** (17:46:08): repetía la búsqueda con cualquier fallo de la lista, también con `/meta` bien, y rompía 11 tests. Se rehízo para que solo la repita cuando `/meta` pasa de error a datos, que es justo el comportamiento que el Tech Lead ha decidido no tener. No se cuenta. Con la rehecha, los otros 565 tests seguían en verde: el hueco era real | Como el intento descartado de N-04 en la sesión 08: una mutación que lo rompe todo no demuestra nada |
| AH-02 | **En SPEC-04 la IA ha tocado dos cosas que el encargo no nombraba**: la frase de 2.5 («al reintentar `/meta` el simulador aparece ya cargado»), que gana la condición «si esas dos peticiones salieron bien (2.1)»; y, en el párrafo de 2.1, además del cliente, **la proyección del simulador**, que es una tercera petición con su propio aviso | La frase de 2.5 decía sin condición lo mismo que se acaba de corregir en 2.2. Lo de la proyección salió del sondeo: no estaba en la pregunta, pero es el mismo caso |
| AH-03 | **Para mirar el detalle y el simulador la IA escribió tres tests temporales dentro de sus `.spec.ts` y los borró.** Al borrarlos con la herramienta de edición los dos ficheros perdieron el salto de línea final; se restauró y se comparó cada fichero, byte a byte, con una copia hecha antes fuera del repositorio | El encargo pedía mirar si pasa, sin añadir test. Leer el código ya lo decía (AG-07); el sondeo lo enseña. Un fichero sin su salto de línea final habría cambiado sin motivo |
| AH-04 | **La matriz se ha regenerado dos veces**, una en cada commit que cambia un test: en el cambio 1, por E-16, y en el 2, porque el test nuevo sube en uno las cifras del frontend (250 declaraciones, 566 casos, E-40 con 103). La cifra de `ai-workspace/README.md` va en el cambio 2. **La del README de la raíz («566 del frontend») va en el commit del cambio 3**: ese fichero ya tenía los dos retoques sin añadir, así que entre los dos commits decía 565 | El documento lleva la fecha y el commit de su generación; dejarlo atrás un commit lo habría hecho falso. Lo del README es una consecuencia del orden |
| AH-05 | **El test nuevo no cita un requisito en su título**: hereda los del `describe` del panel (E-40 entre ellos) y su comentario nombra 2.2 y 5.3. Usa dos errores distintos, un `500` para `/meta` y un `503` para la lista | Es como citan los demás tests del panel. Con el mismo error en las dos peticiones, los dos avisos tendrían el mismo texto y el test no sabría cuál está viendo |
| AH-06 | **La frase del README dice solo lo pedido**: que el oráculo necesita antes el `npm ci` del frontend. La IA no ha ejecutado el oráculo sin `frontend/node_modules`. **La captura no se ha visto dibujada en el README**: el enlace es relativo, a un fichero que existe | Borrar `node_modules` para verlo fallar no merecía el riesgo; lo verá el Tech Lead en la prueba en limpio |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git log -1` (16:14:12) | Limpio, `7845574` |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000, 4200, 8001 y 4201 (16:14:12) | Ninguno en escucha |
| Herramientas | `node --version`, `npm --version`, `uv --version`, `python --version`, `git --version` y `cmd /c ver` (16:14:12) | Node 24.18.0, npm 11.16.0, uv 0.12.13, Python 3.12.0, git 2.55.0.windows.3, Windows 10.0.26300.9974 |
| Navegador de Playwright ya descargado | Listado de la carpeta `ms-playwright` de los datos locales del usuario (16:14:12) | Las tres carpetas de la sesión 08: `chromium_headless_shell-1254`, `ffmpeg-1013` y `winldd-1007` |

Paso 1:

| Qué | Cómo | Resultado |
|---|---|---|
| Rojo y verde del script | `python -m unittest discover -s scripts/tests -t scripts -p "test_tracematrix*.py"` (16:20:43, 16:22:07, 16:22:44 y 16:22:56) | 18 fallos por aserción, 1 error y 1 correcto de 20; 20 en verde; 1 fallo por aserción de 21; 21 en verde |
| La matriz | `uv run scripts/traceability.py` (16:24) | Código 0; 185 líneas |
| **Los totales, contados de otra forma** | Funciones `test_…` con el módulo `ast` en un script aparte, y una búsqueda de las líneas que empiezan por `it` o `test` en los `.spec.ts` (16:23) | 183 en 23 ficheros, 249 en 19 y 14: los de la matriz |
| Requisitos por spec | Recuento de las filas `E-nn` de cada spec (16:19) | 35, 15, 33 y 57; ninguno repetido |
| El apartado 4 es la salida de la orden | Segunda ejecución y `cmp` con lo que hay bajo el marcador del documento (16:25) | Idénticos |
| Cifras de los *runners* | `uv run --locked pytest --collect-only -q`, `npx playwright test --list` con cada configuración y `npx ng test --watch=false` (16:23:45 a 16:24:08) | 741 recogidos; 18 pruebas en 5 ficheros y 4 capturas en 1; 565 en verde en 19 ficheros |
| `backend/` y `frontend/` sin cambios al generar | `git status --short backend frontend` (16:24:18) | Vacío |
| Finales de línea de lo nuevo | `git ls-files --eol -o --exclude-standard` (16:25) | Los siete ficheros, `w/lf` |

Paso 2:

| Qué | Cómo | Resultado |
|---|---|---|
| Puerto libre antes de arrancar | `netstat -ano` filtrado por `LISTENING` y los puertos 8011, 4211, 8000 y 4200 (16:28:37) | Ninguno en escucha |
| **Backend de la IA** | `uv run --locked uvicorn --factory app.main:create_app --port 8011`, con `DATABASE_PATH` en la carpeta de trabajo de la sesión; espera hasta ver en `netstat` el PID que escucha (16:29:05) | `127.0.0.1:8011`, PID 24632. La base, creada al arrancar: 28.672 bytes |
| **Los datos del guion y del README** | Script de usar y tirar con `urllib`, fuera del repositorio (16:29:05) | `B12345675`: `422` con `invalid_tax_id_check_character`. `B1234567`: `422` con `invalid_tax_id_format`. `b-1234567.4`: `201`, guardado como `B12345674`. El mismo otra vez: `409` `customer_already_exists`. Un `201` en cada uno de los otros ocho países con el identificador del README, y con `12345678Z`, `X1234567L` y `A12345674` en España. Proyección de 10 usuarios: 10000, 2100 y 12100 céntimos; de 15: 14000, 2940 y 16940. Dos simulaciones, de 15 y de 51 usuarios: el detalle las devuelve con la de 51 primero (51425 céntimos). `GET /customers/%31`: `200`. `GET /customers/999999`: `404` `customer_not_found`. `q=manual`: un cliente; `q=zzzz`: ninguno. `/docs`: `200`, y su HTML carga de `cdn.jsdelivr.net` |
| Parada del backend de la IA | `taskkill` con el PID 24632; después, `netstat` y un listado de `backend/data/` (16:29:39) | Nada en el 8011, el 8000 ni el 4200. `backend/data/saas-o-matic.db`, igual: 28.672 bytes, 2026-11-14 18:37. La base temporal, borrada |
| Los textos del guion | Lectura de las plantillas (`app.html`, `panel.html`, `alta.html`, `detalle.html`, `simulador.html`, `quote-panel.html`), de `alta-help.ts`, `simulador-help.ts`, `api-error.ts`, `rate-note.ts`, `not-found.ts`, `customer-not-found.ts`, `meta-gate.ts`, `panel.ts` y `styles/` (16:27 a 16:31) | Copiados de ahí. El anillo de foco es un contorno de 3 px del color de acento, separado 2 px del elemento |

Paso 4:

| Qué | Cómo | Resultado |
|---|---|---|
| `npm audit` | En `frontend/` (16:34:01) | 27 avisos, los 27 de gravedad moderada: como en L-07 |
| **`npm ci`** | En `frontend/` (16:34:35 a 16:35:26) | Código 0. Termina con el aviso de `npm audit` y con «4 packages have install scripts not yet covered by allowScripts» (`@parcel/watcher`, `esbuild`, `lmdb` y `msgpackr-extract`). `git status` no cambia |
| Origen y destino del navegador | `npx playwright install --dry-run --only-shell chromium` (16:35:37) | Chrome Headless Shell 158.0.8127.18, FFmpeg y winldd, de `cdn.playwright.dev`, a la carpeta `ms-playwright` de los datos locales del usuario |
| La orden de instalación, tal cual | `npx playwright install --only-shell chromium` (16:35:37) | Código 0, sin salida: ya estaba instalado |
| Tamaño de la descarga | `curl -sIL` a las tres direcciones (16:35:58) | 129.186.142, 1.663.577 y 128.684 bytes: 130.978.403 en total. El navegador llega redirigido de `storage.googleapis.com/chrome-for-testing-public`; los otros dos, de `playwright.download.prss.microsoft.com` |
| Tamaño en disco | `du -sb` de la carpeta `ms-playwright` (16:35:37) | 303.971.876 bytes |
| Tests del backend, con la orden del README | `uv run --locked pytest`, en `backend/` (16:36:10 a 16:36:38) | 741 en verde en 26 s |
| Variables de entorno que lee el proyecto | Búsqueda de `os.environ`, `getenv` y `process.env` en `backend/app`, `scripts/` y `frontend/` (16:33) | `CORS_ORIGINS` y `DATABASE_PATH` en `backend/app/config.py`. Además, `PATHEXT` en el oráculo y una variable interna de las pruebas de Playwright, que no son configuración |
| Qué npm trae Node 24.18.0 | `package.json` del npm que hay en la carpeta de Node (16:33) | 11.16.0 |

Paso 5:

| Qué | Cómo | Resultado |
|---|---|---|
| Lo que promete el recorrido existe | Títulos de `respuesta-evaluacion-frontend-02.md` y de ADR-002, recuento de los informes y de las filas de limitaciones, y búsqueda de AC-03 y AF-05 en la bitácora de la sesión 08 (16:38) | La respuesta tiene su apartado 4, «Decisión del Tech Lead»; ADR-002, sus «Opciones»; siete informes; once limitaciones; las dos precisiones están |

Paso 3:

| Qué | Cómo | Resultado |
|---|---|---|
| Etiquetas y SHA | `git ls-remote --tags https://github.com/<repositorio>`, tres veces (16:42:40) | Código 0 las tres. Tabla del apartado 3 |
| Fecha de publicación | `curl` a `https://api.github.com/repos/<repositorio>/releases?per_page=8`, tres veces (16:42:55) | v7.0.1, 2026-07-20; v7.1.0, 2026-10-08; v10.3.3, 2026-10-28. Ninguna es preliminar ni borrador |
| Cada SHA es un commit | `git fetch --depth 1` de cada SHA a una carpeta vacía de la carpeta de trabajo de la sesión, y `git cat-file -t` (16:43) | `commit` los tres. Nada de lo descargado se ha ejecutado |
| Parámetros de cada acción | `git show <SHA>:action.yml` (16:43) | Los que usa el workflow existen con ese nombre |
| **Sintaxis del workflow** | Lectura. Se buscó un analizador de YAML ya instalado, en `frontend/node_modules` y en Python (16:44) | **No hay ninguno: sin analizar** (apartado 5) |

Oráculo:

| Qué | Cómo | Resultado |
|---|---|---|
| **Antes de cada commit** | `uv run scripts/check.py`, con la salida a un fichero y el commit en la misma orden, solo con código 0. Siete pasadas, de las 16:15 a las 16:54, para los siete commits anteriores a este | Código 0 en las siete: 23 correctas, 0 con fallo y 1 inactiva (Playwright). Unos 105 s cada una |
| **Pasada final con `--e2e`** | `uv run scripts/check.py --e2e` (16:50:49 a 16:52:45), sobre `a7684a1` | Código 0: 24 correctas, 0 con fallo y 0 inactivas |
| Puertos y carpeta temporal después | `netstat` filtrado por `LISTENING` y los puertos 8000 y 4200, y un listado de la carpeta temporal del sistema (16:52:45 y 16:53:20) | Ninguno en escucha y ninguna carpeta `saas-o-matic-e2e-*` |
| La base local del Tech Lead | Listado de `backend/data/` al empezar, tras el sondeo y al acabar | Igual las tres veces: 28.672 bytes, 2026-11-14 18:37 |
| `backend/` y `frontend/` no han cambiado en la sesión | `git diff --stat 7845574 HEAD -- backend frontend` (al cerrar) | Vacío |

Cambios de la revisión de la parada 1:

| Qué | Cómo | Resultado |
|---|---|---|
| Estado al empezar | `git status --short`, `git log -1` y `netstat` (17:40:41) | Limpio, `f82184e`; nada en escucha en el 8000 ni en el 4200 |
| El título nuevo de la prueba del detalle | `npx playwright test --list` (17:41:33) | Una prueba, y solo una, con `E-16` en su título |
| La matriz, tras el cambio 1 | `uv run scripts/traceability.py` (17:41:33) y `cmp` con el apartado 4 del documento | Código 0. «Requisitos sin ningún test que los cite: Ninguno.» E-16: 1 test, en su propio título. Idénticos |
| El test nuevo del panel, en verde | `npx ng test --watch=false --include …/panel.spec.ts` (17:45:41) | 36 en verde |
| Mutación 1, primer intento | `npx ng test --watch=false`, los 566 tests (17:46:08) | 11 fallos: demasiado gruesa (AH-01) |
| **Mutación 1** | Lo mismo (17:46:40) | **1 fallo y 565 en verde**: el test nuevo, por aserción |
| **Mutación 2** | Lo mismo (17:47:10) | 6 fallos y 560 en verde; el nuevo, entre ellos |
| Las mutaciones están deshechas | `git status --short` y `git diff --stat -- frontend/src`, sin contar los `.spec.ts` (17:47) | Solo `panel.spec.ts` cambiado |
| **El detalle y el simulador** | Tres tests temporales, con las utilidades de sus `.spec.ts` (17:48:20 y 17:48:54) | Tabla del apartado 3 |
| Los tests temporales, borrados | `cmp` de `detalle.spec.ts` y de `simulador.spec.ts` con su copia de antes (17:49:41) | Idénticos los dos, tras restaurar el salto de línea final |
| Formato y lint del test nuevo | `npx prettier --check` y `npx eslint --max-warnings 0` sobre `panel.spec.ts` (17:51) | Código 0 los dos |
| La matriz, tras el cambio 2 | `uv run scripts/traceability.py` (17:50:37) y `cmp` con el apartado 4 | Código 0. 250 declaraciones del frontend, en 19 ficheros; E-40, 103; ningún requisito sin cita. Idénticos |
| La captura del README | Lectura de `04-calidad/capturas/simulador-usd-1280.png` (17:44) | El simulador con 15 usuarios en USD: 155,95, 32,75 y 188,69 USD, y «Total en EUR» 169,40 EUR |
| **Oráculo antes de cada commit** | `uv run scripts/check.py`, con `--e2e` en los cambios 1 y 2, que tocan `frontend/`; la salida, a un fichero, y el commit en la misma orden, solo con código 0 | Código 0 en todas (cronología) |
| Puertos y carpeta temporal tras cada pasada con `--e2e` | `netstat` y un listado de la carpeta temporal del sistema | Ninguno en escucha y ninguna carpeta `saas-o-matic-e2e-*` |

## 5. No verificado

Al llegar a la parada 2 (cierre de la sesión), además de lo de la parada
1, que sigue debajo:

- **Los dos «Reintentar» en un navegador**: en el panel, en el detalle y
  en el simulador se han visto en tests, no en pantalla. Es el paso 22 del
  guion.
- **El detalle y el simulador no tienen test** de ese caso: lo que dice el
  párrafo nuevo de 2.1 sobre ellos sale de tres tests temporales que ya no
  existen (AH-03).
- **La captura, dibujada en el README**, y el oráculo sin
  `frontend/node_modules` (AH-06).
- **Ningún evaluador ha mirado los cambios de esta sesión.**
- Lo que el Tech Lead ha dicho que comprueba él: los tres SHA (ya
  comprobados, según su mensaje), las tres frases de AG-08 y la
  integración continua tras el `push`.

Al llegar a la parada 1:

- **El workflow no se ha ejecutado nunca.** No se puede antes del `push`.
  No se sabe si su sintaxis es válida para GitHub, si las tres acciones
  funcionan con esos parámetros, si `npx playwright install --with-deps`
  instala lo que Chromium necesita en `ubuntu-latest`, ni cuánto tarda.
  **Ningún analizador ha leído el fichero**: no hay ninguno instalado y la
  IA no ha descargado uno.
- **Nada del proyecto se ha ejecutado fuera de Windows.** El job de Linux
  sería la primera vez. Lo que puede fallar allí y no se ha podido mirar:
  cómo resuelve `localhost` el servidor de desarrollo de Angular (en este
  equipo escucha solo en `[::1]:4200`), la revisión de Python 3.12 que
  elija uv y el SQLite que traiga.
- **El guion de pruebas manuales, entero** (AG-06). En particular, lo que
  ya estaba sin ver en la sesión 08: el anillo azul sobre el botón azul, la
  barra de direcciones con `/clientes/%31`, los títulos en un navegador y
  la ejecución de Playwright interrumpida con Ctrl+C. Y los dos
  «Reintentar» del paso 22 (AG-07).
- **Las órdenes del paso 30 del guion**: las de PowerShell y las de Linux y
  macOS no se han ejecutado (AG-12). Las equivalentes de Git Bash, sí.
- **El texto del menú de Chrome para bloquear un dominio** (paso 18): la
  IA lo cita en inglés, de memoria.
- **Las órdenes de arranque del README en los puertos 8000 y 4200 y con la
  base por defecto**, lanzadas por una persona (tabla del apartado 3), y
  las tres frases de AG-08.
- **Un clon limpio.** `npm ci` se ha ejecutado sobre la copia de trabajo,
  con la caché de npm y el entorno de uv ya creados. La prueba en limpio
  es del Tech Lead.
- **Que el README se lea en tres minutos**: no se ha medido.
- **La matriz no dice qué comprueba cada test**: dice qué citan (AG-05). Y
  su lector de TypeScript depende del formato de Prettier: un fichero sin
  formatear daría otros números. El oráculo comprueba el formato de
  `frontend/`.
- **Los cuatro scripts de instalación sin aprobar** que anuncia `npm ci`:
  siguen como en la sesión 08; la IA no ha mirado qué supone para quien
  clona.
- **Nada con lector de pantalla** (L-10), como en la sesión 08.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Paso 1: `04-calidad/trazabilidad.md`~~ | Hecho (`4ab6986`) |
| ~~Paso 2: `04-calidad/pruebas-manuales.md`~~ | Hecho (`69d2b3b`) |
| ~~Paso 3: `.github/workflows/ci.yml`~~ | Hecho (`d7cb4af`). **Sin ejecutar** |
| ~~Paso 4: `README.md` de la raíz~~ | Hecho (`1c0ab2e` y `8cbcc25`) |
| ~~Paso 5: `ai-workspace/README.md`~~ | Hecho (`a7684a1`) |
| ~~**Parada 1: la revisa el Tech Lead.** Las precisiones AG-01 a AG-12~~ | Aprobada a las 17:40, con AG-01 a AG-12 admitidas y sus tres cambios aplicados (`426be86`, `eaed046` y `59b0a00`) |
| ~~**Decidir SPEC-04/E-16**, el único requisito sin test que lo cite~~ | Decidido y hecho (`426be86`): la prueba del detalle lo cita en su título. 140 de 140 |
| ~~**Decidir lo que la matriz deja ver y no se ha tocado**: los 21 tests del frontend que citan un apartado y no un requisito; E-06 y E-19; y si las citas del frontend deben bajar del `describe` a cada test~~ | Decidido a las 17:40: se queda como está; la matriz ya lo explica |
| ~~**Decidir los dos «Reintentar» del panel** (AG-07)~~ | Decidido y hecho (`eaed046`): no cambia el comportamiento; escrito en SPEC-04, con un test en el panel |
| **Parada 2: el Tech Lead revisa** los tres cambios y las precisiones AH-01 a AH-06. En particular, **si el detalle y el simulador deben tener un test del caso de los dos «Reintentar»**: hoy está dicho en SPEC-04 (2.1) y no lo fija ninguno | Ahora |
| **Ejecutar el guion de pruebas manuales** y rellenar su columna de resultados, con fecha, navegador y commit. Incluye la ejecución interrumpida con Ctrl+C y la pasada con el tabulador, heredadas de la sesión 08 | Del Tech Lead |
| **Prueba en limpio y `push`**. Tras el `push`, ver el primer resultado de la integración continua en Linux y en Windows y corregir lo que falle | Del Tech Lead; la corrección, en una sesión nueva |
| Poner al día `ai-workspace/README.md` («Estado») y el README de la raíz («solo se ha probado en Windows 11») cuando la integración continua y el guion tengan resultado | Entonces |
| Pendientes heredados que esta sesión no toca: L-07 y los avisos de `npm audit`, los cuatro scripts de instalación sin aprobar, las fechas del fichero de bloqueo en el oráculo y los de la sesión 06 | A decidir por el Tech Lead |
