# Evaluación documental de las especificaciones (segunda pasada)

- **Fecha**: 2026-11-12
- **Evaluador**: subagente independiente, solo lectura.
- **Leído**: `00-analisis/`, `01-specs/` (índice y SPEC-01 a SPEC-04), `02-arquitectura/` (README y ADR-001 a ADR-004), `CLAUDE.md`, `.claude/rules/` y, con la excepción autorizada, `04-calidad/evaluacion-specs-01.md`.
- **No leído**: ningún otro fichero de `04-calidad/`, nada de `03-proceso/`. No he usado `git log`, `git show` ni `git diff`.

## 1. Resumen

**Alcance.** He comprobado los 26 hallazgos de la primera evaluación contra el estado actual de los documentos. También he buscado contradicciones nuevas entre specs, ADR, supuestos, requisitos y reglas.

**Qué no aplica.**
- **Oráculo:** no existe. `ls scripts` → `No such file or directory`.
- **Código y tests:** no hay. `backend/` y `frontend/` están vacíos.
- **Consecuencia:** no se ha ejecutado nada del producto y ningún requisito está demostrado por un test.

**Cifras recalculadas.** Todas cuadran. Usé `python -c` y Node 24.18.0 con `Intl.NumberFormat('es-ES')`:
- **SPEC-01:**
  - 5.2: letras de DNI y NIE, y los valores de pares, impares y `C` del CIF.
  - 5.9: los 15 órdenes del buscador, incluido `5, 2, 3, 6, 7, 4, 1`.
  - Formas de búsqueda de CA-18.
  - Caracteres U+FF18 (línea 545) y U+200B, categoría Cf (línea 586): presentes.
- **SPEC-02:** 5.1, 5.2 y 5.3.
- **SPEC-03:** 5.1 y 5.4, incluido 24000 / 2400 / 26400.
- **SPEC-04:** las 28 celdas de 5.1. El separador es U+00A0 y el céntimo de diferencia en USD se confirma (155,95 + 32,75 = 188,70 frente a 188,69).

| Veredicto | H-xx |
|---|---|
| RESUELTO | 22 |
| RESUELTO EN PARTE | 4 (H-06, H-12, H-14, H-20) |
| NO RESUELTO | 0 |

**Hallazgos nuevos: 17** (1 media, 16 baja). Incluyen lo pendiente de los cuatro resueltos en parte. El más relevante es N-01: las correcciones de H-01, H-03 y H-05 crean una dependencia circular entre SPEC-01 y SPEC-03.

## 2. Verificación de H-01 a H-26

