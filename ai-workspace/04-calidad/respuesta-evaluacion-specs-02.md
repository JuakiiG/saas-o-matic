# Respuesta a la segunda evaluación de las specs 01 a 04

| | |
|---|---|
| **Fecha** | 2026-11-12 |
| **Responde a** | [`evaluacion-specs-02.md`](evaluacion-specs-02.md), que queda intacto (commit `27b9373`) |
| **Decide** | Tech Lead. Todas las decisiones de la tabla son suyas |
| **Aplica** | IA (Claude Code) |
| **Commits** | `710917b` (specs y análisis) · `2469bd0` (arquitectura y ADR-005) |

Procedimiento: el informe del evaluador no se modifica; se responde a cada
hallazgo. El informe verifica los 26 hallazgos de la primera evaluación (22
resueltos, 4 resueltos en parte, ninguno sin resolver) y añade 17 nuevos,
N-01 a N-17. Los 17 se aceptaron y se corrigieron; ninguno se rechazó. Lo
pendiente de los cuatro resueltos en parte queda cubierto por N-02 (H-12),
N-08 (H-14), N-14 (H-20) y N-15 (H-06).

Lo que esta respuesta **no** demuestra: sigue sin haber código, tests ni
oráculo. Las correcciones son de documentos y nadie independiente las ha
vuelto a evaluar. Al escribirla quedaban cuatro cuestiones abiertas, que el
Tech Lead decidió después (apartado 3).

## 1. Respuesta por hallazgo

Donde el Tech Lead no dio un motivo aparte, figura el del propio hallazgo.

