# Sesión 11 · Las conversaciones publicadas y la nota de método

| | |
|---|---|
| **Fecha** | 2026-11-16 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | **Parada 1 alcanzada (15:33): los tres pasos, hechos, cada uno en su commit y con el oráculo en código 0 antes, sin `--e2e`.** No ha cambiado el código de la aplicación ni ningún test: entre `df1740f` y el último commit no cambia nada en `backend/`, `frontend/` ni `scripts/`. **Paso 1** (`4655810`): las nueve conversaciones, idénticas byte a byte a las que dejó el Tech Lead, y su índice. **Paso 2** (`1b84ee2`): la nota de método «Dos sesiones de IA y una persona» en `ai-workspace/README.md`, literal, con sus tres remisiones. **Paso 3** (`41e15c4`): la frase del README de la raíz. **Lo que el Tech Lead tiene que conocer**: (1) **la nota no se ha cambiado, y la IA no puede confirmar nada de lo que dice de la sesión que audita**, porque no la ve; dónde se cruza con otros textos está en N-1 a N-9, y los que más pesan son N-1 (quién revisa cada diff), N-4 (dónde están sus notas) y N-6 (el material previo de la sesión 01); (2) las conversaciones llevan 20 líneas con rutas de la carpeta de usuario y la dirección `noreply` del autor de los commits, y la IA no ha buscado si llevan contenido de `.private/` (AJ-02); (3) «cinco documentos» pasó a «seis» en el recorrido (AJ-06); (4) la sesión tiene cinco commits, con el de apertura (AJ-01). Quedan sin aprobar AJ-01 a AJ-07. · Antes, sesión abierta a las 15:16 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

**La conversación es nueva**, sin el contexto de la sesión 10: la IA llega
con lo que ha leído al empezar (`CLAUDE.md`, `ai-workspace/README.md` y la
bitácora de la sesión 10, con sus pendientes) y con sus cuatro notas de
memoria, no con lo que hizo hace una hora.

