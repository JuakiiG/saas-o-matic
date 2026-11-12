# Evaluación documental de las especificaciones SPEC-01 a SPEC-04

- **Fecha**: 2026-11-12
- **Evaluador**: subagente independiente (`.claude/agents/evaluador.md`), solo lectura
- **Alcance**: `00-analisis/`, `01-specs/` (índice y cuatro specs), `02-arquitectura/`, `CLAUDE.md` y `.claude/rules/`. No se han leído `03-proceso/` ni `04-calidad/`.

## 1. Resumen

**Oráculo**: no existe (`scripts/check.py` no está en el repo; `backend/` y `frontend/` solo contienen `.gitkeep`). No había nada que ejecutar. Es una revisión documental.

**Cifras recalculadas**: todas cuadran. Recalculé con Python y con Node 24.18.0:
- SPEC-01, 5.2, 5.3 y 5.5: letras de DNI y NIE y control del CIF.
- SPEC-01, 5.9: orden y resultados del buscador.
- SPEC-02, 5.1, 5.2 y 5.3: tramos, impuesto y redondeo.
- SPEC-03, 5.1, 5.3 y 5.4: importes, incluido el caso de la tarifa sustituida (24000 / 2400 / 26400).
- SPEC-04, 5.1: conversión y formato con `Intl.NumberFormat`, con espacio de no separación U+00A0. El céntimo de diferencia en USD se confirma.

| Severidad | Hallazgos |
|---|---|
| alta | 1 |
| media | 7 |
| baja | 18 |
| **Total** | **26** |

## 2. Cobertura de los requisitos R-xx

| R-xx | Dónde se cubre | Estado |
|---|---|---|
| R-01 | ADR-001. SPEC-04/CA-14 (de principio a fin, contra el backend real) | Cubierto por arquitectura. CA-14 está pendiente de la fase de QA |
| R-02 | ADR-001 | Cubierto (decisión, sin EARS) |
| R-03 | SPEC-01 E-01 a E-07 · CA-06, CA-07 | Cubierto |
| R-04 | SPEC-01 E-10 a E-13, E-15 a E-17 · CA-02 a CA-04, CA-08, CA-09 | **Parcial**: el CIF no se apoya en un «algoritmo oficial» (H-06) |
| R-05 | SPEC-03 E-01, E-03, E-08, E-11, E-22 · CA-01, CA-02, CA-06, CA-12 | Cubierto |
| R-06 | SPEC-02 E-01, E-02 · CA-01, CA-03 | Cubierto |
| R-07 | SPEC-02 E-03, E-04, E-07 · CA-01, CA-02, CA-05 | Cubierto (A4 y A5 siguen pendientes) |
| R-08 | ADR-001 | Cubierto (decisión) |
| R-09 | SPEC-04 E-26 a E-31 · CA-01 a CA-03, CA-09 | Cubierto. E-29 no lo cita ningún CA (H-09) |
| R-10 | SPEC-01 E-25 a E-31, E-33 · SPEC-04 E-01 a E-04 | Cubierto. E-30 solo en parte (H-10) |
| R-11 | SPEC-01 E-22 · SPEC-03 E-12 a E-17 · SPEC-04 E-12 a E-16 | Cubierto. El contrato de la ficha es incoherente entre specs (H-01) |
| R-12 | SPEC-02 E-06, E-08, E-11 · SPEC-04 E-17 a E-23 | Cubierto |
| R-13 | `ai-workspace/` existe | Entregable, fuera de las specs |
| R-14 | `00-analisis/`, `01-specs/` | Entregable. Las specs están en `borrador` |
| R-15 | SPEC-03 2.6 (esquema provisional). `02-arquitectura/README.md:27` lo da por pendiente | Parcial, declarado como pendiente |
| R-16 | `03-proceso/` | No comprobado (lectura vetada) |
| R-17 | SPEC-04 E-04, E-09, E-15, E-20, E-21, E-25, E-30, E-32, E-33 · CA-02, CA-03, CA-07, CA-08, CA-10 | Cubierto |
| R-18 | `README.md` existe | No evaluado (fuera del bloque) |
| R-19 | A1, A15 (logística) | Fuera del producto |

