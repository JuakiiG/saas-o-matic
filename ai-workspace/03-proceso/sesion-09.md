# Sesión 09 · Documentación de entrega e integración continua

| | |
|---|---|
| **Fecha** | 2026-11-15 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | Sesión abierta a las 16:14 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

**La conversación es nueva**, sin el contexto de la sesión 08: la IA llega
con lo que ha leído al empezar (`CLAUDE.md`, `README.md`,
`ai-workspace/README.md`, `04-calidad/limitaciones-conocidas.md` y la
bitácora de la sesión 08, con sus pendientes) y con sus cuatro notas de
memoria, no con lo que hizo esta mañana.

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 09: documentación de entrega e integración continua. Antes de
> nada, leer `CLAUDE.md`, `README.md`, `ai-workspace/README.md`,
> `04-calidad/limitaciones-conocidas.md` y los pendientes de
> `03-proceso/sesion-08.md`. Abrir esta bitácora con el mismo formato que
> las anteriores.
>
> Parada 4 de la sesión 08 aprobada. Admitidas AF-01 a AF-09. AF-05: bien
> hecho; los dos tests se quedan; el permiso se apoyaba en una afirmación
> que nadie había probado. AF-01: admitido; la forma exigida es la que
> escribe el backend y la spec lo dice. AF-07: admitida la falta; el commit
> depende del código de salida del oráculo, sin filtros en medio.
>
> En esta sesión no cambia el código de la aplicación. Un commit por paso.
> El oráculo sin `--e2e` antes de cada commit y una pasada final con
> `--e2e`, siempre por su código de salida. Si algo obliga a tocar
> `backend/` o `frontend/src`, parar y preguntar.
>
> **Paso 1. Trazabilidad.** `ai-workspace/README.md` promete en
> `04-calidad` una matriz de requisito a test que no existe. Crearla en
> `04-calidad/trazabilidad.md`: por cada spec, una fila por requisito EARS
> con cuántos tests lo citan y en qué ficheros, contando backend, frontend
> y Playwright. Sacarla de las citas reales de los tests, con una orden que
> quede escrita en el propio documento, y poner la fecha y el commit sobre
> el que se generó. Los requisitos sin ningún test que los cite van en una
> lista aparte, cada uno con el criterio que lo cubre o «sin cubrir». No
> arreglar ninguno: los decide el Tech Lead.
>
> **Paso 2. `04-calidad/pruebas-manuales.md`.** Un guion para que el Tech
> Lead lo ejecute a mano en unos 15 minutos, con los dos servidores
> arrancados como dirá el README. Pasos numerados, cada uno con lo que hay
> que hacer, lo que se debe ver y el requisito o criterio del que sale. La
> columna del resultado se queda vacía: la rellena él, con fecha, navegador
> y commit. Que incluya al menos: alta de un cliente, detalle, simulador,
> guardar, y la simulación nueva la primera; un alta con errores (el foco
> va al primer campo con error); un identificador fiscal no válido y un
> duplicado; otra divisa (importes, tipo y fecha) y la API de divisas sin
> conexión, con las herramientas del navegador; el backend parado (el aviso
> y «Reintentar»); una dirección que no existe y `/clientes/%31`; el título
> de la pestaña en las cinco vistas; el tabulador por el alta (se ve el
> anillo de foco, también sobre el botón «Guardar»); 375 px de ancho en las
> cuatro vistas, con las herramientas del navegador; y Ctrl+C a mitad de
> `npm run e2e` (los puertos 8000 y 4200 quedan libres y no queda carpeta
> temporal).
>
> **Paso 3. Integración continua.** `.github/workflows/ci.yml`, que ejecute
> lo mismo que se ejecuta en local: el oráculo con `--e2e`. En Linux y en
> Windows (hasta hoy el proyecto solo se ha probado en Windows: el job de
> Linux será la primera prueba fuera). `uv`, Python y Node en las versiones
> que usa el proyecto. `npm ci`. El navegador de Playwright, solo Chromium,
> con sus dependencias de sistema en Linux. Cada acción fijada por su SHA
> completo, con la versión en un comentario; decir de dónde sale cada SHA y,
> si hace falta la red para consultarlo, pedirlo antes. Permisos mínimos
> (`contents: read`), sin secretos, con tiempo máximo, en `push` y en
> `pull_request`. El oráculo lee la historia de git: comprobar qué necesita
> del checkout. No se puede ejecutar antes del `push`: decirlo en la
> bitácora. Sin insignia en el README y sin afirmar que pasa: lo verá el
> Tech Lead tras el `push` y se corrige entonces lo que falle.
>
> **Paso 4. `README.md` de la raíz**, para quien clona el repositorio y
> quiere verlo funcionar en pocos pasos. Corto: se lee en tres minutos y
> enlaza lo demás. Qué es, en tres líneas, fuera el «en desarrollo».
> Requisitos, con las versiones exactas con las que se ha probado. Arranque
> del backend y del frontend, con las órdenes exactas; se abre en
> `http://localhost:4200`, no en `127.0.0.1`, y por qué; qué pasa con la
> base de datos la primera vez. Datos para probar: un identificador fiscal
> válido de cada país admitido, sin script de datos de ejemplo. Tests y
> oráculo: las órdenes, cuántos tests hay, y que las pruebas de Playwright
> descargan Chromium una vez (origen y tamaño), usan los puertos 8000 y
> 4200 y solo funcionan en Chromium. Configuración: las variables de
> entorno que existen y su valor por defecto. Qué necesita internet: la API
> de divisas, y qué se ve si falla, y `/docs`. Límites, sin esconderlos:
> enlace a `limitaciones-conocidas.md`, sin copiar la tabla, y además: solo
> probado en Windows 11, los avisos de `npm audit` con su número de hoy,
> dos ejecuciones de Playwright a la vez se estorban, y el céntimo que
> puede bailar entre el desglose y el total en otra divisa. Cómo se ha
> hecho y por dónde leerlo: enlace a `ai-workspace/README.md`. **Reglas del
> README**: cada orden, ejecutada tal como está escrita, o decir cuál no y
> por qué; con la regla 8, los servidores de la IA van en otros puertos;
> las cifras se copian de una salida de hoy; nada de nombres de quien
> propone el reto.
>
> **Paso 5. `ai-workspace/README.md`.** El apartado «Estado», al día. Un
> recorrido de cinco minutos: qué leer primero para ver el método (una
> spec, un ADR, una bitácora, una evaluación con su respuesta y la
> trazabilidad). La fila de `04-calidad` dice lo que hay de verdad.
>
> **Parar ahí (parada 1)**: qué se ha escrito, qué órdenes del README no se
> han podido ejecutar tal cual, qué requisitos salen sin test, qué acciones
> y qué SHA usa el workflow, y qué no se ha podido comprobar. La prueba en
> limpio y el `push` los hace el Tech Lead.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 16:14 | — | Mensaje recibido a las 16:13 (primera lectura del reloj, 16:13:12). `git status` limpio; el último commit es `7845574` (2026-11-15 15:47:40), el último de la sesión 08. Lecturas del encargo hechas, y además `scripts/check.py` con los módulos del oráculo que usan git, `frontend/package.json`, `frontend/playwright.config.ts`, `backend/pyproject.toml` y `.claude/rules/frontend.md`. **`netstat` a las 16:14:12: nada escucha en el 8000, el 4200, el 8001 ni el 4201.** Existe `backend/data/saas-o-matic.db`, que es del Tech Lead (28.672 bytes, 2026-11-14 18:37): la IA no lo toca. No existe `.github/`. Apertura de esta bitácora |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (16:13)

