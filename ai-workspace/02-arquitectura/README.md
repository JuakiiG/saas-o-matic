# Arquitectura

## Decisiones (ADR)

| ADR | Decisión | Estado |
|---|---|---|
| [ADR-001](ADR-001-stack.md) | Python + FastAPI + SQLite en el backend y Angular en el frontend | `aceptado` (2026-11-12) |
| [ADR-002](ADR-002-calculo-en-tiempo-real.md) | El backend es la única fuente del cálculo; la divisa es solo presentación | `aceptado` (2026-11-12) |

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

- Esquema de la base de datos: se define con SPEC-01 y SPEC-03.
- Estructura de carpetas definitiva de cada proyecto: se documenta al
  crearlos.
