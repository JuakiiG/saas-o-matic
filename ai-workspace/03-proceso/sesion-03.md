# Sesión 03 · Segunda evaluación independiente de las specs

| | |
|---|---|
| **Fecha** | 2026-11-12 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | *(sesión abierta)* |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Antes de nada, comprobar si el tipo de subagente `evaluador` aparece entre
> los tipos disponibles para la herramienta Agent y copiar literalmente la
> línea donde aparece. Si no aparece, parar y no hacer nada más.
>
> Si aparece: leer `CLAUDE.md`, `ai-workspace/README.md`,
> `01-specs/README.md` y la bitácora de la sesión 02. Abrir ya esta bitácora
> y anotar cada revisión en el momento, empezando por la comprobación del
> evaluador.
>
> Primera tarea: lanzar el subagente `evaluador` (el tipo real, no la
> alternativa) para una segunda evaluación independiente de las specs 01 a
> 04 y de los ADR 001 a 004. Encargo para él, sin ninguna conclusión de la
> IA: comprobar que los 26 hallazgos de
> `04-calidad/evaluacion-specs-01.md` están bien resueltos en los documentos
> actuales (para esta tarea sí puede leer ese fichero, pero no la respuesta
> ni la bitácora) y buscar contradicciones nuevas introducidas por las
> correcciones. Guardar su informe intacto en
> `04-calidad/evaluacion-specs-02.md`, confirmar con `git status` que el
> subagente no ha modificado nada y parar para la revisión.

## 2. Cronología

| Hora | Commit | Qué |
|---|---|---|
| 15:42 | — | Comprobación del tipo `evaluador` (apartado 3). Lectura de los cuatro documentos indicados y de `.claude/agents/evaluador.md`. `git status` limpio, `HEAD` en `fd46774`. Apertura de esta bitácora |
| 15:44 | — | Lanzado el subagente de tipo `evaluador` (el tipo real). Encargo: verificar H-01 a H-26 de `evaluacion-specs-01.md` en los documentos actuales y buscar contradicciones nuevas en las specs 01 a 04, el índice, los ADR 001 a 004, `00-analisis/`, `CLAUDE.md` y `.claude/rules/`. Sin ninguna conclusión de la IA. Autorizado a leer solo ese fichero de `04-calidad/`; prohibidos la respuesta, `03-proceso/` y el historial de git como vía para reconstruirlos. Se le avisó de que no hay código ni oráculo |
| 15:45 | — | El Tech Lead aprueba los cuatro añadidos al encargo y da por verificado el modelo del subagente (apartado 3). El evaluador sigue en ejecución |
| 15:50 | — | El evaluador termina (unos 6 minutos, 22 usos de herramientas según el aviso de la sesión). Informe guardado en `04-calidad/evaluacion-specs-02.md`: 22 hallazgos `RESUELTO`, 4 `RESUELTO EN PARTE` (H-06, H-12, H-14, H-20), 0 `NO RESUELTO`; 17 hallazgos nuevos, N-01 a N-17 (1 de severidad media, 16 baja). Comprobación con `git status` (más abajo). La IA no ha corregido nada ni ha valorado los hallazgos. Sin commit, a la espera de la revisión del Tech Lead |
| 15:55 | — | Revisión del informe por el Tech Lead: decisiones sobre N-01 a N-17 y lo pendiente de H-06 y H-13 (apartado 3) |
| 15:55 | `27b9373` | Informe del evaluador, intacto, en un commit propio. `git diff --cached` estaba vacío antes de añadirlo; sin trailer de coautoría |
| 15:56 | — | Lectura completa de las cuatro specs, `supuestos.md`, `requisitos.md`, ADR-001, ADR-003, ADR-004, el índice de arquitectura, las reglas por capa y la primera respuesta (para el formato). ADR-002 no se releyó |
| 16:01 | `710917b` | Correcciones en las cuatro specs, el índice, `supuestos.md` y `requisitos.md` |
| 16:03 | `2469bd0` | ADR-005, criterio de los ADR y apartado «Modelo de datos» en el índice de arquitectura, y nota en ADR-004 |
| 16:08 | *(este commit)* | Respuesta a la evaluación (`04-calidad/respuesta-evaluacion-specs-02.md`) y esta bitácora, que entra por primera vez en un commit |
| 16:06 | — | El commit anterior es `ef9f05c`. **Corrección de horas**: las tres filas anteriores a esta y la de las 15:56 las escribió la IA con horas estimadas, sin mirar el reloj. Las horas reales de los commits, según `git log --format=%ci`, son 16:02 (`710917b`), 16:03 (`2469bd0`) y 16:05 (`ef9f05c`), no 16:01, 16:03 y 16:08; la de la lectura (15:56) es aproximada. Las filas se dejan como se escribieron. Sin commit, a la espera de la revisión del Tech Lead |
| 16:15 | — | Revisión del Tech Lead: aprobadas P-01 a P-14 y decididas Q-01 a Q-04 (apartado 3). Relectura de ADR-002 |
| 16:17 | `5346ccb` | Decisiones Q-01, Q-02 y Q-04 en SPEC-03, SPEC-01, el índice y A14; respuesta actualizada; esta bitácora, con la fila de las horas. Hora tomada de `git log --format=%ci` |
| 16:18 | `22835b9` | ADR-006 y su fila en el índice de arquitectura. Entre `5346ccb` y este commit, el índice de specs enlazaba a un ADR-006 que aún no existía |
| 16:20 | — | Propuesta de diseño de `scripts/check.py` y del hook `PreToolUse`, presentada en la conversación, sin crear ningún fichero. Antes se leyó `.claude/settings.json` y se consultaron las versiones instaladas (uv 0.12.13, Node 24.18.0, Python 3.12.0). Sin commit, a la espera de la revisión del Tech Lead |
| 16:30 | — | Revisión del diseño por el Tech Lead (apartado 3). Lanzado un subagente de consulta de documentación (`claude-code-guide`) para contrastar el protocolo de los hooks |
| 16:33 | — | Tests del hook y del oráculo escritos y ejecutados en rojo |
| 16:38 | `5d0df9f` | Oráculo `scripts/check.py`, módulos de `scripts/oracle/`, script del hook y sus 63 tests. Oráculo en verde antes del commit. El hook aún no está registrado. Hora tomada de `git log --format=%ci` |
| 16:45 | *(este commit)* | Registro del hook en `.claude/settings.json` y esta bitácora. **La IA para aquí, sin la prueba en vivo.** La hora de esta fila es aproximada: se escribió antes de hacer el commit |

