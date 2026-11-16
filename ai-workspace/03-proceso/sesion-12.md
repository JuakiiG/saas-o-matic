# Sesión 12 · La nota de método corregida y las conversaciones sin rutas de usuario ni correo

| | |
|---|---|
| **Fecha** | 2026-11-16 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | **Parada 1 alcanzada (16:22): los tres pasos, hechos, cada uno en su commit y con el oráculo en código 0 antes, sin `--e2e`.** No ha cambiado el código de la aplicación ni ningún test: entre `9b58091` y el último commit no cambia nada en `backend/`, `frontend/` ni `scripts/`. **Paso 1** (`4020b1c`): las conversaciones regeneradas y `sesion-11.txt`, idénticas byte a byte a las que dejó el Tech Lead, y el índice al día. **Paso 2** (`b58083b`): la nota de método, sustituida entera y literal. **Paso 3** (`53768f7`): quién anotó los resultados del guion y el «Estado» al cerrar la sesión 12. **Lo que el Tech Lead tiene que conocer**: (1) **el `git diff` de las conversaciones es lo que decía el encargo y nada más**: 26 líneas, 19 rutas y 7 correos; (2) **el nombre de la carpeta de usuario sigue, suelto, en dos líneas de `sesion-11.txt` y en dos de la bitácora de la sesión 11**, y las 26 líneas siguen en el historial, en `4655810` (AK-02); (3) **la nota no se ha cambiado**; de lo que queda, N-10 a N-14, pesan dos: el motivo 3 de ADR-001 se apoya en quien lee cada diff (N-10) y «este mismo directorio» apunta a `ai-workspace/`, donde `.private/` no está (N-11); (4) la cabecera del guion sigue diciendo «Lo rellena quien ejecuta el guion» (AK-04); (5) la sesión tiene cinco commits, con el de apertura (AK-01). Quedan sin aprobar AK-01 a AK-05. · Antes, sesión abierta a las 16:06 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

**La conversación es nueva**, sin el contexto de la sesión 11: la IA llega
con lo que ha leído al empezar (`CLAUDE.md`, `ai-workspace/README.md` y la
bitácora de la sesión 11, con sus pendientes) y con sus cuatro notas de
memoria, no con lo que hizo hace una hora.

**La segunda sesión de IA, «la que audita»**, sigue sin verse desde esta
conversación: lo que esta bitácora dice de ella es lo que dicen el encargo y
la nota de método. La fila de participantes de arriba nombra a quienes
hablan en esta conversación.

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 12: se corrige la nota de método con lo que la IA encontró y se
> retiran de las conversaciones las rutas de usuario y el correo. Antes de
> nada, leer `CLAUDE.md`, `ai-workspace/README.md` y los pendientes de
> `03-proceso/sesion-11.md`. Abrir esta bitácora con el mismo formato que
> las anteriores.
>
> Parada 1 de la sesión 11 aprobada. Admitidas AJ-01 a AJ-07. Los nueve
> cruces N-1 a N-9 estaban bien vistos: los cuatro que pesan se corrigen
> aquí. N-3, N-5, N-7, N-8 y N-9 se quedan como están.
>
> En esta sesión no cambia el código de la aplicación ni ningún test. Un
> commit por paso, con el oráculo en verde por su código de salida, sin
> `--e2e`.
>
> **Paso 1. Las conversaciones (AJ-02).** El Tech Lead ha regenerado los
> ficheros de `03-proceso/conversaciones/` y ha añadido `sesion-11.txt`,
> sin commit: git enseña cinco modificados y uno nuevo. **No editarlos.**
> Lo que cambia respecto a `4655810`, y nada más: la carpeta de usuario de
> las rutas locales pasa a ser `<usuario>` (19 veces, en las sesiones 05,
> 06-07, 08 y 09) y el correo `noreply` del autor pasa a ser una marca (7
> veces, en la 01). Son 26 líneas. El fichero nuevo, `sesion-11.txt`,
> lleva ya la misma sustitución (3 rutas). Comprobar con `git diff` que es
> eso y solo eso, y decir si se ve otra cosa. Poner al día el índice:
>
> - La tabla gana la sesión 11. La que falta ahora es la 12, por la misma
>   razón.
> - «Qué se ha cambiado al publicarlas» gana las dos sustituciones, y dice
>   que la primera versión publicada, la del commit `4655810`, todavía las
>   llevaba.
>
> **Paso 2. La nota de método.** Sustituir entero el apartado «Dos
> sesiones de IA y una persona» de `ai-workspace/README.md` por el que
> trae el encargo, literal. Solo ajustar los saltos de línea. Si algo
> sigue contradiciendo lo que la IA sabe del repositorio, decirlo en la
> parada sin cambiarlo.
>
> **Paso 3. Dos retoques, en un commit:**
>
> - En `pruebas-manuales.md`, en el apartado final y sin tocar las tablas:
>   los resultados los anotó, al dictado del Tech Lead, la sesión que
>   audita, con enlace a la nota (N-2).
> - El «Estado» de `ai-workspace/README.md`, al día: al cerrar la sesión
>   12. Siguen pendientes la integración continua y el clon limpio.
>
> **Parar ahí (parada 1)** y cerrar la bitácora de la sesión 12. Decir qué
> cambió, qué enseñó el `git diff` de las conversaciones y si algo de la
> nota sigue contradiciendo lo que la IA sabe. No leer ni citar
> `.private/`.

