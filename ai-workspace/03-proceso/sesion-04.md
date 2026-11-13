# Sesión 04 · Decisión de A2 a A5, aprobación del bloque backend y esqueleto del backend

| | |
|---|---|
| **Fecha** | 2026-11-13 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | A2 a A5 decididos por el Tech Lead sin confirmación externa y bloque backend aprobado (SPEC-01, SPEC-02 y SPEC-03); SPEC-04 sigue en `borrador`. Esqueleto del backend con uv, revisado y aprobado: `httpx2` en lugar de `httpx`, avisos como errores y margen de una semana en las versiones (ADR-007). El oráculo usa `uv run --locked` y mide el 90 % sobre las ramas. **Paso 1 del backend completo**: errores genéricos, CORS, `GET /health` y esquema, con 64 tests. Oráculo en verde con 20 comprobaciones activas y 4 inactivas. Sesión parada a la espera de la revisión del paso 1, antes de SPEC-02. **Añadido a las 12:34**: llegó la respuesta a la consulta de A2 a A5 (registrada sin cambiar ninguna regla; ADR-008 propuesto); el paso 1 se aprobó con cinco correcciones, hechas una por commit (p1 a p5); y **SPEC-02 está implementada** en tres piezas: dominio, traducción de los errores de validación y `POST /pricing/quote`. 160 tests del backend, `domain/` al 100 %, oráculo en verde con 20 comprobaciones activas y 4 inactivas. Quedan 34 precisiones de la IA sin aprobar (P-01 a P-08 y W-01 a W-26; la más importante, W-14). Sesión parada a la espera de la revisión de SPEC-02, antes de SPEC-01 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Leer `CLAUDE.md`, `ai-workspace/README.md`, `00-analisis/supuestos.md`,
> `01-specs/README.md` y la bitácora de la sesión 03. Abrir ya esta bitácora
> y anotar cada revisión en el momento.
>
> 1. Fecha límite cumplida sin respuesta externa. El Tech Lead decide A2,
>    A3, A4 y A5 con la hipótesis ya documentada en cada uno; pasan a
>    `decidido (sin confirmación externa)` con fecha de hoy. Actualizar
>    `supuestos.md`, las cabeceras y «Pendiente antes de aprobar» de las
>    specs y el índice. La consulta sigue abierta: si llega la respuesta, se
>    aplica como cambio de spec con fecha y motivo en su historial. Anotarlo
>    así en `supuestos.md` y aquí, sin nombres.
> 2. Aprobado el bloque backend: SPEC-01, SPEC-02 y SPEC-03 pasan a
>    `aprobada (2026-11-13)`, en las cabeceras y en el índice. El hook pedirá
>    confirmación y el Tech Lead la dará. SPEC-04 sigue en borrador hasta
>    antes del frontend.
> 3. Ejecutar el oráculo, enseñar la salida y hacer el commit
>    «docs(specs): decisión de A2 a A5 y aprobación del bloque backend».
> 4. Primera tarea de código, paso 1 del orden (lo común), empezando solo
>    por el esqueleto: proyecto backend con uv (Python 3.12), dependencias
>    con versión exacta fijada en `uv.lock` (FastAPI, Pydantic v2, uvicorn;
>    de desarrollo pytest, pytest-cov, ruff, mypy, httpx y python-stdnum),
>    estructura `api/services/domain/repositories`, configuración de ruff,
>    `mypy --strict` y cobertura según `backend.md`, y un único test de humo.
>    Comprobar que el oráculo activa el bloque backend y queda en verde.
>    Commit y **parar**: el Tech Lead quiere revisar versiones y estructura
>    antes de seguir con errores, CORS, `/health` y el esquema.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 10:26 | — | Lectura de los cinco documentos indicados, de `.claude/rules/backend.md`, de las cabeceras y los apartados finales de las cuatro specs, de ADR-001 y ADR-005 y de los módulos del oráculo y del hook. `git status` limpio, `HEAD` en `bd930dc`. El reloj marca las 10:26 del 2026-11-13: la fecha límite (10:00) ha pasado |
| 10:31 | — | Apertura de esta bitácora, con las decisiones de los puntos 1 y 2 del encargo (apartado 3) |
| 10:36 | — | Punto 1: `supuestos.md`, la fila «Supuestos» y el apartado «Pendiente antes de aprobar» de las cuatro specs, las tres menciones a A3 y A4 dentro de SPEC-02 y el párrafo de la fecha límite del índice |
| 10:40 | — | Punto 2: estado `aprobada` (2026-11-13) en las cabeceras de SPEC-01, SPEC-02 y SPEC-03 y en sus tres filas del índice; filas «Depende de» y «Bloqueos para aprobarla» de las cuatro specs; historial de las cuatro; tabla de bloques del índice. Las ediciones se aplicaron (ver «Hook», apartado 3) |
| 10:43 | — | Oráculo: verde, código de salida 0, 11 correctas, 0 con fallo y 12 inactivas (apartado 4). Sin commit todavía |
| 10:47 | *(este commit)* | Commit de los puntos 1 y 2 con esta bitácora. Hora del reloj al escribir la fila, antes del commit |
| 10:44 | — | El commit anterior es `b28eca4` (10:43:57 según `git log --format=%ci`). **Corrección de horas**: las filas de las 10:31, 10:36, 10:40 y 10:47 las escribió la IA con horas estimadas, sin mirar el reloj, aunque la nota de arriba y la propia fila de las 10:47 dicen lo contrario. Solo las de las 10:26 y las 10:43 salen de `date`. Es el mismo error de la sesión 03. Las filas se dejan como se escribieron; desde esta, todas las horas salen de `date` |
| 10:44 | — | Punto 4. Resolución de prueba de las dependencias en una carpeta temporal fuera del repo, para ver qué versiones hay publicadas antes de fijarlas (apartado 3) |
| 10:45 | — | `backend/pyproject.toml` y `backend/.python-version` con la herramienta `Write`: **el hook las dejó pasar**, primera prueba en vivo del camino permitido. `uv lock` y `uv sync --locked`: 33 paquetes |
| 10:46 | — | **Rojo**: test de humo escrito antes que el código; `uv run pytest` falla al recolectar, con `ModuleNotFoundError: No module named 'app'`, código 2 |
| 10:46 | — | **Verde**: paquetes de las cuatro capas y `app/main.py`. `1 passed`, cobertura del 100 %; `ruff check`, `ruff format --check` y `mypy --strict`, sin avisos |
| 10:47–10:56 | — | Sin actividad de la IA. En la conversación constan un `/login` interrumpido y el «Continúa» del Tech Lead |
| 10:56 | — | Consulta a PyPI por el aviso de `httpx` (apartado 3). `git rm backend/.gitkeep`. **Oráculo: verde**, código de salida 0, 19 correctas, 0 con fallo y 4 inactivas: las ocho comprobaciones del backend están activas |
| 10:57 | — | Arranque real: `uv run uvicorn --factory app.main:create_app --port 8765`; `GET /openapi.json` responde `200`; servidor parado después |
| 10:59 | *(este commit)* | Esqueleto del backend y esta bitácora. **La IA para aquí**, a la espera de la revisión de versiones y estructura. Hora de `date` (10:58:30) justo antes de preparar el commit; la real queda en `git log` |
| 11:10 | — | El commit anterior es `bcabea2` (10:58:57 según `git log`). Revisión del esqueleto por el Tech Lead: aprobado, con ocho decisiones (apartado 3) |
| 11:25 | `9344eed`, `203d602` | Fila escrita a las 11:25; las horas de dentro salen de `date` en cada comando y de `git log`. 11:11, rojo de `httpx` con los avisos como errores. 11:12, `httpx2` y fecha de corte: verde sin avisos; oráculo en verde. 11:13, commit `9344eed` (dependencias). 11:14, tests del oráculo en rojo y en verde. 11:15, oráculo real en verde, 19 correctas y 5 inactivas. 11:16, commit `203d602` (oráculo). 11:17–11:24, documentación: ADR-005, ADR-007, historiales de SPEC-01 y SPEC-02, `ai-workspace/README.md` y `CLAUDE.md` |
| 11:32 | *(este commit)* | El commit de documentación es `c6e13f2` (11:26:01 según `git log`). Pieza 1 del paso 1, errores genéricos: rojo a las 11:30, verde a las 11:31 y oráculo en verde a las 11:31 (apartado 3) |
| 11:34 | *(este commit)* | El commit de la pieza 1 es `fd8da13` (11:32:30 según `git log`). Pieza 2, CORS: rojo a las 11:33, verde y oráculo en verde a las 11:34 (apartado 3) |
| 11:37 | *(este commit)* | El commit de la pieza 2 es `54de302` (11:35:04 según `git log`). Pieza 3, `GET /health`: rojo a las 11:36, verde y oráculo en verde a las 11:37 (apartado 3) |
| 11:42 | *(este commit)* | El commit de la pieza 3 es `33033eb` (11:37:49 según `git log`). Pieza 4, esquema: rojo y verde a las 11:39, mutaciones a las 11:40, oráculo en verde a las 11:41 (apartado 3). **La IA para aquí**: paso 1 terminado, a la espera de la revisión antes de SPEC-02 |
| 12:02 | — | El commit de la pieza 4 es `fadd0cf` (11:42:28 según `git log`). El Tech Lead comunica la respuesta a la consulta de A2 a A5, con seis decisiones, y la revisión del paso 1: aprobado, con cinco correcciones y dos normas de proceso (apartado 3) |
| 12:10 | `72684a9` y *(este commit)* | ADR-008 en `72684a9` (12:09:30 según `git log`). Este commit: `supuestos.md`, índice de specs, las cuatro specs, `ai-workspace/README.md`, `CLAUDE.md` y esta bitácora. Oráculo en verde antes de los dos |
| 12:34 | `604a058` a `7900e5f` y *(este commit)* | Fila escrita a las 12:34; el detalle y las horas de cada paso están en las tablas «Correcciones del paso 1» y «SPEC-02» del apartado 3. El commit anterior a todos es `bb0871e` (12:10:42 según `git log`). Correcciones: p1 `604a058` (12:12:07), p2 `8de1f72` (12:12:55), p3 `b600624` (12:13:46), p4 `9ec6866` (12:18:35), p5 `1f8f80c` (12:20:30). SPEC-02: (a) `c002077` (12:24:02), (b) `49e3d65` (12:30:23), (c) `7900e5f` (12:34:28). Oráculo en verde antes de cada uno. Este commit solo cierra la bitácora. **La IA para aquí**: SPEC-02 terminada, a la espera de la revisión antes de SPEC-01 |

