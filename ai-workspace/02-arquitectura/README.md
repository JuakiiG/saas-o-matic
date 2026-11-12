# Arquitectura

## Decisiones (ADR)

| ADR | Decisión | Estado |
|---|---|---|
| [ADR-001](ADR-001-stack.md) | Python + FastAPI + SQLite en el backend y Angular en el frontend | `aceptado` (2026-11-12) |
| [ADR-002](ADR-002-calculo-en-tiempo-real.md) | El backend es la única fuente del cálculo; la divisa es solo presentación | `aceptado` (2026-11-12) |
| [ADR-003](ADR-003-api-de-divisas.md) | Tipos de cambio de la API pública Frankfurter `v2`, llamada desde el navegador | `aceptado` (2026-11-12) |
| [ADR-004](ADR-004-persistencia.md) | Tres tablas, foto completa del cálculo en `simulation_tiers`, solo invariantes en la base de datos y sin migraciones | `aceptado` (2026-11-12) |

Cada ADR recoge el contexto, las opciones comparadas, la decisión con su
motivo y las consecuencias, también las negativas.

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

- Esquema de la base de datos: las tablas y sus restricciones están en
  SPEC-03 (2.6) y sus decisiones en ADR-004. El DDL definitivo
  (`schema.sql`) se escribe con el esqueleto del backend.
- Estructura de carpetas definitiva de cada proyecto: se documenta al
  crearlos.