Supuestos decididos que ninguna spec convierte en requisito: A16 (CORS) y el `GET /health` de A13 (H-05).

## 3. Hallazgos

### H-01 · alta · La forma de `GET /customers/{id}` difiere entre SPEC-01 y SPEC-03, y el cambio no está aplicado

**Defecto.** Los dos contratos de la ficha no coinciden:
- SPEC-01 fija que la ficha es «el mismo objeto que devuelve el alta». CA-06 exige que la ficha devuelva ese mismo objeto, y CA-16 exige que el OpenAPI declare esos campos.
- SPEC-03 añade a la ficha `simulation_count` y `simulations`.

SPEC-03 anota el cambio en SPEC-01, pero aplazado hasta que se apruebe SPEC-03. Y SPEC-03 no puede aprobarse hasta que SPEC-01 esté aprobada.

**Consecuencia.** SPEC-01 se aprobará e implementará con CA-06 y CA-16 incoherentes. Al implementar SPEC-03, habrá que cambiar un test ya en verde, y eso choca con la regla de `CLAUDE.md` de no relajar tests. SPEC-04 depende del contrato de SPEC-03.

**Evidencia**:
- `SPEC-01…md:316`: «Respuesta `200`: el mismo objeto que devuelve el alta.»
- `SPEC-01…md:556` (CA-06): «`GET /customers/{id}` devuelve el mismo objeto.»
- `SPEC-01…md:566` (CA-16).
- `SPEC-03…md:236-257`: «A los datos del cliente se añaden dos campos».
- `SPEC-03…md:390`: «No se han aplicado: se aplican cuando se apruebe esta spec.»
- `SPEC-03…md:9`: «SPEC-01 y SPEC-02 sin aprobar».
- `SPEC-04…md:452`.
- `CLAUDE.md:25`: «Un test nunca se relaja…»

**Documentos afectados**: SPEC-01, SPEC-03, SPEC-04. **El destino sigue siendo incoherente mientras tanto.**

### H-02 · media · Specs que dependen de supuestos sin citarlos (uno de ellos pendiente)

**Defecto 1. SPEC-04 depende de A3, que está `pendiente de confirmar`.** Su cabecera y el índice dicen que todos sus supuestos están decididos. El índice prohíbe aprobar una spec que dependa de un supuesto no decidido, así que la puerta se salta sobre el papel.
- `SPEC-04…md:239` (E-22, «Cubre A3, A7»).
- `SPEC-04…md:100-101`: «porque no tienen precio (A3)».
- `SPEC-04…md:7`: «A8, A9, A13, A14, A16 y A17 (`decidido`)».
- `01-specs/README.md:13`.
- `01-specs/README.md:15-16`: «Una spec no puede pasar a `aprobada` mientras dependa de un supuesto que no esté `decidido`».

**Defecto 2. SPEC-04 cita además A7, A12 y A6 sin listarlos.** A7 y A12 aparecen en E-22 y E-10 (`SPEC-04…md:98, 217`). A6 está implícito en el uso de céntimos.

**Defecto 3. SPEC-03 depende de A4, que está pendiente, y no lo lista.**
- `SPEC-03…md:150` (E-03, «R-05, A4»).
- `SPEC-03…md:168` (E-16, «A4»).
- `SPEC-03…md:47`: «A4 ya exige guardar el tipo aplicado».
- La cabecera (`SPEC-03…md:7`) y el índice (`README.md:12`) no lo listan.

**Defecto 4. SPEC-02 cita A14 en E-14 y no lo lista.**
- `SPEC-02…md:98`: «Cubre A14».
- No aparece en la cabecera (`SPEC-02…md:7`) ni en el índice (`README.md:11`).

**Atenuante.** SPEC-03 y SPEC-04 quedan bloqueadas de forma indirecta por las specs de las que dependen. Aun así, la cabecera y el índice no reflejan la dependencia real.

**Documentos afectados**: SPEC-02, SPEC-03, SPEC-04, índice.

### H-03 · media · Errores genéricos de la API sin `code` ni estado definidos

