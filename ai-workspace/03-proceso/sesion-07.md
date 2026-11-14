# Sesión 07 · Frontend: armazón, lo común de `core/`, `/meta`, panel, alta, detalle y simulador en EUR

| | |
|---|---|
| **Fecha** | 2026-11-14 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | **Parada 2 alcanzada (17:01): alta, detalle y simulador en EUR**, en siete commits de código de una tarea cada uno (`e33c800` a `35a2a2f`), todos con el oráculo en verde antes y, los que traen comportamiento nuevo, con su test visto en rojo antes. 458 tests en 15 ficheros, 99,18 % de líneas. Las cuatro rutas de la spec existen. **Un error de la IA que el Tech Lead tiene que conocer (Z-14)**: al comprobar el recorrido con `curl`, la IA escribió en la base de datos local del Tech Lead un cliente y una simulación, porque su backend de prueba no arrancó y las peticiones fueron al que el Tech Lead tenía abierto. **Nada se ha visto en un navegador.** Quedan sin aprobar las precisiones Z-01 a Z-20. · **Antes, parada 1 (15:27), aprobada a las 16:03**: el frontend existe, con el armazón, lo común de `core/`, `/meta` y el panel**, en nueve commits de una tarea cada uno (`0e9966e` a `29d1e11`), todos con su test visto en rojo antes y el oráculo en verde. 221 tests, 98,83 % de líneas. Antes, un commit de documentación (`6b66622`: el margen de npm en ADR-007, las versiones en ADR-001 y la limitación L-07). **Un imprevisto**: al activarse las comprobaciones del frontend, el oráculo no podía ejecutar `npm` en Windows con Python 3.12.0; la IA paró sin tocar `scripts/`, el Tech Lead decidió que lo corrigiera y se hizo con test en rojo y commit propio (`6859f61`). El oráculo queda con 23 comprobaciones correctas y 1 inactiva (Playwright). El fichero de bloqueo tiene 650 versiones, ninguna posterior a la fecha de corte. **Nada se ha visto en un navegador**: eso es la parada. Quedan sin aprobar las precisiones Y-01 a Y-13 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

**La conversación es la misma que la de la sesión 06, sin `/clear`**, por
decisión del Tech Lead: el ensayo de npm y del CLI que sostiene el plan
está en el contexto de la IA. Consecuencia que conviene tener presente al
revisar: la IA llega a esta sesión con lo que leyó y probó en la anterior,
no con un contexto limpio, y parte de ese contexto es un resumen de la
propia conversación, no la conversación entera.

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Plan del frontend aprobado. Decisiones sobre P-01 a P-09 (en la bitácora
> de la sesión 06, apartado 3). Admitidas X-01 a X-10; en X-01 vale: `015`
> es válido y vale 15.
>
> Antes de crear nada: cerrar la bitácora de la sesión 06 con su resultado
> y hacer su commit; abrir `03-proceso/sesion-07.md` para el frontend, con
> el mismo formato (la conversación sigue sin `/clear`, porque el ensayo
> está en el contexto de la IA, y hay que decirlo en la bitácora); y un
> commit de documentación con el mecanismo del margen y las versiones en
> ADR-007 y ADR-001, y la fila L-07.
>
> Después, las piezas 0 a 3 como dice el plan: una tarea, un test en rojo
> visto antes del código, un commit, con el oráculo en verde. El commit del
> armazón trae ya los tres scripts pasando, la comprobación del fichero de
> bloqueo anotada en la bitácora y el apartado «Qué comprueba hoy el
> oráculo» de `CLAUDE.md` al día.
>
> **Parar en la parada 1, después del panel.** En ese mensaje: las órdenes
> exactas, en PowerShell, para arrancar el backend y el frontend en local;
> qué va a ver el Tech Lead en `http://localhost:4200` con la base de datos
> recién creada; y qué no se ha podido comprobar sin navegador.

