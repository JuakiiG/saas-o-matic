# Sesión 14 · Los textos que la sesión 13 dejó señalados, al día

| | |
|---|---|
| **Fecha** | 2026-11-17 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | **Parada 1 alcanzada (11:35): los tres pasos, hechos, cada uno en su commit y con el oráculo en código 0 antes, sin `--e2e`.** No ha cambiado el código de la aplicación, ningún test, ninguna spec ni el fichero de la CI: entre `3591202` y el último commit no cambia nada en `backend/`, `frontend/`, `scripts/`, `.github/` ni `01-specs/`. **Paso 1** (`d9b51b3`): `sesion-13.txt`, idéntica byte a byte a la que dejó el Tech Lead, y el índice al día, con el hecho F. **Paso 2** (`b1681fb`): la cabecera de `limitaciones-conocidas.md`, L-06 y ADR-005. **Paso 3** (`4f61c19`): el «Estado» al cerrar la sesión 14. **Lo que el Tech Lead tiene que conocer**: (1) **en `sesion-13.txt` no hay nada más que no deba publicarse**; (2) **L-06 sí tiene tests**: cuatro ficheros de test unitario del frontend comprueban ese `id`, y ni Playwright ni el guion manual lo recorren (AM-03); (3) **quedan frases que ya no son verdad en seis documentos que la IA no ha tocado**, porque el encargo no los nombra: `requisitos.md`, ADR-001, ADR-003, ADR-005 (otras dos, sobre `python-stdnum`), ADR-006 y el índice de `02-arquitectura/` (tabla del apartado 3); (4) la línea nueva del «Estado» no está bajo «Sin probar», sino como último hecho de la lista (AM-05). Quedan sin aprobar AM-01 a AM-06. · Antes, sesión abierta a las 11:22 |

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
| 11:29 | `573493e` | **Apertura de la bitácora**, 11:28:41 según `git log`, tras el oráculo sin `--e2e` de 11:27:16 a 11:28:41, código 0 (23 correctas, 1 inactiva); la salida, a un fichero, y el commit, en la misma orden, solo con ese código. Solo entra `sesion-14.md`: `sesion-13.txt` sigue sin commit (AM-01) |
| 11:29 | — | **Paso 1, el índice**: `conversaciones/README.md`, con la herramienta de edición, de 63 a 69 líneas. La tabla gana la sesión 13 (1.341 líneas) y dice «de la 01 a la 13»; «Lo que falta» nombra la sesión 14 en lugar de la 13; y «Qué se ha cambiado al publicarlas» gana un punto con el hecho F (AM-02). En `ai-workspace/README.md`, la fila de `03-proceso` de «Cómo leerlo» decía «sesiones 01 a 12» y dice «01 a 13»; era el único sitio (11:28:59). Los 27 destinos de los enlaces del índice existen. `sesion-13.txt` no se ha tocado: misma huella que a las 11:23:00 |
| 11:31 | `d9b51b3` | **Paso 1**, 11:30:43 según `git log`: `sesion-13.txt`, el índice y la fila de `ai-workspace/README.md`; tres ficheros, 1.351 líneas añadidas y 4 quitadas. Antes, oráculo sin `--e2e` de 11:29:18 a 11:30:43, código 0 (23 correctas, 1 inactiva). Después (11:30:43): **`sesion-13.txt` tiene en el commit la misma huella que el fichero que dejó el Tech Lead** y el de la carpeta sigue igual; `git ls-files --eol` dice `i/lf w/lf` |
| 11:31 | — | **Paso 2, tres textos desfasados**, con la herramienta de edición (11:31:01). (1) **La cabecera de `limitaciones-conocidas.md`**: «que se escribirá cuando el proyecto pueda levantarse en local» pasa a «Esta lista es la fuente del apartado «Límites» del `README.md` de la raíz, que remite a ella». (2) **L-06**: «el frontend todavía no existe, así que no hay test» pasa a decir los cuatro ficheros de test del frontend que lo comprueban y lo que no lo comprueba, Playwright y el guion manual (AM-03); cambia una sola línea de la tabla, sin ningún test nuevo. (3) **ADR-005, «No verificado»**: «en macOS y en Linux no se han ejecutado» queda tachada, y detrás, «Desde el 2026-11-17 pasan también en Ubuntu 26.04 y en Windows Server 2025, en la integración continua; en macOS no se han ejecutado nunca» (AM-04). Nada más de los dos ficheros cambia |
| 11:33 | `b1681fb` | **Paso 2**, 11:32:45 según `git log`: `limitaciones-conocidas.md` y ADR-005, 7 líneas añadidas y 5 quitadas. Antes, oráculo sin `--e2e` de 11:31:20 a 11:32:45, código 0 (23 correctas, 1 inactiva) |
| 11:33 | — | **Paso 3, el «Estado»** de `ai-workspace/README.md`, con la herramienta de edición, 18 líneas añadidas y 5 quitadas (11:33:11). (1) Dice «al cerrar la sesión 14 (las sesiones 11 a 14 solo han cambiado documentación)». (2) **La línea de «Sin probar» sobre los commits de la sesión 13 desaparece** y en su lugar hay un punto nuevo, el último de la lista de hechos, «Después de `3591202`»: los commits posteriores solo cambian documentación, los hechos D y E, y que la integración continua se ejecuta en cada `push`, con su resultado en la insignia, y que la ejecución descrita es la primera (AM-05). (3) «Sin probar» se queda con macOS y Linux a mano. **La comprobación del encargo**: `git diff --stat 3591202 -- backend frontend scripts .github`, vacío, y `git diff --name-only 3591202`, diez ficheros, ocho `.md` y dos `.txt`, todos el `README.md` de la raíz o de `ai-workspace/` (11:33:11, sobre el árbol de trabajo, con este paso ya escrito). Los 31 destinos de los enlaces del fichero existen; su línea más larga desde «Estado» tiene 75 columnas |
| 11:35 | `4f61c19` | **Paso 3**, 11:34:58 según `git log`: solo `ai-workspace/README.md`, 18 líneas añadidas y 5 quitadas. Antes, oráculo sin `--e2e` de 11:33:32 a 11:34:58, código 0 (23 correctas, 1 inactiva). Después (11:34:59): entre `3591202` y este commit cambian 10 ficheros, **ninguno en `backend/`, `frontend/`, `scripts/`, `.github/` ni `01-specs/`**; nada escucha en el 8000 ni en el 4200; `backend/data/saas-o-matic.db`, igual. La IA no ha arrancado ningún servidor ni ha hecho `push` |
| 11:35 | *(este commit)* | **Cierre de esta bitácora para la parada 1.** Las filas anteriores se han escrito cada una en su momento, con el reloj leído justo antes, y con el fichero sin commit entre la apertura y este cierre: los commits de los pasos llevan solo los ficheros de su paso. Antes de cerrar, contraste de cuatro candidatos del barrido de frases desfasadas (11:35:37). La IA para aquí: el Tech Lead revisa los tres pasos, lo que dice L-06, la tabla de frases que ya no son verdad y las precisiones AM-01 a AM-06. El `push` es suyo. La hora de este commit se ve con `git log` |

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

