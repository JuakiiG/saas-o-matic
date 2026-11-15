# SaaS-O-Matic — directrices para la IA

Estas reglas se cargan en cada sesión. Son pocas a propósito: cada una existe
por un motivo y, cuando es posible, la comprueba una herramienta en vez de la
buena voluntad. Las reglas por capa están en `.claude/rules/` y solo se cargan
al tocar esa parte del repo.

## Roles

- **Tech Lead (persona)**: decide el alcance, aprueba las specs, revisa cada
  diff y es el autor de los commits.
- **IA (esta sesión)**: analiza, propone e implementa solo lo aprobado.
- **Evaluador** (`.claude/agents/evaluador.md`): subagente con contexto limpio
  que revisa el resultado contra las specs. No escribe código.
  *Por qué: quien genera no se evalúa a sí mismo.*

## Flujo de trabajo

1. **Spec antes que código.** No se escribe código de aplicación de una parte
   hasta que su spec en `ai-workspace/01-specs/` está en estado `aprobada`.
   Si la spec no cubre un caso, se para y se pregunta; no se inventa la regla
   de negocio.
2. **TDD por tarea**: test en rojo (se ve fallar) → verde → refactor → commit.
   Una tarea, un commit. El test se ejecuta y su rojo se ve **antes** de
   escribir el código, nunca en el mismo lote, y debe fallar por aserción,
   no por importación. *Por qué: un rojo que el código no esperó a ver no
   demuestra que el test se escribiera primero.*
3. **Un test nunca se relaja, se salta ni se borra para que pase.** Si un test
   parece erróneo, se avisa al Tech Lead y decide él.
4. **Oráculo único**: `uv run scripts/check.py`, desde la raíz, ejecuta tests,
   lint, tipos, cobertura y límites de tamaño de backend y frontend, además
   del control de specs y la higiene del repo. Una tarea solo está terminada
   si termina en verde. Lo que todavía no tiene código que comprobar sale
   como `INACTIVO`, nunca como correcto, y se activa solo cuando aparece ese
   código: un verde con comprobaciones inactivas solo dice que lo activo
   está bien.
   *Por qué un script de Python con metadatos en línea (PEP 723) y no `make`:
   `uv` y Node ya son requisitos del proyecto, no hace falta un `pyproject`
   en la raíz y funciona igual en Windows, macOS y Linux.*
5. **Honestidad sobre el estado**: nunca se afirma que algo funciona sin haber
   ejecutado el oráculo y mostrar su salida. Lo que no se ha comprobado se
   declara «no verificado». *Por qué: una afirmación sin evidencia obliga al
   revisor a repetir el trabajo o, peor, a fiarse.*
6. **Bitácora al momento**: cada sesión se registra en
   `ai-workspace/03-proceso/`, incluida cada propuesta de la IA que el Tech
   Lead corrige o rechaza (qué se propuso, por qué no y qué se hizo). Nunca se
   reconstruye ni se embellece después. **Las horas salen del reloj**
   (`date`) en el momento de escribir cada fila, y la de un commit, de
   `git log --format=%ci` después de hacerlo; nunca se estiman. *Por qué: en
   dos sesiones seguidas hubo que corregir horas estimadas.*
7. **Commits**: Conventional Commits en español (`feat(pricing): …`), citando
   los requisitos que cubren. La IA propone el mensaje; solo hace el commit
   cuando el Tech Lead lo pide. **Un encargo con pasos autoriza un commit
   por paso**, con el oráculo en verde, sin pedirlo otra vez en cada uno.
   *Por qué: es como se trabaja desde la sesión 07, y la regla tiene que
   decir lo que se hace (AC-01 de la sesión 08).* Nunca hace `push`: es
   solo del Tech Lead. Sin trailers de coautoría
   ni firmas de herramientas; el uso de la IA se documenta en
   `ai-workspace/`. Un commit solo se enmienda (`--amend`) si es el último
   y no está subido, y la enmienda se anota en la bitácora. *Por qué: una
   enmienda sin anotar cambia el historial sin dejar rastro.*
   **El commit depende del código de salida del oráculo, nunca de un filtro
   de su salida**: la salida se guarda en un fichero, se mira el código y
   solo con 0 se hace el commit; no se encadena detrás de un `grep` ni de
   un `tail`. *Por qué: en la sesión 07 un commit salió con el oráculo en
   rojo porque la cadena dependía del `grep` que filtraba su salida, y el
   `grep` había encontrado texto (AA-03).*
