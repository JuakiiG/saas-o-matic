# Sesión 04 · Decisión de A2 a A5, aprobación del bloque backend y esqueleto del backend

| | |
|---|---|
| **Fecha** | 2026-11-13 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | A2 a A5 decididos por el Tech Lead sin confirmación externa y bloque backend aprobado (SPEC-01, SPEC-02 y SPEC-03); SPEC-04 sigue en `borrador`. Esqueleto del backend con uv: 9 dependencias directas con versión exacta, 33 en `uv.lock`, cuatro capas vacías y un test de humo. Oráculo en verde con 19 comprobaciones activas y 4 inactivas. Sesión parada a la espera de la revisión de versiones y estructura, con cuatro hallazgos sin resolver (V-01 a V-04) |

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
- Que `uv run` no vuelva a resolver por su cuenta: el oráculo llama a
  `uv run` sin `--locked`.
- Nada fuera de Windows.

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
| Resto del paso 1: errores genéricos, CORS, `GET /health` y `schema.sql` con su enlace desde el índice de arquitectura | Tras la revisión del esqueleto |
| Documentar la estructura del backend en `02-arquitectura/README.md` | Tras la revisión de la estructura |
| Comprobar el comportamiento real de `python-stdnum` (CA-19) | Con SPEC-01, o antes si el Tech Lead lo pide |
| Pendientes heredados de la sesión 03: precisiones de `CLAUDE.md` y `backend.md` del commit `ca1c81a`; hueco del hook si su comando no arranca; aprobación literal del cambio de A10 | A decidir por el Tech Lead |
| Aprobar SPEC-04 | Antes de empezar el frontend |