### Los tres pasos · lo hecho

| # | Commit | Qué toca |
|---|---|---|
| 1 · La conversación de la sesión 13 | `d9b51b3` | `sesion-13.txt`, tal como la dejó el Tech Lead; `conversaciones/README.md` (la tabla, «Lo que falta» y un punto nuevo en «Qué se ha cambiado al publicarlas»); y una fila de `ai-workspace/README.md` («01 a 13») |
| 2 · Tres textos desfasados | `b1681fb` | `04-calidad/limitaciones-conocidas.md`: la última frase de la cabecera y el final de la tercera columna de L-06. `02-arquitectura/ADR-005-dependencias-de-test.md`: una frase del primer punto de «No verificado» |
| 3 · El «Estado» | `4f61c19` | `ai-workspace/README.md`: la primera línea del «Estado», un punto nuevo al final de su lista y una línea menos en «Sin probar» |

Ningún test nuevo ni cambiado: no hay rojo ni mutación que anotar.

### Qué dice hoy L-06 y por qué

La fila decía: «Lo fija SPEC-04 (2.1 y tabla 5.7); el frontend todavía no
existe, así que no hay test». Es del 14/11, anterior al frontend. Hoy dice:

> Lo fija SPEC-04 (2.1 y tabla 5.7) y lo comprueban los tests unitarios del
> frontend, con ese mismo `id`, en cuatro ficheros de `frontend/src/app/`:
> `core/customer-id.spec.ts` (el filtro lo rechaza, igual que
> 9007199254740992, y admite 9007199254740991), `core/customer-loader.spec.ts`
> (la carga queda en «no encontrado» sin pedir nada),
> `features/detalle/detalle.spec.ts` y `features/simulador/simulador.spec.ts`
> (cada vista muestra «Cliente no encontrado» sin ninguna petición). Ninguna
> prueba de Playwright lo recorre en un navegador y el guion de pruebas
> manuales no lo incluye

