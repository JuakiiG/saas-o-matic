# Sesión 10 · Cierre tras la pasada manual

| | |
|---|---|
| **Fecha** | 2026-11-16 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | **Parada 1 alcanzada (14:18): los tres cambios, hechos, cada uno en su commit y con el oráculo en código 0 antes; con `--e2e` el que toca `frontend/`.** No ha cambiado el código de la aplicación: en `backend/` y `frontend/` solo hay dos `.spec.ts` con tests nuevos. **Cambio 1** (`dd4d58d`): el guion de pruebas manuales con los resultados del Tech Lead, intactos, y tres retoques en el texto. **Cambio 2** (`2a422a9`): tres tests de los dos «Reintentar», uno en el detalle y dos en el simulador; **nacen en verde y a cada uno lo mata su mutación, solo a él (1 de 569 las tres veces)**, deshechas; SPEC-04 gana dos filas en 5.5 y su fila de historial. **Cambio 3** (`27213b6`): la matriz regenerada (sigue en 140 de 140), las cifras de los dos README y el guion como ejecutado en el «Estado». El frontend acaba con **569 tests unitarios** (eran 566) y 18 de Playwright; el backend, con 741; los scripts, con 96. **Lo que el Tech Lead tiene que conocer**: (1) la sesión tiene cinco commits y no cuatro: la IA hizo uno de apertura de la bitácora, como en la sesión 09 (AI-01); (2) **que el segundo «Reintentar» no vuelve a pedir `/meta` no lo demuestra ninguna mutación** (AI-02); (3) el detalle no tiene tabla de casos en SPEC-04 y **CA-07 no se ha tocado** (AI-03); (4) las filas de la cronología de los tres cambios se escribieron al cerrar, no en cada momento (AI-06). Quedan sin aprobar AI-01 a AI-07. La integración continua sigue sin ejecutarse: la prueba en limpio y el `push` son del Tech Lead. · Antes, sesión abierta a las 14:02 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

