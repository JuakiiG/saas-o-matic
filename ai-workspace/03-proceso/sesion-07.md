# Sesión 07 · Frontend: armazón, lo común de `core/`, `/meta` y panel

| | |
|---|---|
| **Fecha** | 2026-11-14 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | *En curso.* Se rellena al cerrar |

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

## 5. No verificado

Se rellena al cerrar.

## 6. Tareas pendientes

Se rellena al cerrar.