Por qué, con lo que la IA ha leído en cada fichero (11:23:34 a 11:23:57):

| Fichero | Qué comprueba con `9007199254740993` |
|---|---|
| `core/customer-id.spec.ts` | `isRouteCustomerId` devuelve `false`; el caso se llama «16 digits above 2^53 − 1 (L-06)». En la misma tabla, `9007199254740992` también se rechaza, y `9007199254740991` está entre los que se aceptan. Es la frontera exacta de la limitación |
| `core/customer-loader.spec.ts` | El estado queda en `not-found` y no sale ninguna petición |
| `features/detalle/detalle.spec.ts` | Con la ruta `/clientes/9007199254740993`: ninguna petición del cliente, el título «Cliente no encontrado» y el enlace «Volver al panel». Es, letra por letra, lo que la fila dice que ocurre |
| `features/simulador/simulador.spec.ts` | Lo mismo en el simulador: ni petición del cliente ni de proyección, y «Cliente no encontrado» |

El código que lo hace, `core/customer-id.ts`, cita L-06 en un comentario.
En `frontend/e2e/` no aparece ese `id` ni «L-06», y en
`pruebas-manuales.md`, tampoco (11:26:03 y 11:31:01). **Los cuatro ficheros
los ejecuta el oráculo**, dentro de los tests del frontend, en las cinco
pasadas de esta sesión; la IA no los ha ejecutado por separado.

### Frases que ya no son verdad, fuera de bitácoras, evaluaciones y conversaciones

Lo pide el encargo. **Cómo se ha mirado**: una búsqueda de palabras que
hablan de futuro o de pendientes («todavía», «se escribirá», «cuando se
instale», «no verificado», «pendiente», «se comprobará»… ) en los 26
documentos `.md` versionados que no están en `03-proceso/` ni son informes
de evaluación o sus respuestas (11:23:57 y 11:24:20), y la lectura de cada
pasaje encontrado. Enteros, la IA solo ha leído el `README.md` de la raíz,
`ai-workspace/README.md`, el índice de las conversaciones,
`limitaciones-conocidas.md` y ADR-005. **Una frase caducada que no lleve
ninguna de esas palabras no la encuentra esta búsqueda.**

Corregidas en esta sesión: las tres del paso 2 y la línea del «Estado».
**Quedan, sin tocar, porque el encargo no las nombra**:

