# Arquitectura

## Decisiones (ADR)

| ADR | Decisión | Estado |
|---|---|---|
| [ADR-001](ADR-001-stack.md) | Python + FastAPI + SQLite en el backend y Angular en el frontend | `aceptado` (2026-11-12) |
| [ADR-002](ADR-002-calculo-en-tiempo-real.md) | El backend es la única fuente del cálculo; la divisa es solo presentación | `aceptado` (2026-11-12) |
| [ADR-003](ADR-003-api-de-divisas.md) | Tipos de cambio de la API pública Frankfurter `v2`, llamada desde el navegador | `aceptado` (2026-11-12) |
| [ADR-004](ADR-004-persistencia.md) | Tres tablas, foto completa del cálculo en `simulation_tiers`, solo invariantes en la base de datos y sin migraciones | `aceptado` (2026-11-12) |
| [ADR-005](ADR-005-dependencias-de-test.md) | Dependencias solo de test: `python-stdnum` para contrastar el validador fiscal, `httpx2` para el cliente de test y Playwright para la prueba de principio a fin y los 375 px | `aceptado` (2026-11-12); ampliado el 2026-11-13 |
| [ADR-006](ADR-006-convenciones-transversales-de-la-api.md) | Convenciones transversales de la API: errores en `problem+json` con código estable, identificadores, fechas, constante única de países e historial dentro de la ficha | `aceptado` (2026-11-12) |
| [ADR-007](ADR-007-margen-de-las-versiones.md) | Ninguna dependencia se fija en una versión publicada hace menos de una semana: fecha de corte `exclude-newer` de uv | `aceptado` (2026-11-13) |
| [ADR-008](ADR-008-casos-fiscales-no-modelados.md) | Cómo se abordarían la inversión del sujeto pasivo y los demás casos fiscales que hoy no se modelan. Es un diseño: nada está implementado | `aceptado` (2026-11-13) |
| [ADR-009](ADR-009-validacion-del-alta-en-el-dominio.md) | El alta de clientes la valida a mano una función pura del dominio; Pydantic sigue validando los endpoints sin orden de comprobaciones ni dependencias entre campos | `aceptado` (2026-11-13) |

Cada ADR recoge el contexto, las opciones comparadas, la decisión con su
motivo y las consecuencias, también las negativas.

**Qué decisiones llevan ADR** (criterio del Tech Lead, 2026-11-12): toda
decisión que afecte a la arquitectura o a más de una spec. Las que solo
afectan a una spec se quedan en la tabla de decisiones de esa spec, con su
alternativa descartada. Las decisiones de proceso, como el bloque de
aprobación de las specs del backend, no son arquitectura y viven en el
índice de specs.

## Modelo de datos

Tres tablas de SQLite. Las columnas y sus restricciones están en SPEC-03
(2.6); las decisiones y sus alternativas, en ADR-004.

| Tabla | Contenido | Relación |
|---|---|---|
| `customers` | Datos del cliente y la forma de búsqueda de su nombre. `UNIQUE (country, tax_id)` | — |
| `simulations` | Datos de entrada de la simulación y la foto de su cálculo: país, base, tipo, impuesto y total | Muchas por cliente (`customer_id`), sin borrado en cascada |
| `simulation_tiers` | El desglose del cálculo, una fila por tramo | Tres por simulación (`simulation_id`, `position`) |

**El DDL vive en el backend**, en
[`backend/app/repositories/schema.sql`](../../backend/app/repositories/schema.sql),
versionado, que se aplica al arrancar. Esta carpeta no guarda una copia:
muestra el modelo y enlaza a ese fichero.

## Organización de carpetas

Lo versionado a 2026-11-17 (`git ls-files`), hasta el nivel de carpeta; de
ficheros, solo los puntos de entrada.

