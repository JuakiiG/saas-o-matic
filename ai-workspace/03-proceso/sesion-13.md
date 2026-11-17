# Sesión 13 · Cierre de documentación tras la prueba en limpio y la primera integración continua

| | |
|---|---|
| **Fecha** | 2026-11-17 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | **Parada 1 alcanzada (10:54): los tres pasos, hechos, cada uno en su commit y con el oráculo en código 0 antes, sin `--e2e`.** No ha cambiado el código de la aplicación, ningún test ni el fichero de la CI: entre `3591202` y el último commit no cambia nada en `backend/`, `frontend/`, `scripts/` ni `.github/`. **Paso 1** (`bc4ee0d`): `sesion-12.txt`, idéntica byte a byte a la que dejó el Tech Lead, y el índice al día. **Paso 2** (`2a33120`): el README de la raíz, con R-1, R-2, dónde se ha probado y la insignia. **Paso 3** (`e965ce2`): el «Estado» al cerrar la sesión 13, los tres retoques de la nota y la cabecera del guion. **Lo que el Tech Lead tiene que conocer**: (1) **nada de los hechos A, B y C contradice el repositorio** (HE-1 a HE-6); (2) **quedan dos textos con frases antiguas que la IA no ha tocado**, porque están fuera de lo que nombra el encargo: ADR-005 dice que Playwright no se ha ejecutado en Linux, y SPEC-04, 2.9, pone `http://127.0.0.1:4200` como ejemplo de origen desde el que se ocultan las respuestas; (3) **la insignia escribe por primera vez el nombre de usuario de GitHub en un fichero versionado**, y mientras el repositorio sea privado no se ve desde fuera (AL-05); (4) en los bloques de «Tests y oráculo» la carpeta va en una línea de comentario, no en un `cd` (AL-03); (5) el «Estado» gana una línea que el encargo no daba: los commits de esta sesión no los ha probado nadie (AL-06). Quedan sin aprobar AL-01 a AL-07. · Antes, sesión abierta a las 10:40 |

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
| 10:48 | `e3e2c61` | **Apertura de la bitácora**, 10:47:16 según `git log`, tras el oráculo sin `--e2e` de 10:45:39 a 10:47:16, código 0 (23 correctas, 1 inactiva); la salida, a un fichero, y el commit, en la misma orden, solo con ese código. Solo entra `sesion-13.md`: `sesion-12.txt` sigue sin commit (AL-01) |
| 10:48 | — | **Paso 1, el índice**: `conversaciones/README.md`, con la herramienta de edición, de 62 a 63 líneas. La tabla gana la sesión 12 (1.394 líneas) y dice «de la 01 a la 12»; «Lo que falta» nombra la sesión 13 en lugar de la 12. «Qué se ha cambiado al publicarlas» no se ha tocado (AL-02). En `ai-workspace/README.md`, la fila de `03-proceso` de «Cómo leerlo» decía «sesiones 01 a 11» y dice «01 a 12»; era el único sitio (10:47:34). Los 25 destinos de los enlaces del índice existen. `sesion-12.txt` no se ha tocado |
| 10:50 | `bc4ee0d` | **Paso 1**, 10:49:19 según `git log`: `sesion-12.txt`, el índice y la fila de `ai-workspace/README.md`; tres ficheros, 1.399 líneas añadidas y 4 quitadas. Antes, oráculo sin `--e2e` de 10:47:52 a 10:49:19, código 0 (23 correctas, 1 inactiva). Después (10:49:19): **`sesion-12.txt` tiene en el commit la misma huella que el fichero que dejó el Tech Lead** y el de la carpeta sigue igual; `git ls-files --eol` dice `i/lf w/lf` |
| 10:50 | — | **Paso 2, el README de la raíz**, con la herramienta de edición: los cuatro cambios del encargo, 39 líneas añadidas y 12 quitadas (10:49:59). (1) **R-1**: el párrafo de «Abrir `http://localhost:4200`», reescrito con el hecho B; pasa de 4 a 7 líneas. (2) **R-2**: en «Tests y oráculo», tres bloques en lugar de dos, cada uno con una primera línea que dice su carpeta, y la instalación del navegador antes de la orden con `--e2e` (AL-03). (3) **Dónde se ha probado**: «Requisitos» dice «Probado a mano» y gana un párrafo detrás de la tabla; en «Límites», la primera fila dice a mano, en la integración continua y nunca (AL-04). (4) **La insignia**, bajo el título, y una frase en «Tests y oráculo» con enlace a `.github/workflows/ci.yml` (AL-05). Lo demás del README no se ha tocado: ni las cifras de tests ni su fecha |
| 10:52 | `2a33120` | **Paso 2**, 10:51:44 según `git log`: solo `README.md`, 39 líneas añadidas y 12 quitadas. Antes, oráculo sin `--e2e` de 10:50:19 a 10:51:44, código 0 (23 correctas, 1 inactiva) |
| 10:52 | — | **Paso 3, `ai-workspace`**, con la herramienta de edición. (1) **El «Estado»** de `ai-workspace/README.md`: «al cerrar la sesión 13»; el bloque «Pendiente» desaparece y sus dos líneas pasan a ser dos hechos de la lista, el clon limpio (las dos pruebas, con fecha, horas y quién) y la integración continua (hecho C); detrás, un bloque «Sin probar» con macOS, Linux a mano y los commits de esta sesión (AL-06). (2) **La nota**, los tres retoques: «la carpeta de la raíz del repositorio que git ignora» (N-11); «salieron del borrador de respuesta de la sesión que audita, no del análisis previo: los redactó ella con el Tech Lead» (N-13); y, en la consecuencia de «comprobado» o «he visto», la prueba en limpio del 16/11 como segundo ejemplo y la del 17/11 como segunda excepción. Lo demás de la nota no cambia; su línea más larga sigue en 76 columnas. (3) **`pruebas-manuales.md`**: «Lo rellena quien ejecuta el guion o quien anota a su dictado.»; ninguna línea de tabla cambia (10:52:30). (4) **En `04-calidad` no se ha tocado nada más**: ningún documento de esa carpeta decía que la CI no se hubiera ejecutado ni que solo se hubiera probado en Windows (apartado 3) |
| 10:54 | `e965ce2` | **Paso 3**, 10:54:14 según `git log`: `ai-workspace/README.md` y `pruebas-manuales.md`, 53 líneas añadidas y 16 quitadas. Antes, oráculo sin `--e2e` de 10:52:49 a 10:54:14, código 0 (23 correctas, 1 inactiva). Después (10:54:14): entre `3591202` y este commit cambian 6 ficheros, **ninguno en `backend/`, `frontend/`, `scripts/` ni `.github/`**; nada escucha en el 8000 ni en el 4200; `backend/data/saas-o-matic.db`, igual. La IA no ha arrancado ningún servidor ni ha hecho `push` |
| 10:54 | *(este commit)* | **Cierre de esta bitácora para la parada 1.** Las filas anteriores se han escrito cada una en su momento, con el fichero sin commit entre la apertura y este cierre: los commits de los pasos llevan solo los ficheros de su paso. La IA para aquí: el Tech Lead revisa los tres pasos, la tabla de documentos, HE-1 a HE-6 y las precisiones AL-01 a AL-07. El `push` es suyo. La hora de este commit se ve con `git log` |

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