**Cómo se guardó el informe.** El subagente devuelve su informe como texto;
no escribe el fichero. La IA lo transcribió a
`04-calidad/evaluacion-specs-02.md` sin cambiar el contenido. Dos cosas que
no son del informe y no se guardaron: la sangría de dos espacios que la
sesión añade a cada línea al entregarlo, y una nota de la propia sesión,
anterior al informe, que avisa de que el texto contiene un patrón con forma
de instrucción (la mención a `.claude/settings.json` de su última línea).
Límite: es una transcripción hecha por la IA, no una copia byte a byte; la
IA no la ha cotejado contra el transcript del subagente.

**Comprobación tras el evaluador (15:50)**, con `git status --short
--untracked-files=all`, `git diff --stat`, `git diff --cached --stat` y
`git rev-parse`:

- Ningún fichero con seguimiento modificado; nada preparado en el índice.
  `HEAD` sigue en `fd46774`.
- Sin seguimiento, solo dos ficheros, los dos escritos por la IA: esta
  bitácora y `ai-workspace/04-calidad/evaluacion-specs-02.md`.
- Ninguna spec, ADR, regla ni `CLAUDE.md` aparece modificado.

Más allá de `git status` (su límite, anotado en la sesión 02, es que no ve
lo ignorado): búsqueda de ficheros del repo modificados en los últimos 15
minutos, incluidos los ignorados. Dentro de lo que git sigue, solo aparecen
los dos ficheros anteriores y dos con la hora del commit de cierre de la
sesión 02 (15:37), sin diferencias. En el directorio ignorado `.private/`
hay dos ficheros con hora de modificación de esta sesión: uno a las 15:39,
antes de lanzar el evaluador, y otro a las 15:43:50, alrededor del momento
del lanzamiento. La IA no los ha escrito ni leído y **no puede determinar
quién modificó el segundo**. No se ha comprobado nada fuera del repo.

**Añadidos de la IA al encargo, no pedidos por el Tech Lead**: la prohibición
de usar `git log`, `git show` o `git diff` para reconstruir la respuesta o la
bitácora; numerar los hallazgos nuevos como `N-xx` para no confundirlos con
los `H-xx` de la primera evaluación; los tres veredictos por hallazgo
(`RESUELTO`, `RESUELTO EN PARTE`, `NO RESUELTO`); y la petición de recalcular
los valores de las tablas de casos que pueda.

## 3. Revisiones y comprobaciones pedidas por el Tech Lead

### Disponibilidad del tipo `evaluador` (15:42)

