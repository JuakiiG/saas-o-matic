# Sesión 14 · Los textos que la sesión 13 dejó señalados, al día

| | |
|---|---|
| **Fecha** | 2026-11-17 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | Sesión abierta a las 11:22 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

**La conversación es nueva**, sin el contexto de la sesión 13: la IA llega
con lo que ha leído al empezar (`CLAUDE.md`, `ai-workspace/README.md` y la
bitácora de la sesión 13, con sus pendientes) y con sus cuatro notas de
memoria.

**La segunda sesión de IA, «la que audita»**, sigue sin verse desde esta
conversación: lo que esta bitácora dice de ella es lo que dicen el encargo y
la nota de método. La fila de participantes de arriba nombra a quienes
hablan en esta conversación.

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 14, la última: se ponen al día los textos que la sesión 13 dejó
> señalados. Antes de nada, leer `CLAUDE.md`, `ai-workspace/README.md` y los
> pendientes de `03-proceso/sesion-13.md`. Abrir esta bitácora con el mismo
> formato que las anteriores.
>
> Parada 1 de la sesión 13 aprobada. Admitidas AL-01 a AL-07. Decisiones:
>
> - AL-03: los comentarios de los bloques se quedan como están.
> - AL-05: la insignia se queda. El repositorio va a estar en esa cuenta.
> - SPEC-04, 2.9, se queda como está: habla de orígenes, y
>   `http://127.0.0.1:4200` es otro origen aunque en este equipo no cargue.
> - La imprecisión de la bitácora de la sesión 13 (dice dos enlaces nuevos
>   y son tres) no se enmienda: se anota en la bitácora de esta sesión.
> - Lo demás, en los pasos de abajo.
>
> En esta sesión no cambia el código de la aplicación, ningún test, ninguna
> spec ni el fichero de la CI. Un commit por paso, con el oráculo en verde
> por su código de salida, sin `--e2e`. Sin `push`.
>
> Hechos nuevos, que son del Tech Lead y que la IA no tiene que comprobar:
> D (el oráculo con `--e2e` sobre `c06630c`), E (los tres bloques
> corregidos del README, seguidos en un clon) y F (qué se sustituyó al
> publicar `sesion-12.txt` y `sesion-13.txt`). Están enteros en el
> apartado 3.
>
> **Paso 1. La conversación de la sesión 13.** El Tech Lead ha dejado
> `sesion-13.txt` en `03-proceso/conversaciones/`, sin commit, con las
> mismas reglas que las demás. **No editarla.** Poner al día el índice: la
> tabla gana la sesión 13, la que falta es la 14, y «Qué se ha cambiado al
> publicarlas» dice lo del hecho F para la 12 y la 13. Si al mirar
> `sesion-13.txt` se ve algo más que no deba publicarse, decirlo antes de
> hacer el commit. Donde `ai-workspace/README.md` diga «01 a 12», pasa a
> «01 a 13».
>
> **Paso 2. Tres textos desfasados, en un commit:**
>
> - `limitaciones-conocidas.md`, cabecera: dice que el README de la raíz
>   «se escribirá». Ya existe: decirlo en presente.
> - `limitaciones-conocidas.md`, L-06: dice que «el frontend todavía no
>   existe, así que no hay test». Mirar qué hay hoy y escribir lo que sea
>   verdad: si un test lo cubre, cuál; si no, que no lo hay. Sin añadir
>   ningún test.
> - ADR-005, «No verificado»: la frase de que las pruebas de Playwright no
>   se han ejecutado en Linux. Con el mismo estilo que ya usa ese apartado
>   (lo antiguo tachado y la puesta al día con su fecha): desde el
>   17/11/2026 pasan en Ubuntu 26.04 y en Windows Server 2025, en la
>   integración continua; en macOS, nunca.
>
> **Paso 3. El «Estado» de `ai-workspace/README.md`, al cerrar la sesión
> 14.** La línea de «Sin probar» sobre los commits de la sesión 13 caduca
> con el próximo `push`: sustituirla por una que siga siendo verdad
> después. Lo que tiene que decir:
>
> - Los commits posteriores a `3591202` solo cambian documentación
>   (comprobarlo con `git diff` y decir la orden en la bitácora).
> - Los hechos D y E.
> - La integración continua se ejecuta en cada `push`: su resultado sobre
>   el último commit es el de la insignia del README de la raíz. La
>   ejecución que el «Estado» describe es la primera.
>
> macOS y Linux a mano siguen en «Sin probar».
>
> **Parar ahí (parada 1)** y cerrar la bitácora de la sesión 14. Decir qué
> cambió, qué dice hoy L-06 y por qué, y si queda en algún documento que no
> sea una bitácora, un informe de evaluación o una conversación alguna
> frase que ya no sea verdad. No leer ni citar `.private/`. El `push` lo
> hace el Tech Lead.

