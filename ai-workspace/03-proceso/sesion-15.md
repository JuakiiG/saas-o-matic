# Sesión 15 · La organización de carpetas, documentada

| | |
|---|---|
| **Fecha** | 2026-11-17 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | **Parada 1 alcanzada (14:05): los tres pasos, hechos, cada uno en su commit y con el oráculo en código 0 antes, sin `--e2e`.** No ha cambiado el código de la aplicación, ningún test, ninguna spec, el fichero de la CI ni nada de `.claude/`: entre `df1740f`, el cierre de la sesión 10, y el último commit no cambia nada en `backend/`, `frontend/`, `scripts/`, `.github/`, `.claude/`, `01-specs/` ni `CLAUDE.md`. **Paso 1** (`0eed79f`): `sesion-14.txt`, idéntica byte a byte a la que dejó el Tech Lead, y el índice al día, con el hecho I. **Paso 2** (`bb3e286`): el apartado «Organización de carpetas» del índice de arquitectura, en lugar de «Pendiente». **Paso 3** (`ea63eb6`): el «Estado» al cerrar la sesión 15, con los hechos G y H. **Lo que el Tech Lead tiene que conocer**: (1) **el apartado tiene 74 líneas y 548 palabras**, 220 de prosa: la IA no ha cronometrado si se lee en un minuto (AN-03); (2) **siete reglas de organización no las vigila nada**, y el apartado las nombra; (3) **las reglas y las carpetas no coinciden en tres líneas**: las vistas, los interceptores y lo que prueba `unit/`; el apartado las cuenta como «dos cosas», una por fichero de reglas; (4) `ai-workspace/README.md` y `requisitos.md` remiten a la carpeta `02-arquitectura/`, no al apartado, y no se han tocado (AN-04); (5) `sesion-14.txt` **no se ha leído entera**, solo se ha buscado en ella (AN-01). Quedan sin aprobar AN-01 a AN-06. · Antes, sesión abierta a las 13:51 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

**La conversación es nueva**, sin el contexto de la sesión 14: la IA llega
con lo que ha leído al empezar (`CLAUDE.md`, `ai-workspace/README.md`, el
índice de `02-arquitectura/`, las dos reglas de `.claude/rules/` y la
bitácora de la sesión 14, con sus pendientes) y con sus cuatro notas de
memoria.

**La segunda sesión de IA, «la que audita»**, sigue sin verse desde esta
conversación: lo que esta bitácora dice de ella es lo que dice el encargo.
La fila de participantes de arriba nombra a quienes hablan en esta
conversación.

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 15: se documenta la organización de carpetas, que el encargo pide
> de forma expresa y hoy está como pendiente. Antes de nada, leer
> `CLAUDE.md`, `ai-workspace/README.md`, `02-arquitectura/README.md`,
> `.claude/rules/backend.md`, `.claude/rules/frontend.md` y los pendientes
> de `03-proceso/sesion-14.md`. Abrir esta bitácora con el mismo formato
> que las anteriores.
>
> Parada 1 de la sesión 14 aprobada. Admitidas AM-01 a AM-06. Decisiones:
>
> - AM-03: la frase de L-06 sobre Playwright y el guion se queda.
> - Las frases caducadas de `requisitos.md`, ADR-001, ADR-003, ADR-005,
>   ADR-006 y L-07 se quedan: son documentos con fecha y dicen lo que se
>   sabía ese día. La lista de la sesión 14 es su registro.
> - La de `02-arquitectura/README.md`, «Pendiente», no se queda: es el
>   paso 2 de esta sesión.
>
> Por qué: el encargo pide mostrar el diseño de la base de datos y la
> organización de carpetas del proyecto (R-15). La base de datos está en
> `02-arquitectura/README.md`. La organización de carpetas está en las
> reglas de `.claude/rules/`, pero el índice de arquitectura no la enseña
> y acaba diciendo que se documentará al crear los proyectos.
>
> En esta sesión no cambia el código de la aplicación, ningún test,
> ninguna spec, el fichero de la CI ni nada de `.claude/`. Un commit por
> paso, con el oráculo en verde por su código de salida, sin `--e2e`. Sin
> `push`.
>
> Hechos nuevos, que son del Tech Lead y que la IA no tiene que comprobar:
> G (el `push` de las sesiones 13 y 14 y la segunda ejecución de la
> integración continua), H (el repositorio es público) e I (qué se
> sustituyó al publicar `sesion-14.txt`). Están enteros en el apartado 3.
>
> **Paso 1. La conversación de la sesión 14.** El Tech Lead ha dejado
> `sesion-14.txt` en `03-proceso/conversaciones/`, sin commit, con las
> mismas reglas que las demás. **No editarla.** Poner al día el índice: la
> tabla gana la sesión 14, la que falta es la 15, y «Qué se ha cambiado al
> publicarlas» recoge el hecho I. Donde `ai-workspace/README.md` diga
> «01 a 13», pasa a «01 a 14».
>
> **Paso 2. La organización de carpetas.** En
> `ai-workspace/02-arquitectura/README.md`, el apartado «Pendiente» se
> sustituye por uno nuevo, «Organización de carpetas», delante de
> «Directrices dadas a la IA». Lo que tiene que tener, y nada más:
>
> - El árbol real de los tres bloques, sacado de `git ls-files` y no de
>   memoria: `backend/` (`app/` con sus capas y `tests/`), `frontend/`
>   (`src/app/` con `core`, `features` y `shared`, y `e2e/`) y `scripts/`.
>   Hasta el nivel de carpeta, con una línea por carpeta que diga qué
>   contiene. Sin listar ficheros, salvo los pocos que sean puntos de
>   entrada.
> - El sentido de las dependencias entre capas del backend y entre
>   carpetas del frontend, en una frase cada uno.
> - Qué lo vigila: para cada regla de organización, la comprobación del
>   oráculo que la hace cumplir, con su nombre literal tal como sale en la
>   salida del oráculo, o que no la vigila nada si es así. Incluye los
>   límites de tamaño de fichero y de función, que son la respuesta a
>   «evitar archivos masivos».
> - Un enlace a las dos reglas de `.claude/rules/`, que es donde se le dio
>   a la IA antes de escribir el código.
> - Si las reglas nombran carpetas o vistas que no coinciden con las que
>   existen hoy, decirlo en una frase del apartado. No cambiar las reglas.
>
> Corto: tiene que leerse en un minuto. En el mismo commit, si
> `ai-workspace/README.md` o `requisitos.md` remiten a la estructura del
> proyecto, comprobar que el enlace o la referencia llevan a este
> apartado; no reescribir nada más.
>
> **Paso 3. El «Estado» de `ai-workspace/README.md`, al cerrar la sesión
> 15**: las sesiones 11 a 15 solo han cambiado documentación (comprobarlo
> con `git diff` y decir la orden); el punto «Después de `3591202`» gana
> los hechos G y H, como hechos con su fecha. La frase de que la
> integración continua se ejecuta en cada `push` y su resultado es el de
> la insignia se queda.
>
> **Parar ahí (parada 1)** y cerrar la bitácora de la sesión 15. Decir qué
> cambió, qué árbol se ha puesto y de dónde sale cada línea, qué regla de
> organización no vigila nadie y en qué no coinciden las reglas con las
> carpetas de hoy. No leer ni citar `.private/`. El `push` lo hace el Tech
> Lead.