Pedida por el Tech Lead como condición para seguir. **Resultado: aparece.**
Línea literal de la lista de tipos de agente disponibles en esta sesión:

```
- evaluador: Evaluador independiente. Usar al cerrar un bloque (backend o frontend) para comprobar el resultado contra los requisitos EARS de las specs. Solo lectura, no corrige nada. (Tools: Read, Grep, Glob, Bash)
```

Diferencia con la sesión 02: allí el tipo no figuraba y se usó un subagente
de propósito general. Aquí sus herramientas declaradas son `Read`, `Grep`,
`Glob` y `Bash`: no tiene las de edición, pero con `Bash` podría escribir en
disco, así que la comprobación con `git status` sigue siendo necesaria.

Lo que la IA no puede comprobar desde la lista: qué modelo usará el
subagente. La lista no lo muestra; `.claude/agents/evaluador.md` declara
`model: opus`.

### Encargo del evaluador y modelo del subagente (15:45)

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| x1 | Añadió cuatro cosas al encargo del evaluador sin que estuvieran pedidas (ver la nota de la cronología) y lo lanzó sin consultarlas antes, avisándolo al entregar | **Aprobadas las cuatro** | — |
| x2 | Declaró «no verificado» el modelo con el que se ejecuta el subagente | **Verificado por él**: el transcript del subagente registra el modelo `claude-opus-5-5`, así que `model: opus` funciona | — |

La comprobación de x2 es del Tech Lead; la IA no ha leído el transcript.

### Informe de la segunda evaluación · Revisión (15:55)

Mismo procedimiento que en la primera: **el informe no se toca; se responde
a cada hallazgo**. Primero un commit solo con el informe intacto; después
las correcciones, ADR-005 y un documento de respuesta
(`04-calidad/respuesta-evaluacion-specs-02.md`), en commits separados. Todas
las decisiones de esta tabla son del Tech Lead. Donde no dio motivo figura
un guion.