Dos frases del mensaje llegaron cortadas. La IA las lee así, y lo dice
para que el Tech Lead lo corrija si no es eso: «la comprobe bloqueo
anotada en la bitácora» es la comprobación de las fechas del fichero de
bloqueo; y «con la base de», la base de datos recién creada, sin clientes.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 14:23 | — | El cierre de la sesión 06 es `ca8f7af` (14:23:04 según `git log`), con el oráculo en verde antes. `git status` limpio. Apertura de esta bitácora |
| 14:35 | `6b66622` | Fila escrita a las 14:35. Commit de documentación (14:25:45 según `git log`): el mecanismo del margen en ADR-007, las versiones exactas en ADR-001 y la fila L-07. Oráculo en verde antes |
| 14:35 | — | Fila escrita a las 14:35. **Pieza 0, armazón.** 14:26: `ng new` con la orden aprobada (23 ficheros). 14:27: quitado lo de la tabla de P-04 (`.vscode/`, `README.md`, `.gitignore` y `public/favicon.ico`, con sus carpetas). Versiones exactas y scripts en `package.json`, `.npmrc`, `.prettierignore`, `eslint.config.js`, `angular.json` e `index.html`, con las herramientas de edición. 14:28: `npm install` con la fecha de corte. 14:29: fechas del fichero de bloqueo comprobadas (apartado 4). 14:30: `ng generate environments` y `npm audit` |
| 14:35 | — | Fila escrita a las 14:35. **Rojo visto a las 14:30:43**: los tres tests de `app.spec.ts` fallan por aserción contra la página de bienvenida del CLI (apartado 4). Después, el armazón: `app.ts`, `app.html`, `app.css` y los estilos globales. 14:31: `prettier --write`; `npm run lint`, `npm run build` y `npm run test:ci` pasan, ejecutados a mano en `frontend/` |
| 14:35 | — | **El oráculo, en rojo a las 14:33, y no por el frontend**: no consigue ejecutar `npm` (`[WinError 193] %1 no es una aplicación Win32 válida`) en las tres comprobaciones que acaban de activarse. Causa, comprobada a las 14:34: `scripts/oracle/repo.py` localiza el ejecutable con `shutil.which('npm')`, y con el Python que usa `uv` en este equipo (3.12.0) eso devuelve el fichero `npm` sin extensión, un script de shell que Node instala junto a `npm.cmd` y que Windows no puede ejecutar. **La IA no toca `scripts/` ni hace el commit del armazón con el oráculo en rojo: para y pregunta.** Todo lo de la pieza 0 queda preparado (`git add`) y sin commit |
| 14:46 | — | Fila escrita a las 14:50. **El Tech Lead decide**: la IA corrige `scripts/oracle/repo.py`, con condiciones (apartado 3) |
| 14:50 | `6859f61` | Corrección del oráculo (14:49:37 según `git log`), con solo sus dos ficheros. **Rojo visto a las 14:47:39** en `scripts/tests/test_repo.py`: el test reproduce el `WinError 193` y falla por aserción. Después del cambio, sus 2 tests y los 75 del oráculo pasan, y el oráculo entero queda en verde con el frontend activo: 23 correctas, 0 con fallo y 1 inactiva |
| 14:50 | *(este commit)* | **Armazón** (pieza 0, primera tarea). Trae los tres scripts pasando por el oráculo, esta bitácora con la comprobación del fichero de bloqueo, `CLAUDE.md` con «Qué comprueba hoy el oráculo» al día y L-07 con el recuento del proyecto. Se quita `frontend/.gitkeep`, que guardaba la carpeta vacía |
| 14:55 | `0e9966e`, `e2262da` | El armazón es `0e9966e` (14:51:40 según `git log`). **Pieza 0, segunda tarea: página «no encontrada»** (E-34), `e2262da` (14:55:00). Rojo visto a las 14:53:08: los 2 tests fallan por aserción, porque la navegación a una ruta desconocida se rechaza (`NG04002: Cannot match any routes`). Oráculo en verde antes del commit. Hasta que llegue el panel, también `/` cae en esa página |
| 15:00 | `3f7ced1` | **Pieza 1a, medidas de texto** (E-41, E-45, la medida de E-50), 14:57:35. Rojo visto a las 14:55:34: 11 de 24 tests fallan por aserción contra unas funciones que solo tenían la firma (`text.length`, `trim()`). Oráculo en verde antes del commit |
| 15:00 | `16dcad4` | **Pieza 1b, filtro del `id` de la ruta** (E-47, forma de E-15), 14:59:49. Rojo visto a las 14:57:51: 15 de 21 fallan por aserción. El límite de 2^53 − 1 se compara sobre el texto, sin convertirlo en número. Oráculo en verde antes |
| 15:07 | `16a0cdc` | **Pieza 1c, formato del dinero** (E-28, formato de E-29; CA-01), 15:03:22. Rojo visto a las 15:01:04: 48 de 49 fallan por aserción. El *pipe* reproduce las 36 celdas de la tabla de importes de 5.1. Para que pueda mostrar otra divisa hace falta saber cuál está elegida: la IA ha puesto ya en `core/` el estado de la divisa mostrada, que empieza en EUR; el servicio de tipos y el selector siguen siendo de la pieza 7 (Y-02). El formato de fechas no se ha hecho aquí: va con las vistas que las muestran (Y-03). Oráculo en verde antes |
| 15:07 | `c08199a` | **Pieza 1d, errores por su `code`** (E-11, E-42, E-43 y el reparto de E-09 y E-48; CA-06), 15:06:37. Rojo visto a las 15:04:27: 33 de 35 fallan por aserción. Oráculo en verde antes |
| 15:12 | `7acce64` | **Pieza 1e, cliente de la API** (E-32, E-33, E-51, E-52 y los cuerpos de E-46, E-47 y E-49; CA-10), 15:11:44. Un primer intento, a las 15:09:01, no llegó a ejecutarse: el propio test no compilaba por un tipo (`unknown` donde hacía falta `object`); corregido el test, **rojo visto a las 15:09:16**: 35 de 35 fallan por aserción. Un solo servicio para las cinco llamadas; el `id` de un cliente es un tipo que solo da el filtro de la pieza 1b. `provideHttpClient()` en la configuración de la aplicación, sin interceptores. Oráculo en verde antes |
| 15:16 | `cd9e186` | **Pieza 2, `/meta`** (E-39, E-35, E-40 y la fuente de E-05), 15:15:49. Dos rojos vistos: a las 15:12:47, 17 tests fallan por aserción (los 5 de la llamada y 12 del almacén); a las 15:13:42, el de que la aplicación pide `/meta` al arrancar (`expected [] to deeply equal [ '…/meta' ]`). Al añadir ese test la IA cambió sin motivo una aserción de otro test del armazón (`h1` por `header h1`) y la devolvió a como estaba antes de ejecutar nada más (Y-04). Los tests que usan la configuración real de la aplicación sustituyen ahora la red. Oráculo en verde antes |
| 15:27 | `29d1e11` | Fila escrita a las 15:27. **Pieza 3, panel** (E-01 a E-04, E-50, E-51, E-53, E-54; CA-04), 15:23:53. **Rojo visto a las 15:18:18**: 34 de 36 tests fallan, con el componente reducido a su título; todas las líneas de error recogidas son `AssertionError` (Y-06). Con el código, los 36 pasan a la primera. El oráculo, en cambio, **salió en rojo a las 15:21**: ESLint señaló que el test del panel importaba el fichero de entorno, y una feature solo puede salir hacia `core/` o `shared/`. La regla no se tocó: `core/` exporta la URL base del backend y el test la toma de ahí. Oráculo en verde antes del commit. Recorrido de `frontend/src` con Python: ningún carácter invisible |
| 15:27 | — | Fila escrita a las 15:27. **Comprobación de las órdenes de arranque, sin navegador** (15:24 a 15:25): backend con `uv run --locked uvicorn --factory app.main:create_app` y una base de datos en la carpeta temporal, y frontend con `npm start`; peticiones con `curl`; los dos procesos, parados por su PID (apartado 4). No se ha creado `backend/data/` |
| 15:27 | *(este commit)* | Cierre de esta bitácora para la **parada 1**. La IA para aquí: el Tech Lead revisa las piezas 0 a 3 y abre la aplicación en el navegador |
| 16:03 | — | El commit anterior es `530e909` (15:28:52 según `git log`). **El Tech Lead aprueba la parada 1**, después de abrir la aplicación en Chrome con el backend real; admite Y-01 a Y-13 con cuatro cambios y manda seguir con las piezas 4 a 6 hasta la parada 2 (apartado 3). La bitácora sigue en este fichero: el encargo de la sesión 07 es el frontend |
| 16:12 | `1967209`, `6cd21b5`, `8d09fe6`, `4703eb9` | Fila escrita a las 16:12. **Los cuatro cambios de la revisión**, un commit cada uno y con el oráculo en verde antes: SPEC-04 recoge las reglas de Y-07 (16:05:38), con un test nuevo del panel que nace en verde porque el código ya lo hacía; la regla 9 de `CLAUDE.md` (16:07:34); `.claude/rules/frontend.md` (16:09:23); y el corrector ortográfico del buscador (16:11:28), con su **rojo visto a las 16:09:26** (`expected null to be 'false'`) y la regla escrita en SPEC-04 2.8. Al escribir Y-07 en la spec la IA añadió una regla más, que el Tech Lead no ha visto (Z-01) |
| 16:28 | `e33c800` | Fila escrita a las 16:28. **Refactor sin cambio de comportamiento**, 16:14:32: el estado de `/meta` (cargando, error con «Reintentar» o el contenido) pasa del panel a un componente compartido, `shared/meta-gate.ts`, porque el alta, el detalle y el simulador lo necesitan igual. Sin test nuevo: los 35 del panel siguen en verde. Oráculo en verde antes. Nadie lo pidió (Z-03) |
| 16:28 | `c4ef635` | **Pieza 4, alta de cliente** (E-05 a E-11, E-40, E-41, E-44 a E-46; CA-05, CA-06 y las filas de `POST /customers` de CA-16), 16:27:53. **Primer rojo, a las 16:16:00, no válido**: el test no compilaba (`TS2345`, un error del propio test). Corregido el test, **rojo por aserción a las 16:18:37**: 44 de 47. Antes de escribir el componente la IA rehízo los tests para seguir CA-05 al pie de la letra (Z-04) y volvió a ver el rojo, **a las 16:23:29: 56 de 59 fallan, todos `AssertionError`**; los 3 que pasan son las filas de rutas que ya existían. Verde a las 16:25:45 (59 de 59) y oráculo en verde a las 16:26 |
| 16:43 | `e96d1a5` | Fila escrita a las 16:43. Commit de esta bitácora con la revisión de la parada 1 y la pieza 4, 16:30:48, con el oráculo en verde antes |
| 16:43 | `e7aea4f` | **Pieza 5a, carga del cliente de la ruta** (E-15, E-47, E-32, E-33; CA-10), 16:34:52. `core/customer-loader.ts`, que usan el detalle y el simulador. Rojo visto a las 16:32:25: 20 de 20 fallan por aserción. Verde a las 16:32:54. Oráculo en verde antes |
| 16:43 | `76051f7` | **Pieza 5b, formato de fechas y de recuentos** (SPEC-04 2.8), 16:37:51. Rojo visto a las 16:35:31: 9 de los 13 tests nuevos fallan por aserción; los otros 4 son valores que la firma trivial ya devolvía igual (`ayer`, 0, 15 y 1000). Los valores esperados se sacaron antes sondeando `Intl` con `node -e`, sin escribir nada. Oráculo en verde antes |
| 16:43 | `f3179e9` | **Pieza 5c, detalle del cliente** (E-12 a E-15, E-35, E-40, E-47; CA-07, CA-17 y las filas de `GET /customers/{id}` de CA-16), 16:43:17. Rojo visto a las 16:40:01: 36 de 40 fallan por aserción (los 35 del detalle y la fila nueva de rutas). Verde a las 16:41:13 y oráculo en verde a las 16:43 |
| 17:01 | `d4a60f7` | Fila escrita a las 17:01. **Pieza 6a, el reparto de un error de formulario pasa a `core/`** (E-09, E-11, E-48), 16:49:25. `formErrors` en `core/api-error.ts`; el alta deja su copia y sus 55 tests siguen en verde sin tocarlos. Rojo visto a las 16:46:53: 9 de los 10 tests nuevos fallan por aserción. Oráculo en verde antes |
| 17:01 | `35a2a2f` | **Pieza 6b, simulador en EUR** (E-15, E-17 a E-25, E-35 a E-38, E-40, E-47 a E-49, E-55; CA-08 menos sus dos filas de divisa, CA-17 y las filas de la proyección y del guardado de CA-16), 16:59:05. Rojo visto a las 16:51:36: fallan por aserción los 100 tests nuevos. **Primer intento de verde, a las 16:54:03, con 11 fallos**: «Guardar» no enviaba nada, por un defecto del código y no de los tests (Z-16). Verde a las 16:54:41, pero con `simulador.ts` en 340 líneas y su plantilla en 121: se dividió por responsabilidad sin tocar los tests (Z-15) y volvió a verde a las 16:56:57. Oráculo en verde a las 16:58 |
| 17:01 | — | **Comprobación del recorrido con `curl`, y un error de la IA** (16:59 a 17:01). La IA arrancó un backend con una base de datos temporal sin mirar antes si el puerto 8000 estaba libre. **No lo estaba**: lo ocupaba el backend del Tech Lead (PID 2916), el de la IA no llegó a arrancar y las peticiones fueron al del Tech Lead. **Se crearon en `backend/data/saas-o-matic.db` un cliente y una simulación** (Z-14). La IA no ha tocado ese fichero ni ese proceso. Después repitió la comprobación con un backend propio en el puerto 8001, comprobado libre antes, y lo paró por su PID (apartado 4) |
| 17:01 | *(este commit)* | Cierre de esta bitácora para la **parada 2**. La IA para aquí: el Tech Lead revisa las piezas 4 a 6 y hace el recorrido en el navegador |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (14:18)

