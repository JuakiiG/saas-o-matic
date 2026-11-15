# Sesión 08 · Fase de QA del frontend, primera parte: Playwright, capturas y evaluación independiente

| | |
|---|---|
| **Fecha** | 2026-11-15 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | **Parada 3 alcanzada (14:20): los hallazgos de la primera evaluación, aplicados, y una segunda evaluación acotada.** La parada 2 se aprobó a las 13:11, con AD-01 a AD-10 admitidas y cada hallazgo decidido. **Diez commits, uno por hallazgo** (`35d482a` a `13351c9`), cada uno con el oráculo con `--e2e` en código 0: H-01 (el `id` ya descodificado, en la spec y en los tests), H-02 (anillo de foco azul y borde de los campos en una variable propia, con una prueba de Playwright del contraste, CA-19, y catorce capturas), H-03 (título por ruta, E-57), H-04 (los mensajes de campo del alta sin `role="alert"`), H-05 (tres reglas a la spec), H-06, H-07, H-08 (las capturas, en su propia configuración de Playwright), H-09 y H-10; limitaciones nuevas L-10 y L-11. **Rojo visto por aserción** en H-02 (dos veces), H-03 y H-04; **mutación** en H-01 y H-09. **La segunda evaluación** (subagente, Opus 5.5, de 14:00 a 14:08, en solo lectura; informe en `8045884`, idéntico a su mensaje, y respuesta de la IA, sin aplicar nada, en `5eb8d8a`): las 109 filas de 5.3 a 5.6 tienen test, pero **CA-04, CA-05, CA-08 y CA-16 salen `NO CUMPLE`** porque varios tests no comprueban todo lo que el criterio pide; ninguna diferencia en el contrato; los diez cambios se sostienen; **9 hallazgos, dos medios y siete bajos**, ninguno por un comportamiento que falle salvo N-07. **Lo que el Tech Lead tiene que conocer**: (1) la mutación de H-01 solo mata la mitad de los casos: el de `%31` lo resuelve el router de Angular (AE-02); (2) la página «no encontrada» no tiene título y conserva el de la vista anterior (AE-08, N-06): falta su decisión; (3) **N-07**: la frase que la IA escribió hoy en 2.8 no es cierta para cualquier texto, porque `Date` lee `Ejemplo 7` como una fecha; (4) un test de la sesión 07 no puede fallar (`panel.spec.ts:304`, N-04); (5) al menos quince números de línea del segundo informe son erróneos (AE-17); (6) las capturas que hay que mirar son las de `f6d0d04` (AE-12). Quedan sin aprobar AE-01 a AE-18 y sin decidir N-01 a N-09 y C-01 a C-05. · **Antes, parada 2 alcanzada (12:43): evaluación independiente del frontend.** Antes, la parada 1 aprobada a las 12:04 y sus cinco cambios, un commit cada uno (`e75ea0b` a `377233c`): la regla 7, los tipos de `e2e/` dentro de `npm run lint` (sin ningún error de tipos), SPEC-04, las reglas del frontend y las capturas sin foco. **El evaluador** (subagente, Opus 5.5, de 12:23 a 12:32, en solo lectura): CA-12 cumple; los 56 requisitos cumplen; de los 18 criterios, 17 cumplen (cuatro por muestreo) y CA-15 queda sin demostrar porque no puede leer las capturas; **10 hallazgos, uno medio (H-02, el contraste del anillo de foco y del borde de los campos) y nueve bajos**. Informe en `c149ca0` y respuesta de la IA, sin aplicar nada, en `be9fef7`. **Lo que el Tech Lead tiene que conocer**: (1) el informe guardado difiere del mensaje del evaluador en un carácter, un U+00A0 de la línea 43, que la IA no ha restaurado (AD-06); (2) dos hallazgos son errores de la IA de esta sesión: la prueba de la fecha cita E-27 y es E-29 (H-07), y `npx playwright test` sin opciones reescribiría las capturas (H-08); (3) el evaluador revisó cuatro criterios por muestreo y no leyó enteras las specs del backend. Quedan sin aprobar AD-01 a AD-10 y sin decidir H-01 a H-10 y B-01 a B-04. · **Antes, parada 1 alcanzada (11:37): Playwright y las capturas de CA-15.** `@playwright/test` 1.65.0 instalado y catorce pruebas en `frontend/e2e/` (CA-14, CA-13 con la cabecera del aviso, L-09 y la fila de la zona horaria), en un commit (`895f55d`); el oráculo sale con código 0 con `--e2e` (24 correctas, 0 inactivas) y sin él sigue como ayer (23 y 1 inactiva). Las pruebas tardan unos 20 s con el arranque de los dos servidores. Doce capturas en `04-calidad/capturas/` y CA-15 cambiado en SPEC-04. **Lo que el Tech Lead tiene que conocer**: (1) **la primera mutación de CA-14 sobrevivió**: con la API de divisas interceptada con `page.route()`, Playwright respondía él mismo a las comprobaciones previas de CORS y la prueba no comprobaba el CORS del backend; se cambió el mecanismo (protocolo de depuración de Chromium, solo para la URL de los tipos) y la mutación muere (AC-03); (2) la IA ha hecho los commits sin que se le pidiera cada uno (AC-01); (3) son catorce pruebas, no cuatro, y L-09 cubre todos los límites y no un campo (AC-08); (4) los ficheros de `e2e/` no los compila nadie con tipos (AC-09). Quedan sin aprobar las precisiones AC-01 a AC-18. **El paso 3 (evaluador) no se ha empezado**: espera la aprobación de esta parada. · Antes, sesión abierta a las 10:46 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