**El encargo declara una segunda sesión de IA, «la que audita»** (paso 2).
Desde esta conversación no se ve: lo que esta bitácora dice de ella es lo
que dice el encargo. La fila de participantes de arriba es la de las
bitácoras anteriores y nombra a quienes hablan en esta conversación.

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 11: se publican las conversaciones y se declara cómo se ha
> trabajado. Antes de nada, leer `CLAUDE.md`, `ai-workspace/README.md` y
> los pendientes de `03-proceso/sesion-10.md`. Abrir esta bitácora con el
> mismo formato que las anteriores.
>
> Parada 1 de la sesión 10 aprobada. Admitidas AI-01 a AI-07. AI-03: CA-07
> se queda como está.
>
> En esta sesión no cambia el código de la aplicación ni ningún test. Un
> commit por paso, con el oráculo en verde por su código de salida, sin
> `--e2e`.
>
> **Paso 1. Las conversaciones.** El Tech Lead ha dejado en
> `ai-workspace/03-proceso/conversaciones/` nueve ficheros de texto, sin
> commit: las conversaciones de esta sesión de Claude Code con cada sesión
> de trabajo, exportadas con `/export`. No editarlos: se publican tal como
> están. Escribir su índice, `conversaciones/README.md`, corto, con estos
> hechos, que son del Tech Lead y la IA no tiene que comprobar:
>
> - Un fichero por sesión, de la 01 a la 10. La 06 y la 07 comparten
>   conversación y fichero, `sesion-06-07.txt`, que empieza a mitad de la
>   06 (14/11, hacia las 10:47): la conversación se había compactado y lo
>   anterior no se pudo exportar. Lo que falta de la 06 está en su
>   bitácora.
> - La sesión 11, la que publica estos ficheros, no está: no puede
>   exportarse a sí misma antes de acabar.
> - Qué se ha cambiado al publicarlas: los finales de línea, los espacios
>   al final de cada línea y, en la 03, dos líneas que listaban otra
>   sesión abierta en el equipo, ajena al proyecto, sustituidas por una
>   marca. Nada más: el contenido de la interacción no se ha tocado.
> - Qué se ve y conviene explicar: las líneas «※ recap» son resúmenes de
>   la herramienta; los comentarios «buddy» son de un complemento de la
>   barra de estado; las rutas de `.private/` son material privado del
>   Tech Lead que no se publica; y los ficheros son largos porque incluyen
>   las salidas de las herramientas.
> - Cómo leerlas: cada intervención del Tech Lead empieza con «❯». Con
>   buscar ese carácter se recorren los prompts de una sesión.
>
> El índice enlaza cada fichero con su bitácora. Las bitácoras antiguas no
> se tocan.
>
> **Paso 2. La nota de método.** Añadir a `ai-workspace/README.md`, detrás
> de «Convenciones», el apartado «Dos sesiones de IA y una persona»,
> literal. Es del Tech Lead: no reescribirlo. Si algo de lo que dice
> contradice lo que la IA sabe del repositorio, decirlo en la parada sin
> cambiarlo. Ajustar solo los saltos de línea al ancho del fichero. En el
> mismo commit: la línea de «Roles» de «Convenciones» remite a este
> apartado, la fila de `03-proceso` de la tabla «Cómo leerlo» nombra las
> conversaciones, y el recorrido de cinco minutos gana una fila: una
> conversación (la de la sesión 08, buscando «❯») para ver cómo se dirigió
> a la IA.
>
> **Paso 3. El README de la raíz**, una frase en «Cómo se ha hecho»: que
> las conversaciones con la IA están publicadas y que el método, con sus
> dos sesiones, está explicado en `ai-workspace/README.md`.
>
> **Parar ahí (parada 1)** y cerrar la bitácora de la sesión 11. Decir qué
> se ha escrito, si algo de la nota contradice lo que la IA sabe y qué no
> ha podido comprobar. No leer ni citar `.private/`.