| H | Veredicto | Evidencia |
|---|---|---|
| H-01 | RESUELTO | Hay un solo contrato de la ficha:<br>• `SPEC-01:409-413` (4.2): siete campos del alta más `simulation_count` y `simulations`, en la forma de SPEC-03.<br>• `SPEC-01:279` (E-22).<br>• `SPEC-01:676` (CA-06 excluye los dos campos).<br>• `SPEC-03:269-292`; `SPEC-03:471-480` («Aplicado»); `SPEC-04:480`.<br>Desaparece la incoherencia del destino. Efecto colateral en N-01 |
| H-02 | RESUELTO | Cabeceras e índice coinciden con los supuestos citados en cada spec. Comando: `grep -o '\bA[0-9]{1,2}\b'` por spec da:<br>• SPEC-01: A2 A4 A10–A14 A18.<br>• SPEC-02: A2–A7 A9 A13 A14.<br>• SPEC-03: A3 A4 A6 A7 A9 A13 A14 A16 A18.<br>• SPEC-04: A3 A6–A9 A12–A14 A16 A17.<br>Los cuatro conjuntos son idénticos a `SPEC-0x:7` y a `01-specs/README.md:10-13`. A3 figura como bloqueo de SPEC-04 (`SPEC-04:9`) |
| H-03 | RESUELTO | • Tabla de errores genéricos con estado y `code`: `01-specs/README.md:94-109`.<br>• Requisito: `SPEC-03:215` (E-29).<br>• Casos: `SPEC-03:416-426` (5.7).<br>• Criterio: `SPEC-03:448` (CA-17).<br>• `405` para cualquier método: `SPEC-03:296-300`.<br>Quedan ambigüedades menores (N-13) y un choque con la comprobación previa de CORS (N-05) |
| H-04 | RESUELTO | • Rango 1..2^63−1 en `README.md:61-64`, `SPEC-01:281` (E-24) y `SPEC-02:105` (E-15).<br>• SPEC-02 fija `out_of_range` para `0` y `-1` (`SPEC-02:240-241`).<br>• Casos de 2^63: `SPEC-01:663`, `SPEC-02:242`, `SPEC-03:348` |
| H-05 | RESUELTO | • `SPEC-03:150-160` (2.7).<br>• `SPEC-03:210-214` (E-24 a E-28), `SPEC-03:302-314` (4.4), `SPEC-03:404-414` (5.6), CA-15 y CA-16.<br>• `supuestos.md:230` y `supuestos.md:249` remiten a SPEC-03 |
| H-06 | RESUELTO EN PARTE | • La circularidad se ataca con una prueba diferencial: `SPEC-01:144-152`, `SPEC-01:690` (CA-19).<br>• `requisitos.md:33-39` documenta la desviación de R-04.<br>Pendiente en N-15 |
| H-07 | RESUELTO | `frontend.md:53-56`: «siempre como enteros en céntimos» |
| H-08 | RESUELTO | `CLAUDE.md:60-63` recoge la excepción de la conversión de divisa, coherente con:<br>• `SPEC-04:145-148`;<br>• `ADR-002:78`;<br>• `frontend.md:54-56` |
| H-09 | RESUELTO | `SPEC-04:423` (CA-08 cita E-29), con filas en `SPEC-04:407-408` |
| H-10 | RESUELTO | `SPEC-01:649` (`limit=5` → `unknown_field`). CA-13 dice «las tres de error» (`SPEC-01:683`) y 5.9 tiene tres filas de error (`SPEC-01:647-649`) |
| H-11 | RESUELTO | `SPEC-03:202` (E-21 cubre el subtotal, la posición y el tramo repetido). Queda una incoherencia nueva en N-04 |
| H-12 | RESUELTO EN PARTE | • La constante única se define en `SPEC-02:48-67`.<br>• `SPEC-01:201-204` y CA-15 (`SPEC-01:685`) remiten a «tabla 2.2 de SPEC-02», que ya existe.<br>Pendiente: `SPEC-02:19-20` (N-02) |
| H-13 | RESUELTO | • `SPEC-01:31` remite a «2.3 a 2.6 para España, 2.8 para el resto».<br>• `SPEC-01:93-95` cuenta 15 letras más `N` y `W` (17).<br>Residuo trivial: `SPEC-01:309` dice «2.2 a 2.8», que incluye 2.7 (fuentes) |
| H-14 | RESUELTO EN PARTE | • Ejemplos de `409`, `invalid_tax_id_format` y de dos campos en `SPEC-01:362-401`.<br>• `SPEC-04:420` (CA-05) y `SPEC-04:423` (CA-08) dicen de dónde salen las respuestas simuladas.<br>Pendiente: la fila de 20000 usuarios (N-08) |
| H-15 | RESUELTO | `SPEC-04:94-96`, `SPEC-04:104-107`, `SPEC-04:240` (E-15), `SPEC-04:254` (E-37), `SPEC-04:404-406`, `SPEC-04:422` (CA-07). Queda una ambigüedad nueva en N-06 |
| H-16 | RESUELTO | `SPEC-04:50-53`, `SPEC-04:219` (E-35), `SPEC-04:284`, `SPEC-04:372-373`. Para el panel, sí. El detalle y el simulador con `/meta` caído, en N-09 |
| H-17 | RESUELTO | `SPEC-04:158-160`, `SPEC-04:197-199`, `SPEC-04:266` (E-29), `SPEC-04:407` |
| H-18 | RESUELTO | • El escenario inalcanzable ya no aparece en 2.6 (`SPEC-04:161-177`).<br>• Almacenamiento y llamadas no válidos no retiran la proyección: `SPEC-04:110-112`, `SPEC-04:253` (E-36), `SPEC-04:403` |
| H-19 | RESUELTO | `supuestos.md:254-255`: «ruta propia (`/clientes/nuevo`)» |
| H-20 | RESUELTO EN PARTE | • Los tres casos citados pasan a `ADR-003` y `ADR-004`.<br>• `ADR-001:106` y `ADR-001:117-120` corrigen las «dos tablas».<br>Pendiente en N-14 |
| H-21 | RESUELTO | `CLAUDE.md:89`, `backend.md:46` y `frontend.md:49` usan `invalid_tax_id_format` |
| H-22 | RESUELTO | `SPEC-01:206-233` (2.12) fija el recorte (solo U+0020), Cc/Cf, puntos de código, un error por campo y su orden, el orden de `errors`, el valor de `field` y el límite de `q` antes de recortar. `SPEC-01:248` (E-34). Queda una contradicción nueva en N-03 |
| H-23 | RESUELTO | • `SPEC-03:107` (columna `country`), `SPEC-03:53-55` y `SPEC-03:390-391`.<br>• `ADR-004:36-40`.<br>• Precisión de segundos en `SPEC-01:37-38` |
| H-24 | RESUELTO | • `supuestos.md:25-35`: completada la columna «Afecta a».<br>• `requisitos.md:30`: R-11 incluye SPEC-01.<br>• `requisitos.md:4`: `aprobado` |
| H-25 | RESUELTO | `SPEC-04:22-23` y `SPEC-04:226` (E-06) remiten a `.claude/rules/frontend.md` |
| H-26 | RESUELTO | `ADR-002:41` («200 ms»); `supuestos.md:173-174` (lista cerrada) |

