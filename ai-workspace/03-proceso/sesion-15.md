# Sesión 15 · La organización de carpetas, documentada

| | |
|---|---|
| **Fecha** | 2026-11-17 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | Sesión abierta a las 13:51. En curso |

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

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short`, `git log -12` y `git branch -vv` (13:51:13 y 13:51:28) | `baa1480`; solo `sesion-14.txt`, sin versionar; `main` y `origin/main`, en el mismo commit |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000 y 4200 (13:51:28) | Ninguno en escucha |
| La base local del Tech Lead | Listado de `backend/data/` (13:51:28) | 28.672 bytes, 2026-11-14 18:37 |

## 5. No verificado

Se rellena al llegar a la parada 1.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| Paso 1: `sesion-14.txt` y el índice al día | En curso |
| Paso 2: «Organización de carpetas» en `02-arquitectura/README.md` | Después |
| Paso 3: el «Estado» de `ai-workspace/README.md` | Después |