Las de P-01 a P-09 y la admisión de X-01 a X-10 están en la bitácora de la
sesión 06, que es donde se propusieron. Las que fijan cómo se trabaja en
esta sesión:

| Qué | Decisión del Tech Lead |
|---|---|
| Orden | Primero la documentación (ADR-007, ADR-001 y L-07), en su commit; después las piezas 0 a 3 |
| Ritmo | Una tarea, un test en rojo visto antes del código, un commit, con el oráculo en verde |
| El commit del armazón | Trae los tres scripts pasando, la comprobación del fichero de bloqueo anotada aquí y `CLAUDE.md` al día |
| Qué puede escribir en `frontend/` desde la terminal | `ng new`, `ng generate`, `npm install`, `npm ci` y `prettier --write`, y nada más (P-05) |
| Parada | La 1, después del panel, con las órdenes de PowerShell, lo que se verá en el navegador y lo no comprobado |

### El oráculo no podía ejecutar npm (14:33–14:49)

**Qué pasó.** Al existir `frontend/package.json`, las tres comprobaciones
del frontend se activaron y las tres fallaron igual, sin llegar a ejecutar
nada: «no se pudo ejecutar `npm run lint`: [WinError 193] %1 no es una
aplicación Win32 válida».

**Con qué falla y cómo se reprodujo.** Con **Python 3.12.0**, que es el que
`uv` usa en este equipo para el script del oráculo (`uv python list
--only-installed`). Node instala en la misma carpeta `npm` (un script de
shell, sin extensión), `npm.cmd` y `npm.ps1`. Con ese Python,
`shutil.which('npm')` devuelve el fichero sin extensión y
`shutil.which('npm.cmd')`, el `.cmd`; Windows no puede arrancar el primero.
Reproducido de tres maneras: con el oráculo entero (14:33), con una línea
de Python que llama a `shutil.which` (14:34) y con el test nuevo, que crea
en una carpeta temporal una herramienta con esos dos ficheros gemelos y la
arranca con `repo.run` (14:47). **No comprobado**: con qué versiones de
Python deja de ocurrir; la IA recuerda que las posteriores a la 3.12.0 lo
cambian, y no lo ha visto.

**Por qué no se había visto.** Las comprobaciones del frontend no se habían
ejecutado nunca: estaban inactivas. Los tests del oráculo las prueban con
un ejecutor simulado, que no arranca ningún proceso.

**Propuesta de la IA y decisión del Tech Lead (14:46).** La IA paró sin
tocar `scripts/` ni hacer el commit del armazón, y planteó tres salidas:
corregir `repo.py` (recomendada), que lo corrigiera el Tech Lead, o
instalar un Python más reciente. **Decisión: la primera, con condiciones**:

| Condición | Cómo se cumple |
|---|---|
| Test en rojo visto antes, en `scripts/tests/`, y los tests del oráculo en verde después | `test_repo.py`: rojo a las 14:47:39, por aserción. Después, 75 tests del oráculo correctos (eran 73) |
| Commit propio, anterior al del armazón | `6859f61`, con solo `scripts/oracle/repo.py` y `scripts/tests/test_repo.py`; lo del armazón siguió preparado y sin commit |
| No toca umbrales ni qué comprobaciones se ejecutan; solo cómo se localiza el ejecutable en Windows | Una función nueva, `find_executable`, que `repo.run` usa en lugar de `shutil.which`. Fuera de Windows devuelve lo mismo que antes. En Windows, si lo encontrado no tiene una extensión de `PATHEXT`, prefiere el fichero gemelo que sí la tiene. `checks_stack.py` y los umbrales no cambian |
| Anotado aquí, con la versión de Python y cómo se reprodujo | Este apartado |

### Piezas 0 a 3 · lo hecho (14:26–15:24)

Una tarea, un commit. El rojo de cada una se vio antes de escribir su
código, y el oráculo estaba en verde antes de cada commit.

| Pieza | Commit | Rojo visto | Requisitos | Tests |
|---|---|---|---|---|
| 0 · Armazón | `0e9966e` | 14:30:43, 3 de 3 | SPEC-04 2.1 y 2.9 | 3 |
| 0 · Página «no encontrada» | `e2262da` | 14:53:08, 2 de 2 | E-34 | 2 |
| 1a · Medidas de texto | `3f7ced1` | 14:55:34, 11 de 24 | E-41, E-45, medida de E-50 | 24 |
| 1b · Filtro del `id` | `16dcad4` | 14:57:51, 15 de 21 | E-47, forma de E-15 | 21 |
| 1c · Formato del dinero | `16a0cdc` | 15:01:04, 48 de 49 | E-28, formato de E-29 | 49 |
| 1d · Errores por su `code` | `c08199a` | 15:04:27, 33 de 35 | E-11, E-42, E-43, reparto de E-09 y E-48 | 35 |
| 1e · Cliente de la API | `7acce64` | 15:09:16, 35 de 35 | E-32, E-33, E-51, E-52, cuerpos de E-46, E-47 y E-49 | 35 |
| 2 · `/meta` | `cd9e186` | 15:12:47, 17 de 52; 15:13:42, 1 de 6 | E-39, E-35, E-40, fuente de E-05 | 18 más |
| 3 · Panel | `29d1e11` | 15:18:18, 34 de 36 | E-01 a E-04, E-50, E-51, E-53, E-54 | 34 más |

Al cerrar: **221 tests en 10 ficheros, todos correctos; 98,83 % de líneas**
(169 de 171), con el umbral en 80. Compilación de producción: 247,43 kB
iniciales, con el panel y la página «no encontrada» en trozos de carga
diferida. El fichero de código más largo tiene 141 líneas (`panel.ts`) y
la plantilla del panel, 77.

Precisiones de la IA, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| Y-01 | Los componentes, el servicio, el almacén y el *pipe* se han escrito a mano con las herramientas de edición, con el nombre de fichero que les daría el CLI. `ng generate` solo se ha usado para los ficheros de entorno. `.claude/rules/frontend.md` dice que se usan los generadores | El generador escribe el componente y su test a la vez, y aquí el test va antes y se ve fallar |
| Y-02 | El estado de la divisa mostrada (`core/display-currency.ts`, que empieza en EUR) se ha hecho en la pieza 1c y no en la 7 | CA-01 pide que el *pipe* reproduzca las celdas en USD, GBP y CHF, y sin saber qué divisa está elegida no puede. El servicio de tipos y el selector siguen en la pieza 7 |
| Y-03 | El formato de fechas no se ha hecho en la pieza 1c, donde el plan lo ponía | Depende de la zona horaria y no lo usa nada todavía: va con el detalle (pieza 5) y con las divisas (pieza 7) |
| Y-04 | Al añadir un test, la IA cambió una aserción de otro ya aprobado en verde (`h1` por `header h1`) sin necesidad. La devolvió a como estaba antes de ejecutar nada | Es relajar un test, aunque no llegara a ejecutarse así |
| Y-05 | **Para que el rojo sea por aserción y no por importación, cada test se escribió junto con un fichero que solo tenía las firmas**, con cuerpos triviales (`return text.length`, `return EMPTY`, una plantilla con solo el título). TypeScript no compila un test que importa algo que no existe. Ese fichero es código escrito antes de ver el rojo | Es la única forma que la IA ha encontrado de cumplir «por aserción, no por importación» en TypeScript; si el Tech Lead prefiere otra, se cambia |
| Y-06 | Del rojo del panel se guardó el recuento (34 de 36) y las líneas de error, 28 y todas `AssertionError`; no la salida entera. En las piezas 1c y 1d el recuento hubo que sacarlo con una segunda ejecución, unos segundos después | La orden recortaba la salida |
| Y-07 | **Reglas que la spec no dice y la IA ha puesto**: (a) una entrada de `errors` sin la forma del contrato se ignora; (b) un segundo error del mismo campo va al aviso general; (c) el panel pide su lista aunque `/meta` esté cargando o haya fallado, y la enseña cuando `/meta` llega; (d) los textos que la spec no fija: «Cargando…», «Cargando clientes…», el título «Clientes», «Nuevo cliente», «Dar de alta el primer cliente», «Volver al panel» y la frase de la página «no encontrada» | Ninguna es una regla de negocio, pero las ha decidido la IA |
| Y-08 | La URL del backend es `http://127.0.0.1:8000` en los dos ficheros de entorno. La spec no la fija | Es donde escucha `uvicorn` por defecto; comprobado con `curl` que también responde en `localhost:8000` |
| Y-09 | Un solo servicio, `BackendApi`, para las seis llamadas, y no uno por recurso | Las seis comparten los tres estados, la espera y las reglas de CORS, y así se prueban con una sola tabla |
| Y-10 | Cambios del armazón que no estaban en la tabla de P-04: se quita `frontend/.gitkeep`; se quita la entrada `assets` de `angular.json` junto con `public/`; `.editorconfig` gana `end_of_line = lf`; `.prettierignore` nuevo, porque Prettier no lee el `.gitignore` de la raíz | Consecuencias de lo aprobado, no decisiones nuevas, pero no estaban escritas |
| Y-11 | Los enlaces a `/clientes/nuevo` y a `/clientes/{id}` llevan hoy a «Página no encontrada» | El alta y el detalle son las piezas 4 y 5 |
| Y-12 | La corrección del oráculo no cubre un caso: un fichero sin extensión en una carpeta del `PATH` y su `.cmd` solo en otra posterior | No es el de npm, que los instala juntos |
| Y-13 | `CLAUDE.md`, regla 9, sigue diciendo que los ficheros de `frontend/` se editan con las herramientas de edición, sin la excepción de P-05. La IA no la ha tocado: no se le pidió | Una sesión futura que solo lea `CLAUDE.md` no sabrá que `ng generate`, `npm install`, `npm ci` y `prettier --write` están admitidos |

### Revisión de la parada 1 por el Tech Lead (16:03)