## 3. Hallazgos nuevos

### N-01 · media · Dependencia circular entre SPEC-01 y SPEC-03 por el orden de aprobación

**Defecto.** Las correcciones de H-01, H-03 y H-05 llevan a SPEC-03 comportamiento que SPEC-01 necesita para implementarse:
- La ficha debe incluir el historial «en la forma que define SPEC-03», lo que exige la tabla `simulations`.
- Los errores genéricos y CORS de los endpoints de SPEC-01 se exigen en SPEC-03.

A la vez, SPEC-03 no puede aprobarse hasta que SPEC-01 lo esté. `CLAUDE.md` prohíbe escribir código de una parte sin su spec aprobada. Por tanto, al implementar SPEC-01 hay que dejar E-22 a medias o escribir código de SPEC-03 sin aprobar. SPEC-01 no declara depender de SPEC-03: su cabecera no tiene fila «Depende de».

**Evidencia**:
- `SPEC-01:279` (E-22: «en la forma que define SPEC-03»).
- `SPEC-01:21` (CORS, `/health` y errores genéricos remitidos fuera).
- `SPEC-03:8-9`: «Depende de SPEC-01… Bloqueos: SPEC-01 y SPEC-02 sin aprobar».
- `README.md:106-109`: el requisito de los errores genéricos está en SPEC-03.
- `CLAUDE.md:19-20`.
- `SPEC-01:3-8`: sin dependencia de SPEC-03.

**Afecta a**: SPEC-01/E-22, SPEC-03 (bloqueos), índice, regla de flujo de `CLAUDE.md`.

### N-02 · baja · SPEC-02 sigue situando la lista de países en SPEC-01 (pendiente de H-12)

**Defecto.** El apartado «Fuera» de SPEC-02 deja la lista de países a SPEC-01. El apartado 2.2 de la misma spec dice que esa lista es suya y única.