El texto del apartado del paso 2 venía entero en el encargo. No se repite
aquí: está en `ai-workspace/README.md` tal como llegó.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 15:20 | — | Mensaje recibido hacia las 15:15 (primera lectura del reloj, 15:16:09). El último commit es `df1740f` (2026-11-16 14:21:08), el cierre de la sesión 10. **`git status`: solo la carpeta `03-proceso/conversaciones/`, sin versionar**, con nueve `.txt` (3.633.507 bytes y 71.225 líneas en total, fechados hoy a las 15:11). **`netstat` a las 15:19:17: nada escucha en el 8000 ni en el 4200.** `backend/data/saas-o-matic.db`, del Tech Lead: 28.672 bytes, 2026-11-14 18:37; la IA no lo toca. Lecturas del encargo hechas, y además el README de la raíz, `.gitignore`, `.gitattributes`, `scripts/oracle/checks_hygiene.py` y la cabecera y el final de `04-calidad/pruebas-manuales.md`. Sobre las conversaciones, solo búsquedas de lectura (apartado 4 y AJ-02). Apertura de esta bitácora |
| 15:23 | `f5038e3` | **Apertura de la bitácora**, 15:22:31 según `git log`, tras el oráculo sin `--e2e` de 15:20:45 a 15:22:31, código 0 (23 correctas, 1 inactiva); la salida, a un fichero, y el commit, en la misma orden, solo con ese código. Solo entra `sesion-11.md`: las conversaciones siguen sin versionar (AJ-01) |
| 15:23 | — | **Paso 1, el índice**: `conversaciones/README.md`, 54 líneas, con los hechos del encargo en tres apartados (los ficheros y lo que falta, cómo leerlas y qué se ha cambiado al publicarlas). Lo que la IA ha añadido está en AJ-04. Los 20 destinos de sus enlaces existen (15:23:02). Antes del commit, huella SHA-256 de los nueve `.txt`, guardada fuera del repositorio, para comparar después con lo que quede en el commit |
| 15:25 | `4655810` | **Paso 1**, 15:25:13 según `git log`: los nueve `.txt` y su índice, diez ficheros y 71.279 líneas. Antes, oráculo sin `--e2e` de 15:23:28 a 15:25:13, código 0 (23 correctas, 1 inactiva). Después: **los nueve ficheros del commit tienen la misma huella que los que dejó el Tech Lead** y los de la carpeta siguen igual; `git ls-files --eol` dice `i/lf w/lf` en los diez. Al escribir esta fila, corregidos dos datos de la anterior, que la IA había puesto sin mirar: decía 15:24 y 55 líneas (AJ-05) |
| 15:27 | — | **Paso 2, la nota de método**, en `ai-workspace/README.md`, con la herramienta de edición: el apartado «Dos sesiones de IA y una persona», entre «Convenciones» y «Estado», con los saltos de línea a 76 columnas como mucho; la línea de «Roles» remite a él; la fila de `03-proceso` de «Cómo leerlo» nombra las conversaciones; y el recorrido gana la fila de la conversación de la sesión 08 (AJ-06). **Sin los saltos de línea, el apartado es idéntico al texto del encargo** (15:26:44; lo que esa comparación vale, en AJ-07). Lo que la nota dice frente a lo que la IA sabe del repositorio está en el apartado 3: **la nota no se ha cambiado** |
| 15:30 | `1b84ee2` | **Paso 2**, 15:30:13 según `git log`: solo `ai-workspace/README.md`, 54 líneas añadidas y 3 cambiadas. Antes, oráculo sin `--e2e` de 15:28:29 a 15:30:13, código 0 (23 correctas, 1 inactiva) |
| 15:30 | — | **Paso 3, el README de la raíz**: una frase al final del párrafo de «Cómo se ha hecho», con dos enlaces, al índice de las conversaciones y al apartado de la nota: «Las conversaciones con la IA están publicadas, y el método, con sus dos sesiones de IA, está explicado en `ai-workspace/README.md`.» Nada más cambia en ese fichero |
| 15:33 | `41e15c4` | **Paso 3**, 15:32:18 según `git log`: solo `README.md`, 4 líneas añadidas y 1 cambiada. Antes, oráculo sin `--e2e` de 15:30:32 a 15:32:18, código 0 (23 correctas, 1 inactiva). Después (15:32:19): entre `df1740f` y este commit cambian 13 ficheros, **ninguno en `backend/`, `frontend/` ni `scripts/`**; nada escucha en el 8000 ni en el 4200; `backend/data/saas-o-matic.db`, igual |
| 15:33 | *(este commit)* | **Cierre de esta bitácora para la parada 1**, escrito, como la fila anterior, entre las 15:32:29 y las 15:33:38, que son las dos lecturas del reloj. Las filas anteriores se han escrito cada una en su momento, con el fichero sin commit entre la apertura y este cierre: los commits de los pasos llevan solo los ficheros de su paso. La IA para aquí: el Tech Lead revisa los tres pasos, la tabla N-1 a N-9 y las precisiones AJ-01 a AJ-07. El `push` es suyo. La hora de este commit se ve con `git log` |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (15:15)

**Parada 1 de la sesión 10, aprobada. Admitidas AI-01 a AI-07.** **AI-03:
CA-07 se queda como está**: no nombra el caso del detalle. La bitácora de
la sesión 10 no se toca: la aprobación queda anotada aquí.

**Reglas de esta sesión**, del encargo:

- **No cambia el código de la aplicación ni ningún test.**
- **Un commit por paso**, con el oráculo en verde por su código de salida,
  **sin `--e2e`**.
- **Los nueve ficheros de conversaciones no se editan**: se publican tal
  como los dejó el Tech Lead.
- **Los hechos del índice son del Tech Lead**: la IA no tiene que
  comprobarlos.