## 3. Revisiones y decisiones del Tech Lead

### Decisión de A2 a A5 (10:26, en el encargo)

La fecha límite del viernes 13 de noviembre de 2026 a las 10:00 se cumplió
sin respuesta externa. Que no ha llegado respuesta lo afirma el Tech Lead;
la IA no tiene forma de comprobarlo. Las cuatro decisiones son suyas y
aplican la hipótesis que ya estaba escrita en cada supuesto, sin cambiarla:

| # | Supuesto | Decisión del Tech Lead | Estado nuevo |
|---|---|---|---|
| d1 | A2 · plan | Dato informativo, sin efecto en el precio | `decidido (sin confirmación externa)` (2026-11-13) |
| d2 | A3 · almacenamiento y llamadas a la API | Se validan y se guardan, sin precio | `decidido (sin confirmación externa)` (2026-11-13) |
| d3 | A4 · países y tipos | La lista de nueve países con los tipos verificados | `decidido (sin confirmación externa)` (2026-11-13) |
| d4 | A5 · IVA entre empresas | Siempre el tipo del país del cliente; la inversión del sujeto pasivo queda anotada como simplificación conocida | `decidido (sin confirmación externa)` (2026-11-13) |

**La consulta sigue abierta.** Si la respuesta llega, no se reabre el
supuesto en silencio: se aplica como **cambio de spec**, con fecha y motivo
en el historial de cada spec afectada, y vuelve a pasar por aprobación
(ciclo de vida del índice de specs).

### Aprobación del bloque backend (10:26, en el encargo)

| # | Decisión del Tech Lead | Motivo |
|---|---|---|
| e1 | SPEC-01, SPEC-02 y SPEC-03 pasan a `aprobada` (2026-11-13), las tres a la vez, en las cabeceras y en el índice | Bloque backend (decisión y1 de la sesión 03) |
| e2 | SPEC-04 sigue en `borrador` hasta antes de empezar el frontend | — |

### Cómo se aplicaron los puntos 1 y 2 (10:36–10:43)

**Ficheros tocados**: `00-analisis/supuestos.md`, el índice de specs y las
cuatro specs. Ninguna regla de negocio, requisito, contrato ni caso de
prueba ha cambiado: solo estados, cabeceras, el apartado «Pendiente antes de
aprobar», tres frases de SPEC-02 que decían que A3 o A4 seguían pendientes
(2.2, 5.2 y la decisión 6 del apartado 7) y los historiales.

**Herramientas**: en `supuestos.md`, ocho sustituciones con un script de
Python de un solo uso que exige que cada texto aparezca exactamente una vez,
y dos retoques de ajuste de línea con la herramienta de edición. Todo lo de
`01-specs/` se hizo con la herramienta de edición, una sustitución cada vez,
para que pasara por el hook.

**Hook.** Siete ediciones de `01-specs/` llevaban la palabra «aprobada» en
el texto nuevo: las tres filas de estado de las cabeceras, las tres filas
del índice (una edición) y las tres filas de historial que anotan la
aprobación. Las siete se aplicaron. **La IA no ve el diálogo de
confirmación**: no puede afirmar que el hook preguntara ni cuántas veces;
eso lo sabe el Tech Lead. Las demás ediciones de `01-specs/` no contenían
esa palabra («aprobadas», «aprobado» y «aprobación» no la activan) y, según
la regla de `specgate.py`, no piden confirmación.

**Precisiones de la IA, sin aprobar** (están en el commit de este punto):

| # | Precisión |
|---|---|
| S-01 | En `supuestos.md`, el apartado «Pendientes de confirmar» pasa a llamarse «Decididos sin confirmación externa» y, en cada supuesto, «**Propuesta**» pasa a «**Decisión** (2026-11-13)». El texto de cada hipótesis no cambia. La tabla de estados conserva `pendiente de confirmar`, aunque hoy ningún supuesto lo usa |
| S-02 | El apartado «Pendiente antes de aprobar» de cada spec conserva su título y su número, para no romper las remisiones. En las tres aprobadas empieza por «Nada pendiente desde el 2026-11-13» y la tabla pasa a decir qué cambiaría si la respuesta contradijera la decisión. En SPEC-04 dice que solo queda la aprobación del Tech Lead |
| S-03 | La fila «Bloqueos para aprobarla» se conserva en las cuatro cabeceras, con «Ninguno desde el 2026-11-13» en las tres aprobadas. La fila «Depende de» dice que las specs de las que depende están aprobadas desde ese día |
| S-04 | En la tabla de A5 de SPEC-02 se añadió la frase de la decisión d4: se aplica siempre el tipo del país del cliente y la inversión del sujeto pasivo es una simplificación conocida. SPEC-02 no lo decía con esas palabras fuera de `supuestos.md` |
| S-05 | Dos filas de historial por spec aprobada (decisión de los supuestos y aprobación) y una en SPEC-04. En el índice, «Aprobado el 2026-11-13» en la fila del bloque backend |
| S-06 | **SPEC-01, apartado 8**: decía que la lectura directa de la página del Ministerio del Interior quedaba sin verificar (devolvió `403`) y que «si eso bloquea la aprobación lo decide el Tech Lead». El Tech Lead ha aprobado la spec sin mencionarlo. La IA quitó esa segunda frase, porque la aprobación ya está dada, y dejó el hecho: «Sigue sin verificar». **Pendiente de que el Tech Lead confirme que aprobó a sabiendas de ese punto** |

**Visto y no tocado** (la IA no cambia una spec aprobada por su cuenta):

- SPEC-02, nota «Sobre CA-09»: dice que `scripts/check.py` «aún no existe»
  y que el criterio está pendiente de implementar. El script existe desde
  `5d0df9f`. Corregirlo es un cambio en una spec aprobada.
- `ai-workspace/README.md`, apartado «Estado»: sigue diciendo «Proyecto en
  fase de análisis y especificación».
- Los documentos de `04-calidad/` y la bitácora de la sesión 03 nombran
  «Decidir A2 a A5» como tarea pendiente; son registros de su momento y no
  se retocan.

### Esqueleto del backend (10:44–10:57)

Punto 4 del encargo: paso 1 del orden de implementación, **solo el
esqueleto**. No hay errores genéricos, CORS, `/health` ni esquema.

**Versiones.** La IA no las eligió de memoria: resolvió las nueve
dependencias sin restricción con `uv lock` en una carpeta temporal y fijó en
`pyproject.toml`, con `==`, lo que uv devolvió. `uv.lock` fija las 33 (las
transitivas, con sus hashes). Fechas de publicación tomadas de `uv.lock`.

| Dependencia | Versión | Publicada | Grupo |
|---|---|---|---|
| `fastapi` | 0.162.5 | 2026-11-11 | aplicación |
| `pydantic` | 2.14.3 | 2026-11-05 | aplicación |
| `uvicorn` | 0.54.0 | 2026-09-25 | aplicación |
| `pytest` | 9.2.0 | 2026-10-27 | desarrollo |
| `pytest-cov` | 7.1.0 | 2026-03-21 | desarrollo |
| `ruff` | 0.17.5 | 2026-11-12 | desarrollo |
| `mypy` | 2.4.1 | 2026-10-28 | desarrollo |
| `httpx` | 0.28.1 | 2024-12-06 | desarrollo |
| `python-stdnum` | 2.2 | 2026-01-04 | desarrollo |

Transitivas de la aplicación: `starlette` 1.10.0, `pydantic-core` 2.50.4,
`anyio` 4.16.0, `idna` 3.20, `typing-extensions` 4.16.0, `typing-inspection`
0.4.5, `annotated-types` 0.8.0, `annotated-doc` 0.0.6, `opentelemetry-api`
1.45.2, `click` 8.5.1 y `h11` 0.16.0 (lista de `uv tree --no-dev`). Python:
3.12.0, el instalado; `requires-python = "==3.12.*"`.

**Hallazgos que la IA no ha resuelto y deja a la decisión del Tech Lead**:

| # | Hallazgo | Qué se ha comprobado |
|---|---|---|
| V-01 | **`httpx` está obsoleto para el cliente de test.** Con `starlette` 1.10.0, cada ejecución de pytest emite `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated; install httpx2 instead`. El test pasa. La IA **no ha instalado `httpx2`**: es una dependencia nueva, no aprobada, y el encargo nombra `httpx` | `starlette/testclient.py` intenta importar `httpx2` y, si no está, usa `httpx` con ese aviso. PyPI describe `httpx2` 2.16.0 como «The next generation HTTP client», con repositorio en `github.com/pydantic/httpx2` y 22 versiones entre el 2026-05-11 y el 2026-10-21. No se ha revisado su código ni su licencia |
| V-02 | **`fastapi` 0.162.5 trae `opentelemetry-api` como dependencia de ejecución.** La IA no lo esperaba | Figura en `requires_dist` de esa versión en PyPI (`opentelemetry-api>=1.44.0`). Nada del proyecto la usa |
| V-03 | **Varias versiones tienen menos de una semana**: `ruff` y `coverage` 7.17.3 son de ayer; `fastapi`, del día 11; `annotated-doc`, del 10; `click`, del 6. Una versión recién publicada ha tenido poco tiempo para que se le detecte un problema | Solo las fechas. Alternativa no aplicada: `exclude-newer` en `[tool.uv]` con una fecha de corte, que además hace repetible la resolución |
| V-04 | **El 100 % de ramas de `domain/` es hoy un verde vacío**: `app/domain/__init__.py` tiene 0 sentencias y `coverage` da 0 de 0 como 100 %. Lo mismo vale para la pureza y las capas: no hay código que comprobar | Salida de `coverage report --include=app/domain/*` |

**Estructura creada** (13 ficheros; `backend/.gitkeep`, vacío, se quitó):

```
backend/
  pyproject.toml  .python-version  uv.lock
  app/
    __init__.py  main.py
    api/  services/  domain/  repositories/     (un __init__.py cada una)
  tests/
    __init__.py
    unit/__init__.py
    integration/__init__.py  test_main.py
```