El texto del apartado del paso 2 venía entero en el encargo. No se repite
aquí: está en `ai-workspace/README.md` tal como llegó.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 16:10 | — | Mensaje recibido hacia las 16:06 (primera lectura del reloj, 16:06:49). El último commit es `9b58091` (2026-11-16 15:35:56), el cierre de la sesión 11. **`git status`: cinco `.txt` de `03-proceso/conversaciones/` modificados (01, 05, 06-07, 08 y 09) y `sesion-11.txt` sin versionar**, que es lo que anunciaba el encargo. **`netstat` a las 16:07:41: nada escucha en el 8000 ni en el 4200.** `backend/data/saas-o-matic.db`, del Tech Lead: 28.672 bytes, 2026-11-14 18:37; la IA no lo toca. Lecturas del encargo hechas, y además el índice de las conversaciones y `04-calidad/pruebas-manuales.md`. **El `git diff` de las conversaciones, comprobado antes de tocar nada** (16:07:38 a 16:09:48; apartado 4): son las dos sustituciones y nada más. Lo que la IA ha visto además está en AK-02. Apertura de esta bitácora |
| 16:13 | `1c01eff` | **Apertura de la bitácora**, 16:12:39 según `git log`, tras el oráculo sin `--e2e` de 16:10:54 a 16:12:39, código 0 (23 correctas, 1 inactiva); la salida, a un fichero, y el commit, en la misma orden, solo con ese código. Solo entra `sesion-12.md`: las conversaciones siguen sin commit (AK-01) |
| 16:13 | — | **Paso 1, el índice**: `conversaciones/README.md`, con la herramienta de edición, de 54 a 62 líneas. La tabla gana la sesión 11 (1.379 líneas) y dice «de la 01 a la 11»; «Lo que falta» nombra la sesión 12 en lugar de la 11; «Qué se ha cambiado al publicarlas» gana las dos sustituciones, con sus cuentas, y la frase del commit `4655810`. Sus 22 destinos existen (16:13:05). **Y un cambio que el encargo no nombraba**: en `ai-workspace/README.md`, la fila de `03-proceso` de «Cómo leerlo» decía «sesiones 01 a 10» y dice «01 a 11» (AK-03). Los `.txt` no se han tocado |
| 16:15 | `4020b1c` | **Paso 1**, 16:15:08 según `git log`: los cinco `.txt` regenerados, `sesion-11.txt`, el índice y la fila de `ai-workspace/README.md`; ocho ficheros, 1.418 líneas añadidas y 31 quitadas. Antes, oráculo sin `--e2e` de 16:13:26 a 16:15:08, código 0 (23 correctas, 1 inactiva). Después (16:15:09): **los diez `.txt` del commit tienen la misma huella que los que dejó el Tech Lead** y los de la carpeta siguen igual; `git ls-files --eol` dice `i/lf w/lf` en los once ficheros de la carpeta |
| 16:17 | — | **Paso 2, la nota de método**, en `ai-workspace/README.md`, con la herramienta de edición: el apartado «Dos sesiones de IA y una persona», sustituido por el del encargo, con los saltos de línea a 76 columnas como mucho; pasa de 48 a 65 líneas. Cambian «Tres consecuencias» por «Cinco», dos consecuencias nuevas («El análisis previo» y «Revisa cada diff»), la última consecuencia y el párrafo de las notas; lo demás del apartado ya decía lo mismo. **Sin los saltos de línea, el apartado es idéntico al texto del encargo** (16:16:01; las dos copias son de la IA, como en AJ-07). Lo que la nota nueva dice frente a lo que la IA sabe está en el apartado 3, N-10 a N-14: **la nota no se ha cambiado** |
| 16:19 | `b58083b` | **Paso 2**, 16:19:05 según `git log`: solo `ai-workspace/README.md`, 27 líneas añadidas y 10 quitadas. Antes, oráculo sin `--e2e` de 16:17:24 a 16:19:05, código 0 (23 correctas, 1 inactiva) |
| 16:19 | — | **Paso 3, los dos retoques.** (1) `04-calidad/pruebas-manuales.md`, apartado final «De dónde sale lo que el guion espera»: una frase detrás de la que dice quién lo ejecutó, «Los resultados los anotó, al dictado del Tech Lead mientras lo ejecutaba, la sesión de IA que audita», con enlace a la nota. Ninguna línea de tabla cambia (16:19:32). (2) El «Estado» de `ai-workspace/README.md`: «al cerrar la sesión 10» pasa a «al cerrar la sesión 12 (las sesiones 11 y 12 solo han cambiado documentación)» (AK-04). Los dos pendientes, la integración continua y el clon limpio, siguen como estaban |
| 16:22 | `53768f7` | **Paso 3**, 16:21:37 según `git log`: `pruebas-manuales.md` y `ai-workspace/README.md`, 6 líneas añadidas y 2 quitadas. Antes, oráculo sin `--e2e` de 16:19:54 a 16:21:37, código 0 (23 correctas, 1 inactiva). Después (16:21:37): entre `9b58091` y este commit cambian 10 ficheros, **ninguno en `backend/`, `frontend/` ni `scripts/`**; nada escucha en el 8000 ni en el 4200; `backend/data/saas-o-matic.db`, igual. Al escribir esta fila (reloj, 16:21:51), corregidas dos horas de las filas anteriores, que la IA había puesto sin mirar el reloj (AK-05) |
| 16:22 | *(este commit)* | **Cierre de esta bitácora para la parada 1.** Las filas anteriores se han escrito cada una en su momento, con el fichero sin commit entre la apertura y este cierre: los commits de los pasos llevan solo los ficheros de su paso. La IA para aquí: el Tech Lead revisa los tres pasos, lo que enseñó el `git diff` (AK-02), la tabla N-10 a N-14 y las precisiones AK-01 a AK-05. El `push` es suyo. La hora de este commit se ve con `git log` |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (16:06)