8. **Procesos**: un proceso que la IA arranca se para por su PID, nunca por
   nombre. *Por qué: parar por nombre mata también procesos ajenos.*
   **Los servidores de comprobación de la IA nunca usan el puerto 8000 ni
   el 4200**: antes de arrancar se mira el puerto con `netstat`, y la
   espera comprueba el PID que escucha. *Por qué: son los puertos del
   Tech Lead; en la sesión 07 un backend de la IA no llegó a arrancar en
   el 8000 y sus peticiones de prueba escribieron en la base de datos
   local del Tech Lead (Z-14).* **Única excepción: los dos servidores que
   arranca Playwright** (`webServer`) para las pruebas de `frontend/e2e/`,
   que usan el 8000 y el 4200 con `reuseExistingServer: false` escrito de
   forma explícita y con `DATABASE_PATH` en una carpeta temporal, fuera de
   `backend/data/`, que se crea y se borra en cada ejecución. Con un
   puerto ocupado la prueba falla sin tocar nada; nunca se reutiliza un
   servidor ya arrancado. La excepción solo vale para lo que arranca
   Playwright. *Por qué: CA-14 de SPEC-04 pide el backend real con su CORS
   por defecto, y así se prueba exactamente lo que ejecutará quien revise,
   sin una tercera configuración del frontend que la spec no nombra
   (decisión del Tech Lead en la sesión 08).*
9. **Edición del código**: los ficheros de `backend/` y `frontend/` se editan
   con las herramientas de edición, no con `sed` ni con scripts. *Por qué:
   el hook del control de specs solo ve esas herramientas.* **Excepción,
   solo en `frontend/` y solo estas órdenes**: `ng new`, `ng generate`,
   `npm install`, `npm ci` y `prettier --write` escriben desde la terminal.
   *Por qué: son los generadores del CLI, el gestor de paquetes y un
   formateador; no escriben lógica de la aplicación (decisión P-05 de la
   sesión 06).*

## Arquitectura

```
backend/    API REST (FastAPI) + SQLite   → .claude/rules/backend.md
frontend/   SPA Angular                   → .claude/rules/frontend.md
ai-workspace/  análisis, specs, ADR, bitácora y calidad
scripts/    herramientas del repo (oráculo)
```

- **Las reglas de negocio viven solo en `backend/app/domain/`**, como funciones
  puras. El frontend no calcula precios ni impuestos: los pide al backend.
  *Por qué: dos implementaciones de una tarifa acaban divergiendo (ADR-002).*
- **El dinero nunca es `float`**, ni en Python ni en TypeScript. Única
  excepción: la conversión de divisa del frontend, que es solo para mostrar,
  se redondea al formatear y nunca se guarda ni se envía al backend
  (ADR-002).
- Las decisiones con alternativas se registran como ADR en
  `ai-workspace/02-arquitectura/` antes de aplicarlas.

## Límites de tamaño

| Unidad | Máximo |
|---|---|
| Fichero de código (sin contar tests) | 250 líneas |
| Función o método | 40 líneas |
| Parámetros de una función | 5 |
| Plantilla de componente Angular | 120 líneas |

Qué comprueba hoy el oráculo y qué no:

- **Activo**: las 250 líneas por fichero (Python, TypeScript y JavaScript de
  `backend/`, `frontend/` y `scripts/`), las 120 líneas de las plantillas
  `.html` del frontend y, en Python, las 40 líneas por función y los 5
  parámetros (sin contar `self` ni `cls`).
- **Activo, por ESLint** (`npm run lint`, que el oráculo ejecuta en
  `frontend/`): en TypeScript, las 40 líneas por función y los 5
  parámetros; y que una plantilla escrita dentro del `.ts` del componente
  no pase de 30 líneas.
- **Excepción en los `.spec.ts`**: no se les aplica el límite de 40 líneas
  por función; los 5 parámetros, sí. *Por qué: la función de `describe`
  envuelve todos los tests del fichero, así que el límite acotaría cuántos
  tests caben en él y no el tamaño de cada uno (decisión P-06 de la sesión
  06).*
- **No comprobado**: el tamaño de cada test dentro de un `.spec.ts`. Lo
  mira quien revisa.

Una regla que el oráculo no comprueba no se anuncia aquí como garantizada.
Si algo no cabe, se divide por
responsabilidad; no se sube el límite ni se silencia la regla. *Por qué: los
ficheros grandes son el fallo típico del código generado y lo que más
dificulta revisarlo.*

## Estilo común

- Código, identificadores y comentarios en inglés; documentación, specs y
  textos de la interfaz en español. Los comentarios explican el porqué, no
  repiten el código.
- Los errores de la API llevan un **código estable en inglés** (p. ej.
  `invalid_tax_id_format`) y un mensaje legible en español. El frontend decide por
  el código, nunca por el texto. *Por qué: el texto puede cambiar o
  traducirse sin romper nada.*
- Funciones pequeñas y con nombre de lo que hacen. Errores tratados de forma
  explícita: nada de `except` vacío ni de `catch` que traga el error.
- Sin dependencias nuevas sin aprobación. Versiones siempre fijadas.
- Sin `# noqa`, `# type: ignore`, `eslint-disable` ni `any` salvo con un
  comentario que justifique esa línea concreta. El oráculo comprueba los
  tres primeros; **el uso de `Any` (Python) o `any` (TypeScript) sin su
  comentario no lo comprueba**: lo mira quien revisa. *Por qué se dice
  aquí: un `Any` sin comentario pasó el oráculo y lo encontró el evaluador
  (H-12 de la evaluación del backend).*

## Lo que nunca entra en el repo

- Datos personales (teléfono, email, rutas locales) ni secretos.
- Material de terceros o de otros proyectos.
- Scripts que solo funcionen en un sistema operativo.