**La conversación es nueva**, sin el contexto de la sesión 09: la IA llega
con lo que ha leído al empezar (`CLAUDE.md`, los pendientes de la bitácora
de la sesión 09 y `04-calidad/pruebas-manuales.md`, con los resultados del
Tech Lead sin commit) y con sus cuatro notas de memoria, no con lo que hizo
ayer.

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 10: cierre tras la pasada manual. Antes de nada, leer `CLAUDE.md`,
> los pendientes de `03-proceso/sesion-09.md` y
> `04-calidad/pruebas-manuales.md`. Abrir esta bitácora con el mismo
> formato que las anteriores.
>
> Parada 2 de la sesión 09 aprobada. Admitidas AH-01 a AH-06.
>
> El Tech Lead ha ejecutado el guion de pruebas manuales hoy, 16/11, de
> 12:39 a 13:55, sobre `06a6314`, en Chrome 157 y Windows 11, con una base
> de datos nueva. Los 30 pasos, OK. Sus resultados están escritos en
> `pruebas-manuales.md`, sin commit. No cambiar la columna «Resultado» ni
> la tabla de cabecera. Lo que vio, para la bitácora:
>
> - Paso 5: el anillo azul se distingue sobre el botón «Guardar». El
>   pendiente AE-06 de la sesión 08 queda cerrado.
> - Paso 17: con el tipo 1,1054, la base y el impuesto suman 187,26 USD y
>   el total dice 187,25 USD. Es lo esperado.
> - Paso 22: hacen falta las dos pulsaciones y lo ve aceptable. El
>   comportamiento se queda como está.
> - Paso 24: tras abrir `/clientes/%31`, la barra de direcciones queda en
>   `/clientes/1`.
> - Pasos 29 y 30: tras Ctrl+C a mitad de `npm run e2e`, los puertos 8000
>   y 4200 libres, ninguna carpeta temporal y la base de datos sin tocar.
>   El pendiente del Ctrl+C queda cerrado.
>
> Tres cambios, un commit cada uno, con el oráculo en verde por su código
> de salida; con `--e2e` donde se toque `frontend/`.
>
> **1. El guion.** Commit de `pruebas-manuales.md` con los resultados del
> Tech Lead tal como están. Tres retoques de la IA en el texto, sin tocar
> los resultados: la introducción dice «unos 15 minutos» y la pasada llevó
> 75, con pausas: poner una cifra honrada; las órdenes del paso 30 dicen
> que se lanzan desde la raíz del repositorio (la tercera usa una ruta
> relativa y desde `frontend/` falla); y el apartado final dice que la IA
> no lo ha ejecutado en un navegador: sigue siendo cierto, y se añade que
> lo ejecutó el Tech Lead el 16/11, con los 30 pasos en OK.
>
> **2. Los dos «Reintentar» en el detalle y en el simulador.** Añadir los
> tres tests que hoy solo dice la spec (2.1): el cliente en el detalle, el
> cliente en el simulador y la primera proyección en el simulador. Nacen
> en verde: cada uno con su mutación, deshecha y anotada. Si SPEC-04
> necesita una fila en sus tablas para ellos, con historial.
>
> **3. Puesta al día.** Regenerar la matriz de trazabilidad. Corregir las
> cifras de tests en `README.md` y en `ai-workspace/README.md`. En el
> «Estado» de `ai-workspace/README.md`, el guion pasa de pendiente a
> ejecutado, con su fecha y su resultado. La integración continua y el
> clon limpio siguen pendientes.
>
> **Parar ahí (parada 1)** y cerrar la bitácora de la sesión 10: qué
> cambió, qué mutación mató cada test nuevo, cuántos tests hay y qué no se
> ha podido comprobar. La prueba en limpio y el `push` los hace el Tech
> Lead.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 14:05 | — | Mensaje recibido a las 14:02 (primera lectura del reloj, 14:02:35). El último commit es `06a6314` (2026-11-15 17:57:50), el último de la sesión 09. **`git status`: un solo fichero cambiado y sin commit, `04-calidad/pruebas-manuales.md`**, con los resultados del Tech Lead; su `git diff` toca las cinco filas de la tabla de cabecera y la columna «Resultado» de los 30 pasos, y nada más (35 líneas). **`netstat` a las 14:02:59: nada escucha en el 8000, el 4200, el 8011 ni el 4211.** `backend/data/saas-o-matic.db`, del Tech Lead: 28.672 bytes, 2026-11-14 18:37; la IA no lo toca. Lecturas del encargo hechas, y además SPEC-04 (2.1, 2.4, 2.5, 5.3, 5.5, 5.6, los criterios y el historial), `detalle.spec.ts`, `simulador.spec.ts`, el test del panel de la sesión 09, `detalle.ts`, `simulador.ts`, `projector.ts`, `meta-gate.ts`, `customer-loader.ts`, `meta-store.ts`, los dos README y la cabecera de `trazabilidad.md`. Apertura de esta bitácora |
| 14:18 | `9e8a650` | **Apertura de la bitácora**, 14:07:35 según `git log`, tras el oráculo sin `--e2e` de 14:06:01 a 14:07:35, código 0 (23 correctas, 1 inactiva); la salida, a un fichero, y el commit, en la misma orden, solo con ese código. Solo entra `sesion-10.md`: el guion sigue sin commit. El encargo no nombraba este commit (AI-01) |
| 14:18 | `dd4d58d` | **Cambio 1 (el guion)**, 14:09:33 según `git log`. Tres retoques con la herramienta de edición, fuera de las tablas: la introducción dice «en algo más de una hora: la pasada del 16/11/2026 llevó 75 minutos, con pausas»; el párrafo de las órdenes del paso 30 dice que se lanzan desde la raíz del repositorio y por qué; y el apartado final añade que lo ejecutó el Tech Lead el 16/11/2026, sobre `06a6314`, con los 30 pasos en OK. A las 14:07:53: la ruta relativa de la tercera orden existe desde la raíz y no desde `frontend/` (visto con la orden de Linux en Git Bash, no con la de PowerShell), y el `git diff` contra `06a6314` sigue teniendo las mismas 35 filas de tabla que antes de los retoques (AI-04). Antes del commit, oráculo sin `--e2e` de 14:08:07 a 14:09:33, código 0 |
| 14:18 | — | **Cambio 2, los tests.** Copia de `detalle.ts`, `detalle.spec.ts`, `simulador.ts` y `simulador.spec.ts` fuera del repositorio (14:09:57). Un test nuevo en `detalle.spec.ts` y dos en `simulador.spec.ts`, en el bloque «/meta en error». En los tres, `/meta` falla con un `500` y la otra petición con un `503`, para distinguir un aviso del otro. **Nacen en verde** (14:10:19; 127 tests en los dos ficheros) |
| 14:18 | — | **Cambio 2, las mutaciones**, cada una con los 569 tests y en el código de la vista, con la herramienta de edición. **Detalle** (14:10:50): al recuperarse `/meta` de un error, la vista repite la petición del cliente que había fallado; **1 fallo y 568 en verde, el test nuevo**, por aserción («expected 1 to be 0» en las peticiones del cliente). **Simulador, el cliente** (14:11:30): lo mismo; **1 fallo y 568 en verde, su test**, por la misma aserción. **Simulador, la proyección** (14:11:52): al recuperarse `/meta`, la vista repite la proyección que había fallado; **1 fallo y 568 en verde, su test** («expected 1 to be 0» en las peticiones de proyección). Deshechas: `detalle.ts` y `simulador.ts`, idénticos byte a byte a su copia (14:12:03), y los 569 tests, en verde (14:12:15). Ningún intento descartado (AI-02) |
| 14:18 | — | **Cambio 2, SPEC-04**: dos filas en 5.5, las de `/meta` fallando a la vez que el cliente y a la vez que la primera proyección; una remisión a ellas en 2.1; y su fila de historial, con fecha de hoy. El detalle no tiene tabla de casos y CA-07 no se toca (AI-03) |
| 14:18 | `2a422a9` | **Cambio 2**, 14:14:47 según `git log`: `detalle.spec.ts`, `simulador.spec.ts` y SPEC-04. Antes, `netstat` a las 14:12:52: nada en el 8000 ni en el 4200; oráculo con `--e2e` de 14:13:04 a 14:14:47, código 0: **24 correctas, 0 con fallo y 0 inactivas**. Después, puertos libres, ninguna carpeta `saas-o-matic-e2e-*` y `backend/data/saas-o-matic.db` igual. **Es la única pasada con `--e2e` de la sesión y el único commit que toca `frontend/`** |
| 14:18 | — | **Cambio 3, la matriz y las cifras.** `uv run scripts/traceability.py` a las 14:15:03, sobre `2a422a9`, dos veces: idénticas. Sustituye al apartado 4 de `trazabilidad.md`; respecto de la anterior cambian 9 líneas: 253 declaraciones del frontend (eran 250) y siete requisitos con más tests, E-40 con 106 (eran 103). **Sigue en 140 de 140.** Cabecera y apartados 1 y 2, al día. Cifras de hoy de los *runners* (14:12:15 y 14:15:05): 569, 741 y 18 más 4 capturas; los 96 de los scripts, de la salida del oráculo. `README.md`: la fecha y «569 del frontend». `ai-workspace/README.md`: la fecha, la cifra y, en «Estado», el guion pasa de pendiente a ejecutado, con una frase que el encargo no pedía (AI-05) |
| 14:18 | `27213b6` | **Cambio 3**, 14:17:35 según `git log`: `trazabilidad.md` y los dos README. Antes, oráculo sin `--e2e` de 14:16:08 a 14:17:35, código 0: 23 correctas y 1 inactiva |
| 14:18 | *(este commit)* | **Cierre de esta bitácora para la parada 1.** Las ocho filas anteriores se han escrito ahora, a las 14:18, con las horas de las salidas guardadas, no en el momento de cada una (AI-06). La IA para aquí: el Tech Lead revisa los tres cambios y las precisiones AI-01 a AI-07. La prueba en limpio y el `push` son suyos. La hora de este commit se ve con `git log` |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (14:02)