**Parada 1 de la sesión 11, aprobada. Admitidas AJ-01 a AJ-07.** Los nueve
cruces N-1 a N-9 «estaban bien vistos». **Los cuatro que pesan se corrigen
en esta sesión**: N-1 (quién revisa cada diff), N-4 (dónde están las notas
de la sesión que audita) y N-6 (el material previo de la sesión 01), con la
nota nueva del paso 2, y N-2 (quién anotó los resultados del guion), con el
retoque del paso 3. **N-3, N-5, N-7, N-8 y N-9 se quedan como están.**
**AJ-02: las rutas de usuario y el correo se retiran de las conversaciones**
(paso 1). La bitácora de la sesión 11 no se toca: la aprobación queda
anotada aquí.

**Reglas de esta sesión**, del encargo:

- **No cambia el código de la aplicación ni ningún test.**
- **Un commit por paso**, con el oráculo en verde por su código de salida,
  **sin `--e2e`**.
- **Los ficheros de conversaciones no se editan**: los ha regenerado el
  Tech Lead y entran tal como están.
- **El apartado del paso 2 es literal**: solo se ajustan los saltos de
  línea. Lo que siga contradiciendo lo que la IA sabe se dice en la
  parada, sin cambiarlo.
- **En `pruebas-manuales.md` no se tocan las tablas.**
- **`.private/` no se lee ni se cita.**

