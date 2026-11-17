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
| [`03-proceso/`](03-proceso/) | Bitácora por sesión: prompts clave y cada propuesta de la IA corregida o rechazada, con su motivo. Y las [conversaciones exportadas](03-proceso/conversaciones/README.md) de las sesiones 01 a 14 | ¿Cómo se dirigió a la IA? |
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
  conversaciones salieron del borrador de respuesta de la sesión que
  audita, no del análisis previo: los redactó ella con el Tech Lead, y él
  los revisó y los pegó.
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
  las sesiones 06 y 07 y la prueba en limpio del 16/11/2026. Las
  excepciones son el
  [guion de pruebas manuales](04-calidad/pruebas-manuales.md) del
  16/11/2026, que ejecutó él a mano, paso a paso, y la prueba en limpio
  del 17/11/2026, que hizo también él, a mano.
- **La sesión que audita no ha escrito en nada de lo que git versiona en
  este repositorio**, con dos excepciones: el 16/11/2026 anotó en el guion
  de pruebas manuales los resultados que el Tech Lead le iba dictando
  mientras lo ejecutaba, y ese mismo día dejó en
  `03-proceso/conversaciones/` los ficheros exportados, ya revisados.

Sus notas de trabajo y los borradores de los prompts no se publican: están
en `.private/`, la carpeta de la raíz del repositorio que git ignora,
junto con material ajeno a este proyecto.

*Por qué así*: quien genera no se evalúa a sí mismo. El evaluador
independiente revisa el resultado contra las specs; la sesión que audita
revisa el proceso (que lo que la bitácora dice que pasó, pasó); y la persona
decide con las dos cosas delante.

## Estado

A 2026-11-17, al cerrar la sesión 15 (las sesiones 11 a 15 solo han
cambiado documentación):

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
- **Instalación desde un clon limpio**: hecha dos veces, las dos sobre el
  commit `3591202`, en Windows 11 y siguiendo el
  [`README.md`](../README.md) de la raíz.
  - **El 16/11/2026, de 17:27 a 17:33, la sesión de IA que audita**, con
    la autorización del Tech Lead para usar los puertos 8000 y 4200: un
    clon en una carpeta vacía, las órdenes del README al pie de la letra,
    la parte de navegador con el Chromium de Playwright (no con Chrome) y
    el oráculo con `--e2e` dentro del clon: 24 correctas, 0 inactivas.
  - **El 17/11/2026, de 08:34 a 10:03, el Tech Lead, a mano**, en otro
    clon vacío, con Chrome y solo con el README delante: el backend,
    `npm ci` (los dos avisos anunciados y solo esos), `npm start`, el
    alta de un cliente de España, el identificador que da error, el alta
    de un cliente de otro país, una simulación de 15 usuarios, la divisa
    USD, `/docs` y el oráculo, sin opciones (23 correctas, 1 inactiva) y
    con `--e2e` (24 correctas, 0 inactivas).

  En los dos clones, después: árbol de git limpio, puertos libres y
  ninguna carpeta temporal. De ahí salieron dos fallos del README (qué se
  ve al abrir otra dirección y desde qué carpeta se lanza el oráculo),
  corregidos en la sesión 13: son R-1 y R-2 en su
  [bitácora](03-proceso/sesion-13.md).
- **Integración continua**
  ([`.github/workflows/ci.yml`](../.github/workflows/ci.yml)): **primera
  ejecución el 17/11/2026**, sola, tras el `push` del Tech Lead de
  `3591202` a un repositorio privado de GitHub, a las 10:09. Los dos
  trabajos, en verde, y en los dos la línea «ORÁCULO EN VERDE · 24
  correctas, 0 con fallo, 0 inactivas»: en Ubuntu 26.04.1, en tres
  minutos y medio, y en Windows Server 2025, en seis. En los dos, uv
  0.12.13, Node 24.18.0 y npm 11.16.0, y el navegador de Playwright
  descargado desde cero. **Es la primera vez que el proyecto se ejecuta
  fuera de Windows.**
- **Después de `3591202`**: los commits posteriores, que son los de las
  sesiones 13, 14 y 15, **solo cambian documentación**; ninguno toca
  `backend/`, `frontend/`, `scripts/` ni `.github/`. Sobre `c06630c`, el
  cierre de la sesión 13, **la sesión de IA que audita, el 17/11/2026**:
  - de 11:04 a 11:05, el oráculo con `--e2e`: 24 correctas, 0 con fallo,
    0 inactivas;
  - de 11:06 a 11:09, en su clon, los tres bloques corregidos de «Tests y
    oráculo» del README de la raíz, en PowerShell, tal como están
    escritos y empezando en `frontend/`: el primero, 23 correctas y 1
    inactiva; el segundo, sin error; el tercero, 24 correctas, 0 con
    fallo y 0 inactivas. Los tres con código 0, y al acabar la terminal
    queda en la raíz del clon.

  Sobre `baa1480`, el cierre de la sesión 14, **también el 17/11/2026**:
  - de 12:34 a 12:36, la sesión de IA que audita, el oráculo con `--e2e`:
    24 correctas, 0 con fallo, 0 inactivas;
  - a las 12:48, el `push` del Tech Lead de los diez commits de las
    sesiones 13 y 14. La integración continua se lanzó sola, **su segunda
    ejecución**: los dos trabajos, en verde, y en los dos «ORÁCULO EN
    VERDE · 24 correctas, 0 con fallo, 0 inactivas»; en Linux, en tres
    minutos y medio, y en Windows, en algo menos de seis.

  **El repositorio es público desde el 17/11/2026**: sin iniciar sesión,
  la página carga y la insignia dice «passing».

  Los commits de las sesiones 14 y 15, posteriores a `c06630c`, no tocan
  el README de la raíz. **La integración continua se ejecuta en cada
  `push`**: su resultado sobre el último commit es el de la insignia del
  README de la raíz. La ejecución descrita en el punto anterior es la
  primera.

**Sin probar**:

- **macOS**: nunca.
- **Linux a mano, con un navegador**: allí solo se ha ejecutado el oráculo
  en la integración continua, sin nadie mirando.

El detalle de cada día está en la bitácora de [`03-proceso/`](03-proceso/).