## 2. Cronología

Las horas son las del reloj del sistema (`date`), leído justo antes de
escribir cada fila; las de los commits se toman de `git log --format=%ci`
después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 13:52 | — | Mensaje recibido hacia las 13:51 (primera lectura del reloj, 13:51:13). El último commit es `baa1480` (2026-11-17 11:39:12), el cierre de la sesión 14; `git branch -vv` dice que `main` y `origin/main` están en el mismo commit (referencia local, sin consultar la red). **`git status`: solo `sesion-14.txt`, sin versionar**, que es lo que anunciaba el encargo. **`netstat` a las 13:51:28: nada escucha en el 8000 ni en el 4200.** `backend/data/saas-o-matic.db`, del Tech Lead: 28.672 bytes, 2026-11-14 18:37, como al cerrar la sesión 14; la IA no lo toca. Lecturas del encargo hechas, y además el índice de las conversaciones, `scripts/check.py`, `scripts/oracle/checks_purity.py`, `scripts/oracle/checks_code.py` y `frontend/eslint.config.js`. `sesion-14.txt`, mirada **solo con órdenes de lectura y sin leerla entera** (apartado 4). Apertura de esta bitácora |
| 13:54 | `e17b6a5` | **Apertura de la bitácora**, 13:54:22 según `git log`, tras el oráculo sin `--e2e` de 13:52:55 a 13:54:22, código 0 (23 correctas, 1 inactiva); la salida, a un fichero fuera del repositorio, y el commit, en la misma orden, solo con ese código. Solo entra `sesion-15.md`: `sesion-14.txt` sigue sin commit |
| 13:55 | — | **Paso 1, el índice**: `conversaciones/README.md`, con la herramienta de edición, de 69 a 73 líneas (13:54:42). La tabla gana la sesión 14 (1.438 líneas) y dice «de la 01 a la 14»; «Lo que falta» nombra la sesión 15 en lugar de la 14; y «Qué se ha cambiado al publicarlas» gana un punto con el hecho I (AN-01). En `ai-workspace/README.md`, la fila de `03-proceso` de «Cómo leerlo» decía «sesiones 01 a 13» y dice «01 a 14»; era el único sitio. Los 29 destinos de los enlaces del índice existen. `sesion-14.txt` no se ha tocado: misma huella que a las 13:51:29 |
| 13:57 | `0eed79f` | **Paso 1**, 13:56:20 según `git log`: `sesion-14.txt`, el índice y la fila de `ai-workspace/README.md`; tres ficheros, 1.446 líneas añadidas y 4 quitadas. Antes, oráculo sin `--e2e` de 13:54:55 a 13:56:20, código 0 (23 correctas, 1 inactiva). Después (13:56:20): **`sesion-14.txt` tiene en el commit la misma huella que el fichero que dejó el Tech Lead** y el de la carpeta sigue igual; `git ls-files --eol` dice `i/lf w/lf` |
| 14:00 | — | **Paso 2, «Organización de carpetas»** en `02-arquitectura/README.md`, con la herramienta de edición (13:58:33 la primera versión; 13:59:45 la que queda). De dónde sale cada cosa: de 13:56:59 a 13:59:08, `git ls-files backend frontend scripts` agrupado por carpeta, las cabeceras de los ficheros de cada una, `app.routes.ts`, la configuración de Playwright, las importaciones entre `core/`, `shared/` y `features/`, las de los tests de `unit/`, y el código de las comprobaciones (`checks_purity.py`, `checks_code.py`, `checks_stack.py`, `eslint.config.js`). **La primera versión tenía 82 líneas y 646 palabras y la IA la recortó antes de seguir**: el encargo pide que se lea en un minuto (AN-03). Queda en **74 líneas y 548 palabras**, de ellas 35 del árbol. El apartado «Pendiente» desaparece; del resto del fichero no cambia nada (`git diff -U0`: un bloque añadido y uno quitado). Los cinco nombres de comprobación están letra por letra en la salida del oráculo de las 13:56; cada carpeta y cada fichero del árbol existe en `git ls-files`, y no hay ninguna carpeta versionada de los tres bloques que el árbol no nombre; los 17 destinos de los enlaces del fichero existen. **`ai-workspace/README.md` y `requisitos.md` no se tocan en este paso**: los dos remiten a `02-arquitectura/`, la carpeta, cuyo índice es este fichero (AN-04) |
| 14:02 | `bb3e286` | **Paso 2**, 14:01:40 según `git log`: solo `02-arquitectura/README.md`, 74 líneas añadidas y 5 quitadas. Antes, oráculo sin `--e2e` de 14:00:14 a 14:01:40, código 0 (23 correctas, 1 inactiva) |
| 14:03 | — | **Paso 3, el «Estado»** de `ai-workspace/README.md`, con la herramienta de edición, 19 líneas añadidas y 6 quitadas (14:02:26 y 14:02:37). (1) Dice «al cerrar la sesión 15 (las sesiones 11 a 15 solo han cambiado documentación)». (2) En el punto «Después de `3591202`»: los commits posteriores son los de las sesiones 13, 14 y 15; **gana los hechos G y H**, cada uno con su fecha, detrás de los de `c06630c`; y la frase de que los commits no tocan el README de la raíz nombra las sesiones 14 y 15 (AN-05). (3) La frase de que la integración continua se ejecuta en cada `push` y su resultado es el de la insignia se queda, palabra por palabra. **La comprobación del encargo**: `git diff --stat df1740f -- backend frontend scripts .github .claude ai-workspace/01-specs CLAUDE.md`, vacío (`df1740f` es el cierre de la sesión 10), y `git diff --name-only df1740f`, 25 ficheros: el `README.md` de la raíz y 24 de `ai-workspace/`. Lo mismo desde `3591202`: vacío, y 13 ficheros (14:02:26, sobre el árbol de trabajo, con este paso ya escrito). Los 31 destinos de los enlaces del fichero existen; su línea más larga desde «Estado» tiene 75 columnas, después de recolocar un párrafo que había quedado en 81 |
| 14:05 | `ea63eb6` | **Paso 3**, 14:04:18 según `git log`: solo `ai-workspace/README.md`, 19 líneas añadidas y 6 quitadas. Antes, oráculo sin `--e2e` de 14:02:52 a 14:04:18, código 0 (23 correctas, 1 inactiva). Después (14:04:18): entre `df1740f` y este commit cambian 25 ficheros, y entre `3591202` y este commit, 13, **ninguno en `backend/`, `frontend/`, `scripts/`, `.github/`, `.claude/` ni `01-specs/`**; nada escucha en el 8000 ni en el 4200; `backend/data/saas-o-matic.db`, igual. `main` va cuatro commits por delante de `origin/main` (referencia local). La IA no ha arrancado ningún servidor ni ha hecho `push` |
| 14:05 | *(este commit)* | **Cierre de esta bitácora para la parada 1.** Las filas anteriores se han escrito cada una en su momento, con el reloj leído justo antes, y con el fichero sin commit entre la apertura y este cierre: los commits de los pasos llevan solo los ficheros de su paso. Antes de cerrar, medida del apartado (14:04:57). La IA para aquí: el Tech Lead revisa los tres pasos, el apartado y las precisiones AN-01 a AN-06. El `push` es suyo. La hora de este commit se ve con `git log` |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (13:51)