### Los tres pasos · lo hecho

| # | Commit | Qué toca |
|---|---|---|
| 1 · Las conversaciones | `4020b1c` | Los cinco `.txt` regenerados y `sesion-11.txt`, tal como los dejó el Tech Lead; `conversaciones/README.md`; y una fila de `ai-workspace/README.md` («01 a 11») |
| 2 · La nota de método | `b58083b` | `ai-workspace/README.md`: el apartado «Dos sesiones de IA y una persona», sustituido entero |
| 3 · Dos retoques | `53768f7` | `04-calidad/pruebas-manuales.md`: una frase en el apartado final. `ai-workspace/README.md`: la primera línea del «Estado» |

Ningún test nuevo ni cambiado: no hay rojo ni mutación que anotar.

Precisiones de la IA, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| AK-01 | **La sesión tendrá cinco commits**: este de apertura de la bitácora, los tres pasos y el cierre. En el de apertura solo entra `sesion-12.md`; las conversaciones siguen sin commit hasta el paso 1 | Es lo que se hizo en las sesiones 09 a 11 y lo admitido en AJ-01 |
| AK-02 | **El `git diff` es lo que dice el encargo, y además la IA ha visto cuatro cosas**, sin cambiar ninguna. (1) **El nombre de la carpeta de usuario sigue escrito, suelto, en dos líneas de `sesion-11.txt`** (221 y 350): son la fila AJ-02 de la bitácora de la sesión 11 tal como salió en pantalla, que dice cuál es el usuario de esas rutas. La sustitución cambió la ruta de esa fila, no esa frase. (2) **La bitácora de la sesión 11, que está versionada, lo lleva en dos líneas** (147, con la ruta y el nombre, y 195, con el nombre): `sesion-11.txt` enseña ahora esa fila con `<usuario>` y el fichero que esa conversación escribía dice el nombre. (3) **El historial**: el commit `4655810` conserva las 26 líneas, como dice el encargo, y el correo es el del autor de los 226 commits. (4) En `sesion-11.txt`, «❯» aparece también seis veces dentro del texto, citado; en las otras nueve conversaciones solo estaba al principio de línea | El encargo pedía decir si se veía otra cosa. La regla de `CLAUDE.md` habla de rutas locales; un nombre suelto no es una ruta, pero es justo lo que la sustitución retira. Las bitácoras antiguas no se tocan y los `.txt` no se editan: lo decide el Tech Lead |
| AK-03 | **Dos cosas del paso 1 que el encargo no daba.** (1) En `ai-workspace/README.md`, la fila de `03-proceso` de «Cómo leerlo» pasa de «sesiones 01 a 10» a «01 a 11»; va en el commit del paso 1. (2) En el índice, las dos sustituciones llevan sus cuentas (19 y 3 rutas, 7 correos), y la entrada de la sesión 12 dice «la que publica esta versión de los ficheros» | Con `sesion-11.txt` publicada, «01 a 10» era falso; es el mismo caso que «cinco documentos» en AJ-06, admitida. Las cuentas son las del encargo, comprobadas en el apartado 4. Si sobran, se quitan |
| AK-04 | **Tres cosas del paso 3.** (1) El «Estado» gana un paréntesis que el encargo no daba: «las sesiones 11 y 12 solo han cambiado documentación». (2) **Sus cifras no se han vuelto a contar**: son las de la sesión 10. La salida del oráculo, en verde, solo enseña los 96 tests de los scripts; los 741, los 569 y los 18 no salen, y Playwright no se ha ejecutado. (3) En el guion, la frase nueva dice «la sesión de IA que audita» y remite a la nota con «quién es y qué hace»; **la frase de la cabecera, «Lo rellena quien ejecuta el guion», y «Quién: JGH» siguen como estaban**: no están en el apartado final y una es de una tabla | (1) Sin el paréntesis, «al cerrar la sesión 12» delante de cifras de la sesión 10 hace pensar que se han vuelto a medir; que solo ha cambiado documentación lo dice `git diff df1740f HEAD -- backend frontend scripts`, vacío. (3) El encargo acotaba el retoque al apartado final. La cabecera y el final dicen ahora cosas distintas sobre quién rellena |
| AK-05 | **Dos errores de la IA en esta sesión.** (1) **Horas puestas sin mirar el reloj**: las filas del commit del paso 2 y del paso 3 decían 16:20 y se escribieron entre las 16:19:32 y las 16:19:54, que son las lecturas de antes y de después; corregidas a 16:19 antes de entrar en ningún commit. Otras dos celdas tampoco salieron de una lectura hecha al escribirlas, y no se pueden afinar más: la fila de apertura (16:10) se escribió entre las 16:09:48 y las 16:10:54, y la del paso 2 (16:17), entre las 16:16:43 y las 16:17:24. (2) **Una orden mal escrita al comprobar el `git diff`**: la primera comparación (16:07:38) dio las líneas por distintas porque la sustitución de la IA no cambiaba las rutas con `\`; con la orden bien escrita (16:08:04), idénticas | La regla 6 dice que las horas salen del reloj y nunca se estiman; es el mismo error de AJ-05. El de la orden duró medio minuto y no llegó a ningún texto: se anota porque la comprobación que vale es la segunda |

### La nota nueva frente a lo que la IA sabe del repositorio

El encargo pedía decirlo sin cambiar la nota. **La nota está en el README
tal como llegó.** Como en la sesión 11, la IA no puede confirmar ni
desmentir nada de lo que la nota dice de la sesión que audita: no la ve.
**De los cuatro cruces que pesaban, la nota cierra tres** (N-1, N-4 y N-6)
y el paso 3 cierra el cuarto (N-2). Lo que sigue es lo que queda después.
La numeración continúa la de la sesión 11. **Ninguno de los textos citados
se ha tocado.**

| # | Qué dice la nota | Qué dice el repositorio | Qué ha hecho la IA |
|---|---|---|---|
| N-10 | «`CLAUDE.md`, las convenciones de este documento y ADR-001 dicen que el Tech Lead revisa cada diff», y en la práctica él lee sobre todo el veredicto | `CLAUDE.md` lo dice así. Las convenciones dicen «revisa cada cambio». **ADR-001 no lo dice como reparto, lo usa como argumento**: el criterio «Experiencia previa de quien revisa» (alta en Python, menor en Node) y el motivo 3 de la decisión del backend, «Quien revisa cada diff conoce bien este stack. Auditar código generado exige entenderlo sin esfuerzo»; y en los riesgos del frontend, «Quien revisa tiene menos experiencia en Angular que en Python. Se mitiga con […] revisión explicada de cada componente generado». Hay dos textos más que la nota no nombra: el primer encargo, en `sesion-01.txt` (línea 63: «reviso cada diff»), y ADR-005 («las capturas […] las revisa el Tech Lead») | Nada. La nota declara la diferencia y los tres textos siguen como estaban. **Lo que pesa es ADR-001**: uno de los tres motivos del stack se apoya en quien lee cada diff, y la nota dice que quien lee el código en cada parada es la sesión que audita |
| N-11 | Las notas y los borradores «están en `.private/`, la carpeta de este mismo directorio que git ignora» | La nota está en `ai-workspace/README.md`. `.private/` existe en la raíz del repositorio y no en `ai-workspace/` (`test -d`, sin listarla); la ignora la línea 2 de `.gitignore` | Nada. Leído desde ese documento, «este mismo directorio» apunta a `ai-workspace/`. Además, la primera consecuencia dice «la carpeta privada» antes de que la nota la nombre |
| N-12 | El análisis previo y el estudio del stack los preparó el Tech Lead con la sesión que audita; las decisiones de stack y del cálculo las tomó él; la sesión que implementa redactó `00-analisis/` y los dos primeros ADR «a partir de ese material y del enunciado» | `sesion-01.txt`, líneas 66 a 72 y 74: coincide (el primer encargo manda leer el enunciado, el análisis y el estudio, y dice «Decisiones ya tomadas por mí»). ADR-001 y ADR-002: «Decide: Tech Lead». Los dos primeros ADR son del commit `45b913d`, de la sesión 01. Quedan dos cruces: ese mismo encargo dice del material privado que «no se publica ni se cita nunca en el repo», y la bitácora de la sesión 01 dice «redactados como análisis propio»; `requisitos.md` dice «nuestra lectura del encargo» | Nada. La nota dice que ese material existe y qué es, no lo que contiene; sus nombres de fichero ya se veían en `sesion-01.txt` |
| N-13 | Los prompts largos «salieron de ese borrador» | El borrador es el «borrador de respuesta» de la sesión que audita, tres párrafos más arriba. Entre los dos está ahora la consecuencia del análisis previo, que habla de «ese estudio» y «ese material» | Nada. Es de redacción, no de hechos: «ese borrador» puede leerse como el análisis previo |
| N-14 | Los ficheros exportados se dejaron en la carpeta «ya revisados» | El índice de las conversaciones dice desde hoy que la primera versión publicada todavía llevaba las rutas de usuario y el correo (AJ-02). Los ficheros se han dejado dos veces el 16/11: los nueve de la sesión 11 y los de esta | Nada. «Ese mismo día» sigue siendo cierto |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git log -1` (16:06:49 y 16:09:48) | `9b58091`; cinco `.txt` modificados y `sesion-11.txt` sin versionar |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000 y 4200 (16:07:41) | Ninguno en escucha |
| La base local del Tech Lead | Listado de `backend/data/` (16:07:41) | 28.672 bytes, 2026-11-14 18:37 |

