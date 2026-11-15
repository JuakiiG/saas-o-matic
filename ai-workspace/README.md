# ai-workspace

Registro del proceso de ingeniería de SaaS-O-Matic: qué se analizó, qué se
especificó, qué se decidió y cómo se dirigió y auditó a la IA. Se escribe
**mientras se trabaja**, no se reconstruye al final; el historial de git lo
acredita (los commits de análisis y specs son anteriores a los del código).

## Cómo leerlo

Las carpetas siguen el orden en que se hizo el trabajo:

| Carpeta | Contenido | Responde a |
|---|---|---|
| [`00-analisis/`](00-analisis/) | Requisitos numerados (`R-xx`) y supuestos sobre las ambigüedades (`A-xx`) | ¿Qué hay que construir y qué no estaba definido? |
| [`01-specs/`](01-specs/) | Especificaciones (`SPEC-xx`) con requisitos EARS, criterios de aceptación y contratos de API | ¿Qué debe hacer exactamente cada parte? |
| [`02-arquitectura/`](02-arquitectura/) | Decisiones de arquitectura (`ADR-xxx`), esquema de datos, estructura del proyecto y directrices dadas a la IA | ¿Cómo se construye y por qué así? |
| [`03-proceso/`](03-proceso/) | Bitácora por sesión: prompts clave y cada propuesta de la IA corregida o rechazada, con su motivo | ¿Cómo se dirigió a la IA? |
| [`04-calidad/`](04-calidad/) | Siete evaluaciones independientes, cada una con su respuesta y la decisión sobre cada hallazgo; la [matriz de trazabilidad](04-calidad/trazabilidad.md) requisito → test; las [limitaciones conocidas](04-calidad/limitaciones-conocidas.md); el [guion de pruebas manuales](04-calidad/pruebas-manuales.md) y las capturas de las vistas | ¿Cómo se sabe que funciona, y qué se sabe que no? |

## Recorrido de cinco minutos

Para ver el método sin leerlo todo, cinco documentos, en este orden:

| Qué | Dónde | En qué fijarse |
|---|---|---|
| Una spec | [SPEC-02](01-specs/SPEC-02-tarificacion-e-impuestos.md), la más corta | Los requisitos EARS (apartado 3), los casos de prueba con sus importes en céntimos (5) y los criterios de aceptación (6): los tests salen de esas tablas |
| Un ADR | [ADR-002](02-arquitectura/ADR-002-calculo-en-tiempo-real.md) | Las opciones comparadas y por qué el cálculo vive solo en el backend |
| Una bitácora | [Sesión 08](03-proceso/sesion-08.md), apartado 3 | Las tablas de precisiones de la IA y las decisiones del Tech Lead. Dos casos: la primera mutación de la prueba de principio a fin sobrevivió (AC-03), y la IA no quitó un test que tenía permiso para quitar, porque el permiso se apoyaba en algo falso (AF-05) |
| Una evaluación y su respuesta | [Segunda evaluación del frontend](04-calidad/evaluacion-frontend-02.md) y [su respuesta](04-calidad/respuesta-evaluacion-frontend-02.md) | El informe de un subagente con contexto limpio, guardado intacto; la respuesta de la IA, sin aplicar nada; y, en su apartado 4, lo que decidió el Tech Lead, con el commit de cada cambio |
| La trazabilidad | [`trazabilidad.md`](04-calidad/trazabilidad.md), apartados 2 y 3 | Qué tests citan cada requisito, y lo que esa matriz no demuestra |

## Dónde están las decisiones propias

El encargo deja puntos abiertos. Cada decisión tomada por cuenta propia está
escrita con su motivo y con la alternativa descartada, en uno de estos
sitios:

| Qué se decidió | Dónde |
|---|---|
| Lo que el encargo no define: plan, impuestos, países, redondeo, duplicados, endpoints añadidos… También qué se consultó, qué se respondió y qué sigue siendo decisión propia | [`00-analisis/supuestos.md`](00-analisis/supuestos.md) (`A-xx`) |
| Arquitectura y lo que afecta a más de una spec: stack, dónde se calcula, persistencia, dependencias, convenciones de la API, casos fiscales no modelados | [`02-arquitectura/`](02-arquitectura/README.md) (`ADR-xxx`) |
| Lo que solo afecta a una spec: límites, códigos de error, comportamiento ante entradas dudosas | Apartado «Decisiones de diseño» de cada spec de [`01-specs/`](01-specs/README.md) |
| Lo que la IA precisó al implementar y lo que el Tech Lead aprobó, cambió o rechazó | Bitácora de [`03-proceso/`](03-proceso/) |

## Convenciones

- **Identificadores estables**: `R-xx` (requisito), `A-xx` (supuesto),
  `SPEC-xx` (especificación), `ADR-xxx` (decisión). Se citan en specs, tests y
  commits para poder seguir un requisito de principio a fin.
- **Estado de cada spec**: `borrador` o `aprobada` (con fecha). No se escribe
  código de una parte hasta que su spec está aprobada.
- **Roles**: una persona decide, aprueba las specs y revisa cada cambio; la IA
  analiza, propone e implementa sobre lo aprobado; un evaluador independiente
  (subagente con contexto limpio) revisa el resultado contra las specs.
- **Bitácora sin retoques**: se anotan los hechos tal como ocurrieron,
  incluidas las propuestas descartadas.

## Estado

A 2026-11-15, al cerrar la sesión 09:

- **Specs**: las cuatro, `aprobadas` (el bloque backend el 2026-11-13 y
  SPEC-04 el 2026-11-14).
- **Código**: backend y frontend implementados sobre ellas. El oráculo
  (`uv run scripts/check.py --e2e`, desde la raíz) ejecuta 741 tests del
  backend, 566 del frontend, 18 pruebas de Playwright y 96 de los propios
  scripts.
- **Evaluaciones independientes**: siete (tres de las specs, dos del
  backend y dos del frontend), todas respondidas y con cada hallazgo
  decidido por el Tech Lead.
- **Lo que se sabe que no hace**: once limitaciones aceptadas (L-01 a
  L-11) y los casos fiscales no modelados (ADR-008).
- **Trazabilidad**: los 140 requisitos EARS tienen algún test que los
  cita, 140 de 140 ([`trazabilidad.md`](04-calidad/trazabilidad.md), que
  dice también lo que esa cifra no demuestra).

**Pendiente**, y por tanto sin comprobar:

- El [guion de pruebas manuales](04-calidad/pruebas-manuales.md) está
  escrito y **sin ejecutar**: su columna de resultados está vacía.
- La integración continua (`.github/workflows/ci.yml`) está escrita y **no
  se ha ejecutado nunca**: solo puede hacerlo tras subir el repositorio.
  Sería la primera ejecución fuera de Windows.
- La instalación desde un clon limpio.

El detalle de cada día está en la bitácora de [`03-proceso/`](03-proceso/).