**La conversación es nueva**, sin el contexto de la sesión 07: la IA llega
con lo que ha leído al empezar (`CLAUDE.md`, `.claude/rules/frontend.md`,
ADR-005, SPEC-04, `04-calidad/limitaciones-conocidas.md` y la bitácora de
la sesión 07) y con sus cuatro notas de memoria, no con lo que hizo ayer.

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 08: fase de QA del frontend, primera parte. Antes de nada, leer
> `CLAUDE.md`, `.claude/rules/frontend.md`, ADR-005, los criterios CA-12 a
> CA-15 de SPEC-04, `04-calidad/limitaciones-conocidas.md` y el apartado 6
> de `03-proceso/sesion-07.md`. Abrir esta bitácora con el mismo formato
> que las anteriores.
>
> Admitidas AB-01 a AB-07 de la sesión 07. La lectura de las dos frases
> cortadas era correcta. El aviso compacto de la cabecera está visto en
> Chrome con la API de divisas caída: 130 px de alto en escritorio, con el
> texto y «Reintentar» en una línea, y 187 px a 375 px, con el selector en
> su sitio y sin desplazamiento horizontal. También está vista la espera
> agotada real de los tipos: a los 5 s sale el aviso y una respuesta que
> llega después no lo cambia. Y al reintentar se ve «Cargando tipos…» y el
> botón desaparece.
>
> **Cambio de una decisión de ayer. Playwright NO lleva configuración
> propia**: usa los puertos por defecto, 8000 y 4200. Por qué: CA-14 pide el
> backend real con su CORS por defecto, y así se prueba exactamente lo que
> ejecutará quien revise, sin una tercera configuración del frontend que
> SPEC-04 no nombra. Condiciones: los dos servidores los arranca Playwright
> con `webServer`, con `reuseExistingServer` en `false`, escrito de forma
> explícita (si un puerto está ocupado, la prueba falla sin tocar nada;
> nunca se reutiliza un servidor ya arrancado); el backend de la prueba
> lleva `DATABASE_PATH` en una carpeta temporal, fuera de `backend/data/`,
> que se crea y se borra en cada ejecución; es la única excepción a la
> regla de las 17:36 de ayer sobre el 8000 y el 4200, solo vale para lo que
> arranca Playwright y se escribe en la regla 8 de `CLAUDE.md`, con su
> porqué; la API de divisas se intercepta en el navegador de la prueba con
> tipos fijos, y ningún test llama a un servicio externo; no se toca
> `scripts/`, porque el oráculo ya ejecuta `npm run e2e` con `--e2e`. La
> anotación del apartado 6 de la sesión 07 se corrige con esta decisión,
> sin borrar la anterior: se tacha y se dice por qué cambió.
>
> **Paso 1. Playwright.** Instalar `@playwright/test` 1.65.0 como
> dependencia de desarrollo, con el margen de una semana de
> `frontend/.npmrc`, y comprobar las fechas de las entradas nuevas del
> fichero de bloqueo, como con el armazón. Antes de descargar el navegador
> de Playwright, decir origen y tamaño y esperar el sí; solo Chromium. Las
> pruebas, en `frontend/e2e/`, cada una citando su requisito: (1) CA-14:
> alta de un cliente, simulador, guardar y la simulación aparece la primera
> en el detalle; (2) CA-13: a 375 px ninguna de las cuatro vistas tiene
> desplazamiento horizontal, y además la cabecera con el aviso del fallo de
> los tipos; (3) L-09: un valor en el límite de un campo se guarda y uno un
> paso más allá lo rechazan la ayuda y el backend; (4) la fila de 5.5 de la
> zona horaria: con el navegador en `America/Los_Angeles` y otra divisa
> elegida, la fecha del tipo es la de la respuesta. Nacen en verde: se
> demuestra que cada una muerde con una mutación, se deshace y se anota qué
> se rompió y qué falló. El oráculo con `--e2e` en verde, mirando su código
> de salida, antes del commit; y sin `--e2e` sigue igual que hoy. Al
> terminar, los puertos 8000 y 4200 libres y ninguna carpeta temporal sin
> borrar, comprobado con `netstat`.
>
> **Paso 2. Capturas de CA-15.** Generar con Playwright las capturas de las
> cuatro vistas a 375 px y a 1280 px, con datos de ejemplo, en
> `04-calidad/capturas/`, más una del simulador con otra divisa y una de la
> cabecera con el aviso del fallo. CA-15 dice «capturas manuales»: se
> cambia en SPEC-04, con historial, por «capturas generadas con Playwright
> y revisadas por el Tech Lead». Las revisa él en la parada.
>
> **Parar ahí (parada 1)**: qué pruebas hay, qué mutación mató cada una,
> cuánto tardan, qué se ha descargado y dónde ha quedado, y qué no se ha
> podido comprobar.
>
> **Paso 3, solo cuando el Tech Lead apruebe la parada 1.** Evaluación
> independiente del frontend, con el subagente evaluador, en solo lectura y
> con las restricciones de siempre (no lee `03-proceso`, `04-calidad` ni la
> historia de git). Tres cosas: CA-12 (que `frontend/src` no contiene la
> tarifa, los tipos impositivos, la tabla de letras del DNI ni el cálculo
> del CIF); el frontend contra SPEC-04 y contra el contrato real del
> backend (requisitos sin test, tests que no comprueban lo que dicen,
> reglas del código que la spec no dice y cualquier defecto que encuentre
> ejecutando la aplicación); y accesibilidad básica, seguridad del lado del
> navegador y lo que un revisor exigente señalaría. El informe, intacto, en
> `04-calidad/evaluacion-frontend-01.md`, comparado con el mensaje del
> subagente antes de guardarlo; la respuesta de la IA, sin aplicar nada, en
> `04-calidad/respuesta-evaluacion-frontend-01.md`.
>
> **Parar ahí (parada 2)**: el Tech Lead decide cada hallazgo. El README,
> el documento de pruebas manuales y la integración continua vienen
> después.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 10:46 | — | Mensaje recibido a las 10:43 (primera lectura del reloj, 10:43:14). `git status` limpio; el último commit es `2fdf99f` (2026-11-14 19:16:03), el cierre de la sesión 07. Lecturas del encargo hechas. **`netstat` a las 10:46:12: nada escucha en el 8000 ni en el 4200.** Existe `backend/data/`, que es del Tech Lead: la IA no lo toca. Apertura de esta bitácora |
| 11:37 | `4b17ff6`, `dc47ccc` | Fila escrita a las 11:37, como todas las que siguen hasta la de la parada: **la IA no fue anotando al momento** y las horas salen de las órdenes ejecutadas, que llevaban `date` (AC-18). Dos commits de documentación, los dos a las 10:50:00 según `git log`, con el oráculo en código 0 antes (10:49:46): la regla 8 de `CLAUDE.md`, con la regla de los puertos y su excepción, y esta bitácora con la fila del apartado 6 de la sesión 07 tachada y su porqué |
| 11:37 | — | **Instalación** (10:50:16): `npm install --save-dev @playwright/test@1.65.0`, con `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`. Tres entradas nuevas en el fichero de bloqueo y ninguna más cambiada; las tres del 2026-11-05, anteriores a la fecha de corte (apartado 4). `npm audit` sigue en 27 avisos moderados (L-07). Ningún navegador descargado |
| 11:37 | — | **Origen y tamaño de Chromium, sin descargar** (10:51): `npx playwright install --dry-run` y cuatro peticiones `HEAD` (apartado 4). La IA lo preguntó y paró. **El Tech Lead eligió «solo el headless shell»**; la descarga, de 11:05:12 a 11:07:43 |
| 11:37 | — | **Configuración y primera prueba, CA-14** (11:10:57): los dos servidores arrancan, el recorrido completo pasa el CORS real y la prueba **falla por un error de la propia prueba**: esperaba «500» donde el detalle muestra «500 GB». Corregida la expectativa, no el código (AC-13). Puertos libres y carpeta temporal borrada después |
| 11:37 | — | **Las catorce pruebas, en verde a la primera** (11:13:58 a 11:14:18; 18,7 s según Playwright). A las 11:14:59, otra ejecución observada desde fuera: qué PID escucha en cada puerto, la carpeta temporal mientras dura y la base del Tech Lead antes y después (apartado 4) |
| 11:37 | — | **La primera mutación de CA-14 sobrevive** (11:15:44): con una cabecera propia en cada `POST`, el recorrido **pasa**. Causa, leída en el código de Playwright 1.65.0: con cualquier ruta interceptada (`page.route()` o `context.route()`), Playwright responde él mismo a toda comprobación previa de CORS con un `204` que admite el origen, el método y las cabeceras pedidas. La IA interceptaba así la API de divisas en todas las pruebas, de modo que **ninguna comprobación previa llegaba al backend** (AC-03). Cambio: la API de divisas se responde por el protocolo de depuración de Chromium, solo para su URL, y el navegador se lanza sin poder resolver ningún nombre que no sea local. Un primer intento (11:18:00) falló por un error de la IA en esa regla, que dejaba fuera también `127.0.0.1`; corregido |
| 11:37 | — | **Mutaciones** (11:19:09 a 11:26:27): doce ejecuciones con veintiuna mutaciones, en `frontend/src` y en `backend/app`, cada una hecha y deshecha con las herramientas de edición (tabla en el apartado 3). Todas hacen fallar la prueba que vigila lo roto. `git diff` vacío en `backend/` y `frontend/src` al acabar |
| 11:37 | — | **Puerto ocupado** (11:27:25): una segunda ejecución lanzada mientras la primera tenía los dos servidores en escucha termina en 2 s con código 1 y «`http://localhost:8000 is already used`», sin tocar los servidores. **Pero hizo fallar una prueba de la primera**: Playwright vacía `test-results/` al empezar, antes de mirar los puertos, y se llevó la traza que la primera estaba escribiendo (apartado 5) |
| 11:37 | `895f55d` | **Commit de Playwright y sus pruebas** (11:34:12 según `git log`). Antes, con todo añadido (`git add`): oráculo sin `--e2e`, código 0, 23 correctas y 1 inactiva (11:30:26 a 11:32:04); oráculo con `--e2e`, código 0, 24 correctas y 0 inactivas (11:32:04 a 11:33:59). Una pasada anterior con `--e2e`, a las 11:28:10, también en 0. Las salidas, guardadas en ficheros; el commit, solo después de ver el código |
| 11:37 | — | **Paso 2, capturas** (11:35:00 a 11:35:14): `npm run e2e:capturas` escribe doce ficheros en `04-calidad/capturas/`. La IA ha mirado tres. CA-15 cambiado en SPEC-04, con su fila de historial, y una nota fechada en ADR-005 (AC-11 y AC-12) |
| 11:43 | `949b414`, `f5a1254`, `6123e69` | Tres commits, a las 11:42:50 y 11:42:51 según `git log`: el generador con las doce capturas, CA-15 en SPEC-04 y ADR-005. Antes, con todo añadido, oráculo sin `--e2e` (11:39:00 a 11:40:33) y con `--e2e` (11:40:33 a 11:42:29), los dos con código 0. Después, `netstat`: ninguno de los dos puertos en escucha y ninguna carpeta temporal |
| 11:43 | *(este commit)* | Cierre de esta bitácora para la **parada 1**. La IA para aquí: el Tech Lead revisa las pruebas, las mutaciones, las capturas y las precisiones AC-01 a AC-18. **El paso 3 no se empieza sin su aprobación.** La hora de este commit se ve con `git log` |
| 12:05 | — | El commit anterior es `409a393` (11:44:40 según `git log`). **El Tech Lead aprueba la parada 1** (mensaje leído a las 12:04:34): ha revisado las doce capturas y son correctas, admite AC-01 a AC-18 y responde que sí a las tres preguntas, con matices. Manda cinco cambios, un commit cada uno con el oráculo en código 0, y después el paso 3 sin parar otra vez (apartado 3). `git status` limpio; nada escucha en el 8000 ni en el 4200 |
| 12:14 | `e75ea0b` | **Cambio 1 (AC-01)**, 12:06:40 según `git log`: la regla 7 de `CLAUDE.md` dice que un encargo con pasos autoriza un commit por paso, con el oráculo en verde, y que el `push` es solo del Tech Lead. Oráculo con código 0 antes |
| 12:14 | `596dede` | **Cambio 2 (AC-09)**, 12:13:54: `@types/node` 24.19.2 (12:06:55), `tsconfig.e2e.json`, su referencia en `tsconfig.json` y `tsc --noEmit -p tsconfig.e2e.json` al final de `npm run lint`. **Ningún error de tipos**: `tsc` salió con 0 a la primera (12:07:38) sobre los once ficheros. Para saber que mira algo, la IA puso un error a propósito en `e2e/support/rates.ts` (12:07:54: `TS2322`, código 2) y lo deshizo. Dos entradas nuevas en el fichero de bloqueo, dentro del margen (apartado 4). Filas de `@types/node` y de Playwright en la tabla de dependencias de ADR-001. Oráculo con código 0 sin `--e2e` y con él (12:08:19 a 12:11:52) y otra vez sin él tras tocar ADR-001 |
| 12:21 | `d76f52b` | **Cambio 3 (AC-11)**, 12:16:18: SPEC-04. La nota bajo los criterios dice dónde están CA-13 y CA-14, cómo se ejecutan y que la API de divisas se responde con el protocolo de depuración de Chromium y no con `page.route()`; CA-15 nombra las dos capturas añadidas; nota fechada junto a D-09; fila de historial. Oráculo con código 0 antes |
| 12:21 | `6f653fc` | **Cambio 4 (AC-17)**, 12:18:15: apartado «Pruebas de principio a fin (`e2e/`)» en `.claude/rules/frontend.md`, con los cuatro puntos mandados. Oráculo con código 0 antes |
| 12:21 | `377233c` | **Cambio 5 (capturas)**, 12:20:38: `capture` quita el foco del elemento activo antes de cada captura. Generadas de nuevo (12:18:31 a 12:18:45; 4 pruebas en 12,8 s): cambian nueve de los doce ficheros; los tres que no cambian son las dos de la cabecera con el aviso y el panel a 375 px, que no tenían foco ni hora. La IA ha mirado dos (el simulador a 375 px y el alta a 1280 px): sin anillo. Oráculo con código 0 antes; puertos libres y sin carpeta temporal después |
| 12:21 | *(este commit)* | Esta bitácora, con la revisión de la parada 1 y sus cinco cambios. **Después, el paso 3**: el evaluador independiente |
| 12:43 | — | Fila escrita a las 12:43, como las tres que siguen: **mientras el evaluador trabajaba la IA no tocó el repositorio**, para que su `git status` final saliera vacío (AD-08). El commit anterior es `bab2922` (12:22:48 según `git log`). **12:23:12**: árbol limpio en `bab2922` y nada en escucha en el 8000 ni en el 4200. **Lanzado el subagente `evaluador`** con el encargo del paso 3 y sus dos añadidos (apartado 3) |
| 12:43 | — | **12:34**: llega el informe (su cabecera dice de 12:23:41 a 12:32:05). `git status` vacío, `HEAD` en `bab2922`, nada en escucha en el 8000, el 4200 ni en ningún 80xx y ninguna carpeta temporal. **12:36:30**: informe escrito con `Write` en `04-calidad/evaluacion-frontend-01.md`, quitando solo la sangría de dos espacios con la que llega, y comparado con el mensaje del registro del subagente: 203 líneas y 20.039 caracteres los dos y **una línea distinta, la 43**, por un U+00A0 que la herramienta guarda como U+0020 (AD-06) |
| 12:43 | — | **12:37 a 12:40**: la IA repite en solo lectura lo que afirman los hallazgos (serializador de Angular, contrastes, `playwright --list`, el backend con el cliente de test y una base temporal fuera del repositorio, borrada después) y escribe su respuesta en `04-calidad/respuesta-evaluacion-frontend-01.md`. **No aplica nada** |
| 12:43 | `c149ca0`, `be9fef7` | El informe y la respuesta, un commit cada uno, los dos a las 12:42:09 según `git log`, con el oráculo en código 0 antes (23 correctas y 1 inactiva) |
| 12:43 | *(este commit)* | Cierre de esta bitácora para la **parada 2**. La IA para aquí: el Tech Lead decide cada hallazgo. La hora de este commit se ve con `git log` |
| 13:15 | — | El commit anterior es `ccafe3d` (12:45:00 según `git log`). **El Tech Lead aprueba la parada 2** (mensaje leído a las 13:11:49): admite AD-01 a AD-10 y decide cada hallazgo, H-01 a H-10, y cada caso, B-01 a B-04 (apartado 3). Manda aplicarlos en orden, una tarea y un commit cada uno, con el oráculo con `--e2e` en código 0; después, una segunda evaluación acotada y la **parada 3**. `git status` limpio; nada escucha en el 8000 ni en el 4200. Desde aquí las filas se escriben al acabar cada tarea, no al final |
| 13:22 | `35d482a` | **H-01**, 13:21:43 según `git log`. Dos casos nuevos en los tests de 5.7 del detalle y dos en los del simulador; estos dos abren el simulador por su dirección, con el router de verdad, porque los demás tests del simulador le dan el `id` ya hecho. **Nacen en verde** (13:17:28), tras corregir una expectativa mal escrita por la IA en los del detalle (AE-01). **Mutación** (13:17:56, con los 539 tests): el cargador toma el `id` de `Router.url` en vez de los parámetros de la ruta; **fallan los dos casos de `1;x=y` y sobreviven los dos de `%31`** (AE-02). Deshecha; `git diff` sin nada fuera de los tests. SPEC-04: párrafo en 2.1, dos filas en 5.7 e historial. Oráculo con `--e2e` de 13:19:29 a 13:21:32, código 0, 24 correctas; puertos libres y sin carpeta temporal después |
| 13:28 | `72f8544` | **H-02**, 13:28:03. Prueba nueva `e2e/contrast.spec.ts` (cuatro campos: un texto y un desplegable del alta, el buscador y el selector de divisa), **vista en rojo dos veces por aserción**: con los colores de hoy (13:23:40; anillo `rgb(245, 158, 11)` sobre blanco, 2,15) y, con solo el anillo cambiado, por el borde (13:24:07; `rgb(201, 206, 216)` sobre blanco, 1,58). Verde a las 13:24:33 con el anillo en el color de acento y el borde de `input` y `select` en la variable nueva `--color-control-border`, `#7c8698`. **Capturas regeneradas** (13:25:09; 4 pruebas en 12,9 s): cambian las doce y hay dos nuevas, `alta-foco-375.png` y `alta-foco-1280.png`, que la IA ha mirado: anillo azul alrededor del identificador fiscal y bordes de los campos más oscuros que el de la cabecera. SPEC-04: frase en 2.8, CA-19, CA-15 e historial. Oráculo con `--e2e` de 13:25:54 a 13:27:54, código 0 |
| 13:33 | `8a16e2e` | **H-03**, 13:32:39. Primero SPEC-04 (párrafo en 2.1, requisito E-57, CA-11 e historial). Cuatro casos nuevos en `app.routes.spec.ts`, **vistos en rojo por aserción** (13:29:14: el título seguía siendo el que el test deja puesto antes de navegar). Verde a las 13:29:37 con la opción `title` en las cuatro rutas. Fila **L-10** en `limitaciones-conocidas.md`: el anuncio de la búsqueda y el foco al navegar, con cómo se cerrarían. **La página «no encontrada» se queda sin título propio** (AE-08). Oráculo con `--e2e` de 13:30:41 a 13:32:38, código 0; el commit, encadenado a ese código |
| 13:37 | `64f5e7b` | **H-04**, 13:36:49. Primero SPEC-04 2.7. Dos tests nuevos en `alta.spec.ts` (el envío vacío con sus cinco mensajes, y un `422` del backend junto a su campo), **vistos en rojo por aserción** (13:33:52: `expected 'alert' to be null`). Verde a las 13:34:18 al quitar `role="alert"` de los cinco mensajes de `alta.html`; el aviso general y los del simulador no se tocan. L-10 dice que nada se ha probado con lector de pantalla. Oráculo con `--e2e` de 13:34:48 a 13:36:48, código 0 |
| 13:41 | `b33ea2e` | **H-05**, 13:40:19. Solo SPEC-04, tal como está el código: el `409` y el aviso general de un `422` sin «Reintentar» (2.3, la fila del `409` y 2.7), la excepción en la fila «Error» de la tabla de 2.5, un `created_at` que no es fecha (2.8) e historial. Ni código ni tests (AE-11). Oráculo con `--e2e` de 13:38:21 a 13:40:19, código 0 |
| 13:46 | `04404af` | **H-06**, 13:42:57. El comentario de `core/limits.ts` dice que son los límites del buscador y dónde están los demás. L-09 gana la frase de los tres textos con la cifra escrita (los tres, localizados con una búsqueda: `alta-help.ts` y dos en `panel.html`) y dice que su caso de frontera está hecho. Oráculo con `--e2e` de 13:40:58 a 13:42:57, código 0 |
| 13:46 | `3728349` | **H-07**, 13:45:23. `rate-date.spec.ts` cita E-29 en el comentario y en el título. **Los mensajes de `895f55d`, `6123e69` y `409a393` siguen diciendo E-27 y no se reescriben**; la fila de la tabla de pruebas de esta bitácora (apartado 3) lleva una nota y conserva lo que se escribió. Oráculo con `--e2e` de 13:43:25 a 13:45:23, código 0 |
| 13:50 | `f6d0d04` | **H-08**, 13:49:31. `playwright.config.ts` ya no tiene proyectos y deja fuera `e2e/capturas/`; `playwright.capturas.config.ts`, nuevo, parte de él y apunta a esa carpeta; `npm run e2e` es `playwright test` y `npm run e2e:capturas` usa `-c`. **`npx playwright test --list` sin opciones (13:46:22): 18 pruebas en 5 ficheros** (las 14 de antes y las 4 del contraste) **y ninguna de `capturas`**; con `-c playwright.capturas.config.ts`, las 4 capturas; y pidiendo `e2e/capturas` a la configuración por defecto, 0. `tsc` con código 0 sobre los trece ficheros. Al día `tsconfig.e2e.json` y `.claude/rules/frontend.md`. **Capturas generadas con la orden nueva** (13:46:53; 4 pruebas en 13,0 s): cambian cuatro ficheros (AE-12). Oráculo con `--e2e` de 13:47:25 a 13:49:30, código 0 |
| 13:55 | `596f1ec` | **H-09**, 13:54:07. Test nuevo en `meta-store.spec.ts`: a los 10 s sin respuesta el almacén queda en error con `timeout`, la petición se cancela y un reintento vuelve a pedir. **Nace en verde** (13:50:22). **Dos mutaciones**, cada una con los 546 tests: el almacén descarta el estado de error por tiempo agotado (13:50:50: falla solo el test nuevo); y `/meta` espera 20 s en `BackendApi` (13:51:24: fallan el nuevo y el de `BackendApi` que ya había). Deshechas; `git diff` sin nada fuera del test. Oráculo con `--e2e` de 13:51:59 a 13:54:07, código 0 |
| 13:58 | `13351c9` | **H-10**, 13:57:01. Fila **L-11** en `limitaciones-conocidas.md`: sin política de contenido, y cómo se cerraría en un despliegue. Ningún código. Oráculo con `--e2e` de 13:54:56 a 13:57:01, código 0 |
| 13:58 | *(el siguiente)* | **Apartado 4 de la respuesta** a la primera evaluación: la decisión del Tech Lead sobre H-01 a H-10 y B-01 a B-04, con el commit de cada una; el «Pendiente» anterior, tachado. El informe no se toca. Va en un commit con esta bitácora en otro, los dos tras una sola pasada del oráculo (AE-13). **Después, la segunda evaluación** (B-03), con el árbol limpio |
| 14:20 | `d44f18f`, `7f8c974` | Fila escrita a las 14:20, como las cuatro que siguen: **mientras el evaluador trabajaba la IA no tocó el repositorio** (AE-14). Los dos commits anteriores, a las 13:59:32 según `git log`, tras el oráculo con `--e2e` de 13:57:29 a 13:59:32, código 0. **14:00:08**: árbol limpio en `7f8c974` y nada en escucha en el 8000, el 4200 ni en ningún 80xx. **Lanzado el subagente `evaluador`** con el encargo acotado de B-03 (apartado 3) |
| 14:20 | — | **14:11:32**: llega el informe (su cabecera dice de 14:00:55 a 14:08:44). `git status` vacío, `HEAD` en `7f8c974`, nada en escucha en el 8000, el 4200, el 18765 (el de su backend) ni en ningún 80xx y ninguna carpeta temporal. **14:13:47**: informe escrito con `Write` en `04-calidad/evaluacion-frontend-02.md`, quitando solo la sangría, y comparado con el mensaje del registro: **362 líneas y 34.340 caracteres los dos, ninguna línea distinta y ningún carácter invisible** |
| 14:20 | — | **14:14 a 14:17**: la IA repite en solo lectura lo que afirman los nueve hallazgos (los nueve se reproducen), cuenta las filas de las cuatro tablas y contrasta los números de línea del informe, y escribe su respuesta en `04-calidad/respuesta-evaluacion-frontend-02.md`. **No aplica nada** |
| 14:20 | `8045884`, `5eb8d8a` | El informe y la respuesta, un commit cada uno, los dos a las 14:19:18 según `git log`, tras el oráculo con `--e2e` de 14:17:12 a 14:19:17, código 0, 24 correctas; puertos libres y sin carpeta temporal después |
| 14:20 | *(este commit)* | Cierre de esta bitácora para la **parada 3**. La IA para aquí: el Tech Lead decide N-01 a N-09 y C-01 a C-05 y revisa AE-01 a AE-18. La hora de este commit se ve con `git log` |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (10:43)