**Parada 1 aprobada.** Lo que el Tech Lead dice haber comprobado en Chrome
con el backend real (lo afirma él; la IA no lo ha visto): el panel carga
con CORS, muestra los nombres de `/meta`, busca «EJEMPLÓ» y encuentra
«Ejemplo Uno SL» con una sola petición, y con el backend parado muestra el
error con «Reintentar». La consola no tiene errores. **No ha comprobado la
vista a 375 px.**

**Admitidas Y-01 a Y-13**, con estos cambios, un commit por cambio y con el
oráculo en verde:

| Sobre | Decisión del Tech Lead | Frente a lo que hizo la IA |
|---|---|---|
| Y-07 (a), (b) y (c) | Se escriben en SPEC-04, con historial. Por qué: una regla no puede estar solo en el código. Los textos de (d) valen | **Corregido**: la IA las había dejado en el código y en la bitácora |
| Y-13 | La regla 9 de `CLAUDE.md` recoge la excepción de P-05 | La IA lo había dejado a su decisión |
| Y-01 | Se ajusta `.claude/rules/frontend.md`: los generadores se usan para el proyecto y los ficheros de entorno; los componentes se escriben a mano, con el nombre que les daría el CLI, porque el test va antes | Admitido lo hecho, cambiando la regla |
| El campo de búsqueda | **Defecto visto por el Tech Lead en el navegador**: el corrector subraya el texto. Se desactiva ahí y en los campos del alta donde no tiene sentido (nombre, identificador fiscal y email) | La IA no lo había previsto ni podía verlo sin navegador |

Después, las piezas 4 a 6 como dice el plan (alta, detalle y simulador en
EUR) y **parada 2**, con el recorrido que el Tech Lead tiene que hacer en el
navegador, de dar de alta un cliente a ver su simulación guardada, y lo no
comprobado.

### Piezas 4 a 6 · lo hecho (desde las 16:14)

Una tarea, un commit, con el rojo visto antes del código y el oráculo en
verde antes de cada commit.

| Pieza | Commit | Rojo visto | Requisitos | Tests |
|---|---|---|---|---|
| Preparación · `MetaGate` | `e33c800` | — (refactor en verde) | E-40 | 0 nuevos |
| 4 · Alta | `c4ef635` | 16:23:29, 56 de 59 | E-05 a E-11, E-40, E-41, E-44 a E-46 | 56 más |
| 5a · Carga del cliente | `e7aea4f` | 16:32:25, 20 de 20 | E-15, E-47, E-32, E-33 | 20 más |
| 5b · Fechas y recuentos | `76051f7` | 16:35:31, 9 de 13 | SPEC-04 2.8 | 13 más |
| 5c · Detalle | `f3179e9` | 16:40:01, 36 de 40 | E-12 a E-15, E-35, E-40, E-47 | 36 más |
| 6a · Errores de un formulario | `d4a60f7` | 16:46:53, 9 de 10 | E-09, E-11, E-48 | 10 más |
| 6b · Simulador en EUR | `35a2a2f` | 16:51:36, 100 de 105 | E-15, E-17 a E-25, E-35 a E-38, E-40, E-47 a E-49, E-55 | 100 más |

Al cerrar: **458 tests en 15 ficheros, todos correctos; 99,18 % de líneas**
(488 de 492), con el umbral en 80. Compilación de producción: 256,69 kB
iniciales, con el panel, el alta, el detalle y el simulador en trozos de
carga diferida. El fichero de código más largo tiene 206 líneas
(`simulador.ts`) y la plantilla más larga, 111 (`simulador.html`).

Precisiones de la IA, **sin aprobar**:

| # | Precisión | Motivo |
|---|---|---|
| Z-01 | Al escribir Y-07 en SPEC-04 (2.3) la IA añadió una regla que el Tech Lead no había visto: **un `422` que no deja ninguna entrada que mostrar se trata como error inesperado**, con aviso general y conservando lo escrito | Sin ella, un `422` con `errors` vacío o mal formado dejaría el formulario sin ningún mensaje. Está en la spec y en su historial, pero no la ha aprobado nadie |
| Z-02 | El test del panel añadido con Y-07 (c) («la lista no espera a `/meta`») **nació en verde** | El código ya lo hacía; la regla se escribió después que el código, así que no hubo rojo que ver |
| Z-03 | El refactor `e33c800` no estaba en el encargo | Evita repetir en cuatro vistas los tres estados de `/meta`. No cambia lo que se ve: los tests del panel no se tocaron |
| Z-04 | **Los tests del alta se escribieron tres veces antes del código.** (1) La primera versión no compilaba. (2) La segunda dio rojo por aserción (16:18:37), pero no seguía CA-05: los textos y el sobre de los errores eran inventados y no los ejemplos de SPEC-01 4.1, y de las cuatro filas de 5.4 que dicen «se envía, y el `422` del backend se muestra junto al campo» solo comprobaba el envío. (3) La tercera usa los ejemplos de SPEC-01 4.1, comprueba las dos mitades de esas filas, añade las filas de 5.6 que faltaban (`400`, `502` sin JSON y espera agotada) y **corrige un error del propio test**: el email «de 254 caracteres» tenía 255 y el «de 255», 256. Entre la segunda y la tercera, una ejecución a las 16:22:08 corrió contra la versión vieja porque la escritura del fichero había fallado; no cuenta | Los cambios endurecen los tests; ninguno se relajó. El componente no se empezó hasta ver el rojo de la tercera |
| Z-05 | **Reglas del alta que la spec no dice y la IA ha puesto**, cada una con su test: (a) la ayuda calla hasta el primer intento de envío y después acompaña a lo que se escribe; (b) el mensaje del backend junto a un campo se retira cuando ese campo cambia; (c) **«Reintentar» envía lo que el formulario tiene en ese momento**, pasando otra vez por la ayuda, y no el cuerpo anterior tal cual (2.7 dice «repite la misma petición»); (d) cada desplegable tiene una primera opción desactivada, «Elige un país» y «Elige un plan», y 5.4 dice «ninguna opción más»: el test cuenta las que se pueden elegir; (e) «Guardar» sigue desactivado después del `201`, hasta que la navegación saca el formulario; (f) la ayuda de país y plan comprueba que el código está en la lista de `/meta`, no solo que no está vacío | (c) Si se cambió algo tras el error, enviar el cuerpo viejo daría de alta datos que ya no están en pantalla. (d) Sin ella, el desplegable enseñaría «España» elegido sin que nadie lo eligiera. (e) Un doble clic entre el `201` y la navegación crearía un segundo cliente o un `409` |
| Z-06 | Textos que la spec no fija: los siete mensajes de la ayuda, las etiquetas, «Guardando el cliente…», el enlace «Cancelar» y el aviso del `409`, que es una constante del frontend aunque hoy coincida con el `detail` del backend (el test de CA-06 comprueba que no lo copia). El email lleva `inputmode="email"` y `autocapitalize="none"`, que no validan nada | Como Y-07 (d) |
| Z-07 | Componente nuevo `shared/form-notice.ts` (el aviso general de un formulario, con «Reintentar» opcional) y dos clases globales, `.field` y `.form-actions`. **No tiene fichero de test propio**: lo cubren los tests del alta | Lo usará también el simulador |
| Z-08 | De las filas «cualquiera» de 5.6, en la vista del alta se reproducen `500`, `503`, `400`, un código desconocido, `502` sin JSON, sin conexión y espera agotada. **`415` y `405` no**: van por la misma rama que el `400` y están probados en `core/api-error.spec.ts` | CA-16 pide «cada fila» en los servicios y en las vistas; aquí se ha tomado una por rama |
| Z-09 | El plan traía el detalle como una pieza y se ha hecho en **tres commits**: la carga del cliente (`core/customer-loader.ts`, que cada vista provee para sí), el formato de fechas y recuentos, y la vista | Las dos primeras las usa también el simulador y se prueban solas |
| Z-10 | **Lo que la spec no dice del detalle y la IA ha puesto**: (a) el título de la vista es fijo, «Detalle del cliente», y el nombre de la empresa encabeza su tarjeta; (b) el almacenamiento se muestra como «500 GB»; (c) los recuentos se agrupan a la española, y `Intl` en `es-ES` no separa los números de cuatro cifras («1000», «20.000»); (d) una fecha que no se puede leer se muestra tal como llega; (e) la fecha lleva día, mes, año, hora y minuto («12/11/2026, 15:30»); (f) el desglose por tramos es una lista y no una tabla; (g) el cliente se pide aunque `/meta` esté cargando, como la lista del panel; (h) «Cliente no encontrado» no espera a `/meta`; (i) los textos «Cargando el cliente…», «Simulaciones», «Nueva simulación», «Crear la primera simulación», «Este cliente todavía no tiene simulaciones.», «Desglose por tramos» y «No hay ningún cliente en esta dirección.» | (f) Una tabla de cuatro columnas no cabe en 375 px con importes de seis cifras. (h) Esa vista no enseña ni país ni plan |
| Z-11 | En la vista del detalle no se reproduce la fila de la espera agotada de 5.6: está en el test de la carga del cliente, con temporizadores simulados. Tampoco `400`, `415` ni `405`, como en Z-08. El texto esperado de las fechas se calcula en el test con la misma función `formatDateTime`, que tiene sus tests con la zona fijada | Los tests de la vista usan el *router* de verdad (`RouterTestingHarness`), que espera a que la aplicación se estabilice y no se lleva bien con los temporizadores simulados. La fecha visible depende de la zona de la máquina |
| Z-12 | La regla `.card` pasa de `panel.css` a un fichero global nuevo, `styles/cards.css`, con la lista de datos de una tarjeta | La usan tres vistas. Ningún test ve el CSS: **el aspecto del panel hay que volver a mirarlo en el navegador** |
| Z-13 | Las cuatro filas de las 16:43 de la cronología se escribieron con «16:44» **antes de leer el reloj**, que marcaba 16:43:54. Corregidas al momento | Es el mismo desliz de la fila de las 14:23: la hora se lee antes de escribir, no después |
| Z-14 | **Error de la IA: escribió en la base de datos local del Tech Lead.** Para comprobar el recorrido arrancó `uvicorn` con `DATABASE_PATH` en la carpeta temporal **sin mirar antes si el puerto 8000 estaba libre**. Lo ocupaba el backend del Tech Lead (PID 2916, que la IA no arrancó), así que el de la IA terminó con `[Errno 10048]` y su espera a `/health` dio por bueno el otro. Las peticiones de las 16:59:53 y 16:59:54 fueron a ese backend: `POST /customers` creó el **cliente `id` 1** («Ejemplo Uno SL», `B12345674`, `ES`, `professional`, email `compras@ejemplo-uno.example`) y `POST /simulations` creó la **simulación `id` 1** de ese cliente (15 usuarios, 500 GB, 250.000 llamadas, 169,40 EUR). `backend/data/saas-o-matic.db` cambió a las 16:59:54. Otras dos peticiones respondieron `409` y `422` y no escribieron nada; las demás eran lecturas. La lista inicial solo trae ese cliente | La IA **no ha tocado** la base de datos ni los procesos del Tech Lead (PID 2916 en el 8000 y 18116 en el 4200): la API no tiene borrado, y borrar a mano o parar un proceso ajeno no le corresponde. El fichero está fuera de git (`*.db`). **Qué hacer con esos dos registros lo decide el Tech Lead.** Para que no se repita: antes de arrancar un servidor se mira el puerto con `netstat`, y la espera comprueba el PID que escucha, no solo que algo responda |
| Z-15 | La primera versión del simulador que pasó los tests tenía **340 líneas en `simulador.ts` y 121 en la plantilla**, por encima de los límites. Antes del oráculo se dividió en `projector.ts` (el motor de la proyección: espera de 200 ms, cancelación y qué importes se enseñan), `quote-panel` (la tarjeta de la proyección en sus tres estados), `simulador-view.ts` (qué se enseña de cada campo y de un guardado fallido, como funciones puras) y `simulador-help.ts` (la lectura de los campos y sus límites) | No se subió ningún límite ni se tocó ningún test. `Projector` es un servicio de la carpeta de la vista, no de `core/`, y **ni él ni `simulador-view.ts` tienen fichero de test propio**: los cubren los 73 tests de la vista |
| Z-16 | En el primer intento de verde, «Guardar» no enviaba nada: el `<form>` no tenía grupo y sin él Angular no emite `ngSubmit`. Corregido en el código (un `FormGroup` con los cuatro controles); los tests no se tocaron | Lo encontraron los 11 tests del guardado. Sin ellos habría llegado al navegador |
| Z-17 | **Reglas del simulador que la spec no dice y la IA ha puesto**, con test salvo (h): (a) la primera proyección se pide en cuanto llega el cliente, sin esperar los 200 ms; (b) durante esos 200 ms los importes ya están marcados como «actualizando» y «Guardar», desactivado; (c) «Reintentar» de la proyección pide al momento; (d) la ayuda de los tres campos habla desde el primer carácter, no tras un intento de guardar; (e) con un texto no válido el deslizante se queda donde estaba; (f) el mensaje del backend junto a un campo tras un guardado fallido se retira cuando ese campo cambia; (g) «Reintentar» tras un guardado fallido guarda lo que el formulario tiene en ese momento, como en el alta (Z-05 c), **también tras la espera agotada**; (h) con `/meta` en error, el cliente y la proyección se piden igual, por detrás del aviso; (i) «Guardar» sigue desactivado después del `201`; (j) los textos: la frase de la ayuda («Escribe un número entero de 0 a 100.000, solo con cifras.»), «Calculando la proyección…», «Actualizando…», «Guardando la simulación…», «Proyección», «Almacenamiento (GB)», «Llamadas a la API estimadas», «Volver al detalle», «Ver el detalle del cliente» y la frase de la espera agotada | (a) El cliente ya ha tardado lo suyo. (b) Es lo que pide E-23: la proyección del valor actual aún no está. (g) Tras una espera agotada, reintentar puede guardar dos veces: el aviso lo dice y enlaza al detalle, pero no lo impide |
| Z-18 | Los tests del simulador **no usan el *router* de verdad**: la ruta es un objeto de prueba con el `id`, por los temporizadores simulados (Z-11). Las filas de 5.7 le dan el texto ya descodificado (`1` y un espacio, no `1%20`). La navegación tras el `201` se comprueba espiando `navigateByUrl`, no navegando. Que «la simulación nueva es la primera» se comprueba en el detalle por el orden de la API, no de principio a fin | De principio a fin es CA-14, con Playwright, en la fase de QA. El detalle sí usa el *router* de verdad con las mismas filas |
| Z-19 | Los límites de los campos están escritos en el frontend: 100.000, 1.000.000 y 1.000.000.000 en `simulador-help.ts`, y 2 a 120, 30 y 254 en `alta-help.ts` | La spec manda que la ayuda use los mismos límites que el backend, pero son dos sitios: si cambian en el backend hay que cambiarlos aquí. Ninguna comprobación lo vigila |
| Z-20 | Para verificar el recorrido sin navegador la IA usó `curl` contra el backend real: primero, por error, contra el del Tech Lead (Z-14); después contra uno propio en el puerto 8001. **El frontend no se arrancó**: el puerto 4200 lo ocupa el servidor de desarrollo del Tech Lead | `curl` prueba el backend, no la aplicación |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git log -1` (14:23) | Limpio, `ca8f7af` |
| **Fechas del fichero de bloqueo** (ADR-007) | Script de solo lectura, fuera del repositorio, que consulta en el registro de npm la fecha de publicación de cada entrada de `frontend/package-lock.json` (14:29) | 674 entradas, 650 versiones de 618 paquetes: **ninguna posterior a `2026-11-07T00:00:00Z`** y ninguna sin comprobar. La más reciente, `tough-cookie` 6.1.0, del 2026-11-06 a las 17:26 UTC |
| Scripts de instalación | Salida de `npm install` (14:29) | Cuatro pendientes de aprobar (`esbuild`, `lmdb`, `msgpackr-extract` y `@parcel/watcher`); no se aprueba ninguno |
| `npm audit` del proyecto | En `frontend/` (14:30) | 27 avisos moderados, de los dos avisos de origen de L-07; ninguno alto ni crítico |
| Rojo de la pieza 0 | `ng test --no-watch` con el test nuevo y la página de bienvenida del CLI (14:30:43) | 3 tests, 3 fallos, los tres `AssertionError`: la cabecera no existe, el enlace no existe y no hay `main router-outlet` |
| Los tres scripts del oráculo, a mano | `npm run lint`, `npm run build` y `npm run test:ci` en `frontend/` (14:31) | Código de salida 0 los tres. ESLint y Prettier sin avisos; compilación de 202,96 kB iniciales; 3 tests correctos y 100 % de líneas (3 de 3) |
| La configuración definitiva de ESLint señala lo que debe | Copiada al proyecto de ensayo, fuera del repositorio, y ejecutada contra sus ficheros con infracciones (14:32) | 7 errores: `OnPush`, import de `features/` desde `core/`, 6 parámetros, `any`, función de 42 líneas, import entre features y plantilla en línea de 32 líneas. El `describe` de 45 líneas del `.spec.ts` ya no se señala |
| Finales de línea del proyecto | `git ls-files --eol frontend` tras `git add` (14:33) | 24 ficheros, todos `i/lf w/lf` |
| Oráculo con el frontend creado | `uv run scripts/check.py` (14:33) | **En rojo**: 20 correctas, 3 con fallo y 1 inactiva. Los tres fallos son el mismo: no se pudo ejecutar `npm run …`, `WinError 193` |
| Por qué falla | `uv python list --only-installed` y `shutil.which` con ese Python (14:34) | Python 3.12.0. `shutil.which('npm')` devuelve el fichero `npm` sin extensión; `shutil.which('npm.cmd')`, el `.cmd`. En la carpeta de Node están `npm`, `npm.cmd` y `npm.ps1` |
| Rojo de la corrección del oráculo | `python -m unittest` sobre `scripts/tests/test_repo.py`, antes de tocar `repo.py` (14:47:39) | 2 tests, 1 fallo: `AssertionError: the tool could not be started … [WinError 193]` |
| Oráculo con el frontend activo | `uv run scripts/check.py` (14:49) | **En verde**: 23 correctas, 0 con fallo y 1 inactiva (Playwright, «solo se ejecuta con --e2e»). ESLint, la compilación y los tests con el 80 % de líneas, correctos |

| Oráculo antes de cada commit del frontend | `uv run scripts/check.py`, antes de los nueve commits de las 14:51 a las 15:23 | Verde las nueve: 23 correctas, 0 con fallo y 1 inactiva. Una pasada intermedia, a las 15:21, en rojo por ESLint (fila de las 15:27 de la cronología), corregida antes del commit |
| Caracteres invisibles en `frontend/src` | Recorrido con Python de los `.ts`, `.html` y `.css` (15:21) | Ninguno: los tests los construyen por su código |
| Totales al cerrar | `npm run test:ci` y `npm run build` (15:25) | 221 tests en 10 ficheros, correctos; 98,83 % de líneas; 247,43 kB iniciales |
| El backend arranca con la orden de la parada y responde al origen del frontend | `uv run --locked uvicorn --factory app.main:create_app`, con `DATABASE_PATH` en la carpeta temporal, y `curl` con `Origin: http://localhost:4200` (15:24) | `GET /health` 200; `GET /meta` 200 con `access-control-allow-origin: http://localhost:4200`; `GET /customers` devuelve `{"items":[]}`; la comprobación previa de un `POST` responde 200 con `GET, POST`. Escucha en `127.0.0.1:8000` y responde también en `localhost:8000` |
| El frontend arranca con la orden de la parada | `npm start` y `curl` (15:24) | `http://localhost:4200/` sirve la página con `lang="es"` y `<app-root>`, `main.js` y `styles.css`; el panel y la página «no encontrada» salen como trozos de carga diferida. Sin aprobar ningún script de instalación |
| Los dos procesos, parados | `taskkill` con el PID que escuchaba en cada puerto, sacado de `netstat` (15:25) | Parados el 8484 (backend) y el 23468 (frontend) con sus procesos hijos; ningún puerto ocupado después; `backend/data/` no existe |
| `npm ci` acepta el fichero de bloqueo | `npm ci --dry-run` (15:26) | Código de salida 0 |

