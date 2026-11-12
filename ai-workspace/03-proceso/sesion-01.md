# Sesión 01 · Arranque, análisis, SPEC-02 y ADR

| | |
|---|---|
| **Fecha** | 2026-11-12 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | Repositorio preparado, directrices para la IA, análisis, SPEC-02 en `borrador` y dos ADR aceptados. Ninguna línea de código de aplicación |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Recoge lo que pasó,
incluidas las propuestas de la IA que se corrigieron o descartaron. Se
escribió al cerrar el último punto de la sesión, a partir de la conversación
completa, que seguía abierta; no hubo notas intermedias en fichero.

## 1. Encargo de la sesión

El Tech Lead abrió la sesión fijando los roles, las reglas de trabajo y una
primera tarea en seis puntos, con parada y revisión suya tras cada uno.

**Decisiones que traía tomadas**: backend en Python 3.12 con FastAPI,
Pydantic v2 y SQLite, gestionado con uv; frontend en Angular; el backend como
única fuente del cálculo; todo en EUR; nada de nube; cinco supuestos
consultados a quien propone el reto y sin respuesta.

**Reglas que fijó**, resumidas:

1. Specs antes que código, con requisitos EARS, criterios de aceptación y
   estado.
2. Git desde el primer minuto; los commits de análisis y specs, anteriores a
   los de código. Conventional Commits en español.
3. `ai-workspace/` como registro del proceso, escrito mientras se trabaja.
4. TDD por tarea; un test nunca se relaja ni se borra para que pase.
5. Quien genera no se evalúa: un subagente con contexto limpio revisa cada
   bloque.
6. Nada personal ni ajeno en el repo; todo portable entre sistemas.

**Prompt de la primera tarea** (resumen fiel de los seis puntos):

> a) estructura vacía del repo y revisión del `.gitignore` · b) proponer
> `CLAUDE.md` y `.claude/` · c) requisitos y supuestos, redactados como
> análisis propio · d) índice de specs y SPEC-02 completa con los casos
> límite 0, 1, 10, 11, 50, 51 y 15 = 140 € · e) ADR-001 y ADR-002 · f) abrir
> esta bitácora.

## 2. Cronología

| Hora | Commit | Qué |
|---|---|---|
| 12:08 | `81f7adb` | a) Estructura inicial, `.gitattributes`, `.gitignore` revisado, README raíz e índice del workspace |
| 12:37 | `2604c72` | b) `CLAUDE.md`, reglas por capa, subagente evaluador y `settings.json` |
| 12:47 | `ab4f882` | c) Requisitos R-01 a R-19 y supuestos A1 a A18 |
| 12:47 | `574dd7b` | Corrección de `settings.json` y de una línea de `CLAUDE.md` |
| 12:58 | `64fc571` | d) Índice de specs y SPEC-02 en `borrador` |
| 13:13 | `45b913d` | e) ADR-001 y ADR-002 |

Cada punto siguió el mismo ciclo: la IA deja la propuesta en disco sin
commit, el Tech Lead la revisa y responde con decisiones numeradas, la IA las
aplica, enseña el diff y hace el commit.

## 3. Revisiones del Tech Lead

En cada tabla: qué propuso o hizo la IA, qué decidió el Tech Lead y por qué.
Los motivos son los que dio él.

### Punto a) · Estructura

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| a1 | Aún no había empezado el punto; el encargo incluía `git init` | **Aviso previo**: git ya estaba iniciado y con la identidad local verificada (lo había hecho la IA a petición suya al abrir la sesión); no repetirlo | Ya estaba hecho |
| a2 | Aún no había empezado el punto; el encargo no pedía `.gitattributes` | **Añadido por él**: `* text=auto eol=lf` | El repo se evaluará probablemente en macOS o Linux y los scripts con CRLF fallan allí |
| a3 | No creó el README de la raíz, para no publicar instrucciones que aún no existían | **Descartado**: crear ya un esqueleto mínimo, sin instrucciones de instalación | Es lo primero que ve quien abre el repo y debe orientar desde el primer commit |
| a4 | Avisó de que el primer comentario del `.gitignore` describía el contenido de la carpeta privada | **Aceptado**: dejarlo en `# Private material: never published` | No hace falta anunciar qué contiene |
| a5 | Dejó `.vscode/` ignorado | **Aceptado** | — |
| a6 | Proponía el mensaje de commit y esperaba a que el Tech Lead lo hiciera, según la regla inicial | **Cambiado**: la IA hace el commit cuando él lo pide | La identidad local del repo ya es la suya |