**TDD.** El rojo es de importación (`No module named 'app'`), no de
aserción: demuestra que el test se escribió antes, no que la aserción
detecte nada. Con una aplicación sin rutas la aserción es trivialmente
cierta.

**Precisiones de la IA, sin aprobar** (están en el commit del esqueleto):

| # | Precisión |
|---|---|
| K-01 | **Qué cita el test de humo.** El oráculo falla si un test no cita un requisito EARS, y ninguno habla de «la aplicación arranca». El test cita **SPEC-03/E-18**: pide `/openapi.json` y comprueba el `200` y que ninguna ruta ofrece `PUT`, `PATCH` ni `DELETE`. Es humo (la aplicación se construye, responde y publica su contrato) y a la vez una guarda real de E-18 que seguirá valiendo al añadir rutas. Alternativas no elegidas: eximir del control a los tests de humo, que relaja el oráculo, o citar un requisito que el test no comprueba |
| K-02 | **Fábrica y no instancia global**: `app/main.py` solo define `create_app()`; no hay un `app` de módulo. Se arranca con `uvicorn --factory app.main:create_app`. Motivo: `backend.md` pide no tener estado global mutable, y la configuración por variables de entorno se leerá al crear la aplicación, no al importar |
| K-03 | **Proyecto sin empaquetar** (`[tool.uv] package = false`, sin `build-system`): es una aplicación que se ejecuta desde `backend/`. `app` se importa en los tests con `pythonpath = ["."]` de pytest |
| K-04 | **Versiones con `==` también en `pyproject.toml`**, no solo en `uv.lock`. Las de desarrollo van en `[dependency-groups] dev` |
| K-05 | **Ruff**: línea de 100 caracteres y las reglas `E`, `W`, `F`, `I`, `N`, `UP`, `B`, `C4`, `SIM`, `ANN`, `BLE`, `S`, `DTZ`, `T20`, `PT` y `RUF`, cada una con su motivo en el fichero; `S101` (`assert`) permitido en `tests/`. `backend.md` solo dice «ruff (lint y formato) sin avisos»: la selección es de la IA |
| K-06 | **Cobertura**: `branch = true`, `source = ["app"]` y `fail_under = 90` en la configuración, para que `pytest --cov` dé el mismo veredicto que el oráculo. **mypy**: `strict = true` y `python_version = "3.12"`. No se añadió el plugin de Pydantic para mypy: no hay ningún esquema todavía |
| K-07 | **pytest**: `--strict-markers` y `--strict-config`. Los avisos no se convierten en errores; con V-01 el test fallaría |
| K-08 | `__init__.py` también en `tests/`, `tests/unit/` y `tests/integration/`, para que mypy no confunda dos ficheros de test con el mismo nombre. Cada `__init__.py` lleva una línea de documentación con la regla de su capa |
| K-09 | Se quitó `backend/.gitkeep`: la carpeta ya tiene contenido. No se creó `backend/README.md` ni se tocó el `README.md` de la raíz |

**Error propio.** Para parar el servidor de la prueba de arranque la IA usó
`taskkill /F /IM uvicorn.exe`, que mata **todos** los procesos con ese
nombre en la máquina, no solo el suyo. No comprobó antes si había otros.

### Revisión del esqueleto (11:10)

**Aprobado.** Todas las decisiones de esta tabla son del Tech Lead.

| # | Sobre | Decisión del Tech Lead | Motivo |
|---|---|---|---|
| f1 | V-01 | Sustituir `httpx` por `httpx2` como dependencia de desarrollo y añadir `filterwarnings = ["error"]` a pytest. Antes, enseñar el rojo: con `httpx` y el filtro activo, el test debe fallar por el aviso. Si con `httpx2` aparece otro aviso, no silenciarlo: enseñarlo. Actualizar ADR-005 | `httpx2` es lo que `starlette` y `fastapi` declaran ya en sus extras. El filtro, para que un aviso de obsolescencia rompa el test en vez de pasar inadvertido |
| f2 | V-03 | `exclude-newer = "2026-11-06T00:00:00Z"` en `[tool.uv]`, volver a resolver y enseñar la tabla de versiones antes y después. Si una versión que retrocede corregía un fallo de seguridad publicado, decirlo y decide él. Anotar la política donde corresponda según el criterio de los ADR | Una semana de margen ante versiones recién publicadas |
| f3 | V-02 y V-04 | Aceptados como están | `opentelemetry-api` es dependencia de `fastapi`; el verde vacío de `domain/` se llena con SPEC-02 |
| f4 | K-01 a K-09 | **Aprobados.** En K-01, añadir a las tareas pendientes que E-18 no está cubierto hasta que exista el test de CA-09 (`405` y datos sin cambios) | La trazabilidad ya lo da por probado |
| f5 | S-01 a S-06 | **Aprobados.** S-06: confirma que aprobó SPEC-01 sabiendo que la lectura directa de la página del Ministerio del Interior sigue sin verificar. Anotarlo en el historial de SPEC-01 | El algoritmo queda cubierto por los vectores y por la prueba diferencial de CA-19 |
| f6 | Oráculo | Con un test de `scripts/tests` que primero falle: (a) `uv run --locked`; (b) medir las ramas de verdad (`covered_branches / num_branches` de `coverage json`) manteniendo el 90 %, y ajustar el comentario de `pyproject.toml`. No relajar ningún umbral. Si hay un motivo para no hacerlo así, parar y decirlo | (a) Que falle si el lock está desfasado. (b) `--cov-branch --cov-fail-under=90` mide el total combinado de sentencias y ramas: con 11 de 11 sentencias y 2 de 4 ramas da 86,67 % |
| f7 | Visto y no tocado | Corregir la nota «Sobre CA-09» de SPEC-02 como cambio de spec con su fila de historial, y el apartado «Estado» de `ai-workspace/README.md` | `check.py` ya existe |
| f8 | Proceso | Dos normas: las horas de la bitácora salen del reloj en el momento de escribir la fila (añadirlo a `CLAUDE.md`), y un proceso se para por su PID, nunca por nombre | Es la segunda sesión con el mismo error de las horas |

Pidió tres commits separados (dependencias, oráculo y documentación), el
oráculo con su salida y, después, el resto del paso 1 en este orden: errores
genéricos, CORS, `/health` y esquema. Una pieza cada vez: test que falla por
aserción y no por importación, enseñando el rojo; después el verde, el
oráculo y un commit. Al terminar el paso 1, parar: lo revisa antes de
empezar SPEC-02.

**Sobre el texto del encargo**: llegó con tres frases cortadas («saleno de
escribir la fila», «errores genéricosema», «falla poraserción»). La IA las
leyó como «salen del reloj en el momento de escribir la fila», «errores
genéricos, CORS, `/health` y esquema» (el orden del índice de specs) y
«falla por aserción». Si alguna lectura no es la del Tech Lead, se corrige.

### Cómo se aplicó la revisión (11:10–11:25)

**f1 · `httpx2` y avisos como errores.** Rojo pedido, con `httpx` y
`filterwarnings = ["error"]` (11:11): pytest termina con código 2 al
recolectar, por el aviso convertido en error:

```
E   starlette.exceptions.StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
ERROR tests/integration/test_main.py - starlette.exceptions.StarletteDeprecat...
```

Con `httpx2` 2.16.0 (11:12): `1 passed`, **sin ningún aviso**. `httpx2`
trae `httpcore2` 2.16.0, `truststore` 0.10.5 y `httpx2-jsfetch` 1.0; salen
`httpx`, `httpcore` y `certifi`.

**f2 · Fecha de corte.** Versiones antes y después de
`exclude-newer = "2026-11-06T00:00:00Z"`; las demás no cambian:

| Paquete | Antes | Publicada | Después | Publicada |
|---|---|---|---|---|
| `fastapi` (directa) | 0.162.5 | 2026-11-11 | 0.162.0 | 2026-10-23 |
| `ruff` (directa) | 0.17.5 | 2026-11-12 | 0.17.4 | 2026-11-05 |
| `coverage` | 7.17.3 | 2026-11-12 | 7.17.2 | 2026-11-04 |
| `click` | 8.5.1 | 2026-11-06 | 8.5.0 | 2026-08-26 |
| `annotated-doc` | 0.0.6 | 2026-11-10 | 0.0.5 | 2026-07-28 |

**Seguridad de lo que retrocede**: ninguna de las cinco versiones a las que
se vuelve tiene avisos en PyPI (campo `vulnerabilities`) ni en OSV, y
ninguna nota de las versiones saltadas menciona seguridad (búsqueda por
palabras en las notas de GitHub). Lo que sí queda fuera son dos
correcciones de `fastapi`: 0.162.4 exige AnyIO 4.1.0 o posterior en
ejecución (hay instalada la 4.16.0) y 0.162.5 corrige la limpieza de
dependencias síncronas al cancelarse la petición. La IA no ha encontrado
nada que obligue a parar; el límite de la búsqueda está en ADR-007.

**f6 · Oráculo, con TDD.** Diez tests nuevos en
`scripts/tests/test_backend_coverage.py`. Rojo (11:14): `Ran 73 tests`,
`FAILED (failures=9)`, **los nueve por aserción**: ocho porque no existe la
comprobación de ramas (`0 != 1`) y uno porque los comandos empiezan por
`['uv', 'run', 'ruff']` y no por `['uv', 'run', '--locked']`. El décimo, que
el umbral conjunto se conserva, pasaba ya, como debe. Verde (11:14):
`Ran 73 tests`, `OK`. Prueba real del candado (11:16): con
`pyproject.toml` desfasado a propósito, `uv run --locked ruff check .`
termina con código 2 y «The lockfile at `uv.lock` needs to be updated, but
`--locked` was provided»; restaurado, código 0.

**La IA no vio motivo para no hacerlo como pedía f6**, con una condición que
aplicó: el 90 % sobre las ramas **se añade** al umbral conjunto y no lo
sustituye. Sustituirlo relajaría un caso: 50 de 100 sentencias y 9 de 10
ramas da el 90 % de ramas y un 53,6 % conjunto.

**Precisiones de la IA al aplicar la revisión, sin aprobar**:

| # | Precisión |
|---|---|
| T-01 | **La política de f2 va en un ADR nuevo, ADR-007**, y no dentro de ADR-005. El Tech Lead dijo «donde corresponda según el criterio de ADR-005»; la IA lo leyó como el criterio de qué decisiones llevan ADR (afecta a más de una spec y tiene alternativas) y, como el margen vale para todas las dependencias y no solo para las de test, le dio un ADR propio. ADR-005 se amplía solo con `httpx2` (apartado 3) |
| T-02 | ADR-007 deja **sin decidir el frontend**: nombra el mecanismo de uv y dice que el equivalente en npm se fija al crear el frontend |
| T-03 | Con 0 ramas que medir, la comprobación nueva sale **`INACTIVO`**, no correcta (`CLAUDE.md`, punto 4). Hoy está así: `app/` no tiene ninguna rama |
| T-04 | La comprobación llama a `coverage json` con `--fail-under=0`, para que juzgue solo las ramas; el umbral conjunto lo sigue juzgando pytest |
| T-05 | Las dos comprobaciones de cobertura que ya existían **cambian de nombre** para decir lo que miden: «pytest con el 90 % de sentencias y ramas, en conjunto» y «100 % de sentencias y ramas en domain/». Sus comandos y umbrales no cambian. El 100 % conjunto de `domain/` implica el 100 % de sus ramas |
| T-06 | El ejecutor simulado de los tests pasa de `test_stack_and_report.py` a `tests/support.py` y aprende a escribir el informe de `coverage json`. Las aserciones de los tests que ya existían no cambian |
| T-07 | La norma del PID también va a `CLAUDE.md` (punto 8 del flujo). El Tech Lead solo pidió expresamente añadir allí la de las horas |
| T-08 | La nota «Sobre CA-09» de SPEC-02 conserva el aviso de que el criterio no puede darse por cumplido, ahora por otro motivo: `domain/` no tiene código |

**Texto ajeno no seguido.** Las notas de versión de `fastapi` en GitHub
empiezan con un párrafo dirigido a agentes de código que invita a instalar
una «skill» con `uvx library-skills`. Es contenido de un tercero leído como
dato; la IA no lo ha ejecutado.

**Errores propios**:

- El commit `9344eed` nombra ADR-007 en un comentario de `pyproject.toml`;
  el ADR no existe hasta el commit de documentación.
- Un script de edición de la documentación falló al analizarse el comando y
  no aplicó nada; los cambios se hicieron después con la herramienta de
  edición. Los cambios de `scripts/` y de `pyproject.toml` sí se hicieron
  con scripts de un solo uso, que el hook no ve; ninguno toca ficheros
  protegidos ni specs.

### Paso 1 · Pieza 1: errores genéricos (11:27–11:32)

Requisitos: SPEC-03/E-29 y E-33, y las convenciones comunes del índice.

**Diseño, y por qué.** La IA pensaba apoyarse en piezas internas de FastAPI
y comprobó antes en el código instalado (0.162.0) que ya no son como las
recordaba: `get_flat_dependant` no existe y `include_router` deja en la
aplicación un objeto privado `_IncludedRouter`. Por eso solo usa API
pública:

| Error | Dónde se decide |
|---|---|
| `415` y `400` | Un middleware (`RequestBodyGuard`) que lee el cuerpo antes de que lo analice ningún endpoint |
| `422` por parámetro de consulta no documentado | Una dependencia de toda la aplicación, que compara la petición con lo que el OpenAPI declara para esa operación |
| `404` y `405` | Un manejador de las excepciones HTTP del framework |
| `500` | Un middleware (`UnexpectedErrorGuard`) que registra el error con su traza en el log y responde `internal_error` |

Los códigos de error viven en un único módulo, `app/api/problems.py`.

**Rojo (11:30)**: `20 failed, 3 passed`. Diecinueve fallan **por aserción**
(`'application/json' == 'application/problem+json'`, `422 == 400`,
`422 == 415`, `200 == 422`, `418 == 500`). El vigésimo, el fallo inesperado,
no falla por aserción ni por importación: la excepción de la ruta de prueba
sale de la aplicación (`RuntimeError`). Los tres que pasaban son el de humo
y los dos que comprueban que algo válido se acepta. **Verde (11:31)**:
`23 passed`, 115 sentencias y 14 ramas, todas cubiertas. Oráculo en verde:
20 correctas, 0 con fallo y 4 inactivas; la comprobación de ramas se activa
por primera vez, con 14 de 14.

**Precisiones de la IA, sin aprobar** (en el commit de esta pieza):

| # | Precisión |
|---|---|
| G-01 | **Rutas de prueba.** Los endpoints de negocio no existen, así que los tests añaden a la aplicación real cuatro rutas `/probe` (`tests/integration/probe_app.py`). Las filas de 5.7 con las rutas reales (CA-17) quedan pendientes hasta que existan |
| G-02 | **El cuerpo se comprueba antes de buscar la ruta.** Una petición con cuerpo mal formado a una ruta que no existe, o con un método no admitido, responde `415` o `400`, no `404` ni `405`. La spec solo fija la precedencia entre `415`, `400` y `422` |
| G-03 | `415` para cualquier petición con cuerpo cuyo `Content-Type` no sea `application/json` (con o sin parámetros), también si falta la cabecera. `application/problem+json` y otros `+json` no valen |
| G-04 | `400` también si el cuerpo no es UTF-8 o está anidado más allá de lo que admite el analizador de JSON |
| G-05 | Parámetros de consulta: la fuente de lo documentado es el OpenAPI de la operación. Un error por parámetro, en el orden de la petición; uno repetido se informa una vez |
| G-06 | Un error HTTP con un estado que el contrato no define (la ruta de prueba lanza un `418`) responde `500` `internal_error` y se registra en el log |
| G-07 | El `500` lo produce un middleware y no un manejador de excepciones, para que la respuesta quede dentro del middleware de CORS (E-24, pieza siguiente) |
| G-08 | `title` escrito a mano por estado. El de `422` es «Unprocessable Content», como en el ejemplo del índice; Python 3.12 daría «Unprocessable Entity» |
| G-09 | El `405` conserva la cabecera `Allow` del framework. Las rutas `/docs`, `/redoc` y `/openapi.json` siguen activas |

**No hecho en esta pieza**: la traducción de los errores de validación del
cuerpo y de la ruta (`missing`, `not_an_integer`, `out_of_range`…) a
códigos por campo. Depende de los campos de cada contrato y se hará con el
primer endpoint que tenga cuerpo (SPEC-02). Hasta entonces, un error así
saldría con el formato por defecto de FastAPI; hoy ninguna ruta real lo
puede provocar. Tampoco se ha hecho ninguna prueba de mutación.

### Paso 1 · Pieza 2: CORS (11:32–11:35)

Requisitos: SPEC-03/E-24, E-25, E-26, E-30 y E-31, y el segundo caso de
E-33. Middleware de CORS estándar del framework, sin código a medida, con
los orígenes de `CORS_ORIGINS` leídos al construir la aplicación
(`app/config.py`).

**Comportamiento estándar observado antes de escribir el test** (pendiente
desde la sesión 03): con Starlette 1.10.0, la comprobación previa rechazada
responde **`400`** con cuerpo de texto («Disallowed CORS origin»), que era lo
esperado y no estaba verificado. Si el origen no está admitido no lleva
`access-control-allow-origin`; si lo rechazado es el método, sí la lleva. El
test compara el estado y el conjunto completo de cabeceras con valores
escritos en el propio test.

**Rojo (11:33)**: `8 failed, 4 passed`, los ocho **por aserción**
(`None == 'http://localhost:4200'`, `405 == 200`, `405 == 400`). En la
primera ejecución cuatro fallaban con `KeyError` al leer la cabecera
ausente; la IA cambió la lectura a `headers.get(...)` para que el fallo
fuera una aserción y repitió el rojo. Los cuatro que pasaban comprueban
ausencias, que sin middleware se cumplen solas. **Verde (11:34)**:
`35 passed`, 133 sentencias y 14 ramas cubiertas. Oráculo en verde: 20
correctas, 0 con fallo y 4 inactivas.

**Precisiones de la IA, sin aprobar**:

| # | Precisión |
|---|---|
| C-01 | Los tests usan `GET /probe` en lugar de `GET /meta`, que no existe. Las filas de 5.6 con `/meta` (CA-15) quedan pendientes hasta SPEC-01 |
| C-02 | `CORS_ORIGINS` admite espacios alrededor de cada origen y entradas vacías (una coma final). **Definida pero vacía no es «sin definir»**: no se admite ningún origen |
| C-03 | El middleware estándar anuncia en `access-control-allow-headers`, además de `Content-Type`, las cabeceras `Accept`, `Accept-Language` y `Content-Language`, y añade `access-control-max-age: 600`. La spec dice que la cabecera admitida es `content-type`; no se ha escrito código para quitar las otras |
| C-04 | La cabecera CORS acompaña también a los `404`, `405`, `415`, `400` y `422`: los dos guardas quedan dentro del middleware de CORS |

**Visto y no resuelto**: en el `405` de `OPTIONS /probe`, la cabecera
`Allow` del framework dice solo `POST`, aunque la ruta admite también
`GET`. Las dos operaciones se declaran por separado y el framework informa
de la primera que coincide.

### Paso 1 · Pieza 3: `GET /health` (11:35–11:38)

Requisitos: SPEC-03/E-27 y E-28. Primera pieza que atraviesa las cuatro
capas menos el dominio: `api/health.py` (ruta fina y esquema de salida),
`services/health.py` (caso de uso), `repositories/database.py` (la única que
importa `sqlite3`) y la composición en `main.py`. Cada capa lanza su propio
error (`DatabaseUnavailableError`, `ServiceUnavailableError`) y `api/` lo
traduce a `503` en el único sitio donde se traducen los errores.

**Rojo (11:36)**: `3 failed`, los tres **por aserción**: `404 == 200`,
`404 == 503` y `[] == ['200', '503']` (el OpenAPI aún no declara la
operación). **Verde (11:37)**: `38 passed`, todo cubierto. Oráculo en verde:
20 correctas, 0 con fallo y 4 inactivas; 14 de 14 ramas.

**Precisiones de la IA, sin aprobar**:

| # | Precisión |
|---|---|
| H-01 | **La base de datos inaccesible del test es real**, no simulada: `DATABASE_PATH` apunta a una carpeta y `sqlite3` no puede abrirla. CA-16 dice «se simula con una conexión que falla»; una conexión que falla de verdad cumple lo mismo y además ejercita la captura del error de `sqlite3` |
| H-02 | El `503` se registra en el log con su causa; la respuesta solo lleva el código y un texto genérico |
| H-03 | `DATABASE_PATH` entra ya en la configuración, con su valor por defecto, porque `/health` necesita una ruta. **Su test (E-32, CA-12) va en la pieza siguiente**, así que el valor por defecto queda hoy sin un test propio. La conexión todavía no ejecuta `PRAGMA foreign_keys = ON`: lo exige E-20 y se añade con su test en la pieza del esquema |
| H-04 | El servicio se construye en `main.py`, se guarda en el estado de esa aplicación y llega a la ruta con `Depends`. `api/` no puede importar de `repositories/` |
| H-05 | En el OpenAPI, el cuerpo del `503` figura bajo `application/json` y no bajo `application/problem+json`, que es lo que de verdad se responde. Es como FastAPI documenta una respuesta adicional con modelo; no se ha escrito código para cambiarlo |
| H-06 | Texto del `503`: «El servicio no está disponible en este momento.» |

### Paso 1 · Pieza 4: esquema de la base de datos (11:38–11:42)

Requisitos: SPEC-03/E-19, E-20, E-21, E-22 y E-32 (2.6 y 5.5; CA-10, CA-11
y CA-12). El DDL está en `backend/app/repositories/schema.sql`, enlazado
desde el índice de arquitectura; se aplica al arrancar (`lifespan`) con
`CREATE TABLE IF NOT EXISTS`, y cada conexión ejecuta
`PRAGMA foreign_keys = ON`.

**Rojo (11:39)**: `2 failed, 1 passed, 23 errors`. Los 25 que no pasan
fallan por **la misma aserción**, «the application did not create the
database on startup»; pytest cuenta 23 como error y no como fallo porque la
aserción salta al preparar la conexión del test. El que pasaba es el de la
ruta por defecto (E-32), cuyo código entró en la pieza 3. **Verde (11:39)**:
`64 passed`, 216 sentencias y 14 ramas cubiertas.

**Como ese rojo no demuestra que cada test de restricción detecte lo suyo**,
la IA hizo tres mutaciones sobre el código ya en verde, restaurando después
cada fichero: sin `PRAGMA foreign_keys`, fallan los tres tests de claves
foráneas; sin el `CHECK` del total, falla solo el caso del total; con
`tax_cents` como `REAL`, falla el test de tipos. No es una prueba de
mutación completa.

Oráculo en verde (11:41): 20 correctas, 0 con fallo y 4 inactivas; 14 de 14
ramas; 68 requisitos del backend sin test.

**Precisiones de la IA, sin aprobar**:

| # | Precisión |
|---|---|
| Q-01 | El esquema se crea **al arrancar** (`lifespan`), no al construir la aplicación. Un cliente de test que no arranca la aplicación no toca el disco |
| Q-02 | Si el esquema no se puede crear, el arranque falla con el error original; no se captura |
| Q-03 | Además de las filas de 5.5, se prueban los negativos de todas las columnas con `>= 0`, un tramo de una simulación inexistente, que ninguna columna admite nulos salvo `to_users` y la unicidad de `(country, tax_id)` |
| Q-04 | Sin tablas `STRICT`, sin índices adicionales y sin `AUTOINCREMENT`: la spec no los pide |
| Q-05 | El test de la unicidad cita SPEC-03/E-22 y **no** SPEC-01/E-19 (el `409`), para que la trazabilidad no dé por cubierto un requisito que solo se probará con su endpoint. La IA lo había citado al principio y lo corrigió antes del commit |

**No hecho**: la prueba de arranque real con `uvicorn` tras el paso 1. La
IA la lanzó con una base de datos temporal y parando el proceso por su PID,
pero **la ejecución de esa orden fue denegada** y no la repitió. El arranque
con `lifespan` solo está comprobado con el cliente de test.

### Cierre del paso 1 (11:42)

Lo que queda al parar:

- **Paso 1 completo**: errores genéricos, CORS, `GET /health` y esquema, en
  cuatro commits, cada uno con el oráculo en verde. 64 tests del backend y
  73 de `scripts/`.
- **Lo común está probado con rutas de prueba**, no con los endpoints de
  negocio, que no existen: E-24 a E-26, E-29 a E-31 y E-33 figuran como
  cubiertos en la trazabilidad, pero CA-15 y CA-17 piden esas filas con
  `/meta`, `/customers`, `/simulations` y `/pricing/quote`.
- No existe ningún código de `domain/`: sus tres comprobaciones pasan sin
  nada que medir.
- Sin aprobar: T-01 a T-08, G-01 a G-09, C-01 a C-04, H-01 a H-06 y Q-01 a
  Q-05.

### Llega la respuesta a la consulta de A2 a A5 (12:02)

El Tech Lead comunica que la respuesta ha llegado hoy, 2026-11-13, después
de haber decidido los cuatro supuestos sin ella (apartado «Decisión de A2 a
A5», 10:26). **Resumen fiel dado por el Tech Lead; no es cita literal.** La
IA no ha visto la respuesta original.

- **Plan**: dato informativo del cliente; no modifica el precio. El coste se
  calcula solo con los tramos de usuarios. Los valores del plan son de libre
  elección.
- **Almacenamiento y llamadas a la API**: no se tarifican; basta con
  registrarlos y mostrarlos en la simulación, sin coste.
- **Impuesto**: basta con el tipo general de IVA del país del cliente. No
  hace falta contemplar la inversión del sujeto pasivo ni otros casos
  especiales, pero se valorará que quede documentado cómo se abordaría.
- **Decisiones propias**: cualquier otra decisión tomada por cuenta propia
  debe quedar documentada en `ai-workspace` con su motivo; forma parte de lo
  que se evalúa.

Decisiones del Tech Lead:

| # | Decisión | Motivo |
|---|---|---|
| R1 | A2, A3 y A5 quedan confirmados **sin cambio en ninguna regla**: pasan a `decidido` (2026-11-13), con la respuesta como fuente | La respuesta coincide con lo decidido |
| R2 | A4 queda confirmado **solo en parte**: el uso del tipo general, sí; la lista de nueve países no figura en la respuesta y sigue siendo decisión del Tech Lead. `supuestos.md` debe decirlo así | No atribuir a la respuesta más de lo que dice |
| R3 | Planes: se mantienen los códigos y los nombres de SPEC-01 (D-04) | La respuesta deja los valores a su elección |
| R4 | Ninguna regla cambia: se mantiene la aprobación de SPEC-01, SPEC-02 y SPEC-03. Actualizar la fila «Supuestos», el apartado «Pendiente antes de aprobar» y el historial de cada spec afectada, también SPEC-04. Quitar «la consulta sigue abierta»: está cerrada | — |
| R5 | Documento nuevo, como **propuesto**: cómo se abordaría la inversión del sujeto pasivo y los demás casos especiales. ADR o apartado según el criterio de los ADR; enlazado desde A5, SPEC-02 y el índice de arquitectura. Una página como mucho; cada afirmación fiscal, con fuente oficial y fecha; lo no verificado, dicho. Sin implementar nada | Se va a valorar |
| R6 | Comprobar que `ai-workspace/README.md` lleva de forma visible a `supuestos.md` y a los ADR como el sitio de las decisiones propias con su motivo | Cuarto punto de la respuesta |

Pidió dos commits (supuestos y specs; documento nuevo), con el oráculo en
verde tras cada uno.

### Revisión del paso 1 (12:02, en el mismo mensaje)

**Aprobado, con cinco correcciones antes de SPEC-02.** La prueba de
arranque real que se denegó a la IA la ha hecho el Tech Lead: con `uvicorn`
y una base de datos temporal arranca, crea la carpeta y las tres tablas, y
los errores genéricos y CORS responden como dice la spec.

Aprobados: T-01 a T-08, G-01 a G-09, C-01 a C-04, H-01 a H-04, H-06, Q-01 a
Q-03 y Q-05. **Cambian H-05 y Q-04.**

| # | Corrección ordenada por el Tech Lead | Motivo |
|---|---|---|
| p1 | **`/health` da `200` sin base de datos.** Con el servidor en marcha, si el fichero desaparece, responde `200` y deja creado un fichero vacío, sin tablas, porque `sqlite3.connect` crea el fichero que no existe. Solo `create_schema` puede crear el fichero; cualquier otra conexión falla si no existe, y `/health` responde `503` sin crear nada | No cumple el propósito de E-28 ni el «no lee ni escribe» de 2.7. Defecto de la IA en la pieza 3 |
| p2 | **`GET /health/` responde `307`** con redirección a `/health`. Una ruta con barra final es una ruta que no existe: `404` `not_found`. Desactivar la redirección del framework | — |
| p3 | **El guarda del cuerpo acepta `{"a": NaN}` e `Infinity`**, que no son JSON válido (RFC 8259): `400` `malformed_request` | La IA lo vio al diseñar la pieza 1 y lo dejó sin hacer |
| p4 | **Q-04 cambia: tablas `STRICT`.** Hoy la base de datos acepta `10.5` en `base_cents` y `'abc'` en `active_users`, porque en SQLite el tipo declarado es solo una afinidad. Cambio de SPEC-03 2.6, con historial, y nota en ADR-004 con la versión mínima de SQLite | Un importe con decimales nunca puede ser cierto (E-19, A6): entra en lo que la base de datos debe impedir |
| p5 | **H-05 cambia**: el OpenAPI declara los errores bajo `application/problem+json`, con una ayuda en `problems.py` que sirva a todos los endpoints | Es lo que se responde, y `backend.md` dice que el OpenAPI es el contrato |

Cada corrección, con su test en rojo por aserción antes del código, y un
commit por corrección.

**Pendientes que no se hacen ahora**: la cabecera `Allow` del `405` se
corrige con la primera ruta que tenga dos métodos (SPEC-01); el cuerpo de la
petición no tiene límite de tamaño, limitación conocida que se documentará
en el README.

