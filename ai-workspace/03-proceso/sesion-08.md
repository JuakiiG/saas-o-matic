# Sesión 08 · Fase de QA del frontend, primera parte: Playwright, capturas y evaluación independiente

| | |
|---|---|
| **Fecha** | 2026-11-15 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | **Sesión abierta (10:46).** Encargo: Playwright con cuatro pruebas y sus mutaciones (paso 1), las capturas de CA-15 (paso 2) y **parada 1**; después, solo con la aprobación del Tech Lead, la evaluación independiente del frontend (paso 3) y **parada 2**. Se rellena al llegar a cada parada |

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

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git log -1` (10:46) | Limpio, `2fdf99f` |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000, 4200 y 8001 (10:46:12) | Ninguno en escucha |
| Herramientas | `node --version`, `npm --version`, `uv --version` (10:46) | Node 24.18.0, npm 11.16.0, uv 0.12.13 |

## 5. No verificado

Se rellena al llegar a cada parada.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| Paso 1: Playwright, las cuatro pruebas y sus mutaciones | En curso |
| **Descarga del navegador de Playwright**: la IA dice origen y tamaño y espera el sí del Tech Lead | Antes de descargar |
| Paso 2: capturas de CA-15 y cambio de CA-15 en SPEC-04 | Después del paso 1 |
| **Parada 1** | Al acabar el paso 2 |
| Paso 3: evaluación independiente del frontend | Solo con la parada 1 aprobada |
| **Parada 2** | Al acabar el paso 3 |
| README, documento de pruebas manuales e integración continua | Después, según el Tech Lead |
| Pendientes heredados que esta sesión no toca: los del apartado 6 de la sesión 07 que no son de la fase de QA (L-07, el oráculo y las fechas del fichero de bloqueo, los de la sesión 06) | A decidir por el Tech Lead |