**Admitidas AB-01 a AB-07** de la sesión 07, y confirmada la lectura de las
dos frases cortadas de los cambios 6 y 7.

**Lo que el Tech Lead dice haber visto en Chrome** (lo afirma él; la IA no
lo ha visto): el aviso compacto de la cabecera con la API de divisas caída,
130 px de alto en escritorio, con el texto y «Reintentar» en una línea, y
187 px a 375 px, con el selector en su sitio y sin desplazamiento
horizontal; la espera agotada real de los tipos (a los 5 s sale el aviso y
una respuesta posterior no lo cambia); y que al reintentar se ve «Cargando
tipos…» y el botón desaparece. Con esto quedan vistos el cambio 7 de la
sesión 07 y la primera línea de su apartado 5. La cuenta a mano de la IA
(unos 150 px a 375 px) se quedó corta: son 187.

**Playwright: cambia la decisión de ayer.**

| Qué | Ayer (sesión 07, 18:48) | Hoy | Por qué cambia |
|---|---|---|---|
| Puertos | Otros dos, ni el 8000 ni el 4200 | **Los de por defecto, 8000 y 4200** | CA-14 pide el backend real con su CORS por defecto; así se prueba exactamente lo que ejecutará quien revise |
| Configuración del frontend | Una de compilación más, con la URL del backend en su puerto | **Ninguna**: la de desarrollo, la de `npm start` | Sería una tercera configuración que SPEC-04 no nombra |
| `CORS_ORIGINS` | Propio | **El de por defecto** | Lo mismo: es lo que CA-14 dice comprobar |
| `DATABASE_PATH` | Base temporal fuera de `backend/data/` | **Igual**: carpeta temporal que se crea y se borra en cada ejecución | No cambia |
| API de divisas | Interceptada | **Igual**: interceptada en el navegador de la prueba, con tipos fijos | No cambia |
| Quién arranca los servidores | Por decidir (el oráculo o Playwright) | **Playwright, con `webServer` y `reuseExistingServer: false` escrito**. Con un puerto ocupado la prueba falla sin tocar nada | Cierra la pregunta de ayer sin tocar `scripts/` |
| Regla del 8000 y el 4200 (17:36 de ayer) | Sin excepciones | **Una sola excepción**: lo que arranca Playwright. Se escribe en la regla 8 de `CLAUDE.md` | — |

Las tres cosas que la fila de las 19:11 de ayer dejaba «a decidir antes de
montarlo» quedan decididas con esto: no hay configuración nueva del
frontend, los puertos son los de por defecto y los servidores los arranca
Playwright.

### Descarga del navegador: pregunta de la IA y decisión del Tech Lead (10:52–11:05)

La IA dio origen y tamaño, medidos sin descargar, y tres opciones. **El
Tech Lead eligió la primera.**

| Opción | Qué descarga | Tamaño en zip |
|---|---|---|
| **Solo el *headless shell*** (`npx playwright install --only-shell chromium`), la recomendada por la IA y **la elegida** | Chrome Headless Shell 158.0.8127.18, FFmpeg y winldd | 130.978.403 bytes |
| Chromium completo (`npx playwright install chromium`) | Lo anterior y Chrome for Testing 158.0.8127.18 | 346.798.687 bytes |
| No descargar nada | — | — |

### Paso 1 · lo hecho

**Qué hay en `frontend/`.** `playwright.config.ts`; `e2e/` con cuatro
ficheros de pruebas y cinco de apoyo (`support/`); dos scripts en
`package.json`, `e2e` y `e2e:capturas`; y `@playwright/test` 1.65.0 en las
dependencias de desarrollo. No se ha tocado `scripts/`, ni `angular.json`,
ni los ficheros de entorno, ni ESLint.

| Prueba | Fichero | Casos | Requisitos que cita |
|---|---|---|---|
| 1 · Recorrido | `journey.spec.ts` | 1: alta por la interfaz, simulador, dos guardados, y la segunda simulación aparece la primera | SPEC-04/CA-14 (E-08, E-12, E-24, E-52) |
| 2 · 375 px | `responsive.spec.ts` | 5: panel, alta, detalle, simulador y la cabecera con el aviso del fallo de los tipos | SPEC-04/CA-13 (E-16), E-30 |
| 3 · Límites | `limits.spec.ts` | 7: nombre de 120 y de 2 caracteres, email de 254, identificador de 30, los tres máximos del simulador, el buscador con 100 y la nota de los 20 resultados | L-09; SPEC-04/E-41, E-22, E-36, E-50, E-53 |
| 4 · Fecha del tipo | `rate-date.spec.ts` | 1: navegador en `America/Los_Angeles`, USD elegido, en el simulador y en el detalle | SPEC-04/E-27, fila de 5.5 *(nota de las 13:43: **la cita es errónea, es E-29**; hallazgo H-07, corregida en el fichero. La celda se deja como se escribió)* |

**Cómo cumple cada condición del Tech Lead.**