**Defecto.** Ninguna spec ni el índice fija el estado ni el `code` para:
- JSON mal formado;
- un cuerpo que no es un objeto (una lista, `null`);
- un `Content-Type` incorrecto;
- una ruta inexistente (`404`);
- métodos no listados en SPEC-03 4.3 (por ejemplo `GET /simulations` o `POST /customers/{id}`);
- parámetros de consulta desconocidos en los `POST`;
- un `500` inesperado.

El único `500` con código es `tax_rate_not_defined`. El índice solo muestra el ejemplo de validación. Quien implemente tendrá que inventar estos códigos, que forman parte del contrato estable.

**Evidencia**:
- `01-specs/README.md:61-82`: un único ejemplo, `validation_error`.
- `SPEC-03…md:261-263`: «`PUT`, `PATCH` y `DELETE` sobre `/customers`, `/customers/{id}` y `/simulations` responden `405`… `method_not_allowed`». Es una lista cerrada.
- `SPEC-01…md:197` (E-07) solo trata campos.
- `SPEC-04…md:74`: «Otro error o sin conexión».
- `backend.md:45-48`: «Los códigos se definen en un único módulo, figuran en la spec».

**Documentos afectados**: índice, SPEC-01, SPEC-02, SPEC-03.

### H-04 · media · El rango de `customer_id` y del `id` de ruta no tiene máximo, y SPEC-02 no fija el mínimo

**Defecto 1. Sin máximo.** Ni el `id` de ruta (SPEC-01) ni el `customer_id` del cuerpo (SPEC-02 y SPEC-03) tienen límite superior. He comprobado que el módulo `sqlite3` lanza `OverflowError: Python int too large to convert to SQLite INTEGER` con `2**63`. Con lo especificado, ese valor acaba en un `500` sin código, en lugar de un `422` o un `404`.

**Defecto 2. SPEC-02 no fija el mínimo.** SPEC-02 remite a un «formato en SPEC-01» que solo existe para el `id` de ruta. Sus casos de 5.4 no incluyen `customer_id`. SPEC-03 sí fija `0` y `-1` → `out_of_range`. En `POST /pricing/quote`, `customer_id = 0` puede dar `422` o `404`, y la regla «gana la validación» depende de esa respuesta.

**Evidencia**:
- `SPEC-02…md:106`: «`customer_id` | entero | sí | Cliente existente (formato en SPEC-01)».
- `SPEC-02…md:197-209`: solo filas de `active_users`.
- `SPEC-02…md:146-148` (precedencia).
- `SPEC-03…md:296-297`: «`0`, `-1` | `422` | `out_of_range`».
- `SPEC-01…md:229` (E-24): «entero positivo», sin máximo.
- Comando: `python -c "...execute('select * from t where id=?',(2**63,))"` → `OverflowError`.

**Documentos afectados**: SPEC-01, SPEC-02, SPEC-03.

### H-05 · media · CORS (A16) y `GET /health` (A13) no tienen requisito EARS ni criterio en ninguna spec

**Defecto.** A16 decide limitar CORS al origen del frontend. Sin CORS, el navegador no puede llamar al backend. Solo lo menciona en prosa SPEC-04 2.9, que es una spec de frontend. Ninguna spec de backend fija el origen, la variable de entorno ni su valor por defecto. `GET /health` figura en A13 y SPEC-01 lo aplaza «al esqueleto del backend», sin spec de destino.

**Evidencia**:
- `supuestos.md:248-249`: «Sí se limita CORS al origen del frontend».
- `SPEC-04…md:194-195`: «El backend admite por CORS solo el origen del frontend en local (A16)».
- `backend.md:49-51`.
- `supuestos.md:230`: «`GET /health` | Comprobar que el backend está levantado».
- `SPEC-01…md:21`: «`GET /health` (se especifica con el esqueleto del backend)».

**Documentos afectados**: SPEC-01, SPEC-03, SPEC-04, `supuestos.md`.

### H-06 · media · R-04 exige el «algoritmo oficial»; el del CIF no tiene fuente oficial y sus casos son circulares

