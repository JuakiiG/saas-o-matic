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
| [`03-proceso/`](03-proceso/) | Bitácora por sesión: prompts clave y cada propuesta de la IA corregida o rechazada, con su motivo. Y las [conversaciones exportadas](03-proceso/conversaciones/README.md) de las sesiones 01 a 11 | ¿Cómo se dirigió a la IA? |
| [`04-calidad/`](04-calidad/) | Siete evaluaciones independientes, cada una con su respuesta y la decisión sobre cada hallazgo; la [matriz de trazabilidad](04-calidad/trazabilidad.md) requisito → test; las [limitaciones conocidas](04-calidad/limitaciones-conocidas.md); el [guion de pruebas manuales](04-calidad/pruebas-manuales.md) y las capturas de las vistas | ¿Cómo se sabe que funciona, y qué se sabe que no? |

## Recorrido de cinco minutos

Para ver el método sin leerlo todo, seis documentos, en este orden:

| Qué | Dónde | En qué fijarse |
|---|---|---|
| Una spec | [SPEC-02](01-specs/SPEC-02-tarificacion-e-impuestos.md), la más corta | Los requisitos EARS (apartado 3), los casos de prueba con sus importes en céntimos (5) y los criterios de aceptación (6): los tests salen de esas tablas |
| Un ADR | [ADR-002](02-arquitectura/ADR-002-calculo-en-tiempo-real.md) | Las opciones comparadas y por qué el cálculo vive solo en el backend |
| Una bitácora | [Sesión 08](03-proceso/sesion-08.md), apartado 3 | Las tablas de precisiones de la IA y las decisiones del Tech Lead. Dos casos: la primera mutación de la prueba de principio a fin sobrevivió (AC-03), y la IA no quitó un test que tenía permiso para quitar, porque el permiso se apoyaba en algo falso (AF-05) |
| Una conversación | [La de la sesión 08](03-proceso/conversaciones/sesion-08.txt), buscando «❯» | Cómo se dirigió a la IA: cada intervención del Tech Lead empieza con ese carácter, y en esa sesión son cuatro. De dónde salieron esos prompts lo dice [«Dos sesiones de IA y una persona»](#dos-sesiones-de-ia-y-una-persona) |
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
  (subagente con contexto limpio) revisa el resultado contra las specs. El
  reparto completo, con la segunda sesión de IA, que audita, está en
  [«Dos sesiones de IA y una persona»](#dos-sesiones-de-ia-y-una-persona).
- **Bitácora sin retoques**: se anotan los hechos tal como ocurrieron,
  incluidas las propuestas descartadas.

## Dos sesiones de IA y una persona

En este proyecto han trabajado dos sesiones de Claude Code, separadas, y las
dos se declaran aquí.

- **La sesión que implementa.** Abierta en este repositorio. Analiza,
  propone, escribe las specs, el código, los tests y la bitácora, y lanza a
  los evaluadores independientes. Es la que aparece en
  [`03-proceso/`](03-proceso/) y en las
  [conversaciones exportadas](03-proceso/conversaciones/README.md).
- **La sesión que audita.** Abierta en otra carpeta, sin comunicación con la
  primera: nunca le ha enviado un mensaje. En cada parada lee en disco lo
  que la otra ha hecho (los cambios, los commits y el registro de la propia
  sesión) y lo comprueba por su cuenta: repite el oráculo, mira que cada
  commit vaya detrás de un oráculo en verde, que cada test nuevo se viera
  fallar o tenga su mutación, y que el informe de cada evaluador se guardara
  intacto. Con eso le da al Tech Lead un veredicto y un borrador de
  respuesta.
- **El Tech Lead.** Decide. Lee el veredicto, acepta, cambia o descarta cada
  punto, y pega él la respuesta en la sesión que implementa. Aprueba las
  specs, decide cada hallazgo de las evaluaciones, autoriza los commits, que
  llevan su autoría, y hace el `push`.

Cinco consecuencias que conviene saber al leer el resto:

- **El análisis previo.** Antes de la sesión 01 el Tech Lead preparó con la
  sesión que audita un análisis del encargo (requisitos y ambigüedades
  numerados, calendario y riesgos) y un estudio comparado del stack. Están
  en la carpeta privada, y el primer encargo mandaba leerlos: se ve en
  [`sesion-01.txt`](03-proceso/conversaciones/sesion-01.txt). Las
  decisiones de stack y de dónde vive el cálculo las tomó él con ese
  estudio delante. La sesión que implementa redactó, a partir de ese
  material y del enunciado, el análisis publicado en
  [`00-analisis/`](00-analisis/) y los dos primeros ADR.
- **Los prompts largos de cada sesión y de cada parada** que se ven en las
  conversaciones salieron de ese borrador: los redactó la sesión que audita
  con el Tech Lead, y él los revisó y los pegó.
- **«Revisa cada diff».** `CLAUDE.md`, las convenciones de este documento y
  ADR-001 dicen que el Tech Lead revisa cada diff. En la práctica se ha
  hecho así: la sesión que audita revisa los cambios de cada parada (lee el
  código y las specs que cambian y, de los tests, comprueba que se vieran
  fallar o que tengan su mutación), y el Tech Lead lee sobre todo ese
  veredicto y sigue en paralelo lo que hace la sesión que implementa. No ha
  leído él cada diff línea a línea.
- **Cuando una bitácora o un prompt dice «comprobado» o «he visto»**, la
  comprobación puede haberla ejecutado la sesión que audita bajo la
  dirección del Tech Lead; por ejemplo, los recorridos en el navegador de
  las sesiones 06 y 07. La excepción es el
  [guion de pruebas manuales](04-calidad/pruebas-manuales.md) del
  16/11/2026: lo ejecutó él a mano, paso a paso.
- **La sesión que audita no ha escrito en nada de lo que git versiona en
  este repositorio**, con dos excepciones: el 16/11/2026 anotó en el guion
  de pruebas manuales los resultados que el Tech Lead le iba dictando
  mientras lo ejecutaba, y ese mismo día dejó en
  `03-proceso/conversaciones/` los ficheros exportados, ya revisados.

Sus notas de trabajo y los borradores de los prompts no se publican: están
en `.private/`, la carpeta de este mismo directorio que git ignora, junto
con material ajeno a este proyecto.

*Por qué así*: quien genera no se evalúa a sí mismo. El evaluador
independiente revisa el resultado contra las specs; la sesión que audita
revisa el proceso (que lo que la bitácora dice que pasó, pasó); y la persona
decide con las dos cosas delante.

## Estado

A 2026-11-16, al cerrar la sesión 10:

- **Specs**: las cuatro, `aprobadas` (el bloque backend el 2026-11-13 y
  SPEC-04 el 2026-11-14).
- **Código**: backend y frontend implementados sobre ellas. El oráculo
  (`uv run scripts/check.py --e2e`, desde la raíz) ejecuta 741 tests del
  backend, 569 del frontend, 18 pruebas de Playwright y 96 de los propios
  scripts.
- **Evaluaciones independientes**: siete (tres de las specs, dos del
  backend y dos del frontend), todas respondidas y con cada hallazgo
  decidido por el Tech Lead.
- **Lo que se sabe que no hace**: once limitaciones aceptadas (L-01 a
  L-11) y los casos fiscales no modelados (ADR-008).
- **Trazabilidad**: los 140 requisitos EARS tienen algún test que los
  cita, 140 de 140 ([`trazabilidad.md`](04-calidad/trazabilidad.md), que
  dice también lo que esa cifra no demuestra).
- **Pruebas manuales**: el
  [guion](04-calidad/pruebas-manuales.md), **ejecutado por el Tech Lead el
  16/11/2026**, de 12:39 a 13:55, sobre el commit `06a6314`, en Google
  Chrome 157 y Windows 11, con una base de datos nueva: **los 30 pasos, en
  OK**. Lo que vio en cada uno está en su columna de resultados. Los tres
  tests del frontend añadidos después no cambian el código de la
  aplicación.

**Pendiente**, y por tanto sin comprobar:

- La integración continua (`.github/workflows/ci.yml`) está escrita y **no
  se ha ejecutado nunca**: solo puede hacerlo tras subir el repositorio.
  Sería la primera ejecución fuera de Windows.
- La instalación desde un clon limpio.

El detalle de cada día está en la bitácora de [`03-proceso/`](03-proceso/).
