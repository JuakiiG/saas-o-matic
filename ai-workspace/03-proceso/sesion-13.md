# Sesión 13 · Cierre de documentación tras la prueba en limpio y la primera integración continua

| | |
|---|---|
| **Fecha** | 2026-11-17 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | Sesión abierta a las 10:40 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

**La conversación es nueva**, sin el contexto de la sesión 12: la IA llega
con lo que ha leído al empezar (`CLAUDE.md`, el `README.md` de la raíz,
`ai-workspace/README.md` y la bitácora de la sesión 12, con sus pendientes)
y con sus cuatro notas de memoria.

**La segunda sesión de IA, «la que audita»**, sigue sin verse desde esta
conversación: lo que esta bitácora dice de ella es lo que dicen el encargo y
la nota de método. La fila de participantes de arriba nombra a quienes
hablan en esta conversación.

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 13: cierre de documentación tras la prueba en limpio y la primera
> integración continua. Antes de nada, leer `CLAUDE.md`, `README.md`,
> `ai-workspace/README.md` y los pendientes de `03-proceso/sesion-12.md`.
> Abrir esta bitácora con el mismo formato que las anteriores.
>
> Parada 1 de la sesión 12 aprobada. Admitidas AK-01 a AK-05. Decisiones
> sobre lo que quedó pendiente:
>
> - AK-02: el nombre de la carpeta de usuario, suelto, se queda donde está.
>   No es un dato personal.
> - N-10: ADR-001 se queda como está. Es un registro del 12/11 y la nota ya
>   explica cómo se ha revisado.
> - N-11, N-13 y la cabecera del guion (AK-04) se corrigen en el paso 3.
> - N-12 y N-14 se quedan.
>
> En esta sesión no cambia el código de la aplicación ni ningún test, ni el
> fichero de la CI. Un commit por paso, con el oráculo en verde por su
> código de salida, sin `--e2e`. El repositorio tiene ahora un remoto,
> `origin`, privado: sin `push`.
>
> Hechos nuevos, que son del Tech Lead y que la IA no tiene que comprobar.
> Van a la bitácora y a los documentos que se nombran en cada paso: A (la
> prueba en limpio, dos veces), B (dos fallos del README, R-1 y R-2) y C
> (la primera ejecución de la integración continua). Están enteros en el
> apartado 3.
>
> **Paso 1. La conversación de la sesión 12.** El Tech Lead ha dejado
> `sesion-12.txt` en `03-proceso/conversaciones/`, sin commit, con las
> mismas sustituciones que las demás. **No editarla.** Poner al día el
> índice: la tabla gana la sesión 12 y la que falta es la 13, por la misma
> razón. Si `ai-workspace/README.md` dice «01 a 11» en algún sitio, pasa a
> «01 a 12».
>
> **Paso 2. El README de la raíz.** Cuatro cambios y ninguno más:
>
> - R-1: reescribir el párrafo de «Abrir `http://localhost:4200`» con lo
>   que pasa de verdad (hecho B). Corto.
> - R-2: en «Tests y oráculo», que cada bloque de órdenes diga su carpeta
>   sin tener que leer la frase (un `cd` explícito desde la raíz del
>   repositorio o equivalente), y que la instalación del navegador de
>   Playwright vaya antes de la orden con `--e2e`.
> - «Requisitos» y «Límites»: «Solo se ha probado en Windows 11» ya no es
>   verdad. Decir lo que hay: a mano, solo en Windows 11; en Linux y en
>   Windows Server, el oráculo con `--e2e` en la integración continua
>   (hecho C), sin nadie mirando un navegador; macOS, nunca.
> - Una insignia de la CI bajo el título y una frase que la nombre en
>   «Tests y oráculo», con enlace a `.github/workflows/ci.yml`. La
>   dirección del repositorio sale de `git remote get-url origin`. Mientras
>   el repositorio sea privado la insignia no se ve desde fuera: decirlo en
>   la bitácora, no en el README.
>
> **Paso 3. `ai-workspace`, en un commit:**
>
> - El «Estado» de `ai-workspace/README.md`, al cerrar la sesión 13: los
>   dos pendientes (la integración continua y el clon limpio) pasan a
>   hechos, con sus fechas y con quién hizo cada cosa (hechos A y C). Lo
>   que sigue sin probar, dicho.
> - La nota «Dos sesiones de IA y una persona», tres retoques y nada más:
>   (N-11) «la carpeta de este mismo directorio que git ignora» pasa a «la
>   carpeta de la raíz del repositorio que git ignora»; (N-13) «salieron de
>   ese borrador» pasa a decir sin ambigüedad que es el borrador de
>   respuesta de la sesión que audita, no el análisis previo; y en la
>   consecuencia de «comprobado» / «he visto», la prueba en limpio del
>   16/11 se añade como otro ejemplo de comprobación ejecutada por la
>   sesión que audita, y la del 17/11, a mano, como del Tech Lead.
> - En `pruebas-manuales.md`, la frase de la cabecera «Lo rellena quien
>   ejecuta el guion» pasa a decir que lo rellena quien lo ejecuta o quien
>   anota a su dictado. La tabla y los resultados no se tocan.
> - Si `limitaciones-conocidas.md` o algún otro documento de `04-calidad`
>   dice que la CI no se ha ejecutado o que no se ha probado fuera de
>   Windows, ponerlo al día con los hechos A y C, y decir cuáles se han
>   tocado.
>
> **Parar ahí (parada 1)** y cerrar la bitácora de la sesión 13. Decir qué
> cambió, qué documentos decían todavía «no ejecutada» o «solo Windows» y
> cuáles se han corregido, y si algo de los hechos A, B y C contradice lo
> que la IA sabe del repositorio. No leer ni citar `.private/`. El `push`
> lo hace el Tech Lead.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 10:44 | — | Mensaje recibido hacia las 10:40 (primera lectura del reloj, 10:40:49). El último commit es `3591202` (2026-11-16 16:24:58), el cierre de la sesión 12, y `origin/main` apunta al mismo (referencia local, sin consultar la red). **`git status`: solo `sesion-12.txt`, sin versionar**, que es lo que anunciaba el encargo. **`netstat` a las 10:41:07: nada escucha en el 8000 ni en el 4200.** `backend/data/saas-o-matic.db`, del Tech Lead: 28.672 bytes, 2026-11-14 18:37, como al cerrar la sesión 12; la IA no lo toca. Lecturas del encargo hechas, y además el índice de las conversaciones, `limitaciones-conocidas.md`, la cabecera de `pruebas-manuales.md` y `.github/workflows/ci.yml`, este solo para leerlo. `sesion-12.txt`, mirada sin editarla (apartado 4). Los hechos A, B y C, contrastados con el repositorio antes de tocar nada (apartado 3). Apertura de esta bitácora |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (10:40)