Piezas 4 a 6:

| Qué | Cómo | Resultado |
|---|---|---|
| Oráculo antes de cada commit | `uv run scripts/check.py`, antes de los siete commits de código de las 16:14 a las 16:59 y de los dos de esta bitácora (`e96d1a5` y este, pasado a las 17:04 y repetido tras retocar esta fila) | Verde todas: 23 correctas, 0 con fallo y 1 inactiva (Playwright) |
| Caracteres invisibles en `frontend/src` | Recorrido con Python de los `.ts`, `.html` y `.css` (16:26, 16:43 y 16:58) | Ninguno |
| Qué devuelve `Intl` para las fechas y los recuentos | `node -e`, sin escribir nada (16:35) | «12/11/2026, 15:30» en `Europe/Madrid`; «1000», «10.000», «250.000» |
| Totales al cerrar | `npm run test:ci` y `npm run build` (16:59) | 458 tests en 15 ficheros, correctos; 99,18 % de líneas; 256,69 kB iniciales |
| **El recorrido contra el backend del Tech Lead, por error** (Z-14) | `curl` a `127.0.0.1:8000` con `Origin: http://localhost:4200` (16:59:53) | La comprobación previa de `POST /customers` responde 200 con `GET, POST` y `Content-Type` admitido. Alta `201` con `id` 1 y el identificador normalizado; repetida, `409`; con el control mal, `422` `invalid_tax_id_check_character`. Proyección de 10 usuarios, 12100; de 15, 16940. Guardado `201`. **Dejó un cliente y una simulación en la base de datos del Tech Lead** |
| El recorrido contra un backend propio | `netstat` antes (8001 libre); `uvicorn … --port 8001` con `DATABASE_PATH` en la carpeta temporal; `curl` (17:01:02) | Base vacía (`{"items":[]}`). Alta de «Ejemplo Dos SL» con `12345678z`: `201`, guardado como `12345678Z`. Con `12345678A`: `422` `invalid_tax_id_check_character`. Proyección de 51: 42500, 8925 y 51425. Dos guardados `201`; el detalle devuelve `simulation_count` 2 y **primero la última guardada**. `/customers/999`: `404` `customer_not_found` |
| El proceso de la IA, parado; los del Tech Lead, intactos | `taskkill` con el PID que escuchaba en el 8001, sacado de `netstat` (17:01:13) | Parado el 5952; el 8001, libre. Siguen escuchando el 2916 (8000) y el 18116 (4200), que no son de la IA |