**Parada 1 de la sesión 14, aprobada. Admitidas AM-01 a AM-06.** Sobre lo
que quedó pendiente:

| Qué | Decisión del Tech Lead |
|---|---|
| AM-03 · la frase de L-06 sobre Playwright y el guion | **Se queda** |
| Las frases caducadas de `requisitos.md`, ADR-001, ADR-003, ADR-005, ADR-006 y L-07 | **Se quedan**: son documentos con fecha y dicen lo que se sabía ese día. La tabla de la bitácora de la sesión 14 es su registro |
| La de `02-arquitectura/README.md`, «Pendiente» | **No se queda**: es el paso 2 de esta sesión |

La bitácora de la sesión 14 no se toca: la aprobación queda anotada aquí.

**Reglas de esta sesión**, del encargo:

- **No cambia el código de la aplicación, ningún test, ninguna spec, el
  fichero de la CI ni nada de `.claude/`.**
- **Un commit por paso**, con el oráculo en verde por su código de salida,
  **sin `--e2e`**.
- **`sesion-14.txt` no se edita**: entra tal como la dejó el Tech Lead.
- **Las reglas de `.claude/rules/` no se cambian**, aunque no coincidan
  con las carpetas de hoy: se dice en el apartado nuevo.
- **La IA no hace `push`.**
- **`.private/` no se lee ni se cita.**

### Hechos nuevos del encargo

**Son del Tech Lead. La IA no los ha comprobado**, porque el encargo dice
que no tiene que hacerlo y porque no se pueden ver desde aquí: ni GitHub,
ni la otra sesión, ni los originales de las conversaciones.

**G.** El 17/11 a las 12:48 el Tech Lead hizo `push` de los diez commits de
las sesiones 13 y 14. La integración continua se lanzó sola sobre
`baa1480`, su segunda ejecución: los dos trabajos en verde, y en los dos
«ORÁCULO EN VERDE · 24 correctas, 0 con fallo, 0 inactivas» (Linux en tres
minutos y medio, Windows en algo menos de seis). Antes, de 12:34 a 12:36,
la sesión que audita había ejecutado el oráculo con `--e2e` sobre
`baa1480`: 24 correctas, 0 con fallo, 0 inactivas.

