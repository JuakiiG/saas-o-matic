# Sesión 08 · Fase de QA del frontend, primera parte: Playwright, capturas y evaluación independiente

| | |
|---|---|
| **Fecha** | 2026-11-15 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | **Parada 1 alcanzada (11:37): Playwright y las capturas de CA-15.** `@playwright/test` 1.65.0 instalado y catorce pruebas en `frontend/e2e/` (CA-14, CA-13 con la cabecera del aviso, L-09 y la fila de la zona horaria), en un commit (`895f55d`); el oráculo sale con código 0 con `--e2e` (24 correctas, 0 inactivas) y sin él sigue como ayer (23 y 1 inactiva). Las pruebas tardan unos 20 s con el arranque de los dos servidores. Doce capturas en `04-calidad/capturas/` y CA-15 cambiado en SPEC-04. **Lo que el Tech Lead tiene que conocer**: (1) **la primera mutación de CA-14 sobrevivió**: con la API de divisas interceptada con `page.route()`, Playwright respondía él mismo a las comprobaciones previas de CORS y la prueba no comprobaba el CORS del backend; se cambió el mecanismo (protocolo de depuración de Chromium, solo para la URL de los tipos) y la mutación muere (AC-03); (2) la IA ha hecho los commits sin que se le pidiera cada uno (AC-01); (3) son catorce pruebas, no cuatro, y L-09 cubre todos los límites y no un campo (AC-08); (4) los ficheros de `e2e/` no los compila nadie con tipos (AC-09). Quedan sin aprobar las precisiones AC-01 a AC-18. **El paso 3 (evaluador) no se ha empezado**: espera la aprobación de esta parada. · Antes, sesión abierta a las 10:46 |

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
| 4 · Fecha del tipo | `rate-date.spec.ts` | 1: navegador en `America/Los_Angeles`, USD elegido, en el simulador y en el detalle | SPEC-04/E-27, fila de 5.5 |

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

## 5. No verificado

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
- **Los tipos de `e2e/`**: nadie los compila (AC-09).
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
| **Parada 1: la revisa el Tech Lead.** Las doce capturas de `04-calidad/capturas/`; las precisiones AC-01 a AC-18; y qué hacer con AC-09 (los tipos de `e2e/`) y AC-11 (las frases de SPEC-04 y de D-09 que ya no son ciertas) | Ahora |
| Paso 3: evaluación independiente del frontend | Solo con la parada 1 aprobada |
| **Parada 2** | Al acabar el paso 3 |
| README, documento de pruebas manuales e integración continua | Después, según el Tech Lead |
| Pendientes heredados que esta sesión no toca: los del apartado 6 de la sesión 07 que no son de la fase de QA (L-07, el oráculo y las fechas del fichero de bloqueo, los de la sesión 06) | A decidir por el Tech Lead |