## 5. No verificado

Al cerrar la parada 2 (17:01), además de lo de la parada 1, que sigue
debajo:

- **Nada de las piezas 4 a 6 en un navegador**: ni el alta, ni el detalle,
  ni el simulador. Los 458 tests corren en Node con jsdom.
- **La aplicación no ha hecho ninguna petición real.** Lo comprobado con
  `curl` es que el backend responde lo que los tests suponen; no que el
  código del frontend lo pida bien ni que el navegador dé por buena la
  comprobación previa de CORS de los tres `POST`.
- **El recorrido completo**, de dar de alta a ver la simulación guardada: es
  lo que hace el Tech Lead en esta parada.
- El aspecto de todo lo nuevo, **a 375 px y en escritorio**: el formulario
  del alta, las tarjetas del detalle en una y en dos columnas, el bloque
  desplegable, el deslizante (al que se le ha quitado el borde de los
  campos de texto) y los importes atenuados mientras se actualizan. Y el
  panel otra vez, porque su tarjeta ahora sale de una hoja global (Z-12).
- Arrastrar el deslizante de verdad, el teclado de números del móvil
  (`inputmode`), el orden del foco, y que Intro en un campo guarda.
- Los tiempos reales: los 200 ms y los 10 s son temporizadores simulados.
- La navegación de verdad tras el `201` del simulador (se espía la
  llamada) y que el detalle al que se llega trae la simulación nueva la
  primera.
- Las fechas en un navegador y en otra zona horaria: los tests del formato
  fijan la zona; los de las vistas usan la de esta máquina
  (`Europe/Madrid`).
- Las dos filas de divisa de 5.5: son de la pieza 7.

De la parada 1:

- **Nada en un navegador.** La aplicación no se ha abierto: ni su aspecto,
  ni a 375 px ni en escritorio, ni el foco y el teclado, ni la carga
  diferida de las rutas al navegar. Los 221 tests corren en Node con jsdom,
  que no calcula la disposición ni aplica el CSS.
- **El frontend hablando con el backend.** Se ha visto por separado que el
  backend responde a `curl` con el origen del frontend y que el servidor de
  desarrollo sirve la aplicación; **el código de la aplicación no ha hecho
  ninguna petición real**. `curl` enseña las cabeceras de CORS, no si un
  navegador las da por buenas.
- Las órdenes de arranque se han ejecutado desde Git Bash, no desde
  PowerShell.
- Los tiempos reales (300 ms, 10 s): los tests usan temporizadores
  simulados. Lo que hace un campo real con un texto pegado de más de 100
  caracteres o con un *surrogate* suelto.
- `Intl` en un navegador: el formato del dinero está probado con Node 24.
- `npm ci` de verdad, desde un clon limpio: solo en seco.
- Con qué versiones de Python deja de fallar `shutil.which('npm')`.
- La comprobación de Playwright del oráculo: inactiva.
- Ningún evaluador ha mirado este código.
- Nada fuera de Windows. En macOS y Linux el CLI no debería escribir CRLF y
  la corrección del oráculo no hace nada: no se ha visto.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| ~~Parada 1~~ | Hecha y aprobada a las 16:03, con Y-01 a Y-13 admitidas y sus cuatro cambios aplicados |
| **Parada 2**: revisar las piezas 4 a 6 y hacer el recorrido en el navegador, de dar de alta un cliente a ver su simulación guardada | Ahora; es del Tech Lead |
| **Decidir qué se hace con el cliente `id` 1 y la simulación `id` 1 que la IA creó por error en `backend/data/saas-o-matic.db`** (Z-14) | A decidir por el Tech Lead |
| Aprobar o cambiar las precisiones Z-01 a Z-20. Las que más pesan: Z-14 (el error), Z-01, Z-05 y Z-17 (reglas que la spec no dice; las admitidas habría que escribirlas en SPEC-04, como Y-07), Z-08 y Z-11 (filas de 5.6 que no se repiten en cada vista) y Z-19 (límites en dos sitios). Siguen sin aprobar U-01 a U-05 de la sesión 06 | A decidir por el Tech Lead |
| Piezas 7 y 8: divisas y cierre, hasta la parada 3 | Después de la parada 2 |
| **Para el README de la raíz**: los 27 avisos moderados de `npm audit` que verá quien instale el frontend (L-07), con las demás limitaciones; y que el frontend se abre en `http://localhost:4200`, no en `127.0.0.1:4200` | Cuando se escriba el README |
| L-07: volver a mirar los avisos al adelantar la fecha de corte de `frontend/.npmrc` (ESLint 10.15.0 cumple la semana el 2026-11-20) y, como muy tarde, antes de cerrar la fase de QA | Fase de QA |
| El oráculo no comprueba las fechas del fichero de bloqueo de npm ni que cada test del frontend cite su requisito | A decidir por el Tech Lead |
| Pendientes heredados que esta sesión no toca: los de la última fila del apartado 6 de la sesión 06 | A decidir por el Tech Lead |