**Defecto.** El control del CIF y los grupos de letras son una convención «escrita de memoria por la IA», sin fuente oficial. Los vectores de prueba se generaron con ese mismo algoritmo, así que los tests demostrarían coherencia interna, no corrección frente al algoritmo oficial. El riesgo está documentado y lo decidió el Tech Lead, pero R-04 queda cubierto solo en parte. El DNI y el NIE se verificaron solo a través del extracto de un buscador.

**Evidencia**:
- `requisitos.md:23`: «se comprueba con el algoritmo oficial de control».
- `SPEC-01…md:124-125`: «**Sin fuente oficial**: convención de uso común».
- `SPEC-01…md:131-133`: «**escrita de memoria por la IA**».
- `SPEC-01…md:376-377`: «cuyo control se ha calculado con el algoritmo de 2.4 a 2.6 mediante un script aparte».
- `SPEC-01…md:123` (Interior: «Verificado solo a través del extracto de un buscador»).

**Documentos afectados**: SPEC-01, `requisitos.md`.

### H-07 · media · `frontend.md` admite importes como «cadenas decimales», en contra del contrato

**Defecto.** La regla que se carga al tocar `frontend/` contradice la convención común de la API y A6.

**Evidencia**:
- `.claude/rules/frontend.md:53`: «Los importes llegan del backend como enteros o cadenas decimales».
- `01-specs/README.md:55-56`: «enteros en céntimos de euro… Nunca decimales (A6)».
- `SPEC-02…md:75` (E-05).

**Documentos afectados**: `.claude/rules/frontend.md`, índice.

### H-08 · media · `CLAUDE.md` prohíbe el `float` para dinero en TypeScript sin excepción; SPEC-04, ADR-002 y `frontend.md` lo usan

**Defecto.** La regla raíz es absoluta. SPEC-04, ADR-002 y `frontend.md` admiten la coma flotante en la conversión de divisa. `CLAUDE.md` no recoge esa excepción.

**Evidencia**:
- `CLAUDE.md:60`: «**El dinero nunca es `float`**, ni en Python ni en TypeScript.»
- `SPEC-04…md:134-137`: «`importe mostrado = céntimos × tipo / 100`… Es el único punto del frontend con coma flotante sobre dinero».
- `ADR-002…md:78`: «La conversión de divisa usa coma flotante en el navegador | Aceptado».
- `frontend.md:54-55`: «más allá de la conversión de presentación».

**Documentos afectados**: `CLAUDE.md`, SPEC-04, ADR-002, `frontend.md`.

### H-09 · baja · SPEC-04/E-29 no lo cita ningún criterio de aceptación

**Defecto.** Ningún CA cita E-29. Solo lo ejercita de hecho una fila de 5.5, que CA-08 reproduce sin citar E-29.

**Evidencia**:
- `SPEC-04…md:251` (E-29: «mostrar el tipo aplicado, su fecha y el total en EUR»).
- `SPEC-04…md:394-408`: ningún CA lista E-29.
- `SPEC-04…md:386`: «Total 188,69 USD, con el tipo, su fecha y 169,40 EUR».
- `SPEC-04…md:401` (CA-08 cita E-17, E-18, E-20 a E-25).

### H-10 · baja · SPEC-01/E-30 («parámetro no documentado») no tiene caso de prueba

**Defecto.** La tabla 5.9 solo prueba la longitud de `q`. Ninguna fila envía un parámetro desconocido, aunque 4.3 declara `unknown_field`.

**Evidencia**:
- `SPEC-01…md:240` (E-30: «o la petición trae un parámetro no documentado»).
- `SPEC-01…md:542`: única fila de error, «101 caracteres».
- `SPEC-01…md:345`.
- `SPEC-01…md:563` (CA-13 cita E-29 a E-31).

### H-11 · baja · Dos casos de SPEC-03 5.5 no responden a ningún requisito EARS

**Defecto.** E-21 solo cubre los negativos y la suma del total. Las filas de `subtotal_cents` y de `position` de 5.5 no las cubre ningún requisito.

**Evidencia**:
- `SPEC-03…md:178` (E-21: «valor negativo o cuyo total no es la suma de base e impuesto»).
- `SPEC-03…md:347-348`: «Tramo con `subtotal_cents` ≠…», «Cuarto tramo… o tramo repetido».
- `SPEC-03…md:364` (CA-11 → E-20, E-21).