**Evidencia**:
- `SPEC-02:19-20`: «**Fuera**: … alta de clientes y lista de países admitidos (SPEC-01)».
- `SPEC-02:63-67`: «Es la **única** lista de países del sistema… Esta spec es la dueña».

### N-03 · baja · E-18 contradice a E-34 cuando el país no es válido

**Defecto.**
- E-18 manda no validar el identificador si el país no es válido.
- E-34 manda `too_long` «sea cual sea el país».
- El orden de 2.12 empieza el identificador por `missing` y `not_a_string`, que no dependen del país.

No se puede deducir:
- qué devuelve `country: "XX"` con un `tax_id` de 31 caracteres, ausente o numérico;
- si «país no válido» incluye un país ausente.

La única fila de prueba usa un identificador de 9 caracteres.

**Evidencia**: `SPEC-01:265` (E-18), `SPEC-01:248` (E-34), `SPEC-01:221`, `SPEC-01:602`.

### N-04 · baja · E-21 exige rechazar cualquier valor negativo, pero el esquema no restringe los límites de los tramos

**Defecto.** E-21 promete que la base de datos rechaza «una fila con un valor negativo». En `simulation_tiers`, `from_users` solo es «No nulo» y `to_users` no tiene restricción. Un `from_users = -1` se guardaría.

**Evidencia**: `SPEC-03:202` frente a `SPEC-03:120-121`.

### N-05 · baja · La regla del `405` choca con la comprobación previa de CORS (`OPTIONS`)

**Defecto.**
- 4.3 dice que «cualquier método que una ruta no admite responde `405`».
- Ninguna ruta declara `OPTIONS`.
- La tabla 5.6 exige que `OPTIONS /customers` responda «sin error».

Además, no está definido qué responde una comprobación previa con un `Origin` no admitido. La regla general exige que todo error vaya en `application/problem+json` (A14).

La fila de 5.6 tampoco fija el estado esperado («Respuesta sin error»), así que es poco comprobable.

**Evidencia**: `SPEC-03:296-300`, `SPEC-03:412`, `supuestos.md:239-241`.

### N-06 · baja · E-18 no dice que la proyección espera a que el cliente exista

**Defecto.**
- La tabla de casos exige 0 proyecciones al abrir `/clientes/999/simulacion`, y 2.5 dice que en ese caso «no se pide ninguna proyección».
- E-18 manda pedir la proyección en cuanto el valor lleva 200 ms sin cambiar y es válido; el valor inicial, 10, lo es.

Si el `GET /customers/{id}` tarda más de 200 ms, E-18 obliga a una petición que la tabla prohíbe. Ningún requisito EARS condiciona la proyección a la respuesta del cliente.

**Evidencia**: `SPEC-04:252` (E-18), `SPEC-04:104-107`, `SPEC-04:396`, `SPEC-04:404-405`.

### N-07 · baja · Tres documentos sitúan el DDL en sitios distintos

**Defecto.**
- SPEC-03 dice que el DDL definitivo irá en `02-arquitectura/`.
- El README de arquitectura dice que `schema.sql` se escribe con el esqueleto del backend.
- ADR-001 y ADR-004 lo describen como un fichero versionado que se aplica al arrancar, es decir, código del backend.

**Evidencia**: `SPEC-03:81-82` frente a `02-arquitectura/README.md:29-31`, `ADR-001:110-111` y `ADR-004:61`.

### N-08 · baja · La fila de 20000 usuarios de SPEC-04 5.5 no tiene respuesta de origen (pendiente de H-14)

**Defecto.** CA-08 limita los importes simulados a las filas de 10, 15 y 51 usuarios de SPEC-02 5.1. La fila «Escribir `20000`» necesita una respuesta de 20000 usuarios, que no figura en ninguna tabla. El valor recalculado es base 10017000, impuesto 2103570 y total 12120570.