- **El apartado del paso 2 es literal**: solo se ajustan los saltos de
  línea. Lo que contradiga lo que la IA sabe se dice en la parada, sin
  cambiarlo.
- **Las bitácoras antiguas no se tocan.**
- **`.private/` no se lee ni se cita.**

### Los tres pasos · lo hecho

| # | Commit | Qué toca |
|---|---|---|
| 1 · Las conversaciones | `4655810` | Los nueve `.txt` de `03-proceso/conversaciones/`, tal como estaban, y `conversaciones/README.md`, nuevo |
| 2 · La nota de método | `1b84ee2` | `ai-workspace/README.md`: el apartado nuevo, la línea de «Roles», la fila de `03-proceso` de «Cómo leerlo» y el recorrido (una fila más y «seis documentos») |
| 3 · El README de la raíz | `41e15c4` | `README.md`: una frase en «Cómo se ha hecho» |

Ningún test nuevo ni cambiado: no hay rojo ni mutación que anotar. Las
cifras de tests del «Estado» y del README de la raíz son las de la sesión
10 y no se han vuelto a contar.

Precisiones de la IA, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| AJ-01 | **La sesión tendrá cinco commits**: este de apertura de la bitácora, los tres pasos y el cierre. En el de apertura solo entra `sesion-11.md`; las conversaciones siguen sin commit hasta el paso 1 | Es lo que se hizo en las sesiones 09 y 10 y lo admitido en AI-01 |
| AJ-02 | **Antes de publicar las conversaciones la IA ha buscado en ellas, sin abrirlas enteras y sin tocarlas**, lo que `CLAUDE.md` dice que nunca entra en el repo (apartado 4). El encargo no lo pedía. Lo que hay: **20 líneas con rutas de la carpeta de usuario del equipo** (`C:\Users\Unknown\…`, de la carpeta temporal y de la del registro de las sesiones; en `sesion-05`, `06-07`, `08` y `09`); **la dirección `noreply` de GitHub del autor de los commits**, 7 veces en `sesion-01`, que es la que ya llevan los 221 commits; y **los nombres de cuatro ficheros de `.private/`**. Los demás emails son de ejemplo (`.example`) y no hay teléfonos. **La IA no ha cambiado nada**: lo decide el Tech Lead | La regla dice «datos personales (teléfono, email, rutas locales)» y el commit lo hace la IA. El usuario de esas rutas es `Unknown` y el encargo ya cuenta con que las rutas de `.private/` se ven |
| AJ-03 | **Un error de la IA al mirar los finales de línea**: su primera búsqueda (`grep -c` con un retorno de carro escrito en la orden) contó todas las líneas de los nueve ficheros como CRLF. Era la orden: `git ls-files --eol` dice `w/lf` en los nueve, los primeros bytes de `sesion-10.txt` no llevan `0d` y una segunda búsqueda, con `grep -P '\r'`, no encuentra ninguno | Durante unos minutos la IA creyó que el oráculo iba a fallar por los CRLF. No llegó a hacer nada con ese dato |
| AJ-04 | **El índice lleva cuatro cosas que el encargo no daba**: el número de líneas de cada fichero (`wc -l`), el título abreviado y la fecha de cada sesión (de la cabecera de su bitácora), un enlace a la bitácora de la sesión 11 donde dice que su conversación no está, y una frase de entrada que dice qué son («lo que el Tech Lead escribió, lo que la IA respondió y lo que ejecutó, en bruto»). **El índice no dice quién dejó los ficheros en la carpeta**: eso lo cuenta la nota del paso 2 | El número de líneas avisa de lo largos que son; el título ahorra abrir la bitácora para saber de qué va cada una. Si sobran, se quitan |
| AJ-05 | **Dos datos de la fila del índice estaban puestos a ojo y se corrigieron dos minutos después**: la hora (decía 15:24; la fila se escribió entre las 15:23:02 y las 15:23:28, que son las lecturas del reloj de antes y de después) y las líneas del índice (decía 55; `wc -l` da 54) | La regla 6 dice que las horas salen del reloj y nunca se estiman. La corrección se hizo antes de que la fila entrara en ningún commit, y se anota igual |
| AJ-06 | **Las tres remisiones del paso 2 las ha redactado la IA.** «Roles»: se queda como estaba y gana una frase («El reparto completo, con la segunda sesión de IA, que audita, está en…»). «Cómo leerlo»: la fila gana «Y las conversaciones exportadas de las sesiones 01 a 10», con el enlace al índice. El recorrido: la fila nueva va detrás de la bitácora de la sesión 08, dice que en esa sesión las intervenciones son cuatro (contadas) y remite a la nota para saber de dónde salieron esos prompts. **Y un cambio que el encargo no nombraba: «cinco documentos» pasa a «seis documentos»** en la frase que presenta el recorrido; el título, «Recorrido de cinco minutos», no cambia | Con la fila nueva, «cinco documentos» era falso. La remisión a la nota desde el recorrido está porque quien abra esa conversación va a leer justo los prompts de los que habla la nota |
| AJ-07 | **Cómo se ha comprobado que la nota es literal, y hasta dónde vale**: la IA copió el texto del encargo en un fichero fuera del repositorio y lo comparó con el apartado del README, juntando los saltos de línea y los espacios: idénticos, 2.546 bytes. **Las dos copias las ha escrito la IA a partir del mismo mensaje**: la comparación demuestra que al partir las líneas no se perdió ni cambió nada, no que la IA copiara bien el mensaje. Eso lo ve el Tech Lead con su texto | El encargo pedía el texto literal y la IA no tiene el mensaje como fichero |