### Punto b) · Directrices para la IA

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| b1 | Oráculo `uv run scripts/check.py` en lugar de `make check` | **Aprobado, con precisión**: debe funcionar desde la raíz sin `pyproject` raíz, con metadatos en línea (PEP 723) | Un único comando que funcione igual en cualquier sistema, sin configuración previa (explicado al revisar la bitácora) |
| b2 | Límites de 250 líneas por fichero, 40 por función, 5 parámetros y 120 por plantilla; el texto decía «los comprueba el oráculo» cuando el script no existía | **Aprobado con condición**: el oráculo debe comprobarlos de verdad, incluida la cobertura del 100 % de ramas de `domain/` con `--cov-fail-under`; marcarlo como pendiente hasta entonces | «Si el CLAUDE.md promete algo que el oráculo no comprueba, es una promesa falsa» |
| b3 | Dejó abierto el idioma de la interfaz y de los errores, proponiendo español | **Decidido**: interfaz en español; errores con código estable en inglés y mensaje en español; el frontend decide por el código, nunca por el texto | El frontend no puede depender de textos que cambian; el código es el contrato (explicado al revisar la bitácora) |
| b4 | Evaluador que no lee la bitácora ni evaluaciones anteriores | **Aprobado tal cual** | — |
| b5 | Regla de commits: la IA propone y solo hace el commit cuando se le pide; nunca `push` | **Confirmado** | — |
| b6 | Dejó fuera de las directrices lo que dependía de supuestos sin aprobar | **Correcto** | — |
| b7 | No había regla de honestidad | **Añadida**: lo no verificado se declara «no verificado»; nunca se afirma que algo funciona sin ejecutar el oráculo y enseñar su salida | Lo que se afirma sin ejecutarlo no es evidencia (explicado al revisar la bitácora) |
| b8 | `settings.json` denegaba `git push` y la lectura de `.env` | **Añadido**: denegar también `Read(./.env.*)` | La IA no debe ver secretos (explicado al revisar la bitácora) |
| b9 | — | **Tarea nueva**: un hook `PreToolUse` portable que bloquee la escritura de código si su spec no está aprobada (ver apartado 6) | Se implementa junto con `check.py`, no ahora |

Al aplicar b8, la IA avisó de que `Read(./.env.*)` bloquearía también
`.env.example`. El Tech Lead lo corrigió en la revisión siguiente (c11).

### Punto c) · Análisis

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| c1 | Redactó A1 y A15 con detalles de la logística de entrega | **Descartada la redacción**: una línea neutra en cada uno; se mantienen los identificadores | Son logística de la entrega, no del producto |
| c2 | Incluyó Estados Unidos en la lista de países con un 0 % | **Descartado**: fuera de la lista | No tiene IVA sino impuestos de venta estatales; un 0 % sería una simplificación no pedida. El caso del 0 % se cubre con tests unitarios |
| c3 | Dejó los tipos de IVA como lista candidata «no verificada» | **Ordenó verificarlos ya** con fuente oficial, anotando URL y fecha | Un dato fiscal sin fuente es una suposición (explicado al revisar la bitácora) |
| c4 | No mencionaba los territorios españoles con otro impuesto | **Añadido** como simplificación conocida: «España» es el 21 % de península y Baleares | Canarias tiene IGIC; Ceuta y Melilla, IPSI |
| c5 | Unicidad del cliente por identificador fiscal normalizado | **Corregido**: la unicidad es del par (país, identificador normalizado) | El mismo que recoge A12: el identificador solo es único dentro de su país (explicado al revisar la bitácora) |
| c6 | Buscador sin límite de resultados ni orden | **Añadido**: máximo 20 resultados, ordenados por nombre | Una respuesta acotada y predecible; sin límite, una búsqueda amplia devuelve la tabla entera (explicado al revisar la bitácora) |
| c7 | Almacenamiento y llamadas a la API guardados sin precio; decía «validarlos» sin concretar cómo | **Precisado**: se validan siempre (enteros, no negativos, con máximo), tengan o no precio | Que un dato no tenga precio no justifica guardar basura (explicado al revisar la bitácora) |
| c8 | Regla de redondeo sin más contexto | **Añadido**: con las tarifas actuales el impuesto sale exacto al céntimo; la regla es para tarifas futuras y se prueba con un caso sintético | Que nadie crea que hoy hay redondeos, y que la regla para el futuro esté probada (explicado al revisar la bitácora) |
| c9 | Propuso A10, A11, A14, A16, A17 y A18 | **Aprobados** | — |
| c10 | Dejó abierto si la API de divisas se llama desde el navegador o a través del backend, proponiendo lo primero | **Decidido**: llamada directa desde el frontend | Es la letra del encargo |
| c11 | `Read(./.env.*)` en `settings.json` (instrucción b8) | **Corregido por el Tech Lead**: reglas concretas para `.env`, `.env.local` y `.env.*.local` | No bloquear `.env.example` |
| c12 | Dejó una línea sin partir en `CLAUDE.md` y lo avisó | **Ordenó arreglarla** | — |