## 2. Cronología

Las horas son las del reloj del sistema (`date`), leído justo antes de
escribir cada fila; las de los commits se toman de `git log --format=%ci`
después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 11:26 | — | Mensaje recibido hacia las 11:22 (primera lectura del reloj, 11:22:47). El último commit es `c06630c` (2026-11-17 10:57:38), el cierre de la sesión 13; `main` va cinco commits por delante de `origin/main` (referencia local, sin consultar la red). **`git status`: solo `sesion-13.txt`, sin versionar**, que es lo que anunciaba el encargo. **`netstat` a las 11:23:00: nada escucha en el 8000 ni en el 4200.** `backend/data/saas-o-matic.db`, del Tech Lead: 28.672 bytes, 2026-11-14 18:37, como al cerrar la sesión 13; la IA no lo toca. Lecturas del encargo hechas, y además el índice de las conversaciones, `limitaciones-conocidas.md`, ADR-005, el `README.md` de la raíz y los cuatro ficheros de test del frontend que tocan L-06. **`sesion-13.txt`, leída entera sin editarla** (apartado 4): nada más que no deba publicarse. Barrido de frases desfasadas en los documentos que no son bitácoras, informes de evaluación ni conversaciones (11:23:57 a 11:24:37; el resultado, al cerrar). Apertura de esta bitácora |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (11:22)

**Parada 1 de la sesión 13, aprobada. Admitidas AL-01 a AL-07.** Sobre lo
que quedó pendiente:

| Qué | Decisión del Tech Lead |
|---|---|
| AL-03 · la carpeta de cada bloque de «Tests y oráculo», en una línea de comentario | **Los comentarios se quedan como están** |
| AL-05 · la insignia, con el nombre de usuario de GitHub | **Se queda.** El repositorio va a estar en esa cuenta |
| HE-4 · SPEC-04, 2.9, con `http://127.0.0.1:4200` como ejemplo de otro origen | **Se queda como está**: habla de orígenes, y `http://127.0.0.1:4200` es otro origen aunque en este equipo no cargue |
| La imprecisión de la bitácora de la sesión 13 | **No se enmienda**: se anota aquí (más abajo) |
| ADR-005, la cabecera de `limitaciones-conocidas.md` y L-06 | **Se corrigen** en el paso 2 |
| AL-02 · «Qué se ha cambiado al publicarlas» no decía nada de la 12 | **Se corrige** en el paso 1, con el hecho F |
| AL-06 · la línea de los commits de la sesión 13 en el «Estado» | **Se sustituye** en el paso 3 por una que siga siendo verdad después del `push` |

La bitácora de la sesión 13 no se toca: la aprobación queda anotada aquí.

**La imprecisión de la bitácora de la sesión 13, anotada por decisión del
Tech Lead.** En su apartado 4, la fila «Los enlaces de
`ai-workspace/README.md`» dice que sus 31 destinos existen «con los dos
nuevos: `../README.md` y `../.github/workflows/ci.yml`». **Los enlaces
nuevos eran tres**: falta el de `03-proceso/sesion-13.md`, que entró con el
mismo commit (`e965ce2`). Los 31 destinos existían; lo que está mal es la
cuenta. La IA lo dijo al cerrar la sesión 13, después del commit de cierre;
se ve al final de `sesion-13.txt`.