| Condición | Cómo |
|---|---|
| `webServer` con `reuseExistingServer: false` escrito | Dos entradas, las dos con `reuseExistingServer: false`. El backend, con `uv run --locked uvicorn --factory app.main:create_app` en `../backend`; el frontend, con `npm start`. Los puertos por defecto, sin nombrarlos en las órdenes |
| Con un puerto ocupado, falla sin tocar nada | Las dos entradas llevan `port`, no `url`: Playwright mira si algo acepta conexiones en ese puerto, en `127.0.0.1` y en `::1`, responda lo que responda. Visto con una segunda ejecución (apartado 4) |
| `DATABASE_PATH` en una carpeta temporal que se crea y se borra | `e2e/support/temporary-folder.ts`: la crea el proceso que ejecuta Playwright, con un nombre único bajo la carpeta temporal del sistema, y la borra al salir, después de que Playwright haya parado los servidores. Vista mientras dura y comprobado que no queda (apartado 4) |
| La API de divisas, interceptada en el navegador con tipos fijos | `e2e/support/fixtures.ts`, con los tipos del ejemplo de SPEC-04, 4.2 (`e2e/support/rates.ts`). **No con `page.route()`** (AC-03) |
| Ningún test llama a un servicio externo | El navegador se lanza con una regla que no resuelve ningún nombre salvo `localhost` y `127.0.0.1`; y cada prueba falla si la página pide algo a otro servidor. Visto que, sin la interceptación, la API real no se alcanza (apartado 4) |
| No se toca `scripts/` | No se ha tocado. El oráculo ejecuta `npm run e2e` con `--e2e` |

**Mutaciones: qué se rompió y qué falló.** Cada ejecución arranca los dos
servidores de nuevo, así que el código mutado es el que se sirve. Cuando
una ejecución lleva varias mutaciones, cada una afecta a una prueba
distinta.

| # | Hora | Qué se rompió | Qué falló |
|---|---|---|---|
| M1 | 11:15:44 | `BackendApi.post` añade una cabecera `X-Client` a cada `POST` | **Nada: la prueba pasa.** Con `page.route()` puesto, la comprobación previa la respondía Playwright (AC-03) |
| M1 | 11:19:09 | La misma, ya con la interceptación cambiada | El recorrido: tras «Guardar», la dirección sigue en `/clientes/nuevo` y el formulario dice «No se ha podido conectar con el servidor.» |
| M2 | 11:19:53 | El detalle muestra las simulaciones en orden inverso | El recorrido: en la primera tarjeta, `Expected: "15"`, `Received: "10"` |
| M3 | 11:20:24 | **En el backend**, `CORS_METHODS` admite solo `GET` | El recorrido, en el mismo punto que con M1 |
| M4 | 11:20:52 | `overflow-wrap: normal` en `body` (los textos largos no se parten) | Panel, detalle y simulador: anchos de 2445, 2923 y 1945 px. También la de la cabecera, por el panel que tiene debajo, no por el aviso. El alta pasa |
| M5 | 11:21:29 | `min-width: 32rem` en el formulario del alta; y `white-space: nowrap` en el texto del aviso de la cabecera | El alta (528 px) y la cabecera con el aviso (640 px), y solo ellas |
| M6 | 11:22:12 | Siete límites del frontend: nombre máximo 119 y mínimo 1, identificador 29, email 255, usuarios 100.001, buscador 101 y 21 resultados | Las siete pruebas de límites, cada una por su límite. Con el nombre en 119 y el identificador en 29, el valor del límite **no se guarda** (el caso que L-09 llama silencioso); con las demás, la ayuda no rechaza el valor siguiente o la nota no sale |
| M7 | 11:23:32 | Almacenamiento máximo 999.999 en el frontend | Solo la de los máximos del simulador |
| M8 | 11:24:06 | Llamadas máximas 1.000.000.001 en el frontend | Solo la de los máximos del simulador |
| M9 | 11:24:46 | **En el backend**: nombre máximo 121, buscador 101, 21 resultados y almacenamiento 1.000.001 | Las cuatro pruebas de esos límites: el backend responde `201` o `200` donde se espera `422`, y el panel muestra 21 tarjetas donde se esperan 20. Las otras tres pasan |
| M10 | 11:25:52 | `formatRateDate` pasa la fecha por un `Date` | La de la fecha del tipo: `Expected: "… tipo del 12/11/2026"`, `Received: "… tipo del 11/11/2026"`. Un primer intento, a las 11:25:25, cambiaba además el formato del año y no cuenta |
| M11 | 11:26:27 | **En la propia prueba**: la interceptación de los tipos apunta a otro servidor | La de la fecha del tipo: la cabecera muestra el aviso del fallo y solo ofrece EUR. Es decir, sin interceptación la API real no se alcanza |

Lo que esto **no** demuestra: cada mutación de límites se miró contra
`limits.spec.ts`, no contra toda la batería ni contra los tests unitarios;
del máximo de usuarios, del email y del mínimo del nombre solo se ha roto
un sentido (el del frontend); y la parte «la ayuda no envía nada» de las
pruebas del alta no tiene mutación propia.

Precisiones de la IA, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| AC-01 | **La IA ha hecho los commits sin que el Tech Lead pidiera cada uno**: dos de documentación y el de Playwright; después de esta parada, los de las capturas y esta bitácora | El encargo dice «antes del commit» y las sesiones anteriores iban a un commit por tarea. La regla 7 dice que solo se hace cuando el Tech Lead lo pide: si no era eso, se deshacen, que no están subidos |
| AC-02 | En la regla 8 de `CLAUDE.md` la IA ha escrito, además de la excepción, **la regla misma** de los puertos | No estaba en `CLAUDE.md`, solo en la bitácora de la sesión 07, y una excepción sin su regla no se entiende |
| AC-03 | **La API de divisas no se intercepta con `page.route()`**, sino con el protocolo de depuración de Chromium (`Fetch.enable` con el patrón de su URL). Consecuencia: **las pruebas solo funcionan en Chromium** | Con una ruta puesta, Playwright responde las comprobaciones previas de CORS y CA-14 no comprobaría el CORS del backend. **Lo encontró la mutación M1, no la IA al escribir la prueba**: las catorce pruebas habían pasado en verde con ese defecto |
| AC-04 | El navegador se lanza con `--host-resolver-rules`, que no resuelve ningún nombre que no sea local | Para que «ningún test llama a un servicio externo» no dependa de que la interceptación funcione |
| AC-05 | `port` y no `url` en `webServer`. **Si el 8000 está libre y el 4200 ocupado, Playwright arranca el backend, con su base temporal, y lo para al ver ocupado el 4200**: no toca nada ajeno, pero durante unos segundos hay un backend de prueba en el 8000 | Con `url`, un proceso ajeno que no respondiera bien a esa dirección no contaría como ocupado. Playwright comprueba los servidores uno tras otro, no los dos antes de arrancar |
| AC-06 | La carpeta temporal se crea al cargar la configuración y se borra en el `exit` del proceso de Playwright, no en un `globalTeardown` | El `globalTeardown` se ejecuta antes de parar los servidores, con el fichero de la base todavía en uso |
| AC-07 | La configuración **borra la variable `CORS_ORIGINS`** del entorno del proceso de Playwright | El backend de la prueba tiene que ir con su CORS por defecto; una variable de quien ejecuta lo cambiaría |
| AC-08 | **Catorce pruebas, no cuatro**, y la de L-09 cubre **todos los límites** que nombra la fila L-09, no «un campo»: siete casos, con los 20 resultados del buscador incluidos, que no es un campo | L-09 habla de cada copia de un límite; con un solo campo, los demás seguirían sin vigilancia |
| AC-09 | **Los ficheros de `e2e/` y `playwright.config.ts` no los compila nadie con tipos**: Playwright ejecuta TypeScript sin comprobarlo y la compilación del proyecto solo mira `src/`. ESLint y Prettier sí los ven | Comprobarlos pide `@types/node`, que no está instalado: sería una dependencia nueva. **Propuesta, sin aplicar**: añadirla y que `npm run e2e` empiece con `tsc --noEmit` |
| AC-10 | `npm run e2e` ejecuta solo el proyecto `pruebas`; las capturas van en otro proyecto, con su script `e2e:capturas`, y **el oráculo no las genera** | Las capturas llevan la fecha del día: generarlas en cada pasada del oráculo cambiaría doce ficheros versionados |
| AC-11 | En SPEC-04, además de la fila de CA-15: la carpeta pasa a ser `04-calidad/capturas/` y la nota bajo la tabla dice lo mismo. **No tocado y que ya no es cierto**: esa nota sigue diciendo que CA-13 y CA-14 están «pendientes de implementar», y D-09 y el cuerpo de ADR-005, «capturas manuales». CA-15 tampoco nombra las dos capturas añadidas | El encargo era CA-15; lo demás lo decide el Tech Lead |
| AC-12 | **Una nota fechada en ADR-005** que nadie pidió: los cuatro grupos de pruebas, quién arranca los servidores, las capturas y el porqué de no usar `page.route()`; y su tabla de versiones al día | El ADR decía «dos pruebas», «sin instalar» y «capturas manuales». Lo anterior se conserva |
| AC-13 | La primera ejecución de CA-14 falló por una expectativa mal escrita por la IA («500» por «500 GB») y **se corrigió la prueba** | La prueba no había pasado nunca; lo que muestra el detalle lo fijan sus tests unitarios |
| AC-14 | Para M3 y M9 se editaron cuatro constantes de `backend/app/` y se devolvieron a su valor | Es el escenario de L-09: que el límite cambie en el backend |
| AC-15 | Las pruebas localizan parte de lo que miran por la estructura del HTML (`ul.history > li`, `dl > div`, `.rate-applied`), reunido en `e2e/support/views.ts` | No hay un rol ni un texto que distinga una tarjeta del historial de un tramo del desglose |
| AC-16 | `limits.spec.ts` tiene 259 líneas | El límite de 250 no se aplica a los ficheros de test; lo dice quien lo ha escrito |
| AC-17 | `.claude/rules/frontend.md` no dice nada de `e2e/` (su apartado «Tests» habla de los `.spec.ts` junto al fichero que prueban). No se ha tocado | No se pidió |
| AC-18 | **La cronología de esta parada se escribió de una vez, a las 11:37**, y no fila a fila | La regla 6 pide anotar al momento. Las horas no son estimadas: cada orden ejecutada imprimía `date` |

### Paso 2 · lo hecho

`frontend/e2e/capturas/capturas.spec.ts` crea por la API tres clientes de
ejemplo («Ejemplo Uno SL», «Ejemplo Dos SL» y «Ejemplo Tres SA», con
correos `.example`) y tres simulaciones del primero, y escribe doce
ficheros PNG de página completa en `ai-workspace/04-calidad/capturas/`,
449 kB en total:

| Vista | 375 px | 1280 px | Qué muestra |
|---|---|---|---|
| Panel | `panel-375.png` | `panel-1280.png` | Los tres clientes |
| Alta | `alta-375.png` | `alta-1280.png` | El formulario relleno, sin enviar |
| Detalle | `detalle-375.png` | `detalle-1280.png` | «Ejemplo Uno SL» con sus tres simulaciones |
| Simulador | `simulador-375.png` | `simulador-1280.png` | 15 usuarios, 500 GB y 250.000 llamadas, en EUR |
| Simulador en otra divisa | `simulador-usd-375.png` | `simulador-usd-1280.png` | Lo mismo en USD, con el tipo, su fecha y el total en EUR |
| Cabecera con el aviso | `cabecera-aviso-375.png` | `cabecera-aviso-1280.png` | El panel con la API de divisas caída |

Se pidió una del simulador con otra divisa y una de la cabecera con el
aviso; la IA ha hecho las dos a los dos anchos. Las fechas que se ven son
las de hoy, en `Europe/Madrid`. **La IA ha mirado tres** (la cabecera a
375 px, el simulador en USD a 375 px y el detalle a 1280 px): son lo que
dicen ser. Dos cosas que se ven en ellas y decide el Tech Lead: en el
simulador sale el anillo de foco del último campo escrito; y en
escritorio el enlace «Panel» queda centrado entre el nombre y el selector.

### Revisión de la parada 1 por el Tech Lead (12:04)

**Parada 1 aprobada.** El Tech Lead ha revisado las doce capturas (lo
afirma él) y son correctas. **Admitidas AC-01 a AC-18.** A las tres
preguntas de la IA, sí, con estos cambios, un commit cada uno y con el
oráculo en verde por su código de salida:

| # | Sobre | Decisión del Tech Lead | Frente a lo que hizo o propuso la IA |
|---|---|---|---|
| 1 | AC-01, los commits | Admitido: **un encargo con pasos autoriza un commit por paso, con el oráculo en verde**. Se escribe en la regla 7 de `CLAUDE.md`, para que la regla diga lo que se hace. El `push` sigue siendo solo suyo | La IA lo había leído así sin que la regla lo dijera |
| 2 | AC-09, los tipos de `e2e/` | Sí a `@types/node`: de desarrollo, versión exacta, dentro del margen y con las fechas comprobadas. Un `tsconfig` que cubra `e2e/` y `playwright.config.ts`. **El `tsc --noEmit` va dentro de `npm run lint`, no al principio de `npm run e2e`**. Por qué: el oráculo ejecuta `lint` siempre y `e2e` solo con `--e2e`. No se toca `scripts/`. Los errores de tipos que salgan se corrigen y se anotan | **Cambiado**: la IA proponía ponerlo en `npm run e2e`, donde solo se comprobaría con `--e2e` |
| 3 | AC-11, SPEC-04 | Sí, con historial: la nota bajo los criterios deja de decir «pendientes de implementar» y dice dónde están CA-13 y CA-14 y cómo se ejecutan; precisa que la API de divisas se responde con el protocolo de depuración de Chromium y no con `page.route()`, con su porqué, y que por eso las pruebas solo funcionan en Chromium; CA-15 nombra las dos capturas añadidas; y D-09 no se reescribe: una nota fechada a su lado | La IA lo había dejado sin tocar y a su decisión |
| 4 | AC-17 | Un apartado corto sobre `e2e/` en `.claude/rules/frontend.md`: dónde van las pruebas, que comparten una base de datos por ejecución y cada una trae su identificador fiscal, que no se usa `page.route()` y por qué, y que las capturas no las ejecuta el oráculo | La IA no lo había tocado |
| 5 | Capturas | **Se quita el foco antes de cada captura**: el anillo naranja sobre el último campo parece un aviso de error. Se vuelven a generar. El enlace «Panel» centrado en escritorio se queda como está | **Defecto de las capturas** que la IA había visto y dejado a su decisión |
| 6 | Lo no comprobado | Se queda anotado como está. Irá al README cuando toque: solo Chromium, solo probado en Windows, dos ejecuciones a la vez se estorban y qué pasa con una ejecución interrumpida, que **el Tech Lead prueba a mano con Ctrl+C** | — |

**Paso 3, con dos añadidos al encargo original**: el evaluador revisa
también `frontend/e2e/` y `playwright.config.ts` (pruebas que no comprueban
lo que dicen y si alguna puede tocar algo fuera de su carpeta temporal); y
para ejecutar la aplicación vale la regla 8: puede ejecutar `npm run e2e` y
los tests unitarios, y arrancar el backend en otro puerto con
`DATABASE_PATH` temporal para llamarlo directamente; no arranca nada en el
8000 ni en el 4200 fuera de Playwright, y lo que necesite ver en un
navegador y Playwright no cubra lo anota como no comprobado. **Parada 2**
como estaba prevista.

### Cambios de la revisión de la parada 1 · lo hecho (12:05–12:22)

Un commit por cambio, cada uno con la salida del oráculo en un fichero y
su código en 0 antes.

| # | Cambio | Commit | Qué toca |
|---|---|---|---|
| 1 | AC-01, un commit por paso | `e75ea0b` | `CLAUDE.md`, regla 7 |
| 2 | AC-09, los tipos de `e2e/` en `npm run lint` | `596dede` | `package.json`, `package-lock.json`, `tsconfig.e2e.json`, `tsconfig.json` y la tabla de dependencias de ADR-001 |
| 3 | AC-11, SPEC-04 | `d76f52b` | La nota bajo los criterios, CA-15, una nota junto a D-09 e historial |
| 4 | AC-17, reglas de `e2e/` | `6f653fc` | `.claude/rules/frontend.md` |
| 5 | Capturas sin foco | `377233c` | `e2e/capturas/capturas.spec.ts` y nueve de las doce capturas |
| — | Esta bitácora | `bab2922` | — |

**Cambio 2: no salió ningún error de tipos.** `tsc` pasó a la primera
sobre los once ficheros, así que no hay nada que anotar como corregido.

### Paso 3 · evaluación independiente del frontend (12:23–12:42)

| Hora | Qué |
|---|---|
| 12:23 | Lanzado el subagente `evaluador` (`.claude/agents/evaluador.md`: herramientas `Read`, `Grep`, `Glob` y `Bash`; `model: opus`) con el árbol limpio en `bab2922`. El encargo: las tres cosas del prompt (CA-12; el frontend contra SPEC-04 y contra el contrato real del backend; accesibilidad, seguridad del navegador y lo que señalaría un revisor exigente) y los dos añadidos del Tech Lead (revisar `frontend/e2e/` y `playwright.config.ts`, y la regla 8 para ejecutar). Restricciones: solo lectura, sin instalar ni descargar nada, sin leer `03-proceso/` ni `04-calidad/` ni la historia de git, sin ejecutar `npm run e2e:capturas`, rutas relativas, caracteres invisibles nombrados por su código y cabecera con el modelo |
| 12:34 | Informe recibido: 54 más 18 veredictos según su resumen (su tabla recoge los 56 requisitos), ninguno `NO CUMPLE`, CA-15 `NO DEMOSTRADO`, y **10 hallazgos: uno medio (H-02, contraste) y nueve bajos**. Ejecutó el oráculo con y sin `--e2e` y `npm run e2e`, los tres con código 0, y arrancó un backend propio en el 8011, que paró por su PID |
| 12:36 | Guardado y comparado con el registro del subagente: una línea distinta, la 43, por un U+00A0 (AD-06). Las 130 respuestas del registro llevan el modelo `claude-opus-5-5` |
| 12:40 | Respuesta de la IA escrita, con lo que ha repetido por su cuenta. **De acuerdo con los diez**; dos son errores suyos de esta sesión (H-07 y H-08). Cuatro casos más, B-01 a B-04. Nada aplicado |
| 12:42 | Commits `c149ca0` (informe) y `be9fef7` (respuesta) |

Precisiones de la IA sobre los cambios y el paso 3, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| AD-01 | En el cambio 2 la IA añadió, sin que se pidiera, la fila de `@types/node` a la tabla de dependencias directas de ADR-001 y puso al día la de Playwright, que decía «todavía no instalada» | Es la tabla donde están las versiones de todas las dependencias directas |
| AD-02 | El `tsconfig` nuevo es `frontend/tsconfig.e2e.json`, junto a los del CLI, y `tsconfig.json` lleva una referencia a él | Para que un editor use esa configuración con los ficheros de `e2e/`. `tsconfig.json` es un fichero del CLI que hasta hoy no se había tocado |
| AD-03 | En la regla 7, el porqué («es como se trabaja desde la sesión 07») es redacción de la IA | El Tech Lead dio la regla, no su porqué |
| AD-04 | En la nota de SPEC-04 la IA añadió que sin `--e2e` la comprobación sale como inactiva, y dejó sin tocar la última frase del párrafo «Sobre D-09» («No se ha instalado ni ejecutado»), que la nota fechada de debajo corrige | Lo primero es lo que dice la regla 4 de `CLAUDE.md`; lo segundo, por no reescribir D-09 |
| AD-05 | El apartado de `.claude/rules/frontend.md` dice tres cosas más que las cuatro mandadas: que las pruebas son solo de Chromium, que cada una cita su requisito y que sus tipos los comprueba `npm run lint` | Las tres son ciertas desde hoy y son de ese apartado |
| AD-06 | **El informe guardado difiere del mensaje del evaluador en un carácter**: en la línea 43 hay un U+0020 donde el mensaje trae un U+00A0 literal, que el evaluador escribió aunque se le pidió nombrarlos por su código. **La IA no lo ha restaurado**: hacerlo pide escribir desde la terminal, que es una excepción que hay que pedir | «Intacto» no es exacto y hay que decirlo. Fila B-01 de la respuesta |
| AD-07 | El informe no llegó como último mensaje de texto del subagente sino en su llamada de entrega; el script de comparación leía al principio otro mensaje (61 caracteres) y **la IA lo corrigió antes de comparar** | La primera comparación habría dicho que nada coincidía |
| AD-08 | Las filas de la cronología de las 12:23 a las 12:42 se escribieron a las 12:43, no al momento | Mientras el evaluador trabajaba, cualquier edición habría ensuciado su `git status` final. Las horas salen de `date` y de `git log` |
| AD-09 | El encargo al evaluador lo redactó la IA, incluido un resumen de L-06, L-08 y L-09, que él no puede leer, y tres prohibiciones que el Tech Lead no dictó: instalar o descargar, ejecutar `npm run e2e:capturas` y arrancar `npm start` por su cuenta | Un resumen mal hecho podría haberle orientado; el texto completo consta en el registro del subagente |
| AD-10 | Para responder, la IA arrancó la aplicación del backend con el cliente de test y una base temporal en su carpeta de trabajo, fuera del repositorio, y la borró | Para saber qué hace el backend con un `id` codificado (H-01). No escucha en ningún puerto |

**Admitidas por el Tech Lead a las 13:11**, las diez.

### Revisión de la parada 2 por el Tech Lead (13:11)

**Parada 2 aprobada. Admitidas AD-01 a AD-10.** El Tech Lead decide cada
hallazgo del informe y cada caso de la respuesta. Se aplican en este orden,
una tarea y un commit cada uno, con el oráculo con `--e2e` en verde por su
código de salida; donde cambia el comportamiento, el test en rojo antes;
donde el test nace en verde, una mutación.

| # | Decisión del Tech Lead | Frente a lo que propuso la IA |
|---|---|---|
| H-01 | No se toca el código. SPEC-04 2.1 dice que el filtro se aplica al segmento ya descodificado por el router, y 5.7 gana dos filas: `%31` pide el cliente 1, y `1;x=y` pide el cliente 1 porque el parámetro de matriz no forma parte del `id`. Con historial, y los dos casos en los tests de 5.7 del detalle y del simulador | La recomendada por la IA |
| H-02 | Se corrige. **Anillo de foco: el azul de acento, `#1d4ed8`, no el `#b45309`**: se parece demasiado al color de error, `#b42318`, y un campo enfocado parecería un campo con error. **Borde de los campos: `#7c8698`, en una variable nueva solo para los controles**; las tarjetas, los avisos y la cabecera conservan el borde actual, porque son decorativos y oscurecerlos carga la vista. Una frase en SPEC-04 2.8 y un criterio nuevo (3:1 o más sobre el blanco y sobre el fondo de la página). Una prueba de Playwright que lea los colores que pinta el navegador y calcule el ratio, vista en rojo con los colores de hoy. Capturas regeneradas y una nueva del alta con un campo enfocado, a los dos anchos, que CA-15 nombra | **Elegido y acotado**: la IA daba dos candidatos para cada color (`#b45309` o `#1d4ed8`; `#7c8698` o `#868e9c`) y proponía cambiar el valor de `--color-border`, que habría oscurecido también las tarjetas, los avisos y la cabecera. La prueba, la frase, el criterio y la captura los añade el Tech Lead |
| H-03 | **Solo el título por ruta**: «Clientes», «Nuevo cliente», «Detalle del cliente» y «Simulador», con la opción `title` del router y el nombre de la aplicación detrás. Requisito nuevo en SPEC-04, con su test en rojo antes. **El anuncio del resultado de la búsqueda y el foco al navegar no se hacen**: van a `limitaciones-conocidas.md` como una fila nueva, con cómo se cerrarían. Por qué: sin lector de pantalla no se pueden comprobar, y un atributo ARIA sin probar puede empeorar lo que hay | **Recortado**: la IA habría hecho el título y también el anuncio de la búsqueda, y dejaba el foco para decidirlo con un lector de pantalla |
| H-04 | **Solo en el alta**: los mensajes de campo dejan de llevar `role="alert"`; se siguen leyendo con el campo por `aria-describedby` y `aria-invalid`, que ya están. En el simulador se quedan como están, porque ahí el foco no se mueve y el mensaje sale mientras se escribe. SPEC-04 2.7 dice qué lleva `role="alert"` y qué no. Test en rojo antes. La fila nueva de limitaciones dice que nada de esto se ha probado con lector de pantalla | **Recortado**: la recomendada de la IA lo quitaba en el alta y en el simulador, con la duda sobre el simulador dicha («quizá convenga quitarlo solo en el alta») |
| H-05 | A SPEC-04 tal como está el código, con historial: el `409` y el aviso general de un `422` no ofrecen «Reintentar» porque enviar lo mismo no puede salir bien, y un `created_at` que no es una fecha se muestra como llega. La fila «Error» de la tabla de 2.5 recoge la excepción | La recomendada |
| H-06 | Se corrige el comentario de `core/limits.ts`. Los textos con la cifra se quedan. L-09 gana una frase: tres textos llevan la cifra escrita y, si un límite cambia a propósito en los dos lados, hay que cambiarlos a mano | La recomendada |
| H-07 | Se corrige la cita en `rate-date.spec.ts`. Los commits no se reescriben: nota en la bitácora | La recomendada |
| H-08 | Las capturas salen a `playwright.capturas.config.ts` y `npm run e2e:capturas` lo usa con `-c`. Se comprueba con `--list` que una orden sin opciones enumera solo las pruebas. Se ponen al día `frontend.md` y `tsconfig.e2e.json` | La recomendada |
| H-09 | El test del tiempo agotado en `meta-store.spec.ts`, con su mutación | La recomendada |
| H-10 | **No se pone política de contenido ahora.** Fila nueva en `limitaciones-conocidas.md`, con cómo se cerraría en un despliegue: una cabecera del servidor que sirva la compilación, con `connect-src` limitado al backend y a la API de divisas | — |
| B-01 | **El carácter de la línea 43 no se restaura.** La diferencia ya está dicha en la respuesta y en la bitácora, y la propia línea nombra el U+00A0. No abre una excepción a la regla de no escribir desde la terminal por un carácter invisible | La IA lo había dejado a su decisión |
| B-02, B-04 | Nada | — |
| B-03 | **Sí, una segunda evaluación**, con todo lo anterior aplicado y el oráculo en verde. Mismo subagente, mismas restricciones y la regla 8. Encargo acotado: CA-04, CA-05, CA-08 y CA-16 fila a fila (cada fila de 5.3 a 5.6 con el test que la cubre o «sin test», sin muestreo); el contrato (los apartados de SPEC-01 a SPEC-03 que definen peticiones, respuestas y errores, contra `core/models.ts` y contra lo que el frontend hace con cada código); y los cambios de hoy. Que nombre los caracteres no imprimibles por su código y entregue el informe en su mensaje final. Informe intacto en `evaluacion-frontend-02.md` y respuesta, sin aplicar nada, en `respuesta-evaluacion-frontend-02.md` | La IA lo ofrecía solo para los cuatro criterios; el contrato y los cambios de hoy los añade el Tech Lead |