**Parada 2 de la sesión 09, aprobada. Admitidas AH-01 a AH-06**, sin
comentario. La bitácora de la sesión 09 no se toca: la aprobación queda
anotada aquí.

**El guion de pruebas manuales, ejecutado por el Tech Lead** (lo afirma él;
la IA no estaba): el 16/11/2026, de 12:39 a 13:55, sobre `06a6314`, en
Google Chrome 157 y Windows 11, con una base de datos nueva. **Los 30
pasos, OK.** Lo que vio:

| Paso | Qué vio el Tech Lead | Qué cierra o decide |
|---|---|---|
| 5 | El anillo azul se distingue sobre el botón «Guardar» | **Cerrado el pendiente AE-06 de la sesión 08** |
| 17 | Con el tipo 1,1054, la base y el impuesto suman 187,26 USD y el total dice 187,25 USD | Es lo esperado: el céntimo de SPEC-04, 2.6 y 5.1 |
| 22 | Hacen falta las dos pulsaciones de «Reintentar» | **Lo ve aceptable: el comportamiento se queda como está** |
| 24 | Tras abrir `/clientes/%31`, la barra de direcciones queda en `/clientes/1` | Visto por primera vez en un navegador |
| 29 y 30 | Tras Ctrl+C a mitad de `npm run e2e`: los puertos 8000 y 4200, libres; ninguna carpeta temporal; la base de datos, sin tocar | **Cerrado el pendiente del Ctrl+C de la sesión 08** |