**Reglas de esta sesión**, del encargo:

- **No cambia el código de la aplicación, ningún test, ninguna spec ni el
  fichero de la CI.**
- **Un commit por paso**, con el oráculo en verde por su código de salida,
  **sin `--e2e`**.
- **`sesion-13.txt` no se edita**: entra tal como la dejó el Tech Lead.
- **En L-06 no se añade ningún test**: se escribe lo que hay.
- **La IA no hace `push`.**
- **`.private/` no se lee ni se cita.**

### Hechos nuevos del encargo

**Son del Tech Lead. La IA no los ha comprobado**, porque el encargo dice
que no tiene que hacerlo y porque no se pueden ver desde aquí: ni la otra
sesión, ni su clon, ni los originales de las conversaciones están en este
repositorio.

**D.** El 17/11, de 11:04 a 11:05, la sesión que audita ejecutó el oráculo
con `--e2e` sobre `c06630c`, el cierre de la sesión 13: 24 correctas, 0 con
fallo, 0 inactivas.

**E.** El 17/11, la sesión que audita siguió en su clon, puesto en
`c06630c`, los tres bloques corregidos de «Tests y oráculo» del README, en
PowerShell, tal como están escritos y empezando en `frontend/`, de 11:06 a
11:09: el primero, 23 correctas y 1 inactiva; el segundo, sin error; el
tercero, 24 correctas, 0 con fallo, 0 inactivas. Los tres con código 0, y
al acabar la terminal queda en la raíz del clon.

**F.** En `sesion-12.txt` y en `sesion-13.txt` no hubo nada que sustituir
al publicarlas: los originales no llevaban rutas de usuario ni correos.
Solo los finales de línea y los espacios finales. `sesion-13.txt` lleva dos
veces el nombre de usuario de GitHub del Tech Lead, en las dos líneas de la
insignia: es el mismo que ya está en el README y se queda.

### Los hechos D, E y F frente a lo que la IA ve en el repositorio

El encargo no lo pide. Se anota lo que se ha podido contrastar, mirado
entre las 11:22 y las 11:26, antes de tocar nada. **Nada los contradice.**