### Los tres pasos · lo hecho

| # | Commit | Qué toca |
|---|---|---|
| 1 · La conversación de la sesión 12 | `bc4ee0d` | `sesion-12.txt`, tal como la dejó el Tech Lead; `conversaciones/README.md`; y una fila de `ai-workspace/README.md` («01 a 12») |
| 2 · El README de la raíz | `2a33120` | `README.md`: la insignia, «Requisitos», el párrafo de «Abrir `http://localhost:4200`», «Tests y oráculo» y la primera fila de «Límites» |
| 3 · `ai-workspace` | `e965ce2` | `ai-workspace/README.md`: el «Estado» y tres frases de la nota. `04-calidad/pruebas-manuales.md`: una frase de la cabecera |

Ningún test nuevo ni cambiado: no hay rojo ni mutación que anotar.

### Qué documentos decían todavía «no ejecutada» o «solo Windows»

Búsqueda en todos los `.md` versionados, sin `.private/` (10:42:22 y
10:42:50). Fuera de las bitácoras y de los informes de evaluación:

| Documento | Qué decía | Qué se ha hecho |
|---|---|---|
| `README.md` de la raíz, «Requisitos» | «Probado con estas versiones, y solo con ellas», con Windows 11 en la tabla | **Corregido** (paso 2): «Probado a mano…» y un párrafo con la integración continua y macOS |
| `README.md` de la raíz, «Límites» | «Solo se ha probado en Windows 11. En Linux y en macOS no se ha ejecutado nunca» | **Corregido** (paso 2) |
| `ai-workspace/README.md`, «Estado» | La integración continua «no se ha ejecutado nunca» y «sería la primera ejecución fuera de Windows»; pendiente, la instalación desde un clon limpio | **Corregido** (paso 3) |
| `02-arquitectura/ADR-005-dependencias-de-test.md`, «No verificado» | Las pruebas de Playwright «pasan en Windows 11 con Node 24.18.0; **en macOS y en Linux no se han ejecutado**» | **Nada.** No está en `04-calidad` y el encargo no lo nombra. Con el hecho C, lo de Linux ya no es verdad; lo de macOS, sí. Ese apartado se ha puesto al día otras veces tachando la frase antigua. Lo decide el Tech Lead |
| `04-calidad/` | Ningún documento dice que la CI no se haya ejecutado ni que solo se haya probado en Windows. `limitaciones-conocidas.md` no habla de sistemas operativos ni de la CI | **Nada que corregir.** De `04-calidad` solo se ha tocado la frase de la cabecera de `pruebas-manuales.md`, que es del encargo |
| `04-calidad/pruebas-manuales.md`, paso 30 | Trae las órdenes de «Linux y macOS». No dice que se hayan ejecutado, y no se han ejecutado nunca (AG-12 de la sesión 09) | Nada |
| `CLAUDE.md`, regla 4 | El oráculo es un script de Python porque «funciona igual en Windows, macOS y Linux» | Nada. Es el motivo de una decisión, no un resultado. Hoy está visto en Windows y, por la integración continua, en Linux; en macOS, nunca |
| Las bitácoras de las sesiones 03 a 12, en «No verificado» | «Nada fuera de Windows», «la integración continua no se ha ejecutado nunca», «un clon limpio, tampoco» | Nada: son el registro de su día |
| Los informes de evaluación de `04-calidad/` | — | No se han mirado para esto: se guardan intactos |

