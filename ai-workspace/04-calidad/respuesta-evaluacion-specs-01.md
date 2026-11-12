# Respuesta a la evaluación de las specs 01 a 04

| | |
|---|---|
| **Fecha** | 2026-11-12 |
| **Responde a** | [`evaluacion-specs-01.md`](evaluacion-specs-01.md), que queda intacto (commit `292e96b`) |
| **Decide** | Tech Lead. Todas las decisiones de la tabla son suyas |
| **Aplica** | IA (Claude Code) |

Procedimiento: el informe del evaluador no se modifica; se responde a cada
hallazgo. Los 26 hallazgos se aceptaron y se corrigieron; ninguno se
rechazó.

Lo que esta respuesta **no** demuestra: sigue sin haber código, tests ni
oráculo. Las correcciones son de documentos y nadie independiente las ha
vuelto a evaluar.

## 1. Respuesta por hallazgo

Donde el Tech Lead no dio un motivo aparte, figura el del propio hallazgo.

| Hallazgo | Sev. | Decisión | Motivo | Dónde se cambió |
|---|---|---|---|---|
| H-01 · La ficha difiere entre SPEC-01 y SPEC-03 | alta | Los cambios cruzados se aplican ya, no al aprobar. La ficha incluye `simulation_count` y `simulations`; CA-06 compara excluyéndolos | Con todo en borrador, mantener destinos incoherentes no tiene sentido | SPEC-01: 4.2, E-22, CA-06, D-13 · SPEC-02: CA-08 · SPEC-03: apartado 8 · SPEC-04: apartado 8 |
| H-02 · Supuestos sin citar | media | Corregir cabeceras e índice | El del hallazgo: la cabecera debe reflejar la dependencia real | SPEC-02: cabecera (A13, A14) · SPEC-03: cabecera, bloqueos y apartado 9 (A4, A16) · SPEC-04: cabecera, bloqueos y apartado 9 (A3, A6, A7, A12) · índice de specs |
| H-03 · Errores genéricos sin código | media | Códigos estables en las convenciones comunes: `400 malformed_request`, `415 unsupported_media_type`, `404 not_found`, `405 method_not_allowed` para cualquier método no admitido, `422 unknown_field` para un parámetro de consulta desconocido, `500 internal_error` sin trazas; todos en `problem+json` | El del hallazgo: son parte del contrato y nadie debe inventarlos al implementar | Índice de specs: «Errores genéricos» · SPEC-03: 2.7, 4.3, E-29, tabla 5.7, CA-09, CA-17 |
| H-04 · `id` sin máximo; SPEC-02 sin mínimo | media | Todo `id`, de ruta o de cuerpo, es un entero de 1 a 9223372036854775807; fuera de rango, `422 out_of_range`. Casos 0, −1 y 2^63 en las tablas | Es el máximo de `INTEGER` en SQLite | Índice: «Identificadores» · SPEC-01: 2.1, E-24, 4.2, tabla 5.10, CA-12 · SPEC-02: E-15, contrato, tabla 5.5, CA-07 · SPEC-03: 2.1, 4.1, tabla 5.2 |
| H-05 · CORS y `/health` sin requisito | media | Requisitos EARS con su criterio en un apartado «Operación del backend» de SPEC-03. `CORS_ORIGINS`, por defecto `http://localhost:4200`. `GET /health` → `200 {"status":"ok"}` si la base de datos responde y `503` si no | El del hallazgo: sin CORS el navegador no puede llamar al backend | SPEC-03: 2.7, E-24 a E-28, 4.4, tabla 5.6, CA-14 a CA-16 · SPEC-01: apartado 1 · SPEC-04: 2.9 · `supuestos.md`: A13, A16 |
| H-06 · El CIF no tiene fuente oficial y sus casos son circulares | media | Prueba diferencial con `python-stdnum`, fijado como dependencia solo de test: compara los dos validadores en todas las letras de entidad y en miles de números generados. Toda discrepancia se documenta y la decide el Tech Lead | Romper la circularidad de unos casos generados con el propio algoritmo | SPEC-01: 2.7, CA-19 · `requisitos.md`: nota sobre R-04 |
| H-07 · `frontend.md` admite «cadenas decimales» | media | Importes siempre enteros en céntimos | El del hallazgo: contradecía el contrato y A6 | `.claude/rules/frontend.md` |
| H-08 · `CLAUDE.md` prohíbe el `float` sin excepción | media | Excepción explícita: la conversión de divisa, solo para mostrar | El del hallazgo: la regla raíz contradecía a SPEC-04 y ADR-002 | `CLAUDE.md`: «Arquitectura» |
| H-09 · E-29 de SPEC-04 sin criterio | baja | Corregir | El del hallazgo | SPEC-04: CA-08 cita E-29; fila nueva de la fecha en 5.5 |
| H-10 · E-30 de SPEC-01 sin caso de parámetro desconocido | baja | Corregir | El del hallazgo | SPEC-01: tabla 5.9 (fila `limit=5`), CA-13 |
| H-11 · Dos casos de SPEC-03 5.5 sin requisito | baja | Corregir | El del hallazgo | SPEC-03: E-21 cubre el subtotal, la posición y el tramo repetido |
| H-12 · CA-15 remite a una tabla inexistente; dueño de los tipos ambiguo | baja | Una única constante de países (código, nombre y tipo) en el dominio; los tipos los define SPEC-02 y SPEC-01 la usa | El del hallazgo: no se sabía si había una constante o dos | SPEC-02: tabla nueva en 2.2 · SPEC-01: 2.1, 2.11, E-05, E-32, 4.1, CA-15 |
| H-13 · Referencias internas inexactas en SPEC-01 | baja | Corregir | El del hallazgo | SPEC-01: 2.1 (apartados del identificador) y 2.6 (las quince claves españolas, enumeradas) |
| H-14 · Se piden «ejemplos literales» que no existen | baja | Corregir | El del hallazgo | SPEC-01: 4.1, ejemplos nuevos del `409` y de dos `422` · SPEC-04: CA-05 y CA-08 dicen de dónde sale cada respuesta simulada |
| H-15 · `id` mal formado y simulador de cliente inexistente | baja | Un `422` por `id` mal formado y un `404` en el simulador muestran «Cliente no encontrado» | El del hallazgo: solo estaba especificado el `404` del detalle | SPEC-04: 2.4, 2.5, E-15, E-37, tabla 5.5, CA-07, CA-08 |
| H-16 · El panel no dice si muestra códigos o nombres | baja | El panel muestra los nombres de `/meta` | El del hallazgo | SPEC-04: 2.2, E-35, 4.1, tabla 5.3, CA-04 |
| H-17 · La fecha del tipo de cambio puede salir un día antes | baja | Se muestra tal cual, sin convertir de zona horaria | El del hallazgo: es una fecha sin hora | SPEC-04: 2.6, 2.8, E-29, fila nueva en 5.5 |
| H-18 · Regla inalcanzable y «se retiran los importes» ambiguo | baja | Eliminar el escenario inalcanzable. Un almacenamiento o un número de llamadas no válido no retira la proyección; solo desactiva «Guardar» | El del hallazgo: la proyección no depende de esos campos | SPEC-04: 2.5, 2.6, E-22, E-36, tabla 5.5 |
| H-19 · A17 sitúa el alta «en el panel» | baja | A17 dice ya que el alta está en una ruta propia | El de H-01 | `supuestos.md`: A17 · SPEC-04: apartado 8 |
| H-20 · Decisiones con alternativas fuera de los ADR; «dos tablas» | baja | Crear ADR-003 (API de divisas) y ADR-004 (persistencia); corregir «dos tablas» en ADR-001 | El del hallazgo: `CLAUDE.md` pide un ADR para las decisiones con alternativas | `02-arquitectura/`: ADR-003, ADR-004, ADR-001, README · SPEC-03: 2.6 y apartado 7 · SPEC-04: cabecera y apartado 7 |
| H-21 · Código de error de ejemplo inexistente | baja | Corregir | El del hallazgo | `CLAUDE.md`, `.claude/rules/backend.md`, `.claude/rules/frontend.md`: `invalid_tax_id_format` |
| H-22 · Ambigüedades de validación en SPEC-01 | baja | Recortar quita solo U+0020; cualquier carácter Cc o Cf → `invalid_characters`; longitudes en puntos de código; un error por campo, el primero que falle; `errors` en el orden de los campos del contrato; `field` es `id` para la ruta y `q` para la consulta; el límite de `q` se mide antes de recortar; un `tax_id` de más de 30 caracteres → `too_long` en cualquier país | El del hallazgo: obligaban a inventar la regla al implementar | SPEC-01: 2.1, apartado nuevo 2.12, E-02, E-03, E-30, E-34, E-35, 4.2, 4.3, tablas 5.4, 5.7 y 5.9, CA-07 · índice: «Errores de validación» |
| H-23 · `country` sin columna; precisión de `created_at` | baja | Columna `country` en `simulations`; `created_at` con precisión de segundos en las dos tablas | Que el historial lea solo lo guardado | SPEC-03: 2.1, 2.2, 2.6, E-03, tabla 5.4 · SPEC-01: 2.1 · índice: «Fechas con hora» |
| H-24 · Trazabilidad incompleta | baja | Corregir las columnas «Afecta a» y R-11. **`requisitos.md` queda aprobado** con fecha 2026-11-12 | El del hallazgo | `supuestos.md`: filas de A3, A4, A6, A7, A9, A12 y A13 · `requisitos.md`: estado y R-11 |
| H-25 · E-06 atribuye a ADR-002 una regla que no contiene | baja | Corregir | El del hallazgo | SPEC-04: apartado 1 y E-06, que remiten a `.claude/rules/frontend.md` |
| H-26 · Cambios cruzados pendientes de SPEC-04 | baja | Aplicarlos ya: ADR-002 a 200 ms y A8 con la lista cerrada | El de H-01 | ADR-002 · `supuestos.md`: A8 · SPEC-04: apartado 8 |