La decisión se escribe también en el apartado 4 de la respuesta, sin tocar
el informe. **Parada 3** al acabar. El README, el documento de pruebas
manuales y la integración continua vienen después.

### Cambios de la revisión de la parada 2 · lo hecho (desde las 13:15)

Un commit por hallazgo, cada uno con la salida del oráculo con `--e2e` en
un fichero y su código en 0 antes. Las filas se añaden al acabar cada uno.

| # | Commit | Rojo visto o mutación | Qué toca |
|---|---|---|---|
| H-01 | `35d482a` | **Mutación**, porque los cuatro casos nacen en verde: el cargador toma el `id` del texto de `Router.url`. Fallan los dos de `1;x=y` (0 peticiones donde se espera 1); **los dos de `%31` sobreviven** (AE-02) | `detalle.spec.ts`, `simulador.spec.ts` y SPEC-04 (2.1, 5.7, historial) |
| H-02 | `72f8544` | **Rojo visto, dos veces y por aserción**: el anillo de hoy (2,15 sobre el blanco, donde se pide 3 o más) y, con el anillo ya cambiado, el borde de hoy (1,58) | `tokens.css`, `controls.css`, `e2e/contrast.spec.ts`, `e2e/support/contrast.ts`, `e2e/capturas/capturas.spec.ts`, las catorce capturas y SPEC-04 (2.8, CA-15, CA-19, la nota bajo los criterios, historial) |
| H-03 | `8a16e2e` | **Rojo visto por aserción**: los cuatro títulos | `app.routes.ts`, `app.routes.spec.ts`, SPEC-04 (2.1, E-57, CA-11, historial) y la fila L-10 de `limitaciones-conocidas.md` |
| H-04 | `64f5e7b` | **Rojo visto por aserción**: los mensajes de campo llevaban `role="alert"` | `alta.html`, `alta.spec.ts`, SPEC-04 (2.7, historial) y L-10 |
| H-05 | `b33ea2e` | Ninguno: no cambia código ni tests | SPEC-04 (2.3, 2.5, 2.7, 2.8, historial) |
| H-06 | `04404af` | Ninguno: un comentario | `core/limits.ts` y la fila L-09 |
| H-07 | `3728349` | Ninguno: una cita. La prueba sigue en verde dentro del oráculo | `e2e/rate-date.spec.ts` |
| H-08 | `f6d0d04` | Ninguno: es configuración. Comprobado con `--list` en los tres sentidos y generando las capturas con la orden nueva | `playwright.config.ts`, `playwright.capturas.config.ts`, `package.json`, `tsconfig.e2e.json`, `.claude/rules/frontend.md` y cuatro capturas |
| H-09 | `596f1ec` | **Mutación**, dos: el almacén descarta el error por tiempo agotado (falla solo el test nuevo, 1 de 546) y `/meta` espera 20 s (fallan el nuevo y el de `BackendApi`) | `meta-store.spec.ts` |
| H-10 | `13351c9` | Ninguno: una fila de documentación | La fila L-11 de `limitaciones-conocidas.md` |
| Apartado 4 de la respuesta | `d44f18f` | — | `respuesta-evaluacion-frontend-01.md` |
| Esta bitácora | `7f8c974` | — | — |

Precisiones de la IA sobre estos cambios, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| AE-01 | En H-01, los dos casos nuevos del detalle fallaron la primera vez (13:17:01) **por un error de la IA en el test**: esperaba el nombre de la empresa en el `h1`, que dice «Detalle del cliente». Corregida la expectativa (el `h2` de la tarjeta), no el código | Es un rojo que no demuestra nada y hay que decirlo, como AC-13 |
| AE-02 | **El caso `%31` no lo mata ninguna mutación del código de la aplicación que la IA haya sabido escribir.** La descodificación la hace el router de Angular al leer la dirección, antes de que la aplicación vea nada: `Router.url` ya devuelve `/clientes/1`. El test fija lo que hace el router (fallaría si se cambiara su serializador o si una versión de Angular dejara de descodificar), no una línea de la aplicación. El caso `1;x=y` sí muere | El encargo pide una mutación para cada test que nace en verde, y aquí solo muerde en la mitad |
| AE-03 | En el simulador los dos casos nuevos usan una función de apertura propia, `openThroughRouter`, con el router de verdad; los demás tests del simulador siguen dándole el `id` ya descodificado. Y la frase de 5.7 sobre el simulador dice ahora «las tres primeras filas» donde decía «la primera» | Con el `id` ya hecho no se probaría el router, que es de lo que trata H-01; y la frase de 5.7 habría quedado falsa con las dos filas nuevas |
| AE-04 | En H-02, **el botón desactivado conserva el borde claro** (`--color-border`): la variable nueva solo se aplica a `input` y `select`. Y el anillo se escribe como `var(--color-accent)`, no con la cifra repetida | El Tech Lead dijo «campos de formulario»; un botón desactivado no se puede usar y la IA no lo ha contado como campo. Si debe oscurecerse, es una línea |
| AE-05 | La prueba de contraste mira cuatro campos, no todos, y **no mira el simulador**; comprueba además que el fondo del campo es blanco y el de la página no, y que el anillo mide 3 px y el borde 1 px. CA-19 no cita ningún requisito: remite a 2.8 | Los estilos de los campos son comunes y el simulador pide un cliente creado. El Tech Lead pidió una frase y un criterio, no un requisito |
| AE-06 | **El anillo azul sobre un botón, que también es azul**, se distingue solo por los 2 px de separación entre los dos. La IA no lo ha visto en una captura ni lo comprueba ninguna prueba | El contraste que se pidió es contra los fondos, no contra el propio control |
| AE-07 | La captura del alta con foco enfoca el identificador fiscal, el segundo campo, y la función de captura se parte en dos (`screenshot` y `capture`, que quita el foco antes) | Para que se vea el anillo junto a campos sin él, por arriba y por abajo |
| AE-08 | **La página «no encontrada» no tiene título propio**, y SPEC-04 2.1 lo dice así. El Tech Lead nombró cuatro títulos y la IA no ha inventado el quinto. **Consecuencia**: el router solo cambia el título cuando la ruta trae uno, así que quien llega a esa página desde otra vista (con el botón de atrás, por ejemplo) conserva en la pestaña el título de la vista anterior; abierta directamente, dice «SaaS-O-Matic». Se cierra con una línea: `title` en la quinta ruta | La regla 1 de `CLAUDE.md`: si la spec no cubre un caso, no se inventa. **Pregunta para el Tech Lead**: si quiere «Página no encontrada · SaaS-O-Matic» |
| AE-09 | El separador entre el nombre de la vista y el de la aplicación es « · » (un punto medio, U+00B7, entre espacios), elegido por la IA, y el texto se compone con una función de `app.routes.ts`, no con una estrategia de títulos propia. Los títulos solo se comprueban en el test de rutas, no en Playwright | El Tech Lead dijo «el nombre de la aplicación detrás», no con qué separador. La IA no sabe cómo lee ese carácter un lector de pantalla |
| AE-10 | En H-04, **el mensaje del campo de búsqueda del panel también lleva `role="alert"` y se queda**: SPEC-04 2.7 lo nombra junto a los del simulador. Los tests nuevos citan «SPEC-04 2.7», sin requisito | El Tech Lead nombró el alta y el simulador; el del buscador sale mientras se escribe y sin mover el foco, como los del simulador. No hay requisito EARS que hable de `role` |
| AE-11 | De las tres reglas de H-05, **la del `409` sin «Reintentar» no la fija ningún test de la vista**: la IA no ha encontrado ninguno que afirme que ese aviso no trae el botón. La del aviso general de un `422` la fija `api-error.spec.ts` (`retryable: false`) y la de `created_at`, dos tests de `format.spec.ts`. La IA no ha añadido el test, porque el encargo de H-05 es solo la spec. Y en 2.3 ha escrito además que un `422` sin ninguna entrada que mostrar sí lleva «Reintentar», que es lo que ya decía más abajo | Una regla de la spec sin test es justo lo que H-05 señalaba al revés. Es un test de pocas líneas, con su mutación, si el Tech Lead lo quiere |
| AE-12 | En H-08, **la configuración por defecto se queda sin proyectos** (el navegador va en `use`), así que `--project=pruebas` deja de existir; y la de las capturas copia la primera con el operador de propagación, sin la combinación de configuraciones de Playwright. **Para probar la orden nueva la IA generó otra vez las capturas, y cuatro ficheros cambiaron y van en el commit**: las dos del detalle, que llevan la hora de creación, y `simulador-1280.png` y `simulador-usd-1280.png`, **sin que la IA sepa por qué**; ha mirado la primera y se ve igual. El Tech Lead tiene que mirar las capturas de este commit, no las de H-02 | Dos proyectos era justo lo que permitía ejecutar las capturas sin querer. Que dos capturas sin fecha cambien entre dos pasadas dice que no son idénticas bit a bit de una ejecución a otra, y no se había visto |
| AE-13 | El apartado 4 de la respuesta y esta bitácora van en dos commits tras **una sola pasada del oráculo**, no una cada uno. Y la fila L-11 dice, además de lo mandado, lo que la aplicación sí hace (no inserta HTML de fuera, no carga nada de terceros y solo llama a dos sitios), tomado del propio hallazgo y contrastado con una búsqueda en `frontend/src` | Los dos son documentación y el segundo es la propia bitácora; se hizo igual a las 12:42 |

**Nota de las 14:20 sobre AE-11**: decía que la regla de `created_at` la
fijan «dos tests de `format.spec.ts`». **Es uno**, el de la línea 64; el de
la 80 es de la fecha del tipo de cambio. La IA los encontró con una búsqueda
y no abrió el fichero. Lo vio al responder a N-07 (fila C-04 de la
respuesta). La fila se deja como se escribió.

### Segunda evaluación independiente, acotada (B-03) (14:00–14:19)