### La nota de método frente a lo que la IA sabe del repositorio

El encargo pedía decirlo sin cambiar la nota. **La nota está en el README
tal como llegó.** La IA no puede confirmar ni desmentir nada de lo que la
nota dice de la sesión que audita: no la ve (apartado 5). Lo que sigue es
dónde la nota se cruza con otros textos del repositorio o con lo que
enseñan las conversaciones ya publicadas. **Ninguno de esos textos se ha
tocado**, salvo donde se dice.

| # | Qué dice la nota | Qué dice el repositorio | Qué ha hecho la IA |
|---|---|---|---|
| N-1 | La sesión que audita lee los cambios y los comprueba; el Tech Lead **lee el veredicto** y decide | `CLAUDE.md`, «Roles»: el Tech Lead «revisa cada diff». «Convenciones» de `ai-workspace/README.md`: «revisa cada cambio». ADR-001, motivo 3 del stack: «Quien revisa cada diff conoce bien este stack» | Nada. La línea de «Roles» de «Convenciones» conserva «revisa cada cambio» y solo gana la remisión. **Es el punto en el que la nota y los otros textos dicen cosas distintas** |
| N-2 | Los resultados del guion de pruebas manuales los **anotó la sesión que audita**, al dictado del Tech Lead | `pruebas-manuales.md`: «Lo rellena quien ejecuta el guion» y «Quién: JGH». La bitácora de la sesión 10 habla de «los resultados del Tech Lead» | Nada. Quién ejecutó el guion no cambia: la nota y el guion dicen que él |
| N-3 | Un «comprobado» o un «he visto» puede ser de la sesión que audita; por ejemplo, **los recorridos en el navegador de las sesiones 06 y 07** | La bitácora de la sesión 07 dice «Defecto visto por el Tech Lead en el navegador» y «el Tech Lead […] hace el recorrido en el navegador» | Nada: es justo lo que la nota declara, y las bitácoras antiguas no se tocan |
| N-4 | La sesión que audita está «abierta en otra carpeta» y **«no ha escrito en este repositorio»**, con dos excepciones; sus notas están «en una carpeta privada, ignorada por git» | La única carpeta privada que el repositorio conoce es `.private/`, que está **dentro de esta carpeta de trabajo**. Las conversaciones publicadas enseñan que en la sesión 03 la IA vio que un fichero de `.private/` cambiaba durante la sesión y el Tech Lead respondió que era un fichero privado suyo (`sesion-03.txt`, líneas 850, 3165 y 3181) | Nada. **Si** esa carpeta es la de las notas (la IA lo supone, no lo sabe), «no ha escrito en este repositorio» vale para lo que git versiona, no para la carpeta |
| N-5 | «Sin comunicación con la primera: nunca le ha enviado un mensaje» | En la sesión 10 una búsqueda de la IA le enseñó tres líneas de un fichero de `.private/` (AI-07, admitida) | Nada. No fue un mensaje y la IA no usó esas líneas; es el único cruce que la IA conoce |
| N-6 | La sesión que implementa «analiza, propone, escribe las specs» | `sesion-01.txt` (líneas 67 a 71): el primer encargo mandaba leer tres documentos de `.private/`, el enunciado, un análisis con los requisitos y las ambigüedades ya numerados y un estudio del stack. La bitácora de la sesión 01 dice «requisitos y supuestos, redactados como análisis propio» | Nada. **La nota no dice quién escribió ese material previo**; con las conversaciones publicadas, quien lea la primera lo va a ver |
| N-7 | El Tech Lead «hace el `push`» | `git remote -v` no devuelve nada: todavía no hay remoto. El «Estado» ya dice que el `push` está pendiente | Nada: la nota describe el reparto, no un hecho ya ocurrido |
| N-8 | Los ficheros exportados los dejó en la carpeta **la sesión que audita** | El encargo de esta sesión dice «he dejado» | Nada. El índice de las conversaciones no dice quién los dejó (AJ-04) |
| N-9 | Han trabajado **dos sesiones de IA** | La fila «Participantes» de las once bitácoras, esta incluida, nombra una | Nada en las antiguas. En esta, el párrafo de cabecera lo explica |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git log -1` (15:16:09 y 15:19:17) | `df1740f`; sin versionar, solo `ai-workspace/03-proceso/conversaciones/` |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000 y 4200 (15:19:17) | Ninguno en escucha |
| La base local del Tech Lead | Listado de `backend/data/` (15:19:17) | 28.672 bytes, 2026-11-14 18:37 |
| `.private/` está ignorada | `git check-ignore -v` con una ruta de prueba, sin listar la carpeta (15:17) | La ignora la línea 2 de `.gitignore` |
| Autoría de los commits y remotos | `git log --format=%an` y `%cn`, y `git remote -v` (15:17 y 15:18:59) | 221 commits, todos con el Tech Lead de autor y de *committer*; **ningún remoto configurado** |

Las conversaciones, solo con búsquedas de lectura:

| Qué | Cómo | Resultado |
|---|---|---|
| Finales de línea, espacios finales y salto final | `git ls-files --eol --others`, `grep -c` de espacio o tabulador al final de línea, `grep -c -P '\r'` y el último byte de cada fichero (15:17 a 15:19:42) | Los nueve, `w/lf`; ninguna línea con espacios finales; ningún retorno de carro; todos acaban en salto de línea (AJ-03) |
| Cuántas intervenciones del Tech Lead hay | `grep -c '^❯'` y el total de «❯» en cada fichero (15:18:59) | 9, 9, 11, 11, 3, 5, 4, 3 y 1, de la 01 a la 10: 56. **El carácter solo aparece al principio de línea**: buscarlo no da nada más |
| Dónde empieza `sesion-06-07.txt` | Sus doce primeras líneas y `git log -1 --format=%ci 32393b1` (15:17 y 15:18:59) | Empieza con la IA diciendo «Sexto grupo en `32393b1`»; ese commit es del 2026-11-14 a las 10:47:57 |
| La marca de la 03 | Búsqueda de «ajena» en `sesion-03.txt` (15:17) | Una, en la línea 22: «[línea retirada al publicar: otra sesión abierta en el equipo, ajena a este proyecto]» |
| «※ recap» y «buddy» | `grep -c` en cada fichero (15:17) | Los nueve tienen de las dos |
| Emails | Búsqueda de todo lo que tenga forma de email, agrupado (15:18) | De ejemplo (`.example`), decoradores de Python que la búsqueda confunde y la dirección `noreply` de GitHub del autor, 7 veces en `sesion-01` (AJ-02) |
| Rutas de usuario | Búsqueda de `C:\Users` y de `/c/Users` (15:18 y 15:19:42) | 20 líneas: 1 en `sesion-05`, 15 en `sesion-06-07`, 3 en `sesion-08` y 1 en `sesion-09`; el usuario es `Unknown` o `<usuario>` (AJ-02) |
| Teléfonos | Búsqueda de «+34» y de nueve cifras que empiecen por 6 o 7 (15:18) | Dos coincidencias, las dos trozos de un *diff*; ninguna es un teléfono |
| Qué se nombra de `.private/` | Búsqueda de la ruta, mostrando solo el nombre (15:18:59) | Cuatro nombres de fichero y 28 menciones de la carpeta. En `sesion-10.txt`, tres líneas, las tres de la bitácora y de la respuesta de la IA sobre AI-07. **La IA no ha buscado si hay contenido de esos ficheros** (apartado 5) |

Paso 1:

| Qué | Cómo | Resultado |
|---|---|---|
| Los enlaces del índice | `test -f` de sus 20 destinos (15:23:02) | Existen todos |
| **Las conversaciones entran en el commit sin cambiar** | SHA-256 de los nueve `.txt` antes del commit (15:23:02), de los nueve tal como quedan en `4655810` (`git show`) y de los de la carpeta después (15:25:13) | Las tres series, idénticas |
| Finales de línea de lo versionado | `git ls-files --eol` de la carpeta (15:25:13) | `i/lf w/lf` en los diez ficheros |

Pasos 2 y 3:

| Qué | Cómo | Resultado |
|---|---|---|
| La nota, sin los saltos de línea, es el texto del encargo | `cmp` del apartado del README con una copia del encargo, juntando saltos y espacios (15:26:44) | Idénticos, 2.546 bytes. Las dos copias son de la IA (AJ-07) |
| El ancho del apartado | La línea más larga entre «Dos sesiones…» y «Estado» (15:26:44) | 76 columnas |
| Los enlaces nuevos de `ai-workspace/README.md` | `test -f` de `conversaciones/README.md`, de `sesion-08.txt` y de `pruebas-manuales.md`; el ancla del apartado, escrita igual en sus dos remisiones (15:26:44) | Existen. **El ancla no se ha visto funcionar** (apartado 5) |
| Las citas de la tabla N-1 a N-9 | Lectura de las líneas citadas de ADR-001, de la bitácora de la sesión 07, de `pruebas-manuales.md` y de `sesion-01.txt` y `sesion-03.txt` (15:27) | Dicen lo que la tabla dice que dicen |
| **El código de la aplicación y los tests no han cambiado** | `git diff --stat df1740f HEAD -- backend frontend scripts` (15:32:19) | Vacío. En total, 13 ficheros: esta bitácora, los diez de `conversaciones/` y los dos README |

Oráculo:

| Qué | Cómo | Resultado |
|---|---|---|
| **Antes de cada commit** | `uv run scripts/check.py`, sin `--e2e`; la salida, a un fichero fuera del repositorio, y el commit en la misma orden, solo con código 0 | Código 0 en las cuatro pasadas anteriores a este cierre (15:20:45, 15:23:28, 15:28:29 y 15:30:32): 23 correctas, 0 con fallo y 1 inactiva, Playwright |
| Puertos y base local al cerrar | `netstat` y un listado de `backend/data/` (15:32:19) | Ninguno en escucha; 28.672 bytes, 2026-11-14 18:37, como al empezar. La IA no ha arrancado ningún servidor |

## 5. No verificado

Al llegar a la parada 1:

- **Nada de lo que la nota dice de la sesión que audita.** La IA no la ve:
  ni que exista, ni dónde está abierta, ni qué lee, ni qué comprobó, ni que
  redactara los prompts, ni que anotara los resultados del guion o dejara
  los ficheros exportados. Tampoco lo contrario. Lo que la IA ve son los
  mensajes que llegan a esta conversación y el repositorio.
- **Los hechos del índice que afirma el Tech Lead** y que la IA no ha
  mirado: que cada fichero es la conversación de su sesión y está entera,
  que lo anterior de la 06 no se pudo exportar, qué se cambió al
  publicarlas y que no se cambió nada más. La IA no tiene los ficheros de
  antes de esos cambios. Lo que sí ha mirado está en el apartado 4.
- **Si las conversaciones llevan contenido de los ficheros de `.private/`**
  (por ejemplo, en la salida de una lectura): la IA solo ha buscado las
  rutas, no ha leído los ficheros enteros y no tiene con qué comparar sin
  leer `.private/`. **Tampoco las ha leído enteras buscando otra cosa**:
  son 71.225 líneas y la revisión, dice el encargo, ya estaba hecha.
- **Que la copia de la nota sea fiel al mensaje del Tech Lead**, más allá
  de lo que dice AJ-07.
- **Cómo se ven los tres ficheros una vez publicados**: el ancla
  `#dos-sesiones-de-ia-y-una-persona`, los enlaces a los `.txt` y la
  búsqueda de «❯» en un fichero de 13.478 líneas. Nada de eso se ha visto
  en la web de un servidor de git: no hay remoto.