**Evidencia**: `SPEC-04:399` y `SPEC-04:423`. Comando: `python -c` con la fórmula de `SPEC-02:36-38` → `20000 10000 32000 9975000 10017000 2103570 12120570`.

### N-09 · baja · Sin especificar: el detalle y el simulador con `/meta` caído, y cómo muestra el país el simulador

**Defecto.**
- Solo el panel y el alta dicen qué pasa si `/meta` falla. El detalle también usa los nombres de `/meta` y no lo dice.
- El simulador muestra el «país del cliente» y no consume `/meta`, así que queda abierto si muestra `ES` o «España»: es el defecto de H-16 trasladado a otra vista.
- En el panel, «no se muestran códigos en lugar de nombres» no aclara si la lista de resultados se oculta entera.

**Evidencia**: `SPEC-04:52-53`, `SPEC-04:85-86`, `SPEC-04:284`, `SPEC-04:287`, `SPEC-04:373`.

### N-10 · baja · La validación de ayuda del navegador no fija la unidad de longitud y puede bloquear un alta válida

**Defecto.** El backend mide en puntos de código (2.12). SPEC-04 2.3 no fija ni la unidad ni el recorte del navegador. En JavaScript, `length` cuenta unidades UTF-16 y `trim()` quita también tabuladores y saltos de línea. Un nombre válido para el backend puede ser rechazado por la «ayuda» del navegador.

**Evidencia**:
- `SPEC-04:64-66`.
- `SPEC-01:215`.
- Comando: `node -e 's="𝔸".repeat(61); console.log(s.length,[...s].length)'` → `122 61`. Son 61 puntos de código, válidos en el backend (máximo 120), pero superan 120 en el navegador.

### N-11 · baja · Normalización del identificador con huecos sin caso de prueba

**Defecto 1. Mayúsculas fuera de ASCII.** 2.2 pasa a mayúsculas solo `a`–`z`, pero ninguna fila prueba una minúscula no ASCII que `str.upper()` convierta en ASCII. Una implementación con `upper()` convertiría `ﬁ` en `FI` y aceptaría, por ejemplo, un identificador francés que la regla rechaza. Ninguna prueba lo detectaría: la única fila no ASCII usa `Ñ` mayúscula.

**Defecto 2. «Espacios» sin definir.** 2.2 no define qué cuenta como «espacio». Para el recorte, 2.12 sí lo define (solo U+0020). Queda abierto qué pasa con U+00A0 dentro del identificador.

**Evidencia**: `SPEC-01:47-49`, `SPEC-01:546`. Comando: `python -c "print([c.upper() for c in 'ſﬁıß'])"` → `['S', 'FI', 'I', 'SS']`.

### N-12 · baja · El carácter de escape de `LIKE` no está fijado