**H.** El repositorio es público desde el 17/11/2026. Comprobado sin
iniciar sesión: la página carga y la insignia dice «passing».

**I.** En `sesion-14.txt` no hubo nada que sustituir al publicarla: el
original no llevaba rutas de usuario, correos ni el nombre de usuario de
GitHub del Tech Lead. Solo los finales de línea y los espacios finales.

### Los hechos G, H e I frente a lo que la IA ve en el repositorio

El encargo no lo pide. Se anota lo que se ha podido contrastar, mirado
entre las 13:51 y las 13:52, antes de tocar nada. **Nada los contradice.**

| Hecho | Qué dice el repositorio |
|---|---|
| G: el `push` de los diez commits de las sesiones 13 y 14 | `git rev-list --count 3591202..baa1480` da 10. Al empezar, `git branch -vv` no enseña ningún commit de `main` por delante de `origin/main`, que es lo que deja un `push`; es la referencia local y la IA no ha consultado la red |
| G: las dos pasadas, sobre `baa1480` | Es el cierre de la sesión 14 (11:39:12), anterior a las 12:34. 24 correctas y 0 inactivas es la cuenta de una pasada con `--e2e` |
| H: el repositorio es público y la insignia dice «passing» | No se puede ver desde aquí |
| I: en la 14 no hay rutas de usuario, correos ni el nombre de usuario de GitHub | Es lo que dan las búsquedas en `sesion-14.txt` (apartado 4): ninguna aparición de los tres. Que el original tampoco los llevara solo lo sabe el Tech Lead |

### Los tres pasos · lo hecho

| # | Commit | Qué toca |
|---|---|---|
| 1 · La conversación de la sesión 14 | `0eed79f` | `sesion-14.txt`, tal como la dejó el Tech Lead; `conversaciones/README.md` (la tabla, «Lo que falta» y un punto nuevo en «Qué se ha cambiado al publicarlas»); y una fila de `ai-workspace/README.md` («01 a 14») |
| 2 · La organización de carpetas | `bb3e286` | `02-arquitectura/README.md`: el apartado nuevo, delante de «Directrices dadas a la IA», y el apartado «Pendiente», que desaparece |
| 3 · El «Estado» | `ea63eb6` | `ai-workspace/README.md`: la primera línea del «Estado» y el punto «Después de `3591202`» |

Ningún test nuevo ni cambiado: no hay rojo ni mutación que anotar.

### El árbol del apartado y de dónde sale cada línea

Todas las carpetas y los cinco ficheros salen de
`git ls-files backend frontend scripts` (13:51:28 y 13:56:59); la cifra
es la de ficheros versionados dentro, contando subcarpetas. **La
descripción** sale de lo que dice la columna de la derecha. Donde dice
«nombres», la IA no ha abierto los ficheros.

| Línea del árbol | Ficheros | De dónde sale la descripción |
|---|---|---|
| `backend/` · API REST: FastAPI y SQLite | 64 | `CLAUDE.md`, «Arquitectura» |
| `app/` · la aplicación | 32 | — |
| `main.py` · monta la aplicación FastAPI | 1 | Su docstring: «Composition root: builds the FastAPI application» |
| `config.py` · variables de entorno | 1 | Su docstring |
| `api/` · routers, esquemas Pydantic y errores HTTP | 13 | La regla de `backend.md` y los nombres: cinco routers (`customers`, `pricing`, `simulations`, `health`, `meta`) y lo demás, contrato, validación y errores |
| `services/` · casos de uso | 5 | La regla y los nombres |
| `domain/` · reglas de negocio, funciones puras | 6 | La regla y los nombres (`countries`, `customers`, `pricing`, `simulations`, `tax_id`) |
| `repositories/` · acceso a SQLite y su esquema | 5 | Los nombres: `customers`, `simulations`, `database` y `schema.sql` |
| `tests/` · pytest, y las tablas de casos compartidas | 29 | En su raíz, `customer_cases.py` y `simulation_cases.py`: sus docstrings |
| `unit/` · el dominio y los errores del alta | 6 | Lo que importan sus cinco ficheros de test: `app.domain.*` y, uno, `app.api.customer_errors` y `app.api.problems` |
| `integration/` · la API y los repositorios, con una base temporal | 20 | Los nombres de sus 18 ficheros de test y la regla, que es la que dice lo de la base temporal |
| `frontend/` · SPA Angular | 104 | `CLAUDE.md`, «Arquitectura» |
| `src/` · la aplicación | 78 | — |
| `main.ts` · punto de entrada | 1 | Leído: `bootstrapApplication(App, appConfig)` |
| `app/` · componente raíz y rutas | 69 | En su raíz, `app.ts`, `app.html`, `app.css`, `app.config.ts`, `app.routes.ts` y tres `.spec.ts`. `app.routes.ts`, leído |
| `core/` · servicios de la API, modelos y formatos | 20 | El primer comentario de sus doce ficheros que no son tests |
| `features/` · una carpeta por vista | 25 | Las cinco carpetas: `panel/` (4), `alta/` (5), `detalle/` (4), `simulador/` (11) y `not-found/` (1), y las cinco rutas de `app.routes.ts`, una por carpeta |
| `shared/` · componentes y pipes de presentación | 16 | La regla de `frontend.md` y los nombres |
| `environments/` · las URL | 2 | `environment.ts`, leído: `apiBaseUrl` y `ratesUrl` |
| `styles/` · estilos globales | 4 | La cabecera de `src/styles.css`, que los importa |
| `e2e/` · pruebas de principio a fin (Playwright) | 12 | `testDir: './e2e'` en `playwright.config.ts`; cinco `.spec.ts` en su raíz |
| `support/` · utilidades de esas pruebas | 6 | Las primeras líneas de sus seis ficheros |
| `capturas/` · genera las capturas | 1 | `playwright.capturas.config.ts` y la regla de `frontend.md` |
| `scripts/` · herramientas del repo | 31 | `CLAUDE.md`, «Arquitectura» |
| `check.py` y `traceability.py` | 1 y 1 | Sus docstrings |
| `oracle/`, `tracematrix/`, `hooks/` y `tests/` | 11, 3, 2 y 13 | Los docstrings de sus módulos; el hook está registrado en `.claude/settings.json` |

