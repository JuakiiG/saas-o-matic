# ADR-005 · Dependencias de test: python-stdnum y Playwright

| | |
|---|---|
| **Estado** | `aceptado` (2026-11-12) |
| **Decide** | Tech Lead |
| **Requisitos** | R-04, R-11, R-12 |
| **Specs** | SPEC-01 (D-15, CA-19) · SPEC-04 (D-09, CA-13, CA-14) |
| **Relacionado** | ADR-001 (stack y versiones) · `CLAUDE.md` («Sin dependencias nuevas sin aprobación. Versiones siempre fijadas») |

## Contexto

Dos comprobaciones de las specs no se pueden hacer bien con lo que ya trae
el stack de ADR-001:

1. **El control del CIF no tiene fuente oficial localizada** (SPEC-01,
   2.7). Los casos de prueba se generaron con el mismo algoritmo que
   comprueban, así que solos demuestran coherencia interna, no corrección.
2. **El recorrido completo y el diseño *responsive*** (alta → simulador →
   guardar → la simulación aparece en el detalle; sin desplazamiento
   horizontal a 375 px) no los ejercita ningún test unitario del frontend.

Las dos soluciones añaden una dependencia. `CLAUDE.md` exige aprobación para
cada una y que la decisión, si tiene alternativas, quede en un ADR.

## 1. Contraste del validador fiscal

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **Prueba diferencial contra `python-stdnum`**, como dependencia solo de test | Una implementación independiente y de uso extendido; rompe la circularidad; no entra en el código de la aplicación | Una dependencia más; contrasta con otra convención, no con una norma; puede no distinguir la forma del control por tipo de entidad |
| B | Solo los casos generados con el propio algoritmo | Ninguna dependencia | Circular: un error en el algoritmo se copia a los casos |
| C | Usar `python-stdnum` como validador de la aplicación | Menos código propio | El dominio dejaría de ser puro y sin dependencias (SPEC-01, CA-17); R-04 pide implementar la validación; no separa error de formato y de control con los códigos del contrato |
| D | Casos tomados de identificadores reales | Contraste con datos reales | `CLAUDE.md` prohíbe datos de terceros en el repo |

**Decisión: opción A.**

- `python-stdnum` se declara en el grupo de dependencias de desarrollo del
  backend. Ningún módulo de `backend/app/` la importa.
- La comparación exacta y su resultado esperado están en SPEC-01, CA-19.
- Una discrepancia fuera de la esperada no se resuelve cambiando el test ni
  el validador: la decide el Tech Lead.

## 2. Prueba de principio a fin y *responsive*

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **Playwright** (`@playwright/test`), como dependencia de desarrollo del frontend, solo para lo esencial | Ejercita el backend y el frontend reales en un navegador; comprueba el ancho de 375 px de forma repetible | Una dependencia pesada, que descarga navegadores; pruebas más lentas y más frágiles que las unitarias |
| B | Solo comprobación manual con capturas | Ninguna dependencia | No se repite sola; nada avisa si un cambio rompe el recorrido |
| C | Solo los tests unitarios del frontend con el runner del CLI | Ninguna dependencia | No comprueban la integración real ni el diseño |

**Decisión: opción A**, limitada a dos pruebas: el recorrido de principio a
fin (SPEC-04, CA-14) y la ausencia de desplazamiento horizontal a 375 px en
las cuatro vistas (CA-13). La IA había propuesto la opción B para no añadir
una dependencia; el Tech Lead la cambió. Las capturas manuales quedan como
complemento (CA-15).

- Se implementa en la fase de QA.
- La prueba de principio a fin intercepta la API de divisas con la
  respuesta de SPEC-04 (4.2); no depende de la red (ADR-003).

## Versiones

| Dependencia | Última versión vista el 2026-11-12 | Cómo se consultó | Dónde se fija |
|---|---|---|---|
| `python-stdnum` | 2.2, `requires_python >=3.8` | PyPI | `uv.lock`, al crear el backend |
| `@playwright/test` | 1.65.0, `node >=20` | `npm view` | `package-lock.json`, en la fase de QA |

La versión exacta se fija al añadir cada dependencia. La tabla dice qué
había publicado ese día, no qué se ha instalado.

## No verificado

- **Ninguna de las dos se ha instalado ni ejecutado.**
- **Qué acepta `python-stdnum` para el CIF.** SPEC-01 espera que acepte todo
  lo que acepta el validador del dominio y que solo difiera en la forma del
  control (dígito o letra) según el tipo de entidad. Es una hipótesis: se
  comprueba cuando se instale. Si no se cumple, lo decide el Tech Lead.
- La licencia de las dos dependencias no se ha revisado.
- Que Playwright funcione con la combinación de Node 24 y Angular de
  ADR-001.

## Consecuencias

A favor:

- El CIF deja de apoyarse solo en casos circulares.
- El recorrido principal y el diseño a 375 px se comprueban solos.

En contra, y cómo se trata:

| Consecuencia | Tratamiento |
|---|---|
| Dos dependencias más que mantener | Solo de desarrollo, con la versión fijada; ninguna llega al código de la aplicación |
| La prueba diferencial compara con otra convención, no con una norma | Se dice así en SPEC-01 (2.7) y en `requisitos.md` (R-04); no se presenta como verificación oficial |
| Las pruebas de Playwright son lentas y necesitan los dos proyectos levantados | Solo dos pruebas, en la fase de QA |

## Cuándo habría que revisarla

- Si `python-stdnum` no se comporta como espera CA-19.
- Si apareciera una fuente oficial del cálculo del control del CIF: la
  prueba diferencial pasaría a ser un complemento.