**Parada 1 de la sesión 12, aprobada. Admitidas AK-01 a AK-05.** Sobre lo
que quedó pendiente:

| Qué | Decisión del Tech Lead |
|---|---|
| AK-02 · el nombre de la carpeta de usuario, suelto, en `sesion-11.txt` y en la bitácora de la sesión 11 | **Se queda donde está.** No es un dato personal |
| N-10 · el motivo 3 de ADR-001 se apoya en quien lee cada diff | **ADR-001 se queda como está.** Es un registro del 12/11 y la nota ya explica cómo se ha revisado |
| N-11 · «este mismo directorio» | **Se corrige** en el paso 3 |
| N-13 · «ese borrador» | **Se corrige** en el paso 3 |
| AK-04 · la cabecera del guion, «Lo rellena quien ejecuta el guion» | **Se corrige** en el paso 3 |
| N-12 y N-14 | **Se quedan** |

La bitácora de la sesión 12 no se toca: la aprobación queda anotada aquí.

**Reglas de esta sesión**, del encargo:

- **No cambia el código de la aplicación ni ningún test, ni el fichero de
  la CI.**
- **Un commit por paso**, con el oráculo en verde por su código de salida,
  **sin `--e2e`**.
- **`sesion-12.txt` no se edita**: entra tal como la dejó el Tech Lead.
- **En el README de la raíz, cuatro cambios y ninguno más.**
- **En la nota de método, tres retoques y nada más.** En
  `pruebas-manuales.md`, la tabla y los resultados no se tocan.
- **Hay un remoto, `origin`, privado. La IA no hace `push`.**
- **`.private/` no se lee ni se cita.**

### Hechos nuevos del encargo

**Son del Tech Lead. La IA no los ha comprobado**, porque el encargo dice
que no tiene que hacerlo y porque casi ninguno se puede ver desde aquí: los
clones no están en este repositorio y la ejecución de la integración
continua está en GitHub. Lo que sí se puede contrastar con el repositorio
está en la tabla de más abajo.

**A. Prueba en limpio, dos veces, las dos sobre `3591202` y en Windows 11.**