Visto de paso en `limitaciones-conocidas.md` y **sin tocar**, porque no es
lo que pedía el encargo: su cabecera dice que el README de la raíz «se
escribirá cuando el proyecto pueda levantarse en local», y L-06 dice que
«el frontend todavía no existe, así que no hay test». El README existe
desde la sesión 09 y hay cuatro ficheros de test del frontend que citan ese
límite (10:54:46).

### Precisiones de la IA, **sin aprobar**

| # | Precisión | Motivo |
|---|---|---|
| AL-01 | **La sesión tiene cinco commits**: el de apertura de la bitácora, los tres pasos y el cierre. En el de apertura solo entra `sesion-13.md`; `sesion-12.txt` sigue sin commit hasta el paso 1 | Es lo que se hizo en las sesiones 09 a 12 y lo admitido en AK-01 |
| AL-02 | **Dos cosas del índice.** (1) «Qué se ha cambiado al publicarlas» **no se ha tocado**: sigue dando las cuentas de las sustituciones hasta la sesión 11 y no dice nada de la 12. En `sesion-12.txt` no hay ninguna ruta de usuario ni ningún correo, sustituidos o no: si el original los llevaba, la IA no puede saberlo. (2) La entrada de «Lo que falta» decía «la que publica esta versión de los ficheros» y dice «la que publica la conversación de la 12» | (1) El encargo no pedía tocar ese apartado y no daba cuentas, como sí las dio el de la sesión 12. Si en la 12 no hubo nada que sustituir, el apartado es exacto; si lo hubo, le falta una cifra que solo tiene el Tech Lead. (2) En esta sesión no se regenera ningún fichero: solo entra uno nuevo |
| AL-03 | **R-2: la carpeta de cada bloque va en una primera línea de comentario** («# en la raíz del repositorio»), no en un `cd`. Son tres bloques: el oráculo sin opciones, con «(desde frontend/: cd ..)»; la instalación del navegador, que entra en `frontend` y acaba con `cd ..`; y el oráculo con `--e2e`. La frase de encima dice además «no desde `frontend/`, que es donde deja «Arranque»» | El encargo admitía «un `cd` explícito desde la raíz del repositorio o equivalente». Un `cd` no puede nombrar la raíz: depende de dónde esté quien lo teclea, que es justo lo que falló. La línea es un comentario en PowerShell y en Bash; **pegada en `cmd.exe` da un error de orden no reconocida, sin más efecto**. Si el Tech Lead prefiere otra forma, se cambia |
| AL-04 | **Lo que el README dice ahora de dónde se ha probado.** «Límites» nombra los sistemas del hecho C («Linux (Ubuntu 26.04)» y «Windows Server 2025») y la primera ejecución («2026-11-17, en verde»). «Requisitos» dice «con las mismas versiones de uv, Node.js y npm» y **no dice nada de Python ni de git** en la integración continua | Los sistemas y la fecha son del hecho C. Esa frase es una foto del 17/11: la etiqueta `ubuntu-latest` se mueve y una ejecución futura puede fallar; lo que está al día es la insignia. De Python y de git, HE-6: el hecho C no da esas versiones |
| AL-05 | **La insignia.** La dirección es la de `git remote get-url origin` sin el `.git`, con la ruta de GitHub para la insignia de un workflow (`/actions/workflows/ci.yml/badge.svg`); enlaza a las ejecuciones de ese workflow y no fija rama. **Mientras el repositorio sea privado no se ve desde fuera**: GitHub solo sirve la imagen a quien tiene acceso, y los demás ven una imagen rota o un 404. **Y escribe por primera vez el nombre de usuario de GitHub en un fichero versionado**: en la sesión 12 se comprobó que las conversaciones no lo llevaban. La IA no la ha visto dibujada ni ha consultado la red | El encargo manda poner la insignia, sacar la dirección del remoto y decir aquí, no en el README, lo del repositorio privado. Lo del nombre de usuario se dice porque es lo contrario de lo que hizo la sustitución del correo: va con la dirección del repositorio, que es donde estará quien lo lea, y el encargo lo pide; si no debe estar, la insignia se quita |
| AL-06 | **Tres cosas del «Estado».** (1) El bloque «Pendiente» pasa a llamarse «Sin probar» y **gana una línea que el encargo no daba: los commits de la sesión 13**. Las dos pruebas en limpio y la integración continua son sobre `3591202`; el README corregido no se ha vuelto a seguir desde un clon, y la integración continua no verá estos commits hasta el próximo `push`. (2) El paréntesis dice «las sesiones 11, 12 y 13 solo han cambiado documentación». (3) **Sus cifras no se han vuelto a contar**: son las de la sesión 10 | (1) El encargo pide decir lo que sigue sin probar, y eso también lo está: el README que hoy tiene el repositorio no es el que se probó. Si sobra, se quita. (2) y (3) Como en AK-04: lo dice `git diff 3591202 HEAD -- backend frontend scripts .github`, vacío; la salida del oráculo solo enseña los 96 tests de los scripts |
| AL-07 | **Dos errores de la IA en esta sesión.** (1) **Una orden mal escrita al mirar `sesion-12.txt`**: la primera cuenta (10:41:25) dio 1.394 líneas con retorno de carro y 40 con espacios finales, porque los dos patrones estaban mal escritos; contando los bytes (10:41:47), ninguno. (2) **Las horas de las filas no salen de una lectura hecha al escribirlas**, sino de la última lectura anterior: la fila de apertura (10:44) se escribió entre las 10:44:32 y las 10:45:39; las dos de las 10:48, entre las 10:47:34 y las 10:47:52; las dos de las 10:50, entre las 10:49:59 y las 10:50:19; las dos de las 10:52, entre las 10:52:30 y las 10:52:49. Las dos de las 10:54, con el reloj leído justo antes (10:54:53) | (1) No llegó a ningún texto: se anota porque la comprobación que vale es la segunda. (2) La regla 6 pide el reloj en el momento de escribir cada fila. Ninguna hora está estimada, pero las ocho primeras son el minuto de la lectura anterior y pueden ir un minuto por detrás |

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

Paso 1:

| Qué | Cómo | Resultado |
|---|---|---|
| Que no quede ningún «01 a 11» | Búsqueda en los dos README y en el índice (10:47:34) | Ninguno |
| Los enlaces del índice | `test -e` de sus 25 destinos (10:47:34) | Existen todos |
| **`sesion-12.txt` entra en el commit sin cambiar** | SHA-256 del fichero antes del commit (10:41:25), tal como queda en `bc4ee0d` (`git show`) y en la carpeta después (10:49:19) | Las tres, idénticas |
| Finales de línea de lo versionado | `git ls-files --eol` del fichero (10:49:19) | `i/lf w/lf` |

Pasos 2 y 3:

| Qué | Cómo | Resultado |
|---|---|---|
| Cuánto cambia el README de la raíz | `git diff --stat` y `git diff -U0` (10:49:59) | 39 líneas añadidas y 12 quitadas, en 12 trozos. Las líneas de más de 80 columnas son la insignia y seis que ya lo eran (la imagen y filas de tablas) |
| El enlace de la frase de la CI | `test -e .github/workflows/ci.yml` (10:49:59) | Existe |
| La línea de comentario de los bloques, en Bash | Un comentario seguido de `cd frontend` y `cd ..`, en Git Bash (10:54:46) | Vuelve a la raíz. **En PowerShell y en `cmd.exe` no se ha probado** |
| Qué documentos decían «no ejecutada» o «solo Windows» | Dos búsquedas en los `.md` versionados, sin `.private/` (10:42:22 y 10:42:50) | La tabla del apartado 3 |
| El ancho de la nota y del «Estado» | La línea más larga desde «Dos sesiones…» hasta el final (10:52:30) | 76 columnas |
| Los enlaces de `ai-workspace/README.md` | `test -e` de sus 31 destinos (10:52:30) | Existen todos, con los dos nuevos: `../README.md` y `../.github/workflows/ci.yml` |
| Que no queden las frases antiguas | Búsqueda de «este mismo directorio», «ese borrador», «no se ha ejecutado nunca» y «Pendiente» en `ai-workspace/README.md` (10:52:30) | Ninguna |
| En el guion no cambia ninguna tabla | `git diff -U0` de `pruebas-manuales.md`, contando las líneas cambiadas que empiezan por «\|» (10:52:30) | Ninguna: cambia una línea de texto |
| **El código, los tests y la CI no han cambiado** | `git diff --stat 3591202 HEAD -- backend frontend scripts .github` (10:54:14) | Vacío. Desde `3591202`, 6 ficheros: esta bitácora, `sesion-12.txt`, el índice, los dos README y `pruebas-manuales.md` |
| Los mensajes de los commits | `git log 3591202..HEAD` (10:54:14) | Cuatro commits, sin trailers de coautoría |

Oráculo:

| Qué | Cómo | Resultado |
|---|---|---|
| **Antes de cada commit** | `uv run scripts/check.py`, sin `--e2e`; la salida, a un fichero fuera del repositorio, y el commit en la misma orden, solo con código 0 | Código 0 en las cuatro pasadas anteriores a este cierre (10:45:39, 10:47:52, 10:50:19 y 10:52:49): 23 correctas, 0 con fallo y 1 inactiva, Playwright |
| Puertos y base local al cerrar | `netstat` y un listado de `backend/data/` (10:54:14) | Ninguno en escucha; 28.672 bytes, 2026-11-14 18:37, como al empezar. La IA no ha arrancado ningún servidor |

## 5. No verificado

Al llegar a la parada 1:

- **Los hechos A, B y C**: son del Tech Lead y la IA no ha comprobado
  ninguno. No ha visto los clones, ni la ejecución de la integración
  continua, ni su salida, ni Chrome con `http://127.0.0.1:4200` o con
  `http://[::1]:4200`. Lo que el README y el «Estado» dicen de ellos es lo
  que dice el encargo. Lo único contrastado es la tabla HE-1 a HE-6.
- **Nada de lo que se dice de la sesión que audita**, como en las sesiones
  11 y 12: tampoco que hiciera la prueba en limpio del 16/11.
- **El README corregido no lo ha seguido nadie.** Los tres bloques de
  «Tests y oráculo» no se han ejecutado tal como están escritos desde un
  clon: la orden sin opciones es la que el oráculo ha pasado cuatro veces,
  desde la raíz; la instalación del navegador y la orden con `--e2e` no se
  han ejecutado en esta sesión. La línea de comentario, solo en Git Bash
  (AL-03).
- **La insignia**: ni que la dirección sea la que GitHub sirve para ese
  workflow, ni cómo se ve, ni qué enseña mientras el repositorio es
  privado (AL-05). La IA no ha consultado la red.
- **La revisión de Python 3.12 y la versión de git de la integración
  continua** (HE-6).
- **Que `sesion-12.txt` sea la conversación entera de la sesión 12 y qué
  se le ha sustituido**: es un fichero nuevo y la IA no tiene con qué
  compararlo. Ha mirado su principio, su final y las búsquedas del
  apartado 4; no lo ha leído entero.
- **Si las conversaciones llevan contenido de los ficheros de
  `.private/`**: sigue como en las sesiones 11 y 12.
- **Las cifras del «Estado»** (741, 569, 18 y 96 tests, 140 requisitos,
  siete evaluaciones, once limitaciones): no se han vuelto a contar, salvo
  los 96 tests de los scripts, que salen en el oráculo (AL-06).
- **Cómo se ven los ficheros una vez publicados**: las anclas, los enlaces
  relativos nuevos y los de los `.txt`.
- **Ningún evaluador ha mirado los cambios de esta sesión**, ni los de las
  sesiones 09 a 12.
- **Sin pasada con `--e2e`**, por el encargo: Playwright sale inactivo en
  las cuatro. Los tests no se han tocado.
- **macOS**, nunca; **Linux a mano con un navegador**, tampoco; y **la
  integración continua sobre los commits de esta sesión**, hasta el
  próximo `push`.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Paso 1: `sesion-12.txt` y el índice al día~~ | Hecho (`bc4ee0d`) |
| ~~Paso 2: el README de la raíz, cuatro cambios~~ | Hecho (`2a33120`) |
| ~~Paso 3: el «Estado», la nota, la cabecera del guion y `04-calidad`~~ | Hecho (`e965ce2`) |
| **Parada 1: el Tech Lead revisa** los tres pasos, HE-1 a HE-6 y las precisiones AL-01 a AL-07. En particular: **si ADR-005 se pone al día** con la ejecución en Linux; **si el ejemplo de SPEC-04, 2.9, se queda** (HE-4); **si la línea de comentario de los bloques vale** como carpeta (AL-03); **si el nombre de usuario de GitHub puede estar en el README** (AL-05); y **si la línea de los commits de la sesión 13 se queda en el «Estado»** (AL-06) | Ahora |
| El `push` de los commits de esta sesión, y ver la integración continua sobre ellos | Del Tech Lead |
| La conversación de la sesión 13 no está publicada: el índice lo dice | A decidir por el Tech Lead |
| La cabecera de `limitaciones-conocidas.md` y la frase de L-06, que hablan de un README y de un frontend que «todavía» no existen | A decidir por el Tech Lead |
| Pendientes heredados que esta sesión no toca: L-07 y los avisos de `npm audit`, los cuatro scripts de instalación sin aprobar, las fechas del fichero de bloqueo en el oráculo y los de la sesión 06 | A decidir por el Tech Lead |