| Hora | Qué |
|---|---|
| 14:00 | Lanzado el subagente `evaluador` con el árbol limpio en `7f8c974`. El encargo: las tres partes que dictó el Tech Lead (CA-04, CA-05, CA-08 y CA-16 fila a fila y sin muestreo; el contrato de SPEC-01 a SPEC-03 contra `core/models.ts` y contra lo que el frontend hace con cada código; y los cambios de hoy), las restricciones de la primera vez y la regla 8, los caracteres no imprimibles por su código y el informe en su mensaje final |
| 14:11 | Informe recibido. Las 109 filas de 5.3 a 5.6 emparejadas con un test (24, 40, 29 y 16), 77 con «Sí» y 32 con «Parcial»; **CA-04, CA-05, CA-08 y CA-16, `NO CUMPLE`**, por lo que los tests dejan sin comprobar; el contrato, sin diferencias; los diez cambios, «se sostiene» o «correcto»; **9 hallazgos: dos medios (N-01 y N-02) y siete bajos**. Ejecutó el oráculo con y sin `--e2e`, los tests unitarios (546) y `npm run e2e` (18), todos con código 0, y arrancó un backend propio en el 18765, que paró por su PID |
| 14:13 | Guardado y comparado con el registro del subagente: idéntico. Las 96 respuestas del registro llevan el modelo `claude-opus-5-5`; 45 órdenes de terminal y 12 lecturas |
| 14:17 | Respuesta de la IA escrita. **De acuerdo con los nueve.** Dos ya estaban dichos (N-01 es AE-11 y N-06 es AE-08); N-07 corrige una frase que la IA escribió hoy en la spec; seis son huecos de tests de la sesión 07. Cinco casos más, C-01 a C-05. Nada aplicado |
| 14:19 | Commits `8045884` (informe) y `5eb8d8a` (respuesta) |

Precisiones de la IA sobre la segunda evaluación, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| AE-14 | Las filas de la cronología de las 14:00 a las 14:19 se escribieron a las 14:20, no al momento | Mientras el evaluador trabajaba, cualquier edición habría ensuciado su `git status` final, como en AD-08. Las horas salen de `date` y de `git log` |
| AE-15 | **El encargo al evaluador lo redactó la IA.** Para la tercera parte le describió los diez cambios de hoy, porque no puede leer la historia de git ni `04-calidad/`: se los dio como «lo que afirma quien los hizo», pidiéndole buscar dónde no se sostienen. Le resumió además L-09, L-10 y L-11, le pidió numerar los hallazgos como `N-xx` y añadió tres prohibiciones que el Tech Lead no dictó (instalar o descargar, ejecutar las capturas y arrancar `npm start` por su cuenta) | Un evaluador al que se le cuenta qué se hizo tiende a confirmarlo: los diez cambios le salen bien, y eso vale lo que vale. El texto completo consta en el registro del subagente |
| AE-16 | **Los cuatro criterios pasan de «CUMPLE (muestreo)» a `NO CUMPLE`** entre un informe y otro sin que el código haya cambiado en eso: el primero miró una muestra y el segundo, fila a fila y contra la letra del criterio. Los tests son de la sesión 07, que la IA cerró dando esos criterios por cubiertos | Es lo que B-03 quería saber, y hay que decirlo tal cual |
| AE-17 | **Al menos quince números de línea del segundo informe son erróneos** (fila C-01 de la respuesta): lo que afirman es cierto, pero en otra línea. Parecen posiciones dentro de una salida con varios ficheros seguidos. El informe no se toca | Quien siga una referencia del informe puede no encontrarla. No pasó en el primero, que la IA sepa |
| AE-18 | La IA **no ha repetido la parte B** (el contrato) ni ha abierto los tests de las 77 filas marcadas «Sí» | La respuesta dice de acuerdo con los hallazgos, no con todo el informe |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git log -1` (10:46) | Limpio, `2fdf99f` |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000, 4200 y 8001 (10:46:12) | Ninguno en escucha |
| Herramientas | `node --version`, `npm --version`, `uv --version` (10:46) | Node 24.18.0, npm 11.16.0, uv 0.12.13 |
| Oráculo antes de los commits de documentación | `uv run scripts/check.py`, con la salida a un fichero (10:49:46) | Código 0: 23 correctas, 0 con fallo y 1 inactiva |
| **Entradas nuevas del fichero de bloqueo** (ADR-007) | `git diff` de `package-lock.json` y `npm view <paquete> time` para cada entrada nueva (10:51:04) | Tres entradas y ninguna otra línea cambiada: `@playwright/test` 1.65.0 (2026-11-05, 18:30 UTC), `playwright` 1.65.0 (2026-11-05, 18:28 UTC) y `playwright-core` 1.65.0 (2026-11-05, 20:17 UTC). **Las tres, anteriores a `2026-11-07T00:00:00Z`.** La 1.65.1 de las tres es del 2026-11-13, fuera del margen. La suma de comprobación del registro coincide con la del fichero en las tres. Ninguna declara scripts de instalación |
| `npm audit` tras instalar | Salida de `npm install` (10:50) | 27 avisos moderados, los mismos de L-07: Playwright no añade ninguno. Los cuatro scripts de instalación pendientes de ayer siguen sin aprobar |
| **Origen y tamaño del navegador**, sin descargar | `npx playwright install --dry-run`, con y sin `--only-shell`, y `curl -sI -L` a cada dirección (10:51:39) | Destino: la carpeta `ms-playwright` de los datos locales del usuario, que no existía. Origen: `cdn.playwright.dev`, que redirige (`307`) a `storage.googleapis.com/chrome-for-testing-public` para el navegador y a `playwright.download.prss.microsoft.com` para FFmpeg y winldd. Tamaños (`Content-Length`): *headless shell*, 129.186.142 bytes; Chrome for Testing completo, 215.820.284; FFmpeg, 1.663.577; winldd, 128.684 |
| **Lo descargado** | `npx playwright install --only-shell --no-progress chromium` y `du` (11:05:12 a 11:07:43) | Tres carpetas en `ms-playwright`, fuera del repositorio: `chromium_headless_shell-1254` (287 MB), `ffmpeg-1013` (3,9 MB) y `winldd-1007` (260 kB); 303.971.876 bytes en total. `git status` no cambia |
| Qué hace Playwright con un puerto ocupado | Lectura de `node_modules/playwright/lib/runner/index.js` (11:08) | Con `port`, intenta conectar a ese puerto en `127.0.0.1` y en `::1`; si alguno acepta y `reuseExistingServer` es falso, lanza «is already used» sin arrancar la orden |
| Las catorce pruebas | `npm run e2e` (11:13:58 a 11:14:18) | Código 0; 14 correctas en 18,7 s según Playwright, 20 s de reloj con el arranque y la parada de los dos servidores. La más lenta, el recorrido, 2,2 s |
| **Qué escucha y dónde está la base durante una ejecución** | `netstat` y un listado de la carpeta temporal cada segundo y medio, con `npm run e2e` en marcha (11:14:59 a 11:15:20) | El backend escucha en `127.0.0.1:8000` (PID 25460) y el frontend en `[::1]:4200` (PID 12432): **el servidor de desarrollo de Angular escucha solo en IPv6**. La carpeta `saas-o-matic-e2e-…` existe con `e2e.db` dentro mientras dura y no existe al acabar. **`backend/data/saas-o-matic.db`, igual antes y después**: 28.672 bytes y la misma fecha de modificación, 2026-11-14 18:37:20 |
| Puertos y carpetas tras cada ejecución | `netstat -ano` filtrado por `LISTENING` y los dos puertos, y un listado de la carpeta temporal del sistema, después de cada una de las veintitantas ejecuciones de la sesión | Siempre: ninguno en escucha y ninguna carpeta `saas-o-matic-e2e-*` |
| **Con los puertos ocupados** | Una segunda `npm run e2e` mientras la primera tenía los dos servidores en escucha (11:27:25 a 11:27:46) | La segunda acaba en 2 s con código 1: «`Error: http://localhost:8000 is already used…`». Los PID que escuchaban (14416 y 4224) siguen siendo los mismos después. La primera acabó con 13 correctas y 1 fallo: `ENOENT` al cerrar la traza del recorrido, porque la segunda había vaciado `test-results/` |
| Sin la interceptación, la API real no se alcanza | La mutación M11 (11:26:27) | La cabecera muestra el aviso del fallo de los tipos y el selector solo ofrece EUR |
| Las mutaciones están deshechas | `git diff --stat -- backend frontend/src` tras la última (11:26:27) y `git status` antes del commit | Vacío |
| Finales de línea de lo nuevo | `git ls-files --eol` (11:30) | Los diez ficheros, `i/lf w/lf` |
| **Oráculo sin `--e2e`** | `uv run scripts/check.py`, con todo añadido (11:30:26 a 11:32:04) | Código 0: 23 correctas, 0 con fallo y 1 inactiva (Playwright), **igual que ayer** |
| **Oráculo con `--e2e`** | `uv run scripts/check.py --e2e` (11:28:10 a 11:30:07, y otra vez con todo añadido, 11:32:04 a 11:33:59) | Código 0 las dos: 24 correctas, 0 con fallo y 0 inactivas. Tarda unos dos minutos |
| Las capturas | `npm run e2e:capturas` (11:35:00 a 11:35:14) | Código 0; 4 pruebas en 12,7 s; doce ficheros PNG |

Cambios de la revisión de la parada 1:

| Qué | Cómo | Resultado |
|---|---|---|
| **Entradas nuevas del fichero de bloqueo** (ADR-007) | `git diff` de `package-lock.json` y `npm view <paquete> time` (12:07:29) | Dos entradas y ninguna otra línea cambiada: `@types/node` 24.19.2 (2026-10-09; es la última de su línea 24) y `undici-types` 7.24.6 (2026-03-25), que trae la primera. **Las dos, anteriores a `2026-11-07T00:00:00Z`.** La suma de comprobación del registro coincide en las dos. Ninguna declara scripts de instalación. `npm audit`, 27 avisos moderados, como antes |
| Los tipos de `e2e/` | `npx tsc --noEmit -p tsconfig.e2e.json` (12:07:38) y `--listFilesOnly` | Código 0, sin errores. Cubre once ficheros: los diez de `e2e/` y `playwright.config.ts` |
| La comprobación de tipos mira algo | Un error puesto a propósito en `e2e/support/rates.ts` (12:07:54) | `error TS2322: Type 'string' is not assignable to type 'number'`, código 2. Deshecho |
| `npm run lint` con `tsc` | En `frontend/` (12:08) | Código 0 |
| Oráculo antes de cada commit | `uv run scripts/check.py` con la salida a un fichero, antes de los cinco commits de las 12:06 a las 12:20; con `--e2e` además en el cambio 2 | Código 0 en todos: 23 correctas y 1 inactiva sin `--e2e`; 24 y 0 con él |
| Las capturas, otra vez | `npm run e2e:capturas` (12:18:31 a 12:18:45) | Código 0; 4 pruebas en 12,8 s |

Paso 3:

| Qué | Cómo | Resultado |
|---|---|---|
| Antes de lanzar el evaluador | `git status --short`, `git log -1` y `netstat` (12:23:12) | Limpio, `bab2922`; nada en escucha en el 8000 ni en el 4200 |
| Después del evaluador | Lo mismo, y la carpeta temporal del sistema (12:34:22) | Limpio, `bab2922`; nada en escucha en el 8000, el 4200 ni en ningún 80xx; ninguna carpeta `saas-o-matic-e2e-*` |
| Qué agente y qué modelo | Fichero de metadatos y registro del subagente, con un script de solo lectura fuera del repositorio (12:35) | `agentType` `evaluador`; 130 respuestas, todas con el modelo `claude-opus-5-5`; 69 órdenes de terminal y 5 lecturas. El fichero de metadatos trae un campo `pickedEffortModel` con `claude-fable-5-2`, que la IA no sabe interpretar |
| **Informe, intacto salvo un carácter** | Comparación del fichero con el mensaje del registro (12:36:30) | 203 líneas y 20.039 caracteres los dos; **una línea distinta, la 43**: U+0020 en el fichero, U+00A0 en el mensaje. Ningún otro carácter de control ni separador raro en el mensaje |
| Lo que afirman los hallazgos | Apartado 2 de la respuesta (12:37 a 12:40) | Los diez se reproducen en lo que se puede comprobar sin navegador |
| Oráculo antes de los commits del paso 3 | `uv run scripts/check.py` con la salida a un fichero (12:42) | Código 0: 23 correctas y 1 inactiva |

Cambios de la revisión de la parada 2:

| Qué | Cómo | Resultado |
|---|---|---|
| Estado al empezar | `git status --short`, `git log -1` y `netstat` (13:11:49) | Limpio, `ccafe3d`; nada en escucha en el 8000 ni en el 4200 |
| **Oráculo antes de cada commit** | `uv run scripts/check.py --e2e`, con la salida a un fichero y el commit solo con código 0; desde H-03, encadenado en la misma orden. Doce pasadas, de las 13:19 a las 14:19 | Código 0 en las doce: 24 correctas, 0 con fallo y 0 inactivas. Unos dos minutos cada una |
| Puertos y carpetas tras cada ejecución de Playwright | `netstat` y un listado de la carpeta temporal del sistema, después de las doce pasadas del oráculo, las seis ejecuciones sueltas y los tres listados | Siempre: ninguno en escucha y ninguna carpeta `saas-o-matic-e2e-*` |
| Las mutaciones están deshechas | `git diff --stat -- backend frontend/src`, sin contar los `.spec.ts`, tras H-01 (13:18:47) y tras H-09 (13:51) | Vacío las dos veces |
| H-01, verde y mutación | `npx ng test --watch=false`, los dos ficheros (13:17:28) y los 539 tests con la mutación (13:17:56) | 119 en verde; con la mutación, 2 fallos y 537 en verde |
| H-02, rojo y verde | `npx playwright test contrast.spec.ts` (13:23:40, 13:24:07 y 13:24:33) | 4 fallos por el anillo (2,15); 4 fallos por el borde (1,58); 4 en verde |
| H-02 y H-08, capturas | `npm run e2e:capturas` (13:25:09 y, con la configuración nueva, 13:46:53) | Código 0 las dos; 4 pruebas en 12,9 s y en 13,0 s; catorce ficheros. En la segunda cambian cuatro (AE-12) |
| H-03, rojo y verde | `npx ng test`, `app.routes.spec.ts` (13:29:14 y 13:29:37) | 4 fallos de 10 por aserción; 10 en verde |
| H-04, rojo y verde | `npx ng test`, `alta.spec.ts` (13:33:52 y 13:34:18) | 2 fallos de 67 por aserción; 67 en verde |
| H-08, qué enumera cada orden | `npx playwright test --list`, lo mismo con `-c playwright.capturas.config.ts` y lo mismo pidiendo `e2e/capturas` (13:46:22) | 18 pruebas en 5 ficheros, ninguna de capturas; 4 en 1 fichero; 0 |
| H-08, tipos | `npx tsc --noEmit -p tsconfig.e2e.json` (13:46) | Código 0 |
| H-09, verde y mutaciones | `npx ng test`, `meta-store.spec.ts` (13:50:22) y los 546 tests con cada mutación (13:50:50 y 13:51:24) | 13 en verde; 1 fallo y 545 en verde; 2 fallos y 544 en verde |
| Los tres textos con la cifra (H-06) | Búsqueda en `frontend/src/app`, sin los tests (13:40) | `alta-help.ts:29` y `panel.html:20` y `:68` |
| L-11 dice lo que el código hace | Búsqueda de `innerHTML`, `bypassSecurity` y `DomSanitizer` en `frontend/src`, y lectura de `index.html` (13:55) | Ninguna aparición; `index.html` no carga nada de fuera |

Segunda evaluación:

| Qué | Cómo | Resultado |
|---|---|---|
| Antes de lanzar el evaluador | `git status --short`, `git log -1` y `netstat` (14:00:08) | Limpio, `7f8c974`; nada en escucha en el 8000, el 4200 ni en ningún 80xx |
| Después del evaluador | Lo mismo, y la carpeta temporal del sistema (14:11:32) | Limpio, `7f8c974`; nada en escucha, tampoco en el 18765; ninguna carpeta `saas-o-matic-e2e-*` |
| Qué agente y qué modelo | Fichero de metadatos y registro del subagente, con un script de solo lectura fuera del repositorio (14:12) | `agentType` `evaluador`; 96 respuestas, todas con el modelo `claude-opus-5-5`; 45 órdenes de terminal y 12 lecturas |
| **Informe, intacto** | Comparación del fichero con el mensaje del registro (14:13:47) | 362 líneas y 34.340 caracteres los dos; **ninguna línea distinta**; ningún carácter de control ni separador raro en el mensaje |
| Lo que afirman los hallazgos | Apartado 2 de la respuesta (14:14 a 14:17) | Los nueve se reproducen. `new Date('Ejemplo 7')` da una fecha con Node 24.18.0 |
| Las filas de las tablas | Recuento de las líneas de tabla de 5.3 a 5.6 (14:14) | 24, 40, 29 y 16: las del informe |
| Los números de línea del informe | Longitud de cada fichero citado y búsqueda de lo citado (14:14 y 14:16) | Quince referencias erróneas (AE-17) |
| Oráculo antes de los commits del informe y de la respuesta | `uv run scripts/check.py --e2e` (14:17:12 a 14:19:17) | Código 0: 24 correctas |

## 5. No verificado

Al llegar a la parada 3 (14:20), además de lo de las paradas 1 y 2, que
sigue debajo:

- **Nada de lo que propone la segunda respuesta está aplicado.**
- **El caso `%31` de H-01 con una mutación**: ninguna del código de la
  aplicación lo mata (AE-02). Y **H-01 en un navegador** sigue sin verse:
  qué queda en la barra de direcciones.
- **El anillo azul sobre un botón azul** (AE-06) y el contraste del
  control deslizante, que CA-19 no mira.
- **Los títulos de H-03 en un navegador**, y cómo lee un lector de pantalla
  el separador « · » (AE-09). **La página «no encontrada» con el título
  anterior** (N-06) sale de leer el código del router, no de verlo.
- **H-04 con un lector de pantalla**: que el mensaje se lea con su campo y
  que deje de anunciarse cinco veces.
- **Las reglas de H-05 con tests de vista**: la del `409` no tiene ninguno
  (AE-11, N-01).
- **Por qué cambian dos capturas del simulador** entre dos pasadas
  seguidas (AE-12). **Doce de las catorce capturas de `f6d0d04`**: la IA ha
  mirado las dos del alta con foco (las de `72f8544`, que no cambiaron
  después) y `simulador-1280.png`.
- **La parte B del segundo informe** y las 77 filas «Sí» de su parte A
  (AE-18).
- **N-07 en un navegador**: comprobado con Node, que usa el mismo motor.
- **`npx playwright test` sin opciones, ejecutado de verdad**: se ha visto
  con `--list` y a través de `npm run e2e`, que es esa misma orden.

Al llegar a la parada 2 (12:43), además de lo de la parada 1, que sigue
debajo:

- **Nada de lo que proponen la respuesta y el informe está aplicado**, y
  por tanto nada de ello está probado.
- **H-01 en un navegador**: qué queda en la barra de direcciones con
  `/clientes/%31` y con `/clientes/1;x=y`.
- **H-03 y H-04 con un lector de pantalla.**
- **Los colores candidatos de H-02**: calculados, no vistos.
- **Qué política de contenido admite `ng serve`** (H-10).
- **Las filas de 5.3 a 5.6 una a una**: el evaluador las miró por muestreo
  (B-03 de la respuesta).
- **Siete de las doce capturas nuevas**, las generadas sin foco: la IA ha
  mirado dos y tres no cambiaron. El Tech Lead revisó las anteriores, no
  estas.
- **Una ejecución interrumpida con Ctrl+C**: la prueba el Tech Lead.

Al llegar a la parada 1 (11:37):

- **Un servidor ajeno en el 8000 o en el 4200.** El caso del puerto ocupado
  se ha visto con otra ejecución de Playwright, no con un servidor del Tech
  Lead ni con otro programa: la IA no puede ocupar esos puertos. Por el
  código leído, el camino es el mismo. **Tampoco el caso del 4200 ocupado y
  el 8000 libre** (AC-05).
- **Dos ejecuciones a la vez se estorban**: la segunda falla sin tocar los
  servidores, pero vacía `test-results/` y hace fallar a la primera. Con
  los servidores del Tech Lead abiertos no hay primera ejecución que
  estropear, pero `test-results/` se vacía igual.
- **Una ejecución interrumpida** (Ctrl+C, un cierre de la terminal, un
  corte): que los puertos queden libres y la carpeta temporal borrada solo
  se ha visto en ejecuciones que acaban solas, en verde o en rojo.
- **El aviso de «petición a un servicio externo»** de las pruebas no ha
  saltado nunca: ninguna mutación lo ha provocado.
- ~~**Los tipos de `e2e/`**: nadie los compila (AC-09).~~ Desde las 12:13
  los comprueba `npm run lint` (`596dede`).
- **CA-13 mide el ancho del documento**. Un elemento que tuviera su propio
  desplazamiento horizontal interior, o un contenido recortado, no lo
  detectaría. Y cada vista se mira en los estados que la prueba prepara, no
  en todos (no, por ejemplo, el detalle con 50 simulaciones o un error del
  backend a 375 px).
- **Fuera de Windows**: ni las pruebas ni la descarga del navegador. En
  Linux Playwright puede pedir bibliotecas del sistema.
- **Un clon limpio**: `npm ci` seguido de `npx playwright install
  --only-shell chromium` no se ha ejecutado desde cero.
- **Con ventana** (`--headed`, `--ui`): no se puede con lo descargado.
- **Los tiempos son de este equipo y con las cachés calientes** (`.angular`
  y el entorno de `uv`).
- **Nueve de las doce capturas**: la IA ha mirado tres. Las revisa el Tech
  Lead.
- **Que las mutaciones de límites las detecten también los tests
  unitarios**: solo se ejecutó `limits.spec.ts`.
- La licencia y el código de Playwright no se han revisado.
- **Nada del paso 3**: ningún evaluador ha mirado el frontend (CA-12).

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Paso 1: Playwright, las cuatro pruebas y sus mutaciones~~ | Hecho (`895f55d`) |
| ~~**Descarga del navegador de Playwright**~~ | Hecha a las 11:07, con el sí del Tech Lead: solo el *headless shell* |
| ~~Paso 2: capturas de CA-15 y cambio de CA-15 en SPEC-04~~ | Hecho |
| ~~**Parada 1: la revisa el Tech Lead.**~~ | Aprobada a las 12:04, con AC-01 a AC-18 admitidas y sus cinco cambios aplicados |
| **Probar a mano una ejecución interrumpida con Ctrl+C** (puertos y carpeta temporal después) | Del Tech Lead |
| **Para el README de la raíz**, de lo no comprobado de la parada 1: las pruebas de principio a fin solo funcionan en Chromium; solo se han ejecutado en Windows; dos ejecuciones a la vez se estorban; y qué pasa con una ejecución interrumpida | Cuando se escriba el README |
| ~~Paso 3: evaluación independiente del frontend~~ | Hecho: informe en `c149ca0` y respuesta en `be9fef7` |
| ~~**Parada 2: el Tech Lead decide cada hallazgo**, H-01 a H-10, y los casos B-01 a B-04 de la respuesta; en particular, si se restaura el U+00A0 de la línea 43 del informe (B-01). Y las precisiones AD-01 a AD-10~~ | Aprobada a las 13:11: todo decidido y aplicado (`35d482a` a `d44f18f`); el U+00A0 no se restaura |
| ~~Mirar las capturas generadas sin foco~~ | Sustituidas dos veces desde entonces |
| ~~**Parada 2**~~ | Alcanzada a las 12:43 |
| ~~Segunda evaluación acotada (B-03)~~ | Hecha: informe en `8045884` y respuesta en `5eb8d8a` |
| **Parada 3: el Tech Lead decide** N-01 a N-09 y los casos C-01 a C-05 de la segunda respuesta, y revisa las precisiones AE-01 a AE-18. En particular: el título de la página «no encontrada» (AE-08, N-06), qué es «una fecha» en `created_at` (N-07), qué se hace con `panel.spec.ts:304` (N-04) y si CA-05 y CA-08 se cumplen o se precisan (N-03) | Ahora |
| **Mirar las catorce capturas de `f6d0d04`**, en especial las dos del alta con un campo enfocado | Del Tech Lead |
| README, documento de pruebas manuales e integración continua | Después, según el Tech Lead |
| Pendientes heredados que esta sesión no toca: los del apartado 6 de la sesión 07 que no son de la fase de QA (L-07, el oráculo y las fechas del fichero de bloqueo, los de la sesión 06) | A decidir por el Tech Lead |