**Las cinco carpetas de vista no tienen una línea cada una**: van en la
línea de `features/`. Y el árbol nombra `environments/` y `styles/`, que
el encargo no citaba: son carpetas versionadas de `frontend/src/`.

### Qué vigila cada regla, y qué regla no vigila nadie

Los cinco nombres se han copiado de la salida del oráculo de las 13:56 y
se han buscado, letra por letra, en ella y en el apartado (13:59:45).

| Regla | Qué la hace cumplir | Cómo lo sabe la IA |
|---|---|---|
| Sentido de las capas y `sqlite3` solo en `repositories/` | «Dirección de las capas y `sqlite3` solo en repositories/» | `checks_purity.py`, `ALLOWED_LAYERS` y `check_layers`, leído |
| `domain/` no importa nada externo | «domain/ solo importa la biblioteca estándar y no usa float ni la división `/`» | `check_domain_purity`, leído |
| `core/` y `shared/` no importan de `features/`; una vista, de otra, tampoco | «ESLint, con los límites de tamaño», que es `npm run lint` | Las dos reglas `no-restricted-imports` de `frontend/eslint.config.js`, leído |
| 250 líneas por fichero y 120 por plantilla | «Ficheros de código de 250 líneas como máximo y plantillas de 120» | `check_file_sizes`, leído. Hoy el fichero mayor que no es test tiene 234 líneas y la plantilla mayor, 111 (13:57:15) |
| 40 líneas y 5 parámetros por función | «Funciones de Python de 40 líneas y 5 parámetros como máximo» y, en TypeScript, «ESLint, con los límites de tamaño» | `check_functions` y las reglas `max-lines-per-function` y `max-params`, leídos |

**Lo que no vigila nada**, que es lo que dice el apartado:

| Regla | Por qué la IA dice que no se vigila |
|---|---|
| En qué carpeta va cada test (`unit/` o `integration/`; el `.spec.ts`, junto a su fichero) | Ninguna comprobación de `scripts/oracle/` nombra esas carpetas (13:57) |
| `domain/` no hace entrada/salida ni lee el reloj | `_is_pure_import` admite cualquier módulo de la biblioteca estándar, también `datetime`, `os` o `pathlib` |
| Routers finos, y el texto del SQL solo en `repositories/` | No hay comprobación. La de capas mira la importación de `sqlite3`, no las cadenas |
| `main.py` y `config.py` | `check_layers` se salta lo que no está dentro de una de las cuatro capas, también para `sqlite3` |
| `HttpClient` solo en `core/` | Nada en `eslint.config.js`. Hoy se cumple: solo lo usan `core/backend-api.ts` y `core/exchange-rates.ts` |
| Las rutas, diferidas | Nada en `eslint.config.js`. Hoy se cumple: las cinco rutas usan `loadComponent`. `app.routes.spec.ts` no nombra `loadComponent` |
| El tamaño de los ficheros de test y de cada test | `_is_test` los deja fuera de las 250 líneas, y ESLint quita el límite de función a los `.spec.ts`. Es lo que ya dice `CLAUDE.md` |

**Dos cosas más que la IA ha visto y que el apartado no dice** (AN-03):

- **Entre `core/` y `shared/` no hay regla.** Hoy seis ficheros de
  `shared/` importan de `core/` y ninguno de `core/` importa de
  `shared/`. Ni `frontend.md` lo fija ni ESLint lo mira.
- **La regla de ESLint sobre las vistas solo mira los ficheros que están
  directamente en la carpeta de una vista** (`src/app/features/*/*.ts`).
  Hoy todas las carpetas son planas (decisión P-08); una subcarpeta
  quedaría fuera.

### En qué no coinciden las reglas con las carpetas de hoy

Las reglas no se han tocado. En el apartado va en una frase, que dice
«dos cosas» porque cuenta una por fichero de reglas; las líneas son tres:

| Regla | Qué dice | Qué hay hoy |
|---|---|---|
| `frontend.md`, «Estructura» | `features/`: «una carpeta por vista (búsqueda, cliente, simulador)» | Cinco carpetas: `panel/` (la búsqueda), `detalle/` (el cliente), `simulador/`, `alta/` y `not-found/` |
| `frontend.md`, «Estructura» | `core/`: «servicios de API, modelos de la API, interceptores» | Ningún interceptor. `app.config.ts` dice en un comentario por qué: una cabecera añadida por uno haría que el backend rechazara la comprobación previa de CORS |
| `backend.md`, «Capas y dependencias» | `unit/`: «dominio y servicios, sin red ni disco» | Los cinco ficheros de `unit/` importan de `app.domain` y, uno, de `app.api`. Ninguno importa de `app.services` |

Las tres líneas estaban ya así en el primer commit de las reglas
(`2604c72`, 2026-11-12 12:37), anterior al primer commit con código del
backend (`bcabea2`, 2026-11-13) y del frontend (`0e9966e`, 2026-11-14): de
ahí sale «la IA recibió esta estructura antes de escribir el código».