| Hallazgo | Sev. | Decisión | Motivo | Dónde se cambió |
|---|---|---|---|---|
| N-01 · Dependencia circular entre SPEC-01 y SPEC-03 | media | SPEC-01, SPEC-02 y SPEC-03 forman el bloque backend y se aprueban juntas. Orden de implementación: lo común (errores genéricos, CORS, `/health`, esquema), SPEC-02, SPEC-01, SPEC-03. «Depende de: SPEC-03» en SPEC-01. SPEC-04 se aprueba aparte, antes del frontend | El del hallazgo: aprobarlas una a una obliga a implementar una a medias o a programar otra sin aprobar | Índice: apartado nuevo «Bloques de aprobación y orden de implementación» · SPEC-01: cabecera y apartado 8 · SPEC-02: cabecera · SPEC-03: cabecera y apartado 9 · SPEC-04: cabecera |
| N-02 · SPEC-02 sitúa la lista de países en SPEC-01 (resto de H-12) | baja | Corregir como propone el informe | El del hallazgo | SPEC-02: apartado 1, «Dentro» y «Fuera» |
| N-03 · E-18 contradice a E-34 con un país no válido | baja | Con un país no válido o ausente, del identificador solo se comprueba lo que no depende del país: `missing`, `not_a_string`, `too_long`. Añadir casos | El del hallazgo | SPEC-01: 2.12, E-18, D-11, cinco filas en 5.7 |
| N-04 · El esquema no restringe los límites de los tramos | baja | `CHECK` `from_users >= 1` y `to_users IS NULL OR to_users >= from_users` | El del hallazgo: E-21 prometía más de lo que el esquema impedía | SPEC-03: 2.6, E-21, tres filas en 5.5 · ADR-004: nota |
| N-05 · El `405` choca con la comprobación previa de CORS | baja | `OPTIONS` queda fuera de la regla del `405`. Lo atiende el middleware de CORS: con origen admitido, `200` con sus cabeceras; con origen no admitido, `400` sin cabeceras CORS. Excepción documentada a `problem+json`. Además, los `500` llevan las cabeceras CORS | Esa respuesta la consume el navegador y no el frontend. Lo de los `500`: que el frontend vea `internal_error` y no `network_error` | SPEC-03: 2.7, 4.3, E-24, E-30, E-31, tres filas en 5.6, CA-15 · índice: fila del `405` y excepción · `supuestos.md`: A14 |
| N-06 · E-18 no espera a que el cliente exista | baja | Requisito EARS nuevo: mientras el cliente no se ha cargado, el simulador no pide ninguna proyección | El del hallazgo | SPEC-04: 2.5, E-18, E-38, una fila en 5.5, CA-08 |
| N-07 · Tres documentos sitúan el DDL en sitios distintos | baja | El DDL vive en el backend, en un `schema.sql` versionado. `02-arquitectura/` muestra el modelo y enlaza a ese fichero | El del hallazgo | SPEC-03: 2.6 · `02-arquitectura/README.md`: apartado «Modelo de datos» y «Pendiente» · ADR-004: nota. ADR-001 ya lo decía así y no se toca |
| N-08 · La fila de 20000 usuarios no tiene respuesta de origen (resto de H-14) | baja | Fila de 20000 usuarios en SPEC-02 5.1: 10000 / 32000 / 9975000 / 10017000 / 2103570 / 12120570 | El del hallazgo | SPEC-02: 5.1 · SPEC-04: fila de 5.5 y CA-08 |
| N-09 · Detalle y simulador con `/meta` caído; país en el simulador | baja | `/meta` se pide una vez al arrancar. Si falla, toda vista que necesite nombres (panel, alta, detalle y simulador) muestra el error con «Reintentar», sin códigos sueltos. El simulador muestra el nombre del país desde `/meta` | El del hallazgo | SPEC-04: 2.1, 2.2, 2.3, 2.4, 2.5, E-35, E-39, E-40, 4.1, filas en 5.3 y 5.5, CA-04, CA-05, CA-07, CA-08, D-14 |
| N-10 · La ayuda del navegador no fija la unidad de longitud | baja | La ayuda mide igual que el backend: puntos de código (`[...s].length`) y recorte solo de U+0020 | El del hallazgo: podía bloquear un alta válida | SPEC-04: 2.3, E-41, cuatro filas en 5.4, CA-05, D-13 |
| N-11 · Huecos en la normalización del identificador | baja | A mayúsculas solo `a`–`z` con una correspondencia explícita, nunca `upper()`; «espacio» es solo U+0020; U+00A0 → error de formato. Casos `ﬁ` y NBSP | El del hallazgo | SPEC-01: 2.2, E-08, dos filas en 5.4 y dos en 5.6 |
| N-12 · El carácter de escape de `LIKE` no está fijado | baja | El carácter de escape es `\` | El del hallazgo | SPEC-01: 2.10, E-27 |
| N-13 · Ambigüedades en los errores genéricos y la configuración | baja | `application/json` con parámetros (`charset`) es válido; precedencia `415` > `400` > `422`; `DATABASE_PATH` vale por defecto `backend/data/saas-o-matic.db` (ignorado por git) | El del hallazgo | Índice: tabla de errores genéricos y «Precedencia» · SPEC-03: 2.6, E-29, E-32, tres filas en 5.7, CA-12, D-10 |
| N-14 · Decisiones con alternativas fuera de los ADR (resto de H-20) | baja | ADR-005 para las dependencias de test (`python-stdnum` y Playwright). Criterio en el índice de arquitectura: lleva ADR toda decisión que afecte a la arquitectura o a más de una spec; las que solo afectan a una spec se quedan en su tabla de decisiones | El del hallazgo | `02-arquitectura/`: ADR-005 y README · SPEC-01: D-15 · SPEC-03 y SPEC-04: apartado 7 |
| N-15 · R-04 se presenta como «contrastado» (resto de H-06) | baja | R-04 en futuro («se contrastará»). CA-19 exacto: las 17 letras × 10 valores de control × dígito y letra, más 10.000 números con semilla fija. Resultado esperado: todo lo que el dominio acepta lo acepta `python-stdnum`, y las únicas diferencias son las de la forma del control según los grupos de D-01. Cualquier otra discrepancia la decide el Tech Lead. Comprobar el comportamiento real de la biblioteca cuando se instale | No se afirma lo que no existe | `requisitos.md`: nota de R-04 · SPEC-01: 2.7, CA-19 y su nota |
| N-16 · CA-19 fuera de la tabla de criterios | baja | Corregir como propone el informe | El del hallazgo | SPEC-01: apartado 6 |
| N-17 · Un caso de SPEC-03 5.4 sin requisito | baja | Corregir como propone el informe | El del hallazgo | SPEC-03: E-16 cubre el país guardado |
| H-13 · Residuo: «2.2 a 2.8» incluye el apartado de fuentes | — | Corregir como propone el informe | El del hallazgo | SPEC-01: 4.1, «2.2 a 2.6 y 2.8» |

## 2. Precisiones que añadió la IA al aplicar las decisiones

Las decisiones dejaban detalles sin fijar. La IA los concretó y los lista
aquí para que el Tech Lead los confirme o los cambie.

**Estado**: al escribir esta respuesta ninguna estaba aprobada, y estaban ya
en los commits `710917b` y `2469bd0`. **El Tech Lead aprobó las catorce,
P-01 a P-14, el 2026-11-12 a las 16:15.**

| # | Hallazgo | Precisión de la IA | Dónde |
|---|---|---|---|
| P-01 | N-01 | La fila «Depende de» de SPEC-01 cita, además de SPEC-03, a SPEC-02 (la constante de países). El párrafo «Por qué un bloque» y la correspondencia de «lo común» con requisitos concretos los escribió la IA | SPEC-01, cabecera · índice |
| P-02 | N-15 | **Composición del conjunto aleatorio de CA-19**: con cada uno de los 10.000 números se forman un DNI, un NIE y un CIF, cada uno con su carácter de control correcto y con uno incorrecto. La semilla es «una constante del test»; su valor no se ha fijado. El conjunto exhaustivo se contó: 340 identificadores | SPEC-01, CA-19 |
| P-03 | N-03 | «País no válido o ausente» es cualquier error de `country`: `missing`, `not_a_string` o `unsupported_country`. Los dos campos pueden traer error a la vez, en el orden del contrato (`tax_id` antes que `country`). Los cinco casos son de la IA | SPEC-01, 2.12 y 5.7 |
| P-04 | N-05 | Definición de «comprobación previa»: `OPTIONS` con `Origin` y `Access-Control-Request-Method`. El `200` lleva `access-control-allow-origin`, `POST` en `allow-methods` y `content-type` en `allow-headers`. Lo de los `500` se añadió a E-24, sin requisito nuevo. La excepción se escribió también en A14 y en el índice | SPEC-03 · índice · `supuestos.md` |
| P-05 | N-09 | Si `/meta` falla, la vista muestra el error **en lugar de su contenido** (en el panel, en lugar del buscador y la lista; en el alta, en lugar del formulario). Mientras `/meta` se carga, la vista muestra el estado de carga. «Reintentar» repite la petición de `/meta` | SPEC-04, 2.1 a 2.5, E-40 |
| P-06 | N-10 | Cuatro filas de prueba. Una dice que la ayuda **no rechaza** un tabulador en un extremo: lo envía y es el backend quien responde `invalid_characters` | SPEC-04, 5.4 |
| P-07 | N-11 | Se escribieron también los puntos de código del guion (U+002D) y del punto (U+002E). Además de los casos pedidos (`ﬁ` y NBSP) se añadió `12345679ſ`, que con `upper()` daría un DNI con la letra correcta | SPEC-01, 2.2, 5.4 y 5.6 |
| P-08 | N-13 | La ruta por defecto de `DATABASE_PATH` es **relativa a la raíz del repositorio**, y **si el directorio no existe, se crea**. Requisito E-32 y un test que comprueba el valor por defecto sin crear el fichero. La precedencia se escribió en E-29, con tres casos; no dice nada del `404` ni del `405` | SPEC-03, 2.6, E-29, E-32, 5.7, CA-12 |
| P-09 | N-14 | El contenido de ADR-005 (opciones comparadas, consecuencias, cuándo revisarla) es de la IA; la decisión es del Tech Lead. D-15 en SPEC-01 y D-14 en SPEC-04 recogen en sus tablas las decisiones de H-06 y N-09 | ADR-005 · SPEC-01 · SPEC-04 |
| P-10 | N-07 | El apartado «Modelo de datos» del índice de arquitectura resume las tres tablas. **No enlaza todavía al `schema.sql`**, porque el fichero no existe; el enlace queda pendiente | `02-arquitectura/README.md` |
| P-11 | N-04, N-07 | En ADR-004 no se reescribió el texto aceptado: se añadió una nota fechada, como se hizo con ADR-001 en la primera respuesta (P-14) | ADR-004 |
| P-12 | N-04 | Tres filas de prueba, una de ellas de inserción **aceptada** (`to_users` igual a `from_users`, o nulo) | SPEC-03, 5.5 |
| P-13 | N-08 | La fila de SPEC-04 5.5 dice ahora el total esperado: 121.205,70 EUR | SPEC-04, 5.5 |
| P-14 | N-06 | Además del requisito nuevo (E-38), se añadió a E-18 la condición «y el cliente ya se ha cargado», para que los dos no se contradigan. Fila de prueba con un cliente que tarda 500 ms | SPEC-04, E-18 y 5.5 |

## 3. Cuestiones abiertas para el Tech Lead

Casos que las decisiones no cubren. La IA **no** los ha resuelto.

| # | Cuestión | Dónde está anotada |
|---|---|---|
| Q-01 | **`OPTIONS` fuera de los dos casos decididos**: un `OPTIONS` que no es una comprobación previa (sin `Origin` o sin `Access-Control-Request-Method`), y una comprobación previa de un origen admitido que pide un método o una cabecera no admitidos (por ejemplo `DELETE`) | SPEC-03, 2.7, marcado «Sin especificar» |
| Q-02 | **«`400` sin cabeceras CORS»**: la IA recuerda, **sin haberlo verificado**, que el middleware de CORS estándar del framework, al rechazar una comprobación previa, omite `access-control-allow-origin` pero puede incluir otras cabeceras `access-control-*` (métodos, caducidad). Si es así, cumplir la spec al pie de la letra exige código a medida, o bien precisar la regla como «sin `access-control-allow-origin`». Se comprueba al implementar | SPEC-03, E-31 y 5.6 |
| Q-03 | **El criterio nuevo de los ADR frente a decisiones ya tomadas**: hay decisiones que afectan a más de una spec y no tienen ADR. Las que la IA ha visto: el historial dentro de la ficha (SPEC-03/D-01, que cambia el contrato de SPEC-01), la constante única de países (SPEC-01 y SPEC-02), las convenciones comunes de errores del índice y el bloque de aprobación de N-01. La IA no ha creado ADR para ninguna | `02-arquitectura/README.md` |
| Q-04 | **El valor de la semilla de CA-19** y la composición del conjunto aleatorio (P-02) | SPEC-01, CA-19 |

**Decididas por el Tech Lead el 2026-11-12 a las 16:15**:

| # | Decisión | Dónde se aplicó |
|---|---|---|
| Q-01 | Un `OPTIONS` que no es una comprobación previa responde `405` `method_not_allowed` | SPEC-03: 2.7, 4.3, E-33, una fila en 5.7, CA-17 · índice |
| Q-02 | Sin código a medida. La comprobación previa rechazada se queda con el comportamiento estándar del middleware de CORS; un test fija exactamente su estado y sus cabeceras, y lo que se exige es que no lleve `access-control-allow-origin` | SPEC-03: 2.7, E-31, dos filas en 5.6, CA-15 · índice · `supuestos.md`: A14 |
| Q-03 | ADR-006 «Convenciones transversales de la API»: errores genéricos y `problem+json`, identificadores, fechas, constante única de países e historial dentro de la ficha. El bloque de aprobación es proceso, no arquitectura, y se queda en el índice de specs | `02-arquitectura/`: ADR-006 y README · índice de specs · SPEC-03: apartado 7 |
| Q-04 | Semilla `20261112` | SPEC-01: CA-19 |

**Precisión de la IA al aplicar Q-02, sin aprobar (P-15)**: la segunda mitad
de Q-01 (una comprobación previa de un origen admitido que pide un método o
una cabecera no admitidos) no tenía decisión propia. La IA le aplicó la de
Q-02: respuesta estándar del middleware, fijada por un test. La exigencia
de no llevar `access-control-allow-origin` se escribió solo para el origen
no admitido, que es el caso de la decisión; la IA no sabe qué cabeceras
devuelve el middleware cuando el origen sí está admitido y lo rechazado es
el método. El estado esperado del rechazo (`400`) figura en SPEC-03 como
**no verificado**.

## 4. Lo que sigue sin verificar

- **`python-stdnum`**: no se ha instalado ni ejecutado. El resultado
  esperado de CA-19 es una hipótesis. El evaluador dice recordar, también
  sin verificarlo, que la biblioteca acepta dígito o letra en todas las
  letras de entidad, lo que coincidiría con esa hipótesis. Dos recuerdos no
  son una comprobación.
- **Playwright**: no se ha instalado.
- **Que el framework añada las cabeceras CORS a un `500`** de una excepción
  no capturada sin código a medida (lo señala el evaluador en su apartado
  4), y lo dicho en Q-02.
- **Que el framework acepte `application/json; charset=utf-8`** y permita
  la precedencia `415` > `400` > `422` sin código a medida.
- **Ninguna de las filas de casos nuevas** la ha ejecutado ningún código:
  son comportamiento esperado.
- Las correcciones no han pasado por una tercera evaluación independiente.
- Sigue en pie lo que el evaluador no pudo comprobar (apartado 4 de su
  informe).

Lo que sí se ha comprobado, con `python` y Node 24 fuera del repo:
`12345679 mod 23 = 15` (letra `S`); `'ſ'.upper()` da `S` y `'ﬁ'.upper()`
da `FI`; la fila de 20000 usuarios (10000 / 32000 / 9975000 / 10017000 /
2103570 / 12120570) con la fórmula de SPEC-02; `121.205,70 EUR` con
`Intl.NumberFormat('es-ES')`; `'𝔸'.repeat(61)` mide 122 con `length` y 61
con `[...s].length`; `'\tAB'.trim()` da `AB`.

## 5. Pendiente

| Asunto | Cuándo |
|---|---|
| ~~Aprobar o cambiar P-01 a P-14 y decidir Q-01 a Q-04~~ | Hecho el 2026-11-12 a las 16:15 |
| Aprobar o cambiar P-15 | A decidir por el Tech Lead |
| Fijar en un test el estado y las cabeceras de la comprobación previa rechazada | Al implementar CORS |
| Decidir A2 a A5 | Viernes 13 de noviembre de 2026, 10:00 |
| Aprobar el bloque backend (SPEC-01, SPEC-02 y SPEC-03) y, aparte, SPEC-04 | Tras lo anterior |
| Comprobar el comportamiento real de `python-stdnum` | Cuando se instale |
| `schema.sql` y su enlace desde el índice de arquitectura | Con el esqueleto del backend |
| Tercera evaluación independiente | A decidir por el Tech Lead |