**Defecto.** 2.10 exige escapar «el propio carácter de escape», sin decir cuál es. La fila de prueba usa `\`, que solo prueba E-27 si se elige `\`.

**Evidencia**: `SPEC-01:187-189` y `SPEC-01:643`.

### N-13 · baja · Ambigüedades en los errores genéricos y en la configuración

**Puntos sin regla**:
- Si `application/json; charset=utf-8` es un `Content-Type` válido (`README.md:100`).
- La precedencia cuando coinciden un `400` o un `415` del cuerpo con un parámetro de consulta desconocido (`README.md:99-103`).
- El valor por defecto de `DATABASE_PATH`. `backend.md:49-50` exige valores por defecto para local y SPEC-03 solo lo da para `CORS_ORIGINS` (`SPEC-03:141-143` frente a `SPEC-03:151-152`).

### N-14 · baja · Decisiones con alternativas que siguen fuera de los ADR (pendiente de H-20)

**Defecto 1. Dependencias nuevas sin ADR.** `CLAUDE.md:64` exige un ADR para las decisiones con alternativas. Dos dependencias nuevas no tienen ADR:
- `python-stdnum`: tampoco figura en la tabla de decisiones D-01 a D-14 de SPEC-01.
- Playwright: SPEC-04 D-09, donde la alternativa era la comprobación manual.

**Defecto 2. Criterio de selección sin explicar.** SPEC-03 documenta alternativas descartadas para sus diez decisiones y solo pasa tres a ADR-004. No explica el criterio. Por ejemplo, D-01 (historial dentro de la ficha) cambia el contrato de otra spec.

**Evidencia**: `SPEC-01:144-152`, `SPEC-01:705-720`, `SPEC-04:454`, `SPEC-03:452-458`.

### N-15 · baja · R-04 se presenta como «contrastado» antes de que exista el contraste (pendiente de H-06)

**Defecto.** `requisitos.md` dice en presente que el CIF está «contrastado con una implementación independiente». Pero el test no existe y SPEC-01 admite que no se sabe si la biblioteca coincide con los grupos de D-01. Si la biblioteca no distingue letra y dígito según la entidad, los grupos no quedan contrastados en absoluto: solo se acumularían discrepancias aceptadas.

CA-19 tampoco es del todo comprobable: «varios miles» no es una cantidad fijada.

**Evidencia**: `requisitos.md:37-39`, `SPEC-01:150-152`, `SPEC-01:690`, `SPEC-01:697-698`.

**Afecta a**: R-04 y la regla de honestidad sobre el estado de `CLAUDE.md`.

### N-16 · baja · CA-19 queda fuera de la tabla de criterios

**Defecto.** Una línea en blanco separa CA-19 de la tabla, así que en Markdown no se presenta como fila de la tabla de criterios.

**Evidencia**: `sed -n '688,690p' SPEC-01… | cat -A` → `| CA-18 |…$`, `$`, `| CA-19 |…$`.

### N-17 · baja · Un caso de 5.4 de SPEC-03 no responde a ningún requisito EARS

**Defecto.** Las filas de 5.4 que comprueban que `country` se lee de la simulación no las cubre ningún requisito:
- E-16 solo habla de «importes guardados».
- CA-08 solo cita E-16.

Es el mismo tipo de defecto que H-11.

**Evidencia**: `SPEC-03:192` (E-16), `SPEC-03:390-391`, `SPEC-03:439`.

## 4. Lo que no he podido comprobar

- **Oráculo, código y tests**: no existen, así que ningún requisito está demostrado. Dependen de herramientas o fases futuras:
  - CA-17 de SPEC-01;
  - CA-09 de SPEC-02;
  - CA-12 a CA-15 de SPEC-04;
  - CA-19 de SPEC-01, que necesita `python-stdnum`.
- **`python-stdnum`**: no está instalado (`ModuleNotFoundError: No module named 'stdnum'`). No lo he instalado para no crear ficheros. Por lo que recuerdo de esa biblioteca, sin haberlo verificado, su validación del CIF acepta dígito o letra en todas las letras de entidad. Si es así, CA-19 dará discrepancias sistemáticas en los grupos «exigen letra» y «exigen dígito» de D-01. Hay que comprobarlo antes de aprobar SPEC-01.
- **CORS en las respuestas `500`**: E-24 se aplica a cualquier respuesta. No he verificado si el framework añade la cabecera CORS a los `500` de excepciones no capturadas. Si no la añade, el frontend vería `network_error` en vez de `internal_error`. 5.6 solo prueba `GET /meta`.
- **Fuentes externas**: no he consultado el BOE, la AEAT, el Ministerio del Interior, la Comisión Europea, GOV.UK ni Frankfurter. Los tipos de A4 y la forma real de la respuesta `v2` no están verificados por mí.
- **Formato en navegadores**: lo he verificado solo en Node 24.18.0, no en navegadores reales.
- **Fuera del alcance de la excepción**: no he leído `03-proceso/` ni el resto de `04-calidad/`. Tampoco he revisado el `README.md` raíz (R-18), `.claude/settings.json` ni `.claude/agents/evaluador.md`.