| Documento | Qué dice | Qué hay hoy |
|---|---|---|
| `00-analisis/requisitos.md`, «Sobre R-04» | La convención del CIF «**se contrastará**» con una prueba diferencial. «**Hoy no está contrastada**: la prueba no existe todavía y la biblioteca con la que se compara no se ha instalado» | La prueba existe, `backend/tests/unit/test_tax_id_differential.py`, con dos tests, y `python-stdnum` está instalada desde el 2026-11-13 (ADR-005). El oráculo la ejecuta |
| ADR-005, «No verificado», primer punto | «Con `python-stdnum` no se ha ejecutado nada todavía» | Lo mismo: la prueba diferencial la usa. Está en la misma frase que la del paso 2; no se ha tocado porque el encargo nombra solo la de Linux |
| ADR-005, «No verificado», tercer punto | Qué acepta `python-stdnum` para el CIF «es una hipótesis: se comprueba cuando se instale» | Está instalada y la prueba existe. La bitácora de la sesión 04 habla de esa biblioteca; la IA no la ha releído hoy para ver qué dio la comparación |
| ADR-005, «Consecuencias» | «Solo dos pruebas, en la fase de QA. Medido el 2026-11-15: las catorce pruebas de los cuatro grupos…» | Dudosa, no falsa: la medida lleva su fecha. Hoy el README de la raíz cuenta 18 pruebas de Playwright |
| ADR-001, apartado de Angular | «**No verificado** todavía: que el proyecto se cree, compile y pase sus tests con esa combinación; se comprobará al crearlo», repetido el 2026-11-14 («Sigue sin verificar») y, más abajo, «**No verificado todavía**: lo mismo dentro del repositorio, con la aplicación» | El frontend existe en el repositorio con esas versiones y sus tests pasan en el oráculo. La decisión sobre N-10, del encargo de la sesión 13, dejó ADR-001 como registro del 12/11; estas frases no eran el objeto de aquella decisión |
| ADR-001, apartado de SQLite | «Un test lo comprobará intentando guardar exactamente eso» (una simulación de un cliente que no existe) | Hay tests que esperan `sqlite3.IntegrityError` en `tests/integration/test_schema.py` y `test_customers_repository.py`. La IA no ha comprobado cuál de ellos es exactamente ese caso |
| ADR-003, «No verificado» | «la llamada desde un navegador real» | El guion de pruebas manuales del 16/11, en Chrome, recorre la API de divisas real y su caída (pasos 15, 18 y 28), todos en OK |
| ADR-006, «No verificado» | Que el framework permita los errores genéricos, la precedencia `415` > `400` > `422` y las cabeceras CORS en un `500`; y el rechazo de una comprobación previa, que «los fija un test al implementar» | El backend está implementado y hay tests de CORS y de errores genéricos (`test_cors.py`, `test_generic_errors.py`). **No contrastado punto por punto**: la IA no ha buscado el test de cada afirmación |
| `02-arquitectura/README.md`, «Pendiente» | «Estructura de carpetas definitiva de cada proyecto: se documenta al crearlos» | Los dos proyectos están creados. En esa carpeta no hay ningún documento con su estructura; la que hay está en `.claude/rules/backend.md` y `frontend.md`, que el mismo índice enlaza |
| `limitaciones-conocidas.md`, L-07 | «Cuándo se vuelve a mirar: […] y, como muy tarde, antes de cerrar la fase de QA» | La fase de QA se cerró y el README de la raíz da la cuenta del 2026-11-15, 27 avisos. La otra fecha, el 2026-11-20, no ha llegado. Es el pendiente heredado de L-07 |

Mirados y **sin nada que señalar**: el `README.md` de la raíz (su cuenta de
tests lleva fecha, 2026-11-16), `CLAUDE.md`, las reglas de `.claude/`,
`supuestos.md`, el índice de las specs, `trazabilidad.md` y
`pruebas-manuales.md`. En las cuatro specs, lo que la búsqueda encuentra
son notas con fecha que conservan el texto antiguo a propósito (SPEC-04,
«Sobre D-09», con su nota del 2026-11-15) y filas de historial. ADR-002
dice que la latencia en local «no está medida todavía»: la IA no ha
encontrado ningún documento que la mida, así que sigue siendo verdad.

### Precisiones de la IA, **sin aprobar**

