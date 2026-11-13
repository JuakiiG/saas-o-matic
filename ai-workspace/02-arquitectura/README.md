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

## Directrices dadas a la IA

Viven en la raíz del repo, que es donde la herramienta las carga:

| Fichero | Contenido |
|---|---|
| [`CLAUDE.md`](../../CLAUDE.md) | Roles, flujo de trabajo, dónde vive la lógica de negocio, límites de tamaño y estilo común |
| [`.claude/rules/backend.md`](../../.claude/rules/backend.md) | Capas del backend y convenciones de FastAPI, Pydantic y pytest |
| [`.claude/rules/frontend.md`](../../.claude/rules/frontend.md) | Estructura del frontend y convenciones de Angular |
| [`.claude/agents/evaluador.md`](../../.claude/agents/evaluador.md) | Subagente evaluador independiente, de solo lectura |
| [`.claude/settings.json`](../../.claude/settings.json) | Permisos denegados a la IA: `git push` y lectura de ficheros de entorno |

## Pendiente

- Estructura de carpetas definitiva de cada proyecto: se documenta al
  crearlos.