**Reglas de esta sesión**, del encargo:

- **Tres cambios, un commit cada uno**, con el oráculo en verde por su
  código de salida; con `--e2e` donde se toque `frontend/`.
- **La columna «Resultado» y la tabla de cabecera del guion no se tocan.**
- **La prueba en limpio y el `push` son del Tech Lead.**

### Los tres cambios · lo hecho

| # | Commit | Rojo visto o mutación | Qué toca |
|---|---|---|---|
| 1 · El guion | `dd4d58d` | — | `04-calidad/pruebas-manuales.md`: los resultados del Tech Lead, tal como estaban, y tres retoques en el texto |
| 2 · Los dos «Reintentar» | `2a422a9` | **Mutación**, tres, una por test; cada una la mata **solo su test** (1 de 569) | `detalle.spec.ts`, `simulador.spec.ts` y SPEC-04 (2.1, 5.5 e historial) |
| 3 · Puesta al día | `27213b6` | — | `04-calidad/trazabilidad.md`, `README.md` y `ai-workspace/README.md` |

**Los tres tests nuevos y la mutación que mata cada uno** (cambio 2). Los
tres nacen en verde, porque el comportamiento ya estaba:

| Test | Qué fija | Mutación | Resultado, con los 569 tests |
|---|---|---|---|
| `detalle.spec.ts`: «should show the notice of the customer, with its own retry, when the customer failed too and the retry of /meta succeeds» | `/meta` y el cliente fallan. Tras «Reintentar» de `/meta` con éxito: 1 petición a `/meta`, ninguna del cliente, sin tarjeta y un solo aviso, el del cliente, con su «Reintentar». Al pulsarlo: ninguna a `/meta`, 1 a `/customers/1`, y el detalle con «España» y sin aviso | En `detalle.ts`: cuando `/meta` pasa de error a datos, la vista repite la petición del cliente si había fallado | **1 fallo, 568 en verde** (14:10:50): este test, «expected 1 to be 0» en las peticiones del cliente |
| `simulador.spec.ts`: el mismo título, en el bloque «/meta en error» | Lo mismo en el simulador: ninguna petición del cliente ni de proyección, sin formulario y un solo aviso. Al pulsarlo: ninguna a `/meta`, 1 a `/customers/7` y, al llegar, 1 de proyección con 10 usuarios; «Ejemplo Uno SL · España» y total 121,00 EUR | En `simulador.ts`: la misma, con el cliente | **1 fallo, 568 en verde** (14:11:30): este test, por la misma aserción |
| `simulador.spec.ts`: «should show the notice of the projection, with its own retry, when the first projection failed too and the retry of /meta succeeds» | El cliente llega y fallan `/meta` y la primera proyección. Tras «Reintentar» de `/meta`: ninguna petición, el simulador con «España», sin importes, con el aviso de la proyección y «Guardar» desactivado. Al pulsar su «Reintentar»: ninguna a `/meta` ni del cliente, 1 de proyección con 10 usuarios; total 121,00 EUR, sin aviso y «Guardar» activo | En `simulador.ts`: cuando `/meta` pasa de error a datos, la vista repite la proyección si había fallado | **1 fallo, 568 en verde** (14:11:52): este test, «expected 1 to be 0» en las peticiones de proyección |

Las tres mutaciones están deshechas: `detalle.ts` y `simulador.ts` son
idénticos, byte a byte, a la copia hecha antes de tocarlos.

**Tests al cerrar**, de salidas de hoy:

| Grupo | Tests | De dónde sale |
|---|---|---|
| Backend | 741 | `uv run --locked pytest --collect-only -q` (14:15:05) |
| Frontend | **569** (eran 566: uno más en el detalle y dos en el simulador) | `npx ng test --watch=false` (14:12:15) |
| Playwright | 18 pruebas en 5 ficheros, más las 4 capturas | `npx playwright test --list`, con cada configuración (14:15:10) |
| Scripts | 96 | Salida del oráculo (14:17:35) |

