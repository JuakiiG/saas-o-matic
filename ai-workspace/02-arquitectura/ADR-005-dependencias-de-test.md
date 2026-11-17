# ADR-005 · Dependencias de test: python-stdnum, httpx2 y Playwright

| | |
|---|---|
| **Estado** | `aceptado` (2026-11-12); ampliado el 2026-11-13 con el apartado 3 y el 2026-11-15 con la nota del apartado 2 |
| **Decide** | Tech Lead |
| **Requisitos** | R-04, R-11, R-12 |
| **Specs** | SPEC-01 (D-15, CA-19) · SPEC-04 (D-09, CA-13, CA-14) |
| **Relacionado** | ADR-001 (stack y versiones) · ADR-007 (margen de las versiones) · `CLAUDE.md` («Sin dependencias nuevas sin aprobación. Versiones siempre fijadas») |

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

**Nota del 2026-11-15, al implementarlo en la fase de QA** (decisiones del
Tech Lead de las sesiones 07 y 08; lo de arriba se conserva como se
escribió):

- **Son cuatro grupos de pruebas, no dos**: a CA-14 y CA-13 se suman el
  caso de frontera de la limitación conocida L-09 y la fila de la zona
  horaria de SPEC-04, 5.5. CA-13 comprueba además la cabecera con el aviso
  del fallo de los tipos.
- **Los dos proyectos los arranca Playwright** (`webServer`) en sus puertos
  por defecto, 8000 y 4200, sin reutilizar un servidor ya arrancado, y la
  base de datos va en una carpeta temporal que se borra al acabar
  (`CLAUDE.md`, regla 8). No hay una configuración del frontend propia de
  las pruebas.
- **Las capturas de CA-15 las genera Playwright** y las revisa el Tech
  Lead; ya no son manuales.
- **La API de divisas no se intercepta con `page.route()`**, sino con el
  protocolo de depuración de Chromium, solo para su URL. *Por qué*: con
  una ruta puesta, Playwright 1.65.0 responde él mismo a toda comprobación
  previa de CORS, admitiendo lo que se le pida, y la prueba de CA-14 no
  comprobaría el CORS del backend. Se vio con una mutación (una cabecera
  propia en cada `POST`), que con `page.route()` no hacía fallar la prueba.
  Consecuencia: las pruebas solo funcionan en Chromium.
- **Solo se descarga el *headless shell* de Chromium**
  (`npx playwright install --only-shell chromium`), que es lo que usan las
  pruebas; no permite verlas con ventana.

## 3. Cliente HTTP de los tests de integración

Añadido el 2026-11-13, al crear el backend. Los tests de integración llaman
a la API con el cliente de test de FastAPI (`fastapi.testclient`, que es el
de Starlette), y ese cliente necesita una biblioteca HTTP.

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **`httpx2`**, como dependencia solo de desarrollo | Es la que el cliente de test de `starlette` 1.10.0 intenta importar primero y la que su extra `full` declara (`httpx2>=2.0.0`); sin avisos | Publicada por primera vez el 2026-05-11: poco rodaje. Trae `httpcore2`, `truststore` y `httpx2-jsfetch` |
| B | `httpx` 0.28.1 | La biblioteca de siempre; su última versión es del 2024-12-06 | `starlette` 1.10.0 la da por obsoleta en su cliente de test: cada ejecución emite `StarletteDeprecationWarning` |
| C | `httpx` y silenciar el aviso | No cambia nada | Oculta una obsolescencia que acabará en rotura |

**Decisión: opción A.** El encargo del esqueleto nombraba `httpx` y así se
creó; al aparecer el aviso, la IA no añadió `httpx2` por su cuenta y lo
planteó. El Tech Lead decidió el cambio y, con él, que pytest trate los
avisos como errores (`filterwarnings = ["error"]`), para que una
obsolescencia rompa el test en vez de pasar inadvertida.

Comprobado el 2026-11-13: con `httpx` y ese filtro, el test de humo falla
por el aviso; con `httpx2` 2.16.0 pasa sin ningún aviso. Ningún módulo de
`backend/app/` importa `httpx2`.

## Versiones

| Dependencia | Versión | Estado | Dónde se fija |
|---|---|---|---|
| `python-stdnum` | 2.2 (publicada el 2026-01-04) | **Fijada e instalada** el 2026-11-13 | `backend/pyproject.toml` y `uv.lock` |
| `httpx2` | 2.16.0 (publicada el 2026-10-21) | **Fijada e instalada** el 2026-11-13 | `backend/pyproject.toml` y `uv.lock` |
| `@playwright/test` | 1.65.0 (publicada el 2026-11-05), `node >=20`. Trae `playwright` y `playwright-core`, las dos en 1.65.0 y de ese mismo día | **Fijada e instalada** el 2026-11-15 | `frontend/package.json` y `package-lock.json` |

La versión exacta se fija al añadir cada dependencia, con el margen de
ADR-007.

## No verificado

- `python-stdnum` y `httpx2` están instalados desde el 2026-11-13. Con
  `python-stdnum` no se ha ejecutado nada todavía. ~~Playwright no se ha
  instalado.~~ Playwright está instalado desde el 2026-11-15 y sus pruebas
  pasan en Windows 11 con Node 24.18.0; ~~**en macOS y en Linux no se han
  ejecutado**.~~ Desde el 2026-11-17 pasan también en Ubuntu 26.04 y en
  Windows Server 2025, en la integración continua; **en macOS no se han
  ejecutado nunca**.
- Qué declara `fastapi` en sus extras: solo se ha leído el extra `full` de
  `starlette`.
- **Qué acepta `python-stdnum` para el CIF.** SPEC-01 espera que acepte todo
  lo que acepta el validador del dominio y que solo difiera en la forma del
  control (dígito o letra) según el tipo de entidad. Es una hipótesis: se
  comprueba cuando se instale. Si no se cumple, lo decide el Tech Lead.
- La licencia y el código de las tres dependencias no se han revisado. De
  `httpx2` solo se ha leído su ficha en PyPI (repositorio
  `github.com/pydantic/httpx2`) y se ha consultado que la versión 2.16.0 no
  tiene avisos de seguridad en PyPI ni en OSV.
- ~~Que Playwright funcione con la combinación de Node 24 y Angular de
  ADR-001.~~ Comprobado el 2026-11-15 en Windows 11.

## Consecuencias

A favor:

- El CIF deja de apoyarse solo en casos circulares.
- El recorrido principal y el diseño a 375 px se comprueban solos.

En contra, y cómo se trata:

| Consecuencia | Tratamiento |
|---|---|
| Dos dependencias más que mantener | Solo de desarrollo, con la versión fijada; ninguna llega al código de la aplicación |
| La prueba diferencial compara con otra convención, no con una norma | Se dice así en SPEC-01 (2.7) y en `requisitos.md` (R-04); no se presenta como verificación oficial |
| Las pruebas de Playwright son lentas y necesitan los dos proyectos levantados | Solo dos pruebas, en la fase de QA. Medido el 2026-11-15: las catorce pruebas de los cuatro grupos, con el arranque de los dos servidores, tardan unos 20 s en el equipo de desarrollo; los levanta y los para Playwright |

## Cuándo habría que revisarla

- Si `python-stdnum` no se comporta como espera CA-19.
- Si apareciera una fuente oficial del cálculo del control del CIF: la
  prueba diferencial pasaría a ser un complemento.