**Fuera del apartado, porque no es una carpeta ni una vista**:
`backend.md`, «Calidad», dice que las comprobaciones de cobertura «están
inactivas hasta que exista `backend/pyproject.toml`». Existe, y las tres
salen en verde en el oráculo. Es de `.claude/`, que esta sesión no toca.

### Precisiones de la IA, **sin aprobar**

| # | Precisión | Motivo |
|---|---|---|
| AN-01 | **Tres cosas del paso 1.** (1) **`sesion-14.txt` no se ha leído entera**, a diferencia de la 13 en la sesión 14: se ha medido y se ha buscado en ella lo que no debe publicarse (apartado 4), sin encontrar nada. (2) «Lo que falta» dice de la sesión 15 lo mismo que decía de la 14. (3) El punto nuevo de «Qué se ha cambiado al publicarlas» dice el hecho I entero | (1) El encargo de la sesión 14 pedía mirar si había algo más que no debiera publicarse; este no, y dice que no hubo nada que sustituir. Se declara para que no se lea como una lectura que no se hizo |
| AN-02 | **La sesión tiene cinco commits**: el de apertura de la bitácora, los tres pasos y el cierre | Es lo admitido en AM-01 |
| AN-03 | **El apartado.** (1) **Longitud**: 74 líneas y 548 palabras, de ellas 31 líneas de árbol, una tabla de cinco filas y 220 palabras de prosa. La primera versión tenía 646 y se recortó: salieron la mención de `core/` y `shared/`, una fila de la tabla (las dos de funciones van juntas) y varias descripciones. **La IA no ha cronometrado la lectura.** (2) Los ficheros que nombra son siete: los cinco puntos de entrada del árbol y, entre paréntesis, `app.routes.ts` y `schema.sql`. (3) Una frase que el encargo no pedía: que los tests unitarios del frontend van junto al fichero que prueban. (4) «ESLint, con los límites de tamaño» lleva detrás `no-restricted-imports`, entre paréntesis | (1) El encargo pide que se lea en un minuto y «nada más». (3) Sin ella, el árbol se lee como que el frontend no tiene tests unitarios. (4) Ese nombre no dice que vigile las importaciones: es el de toda la pasada de `npm run lint`. Si algo sobra, se quita |
| AN-04 | **`ai-workspace/README.md` y `requisitos.md` no se han tocado en el paso 2.** El primero, en «Cómo leerlo», enlaza la carpeta `02-arquitectura/` y dice que contiene la «estructura del proyecto»; el segundo, en la fila de R-15, nombra `02-arquitectura/`, `CLAUDE.md` y `.claude/`, sin enlace. **Los dos llevan a la carpeta, cuyo índice es el fichero del apartado; ninguno lleva al apartado mismo** | El encargo pide comprobarlo y no reescribir nada más. La referencia ya no lleva a un «Pendiente». Si el Tech Lead quiere un enlace al apartado, es una línea en cada fichero |
| AN-05 | **Tres cosas del «Estado».** (1) El hecho G va como un segundo bloque, «Sobre `baa1480`», con dos puntos, y el H, como una frase detrás. (2) **Cambia una frase que el encargo no nombraba**: «Los commits de la sesión 14, posteriores a `c06630c`» pasa a «de las sesiones 14 y 15». (3) **No se han tocado**: el punto «Integración continua», que dice que el primer `push` fue «a un repositorio privado», y las cifras, que siguen sin contarse de nuevo | (2) Sin el cambio, la frase dejaría fuera los commits de esta sesión, que tampoco tocan el README de la raíz (`git diff --name-only c06630c`). (3) Lo del repositorio privado era verdad ese día y lleva su fecha |
| AN-06 | **Errores de la IA en esta sesión**, ninguno llegó a un texto versionado salvo el (4). (1) **Una medida falsa de `sesion-14.txt`**: la primera dio 1.438 líneas con retorno de carro y 33 con espacios finales (13:51:29), por dos patrones de `grep` mal escritos; repetida con `tr` y `perl` (13:51:46), 0 y 0. (2) **Dos búsquedas que dieron «sin resultados» en falso**, las de las referencias a la estructura, con la herramienta de búsqueda y un patrón de ficheros mal escrito; repetidas con `grep` (13:51:47). (3) El guion que contrasta el árbol con `git ls-files` no admitía cifras en los nombres y dio por ausente `e2e/` (13:58:33); corregido en la segunda pasada. (4) **La fila de las 14:00 dice «35 del árbol»**: son 31 líneas, 33 con las dos que abren y cierran el bloque. No se ha retocado. (5) Un párrafo del «Estado» quedó en 81 columnas y se recolocó antes del commit | (1) y (2) Se anotan porque la comprobación que vale es la segunda: es el mismo error de AM-06 |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short`, `git log -12` y `git branch -vv` (13:51:13 y 13:51:28) | `baa1480`; solo `sesion-14.txt`, sin versionar; `main` y `origin/main`, en el mismo commit |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000 y 4200 (13:51:28) | Ninguno en escucha |
| La base local del Tech Lead | Listado de `backend/data/` (13:51:28) | 28.672 bytes, 2026-11-14 18:37 |

`sesion-14.txt`, **solo con órdenes de lectura**:

| Qué | Cómo | Resultado |
|---|---|---|
| Forma | `wc`, bytes de retorno de carro (`tr`), líneas con espacios finales (`perl`), último byte y «❯» (13:51:29 y 13:51:46) | 1.438 líneas y 82.743 bytes; ningún retorno de carro ni espacio final; acaba en salto de línea. «❯»: 2, las dos al principio de línea (el `/clear` y el encargo de la sesión 14) |
| Lo que no debe publicarse | Búsquedas de rutas de usuario (`Users`, `AppData`, `/home/`), de cualquier email, de `noreply`, de `<usuario>`, del nombre del Tech Lead, del nombre de usuario de GitHub (el de `git remote get-url origin`), de palabras de secretos, de direcciones IP y de URL (13:52:06) | **Nada.** Ninguna ruta de usuario, ningún email, ningún secreto; ni el nombre del Tech Lead ni su nombre de usuario de GitHub. `noreply` y `<usuario>`, una vez cada uno: son dos líneas del índice, citadas. La única IP es `127.0.0.1`, y la única URL, `http://127.0.0.1:4200`. `.private/`, dos veces |
| La cabecera, el principio y el final | Las tres primeras líneas, las dos líneas con «❯» y las doce últimas (13:51:29 y 13:52:06) | La versión de la herramienta (v2.1.326), «Fable 5.2 · Claude Max» y `Z:\saas-o-matic`, como las trece ya publicadas. Acaba con la respuesta de la parada 1 de la sesión 14 y un comentario «buddy» |
| **No leída entera** | — | AN-01 |
| Huella antes del commit | `sha256sum`, guardada fuera del repositorio (13:51:29) | Para compararla con lo que quede en el commit del paso 1 |