| # | Precisión | Motivo |
|---|---|---|
| AM-01 | **La sesión tiene cinco commits**: el de apertura de la bitácora, los tres pasos y el cierre. En el de apertura solo entra `sesion-14.md`; `sesion-13.txt` sigue sin commit hasta el paso 1 | Es lo admitido en AL-01 |
| AM-02 | **Tres cosas del índice.** (1) El punto nuevo de «Qué se ha cambiado al publicarlas» dice el hecho F entero, **también lo del nombre de usuario de GitHub**, que no es un cambio sino algo que se deja. (2) «Lo que falta» dice de la sesión 14 lo mismo que decía de la 13, «no puede exportarse a sí misma antes de acabar»: el encargo dice que es la última, así que **esa entrada se queda así salvo que el Tech Lead publique después la conversación de la 14**. (3) En `sesion-13.txt` la IA no ha visto nada más que no deba publicarse y por eso hizo el commit sin preguntar. La cabecera lleva el plan de la herramienta («Claude Max») y la carpeta de trabajo (`Z:\saas-o-matic`), como las doce ya publicadas | (1) El encargo pide «lo del hecho F», y quien lea el índice después de leer que el correo se sustituyó tiene que saber que ese nombre está y por qué. (2) y (3) Para que conste lo que se ha mirado y lo que queda abierto |
| AM-03 | **L-06.** (1) La fila nombra los cuatro ficheros y lo que comprueba cada uno, y **añade lo que no lo comprueba**: ninguna prueba de Playwright y el guion manual. (2) Dice «con ese mismo `id`»: es el `9007199254740993` del ejemplo de la fila. (3) Lo demás de la fila no cambia, tampoco «Comprobado con Node el 2026-11-14» | (1) El encargo pedía «si un test lo cubre, cuál». Lo de Playwright y el guion no lo pedía: se dice porque «lo comprueban los tests» sin más se leería como que está visto en un navegador, y no lo está. Si sobra, se quita |
| AM-04 | **ADR-005.** (1) La fecha va como `2026-11-17`, no como «17/11/2026»: es la forma de las demás fechas de ese apartado. (2) La tachadura cubre solo «en macOS y en Linux no se han ejecutado»; lo anterior de la frase sigue valiendo. (3) «Pasan» es el hecho C de la sesión 13, la primera ejecución de la integración continua, sobre `3591202`: la IA no la ha visto. (4) **No se han tocado** la fila «Estado» de la cabecera del ADR («ampliado el 2026-11-13 […] y el 2026-11-15») ni su fila en el índice de `02-arquitectura/` | (1) El encargo pide «el mismo estilo que ya usa ese apartado». (4) Es una puesta al día de «No verificado», no una ampliación de la decisión |
| AM-05 | **Tres cosas del «Estado».** (1) **La línea que sustituye a la de los commits de la sesión 13 no está bajo «Sin probar»**: es el último punto de la lista de hechos, «Después de `3591202`». (2) **Gana una frase que el encargo no daba**: «Los commits de la sesión 14, posteriores a `c06630c`, no tocan el README de la raíz». (3) El paréntesis dice «las sesiones 11 a 14 solo han cambiado documentación», y **sus cifras siguen sin contarse de nuevo**: son las de la sesión 10 | (1) Lo que la línea dice ahora es lo que sí se ha probado; bajo «Sin probar» diría lo contrario de su título. «Sin probar» se queda con macOS y Linux a mano, como pide el encargo. (2) Los hechos D y E son sobre `c06630c`, y esta sesión añade cinco commits detrás: la frase dice por qué E sigue valiendo para el README de hoy, y seguirá siendo verdad después del `push`. Si sobra, se quita. (3) Como en AL-06 |
| AM-06 | **Errores de la IA en esta sesión**, ninguno llegó a un texto. (1) **Una búsqueda que dio «sin resultados» en falso**: la de «L-06» en `ai-workspace/` con un patrón de carpetas mal escrito (11:23:57); repetida con `grep` a las 11:26:03, encuentra las seis líneas de SPEC-04 y la de `limitaciones-conocidas.md`. (2) Una orden `grep` con una barra invertida al final falló al contar `Z:\` en las conversaciones (11:23:34); la cabecera se comparó con las tres primeras líneas de cada fichero. (3) En la primera búsqueda de frases desfasadas, «pendiente» encontraba también «independiente»: ruido, descartado al leer. (4) **Una frase mal escrita en la fila de las 11:33**: «todos el `README.md` de la raíz o de `ai-workspace/`» quiere decir que los diez ficheros son el `README.md` de la raíz y nueve de `ai-workspace/`. No se ha retocado: la lista exacta está en el apartado 4 | (1) Se anota porque la comprobación que vale es la segunda, y porque de la primera habría salido que ninguna spec cita L-06. (4) La bitácora no se retoca |

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

Paso 1:

| Qué | Cómo | Resultado |
|---|---|---|
| Que no quede ningún «01 a 12» | Búsqueda en los dos README y en el índice (11:28:59) | Ninguno |
| Los enlaces del índice | `test -e` de sus 27 destinos (11:28:59) | Existen todos |
| El ancho del índice | La línea más larga fuera de las tablas (11:28:59) | 76 columnas |
| **`sesion-13.txt` entra en el commit sin cambiar** | SHA-256 del fichero antes de tocar nada (11:23:00), antes del commit (11:28:59), tal como queda en `d9b51b3` (`git show`) y en la carpeta después (11:30:43) | Las cuatro, idénticas |
| Finales de línea de lo versionado | `git ls-files --eol` del fichero (11:30:43) | `i/lf w/lf` |

Paso 2:

| Qué | Cómo | Resultado |
|---|---|---|
| Qué tests tocan L-06 | Búsqueda de `9007199254740993`, `9007199254740991`, «2^53» y «L-06» en `frontend/`, y lectura de los cuatro ficheros de test y de `core/customer-id.ts` (11:23:34 a 11:23:57) | La tabla del apartado 3. Los cuatro ficheros existen y cada uno lleva ese `id` una vez (11:31:01) |
| Que Playwright y el guion no lo recorren | Búsqueda de «9007» y «L-06» en `frontend/e2e/` (11:26:03) y de «9007» y «2^53» en `pruebas-manuales.md` (11:31:01) | Ninguna aparición |
| En `limitaciones-conocidas.md` solo cambia la fila de L-06 | `git diff -U0`, contando las líneas cambiadas que empiezan por «\|» (11:31:01) | Dos: la fila antigua y la nueva |
| ADR-005, «No verificado» | Lectura del apartado después de editarlo (11:31:01) | La frase antigua, tachada, y la nueva detrás; 76 columnas como mucho |

Paso 3:

| Qué | Cómo | Resultado |
|---|---|---|
| **Los commits posteriores a `3591202` solo cambian documentación** | `git diff --stat 3591202 -- backend frontend scripts .github` y `git diff --name-only 3591202`, sobre el árbol de trabajo con el paso 3 escrito (11:33:11); y, con el commit hecho, `git diff --stat 3591202 HEAD -- backend frontend scripts .github ai-workspace/01-specs` (11:34:59) | Los dos `--stat`, vacíos. Cambian diez ficheros, ocho `.md` y dos `.txt`: el `README.md` de la raíz, `ai-workspace/README.md`, ADR-005, el índice de las conversaciones, `sesion-12.txt`, `sesion-13.txt`, las bitácoras de las sesiones 13 y 14, `limitaciones-conocidas.md` y `pruebas-manuales.md` |
| Los commits de la sesión 14 no tocan el README de la raíz | `git diff --name-only c06630c` (11:33:11) | Seis ficheros, todos en `ai-workspace/`: ADR-005, el índice, `sesion-13.txt`, esta bitácora, `limitaciones-conocidas.md` y `ai-workspace/README.md` |
| Que no queden las frases antiguas | Búsqueda de «sesión 13 (», «Los commits de la sesión 13» y «hasta el próximo» en `ai-workspace/README.md` (11:33:11) | Ninguna |
| Los enlaces de `ai-workspace/README.md` | `test -e` de sus 31 destinos (11:33:11) | Existen todos. El paso 3 no añade ni quita ninguno |
| Los mensajes de los commits | `git log 3591202..HEAD`, buscando trailers de coautoría o firmas de herramientas (11:34:59) | Ninguno |

Barrido de frases desfasadas:

| Qué | Cómo | Resultado |
|---|---|---|
| Palabras de futuro o de pendiente | Dos búsquedas en los 26 `.md` versionados que no están en `03-proceso/` ni son evaluaciones o respuestas (11:23:57 y 11:24:20), y lectura de los pasajes | La tabla del apartado 3 |
| Lo que hay hoy de cada candidato | Búsquedas en `backend/tests/` de `stdnum`, de `IntegrityError` y de las comprobaciones previas de CORS; en `pruebas-manuales.md`, de la API de divisas; y un listado de `02-arquitectura/` (11:24:37 y 11:35:37) | La columna «Qué hay hoy» de esa tabla |

Oráculo:

| Qué | Cómo | Resultado |
|---|---|---|
| **Antes de cada commit** | `uv run scripts/check.py`, sin `--e2e`; la salida, a un fichero fuera del repositorio, y el commit en la misma orden, solo con código 0 | Código 0 en las cuatro pasadas anteriores a este cierre (11:27:16, 11:29:18, 11:31:20 y 11:33:32): 23 correctas, 0 con fallo y 1 inactiva, Playwright |
| Puertos y base local al cerrar | `netstat` y un listado de `backend/data/` (11:34:59) | Ninguno en escucha; 28.672 bytes, 2026-11-14 18:37, como al empezar. La IA no ha arrancado ningún servidor |

## 5. No verificado

Al llegar a la parada 1:

- **Los hechos D, E y F**: son del Tech Lead y la IA no ha comprobado
  ninguno. No ha visto la otra sesión, ni su clon, ni sus dos pasadas del
  oráculo, ni los originales de las conversaciones. Lo que el «Estado» y
  el índice dicen de ellos es lo que dice el encargo.
- **Nada de lo que se dice de la sesión que audita**, como en las sesiones
  11 a 13.
- **La integración continua**: ni la primera ejecución (hecho C de la
  sesión 13), de la que sale la frase nueva de ADR-005, ni que se lance en
  cada `push`, que es lo que dice `ci.yml` y no se ha visto ocurrir desde
  aquí, ni lo que enseña la insignia. La IA no ha consultado la red.
- **Los commits de esta sesión no los ha ejecutado nadie más que el
  oráculo de esta sesión, sin `--e2e`**: Playwright sale inactivo en las
  cinco pasadas. Solo cambian documentación.
- **Los cuatro ficheros de test de L-06, por separado**: pasan dentro de
  los tests del frontend del oráculo; no se han lanzado solos ni se les ha
  hecho ninguna mutación en esta sesión.
- **Que el barrido de frases desfasadas sea completo**: es una búsqueda
  por palabras en 26 documentos, no una lectura entera de cada uno. De la
  tabla, dos filas no están contrastadas punto por punto (ADR-006 y el
  test de SQLite de ADR-001).
- **Las cifras del «Estado»** (741, 569, 18 y 96 tests, 140 requisitos,
  siete evaluaciones, once limitaciones): no se han vuelto a contar.
- **Que `sesion-13.txt` sea la conversación entera de la sesión 13**: la
  IA la ha leído entera y coincide con la bitácora de esa sesión, pero no
  tiene el original para compararla.
- **Si las conversaciones llevan contenido de los ficheros de
  `.private/`**: sigue como en las sesiones 11 a 13.
- **Cómo se ven los ficheros una vez publicados**: la tachadura de
  ADR-005, que cruza un salto de línea, la fila larga de L-06 y los
  enlaces nuevos del índice.
- **Ningún evaluador ha mirado los cambios de esta sesión**, ni los de las
  sesiones 09 a 13.
- **macOS**, nunca; **Linux a mano con un navegador**, tampoco.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Paso 1: `sesion-13.txt` y el índice al día~~ | Hecho (`d9b51b3`) |
| ~~Paso 2: la cabecera de `limitaciones-conocidas.md`, L-06 y ADR-005~~ | Hecho (`b1681fb`) |
| ~~Paso 3: el «Estado» de `ai-workspace/README.md`~~ | Hecho (`4f61c19`) |
| **Parada 1: el Tech Lead revisa** los tres pasos y las precisiones AM-01 a AM-06. En particular: **si la frase de L-06 sobre Playwright y el guion se queda** (AM-03); **si la línea nueva del «Estado» vale como último hecho de la lista** y si su frase sobre la sesión 14 se queda (AM-05); y **qué se hace con las frases que ya no son verdad** de `requisitos.md`, ADR-001, ADR-003, ADR-005, ADR-006 y el índice de `02-arquitectura/` | Ahora |
| El `push` de los commits de las sesiones 13 y 14, y ver la integración continua sobre ellos | Del Tech Lead |
| La conversación de la sesión 14 no está publicada: el índice lo dice | A decidir por el Tech Lead |
| Pendientes heredados que esta sesión no toca: L-07 y los avisos de `npm audit`, los cuatro scripts de instalación sin aprobar, las fechas del fichero de bloqueo en el oráculo y los de la sesión 06 | A decidir por el Tech Lead |