### H-12 · baja · SPEC-01/CA-15 remite a una «tabla de SPEC-02» que no existe, y no está claro qué spec es dueña de los tipos

**Defecto 1. Referencia inexistente.** SPEC-02 no tiene una tabla de tipos por país. Solo tiene la tabla de pruebas 5.2 y remite a A4.

**Defecto 2. Dueño de los tipos ambiguo.** SPEC-01 dice que las listas de países viven en el dominio. SPEC-02 dice que los tipos son constantes del dominio y deja la lista de países fuera de su alcance. No se fija si existe una sola constante o dos.

**Evidencia**:
- `SPEC-01…md:565`: «tiene tipo en la tabla de SPEC-02».
- `SPEC-02…md:19-20`: «lista de países admitidos (SPEC-01)».
- `SPEC-02…md:60-61`: «La tarifa y los tipos impositivos son datos constantes del dominio».
- `SPEC-01…md:181-183`.

### H-13 · baja · Referencias internas de SPEC-01 inexactas

**Defecto 1. Rango de apartados distinto.** 2.1 remite a «2.3 a 2.7», que excluye 2.8 (fuera de España) e incluye 2.7 (fuentes). 4.1 dice «2.2 a 2.8».
- `SPEC-01…md:30` frente a `SPEC-01…md:257`.

**Defecto 2. «Las 15 primeras».** La frase se refiere al orden de la lista oficial. Leída contra la lista que muestra la spec (alfabética), `N` es la décima, no queda fuera de las 15 primeras.
- `SPEC-01…md:87-89`.

### H-14 · baja · SPEC-04 CA-05 y CA-08 piden «ejemplos literales» que las specs no contienen

**Defecto.** CA-05 pide simular las respuestas con «los ejemplos literales de SPEC-01». SPEC-01 no tiene ejemplo del cuerpo `409`, ni de `invalid_tax_id_format`, ni de errores en varios campos. CA-08 usa «los ejemplos de SPEC-02 y SPEC-03», que solo cubren 15 usuarios. 5.5 necesita también 10 y 51.

**Evidencia**:
- `SPEC-04…md:398, 401`.
- `SPEC-01…md:262-308`: solo el alta y un `422` de carácter de control.
- `SPEC-02…md:112-133`.
- `SPEC-04…md:379, 381`.

### H-15 · baja · SPEC-04 no define qué ve el usuario con un `id` de ruta mal formado o con un simulador de un cliente inexistente

**Defecto.**
- `/clientes/abc` o `/clientes/0` provocan un `422 validation_error` del backend. Solo está especificado el `404`.
- Al abrir `/clientes/999/simulacion`, tanto `GET /customers/{id}` como la primera proyección devuelven `404`. 5.5 solo trata el `404` al guardar.

**Evidencia**:
- `SPEC-04…md:91`: «`404`: vista «Cliente no encontrado»».
- `SPEC-01…md:229` (E-24).
- `SPEC-04…md:272`: el simulador usa `GET /customers/{id}`.
- `SPEC-04…md:388`: «Guardar con `404` o `500`».

### H-16 · baja · El panel no dice si muestra los códigos o los nombres de país y plan

**Defecto.** El detalle usa los nombres de `/meta`, pero el panel no consume `/meta` según 4.1. Quien implemente tendrá que decidir si el panel muestra `professional` o «Profesional».

**Evidencia**:
- `SPEC-04…md:49-50`: «Cada resultado muestra el nombre, el identificador fiscal, el país y el plan».
- `SPEC-04…md:83`: «(con los nombres de `/meta`)».
- `SPEC-04…md:269`: «`GET /meta` | Alta, detalle».

### H-17 · baja · La regla de fechas de 2.8 aplicada a la fecha del tipo de cambio puede mostrar el día anterior

**Defecto.** La fecha de Frankfurter es una fecha sin hora (`AAAA-MM-DD`). Si se interpreta como medianoche UTC y se muestra en la zona del navegador, en zonas con desfase negativo sale el día anterior. 2.8 no excluye este caso.