Paso 1:

| Qué | Cómo | Resultado |
|---|---|---|
| Que no quede ningún «01 a 13» | Búsqueda en los dos README y en el índice (13:54:42) | Ninguno |
| Los enlaces del índice | `test -e` de sus 29 destinos (13:54:42) | Existen todos |
| El ancho del índice | La línea más larga fuera de las tablas (13:54:42) | 76 columnas |
| **`sesion-14.txt` entra en el commit sin cambiar** | SHA-256 del fichero antes de tocar nada (13:51:29), antes del commit (13:54:42), tal como queda en `0eed79f` (`git show`) y en la carpeta después (13:56:20) | Las cuatro, idénticas |
| Finales de línea de lo versionado | `git ls-files --eol` del fichero (13:56:20) | `i/lf w/lf` |

Paso 2:

| Qué | Cómo | Resultado |
|---|---|---|
| Las carpetas de los tres bloques | `git ls-files backend frontend scripts`, agrupado por carpeta (13:51:28) y listado entero (13:56:59) | 29 carpetas con ficheros. La tabla del apartado 3 |
| **El árbol frente a git** | Un guion saca cada ruta del bloque del apartado y cuenta sus ficheros con `git ls-files`; y al revés, cada carpeta versionada se busca en el árbol (13:59:45) | Las 30 rutas del árbol existen (la línea 31 es la continuación de `features/`). De las 29 carpetas versionadas, las únicas que no tienen línea propia son las de las cinco vistas, que el árbol nombra en la línea de `features/`; el guion dio cuatro, porque tomó esa continuación, que empieza por `simulador/`, por una ruta |
| Los nombres de las comprobaciones | Búsqueda literal de los cinco en la salida del oráculo de las 13:56 y en el apartado (13:59:45) | Cada uno, una vez en la salida; en el apartado, una vez, y el de ESLint, dos |
| Qué mira cada comprobación | Lectura de `scripts/check.py`, `checks_purity.py`, `checks_code.py` y `frontend/eslint.config.js`, y de los nombres de `checks_stack.py` (13:52 a 13:57) | Las dos tablas del apartado 3 |
| Las importaciones entre carpetas del frontend | Búsqueda de `shared/` en `core/`, de `core/` en `shared/`, de `HttpClient` y de «interceptor» en `frontend/src` (13:56:59) | `core/` no importa de `shared/`; seis ficheros de `shared/` importan de `core/`; `HttpClient`, en dos servicios de `core/`; ningún interceptor |
| Qué importan los tests de `unit/` | Búsqueda de `from app` en `backend/tests/unit/` (13:56:59) | `app.domain.*`, `app.api.customer_errors` y `app.api.problems` |
| Las reglas, antes que el código | `git log --diff-filter=A` de las dos reglas, de `backend/app` y de `frontend/src`, y `git show 2604c72:` de las dos reglas (13:59:08 y 13:59:45) | `2604c72` (12/11), `bcabea2` (13/11) y `0e9966e` (14/11). Las tres líneas que no coinciden estaban ya en `2604c72` |
| En el fichero solo cambia eso | `git diff -U0` (13:59:45) | Dos bloques: 74 líneas añadidas detrás de «Modelo de datos» y las 5 de «Pendiente», quitadas |
| Los enlaces y el ancho | `test -e` de los 17 destinos y la línea más larga del apartado fuera de la tabla (13:59:45 y 14:00:00) | Existen todos; 74 columnas |
| Las referencias a la estructura | `grep` de «estructura», «carpetas», «organizaci» y «R-15» en los dos README, `00-analisis/`, el índice de specs y `trazabilidad.md` (13:51:47) | Dos: la fila de `02-arquitectura/` de `ai-workspace/README.md` y la fila de R-15 de `requisitos.md` (AN-04). En el `README.md` de la raíz, ninguna |
| Medida del apartado | Líneas, palabras, líneas del árbol y palabras fuera del árbol y de la tabla (13:59:45 y 14:04:57) | 74, 548, 31 y 220 |

Paso 3:

| Qué | Cómo | Resultado |
|---|---|---|
| **Las sesiones 11 a 15 solo cambian documentación** | `git diff --stat df1740f -- backend frontend scripts .github .claude ai-workspace/01-specs CLAUDE.md` y `git diff --name-only df1740f`, sobre el árbol de trabajo con el paso 3 escrito (14:02:26); y las dos, con `HEAD`, con el commit hecho (14:04:18). `df1740f` es el cierre de la sesión 10 | El `--stat`, vacío las dos veces. Cambian 25 ficheros: el `README.md` de la raíz, `ai-workspace/README.md`, dos de `02-arquitectura/`, las cinco bitácoras de las sesiones 11 a 15, catorce de `conversaciones/` y dos de `04-calidad/` |
| Los commits posteriores a `3591202` | Las mismas dos órdenes con `3591202` (14:02:26 y 14:04:18) | El `--stat`, vacío. 13 ficheros, todos `.md` o `.txt` |
| Los commits de las sesiones 14 y 15 no tocan el README de la raíz | `git diff --name-only c06630c` (14:02:26) | No está |
| Los diez commits del hecho G | `git rev-list --count 3591202..baa1480` (14:02:10) | 10 |
| Que no queden las frases antiguas | Búsqueda de «sesión 14 (» y «11 a 14» en `ai-workspace/README.md` (14:02:26) | Ninguna |
| Los enlaces de `ai-workspace/README.md` | `test -e` de sus 31 destinos (14:02:26) | Existen todos. El paso 3 no añade ni quita ninguno |
| Los mensajes de los commits | `git log baa1480..HEAD`, buscando trailers de coautoría o firmas de herramientas (14:04:18) | Ninguno |

Oráculo:

| Qué | Cómo | Resultado |
|---|---|---|
| **Antes de cada commit** | `uv run scripts/check.py`, sin `--e2e`; la salida, a un fichero fuera del repositorio, y el commit en la misma orden, solo con código 0 | Código 0 en las cuatro pasadas anteriores a este cierre (13:52:55, 13:54:55, 14:00:14 y 14:02:52): 23 correctas, 0 con fallo y 1 inactiva, Playwright |
| Puertos y base local al cerrar | `netstat` y un listado de `backend/data/` (14:04:18) | Ninguno en escucha; 28.672 bytes, 2026-11-14 18:37, como al empezar. La IA no ha arrancado ningún servidor |

## 5. No verificado

Al llegar a la parada 1:

- **Los hechos G, H e I**: son del Tech Lead y la IA no ha comprobado
  ninguno. No ha visto GitHub, ni la integración continua, ni la insignia,
  ni la otra sesión, ni el original de la conversación. Lo que el «Estado»
  y el índice dicen de ellos es lo que dice el encargo.
- **`sesion-14.txt`, entera**: no se ha leído. Se ha buscado en ella y se
  han mirado su principio y su final (AN-01).
- **Que cada comprobación falle cuando se rompe su regla**: la IA ha
  leído el código de las comprobaciones, no ha roto ninguna regla para
  verlas fallar. Tampoco ha roto ninguna de las siete que dice que nadie
  vigila para ver que el oráculo sigue en verde: habría sido tocar el
  código, que esta sesión no toca.
- **Las descripciones de `api/`, `services/`, `domain/`,
  `repositories/`, `integration/` y `shared/`**: salen de la regla y de
  los nombres de los ficheros, no de leerlos. Que `integration/` use una
  base temporal y que `unit/` no toque red ni disco lo dice la regla.
- **Que ningún test compruebe de otra forma lo que la IA da por no
  vigilado**: se ha mirado el oráculo, ESLint y `app.routes.spec.ts` por
  una palabra, no los 19 ficheros de test del frontend ni los 23 del
  backend.
- **Que el apartado se lea en un minuto**: no se ha cronometrado.
- **Los commits de esta sesión no los ha ejecutado nadie más que el
  oráculo de esta sesión, sin `--e2e`**: Playwright sale inactivo en las
  cinco pasadas. Solo cambian documentación. La integración continua no
  ha pasado sobre ellos: no están subidos.
- **Las cifras del «Estado»** (741, 569, 18 y 96 tests, 140 requisitos,
  siete evaluaciones, once limitaciones): no se han vuelto a contar. La de
  96 tests de los scripts sí sale en la salida del oráculo de hoy.
- **Si las conversaciones llevan contenido de los ficheros de
  `.private/`**: sigue como en las sesiones 11 a 14.
- **Cómo se ve el apartado una vez publicado**: el árbol, dentro de un
  bloque de código, y la tabla con comillas angulares y acentos graves.
- **Ningún evaluador ha mirado los cambios de esta sesión**, ni los de las
  sesiones 09 a 14.
- **macOS**, nunca; **Linux a mano con un navegador**, tampoco.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Paso 1: `sesion-14.txt` y el índice al día~~ | Hecho (`0eed79f`) |
| ~~Paso 2: «Organización de carpetas» en `02-arquitectura/README.md`~~ | Hecho (`bb3e286`) |
| ~~Paso 3: el «Estado» de `ai-workspace/README.md`~~ | Hecho (`ea63eb6`) |
| **Parada 1: el Tech Lead revisa** los tres pasos y las precisiones AN-01 a AN-06. En particular: **si el apartado es lo bastante corto** y si le sobra o le falta algo (AN-03: la frase de los `.spec.ts`, `environments/` y `styles/`, y lo que no dice de `core/` y `shared/`); **si las referencias de `ai-workspace/README.md` y de `requisitos.md` valen como están** (AN-04); y **qué se hace con las tres líneas de las reglas que no coinciden** con las carpetas de hoy, y con la frase de `backend.md` sobre `pyproject.toml` | Ahora |
| El `push` de los cinco commits de la sesión 15, y ver la integración continua sobre ellos | Del Tech Lead |
| La conversación de la sesión 15 no está publicada: el índice lo dice | A decidir por el Tech Lead |
| Pendientes heredados que esta sesión no toca: L-07 y los avisos de `npm audit`, los cuatro scripts de instalación sin aprobar, las fechas del fichero de bloqueo en el oráculo y los de la sesión 06 | A decidir por el Tech Lead |