| Hecho | Qué dice el repositorio |
|---|---|
| D y E: son sobre `c06630c` | Es `HEAD`, el cierre de la sesión 13 (10:57:38), anterior a las 11:04 |
| D: 24 correctas, 0 con fallo, 0 inactivas, entre las 11:04 y las 11:05 | Es la cuenta de una pasada con `--e2e` (HE-2 de la sesión 13). Las cuatro pasadas sin `--e2e` de la sesión 13 duraron en este equipo entre 85 y 97 segundos: con Playwright, que añade unos 20 (ADR-005), la pasada cabe entre esas dos horas solo si son minutos sin segundos (de 11:04:00 a 11:05:59). La IA no sabe en qué equipo ni en qué copia se ejecutó |
| D: después, esta copia de trabajo sigue igual | A las 11:23:00 nada escucha en el 8000 ni en el 4200, la base local del Tech Lead tiene el tamaño y la fecha de antes, y `git status` solo enseña `sesion-13.txt` |
| E: los tres bloques, empezando en `frontend/` | El README de `c06630c` tiene esos tres bloques. El primero lleva «(desde frontend/: cd ..)» en un comentario: quien empieza en `frontend/` tiene que teclear ese `cd ..`; el comentario, pegado tal cual, no cambia de carpeta. El encargo dice que al acabar la terminal queda en la raíz del clon, que es donde deja el `cd ..` del segundo bloque |
| F: en la 12 y en la 13 no hay rutas de usuario ni correos | Es lo que la IA vio en `sesion-12.txt` (AL-02) y lo que ve en `sesion-13.txt` (apartado 4). Que los originales tampoco los llevaran solo lo sabe el Tech Lead |
| F: el nombre de usuario de GitHub, dos veces, en las dos líneas de la insignia | Dos apariciones, en las líneas 281 y 282 de `sesion-13.txt`, que son el trozo del cambio del README que añade la insignia. Es el mismo de `git remote get-url origin` |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short`, `git log --oneline -15` y `git branch -vv` (11:22:47 y 11:23:00) | `c06630c`; solo `sesion-13.txt`, sin versionar; `main`, cinco commits por delante de `origin/main` |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000 y 4200 (11:23:00) | Ninguno en escucha |
| La base local del Tech Lead | Listado de `backend/data/` (11:23:00) | 28.672 bytes, 2026-11-14 18:37 |
| El código, los tests y la CI, como en `3591202` | `git diff --stat 3591202 HEAD -- backend frontend scripts .github` y `git diff --name-only 3591202 HEAD` (11:26:03) | El primero, vacío. El segundo, los seis ficheros de la sesión 13: los dos README, el índice, `sesion-12.txt`, `sesion-13.md` y `pruebas-manuales.md` |

`sesion-13.txt`, **solo con órdenes de lectura**:

| Qué | Cómo | Resultado |
|---|---|---|
| Forma | `wc`, bytes de retorno de carro, líneas con espacios finales, último byte y «❯» (11:23:00) | 1.341 líneas y 70.995 bytes; ningún retorno de carro ni espacio final; acaba en salto de línea. «❯»: 2, las dos al principio de línea (el `/clear` y el encargo de la sesión 13) |
| **Leída entera** | La herramienta de lectura, de la línea 1 a la 1.341 (11:23:16) | Empieza con el `/clear` y el encargo de la sesión 13 y acaba con la respuesta de la parada 1, un «※ recap» y dos comentarios «buddy». Es la conversación que describe la bitácora de la sesión 13: los mismos pasos, commits y precisiones |
| Lo que no debe publicarse | Búsquedas de rutas de usuario (`Users`, `AppData`, `/home/`), de cualquier email, de `noreply`, de `<usuario>`, del nombre y las iniciales del Tech Lead, del nombre de usuario de GitHub, de palabras de secretos (`token`, `password`, `secret`, `ghp_`…), de teléfonos, de direcciones IP y de URL (11:23:16 y 11:26:03) | **Nada nuevo.** Ninguna ruta de usuario, ningún email, ningún secreto, ningún teléfono; ni el nombre ni las iniciales del Tech Lead. `Users` y `AppData`, una vez, y `noreply` y `<usuario>`, en tres líneas: son texto de la bitácora de la sesión 13 que habla de las búsquedas. La única IP es `127.0.0.1`. Las URL: `localhost`, `127.0.0.1`, `[::1]` y las dos de GitHub de la insignia. **El nombre de usuario de GitHub, dos veces** (hecho F). `.private/`, cinco veces, siempre el nombre de la carpeta y nunca su contenido |
| La cabecera | Las tres primeras líneas, comparadas con las de las otras doce (11:23:34) | Como todas: la versión de la herramienta (v2.1.326), «Fable 5.2 · Claude Max» y `Z:\saas-o-matic`, la carpeta de trabajo. Las doce ya publicadas llevan lo mismo; no es nuevo |
| Huella antes del commit | `sha256sum`, guardada fuera del repositorio (11:23:00) | Para compararla con lo que quede en el commit del paso 1 |

## 5. No verificado

*(Se escribe al cerrar.)*

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| Paso 1: `sesion-13.txt` y el índice al día | En curso |
| Paso 2: la cabecera de `limitaciones-conocidas.md`, L-06 y ADR-005 | Después |
| Paso 3: el «Estado» de `ai-workspace/README.md` | Después |
| Parada 1 | Al acabar el paso 3 |