- **16/11, de 17:27 a 17:33, la sesión que audita**, con autorización del
  Tech Lead para usar los puertos 8000 y 4200: clon en una carpeta vacía,
  las órdenes del README al pie de la letra, la parte de navegador con el
  Chromium de Playwright (no con Chrome), y el oráculo con `--e2e` dentro
  del clon: 24 correctas, 0 inactivas.
- **17/11, de 08:34 a 10:03, el Tech Lead, a mano**, en otro clon vacío,
  con Chrome y solo con el README delante: backend, `npm ci` (los dos
  avisos anunciados y solo esos), `npm start`, alta de un cliente de
  España, el identificador que da error, alta de un cliente de otro país,
  una simulación de 15 usuarios, divisa USD, `/docs`, y el oráculo sin
  opciones (23 correctas, 1 inactiva) y con `--e2e` (24 correctas, 0
  inactivas).
- En los dos clones, después: árbol de git limpio, puertos libres y
  ninguna carpeta temporal.

**B. Dos fallos del README que salieron de ahí.**

- **R-1.** «Arranque» dice que desde `http://127.0.0.1:4200` la aplicación
  muestra «No se ha podido conectar con el servidor.». No es lo que pasa:
  en este Windows esa dirección no carga (Chrome: «No se puede acceder a
  este sitio web»), porque `ng serve` escucha solo en `[::1]:4200`. El
  mensaje sí sale cuando la aplicación carga desde otro origen: visto el
  16/11 con `http://[::1]:4200`. La cabecera `access-control-allow-origin`
  solo se devuelve al origen `http://localhost:4200` (visto con `curl`).
- **R-2.** En «Tests y oráculo» el Tech Lead lanzó `uv run
  scripts/check.py` desde `frontend/`, que es donde deja «Arranque», y
  falló: «Failed to spawn: scripts/check.py». «Desde la raíz» está en la
  frase y no en el bloque de órdenes. Además, las órdenes del oráculo van
  antes que la instalación del navegador de Playwright, que el `--e2e`
  necesita.

**C. Integración continua, primera ejecución, el 17/11.** El Tech Lead hizo
`push` de `3591202` a un repositorio privado de GitHub a las 10:09 y la CI
se lanzó sola. Los dos trabajos, en verde, y en los dos la línea «ORÁCULO
EN VERDE · 24 correctas, 0 con fallo, 0 inactivas»:

- **Oracle (ubuntu-latest)**: Ubuntu 26.04.1, imagen `ubuntu-26.04` versión
  20261111.196.1. Tres minutos y medio.
- **Oracle (windows-latest)**: Microsoft Windows Server 2025, imagen
  `windows-2025-vs2026` versión 20261103.298.1. Seis minutos.
- En los dos: uv 0.12.13, Node 24.18.0 y npm 11.16.0, y el navegador de
  Playwright descargado desde cero.
- Una anotación informativa de GitHub: la etiqueta `ubuntu-latest` pasa a
  Ubuntu 26. No es un fallo.

Es la primera vez que el proyecto se ejecuta fuera de Windows. Sigue sin
probar: macOS, y Linux a mano con un navegador.

### Los hechos A, B y C frente a lo que la IA sabe del repositorio

El encargo pide decir si algo los contradice. **Nada los contradice.** Lo
que sigue es lo que el repositorio dice de cada uno, mirado a las 10:41 y
las 10:42, antes de tocar nada.