```
backend/              API REST: FastAPI y SQLite
  app/                la aplicación
    main.py           punto de entrada: monta la aplicación FastAPI
    config.py         configuración por variables de entorno
    api/              routers, esquemas Pydantic y errores HTTP
    services/         casos de uso: orquestan dominio y repositorios
    domain/           reglas de negocio, como funciones puras
    repositories/     acceso a SQLite y su esquema (schema.sql)
  tests/              pytest, y las tablas de casos compartidas
    unit/             el dominio y los errores del alta
    integration/      la API y los repositorios, con una base temporal
frontend/             SPA Angular
  src/                la aplicación
    main.ts           punto de entrada
    app/              componente raíz y rutas (app.routes.ts)
      core/           servicios de la API, modelos y formatos
      features/       una carpeta por vista: panel/, alta/, detalle/,
                      simulador/ y not-found/
      shared/         componentes y pipes de presentación
    environments/     las URL a las que llama la aplicación
    styles/           estilos globales
  e2e/                pruebas de principio a fin (Playwright)
    support/          utilidades de esas pruebas
    capturas/         genera las capturas de las vistas
scripts/              herramientas del repo
  check.py            punto de entrada: el oráculo
  traceability.py     punto de entrada: la matriz de trazabilidad
  oracle/             las comprobaciones del oráculo
  tracematrix/        la matriz requisito → test
  hooks/              hook: ningún código sin su spec aprobada
  tests/              tests de los propios scripts
```

Los tests unitarios del frontend van junto al fichero que prueban
(`.spec.ts`).

**Dependencias.** Backend: `api → services → domain`,
`services → repositories` y `repositories → domain`; `domain/` no importa
de ninguna otra capa. Frontend: `features/` importa de `core/` y de
`shared/`, nunca al revés, y una vista no importa de otra.

**Qué lo vigila**, con el nombre que sale en la salida del oráculo
(`uv run scripts/check.py`):

| Regla | Comprobación |
|---|---|
| Sentido de las capas del backend, y `sqlite3` solo en `repositories/` | «Dirección de las capas y `sqlite3` solo en repositories/» |
| `domain/` solo importa la biblioteca estándar | «domain/ solo importa la biblioteca estándar y no usa float ni la división `/`» |
| `core/` y `shared/` no importan de `features/`; una vista no importa de otra | «ESLint, con los límites de tamaño» (`no-restricted-imports`) |
| 250 líneas por fichero de código, sin contar tests, y 120 por plantilla | «Ficheros de código de 250 líneas como máximo y plantillas de 120» |
| 40 líneas y 5 parámetros por función | Python: «Funciones de Python de 40 líneas y 5 parámetros como máximo». TypeScript: «ESLint, con los límites de tamaño» |

**No lo vigila nada**, lo mira quien revisa: en qué carpeta va cada test;
que `domain/` no haga entrada/salida ni lea el reloj; que los routers sean
finos y el SQL esté solo en `repositories/`; `main.py` y `config.py`, que
quedan fuera de la comprobación de capas; que `HttpClient` solo se use en
`core/` y las rutas se carguen de forma diferida; y el tamaño de los
tests.

La IA recibió esta estructura antes de escribir el código, en
[`.claude/rules/backend.md`](../../.claude/rules/backend.md) y
[`.claude/rules/frontend.md`](../../.claude/rules/frontend.md). **Hoy no
coinciden en dos cosas**: `frontend.md` nombra tres vistas (búsqueda,
cliente, simulador) e interceptores en `core/`, y hay cinco carpetas de
vista (la búsqueda es `panel/`; el cliente, `detalle/`) y ningún
interceptor; `backend.md` dice que `unit/` prueba «dominio y servicios»,
y prueba el dominio y un módulo de `api/`.

## Directrices dadas a la IA

Viven en la raíz del repo, que es donde la herramienta las carga:

| Fichero | Contenido |
|---|---|
| [`CLAUDE.md`](../../CLAUDE.md) | Roles, flujo de trabajo, dónde vive la lógica de negocio, límites de tamaño y estilo común |
| [`.claude/rules/backend.md`](../../.claude/rules/backend.md) | Capas del backend y convenciones de FastAPI, Pydantic y pytest |
| [`.claude/rules/frontend.md`](../../.claude/rules/frontend.md) | Estructura del frontend y convenciones de Angular |
| [`.claude/agents/evaluador.md`](../../.claude/agents/evaluador.md) | Subagente evaluador independiente, de solo lectura |
| [`.claude/settings.json`](../../.claude/settings.json) | Permisos denegados a la IA: `git push` y lectura de ficheros de entorno |
