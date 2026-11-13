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
| [`04-calidad/`](04-calidad/) | Matriz de trazabilidad requisito → test, evaluaciones independientes y hallazgos | ¿Cómo se sabe que funciona? |

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

Desde el 2026-11-13: bloque backend aprobado (SPEC-01, SPEC-02 y SPEC-03) y
backend en implementación, en el orden del índice de specs. SPEC-04 sigue en
borrador y el frontend no se ha empezado. El detalle de cada día está en la
bitácora de [`03-proceso/`](03-proceso/). Este índice se actualiza a medida
que cada carpeta recibe contenido.