| # | Hecho | Qué dice el repositorio | Qué ha hecho la IA |
|---|---|---|---|
| HE-1 | A y C: las dos pruebas y el `push` son sobre `3591202` | `HEAD` y `origin/main` son `3591202`. Es el cierre de la sesión 12 | Nada. Coincide |
| HE-2 | A y C: 23 correctas y 1 inactiva sin opciones; 24 y 0 con `--e2e`; la línea «ORÁCULO EN VERDE · 24 correctas, 0 con fallo, 0 inactivas» | Las cuatro pasadas de la sesión 12, sin `--e2e`, dieron 23 correctas y 1 inactiva, Playwright. La línea es, letra por letra, la que escribe `scripts/oracle/report.py` cuando no hay ninguna inactiva | Nada. Coincide |
| HE-3 | A: las pruebas se hicieron en clones, con los puertos 8000 y 4200 | La base local del Tech Lead en esta copia de trabajo sigue como al cerrar la sesión 12 (28.672 bytes, 2026-11-14 18:37): nada ha escrito en ella. La regla 8 de `CLAUDE.md` sobre esos puertos habla de los servidores de esta sesión; la que los usó fue la otra, con autorización | Nada. Coincide |
| HE-4 | B, R-1: `ng serve` escucha solo en `[::1]:4200` y `http://127.0.0.1:4200` no carga | La bitácora de la sesión 09 ya decía, en «No verificado», que en este equipo el servidor de desarrollo escucha solo en `[::1]:4200`, y AG-08 decía que la frase del README no salía de haberlo visto, sino de SPEC-04, 2.9. `frontend/package.json`: `npm start` es `ng serve`, sin `--host`. `backend/app/config.py`: el origen por defecto es `http://localhost:4200` | Nada. Coincide. **Queda un texto con la frase antigua, que la IA no ha tocado: SPEC-04, 2.9** («Desde otro origen (`http://127.0.0.1:4200` lo es) el navegador oculta todas las respuestas del backend y cada llamada acaba en `network_error`»). Lo que dice del origen es cierto; el ejemplo es el que en este Windows no carga. Es una spec aprobada y el encargo no la nombra |
| HE-5 | B, R-2: «Arranque» deja en `frontend/` y el bloque del oráculo no dice su carpeta | Es así: el último bloque de «Arranque» empieza por `cd frontend` y el del oráculo no lleva carpeta. El guion de pruebas manuales ya avisaba del mismo caso en su paso 30 («`frontend/`, donde acaba el paso 29: la tercera usa una ruta relativa y desde allí falla») | Nada. Coincide |
| HE-6 | C: los trabajos se llaman «Oracle (ubuntu-latest)» y «Oracle (windows-latest)», con uv 0.12.13, Node 24.18.0 y npm 11.16.0, y descargan el navegador | `ci.yml`: `name: Oracle (${{ matrix.os }})`, `version: "0.12.13"`, `node-version: "24.18.0"`, sin caché, y un paso que instala el navegador. El límite de cada trabajo es de 20 minutos | Nada. Coincide. **Dos versiones que el hecho C no da y el fichero no fija**: la revisión de Python 3.12 que eligió uv (el fichero pide «3.12») y el git de cada ejecutor. La tabla de «Requisitos» del README dice Python 3.12.0 y git 2.55.0, que son las de este equipo |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short`, `git log -1` y `git branch -vv` (10:40:49 a 10:42:22) | `3591202`; solo `sesion-12.txt`, sin versionar; `main` sigue a `origin/main`, en el mismo commit |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000 y 4200 (10:41:07) | Ninguno en escucha |
| La base local del Tech Lead | Listado de `backend/data/` (10:41:07) | 28.672 bytes, 2026-11-14 18:37 |
| El código, los tests y la CI, como en `3591202` | `git diff --stat 3591202 -- backend frontend scripts .github` (10:44:32) | Vacío |

`sesion-12.txt`, **solo con órdenes de lectura**:

| Qué | Cómo | Resultado |
|---|---|---|
| Forma | `wc`, bytes de retorno de carro y de salto de línea, espacios finales, último byte y «❯» (10:41:25 y 10:41:47) | 1.394 líneas y 80.706 bytes; ningún retorno de carro ni espacio final; acaba en salto de línea. «❯»: 2 al principio de línea (el `/clear` y el encargo de la sesión 12) y 8 más dentro del texto |
| Principio y final | Sus 12 primeras líneas y sus 8 últimas (10:41:25) | Empieza con el `/clear` y el encargo de la sesión 12 y acaba con la respuesta de la parada 1 y un «※ recap» |
| Lo que queda de las sustituciones | Búsquedas de rutas de usuario, de `noreply`, de cualquier email, del nombre de usuario de GitHub y de `<usuario>` (10:41:25 a 10:44:32) | Ninguna ruta de usuario (ni `Users` ni `AppData`); ningún email; el nombre de usuario de GitHub no aparece. `noreply`, 4 veces, y `<usuario>`, 8: las doce son texto que habla de las sustituciones (el encargo de la sesión 12, el índice y su bitácora), no rutas ni direcciones |
| Huella antes del commit | `sha256sum`, guardada fuera del repositorio (10:41:25) | Para compararla con lo que quede en el commit del paso 1 |

## 5. No verificado

*(Se escribe al cerrar.)*

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| Paso 1: `sesion-12.txt` y el índice al día | En curso |
| Paso 2: el README de la raíz, cuatro cambios | Después |
| Paso 3: `ai-workspace` (el «Estado», la nota, la cabecera del guion y lo que diga «no ejecutada» en `04-calidad`) | Después |
| Parada 1 | Al acabar el paso 3 |
