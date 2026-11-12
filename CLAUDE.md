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
   Una tarea, un commit.
3. **Un test nunca se relaja, se salta ni se borra para que pase.** Si un test
   parece erróneo, se avisa al Tech Lead y decide él.
4. **Oráculo único**: `uv run scripts/check.py`, desde la raíz, ejecuta tests,
   lint, tipos, cobertura y límites de tamaño de backend y frontend. Una tarea
   solo está terminada si termina en verde. *(Pendiente: el script se crea con
   el esqueleto del backend.)*
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
   reconstruye ni se embellece después.
7. **Commits**: Conventional Commits en español (`feat(pricing): …`), citando
   los requisitos que cubren. La IA propone el mensaje; solo hace el commit
   cuando el Tech Lead lo pide. Nunca hace `push`.

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
- **El dinero nunca es `float`**, ni en Python ni en TypeScript.
- Las decisiones con alternativas se registran como ADR en
  `ai-workspace/02-arquitectura/` antes de aplicarlas.

## Límites de tamaño

| Unidad | Máximo |
|---|---|
| Fichero de código (sin contar tests) | 250 líneas |
| Función o método | 40 líneas |
| Parámetros de una función | 5 |
| Plantilla de componente Angular | 120 líneas |

Los comprueba el oráculo con ruff, ESLint y un recuento de líneas *(lo
implementa el oráculo, pendiente)*. Una regla que el oráculo no comprueba no
se anuncia aquí como garantizada. Si algo no cabe, se divide por
responsabilidad; no se sube el límite ni se silencia la regla. *Por qué: los
ficheros grandes son el fallo típico del código generado y lo que más
dificulta revisarlo.*

## Estilo común

- Código, identificadores y comentarios en inglés; documentación, specs y
  textos de la interfaz en español. Los comentarios explican el porqué, no
  repiten el código.
- Los errores de la API llevan un **código estable en inglés** (p. ej.
  `invalid_tax_id`) y un mensaje legible en español. El frontend decide por
  el código, nunca por el texto. *Por qué: el texto puede cambiar o
  traducirse sin romper nada.*
- Funciones pequeñas y con nombre de lo que hacen. Errores tratados de forma
  explícita: nada de `except` vacío ni de `catch` que traga el error.
- Sin dependencias nuevas sin aprobación. Versiones siempre fijadas.
- Sin `# noqa`, `# type: ignore`, `eslint-disable` ni `any` salvo con un
  comentario que justifique esa línea concreta.

## Lo que nunca entra en el repo

- Datos personales (teléfono, email, rutas locales) ni secretos.
- Material de terceros o de otros proyectos.
- Scripts que solo funcionen en un sistema operativo.