**Parada 4 de la sesión 08, aprobada. Admitidas AF-01 a AF-09.**

| Precisión | Decisión del Tech Lead |
|---|---|
| AF-05 (el test de `panel.spec.ts` que la IA no quitó) | **Bien hecho. Los dos tests se quedan.** Su permiso se apoyaba en una afirmación que nadie había probado |
| AF-01 (`formatDateTime` muestra crudo lo que no tiene la forma del contrato) | **Admitido.** La forma exigida es la que escribe el backend y la spec lo dice |
| AF-07 (un commit encadenado a un `grep`) | **Admitida la falta.** El commit depende del código de salida del oráculo, sin filtros en medio |
| AF-02, AF-03, AF-04, AF-06, AF-08 y AF-09 | Admitidas, sin comentario |

La bitácora de la sesión 08 no se toca: la aprobación queda anotada aquí,
como la de AB-01 a AB-07 quedó en la de la sesión 08.

**Reglas de esta sesión**, del encargo:

- **No cambia el código de la aplicación.** Si algo obliga a tocar
  `backend/` o `frontend/src`, la IA para y pregunta.
- **Un commit por paso**, con el oráculo sin `--e2e` antes de cada uno y
  una pasada final con `--e2e`; el commit depende del código de salida.
- **La prueba en limpio y el `push` son del Tech Lead.** La integración
  continua no se puede ejecutar antes del `push`.

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git log -1` (16:14:12) | Limpio, `7845574` |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000, 4200, 8001 y 4201 (16:14:12) | Ninguno en escucha |
| Herramientas | `node --version`, `npm --version`, `uv --version`, `python --version`, `git --version` y `cmd /c ver` (16:14:12) | Node 24.18.0, npm 11.16.0, uv 0.12.13, Python 3.12.0, git 2.55.0.windows.3, Windows 10.0.26300.9974 |
| Navegador de Playwright ya descargado | Listado de la carpeta `ms-playwright` de los datos locales del usuario (16:14:12) | Las tres carpetas de la sesión 08: `chromium_headless_shell-1254`, `ffmpeg-1013` y `winldd-1007` |

## 5. No verificado

Se rellena al llegar a la parada 1.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| Paso 1: `04-calidad/trazabilidad.md` | Ahora |
| Paso 2: `04-calidad/pruebas-manuales.md` | Después del paso 1 |
| Paso 3: `.github/workflows/ci.yml` | Después del paso 2 |
| Paso 4: `README.md` de la raíz | Después del paso 3 |
| Paso 5: `ai-workspace/README.md` | Después del paso 4 |
| **Parada 1: la revisa el Tech Lead** | Al acabar el paso 5 |
| **Prueba en limpio y `push`** | Del Tech Lead |
| **Probar a mano una ejecución interrumpida con Ctrl+C** y **la pasada manual con el tabulador** (heredadas de la sesión 08) | Del Tech Lead: entran en el guion del paso 2 |