El `git diff` de las conversaciones, **antes de tocar nada** y solo con
órdenes de lectura:

| Qué | Cómo | Resultado |
|---|---|---|
| Cuánto cambia | `git diff --numstat` y `git diff -U0`, guardado fuera del repositorio (16:07:38) | **26 líneas quitadas y 26 puestas**, en 26 trozos de una línea cada uno: 7 en `sesion-01`, 1 en `sesion-05`, 15 en `sesion-06-07`, 2 en `sesion-08` y 1 en `sesion-09`. Los cinco ficheros tienen las mismas líneas que en `4655810` (2.566, 5.839, 15.899, 13.478 y 4.427) |
| **Que sea eso y solo eso** | A las 26 líneas quitadas se les aplican las dos sustituciones y se comparan con las 26 puestas, con `cmp` (16:08:04) | **Idénticas.** En las líneas quitadas hay 19 veces la carpeta de usuario (16 con `\` y 3 con `/`) y 7 veces el correo |
| Los cuatro ficheros que git no da por modificados | SHA-256 de `sesion-02`, `03`, `04` y `10` en la carpeta y en `HEAD` (16:09:48) | Iguales, aunque los diez `.txt` tienen fecha de las 16:02 |
| Lo que queda en los diez `.txt` | Búsquedas de la carpeta de usuario, del correo, del nombre de usuario de GitHub y de cualquier ruta de usuario (16:07:40) | Ninguna ruta con la carpeta de usuario; ningún correo `noreply` ni el nombre de usuario de GitHub. `<usuario>`: 1, 15, 3 y 1 veces en `sesion-05`, `06-07`, `08` y `09` (una de las tres de la 08 ya estaba así) y 3 en `sesion-11`. La marca del correo, 7 veces en `sesion-01`. Los demás emails, de ejemplo (`.example`) o decoradores de Python. **El nombre de la carpeta de usuario, suelto, sigue en dos líneas de `sesion-11.txt`** (AK-02) |
| `sesion-11.txt` | `wc`, finales de línea, espacios finales, último byte, «❯» y sus primeras y últimas líneas (16:07:41 y 16:09:16) | 1.379 líneas y 79.643 bytes; `w/lf`, sin espacios finales ni retornos de carro, acaba en salto de línea. Empieza con el `/clear` y el encargo de la sesión 11 y acaba con la respuesta de la parada 1 y un «※ recap». «❯»: 2 al principio de línea y 6 más dentro del texto (AK-02) |
| Huella de los diez `.txt` antes del commit | `sha256sum`, guardada fuera del repositorio (16:09:48) | Para compararla con lo que quede en el commit del paso 1 |
| El autor de los commits | `git log --format=%ae`, contando sin mostrar la dirección (16:10:54) | 226 commits, una sola dirección, la `noreply` de GitHub |

Paso 1:

| Qué | Cómo | Resultado |
|---|---|---|
| Los enlaces del índice | `test -e` de sus 22 destinos (16:13:05) | Existen todos |
| **Las conversaciones entran en el commit sin cambiar** | SHA-256 de los diez `.txt` antes del commit (16:09:48), de los diez tal como quedan en `4020b1c` (`git show`) y de los de la carpeta después (16:15:09) | Las tres series, idénticas |
| Finales de línea de lo versionado | `git ls-files --eol` de la carpeta (16:15:09) | `i/lf w/lf` en los once ficheros |

Pasos 2 y 3:

| Qué | Cómo | Resultado |
|---|---|---|
| La nota, sin los saltos de línea, es el texto del encargo | `cmp` del apartado del README con una copia del encargo, juntando saltos y espacios (16:16:01) | Idénticos, 3.721 bytes. Las dos copias son de la IA: vale lo que valía en AJ-07 |
| El ancho del apartado | La línea más larga entre «Dos sesiones…» y «Estado» (16:16:01) | 76 columnas, en 65 líneas |
| Los enlaces de la nota | `test -e` de sus cinco destinos (16:16:01) | Existen. El ancla del apartado no cambia: el título es el mismo |
| Las citas de la tabla N-10 a N-14 | Lectura de las líneas citadas de `sesion-01.txt`, de ADR-001 y ADR-005, de la bitácora de la sesión 01 y de `requisitos.md` (16:09:16 a 16:17:24) | Dicen lo que la tabla dice que dicen |
| Dónde está `.private/` | `test -d` en la raíz y en `ai-workspace/`, y `git check-ignore -v` con una ruta de prueba; **sin listarla ni leerla** (16:09:16) | Existe en la raíz y no en `ai-workspace/`; la ignora la línea 2 de `.gitignore` |
| En el guion no cambia ninguna tabla | `git diff -U0` de `pruebas-manuales.md`, contando las líneas cambiadas que empiezan por «\|» (16:19:32) | Ninguna: cambia una línea de texto y se añaden tres |
| **El código de la aplicación y los tests no han cambiado** | `git diff --stat` de `backend`, `frontend` y `scripts`, desde `df1740f` (16:19:32) y desde `9b58091` (16:21:37) | Vacío las dos veces. Desde `9b58091`, 10 ficheros: esta bitácora, seis `.txt`, el índice, `ai-workspace/README.md` y `pruebas-manuales.md` |

Oráculo:

| Qué | Cómo | Resultado |
|---|---|---|
| **Antes de cada commit** | `uv run scripts/check.py`, sin `--e2e`; la salida, a un fichero fuera del repositorio, y el commit en la misma orden, solo con código 0 | Código 0 en las cuatro pasadas anteriores a este cierre (16:10:54, 16:13:26, 16:17:24 y 16:19:54): 23 correctas, 0 con fallo y 1 inactiva, Playwright |
| Puertos y base local al cerrar | `netstat` y un listado de `backend/data/` (16:21:37) | Ninguno en escucha; 28.672 bytes, 2026-11-14 18:37, como al empezar. La IA no ha arrancado ningún servidor |

## 5. No verificado

Al llegar a la parada 1:

- **Nada de lo que la nota dice de la sesión que audita**, como en la
  sesión 11: ni que exista, ni que preparara con el Tech Lead el análisis
  previo y el estudio del stack, ni que redactara los prompts, ni qué lee o
  comprueba en cada parada, ni que anotara los resultados del guion. Tampoco
  lo contrario. La IA ve los mensajes que llegan a esta conversación y el
  repositorio.
- **Que `sesion-11.txt` sea la conversación entera de la sesión 11 y que no
  se le haya cambiado nada más que las tres rutas**: es un fichero nuevo y
  la IA no tiene con qué compararlo. Ha mirado su principio, su final y las
  búsquedas del apartado 4; no lo ha leído entero. De los otros nueve sí
  hay comparación, con `4655810`.
- **Si las conversaciones llevan contenido de los ficheros de `.private/`**:
  sigue como en la sesión 11. La IA no lo ha buscado y no tiene con qué
  comparar sin leer la carpeta.
- **Que la copia de la nota sea fiel al mensaje del Tech Lead**, más allá
  de la comparación de las dos copias de la IA.
- **Las cifras del «Estado»** (741, 569, 18 y 96 tests, 140 requisitos,
  siete evaluaciones, once limitaciones): no se han vuelto a contar, salvo
  los 96 tests de los scripts, que salen en el oráculo (AK-04).
- **Cómo se ven los ficheros una vez publicados**: el ancla
  `#dos-sesiones-de-ia-y-una-persona`, también desde el enlace nuevo del
  guion, y los enlaces a los `.txt`. No hay remoto.
- **Ningún evaluador ha mirado los cambios de esta sesión**, ni los de las
  sesiones 09 a 11.
- **Sin pasada con `--e2e`**, por el encargo: Playwright sale inactivo en
  las cuatro. Los tests no se han tocado.
- Sigue como en la sesión 11: **la integración continua no se ha ejecutado
  nunca**, nada se ha ejecutado fuera de Windows y **un clon limpio**,
  tampoco.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Paso 1: las conversaciones regeneradas, `sesion-11.txt` y el índice al día~~ | Hecho (`4020b1c`) |
| ~~Paso 2: la nota de método nueva en `ai-workspace/README.md`~~ | Hecho (`b58083b`) |
| ~~Paso 3: el apartado final de `pruebas-manuales.md` y el «Estado»~~ | Hecho (`53768f7`) |
| **Parada 1: el Tech Lead revisa** los tres pasos, la tabla N-10 a N-14 y las precisiones AK-01 a AK-05. En particular: **si el nombre de la carpeta de usuario, suelto, se queda en `sesion-11.txt` y en la bitácora de la sesión 11** (AK-02); **si el motivo 3 de ADR-001 se queda como está** (N-10); **si «este mismo directorio» se queda** (N-11); y **si la cabecera del guion, «Lo rellena quien ejecuta el guion», se queda** (AK-04) | Ahora |
| La conversación de la sesión 12 no está publicada: el índice lo dice | A decidir por el Tech Lead |
| **Prueba en limpio y `push`**. Tras el `push`, ver el primer resultado de la integración continua en Linux y en Windows y corregir lo que falle | Del Tech Lead; la corrección, en una sesión nueva |
| Poner al día `ai-workspace/README.md` («Estado») y el README de la raíz («solo se ha probado en Windows 11») cuando la integración continua y el clon limpio tengan resultado | Entonces |
| Pendientes heredados que esta sesión no toca: L-07 y los avisos de `npm audit`, los cuatro scripts de instalación sin aprobar, las fechas del fichero de bloqueo en el oráculo y los de la sesión 06 | A decidir por el Tech Lead |