Sobre la numeración: la lista inicial del Tech Lead situaba «repo público o
privado» dentro de A1–A5, pero A5 ya era el IVA entre empresas. La IA lo
señaló, mantuvo A5 y creó A15. El Tech Lead conservó esa numeración.

Tres supuestos (A16, A17 y A18) no estaban en la lista inicial: los añadió la
IA al releer el encargo y el Tech Lead los aprobó.

### Punto d) · SPEC-02

El Tech Lead comprobó por su cuenta las cifras de las tablas 5.1, 5.2 y 5.3
y las dio por correctas.

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| d1 | Seis decisiones de diseño presentadas para aprobación: cálculo por `customer_id`; máximo de 100.000 usuarios; rechazo de `15.0`, `"15"`, `true` y `null`; `tiers` siempre con tres tramos; el `422` gana al `404`; convenciones comunes en el índice | **Aprobadas las seis**; A7 pasa a `decidido` | Los del apartado 7 de SPEC-02 |
| d2 | El índice no citaba A2 entre los supuestos de SPEC-02, aunque el apartado 8 de la spec sí | **Corregido**: añadir A2 al índice | Coherencia entre los dos documentos |
| d3 | E-10 decía «fallar con un error explícito» sin indicar la respuesta HTTP | **Corregido**: `500` en `problem+json` con el código `tax_rate_not_defined`, sin trazas; nueva fila de errores y nuevo criterio de aceptación | Es un fallo interno: SPEC-01 solo admitirá países de la tabla |
| d4 | Los supuestos pendientes no tenían fecha de caducidad | **Regla nueva**: si el viernes 13 a las 10:00 no hay respuesta a A2–A5, los decide él con la hipótesis documentada y pasan a `decidido (sin confirmación externa)` | Un supuesto sin plazo puede bloquear el calendario indefinidamente (explicado al revisar la bitácora) |
| d5 | CA-09 («sin `float`, sin importaciones externas») era una afirmación que solo se podía comprobar leyendo el código | **Corregido**: debe comprobarlo una máquina; `check.py` lo verificará con el AST | El mismo que en b2: una promesa que nada comprueba es falsa (explicado al revisar la bitácora) |

Al aplicar d5, la IA concretó «no usa `float`» en tres comprobaciones: el
tipo, los literales con decimales y la división `/`. La tercera no estaba
pedida; la IA lo avisó y el Tech Lead la aprobó en la revisión siguiente,
porque en Python `/` siempre devuelve `float`.

La IA había pasado A6 a `decidido` tras la revisión c), interpretando que
fijar su contenido equivalía a aprobarlo, y pidió confirmación. El Tech Lead
no lo objetó en la revisión d), pero tampoco lo aprobó de forma literal. **Lo
aprobó de forma explícita al revisar esta bitácora.**

### Punto e) · ADR

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| e1 | Propuso el módulo `sqlite3` de la biblioteca estándar frente a SQLAlchemy | **Aprobado** | Es la opción más pequeña que cumple (explicado al revisar la bitácora) |
| e2 | No mencionaba las claves foráneas | **Añadido**: cada conexión ejecuta `PRAGMA foreign_keys = ON`, y un test lo comprueba guardando una simulación de un cliente inexistente | SQLite no aplica las claves foráneas por defecto |
| e3 | Fijó Angular CLI **22.2.6**, la estable más reciente | **Descartado**: fijar la **21.2.29** (LTS) | Soporte de larga duración, y la IA conoce mejor la 21, lo que reduce el riesgo de APIs inventadas en código que hay que auditar |
| e4 | En el backend contaba a favor la experiencia de quien revisa; en el frontend no decía nada equivalente | **Corregido**: añadir como consecuencia negativa que quien revisa tiene menos experiencia en Angular que en Python, con sus mitigaciones | «Si en el backend la experiencia cuenta a favor, en el frontend hay que decirlo igual» |
| e5 | 200 ms de espera como valor orientativo hasta SPEC-04 | **De acuerdo** | — |