## 2. Precisiones que añadió la IA al aplicar las decisiones

Las decisiones dejaban algunos detalles sin fijar. Para no dejar otra
ambigüedad, la IA los concretó. **Ninguno está aprobado**: se listan para
que el Tech Lead los confirme o los cambie.

| # | Hallazgo | Precisión de la IA | Dónde |
|---|---|---|---|
| P-01 | H-22 | El **orden de las comprobaciones de cada campo**, del que depende cuál es «el primero que falle» (por ejemplo, en el nombre: `invalid_characters` antes que `too_short`) | SPEC-01, tabla de 2.12 |
| P-02 | H-22 | Los `unknown_field` van al final de `errors`, por orden alfabético del nombre del campo | SPEC-01, 2.12 |
| P-03 | H-22 | Un carácter Cc o Cf en el **email** da también `invalid_characters`; en el **identificador fiscal** sigue siendo `invalid_tax_id_format`, como cualquier otro carácter no admitido | SPEC-01, 2.12 |
| P-04 | H-03 | «Parámetro de consulta desconocido → `422 unknown_field`» se ha escrito como `422 validation_error` con el código de campo `unknown_field`, igual que un campo desconocido del cuerpo. Es una interpretación | Índice, tabla de errores genéricos |
| P-05 | H-03 | Además de la tabla del índice, que es lo pedido, se añadieron un requisito (E-29), casos (5.7) y un criterio (CA-17) en SPEC-03, para que los códigos genéricos no quedaran sin test | SPEC-03 |
| P-06 | H-05 | El `503` de `/health` lleva el código `service_unavailable` | SPEC-03, E-28 y 4.4 |
| P-07 | H-05 | `CORS_ORIGINS` es una lista separada por comas; nunca se responde con `*`; métodos `GET` y `POST` y cabecera `content-type`; caso de la comprobación previa `OPTIONS` | SPEC-03, 2.7 y tabla 5.6 |
| P-08 | H-16 | Si `/meta` falla, el panel muestra el error con «Reintentar», en lugar de enseñar los códigos | SPEC-04, 2.2 y tabla 5.3 |
| P-09 | H-15 | También una proyección que responde `404 customer_not_found` lleva a «Cliente no encontrado» | SPEC-04, E-37 |
| P-10 | H-14 | El informe describe el defecto pero no propone el arreglo. Se resolvió añadiendo tres ejemplos a SPEC-01 y cambiando la redacción de CA-05 y CA-08 de SPEC-04 | SPEC-01, 4.1 · SPEC-04 |
| P-11 | H-04, H-22, H-23 | Las reglas de identificadores, fechas con hora y «un error por campo» se escribieron también como convenciones comunes del índice, porque valen para todas las specs | Índice de specs |
| P-12 | H-02 | Se añadió A16 a la cabecera de SPEC-03, que ahora contiene el requisito de CORS, y A6 a la de SPEC-04 | SPEC-03, SPEC-04, índice |
| P-13 | H-20 | ADR-004 recoge también la decisión de las restricciones `CHECK` (SPEC-03, D-06), que no estaba en la lista del encargo pero tenía alternativas | ADR-004 |
| P-14 | H-20 | En ADR-001 se corrigió «dos tablas» y se añadió una nota que dice que el texto se corrigió y cuándo, para no reescribir en silencio un ADR aceptado | ADR-001 |