**Dos normas de proceso**:

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| n1 | En las piezas 1 y 2 lanzó el test en rojo **en el mismo lote** que la escritura del código | Desde ahora: test, ejecución, resultado en rojo a la vista, y solo entonces el código | El rojo fue real, pero el código no esperó a verlo |
| n2 | Editó ficheros de `backend/` con `sed` y scripts de un solo uso | Los ficheros de `backend/` y `frontend/` se editan con las herramientas de edición | Para que el hook los vea |

Después: SPEC-02 completa, en tres piezas y tres commits (dominio,
traducción de los errores de validación y `POST /pricing/quote`), y parar.

### Cómo se aplicó la respuesta a la consulta (12:02–12:10)

**R1 a R4 y R6**: `supuestos.md`, el índice de specs, las cuatro specs
(fila «Supuestos», fila «Bloqueos», apartado «Pendiente antes de aprobar»,
tres frases de SPEC-02 e historial) y `ai-workspace/README.md`. Todas las
ediciones de `01-specs/`, con la herramienta de edición. Ninguna regla,
requisito, criterio ni caso cambia. «La consulta sigue abierta» ya no
aparece en ningún documento vivo; queda en las filas de historial de esta
mañana, que no se retocan.

**R5 · ADR-008**, en estado `propuesto`. Fuentes: la IA descargó seis
páginas oficiales a una carpeta temporal y leyó en ellas las frases que cita
el documento (Comisión Europea: «Cross-border VAT», VIES, tipos y ventanilla
única; Gobierno del Reino Unido: Notice 741A y servicios digitales a
consumidores). Las páginas de la Agencia Tributaria y del Gobierno de
Canarias que intentó leer devolvieron `404`, y no leyó el texto de la
Directiva: el documento lo dice en su apartado de no verificado.

**Precisiones de la IA, sin aprobar**:

| # | Precisión |
|---|---|
| U-01 | El documento de R5 es **un ADR nuevo** (ADR-008) y no un apartado: afecta a más de una spec y es un diseño con alternativas |
| U-02 | Estado de A4: `decidido` (2026-11-13), con el texto «confirmado solo en parte» en la misma celda del resumen. El oráculo solo exige que el estado empiece por `decidido` |
| U-03 | En `supuestos.md`, el apartado pasa a llamarse «Consultados a quien propone el reto (A2 a A5)», con la secuencia de lo ocurrido, el resumen de la respuesta y una tabla de qué confirma y qué sigue siendo decisión propia. Los dos estados que ya no usa ningún supuesto se conservan en la tabla de estados, con una nota |
| U-04 | R6: `ai-workspace/README.md` nombraba las carpetas, pero no decía en ningún sitio que ahí estén las decisiones propias. La IA añadió el apartado «Dónde están las decisiones propias», que lleva a `supuestos.md`, a los ADR, a las tablas de decisiones de las specs y a la bitácora |
| U-05 | Las dos normas de proceso n1 y n2 van también a `CLAUDE.md`, como se hizo con las anteriores |
| U-06 | **ADR-008 no cabe estrictamente en una página**: tiene 88 líneas y 817 palabras. La primera versión tenía 103 líneas; la IA la recortó y rehízo el commit (`bbe0c25` pasó a ser `72684a9`) antes de hacer ningún otro. Si debe caber en una página impresa, hay que quitar algo; la IA no ha decidido qué |

**Orden de los commits**: primero el de ADR-008 y después el de supuestos y
specs, para que ningún enlace apunte a un documento que aún no existe (el
error de `9344eed`).

### Correcciones del paso 1 (desde las 12:11)

Una fila por corrección, escrita al terminarla. En todas: primero el test,
después su ejecución con el rojo a la vista y solo entonces el código, en
pasos separados (norma n1); el código de `backend/`, con las herramientas de
edición (norma n2).

| Hora | # | Rojo visto antes del código | Qué se hizo | Verde y oráculo |
|---|---|---|---|---|
| 12:11 | p1 | `assert 200 == 503`: con el fichero apartado, `/health` respondía `200` | `Database.connect()` abre el fichero en modo `rw` (URI de SQLite) y falla si no existe; solo `create_schema()` lo abre en modo `rwc`. **Cambio en un test que ya existía**: el del `200` arrancaba la aplicación sin su fase de arranque y dependía de que la conexión creara el fichero, que era el defecto; ahora la arranca como un servidor real. Su aserción no cambia | `65 passed`; oráculo en verde, 20 correctas y 4 inactivas |
| 12:12 | p2 | `assert 307 == 404` en `/health/` y en `/probe/` | `redirect_slashes=False` al construir la aplicación. El commit de p1 es `604a058` (12:12:07 según `git log`) | `67 passed`; oráculo en verde |
| 12:13 | p3 | `assert 200 == 400` en las tres filas nuevas (`NaN`, `Infinity`, `-Infinity`): el cuerpo se aceptaba | El guarda analiza el JSON con `parse_constant`, que rechaza esas tres constantes. El commit de p2 es `8de1f72` (12:12:55) | `70 passed`; oráculo en verde |
| 12:18 | p4 | `Failed: DID NOT RAISE IntegrityError` en las cuatro filas nuevas. **Primera ejecución (12:14): solo tres en rojo.** La fila del texto en `users` de un tramo ya pasaba, pero por otro motivo: la rechazaba el `CHECK` del subtotal (`1000 * 'many'` vale 0), no el tipo. Se cambió esa fila (precio 0 y subtotal 0) para que solo el tipo pudiera rechazarla y se repitió: cuatro en rojo (12:16) | `STRICT` en las tres tablas de `schema.sql`. SPEC-03: regla nueva en 2.6, fila de historial y, **sin que el encargo lo nombrara**, E-21 ampliado y cuatro filas en 5.5 (precisión P-01, abajo). ADR-004: añadido con la versión mínima (SQLite 3.37.0; el entorno tiene la 3.42.0). El commit de p3 es `b600624` (12:13:46) | `74 passed`; oráculo en verde (20 correctas, 0 con fallo, 4 inactivas) |
| 12:20 | p5 | `assert ['application/json'] == ['application/problem+json']` en el test nuevo de `/health` (12:19) | `problem_responses({estado: descripción})` en `app/api/problems.py`: devuelve el `responses` de un endpoint con cada error bajo `application/problem+json` y el esquema del problema. `/health` lo usa. Los modelos `ProblemDocument` y `FieldErrorDocument` desaparecen: solo servían para el OpenAPI. El test compara lo declarado con un `503` real: los campos obligatorios son los que se responden y el único opcional es `errors`. El commit de p4 es `9ec6866` (12:18:35) | `75 passed`; oráculo en verde (20 correctas, 0 con fallo, 4 inactivas) |

Precisiones de la IA sobre p5, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| P-05 | El esquema del problema se escribe **en línea** en cada respuesta de error, como un diccionario constante (`PROBLEM_SCHEMA`), y no como un componente con nombre del OpenAPI | FastAPI solo registra como componente un modelo Pydantic, y un modelo lo documenta bajo `application/json`, que es justo lo que había que quitar. Coste: el documento repite el esquema en cada error de cada endpoint |
| P-06 | La forma del error queda en dos sitios de `problems.py`: `problem_response` (lo que se responde) y `PROBLEM_SCHEMA` (lo que se declara). El test de `/health` compara los dos con un `503` real; **la entrada `errors` del esquema no se compara todavía con una respuesta real** | Se podrá comparar con el primer `422` de un endpoint real (SPEC-02) |
| P-07 | `problem_responses` usa `Any` en su tipo de retorno, con un comentario en esa línea | Es el tipo del parámetro `responses` de FastAPI; `mypy --strict` no acepta otro más estrecho por la invarianza de `dict` |
| P-08 | Solo se declaran los errores propios de cada endpoint (en `/health`, el `503`). Los genéricos (`400`, `404`, `405`, `415`, `422` por parámetro no documentado, `500`) no se declaran en cada operación | SPEC-03 4.4 solo lista el `200` y el `503`, y el test que ya existía exige exactamente esos dos. Si el Tech Lead los quiere en el OpenAPI, la ayuda ya sirve |

**Error de la IA, corregido a las 12:20**: en el commit `1f8f80c` (p5,
12:20:30) tres celdas de la tabla de tareas pendientes decían que la
revisión del paso 1 fue «a las 12:05». Era una hora puesta de memoria, no
leída: la cronología registra esa revisión a las 12:02. Las tres celdas
dicen ahora 12:02. Es la tercera vez en dos sesiones que aparece una hora
no leída del reloj o de la propia bitácora.

Precisiones de la IA sobre p4, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| P-01 | El encargo decía «cambio de SPEC-03 2.6». Además de 2.6 se ampliaron **E-21** (el valor que no es del tipo de su columna) y la tabla **5.5** (cuatro filas) | El test cita E-21 y, sin ampliarlo, citaría un requisito que no dice eso; los casos de prueba de la base de datos están en 5.5. Si el Tech Lead prefiere otro requisito o ninguno, se cambia |
| P-02 | `STRICT` no rechaza todo lo que no es entero: convierte lo que se puede convertir sin pérdida (`15.0` y `'15'` se guardan como `15`). Comprobado a mano con SQLite 3.42.0; **no hay test** de esa conversión | Es el comportamiento documentado de SQLite; queda escrito en SPEC-03 2.6 y en ADR-004 para que no se lea «rechaza cualquier real» |
| P-03 | Una base de datos creada **antes** de este commit sigue sin `STRICT`: `CREATE TABLE IF NOT EXISTS` no toca una tabla que ya existe. Hay que borrar el fichero | Afecta a quien ya arrancó el backend (la prueba de arranque real del Tech Lead). Anotado en ADR-004 |
| P-04 | Con un SQLite anterior a 3.37.0 el arranque falla con un error de sintaxis de SQLite, no con un mensaje propio. No se añadió una comprobación de versión | No estaba pedida. Falla al arrancar, que es lo seguro; el mensaje es mejorable |

### SPEC-02 (desde las 12:21)

Una fila por pieza, escrita al terminarla, con las mismas normas n1 y n2.