- **Ningún evaluador ha mirado los cambios de esta sesión**, ni los de las
  sesiones 09 y 10.
- **Sin pasada con `--e2e`**, por el encargo: Playwright sale inactivo en
  las cuatro. Los tests no se han tocado.
- Sigue como en la sesión 10: **la integración continua no se ha ejecutado
  nunca**, nada se ha ejecutado fuera de Windows y **un clon limpio**,
  tampoco.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Paso 1: las conversaciones y su índice~~ | Hecho (`4655810`) |
| ~~Paso 2: la nota de método en `ai-workspace/README.md` y sus tres remisiones~~ | Hecho (`1b84ee2`) |
| ~~Paso 3: la frase del README de la raíz~~ | Hecho (`41e15c4`) |
| **Parada 1: el Tech Lead revisa** los tres pasos, la tabla N-1 a N-9 y las precisiones AJ-01 a AJ-07. En particular: **si «revisa cada diff» y «revisa cada cambio» se quedan como están** (N-1), **si la nota debe decir de dónde salió el material previo de la sesión 01** (N-6) y **si las rutas de usuario de las conversaciones se quedan** (AJ-02) | Ahora |
| El «Estado» de `ai-workspace/README.md` sigue diciendo «al cerrar la sesión 10». Sus cifras no han cambiado y el encargo no pedía tocarlo | A decidir por el Tech Lead |
| **Prueba en limpio y `push`**. Tras el `push`, ver el primer resultado de la integración continua en Linux y en Windows y corregir lo que falle | Del Tech Lead; la corrección, en una sesión nueva |
| Poner al día `ai-workspace/README.md` («Estado») y el README de la raíz («solo se ha probado en Windows 11») cuando la integración continua y el clon limpio tengan resultado | Entonces |
| Pendientes heredados que esta sesión no toca: L-07 y los avisos de `npm audit`, los cuatro scripts de instalación sin aprobar, las fechas del fichero de bloqueo en el oráculo y los de la sesión 06 | A decidir por el Tech Lead |