**Evidencia**:
- `SPEC-04…md:187-188`: «Las fechas llegan en UTC y se muestran en la zona horaria del navegador».
- `SPEC-04…md:146-148`, `SPEC-04…md:161-162`: «un `date` con forma de fecha (`AAAA-MM-DD`)».

### H-18 · baja · Dos reglas de SPEC-04 son inalcanzables o ambiguas

**Defecto 1. Escenario inalcanzable.** 2.6 trata el reintento fallido «cuando ya hay elegida otra divisa». Pero en estado de error el selector está limitado a EUR, y los tipos solo se piden al arrancar o al reintentar desde ese error. El escenario no se alcanza.
- `SPEC-04…md:166-167` frente a `SPEC-04…md:155`: «selector limitado a EUR y botón «Reintentar»».

**Defecto 2. Alcance de «se retiran los importes».** E-22 y la tabla de estados no dicen si un almacenamiento o un número de llamadas no válido retira los importes de la proyección, que no dependen de esos campos.
- `SPEC-04…md:239`, `SPEC-04…md:113` («se retiran los importes»), `SPEC-04…md:100-101`.

### H-19 · baja · A17 sitúa el alta «en el panel»; SPEC-04 la pone en una ruta propia y no anota el cambio

**Defecto.** SPEC-04 mueve el alta a una ruta propia. Su apartado 8 no recoge que A17 tenga que cambiar.

**Evidencia**:
- `supuestos.md:254-255`: «Se añade un formulario sencillo de alta en el panel».
- `SPEC-04…md:32`: «`/clientes/nuevo` | Alta de cliente».
- `SPEC-04…md:430` (D-07).
- `SPEC-04…md:448-452`: no lista A17.

### H-20 · baja · Decisiones con alternativas registradas fuera de los ADR; ADR-001 razona con «dos tablas»

**Defecto 1. Fuera de los ADR.** `CLAUDE.md` exige un ADR para las decisiones con alternativas. Varias de este tipo están solo en tablas de decisiones de las specs: la API de divisas (Frankfurter `v2`), la tabla `simulation_tiers` frente a JSON y la ausencia de migraciones.
- `CLAUDE.md:61`: «Las decisiones con alternativas se registran como ADR… antes de aplicarlas».
- `SPEC-04…md:424` (D-01), `SPEC-03…md:378` (D-02), `SPEC-03…md:383` (D-07).

**Defecto 2. Premisa desactualizada.** ADR-001 justifica `sqlite3` en que hay «dos tablas». SPEC-03 define tres.
- `ADR-001…md:106-107` frente a `SPEC-03…md:82, 96, 111`.

### H-21 · baja · Las reglas usan como ejemplo un código de error que no existe

**Defecto.** `invalid_tax_id` no es ninguno de los códigos de SPEC-01, que define `invalid_tax_id_format` e `invalid_tax_id_check_character`.

**Evidencia**: `CLAUDE.md:86`, `.claude/rules/backend.md:46`, `.claude/rules/frontend.md:49` frente a `SPEC-01…md:289`.

### H-22 · baja · Ambigüedades de validación en SPEC-01 que obligan a inventar

Puntos sin regla:
- **Qué es «espacio» al recortar.** `str.strip()` quita también `\n` y `\t`, de modo que `"\nEjemplo"` sería válido. Si solo se quitan espacios, sería `invalid_characters`.
- **Qué es un «carácter de control»**: solo Cc o también Cf.
- **Unidad de las longitudes**: puntos de código o grafemas.
- **Varios errores en un mismo campo**: si se devuelven uno o todos.
- **Orden del array `errors`.**
- **Nombre del `field`** para el `id` de ruta y los parámetros de consulta.
- **Momento del límite de 100 caracteres de `q`**: antes o después de recortar. 2.10 recorta y E-30 no lo precisa.
- **Código de un `tax_id` de más de 30 caracteres fuera de España.** 5.4 solo lo fija para España. `too_long` figura en la lista de 4.1.

**Evidencia**: `SPEC-01…md:29, 30, 192, 240, 165, 289, 323, 452`.

### H-23 · baja · El origen de `country` en el historial y la precisión de `created_at` no están fijados