## 3. Lo que sigue sin verificar

- **`python-stdnum`** (H-06): el 2026-11-12 la última versión en PyPI era la
  2.2. No se ha instalado ni ejecutado. **No se sabe si su validación del
  CIF coincide con los grupos de letras de SPEC-01**; es justo lo que la
  prueba diferencial tiene que mostrar.
- **Ninguna de las tablas de casos nuevas** (SPEC-01 5.10; SPEC-02 5.5;
  SPEC-03 5.6 y 5.7; filas añadidas a SPEC-01 5.7 y 5.9, SPEC-03 5.2 y 5.4,
  SPEC-04 5.3 y 5.5) la ha ejecutado ningún código: son comportamiento
  esperado.
- **Que FastAPI permita devolver exactamente esos estados y códigos** en los
  errores genéricos (en especial el `400` y el `415`) sin código a medida:
  no se ha probado.
- Las correcciones no han pasado por una segunda evaluación independiente.
- Sigue en pie lo que el evaluador no pudo comprobar (apartado 4 de su
  informe).

## 4. Pendiente

| Asunto | Cuándo |
|---|---|
| Confirmar o cambiar las precisiones P-01 a P-14 | Revisión del Tech Lead |
| Decidir A2 a A5 | Viernes 13 de noviembre de 2026, 10:00 |
| Segunda evaluación independiente de las specs corregidas | A decidir por el Tech Lead |
| DDL definitivo (`schema.sql`) | Con el esqueleto del backend (R-15) |
