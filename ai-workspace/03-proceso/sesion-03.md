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

## 5. No verificado

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