**Defecto 1. `country` sin columna.** La respuesta de cada simulación incluye `country`, pero la tabla `simulations` no lo guarda. Se deduce del cliente, que es inmutable por A18, pero la spec no lo dice. Eso choca con «el historial lee los importes guardados».
- `SPEC-03…md:98-109` (sin columna `country`), `SPEC-03…md:217, 255`, `SPEC-03…md:52-53`.

**Defecto 2. Precisión de `created_at`.** SPEC-03 fija precisión de segundos; SPEC-01 no fija ninguna para el cliente.
- `SPEC-03…md:36` frente a `SPEC-01…md:36`.

### H-24 · baja · Trazabilidad incompleta en `supuestos.md` y `requisitos.md`

**Defecto 1. Columna «Afecta a» incompleta.** Faltan dependencias que las specs sí declaran:
- A3: falta SPEC-04;
- A4: falta SPEC-03;
- A7: falta SPEC-04;
- A9: falta SPEC-03;
- A12: falta SPEC-04;
- A13: falta SPEC-02.

Evidencia: `supuestos.md:25-35`, frente a `SPEC-04…md:239, 217`, `SPEC-03…md:7, 150` y `SPEC-02…md:7`.

**Defecto 2. R-11 omite SPEC-01**, que declara cubrir su parte de backend.
- `requisitos.md:30`: «R-11 | … | SPEC-04 · SPEC-03».
- `SPEC-01…md:6`.

**Defecto 3. Requisitos sin aprobar.** Las specs se basan en un documento de requisitos que sigue en borrador.
- `requisitos.md:4`: «borrador, pendiente de revisión del Tech Lead».

### H-25 · baja · SPEC-04 atribuye a ADR-002 la prohibición de validar el identificador fiscal en el frontend

**Defecto.** ADR-002 solo trata la tarifa, los impuestos y la divisa. La regla sobre el identificador fiscal está en `frontend.md`.

**Evidencia**:
- `SPEC-04…md:21-22`: «ni el control del identificador fiscal (ADR-002)».
- `SPEC-04…md:213` (E-06, «Cubre ADR-002»).
- `ADR-002…md:36-46`.
- `frontend.md:39-40`.

### H-26 · baja · Cambios cruzados pendientes de SPEC-04

**Defecto.** Están pendientes dos cambios en otros documentos:
- ADR-002 dice «unos 200 ms»; SPEC-04 lo fija en 200 ms.
- A8 deja abierta la lista de divisas; SPEC-04 la cierra en EUR, USD, GBP y CHF.

Ninguno de los dos documentos destino queda incoherente mientras tanto, porque A8 delega en SPEC-04 y «unos 200 ms» admite 200. El pendiente de SPEC-01 sí deja el destino incoherente; se trata en H-01.

**Evidencia**:
- `SPEC-04…md:448-452`.
- `ADR-002…md:41`: «espera unos 200 ms».
- `supuestos.md:173-174`: «EUR, USD, GBP y alguna más), que se cierra en SPEC-04».

## 4. Lo que no he podido comprobar

- **Oráculo, código y tests**: no existen. Ningún requisito está demostrado por un test. CA-17 de SPEC-01, CA-09 de SPEC-02 y CA-13 y CA-14 de SPEC-04 dependen de herramientas que aún no existen.
- **Fuentes externas**: no he consultado el BOE, la AEAT, el Ministerio del Interior, la Comisión Europea ni GOV.UK. No puedo confirmar los tipos de IVA de A4 ni que el cálculo del CIF coincida con un algoritmo oficial (no hay fuente citada). Mi recálculo usa el mismo algoritmo que la spec, así que solo prueba coherencia interna.
- **API de Frankfurter**: no la he llamado. No he verificado la forma de la respuesta de la `v2`, CORS ni la caché.
- **Formato en navegadores**: el formato de `Intl.NumberFormat` se verificó solo en Node 24.18.0, no en los navegadores de destino.
- **`03-proceso/` y `04-calidad/`**: no los he leído porque lo prohíbe el rol. R-16 y CA-15 quedan sin evaluar.
- **Fuera del bloque**: no he revisado el `README.md` raíz (R-18) ni `.claude/settings.json`.
