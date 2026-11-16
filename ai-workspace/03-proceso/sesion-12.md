# Sesión 12 · La nota de método corregida y las conversaciones sin rutas de usuario ni correo

| | |
|---|---|
| **Fecha** | 2026-11-16 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | Sesión abierta a las 16:06 |

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

*(La tabla de los pasos se rellena según se hacen.)*

Precisiones de la IA, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| AK-01 | **La sesión tendrá cinco commits**: este de apertura de la bitácora, los tres pasos y el cierre. En el de apertura solo entra `sesion-12.md`; las conversaciones siguen sin commit hasta el paso 1 | Es lo que se hizo en las sesiones 09 a 11 y lo admitido en AJ-01 |
| AK-02 | **El `git diff` es lo que dice el encargo, y además la IA ha visto cuatro cosas**, sin cambiar ninguna. (1) **El nombre de la carpeta de usuario sigue escrito, suelto, en dos líneas de `sesion-11.txt`** (221 y 350): son la fila AJ-02 de la bitácora de la sesión 11 tal como salió en pantalla, que dice cuál es el usuario de esas rutas. La sustitución cambió la ruta de esa fila, no esa frase. (2) **La bitácora de la sesión 11, que está versionada, lo lleva en dos líneas** (147, con la ruta y el nombre, y 195, con el nombre): `sesion-11.txt` enseña ahora esa fila con `<usuario>` y el fichero que esa conversación escribía dice el nombre. (3) **El historial**: el commit `4655810` conserva las 26 líneas, como dice el encargo, y el correo es el del autor de los 226 commits. (4) En `sesion-11.txt`, «❯» aparece también seis veces dentro del texto, citado; en las otras nueve conversaciones solo estaba al principio de línea | El encargo pedía decir si se veía otra cosa. La regla de `CLAUDE.md` habla de rutas locales; un nombre suelto no es una ruta, pero es justo lo que la sustitución retira. Las bitácoras antiguas no se tocan y los `.txt` no se editan: lo decide el Tech Lead |

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

## 5. No verificado

*(Se rellena al llegar a la parada 1.)*

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| Paso 1: las conversaciones regeneradas, `sesion-11.txt` y el índice al día | Ahora |
| Paso 2: la nota de método nueva en `ai-workspace/README.md` | Después |
| Paso 3: el apartado final de `pruebas-manuales.md` y el «Estado» | Después |
| Parada 1 y cierre de esta bitácora | Después |