Precisiones de la IA, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| AI-01 | **La sesión tiene cinco commits, no cuatro**: además de los tres cambios y de este cierre, la IA hizo uno de apertura de la bitácora (`9e8a650`), con su pasada del oráculo. El encargo no lo nombraba | Es lo que se hizo en la sesión 09 (`f2379c4`), y el encargo pedía abrir la bitácora como las anteriores. Así el commit del guion lleva solo el guion |
| AI-02 | **Cada mutación es la del comportamiento que el Tech Lead ha decidido no tener** (que reintentar `/meta` repita también lo que falló), puesta en el código de la vista y solo para la petición que había fallado. Ningún intento descartado. **Lo que ninguna mutación demuestra**: que el segundo «Reintentar» no vuelve a pedir `/meta`. Los tres tests lo comprueban («ninguna a `/meta`»), pero la IA no ha probado a romperlo: leyendo `meta-store.ts`, su `retry()` no pide nada si `/meta` no está en error, así que la mutación directa (que el «Reintentar» del cliente llame también al de `/meta`) no cambiaría nada. Tampoco se ha visto qué habría roto la mutación sin la condición «si había fallado» | Una mutación por test es lo que pedía el encargo. La condición evita el caso de AH-01 de la sesión 09: sin ella, por lo que dice el código, caería también el test que ya existía en el simulador («appear loaded when /meta comes back»), y no se sabría qué mata el nuevo |
| AI-03 | **En SPEC-04 solo el simulador gana filas** (dos, en 5.5, con CA-08, que pide un test por cada fila de 5.5) y 2.1 remite a ellas. **El detalle no tiene tabla de casos**: lo suyo está en CA-07, que es una lista en un criterio y no nombra este caso. **CA-07 no se ha tocado.** Los tres tests no citan un requisito en su título: heredan los de su bloque (E-40 entre ellos) y su comentario nombra 2.1 y, en el simulador, 5.5 | El encargo hablaba de una fila en las tablas; cambiar la redacción de un criterio es otra cosa y lo decide el Tech Lead. Si lo quiere, es una frase en CA-07 («y `/meta` y el cliente en error a la vez») |
| AI-04 | **En el guion, solo los tres retoques.** La IA no guardó una copia del fichero del Tech Lead antes de editarlo: que sus resultados siguen intactos sale de que el `git diff` contra `06a6314` tiene las mismas 35 filas de tabla antes y después, y de que los tres retoques caen fuera de las tablas. De 12:39 a 13:55 van 76 minutos; el texto dice 75, la cifra del Tech Lead. La frase «la columna «Resultado» se deja vacía hasta entonces» de la introducción se queda como estaba | El encargo mandaba no tocar los resultados ni la tabla de cabecera; el Tech Lead tiene que saber con qué se ha comprobado |
| AI-05 | **En el «Estado» de `ai-workspace/README.md` hay una frase que el encargo no pedía**: que los tres tests añadidos después de la pasada manual no cambian el código de la aplicación. Comprobado: entre `06a6314` y el último commit, en `backend/` y `frontend/` solo cambian `detalle.spec.ts` y `simulador.spec.ts`. En el README de la raíz solo cambian la fecha y la cifra; «solo se ha probado en Windows 11» se queda | La pasada manual es sobre `06a6314` y el estado se escribe tres commits después: sin esa frase no se sabe si los 30 pasos valen para lo que hay ahora |
| AI-06 | **Las filas de la cronología de los tres cambios se escribieron al cerrar** (14:18), todas a la vez, con las horas de las salidas guardadas en la carpeta de trabajo de la sesión; no cada una en su momento. La de apertura sí se escribió al abrir | La regla 6 pide la bitácora al momento. Entre la fila de apertura (14:05) y el cierre (14:18) pasaron trece minutos y la IA encadenó los tres cambios sin parar a anotar. Las horas no son estimadas, pero el orden de escritura no fue el de la regla |
| AI-07 | **Una búsqueda de la IA enseñó tres líneas de `.private/COORDINACION.md`**: buscaba «566» y «sin ejecutar» en todos los `.md` del repositorio, para no dejar cifras antiguas, y no excluyó esa carpeta. No lo ha abierto ni lo ha tocado, y nada de esas líneas se ha usado | `.private/` no está versionado y no es de la IA. El Tech Lead tiene que saber que se ha visto |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git log -1` (14:02:35) | `06a6314`; cambiado y sin commit, solo `04-calidad/pruebas-manuales.md` |
| Qué cambia en el guion sin commit | `git diff` del fichero (14:02:59) | 35 líneas: las cinco filas de la tabla de cabecera y las 30 filas de pasos, en las que solo cambia la última celda |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000, 4200, 8011 y 4211 (14:02:59) | Ninguno en escucha |
| La base local del Tech Lead | Listado de `backend/data/` (14:02:59) | 28.672 bytes, 2026-11-14 18:37 |

Cambio 1:

| Qué | Cómo | Resultado |
|---|---|---|
| La ruta relativa del paso 30 | `ls -l backend/data/saas-o-matic.db` en Git Bash, desde la raíz y desde `frontend/` (14:07:53) | Desde la raíz, el fichero; desde `frontend/`, «No such file or directory», código 2 |
| Los resultados, intactos | `git diff -U0 06a6314` del guion: las líneas que no son filas de tabla, y el recuento de las que sí (14:07:53) | Fuera de las tablas, solo los tres retoques; 35 filas de tabla cambiadas, las mismas que antes de editarlo |

Cambio 2:

| Qué | Cómo | Resultado |
|---|---|---|
| Los tres tests, en verde | `npx ng test --watch=false --include` de `detalle.spec.ts` y de `simulador.spec.ts` (14:10:19) | 127 en verde |
| Formato y lint de los dos ficheros | `npx prettier --check` (14:10:11) y `npx eslint --max-warnings 0` (14:12:15) | Código 0 los dos |
| **Mutación del detalle** | `npx ng test --watch=false`, los 569 tests (14:10:50) | **1 fallo y 568 en verde**: el test nuevo, por aserción, en `detalle.spec.ts:436` |
| **Mutación del cliente en el simulador** | Lo mismo (14:11:30) | **1 fallo y 568 en verde**: su test, en `simulador.spec.ts:1033` |
| **Mutación de la proyección en el simulador** | Lo mismo (14:11:52) | **1 fallo y 568 en verde**: su test, en `simulador.spec.ts:1063` |
| Las mutaciones están deshechas | `cmp` de `detalle.ts` y de `simulador.ts` con su copia de antes, `git status --short` y una búsqueda de `MUTATION` en `frontend/src` (14:11:04 y 14:12:03) | Idénticos los dos; cambiados, solo los dos `.spec.ts`; ninguna coincidencia |
| Todos los tests, sin mutación | `npx ng test --watch=false` (14:12:15) | 569 en verde, en 19 ficheros |
| El salto de línea final | Los últimos bytes de `simulador.spec.ts` y de SPEC-04, que se editaron por el final (14:10:11 y 14:12:52) | Los dos acaban en salto de línea |
| Puertos antes de la pasada con `--e2e` | `netstat` filtrado por `LISTENING` y los puertos 8000 y 4200 (14:12:52) | Ninguno en escucha |

Cambio 3:

| Qué | Cómo | Resultado |
|---|---|---|
| La matriz | `uv run scripts/traceability.py`, dos veces, y `cmp` entre ellas (14:15:03) | Código 0 las dos; idénticas; 183 líneas |
| Qué cambia respecto de la anterior | `diff` con el apartado 4 que había en el documento (14:15:03) | 9 líneas: el frontend, de 250 a 253 declaraciones; E-12, E-13, E-14, E-15, E-35 y E-47, uno más; E-38, dos más; E-40, de 103 a 106 |
| El apartado 4 es la salida de la orden | `cmp` de lo que hay bajo el marcador del documento con la salida, tras escribirlo y tras poner al día la cabecera (14:15:58) | Idénticos |
| Cifras de los *runners* | `uv run --locked pytest --collect-only -q` y `npx playwright test --list` con cada configuración (14:15:05 a 14:15:10) | 741 recogidos; 18 pruebas en 5 ficheros y 4 capturas en 1 |
| Ninguna cifra antigua | Búsqueda de «566» y de «sin ejecutar» en los `.md` (14:15:58) | Fuera de las bitácoras y de los informes de evaluación, ninguna (AI-07) |
| El código de la aplicación no ha cambiado | `git diff --stat 06a6314 -- backend frontend` (14:15:58 y, sobre el último commit, 14:18:00) | Solo `detalle.spec.ts` y `simulador.spec.ts`: 91 líneas añadidas |

Oráculo:

| Qué | Cómo | Resultado |
|---|---|---|
| **Antes de cada commit** | `uv run scripts/check.py`, con `--e2e` en el cambio 2; la salida, a un fichero, y el commit en la misma orden, solo con código 0 | Código 0 en las cuatro pasadas anteriores a este cierre: tres sin `--e2e` (23 correctas, 0 con fallo y 1 inactiva) y una con `--e2e` (24 correctas, 0 con fallo y 0 inactivas) |
| Puertos y carpeta temporal tras la pasada con `--e2e` y al cerrar | `netstat` y un listado de la carpeta temporal del sistema (14:14:47 y 14:18:00) | Ninguno en escucha y ninguna carpeta `saas-o-matic-e2e-*` |
| La base local del Tech Lead | Listado de `backend/data/` al empezar, tras la pasada con `--e2e` y al cerrar | Igual las tres veces: 28.672 bytes, 2026-11-14 18:37 |

## 5. No verificado

Al llegar a la parada 1:

- **La IA no ha visto nada en un navegador.** El guion lo ejecutó el Tech
  Lead; sus resultados y lo que vio constan aquí porque lo afirma él. Los
  dos «Reintentar» del detalle y del simulador se han visto en tests, no
  en pantalla: el paso 22 del guion solo recorre los del panel.
- **Que el segundo «Reintentar» no vuelve a pedir `/meta`**: los tests lo
  comprueban, pero ninguna mutación lo ha roto (AI-02).
- **Las órdenes de PowerShell del paso 30**, por la IA: lo de la ruta
  relativa se ha visto con la orden de Linux en Git Bash. Las de
  PowerShell las ejecutó el Tech Lead en su pasada.
- **Después del cambio 2 no hay pasada con `--e2e`**: los commits del
  cambio 3 y de este cierre solo tocan documentos, y su pasada del
  oráculo deja Playwright como inactivo.
- **Ningún evaluador ha mirado los cambios de esta sesión**, ni los de la
  sesión 09.
- **La integración continua no se ha ejecutado nunca**, y nada del
  proyecto se ha ejecutado fuera de Windows. **Un clon limpio**, tampoco.
- Sigue como en la sesión 09 lo que el Tech Lead dijo que comprueba él en
  la prueba en limpio: las tres frases del README de AG-08, la captura
  dibujada en el README y el oráculo sin `frontend/node_modules` (AH-06).
- **La matriz no dice qué comprueba cada test**: dice qué citan. Los tres
  tests nuevos suman a los requisitos de su bloque sin citarlos en su
  título (AI-03).
- **Nada con lector de pantalla** (L-10), como en las sesiones 08 y 09.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Cambio 1: el guion, con los resultados del Tech Lead y tres retoques~~ | Hecho (`dd4d58d`) |
| ~~Cambio 2: tres tests de los dos «Reintentar», en el detalle y en el simulador, con su mutación~~ | Hecho (`2a422a9`) |
| ~~Cambio 3: la matriz, las cifras de tests y el «Estado»~~ | Hecho (`27213b6`) |
| ~~Ejecutar el guion de pruebas manuales~~ (pendiente de la sesión 09), con ~~el anillo sobre el botón «Guardar» (AE-06)~~ y ~~la ejecución interrumpida con Ctrl+C~~ (pendientes de la sesión 08) | Hecho por el Tech Lead el 16/11/2026: los 30 pasos, en OK |
| **Parada 1: el Tech Lead revisa** los tres cambios y las precisiones AI-01 a AI-07. En particular, **si CA-07 debe nombrar el caso del detalle** (AI-03) | Ahora |
| **Prueba en limpio y `push`**. Tras el `push`, ver el primer resultado de la integración continua en Linux y en Windows y corregir lo que falle | Del Tech Lead; la corrección, en una sesión nueva |
| Poner al día `ai-workspace/README.md` («Estado») y el README de la raíz («solo se ha probado en Windows 11») cuando la integración continua y el clon limpio tengan resultado | Entonces |
| Pendientes heredados que esta sesión no toca: L-07 y los avisos de `npm audit`, los cuatro scripts de instalación sin aprobar, las fechas del fichero de bloqueo en el oráculo y los de la sesión 06 | A decidir por el Tech Lead |