Diff de e3 en `ADR-001-stack.md`:

```diff
-| Angular CLI | **22.2.6** | Etiqueta `latest` del registro de npm el 2026-11-12. […]
+| Angular CLI | **21.2.29** (LTS) | Etiqueta `v21-lts` del registro de npm el 2026-11-12. […]
-El frontend se crea con `npx @angular/cli@22.2.6`, nunca con `latest`.
+El frontend se crea con `npx @angular/cli@21.2.29`, nunca con `latest`.
```

Las correcciones de los puntos d) y e) se pueden ver completas en el
historial: los borradores se añadieron al índice de git antes de aplicarlas,
y el diff se enseñó en la conversación. Las de a), b) y c) se aplicaron
sobre ficheros que aún no tenían ningún commit, así que el historial solo
guarda el resultado.

### Punto f) · Esta bitácora

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| f1 | Dejó un guion en el motivo de doce correcciones, porque no se había dado en el momento | **Aportó los doce motivos**; figuran con la marca «(explicado al revisar la bitácora)» | Que se vea que no se dieron en el momento |
| f2 | En c1 describía el detalle de la redacción descartada de A1 | **Corregido**: dejarlo en «detalles de la logística de entrega» | — |
| f3 | Señaló que A6 no tenía aprobación literal | **Aprobado A6 de forma explícita** | — |
| f4 | Señaló que esta bitácora se escribió al final de la sesión y propuso abrir el fichero al empezar y anotar cada revisión en el momento | **Aprobado**: se hará así desde la sesión 02 | — |

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| La carpeta privada no entra en git | `git status --ignored` y `git check-ignore` | Ignorada |
| Finales de línea | Búsqueda de CRLF antes de cada commit | Ninguno |
| Tipos de IVA de A4 | Lectura de la tabla de la Comisión Europea y de la página del Gobierno del Reino Unido, delegada en un subagente de lectura web | Los nueve tipos coinciden con los propuestos |
| Cifras de las tablas de SPEC-02 | Script aparte que recalcula cada fila | Todas coinciden; además, ningún valor de 0 a 100.000 usuarios necesita redondeo con los tipos de la lista |
| Compatibilidad de Angular CLI con Node 24 | `npm view @angular/cli@<versión> engines` para la 22.2.6 y la 21.2.29 | Las dos admiten Node 24 |
| Términos privados en lo publicado | Búsqueda de nombres, correos y rutas locales antes de los commits | Ninguno |

## 5. No verificado

- Que las reglas de `.claude/rules/` se carguen solo al tocar su carpeta
  (cabecera `paths:`). Se comprobará al crear el primer fichero del backend.
- Que un proyecto de Angular 21.2.29 se cree, compile y pase sus tests con
  Node 24. Solo se ha comprobado la compatibilidad que declara el paquete.
- El impuesto de Ceuta y Melilla: no aparece en la fuente consultada.
- La página del Gobierno del Reino Unido no muestra fecha de actualización.
- Nada de lo que el `CLAUDE.md` atribuye al oráculo, porque `check.py` no
  existe todavía.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| `scripts/check.py` con metadatos en línea (PEP 723): tests, lint, tipos, cobertura del 100 % de ramas de `domain/`, límites de tamaño y comprobación por AST de que `domain/` no usa `float` ni importa nada ajeno a la biblioteca estándar | Con el esqueleto del backend |
| Hook `PreToolUse` portable (script de Python) que bloquee `Write` y `Edit` en `backend/app/**` y `frontend/src/**` si la spec de esa parte no está en estado `aprobada` | Junto con `check.py` |
| Decidir A2 a A5 si no hay respuesta | Viernes 13 de noviembre, 10:00 |
| Aprobar SPEC-02 | Cuando A2 a A5 estén cerrados |
| SPEC-01, SPEC-03 y SPEC-04 | Siguiente sesión |
| Esquema de la base de datos | Con SPEC-01 y SPEC-03 |
| `.env.example` | Con el esqueleto del backend |