| # | Hallazgo | Decisión del Tech Lead | Motivo |
|---|---|---|---|
| y1 | N-01 | SPEC-01, SPEC-02 y SPEC-03 forman el **bloque backend** y se aprueban juntas. Orden de implementación: 1) lo común (errores genéricos, CORS, `/health`, esquema), 2) SPEC-02, 3) SPEC-01, 4) SPEC-03. «Depende de: SPEC-03» en SPEC-01; el bloque y el orden, en el índice. SPEC-04 se aprueba aparte, antes del frontend | — |
| y2 | N-15, H-06 | R-04 en futuro («se contrastará»). CA-19 exacto: las 17 letras × 10 valores de control × dígito y letra, más 10.000 números con semilla fija. Resultado esperado: todo lo que el validador acepta lo acepta `python-stdnum`, y las únicas diferencias son las de la forma del control según los grupos de D-01. Cualquier otra discrepancia la decide él. Comprobar el comportamiento real de la biblioteca cuando se instale | No se afirma lo que no existe |
| y3 | N-03 | Con un país no válido o ausente, del identificador solo se comprueba lo que no depende del país (`missing`, `not_a_string`, `too_long`). Añadir casos | — |
| y4 | N-04 | `CHECK` `from_users >= 1` y `to_users IS NULL OR to_users >= from_users` | — |
| y5 | N-05 | `OPTIONS` queda fuera de la regla del `405`. Lo atiende el middleware de CORS: con origen admitido, `200` con sus cabeceras; con origen no admitido, `400` sin cabeceras CORS. Excepción documentada a `problem+json`. Además, los `500` llevan las cabeceras CORS; añadir el caso | Esa respuesta la consume el navegador y no el frontend. Lo de los `500`: que el frontend vea `internal_error` y no `network_error` |
| y6 | N-06 | Requisito EARS nuevo: mientras el cliente no se ha cargado, el simulador no pide ninguna proyección | — |
| y7 | N-07 | El DDL vive en el backend, en un `schema.sql` versionado. `02-arquitectura/` muestra el modelo y enlaza a ese fichero. Unificar los tres documentos | — |
| y8 | N-08 | Añadir a SPEC-02 5.1 la fila de 20000 usuarios (10000 / 32000 / 9975000 / 10017000 / 2103570 / 12120570) | — |
| y9 | N-09 | `/meta` se pide una vez al arrancar. Si falla, toda vista que necesite nombres (panel, alta, detalle y simulador) muestra el error con «Reintentar», sin códigos sueltos. El simulador muestra el nombre del país desde `/meta` | — |
| y10 | N-10 | La ayuda del navegador mide igual que el backend: puntos de código (`[...s].length`) y recorte solo de U+0020 | — |
| y11 | N-11 | A mayúsculas solo `a`–`z` con una correspondencia explícita, nunca `upper()`; «espacio» es solo U+0020; U+00A0 → error de formato. Añadir los casos `ﬁ` y NBSP | — |
| y12 | N-12 | El carácter de escape es `\` | — |
| y13 | N-13 | `application/json` con parámetros (`charset`) es válido; precedencia `415` > `400` > `422`; `DATABASE_PATH` vale por defecto `backend/data/saas-o-matic.db` (ignorado por git) | — |
| y14 | N-14 | ADR-005 para las dependencias de test (`python-stdnum` y Playwright). En `02-arquitectura/README.md`, el criterio: lleva ADR toda decisión que afecte a la arquitectura o a más de una spec; las que solo afectan a una spec se quedan en la tabla de decisiones de esa spec | — |
| y15 | N-02, N-16, N-17 y el resto de H-13 | Corregirlos como propone el informe | — |

Pidió el resumen y parar después de los commits.

**Cómo se aplicaron las correcciones (15:56–16:03).** Unas 75 sustituciones
de texto en 10 ficheros y un fichero nuevo (ADR-005), hechas una a una con
la herramienta de edición, que exige que el texto a sustituir aparezca
exactamente una vez. No se usó ningún script.

**Precisiones añadidas por la IA sin que estuvieran en las decisiones**:
catorce, numeradas P-01 a P-14 en el apartado 2 de
`04-calidad/respuesta-evaluacion-specs-02.md`. Las más relevantes: la
composición del conjunto aleatorio de CA-19 (P-02), qué cuenta como «país no
válido o ausente» (P-03), que el fallo de `/meta` sustituye al contenido de
la vista (P-05) y que la ruta por defecto de la base de datos es relativa a
la raíz del repo y su directorio se crea si falta (P-08). **Ninguna está
aprobada**, y están ya en los commits `710917b` y `2469bd0`.

**Cuestiones que la IA no resolvió y dejó planteadas**: cuatro, Q-01 a Q-04
en el apartado 3 de la respuesta. La de más peso: con el criterio nuevo de
los ADR, hay decisiones ya tomadas que afectan a más de una spec y no tienen
ADR (Q-03); y los casos de `OPTIONS` que las decisiones no cubren (Q-01),
que en SPEC-03 quedan marcados «Sin especificar».

**Errores propios corregidos antes del commit**:

- En el apartado 7 de SPEC-01 la IA escribió que todas las decisiones de la
  tabla «solo afectan a esta spec». No lo había comprobado y no es evidente
  (D-08 añade una columna al esquema de SPEC-03). Lo sustituyó por una
  remisión al criterio.
- En SPEC-04 escribió «0 peticiones» en dos filas de `/meta` caído (panel y
  simulador). Ninguna decisión dice si esas vistas piden o no sus datos con
  `/meta` en error; lo dejó en «—».

**Sobre «corregir como propone el informe» (y15)**: como en la primera
evaluación, el informe describe el defecto y no propone un arreglo. Los
arreglos de N-02, N-16, N-17 y H-13 los eligió la IA; son los cambios
mínimos que eliminan el defecto descrito.

**Lo que la IA no tocó**: `CLAUDE.md` y `.claude/rules/`. N-01 cita la regla
«spec antes que código»; con la aprobación en bloque deja de chocar y no
hizo falta cambiarla. La IA no instaló `python-stdnum`: la decisión dice
comprobarlo «cuando se instale».

### Correcciones de la segunda evaluación · Revisión (16:15)

Aclaraciones del Tech Lead: el fichero del directorio ignorado `.private/`
modificado a las 15:43:50 es suyo, privado y ajeno a la prueba, y no hay que
tenerlo en cuenta; el cambio en disco de esta bitácora que la IA dio por
externo contenía solo la fila de las horas, escrita por la propia IA.

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| z1 | Añadió catorce precisiones, P-01 a P-14, y las dejó en los commits `710917b` y `2469bd0` sin aprobación previa, avisándolo al entregar | **Aprobadas las catorce** | — |
| z2 | Q-01: dejó «sin especificar» un `OPTIONS` que no es comprobación previa | **Decidido**: responde `405` `method_not_allowed` | — |
| z3 | Q-02: avisó de que «`400` sin cabeceras CORS» podía no coincidir con el middleware estándar | **Cambiado**: sin código a medida. La comprobación previa rechazada se queda con el comportamiento estándar del middleware de CORS; un test fija exactamente su estado y sus cabeceras, y lo que se exige es que no lleve `access-control-allow-origin`. Actualizar la regla | — |
| z4 | Q-03: señaló decisiones que afectan a más de una spec y no tienen ADR, sin crear ninguno | **ADR-006 «Convenciones transversales de la API»**: errores genéricos y `problem+json`, identificadores, fechas, constante única de países e historial dentro de la ficha, con alternativas y motivo. El bloque de aprobación se queda en el índice de specs | El bloque de aprobación es proceso, no arquitectura |
| z5 | Q-04: dejó sin fijar la semilla de CA-19 | **Semilla 20261112** | — |
| z6 | Declaró que no había releído ADR-002 | **Releerlo** y comprobar que encaja con SPEC-04 (200 ms, `v2` de Frankfurter, estados); corregir lo que no encaje | — |

Pidió dos commits (specs y bitácora, incluida la fila de las horas; y
ADR-006) y, después, sin implementar nada, la propuesta de diseño de
`scripts/check.py` y del hook `PreToolUse` que bloquea la escritura de
código sin spec aprobada, parando a esperar su revisión.

**Relectura de ADR-002 (z6)**: encaja con SPEC-04 y la IA **no cambió
nada**. Los 200 ms coinciden (ADR-002 «Decisión», SPEC-04 2.5 y E-18). Los
estados coinciden: ADR-002 exige estados de carga y de error y que un fallo
no deje el importe anterior como válido, que es lo que detallan SPEC-04 2.5,
E-20 y E-21. ADR-002 no nombra Frankfurter ni su versión: dice «la API
pública (A8)», así que no contradice la `v2`; esa decisión está en ADR-003.
Dos cosas que la IA vio y dejó como están, por no ser desajustes: ADR-002
no remite a ADR-003, y cita SPEC-02/CA-08, que a su vez remite a
SPEC-03/CA-03.

**Precisión de la IA al aplicar z3, sin aprobar (P-15)**: la segunda mitad
de Q-01 (comprobación previa de un origen admitido con un método o una
cabecera no admitidos) no tenía decisión propia; la IA le aplicó la de z3.
Detalle en el apartado 3 de la segunda respuesta.

**Sobre el «cambio externo»**: la IA avisó de un cambio en disco ajeno a
ella sin mirar antes qué había cambiado. Era su propia fila. Bastaba un
`git diff` antes de decirlo.

### Diseño del oráculo y del hook · Revisión (16:30)

La IA presentó el diseño en la conversación: un hook `PreToolUse` que
bloquea `Write`, `Edit` y `NotebookEdit` sobre `backend/**` y `frontend/**`
(tests incluidos) mientras su bloque de specs no esté `aprobada`, y pide
confirmación para tocar el propio hook, `settings.json` o el estado de una
spec; y un oráculo `scripts/check.py` con comprobaciones activas desde ya
(código sin spec, coherencia de specs, tamaños, reglas silenciadas, tests
saltados, tests propios) e inactivas hasta que exista el código (backend,
pureza del dominio, trazabilidad, frontend, Playwright). El Tech Lead lo
aprobó.

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| aa1 | Propuso no permitir el esqueleto (`pyproject.toml`, configuración) antes de aprobar el bloque | **De acuerdo** | — |
| aa2 | Propuso confirmación humana para cambiar el estado de una spec y para tocar el hook o `settings.json` | **Sí** | — |
| aa3 | Preguntó si había umbral de cobertura fuera de `domain/` | **Decidido**: 100 % de ramas en `domain/`, 90 % de ramas en todo el backend y 80 % de líneas en el frontend, con fallo por debajo | — |
| aa4 | Trazabilidad: falla si un test cita un requisito inexistente; los requisitos sin test solo se listan hasta el cierre de cada bloque | **Como propone** | — |
| aa5 | `unittest` para los tests de `scripts/`, sin dependencia nueva | **Sí** | — |
| aa6 | P-15 (la comprobación previa rechazada por método o cabecera sigue la decisión de Q-02) | **Aprobada** | — |
| aa7 | No había propuesto comprobar la higiene del repo | **Añadido**: bloque «higiene del repo», activo desde ya: ningún commit con trailer de coautoría ni firma de herramienta, ningún CRLF en ficheros versionados de texto y `.private/` nunca versionado | — |
| aa8 | Dijo que escribía de memoria el protocolo de los hooks y que lo contrastaría antes de implementar | **Ordenado**: contrastarlo con la documentación oficial (entrada JSON, código de salida o JSON de decisión, `deny`/`ask`, variable con la raíz del proyecto, cuándo se cargan) y anotar la fuente | — |

Pidió implementar con TDD (tests del hook y del oráculo en rojo, después el
código, oráculo en verde y commit), los pasos 1 y 3 del plan de pruebas,
registrar el hook en `.claude/settings.json` en el último commit y **parar
ahí, sin la prueba en vivo**: reiniciará la sesión para que se cargue el
hook. Pidió ver la salida real del oráculo.

**Protocolo de los hooks, contrastado con la documentación (aa8).** Lo leyó
un subagente de consulta (`claude-code-guide`) el 2026-11-12 en tres páginas
de la documentación oficial de Claude Code: la referencia de hooks
(<https://code.claude.com/docs/en/hooks>), la guía de hooks
(<https://code.claude.com/docs/en/hooks-guide>) y la de ajustes
(<https://code.claude.com/docs/en/settings>). La IA no leyó las páginas
directamente: trabaja con el informe del subagente, que distingue las frases
literales de las que le llegaron resumidas.

| Punto | Lo que dice la documentación, según el informe | Grado |
|---|---|---|
| Entrada | Un objeto JSON por la entrada estándar con `tool_name`, `tool_input` y `tool_use_id`, además de los campos comunes. `Write` trae `file_path` y `content`; `Edit`, `file_path`, `old_string`, `new_string` | Literal |
| Rutas | `tool_input.file_path` llega siempre absoluta; en Windows, con barras invertidas | Literal |
| Salida 0 | Se aplica el JSON impreso, si lo hay. Sin JSON, la llamada sigue el flujo normal de permisos: salir con 0 no la aprueba | Literal |
| Salida 2 | Bloquea; el modelo ve la salida de error como motivo | Literal |
| Otros códigos | Error **no bloqueante**: la llamada continúa | Literal |
| JSON de decisión | `hookSpecificOutput` con `hookEventName`, `permissionDecision` (`allow`, `deny`, `ask`, `defer`) y `permissionDecisionReason`. El motivo lo ve el modelo en `deny` y el usuario en `ask`. Los campos `decision` y `reason` de nivel superior están obsoletos | Literal |
| Raíz del proyecto | Variable de entorno `CLAUDE_PROJECT_DIR`; en el comando, entre comillas dobles | Literal el ejemplo |
| Shell en Windows | Por defecto `bash` (Git Bash); PowerShell si no hay Git Bash, y allí `$CLAUDE_PROJECT_DIR` sin `$env:` vale nulo | Resumido |
| Cuándo se cargan | Claude Code vigila los ficheros de ajustes y aplica los cambios de `hooks` a la sesión en curso sin reiniciar; si no aparecen en unos segundos, reiniciar | Literal |
| Tiempo máximo | 600 s por defecto para un comando; si se agota, no bloquea | Resumido |

No documentado en lo leído: los campos de `NotebookEdit`, si el `matcher`
distingue mayúsculas y si `MultiEdit` sigue existiendo.

**Dos cosas que la IA tenía mal o no sabía y cambian el diseño**:

- Creía que los hooks se cargan solo al arrancar. La documentación dice que
  se recargan en caliente: el hook puede quedar activo en esta misma sesión
  en cuanto se registre. La prueba en vivo se deja igualmente para después
  del reinicio, como ordenó el Tech Lead.
- Un hook que falla con un código distinto de 0 y de 2 **deja pasar la
  escritura**. Por eso el script captura cualquier error y termina en 2.
  Queda un hueco que el script no puede cerrar: si el comando ni siquiera
  arranca (falta `uv`, o no hay Git Bash y la variable no se expande), la
  escritura pasa. El informe menciona, resumido y no literal, un campo
  `onFailure: "block"` que lo cerraría; la IA **no lo ha usado** porque no
  está verificado. El segundo cerrojo es el oráculo.

**TDD (16:30–16:38)**:

1. **Rojo**: los siete módulos de test, escritos antes que el código,
   fallaron: `Ran 7 tests … FAILED (errors=7)`, todos por
   `ModuleNotFoundError` (`oracle`, `hooks`). Es un rojo de importación, no
   de aserción: demuestra que los tests se escribieron antes, no que cada
   uno falle por el motivo correcto.
2. **Verde**: escrito el código, `Ran 63 tests … OK` a la primera.
3. Como 63 tests en verde a la primera no dicen si los tests detectan algo,
   la IA rompió dos reglas en memoria, sin tocar ficheros: con la tabla de
   bloques vacía fallan 21 de 21 tests del control y del hook (15 fallos y 6
   errores); con el patrón de firmas inutilizado fallan 2 de 9 tests de
   higiene. No es una prueba de mutación completa.

**Paso 3 del plan de pruebas (el atajo por Bash)**: se creó
`backend/app/probe.py` con una redirección de Bash, que el hook no ve. El
oráculo terminó en rojo, con código 1 y la línea `backend/app/probe.py:
falta aprobar SPEC-01 (borrador), SPEC-02 (borrador), SPEC-03 (borrador)`.
Se borró el fichero y su carpeta, y el oráculo volvió a verde.

**El comando del hook, ejecutado a mano** con la variable
`CLAUDE_PROJECT_DIR` puesta por la IA y cargas JSON generadas con Python:
una escritura en `backend/app/probe.py` devuelve `deny` y código 0; una
edición de `.claude/settings.json`, `ask` y código 0; una escritura en
`ai-workspace/`, nada y código 0; una entrada que no es JSON, código 2 y el
motivo por la salida de error. **Error propio**: el primer intento de esta
prueba estaba mal montado (el JSON iba mal escapado desde el shell y el
código de salida que se imprimía era el de otro comando); se repitió bien.
Esto no es la prueba en vivo: quien llamó al script fue la IA, no Claude
Code.

**Precisiones de la IA al implementar, sin aprobar**:

| # | Precisión |
|---|---|
| I-01 | Piden confirmación también `scripts/oracle/specgate.py` (la regla que usa el hook) y `.claude/settings.local.json`, además del hook y de `settings.json` |
| I-02 | En `01-specs/` pide confirmación cualquier escritura cuyo texto nuevo contenga la palabra «aprobada», no solo la fila de estado. Una edición del índice que la mencione también pregunta |
| I-03 | El hook bloquea (código 2) si una herramienta de edición no trae ruta o la entrada no se entiende. Una herramienta que no es de edición la deja pasar |
| I-04 | Límite de parámetros: no cuentan `self` ni `cls`. El límite de 40 líneas se aplica también a las funciones de los tests; el de 250 líneas por fichero, no |
| I-05 | Son tests, para el límite de 250: lo que está bajo `tests/` o `e2e/`, `test_*.py`, `*.spec.ts` y `*.test.ts` |
| I-06 | Una regla silenciada vale si en la misma línea, tras la marca, hay un motivo introducido por `--`, `#` o `//` |
| I-07 | Higiene: firma de herramienta es una línea `Co-Authored-By:`, el texto «Generated with» o el emoji de robot. El CRLF se mira en el índice y en el árbol de trabajo. `.private/` se exige ignorado, sin seguimiento y ausente del historial de todas las ramas |
| I-08 | Capas: lectura estricta de `backend.md`. `repositories/` no puede importar de `domain/`, porque la regla solo nombra `api → services → domain` y `services → repositories`. Si los repositorios deben devolver objetos del dominio, hay que cambiarlo |
| I-09 | El oráculo llama a cuatro scripts de `npm` que el proyecto del frontend tendrá que definir: `lint`, `build`, `test:ci` (con el 80 % de líneas) y `e2e`. Los límites de función y de parámetros en TypeScript quedan a cargo de ESLint |
| I-10 | El 100 % de ramas de `domain/` se comprueba con `coverage report --include=app/domain/* --fail-under=100` tras el `pytest` |
| I-11 | El código se divide en `scripts/oracle/` (ocho módulos), `scripts/hooks/` y `scripts/tests/`, para no pasar de 250 líneas por fichero |

**No hecho**: la comprobación de pureza no prohíbe módulos de la biblioteca
estándar que hacen entrada o salida o leen el reloj; solo exige que lo
importado sea de la biblioteca estándar, como dice SPEC-02/CA-09.
`CLAUDE.md` sigue diciendo que el oráculo está «pendiente»; la IA no lo ha
tocado.

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git rev-parse --short HEAD` | Limpio, `fd46774` |
| Modelo del subagente `evaluador` | Hecha por el Tech Lead, en el transcript del subagente (15:45) | `claude-opus-5-5`: `model: opus` se aplica |
| Estado del repo tras el evaluador | `git status --short --untracked-files=all`, `git diff --stat`, `git diff --cached --stat`, `git rev-parse --short HEAD` (15:50) | Nada con seguimiento modificado ni preparado; `HEAD` en `fd46774`; sin seguimiento solo esta bitácora y el informe |
| Ficheros modificados durante la sesión, incluidos los ignorados | `find` con `-mmin -15` y `stat` | Ver la nota de la cronología: un fichero ignorado con hora 15:43:50 cuyo autor la IA no puede determinar |
| Finales de línea de los dos ficheros nuevos | Recuento de CR | Ninguno |
| Caso `12345679ſ` de SPEC-01 5.4 | `python`, fuera del repo | `12345679 mod 23 = 15`, letra `S`; `'ſ'.upper()` da `S` y `'ﬁ'.upper()` da `FI` |
| Fila de 20000 usuarios de SPEC-02 5.1 | `python` con la fórmula de SPEC-02 | 10000 / 32000 / 9975000 / 10017000 / 2103570 / 12120570, como dio el Tech Lead |
| Total de 20000 usuarios en SPEC-04 5.5 y casos de longitud de 5.4 | Node 24 | `121.205,70 EUR`; `'𝔸'.repeat(61)` mide 122 con `length` y 61 con `[...s].length`; `'\tAB'.trim()` da `AB` |
| CA-19 dentro de la tabla; U+00A0 literal y CRLF en las specs | `grep` | CA-19 va en la línea siguiente a CA-18; ningún U+00A0 literal (los casos lo nombran por su código); ningún CRLF |
| Trailers de coautoría | `git log -1 --pretty=%B \| grep -ci co-authored` tras cada commit | 0 en `27b9373`, `710917b` y `2469bd0` |
| Oráculo | `uv run scripts/check.py`, a las 16:38 | Código de salida 0: 11 comprobaciones correctas, 0 con fallo y 12 inactivas (las ocho del backend y las cuatro del frontend) |
| Tests del oráculo y del hook | `python -m unittest discover -s scripts/tests -t scripts` | `Ran 63 tests`, `OK` |
| Oráculo ante código sin spec | Fichero creado con Bash en `backend/app/` | Código de salida 1, con el fichero y las tres specs pendientes; verde de nuevo al borrarlo |
| Tamaño de los ficheros de `scripts/` | `wc -l` | El mayor, `specgate.py`, tiene 129 líneas |

## 5. No verificado

- **Que Claude Code ejecute el hook y respete su decisión**: no se ha hecho
  la prueba en vivo. Lo comprobado es el script, llamado a mano.
- Qué ocurre si el comando del hook no arranca (sin `uv`, o sin Git Bash en
  Windows), y si el campo `onFailure` existe.
- Que el `matcher` `Write|Edit|MultiEdit|NotebookEdit` coincida con las
  herramientas reales, y los campos de `NotebookEdit`.
- El oráculo y el hook solo se han ejecutado en Windows. La portabilidad a
  macOS y Linux está en el diseño (rutas, procesos sin shell, UTF-8), no
  probada.
- Los comandos del backend y del frontend del oráculo (ruff, mypy, pytest,
  coverage, npm): están inactivos y nunca se han ejecutado.

- El comportamiento real de `python-stdnum` con el CIF: el resultado
  esperado de CA-19 es una hipótesis. No se ha instalado.
- Que el framework permita, sin código a medida, las cabeceras CORS en un
  `500`, el `400` sin cabeceras CORS de la comprobación previa, el
  `Content-Type` con parámetros y la precedencia `415` > `400` > `422`.
- Las filas de casos añadidas hoy: comportamiento esperado, sin código que
  las ejecute.
- Las correcciones de hoy no han pasado por otra evaluación independiente.
- ADR-002 no se releyó al corregir; la IA no ha comprobado que nada de lo
  cambiado lo contradiga.

- Quién modificó a las 15:43:50 el fichero del directorio ignorado
  `.private/`.
- Que el evaluador no haya escrito fuera del repo.
- Que la transcripción del informe coincida carácter a carácter con lo que
  emitió el subagente.
- Ninguno de los hallazgos del informe: la IA no los ha contrastado con los
  documentos.
- Que el evaluador cumpliera las prohibiciones de lectura: lo afirma su
  informe; la IA no ha revisado su transcript.

- ~~El modelo con el que se ejecuta el subagente `evaluador`~~: verificado
  por el Tech Lead a las 15:45 (apartado 4).

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| Aprobar o cambiar las precisiones P-01 a P-14 y decidir Q-01 a Q-04 de la segunda respuesta | A decidir por el Tech Lead |
| Aclarar quién modificó a las 15:43:50 el fichero del directorio ignorado `.private/` | Cuando el Tech Lead lo vea |
| Decidir A2 a A5 | Viernes 13 de noviembre de 2026, 10:00 |
| Aprobar el bloque backend (SPEC-01, SPEC-02 y SPEC-03) y, aparte, SPEC-04 | Tras lo anterior |
| Comprobar el comportamiento real de `python-stdnum` | Cuando se instale |
| `schema.sql` y su enlace desde el índice de arquitectura | Con el esqueleto del backend |
| Aprobación literal del cambio de A10 (pendiente desde la sesión 02) | Cuando el Tech Lead lo vea |