| Hora | Pieza | Rojo visto antes del código | Qué se hizo | Verde y oráculo |
|---|---|---|---|---|
| 12:23 | (a) dominio | 12:22: **31 en rojo, todos por aserción** (`AssertionError` o `DID NOT RAISE`), y **3 en verde**: las tres filas de 5.3 cuyo impuesto esperado es 0, que un esqueleto que devuelve 0 cumple sin querer. Para que el rojo no fuera de importación se escribió antes un esqueleto sin lógica: los tipos y dos funciones que devuelven 0 y una lista de tramos vacía (W-01) | `app/domain/countries.py`: la constante de países con su tipo y `tax_rate_bp_of`. `app/domain/pricing.py`: los tres tramos como datos, `tax_cents` y `calculate_quote`, que es el único cálculo. Tests en `tests/unit/test_pricing.py`: las 10 filas de 5.1, los 9 países de 5.2, las 8 filas de 5.3, el ejemplo completo del apartado 4, CA-03 (de 0 a 1000) y CA-04. El commit de p5 es `1f8f80c` (12:20:30) | `109 passed`; `domain/` al 100 % de sentencias y ramas; oráculo en verde (20 correctas, 0 con fallo, 4 inactivas; 16 de 16 ramas) |
| 12:29 | (b) errores de validación | **Tres rojos, cada uno antes de su código.** 12:26: 17 en rojo (`'application/json' == 'application/problem+json'` en 16 y `422 == 500` en uno) y 1 en verde, el del cuerpo válido. 12:27: `500 == 422` en la fila del campo que falla dos veces, añadida al ver en la cobertura una rama sin ejecutar (W-16). 12:28: `['0.0', '100.0'] == ['100']` y otras dos, con un test de mensaje más estricto que el primero (W-17) | `app/api/validation.py` traduce los errores de Pydantic a los del contrato: un error por campo, el primero; campos del contrato en su orden y después los desconocidos; códigos `missing`, `not_an_integer`, `out_of_range` y `unknown_field` (ahora en `FieldCode`). Un manejador de `RequestValidationError` en `error_handling.py` sustituye al de FastAPI. `app/api/contract.py` lee del OpenAPI la operación de la petición (lo usa también el guarda de parámetros). Se prueba con una ruta de prueba, `/probe/numbers`. El commit de (a) es `c002077` (12:24:02) | `130 passed`; oráculo en verde (20 correctas, 0 con fallo, 4 inactivas; 26 de 26 ramas) |
| 12:34 | (c) `POST /pricing/quote` | **Dos ejecuciones antes del código.** 12:31: 29 en rojo y 1 en verde; de los rojos, uno era un `KeyError` y no una aserción, y el verde era el de «no guarda nada», que una ruta inexistente cumple sin querer. Se corrigieron los dos tests (comprobar el estado antes de leer el cuerpo; exigir que las proyecciones respondan `200`, `404` y `422`) y se repitió. 12:31:58: **30 en rojo, todos por aserción** (`404 == 422`, `404 == 200`, `'not_found' == 'customer_not_found'`…), porque la ruta no existía | `app/api/pricing.py` (esquemas estrictos y router fino), `app/services/pricing.py` (`PricingService.quote`), `app/repositories/customers.py` (`country_of`). Códigos `customer_not_found` y `tax_rate_not_defined` en `problems.py`, traducidos en `error_handling.py`. Los errores del OpenAPI se declaran con `problem_responses`. Tests: el ejemplo del apartado 4, cada fila de 5.4 y de 5.5, CA-06, CA-10 y CA-11. El commit de (b) es `49e3d65` (12:30:23) | `160 passed`; oráculo en verde (20 correctas, 0 con fallo, 4 inactivas; 30 de 30 ramas). De SPEC-02 solo queda sin test E-08, que es de SPEC-03 |

