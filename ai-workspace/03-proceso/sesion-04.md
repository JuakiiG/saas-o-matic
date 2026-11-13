# Sesión 04 · Decisión de A2 a A5, aprobación del bloque backend y esqueleto del backend

| | |
|---|---|
| **Fecha** | 2026-11-13 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | *(sesión en curso; se rellena al cerrar)* |

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

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git rev-parse --short HEAD` | Limpio, `bd930dc` |
| Hora de inicio frente a la fecha límite | `date` | 2026-11-13 10:26 +0100, posterior a las 10:00 |
| Herramientas | `uv --version`, `python --version` | uv 0.12.13, Python 3.12.0 |
| Menciones obsoletas tras los puntos 1 y 2 | `grep` de «pendiente de confirmar», «en `borrador`» y «sin respuesta (con» en `00-analisis/` y `01-specs/` | Solo queda la definición del estado en la tabla de estados de `supuestos.md` |
| Oráculo tras los puntos 1 y 2 | `uv run scripts/check.py` (10:43) | Código de salida 0: 11 correctas, 0 con fallo y 12 inactivas (ocho del backend y cuatro del frontend). Las tres comprobaciones de specs, en verde con el bloque backend aprobado |

## 5. No verificado

- Que no haya llegado respuesta a la consulta de A2 a A5: lo afirma el Tech
  Lead.

## 6. Tareas pendientes

*(se rellena al cerrar)*