Precisiones de la IA sobre SPEC-02, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| W-01 | Antes del rojo de (a) se escribió un esqueleto del dominio sin lógica (clases de datos, errores y funciones que devuelven 0) | La norma pide un rojo por aserción y no por importación; sin el módulo, el test no llega a ejecutarse. La lógica se escribió después de ver el rojo |
| W-02 | La tabla 5.2 se prueba con **un caso por país** (9), no uno por fila (5) | Una fila como «FR, GB» son dos países; así un tipo mal copiado en uno solo no pasa |
| W-03 | El dominio comprueba el **rango** de usuarios, no el tipo: `calculate_quote(True, "ES")` o con un `float` no se rechaza ahí. `tax_cents` no rechaza una base o un tipo negativos | CA-04 solo pide rango y país; el tipo lo valida la API (pieza b). Un valor negativo en `tax_cents` no puede llegar desde `calculate_quote` |
| W-04 | El código de país distingue mayúsculas: `"es"` no tiene tipo y da `TaxRateNotDefinedError` | SPEC-02 no habla de normalizar; el país llega de la base de datos, y cómo se guarda lo decide SPEC-01 |
| W-05 | E-05 tiene un test propio: el impuesto de 2^53 + 1 céntimos al 100 % es exacto, cosa que un `float` no puede dar | El requisito lo comprueba sobre todo el oráculo (CA-09); el test añade un caso que falla si alguien introduce coma flotante |
| W-06 | El «100 % de ramas» de `domain/` son **2 ramas**: `coverage` no cuenta como rama la expresión condicional de `_users_in_tier` (tramo con o sin límite superior) | Los dos lados se ejecutan (tramos 1 y 2 con límite, tramo 3 sin él), pero el porcentaje no lo demuestra por sí solo |
| W-07 | Un test se retocó después del verde: el de la lista de países compara ahora ternas en vez de objetos `Country` | `ruff` (SIM300) rechazaba la forma `CONSTANTE == (…)`. Comprueba lo mismo: código, nombre y tipo de los nueve, en orden |
| W-08 | E-07, E-08 y E-11 a E-15 siguen sin test tras (a) | Son del endpoint (pieza c) o de SPEC-03 (E-08, CA-08) |
| W-09 | Los tests de (b) citan SPEC-02/E-14 y se ejecutan contra una ruta de prueba, no contra `POST /pricing/quote` | La traducción es común a todos los endpoints y el real llega en (c). Hasta entonces la trazabilidad da E-14 por probado sin que lo esté con su endpoint |
| W-10 | **Cuerpo ausente**: se responde igual que a `{}`, con un `missing` por cada campo obligatorio, leídos del contrato | El encargo pide que no salga con el formato de FastAPI, pero ni él ni la spec dicen qué errores lleva. Es la lectura más simple: sin cuerpo faltan todos los campos |
| W-11 | Una validación fallida **sin código en el contrato** (un tipo de error de Pydantic no traducido) responde `500` `internal_error` y se registra; no se inventa un código ni se deja pasar el formato de FastAPI | Es un fallo nuestro, igual que un estado HTTP fuera del contrato. Coste: si a un campo nuevo se le olvida la traducción, quien llama ve un `500` hasta que un test lo detecte |
| W-12 | **Orden de `errors`**: los campos del contrato en su orden y, después, los desconocidos en el orden de la petición | La convención dice «en el orden de los campos del contrato» y no dice dónde va un campo que no está en él |
| W-13 | El mensaje de `out_of_range` es «Debe ser menor o igual que 100000.» (o «mayor o igual que 0.»), no el «Debe estar entre 0 y 100000.» del ejemplo de las convenciones | El límite sale del propio error de Pydantic, donde es un entero exacto; el otro límite solo está en el OpenAPI, y allí es un decimal (W-14). El texto no es parte del contrato |
| W-14 | **Hallazgo, sin corregir**: el OpenAPI que genera FastAPI 0.162.0 publica los límites como decimales: `"minimum": 1.0` y `"maximum": 9.223372036854776e+18` para un identificador, cuando Pydantic da `1` y `9223372036854775807`. El máximo publicado no es el real | Afecta a CA-10 (el OpenAPI declara los campos y tipos del contrato). La validación usa los enteros exactos; solo el documento es inexacto. Corregirlo exige retocar el OpenAPI generado: **decide el Tech Lead** |
| W-15 | Una petición con un parámetro de consulta no documentado **y** un cuerpo no válido responde solo con el `unknown_field` del parámetro. Comprobado a mano; sin test | La dependencia que revisa los parámetros se ejecuta antes de validar el cuerpo. La spec no tiene esa fila |
| W-16 | Defecto propio visto en la cobertura: la rama «campo ya anotado» no se ejecutaba. Al añadir un campo de prueba con dos tipos, falló: `field` salía del último elemento de la localización de Pydantic (`int`, `bool`) y no del campo | Corregido tomando el segundo elemento (`body`, **campo**, …). Con campos de un solo tipo no se notaba |
| W-17 | Defecto propio visto al mirar una respuesta real: el primer mensaje de rango decía «entre 0.0 y 100.0», y el primer test del mensaje (`"100" in mensaje`) lo dejaba pasar. **Se sustituyó ese test** por uno que exige que el único número del mensaje sea el límite, como entero exacto | Un test se cambió, para hacerlo más estricto, no para que pasara: el nuevo se vio en rojo a las 12:28 |
| W-18 | `field` de un error de ruta o de consulta es el nombre del parámetro; para que el identificador de la ruta salga como `id`, el parámetro tendrá que llamarse `id`. Sin test: aún no hay rutas con parámetros | Lo usarán SPEC-01 y SPEC-03 |
| W-19 | `contract.py` y `validation.py` usan `Any` en los tipos de lo que dan Pydantic y el OpenAPI, con un comentario en cada función | Son documentos JSON sin tipo más estrecho |
| W-20 | Los clientes de los tests de (c) se insertan **directamente en la base de datos**; el de CA-11 tiene el país `US` | No existe todavía el alta de clientes (SPEC-01). CA-11 pide justo una inserción directa |
| W-21 | «Sin consultar la base de datos» (E-15) se prueba apartando el fichero de la base de datos: una petición con `customer_id` = 0 sigue respondiendo `422`. Una petición **válida** con la base de datos apartada responde `500` `internal_error` (visto a mano, sin test) | La spec de la proyección no define un `503`; solo `/health` lo tiene |
| W-22 | CA-06 se comprueba contando las filas de las tres tablas antes y después; no compara el contenido de las filas | Bastaría para detectar una inserción o un borrado, no una modificación. El endpoint solo ejecuta un `SELECT` |
| W-23 | El máximo de identificador (`9223372036854775807`) está como constante en `app/api/pricing.py` | Es el primer endpoint que lo usa. Cuando SPEC-01 o SPEC-03 lo necesiten, habrá que moverlo a un módulo común de `api/` |
| W-24 | El comentario de `QuoteRequest` es un comentario y no un docstring | FastAPI publica el docstring de un modelo como `description` en el OpenAPI, y el código va en inglés |
| W-25 | `ActiveUsersOutOfRangeError` del dominio no tiene traducción HTTP propia: si llegara a lanzarse, saldría como `500` `internal_error` | La API valida el rango antes; que el dominio lo lance sería un fallo nuestro |
| W-26 | El `405` de `GET /pricing/quote` lleva `Allow: POST`, correcto porque la ruta solo tiene un método | El pendiente de la cabecera `Allow` sigue para la primera ruta con dos métodos (SPEC-01) |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git rev-parse --short HEAD` | Limpio, `bd930dc` |
| Hora de inicio frente a la fecha límite | `date` | 2026-11-13 10:26 +0100, posterior a las 10:00 |
| Herramientas | `uv --version`, `python --version` | uv 0.12.13, Python 3.12.0 |
| Menciones obsoletas tras los puntos 1 y 2 | `grep` de «pendiente de confirmar», «en `borrador`» y «sin respuesta (con» en `00-analisis/` y `01-specs/` | Solo queda la definición del estado en la tabla de estados de `supuestos.md` |
| Oráculo tras los puntos 1 y 2 | `uv run scripts/check.py` (10:43) | Código de salida 0: 11 correctas, 0 con fallo y 12 inactivas (ocho del backend y cuatro del frontend). Las tres comprobaciones de specs, en verde con el bloque backend aprobado |
| Dependencias declaradas por `fastapi` 0.162.5 y por `starlette` 1.10.0, y ficha de `httpx2` | API JSON de PyPI con `curl`, sin datos del proyecto | Ver V-01 y V-02 |
| Finales de línea de `uv.lock` | Recuento de bytes con Python | 497 LF, ningún CRLF |
| Test de humo en rojo | `uv run pytest` antes de crear `app/` (10:46) | Código 2, `ModuleNotFoundError: No module named 'app'` |
| Herramientas del backend, una a una | `uv run pytest --cov=app --cov-branch --cov-fail-under=90`, `coverage report --include=app/domain/* --fail-under=100`, `ruff check .`, `ruff format --check .`, `mypy --strict .` (10:46) | Todas con código 0: `1 passed, 1 warning`; cobertura total del 100 % (4 sentencias, 0 ramas); `10 files already formatted`; `no issues found in 10 source files` |
| Oráculo con el esqueleto | `uv run scripts/check.py` (10:56) | Código de salida 0: **19 correctas, 0 con fallo y 4 inactivas** (las del frontend). La trazabilidad anota 82 requisitos del backend sin test; solo SPEC-03/E-18 tiene uno |
| Ficheros ignorados en `backend/` | `git status --short --ignored backend` | Solo `.venv/`, `.coverage` y las cachés de pytest, mypy, ruff y Python |
| Arranque real | `uv run uvicorn --factory app.main:create_app --port 8765` y `curl` (10:57) | `200` con `{"openapi":"3.1.0","info":{"title":"SaaS-O-Matic API","version":"0.1.0"},"paths":{}}`; tras parar el proceso, el puerto no responde |

## 5. No verificado

- Que no haya llegado respuesta a la consulta de A2 a A5: lo afirma el Tech
  Lead.
- Que el hook pidiera confirmación en las siete ediciones que escribían
  «aprobada»: la IA no ve el diálogo.
- El hook sobre `Edit` en `backend/`: el camino permitido solo se ha probado
  con `Write`.
- Las versiones fijadas: la IA no conoce de antemano ninguna de ellas (son
  posteriores a lo que sabe) ni ha leído sus notas de cambios. Solo ha
  comprobado que se resuelven, se instalan y pasan el test de humo.
- El código y la licencia de las 33 dependencias, y qué es exactamente
  `httpx2` más allá de su ficha en PyPI.
- El comportamiento real de `python-stdnum` con el CIF (CA-19): está
  instalado, pero no se ha ejecutado nada con él.
- ~~Que `uv run` no vuelva a resolver por su cuenta~~: el oráculo usa
  `uv run --locked` desde `203d602`, comprobado con un `pyproject.toml`
  desfasado a propósito.
- El arranque real con `uvicorn` después del paso 1: solo se comprobó tras
  el esqueleto. La creación del esquema al arrancar está probada con el
  cliente de test.
- Las filas de SPEC-03 5.6 y 5.7 con los endpoints reales: están probadas
  con rutas de prueba.
- El comportamiento de CORS en un navegador de verdad.
- Que la comprobación de ramas del oráculo lea bien un informe real con
  ramas sin cubrir: con el código actual todas están cubiertas (14 de 14);
  los casos por debajo del umbral solo se han probado con informes
  simulados.
- Nada fuera de Windows.
- `POST /pricing/quote` con un servidor real (`uvicorn`) y con un cliente
  dado de alta por la API: solo se ha probado con el cliente de test y con
  clientes insertados directamente (W-20).
- Las tablas `STRICT` con un SQLite anterior a 3.37.0 o distinto del 3.42.0
  del entorno (P-04).
- La conversión sin pérdida de `STRICT` (`15.0` y `'15'`): vista a mano, sin
  test (P-02).
- Un parámetro de consulta no documentado junto a un cuerpo no válido, y una
  petición válida con la base de datos apartada: vistos a mano, sin test
  (W-15, W-21).
- SPEC-02/E-08 y CA-08 (misma función para la proyección y para la
  simulación guardada): no puede comprobarse hasta que exista
  `POST /simulations`.
- Que `calculate_quote` no cambie nada guardado se comprueba contando filas,
  no comparando su contenido (W-22).

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Revisar versiones y estructura del esqueleto; aprobar o cambiar K-01 a K-09~~ | Hecho a las 11:10: aprobados |
| ~~Decidir V-01, V-02 y V-03~~ | Decididos a las 11:10 (f1 a f3) |
| ~~Aprobar o cambiar S-01 a S-06; confirmar S-06~~ | Aprobados y confirmado a las 11:10 (f5) |
| ~~Corregir la nota «Sobre CA-09» de SPEC-02 y el apartado «Estado» de `ai-workspace/README.md`~~ | Hecho (f7) |
| **SPEC-03/E-18 no está cubierto**: la trazabilidad lo da por probado porque el test de humo lo cita, pero falta el test de CA-09 (`405` en `PUT`, `PATCH` y `DELETE` y datos sin cambios) | Con SPEC-03 (decisión f4) |
| Aprobar o cambiar T-01 a T-08 | A decidir por el Tech Lead |
| Fijar en npm el margen de una semana de ADR-007 y comprobar la fecha de Angular CLI 21.2.29 | Al crear el frontend |
| ~~Resto del paso 1: errores genéricos, CORS, `GET /health` y `schema.sql` con su enlace desde el índice de arquitectura~~ | Hecho entre las 11:27 y las 11:42 |
| ~~**Revisar el paso 1** y aprobar o cambiar G-01 a G-09, C-01 a C-04, H-01 a H-06 y Q-01 a Q-05~~ | Hecho a las 12:02: aprobado con cinco correcciones (p1 a p5), hechas entre las 12:11 y las 12:20 |
| Aprobar o cambiar P-01 a P-08 (precisiones de p4 y p5) | A decidir por el Tech Lead |
| **Base de datos creada antes de `9ec6866`**: sigue sin `STRICT`; hay que borrar el fichero (P-03) | Quien ya haya arrancado el backend |
| **El cuerpo de la petición no tiene límite de tamaño**: limitación conocida | A documentar en el README (decisión del Tech Lead, 12:02) |
| Reproducir las filas de SPEC-03 5.6 y 5.7 con los endpoints reales (CA-15 y CA-17); hoy están probadas con rutas de prueba | Con SPEC-02, SPEC-01 y SPEC-03, según exista cada endpoint |
| ~~Traducir los errores de validación del cuerpo~~ y de la ruta a códigos por campo (`missing`, `not_an_integer`, `out_of_range`…) | Cuerpo: hecho en `49e3d65`. Ruta: con la primera ruta con parámetro (SPEC-01), ver W-18 |
| **Revisar SPEC-02** y aprobar o cambiar W-01 a W-26 | Ahora, por el Tech Lead, antes de SPEC-01 |
| **Decidir W-14**: el OpenAPI publica los límites como decimales (`9.223372036854776e+18` como máximo de un identificador); afecta a CA-10 | A decidir por el Tech Lead |
| Decidir W-10 (cuerpo ausente igual que `{}`), W-11 (validación sin código, `500`) y W-12 (campos desconocidos al final) | A decidir por el Tech Lead: son reglas que la spec no dice |
| La nota «Sobre CA-09» de SPEC-02 dice que el criterio no puede darse por cumplido hasta que exista el cálculo: ya existe y `domain/` está al 100 % | Cambio de una spec aprobada: lo decide el Tech Lead |
| SPEC-02/E-08 y CA-08 | Con SPEC-03 |
| Mover el máximo de identificador a un módulo común de `api/` (W-23) | Con SPEC-01 o SPEC-03 |
| ~~Prueba de arranque real con `uvicorn` tras el paso 1 (la orden fue denegada)~~ | Hecha por el Tech Lead (lo afirma él; la IA no la ha visto) |
| ~~Decidir si se corrige~~ **Corregir la cabecera `Allow` del `405`**, que solo nombra un método cuando la ruta admite dos | Con la primera ruta que tenga dos métodos, en SPEC-01 (decisión del Tech Lead, 12:02) |
| Documentar la estructura del backend en `02-arquitectura/README.md` | Tras la revisión de la estructura |
| Comprobar el comportamiento real de `python-stdnum` (CA-19) | Con SPEC-01, o antes si el Tech Lead lo pide |
| Pendientes heredados de la sesión 03: precisiones de `CLAUDE.md` y `backend.md` del commit `ca1c81a`; hueco del hook si su comando no arranca; aprobación literal del cambio de A10 | A decidir por el Tech Lead |
| Aprobar SPEC-04 | Antes de empezar el frontend |
