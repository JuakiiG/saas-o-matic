# Evaluación independiente del backend, segunda pasada (verificación de H-01 a H-15 y A-01)

- **Fecha y hora**: 2026-11-13 19:31 (inicio) y 19:37 (fin), según `date`.
- **Agente**: evaluador independiente (subagente de Claude Agent SDK), de contexto limpio. Trabajo en solo lectura.
- **Modelo**: Claude Opus 5.5 (`claude-opus-5-5`).
- **Herramientas**: `uv` 0.12.13 y Python 3.12.0 (el entorno de `backend/`).
- **Leído**: `ai-workspace/01-specs/README.md`, SPEC-01 (2.1, 2.10 a 2.12, 3, 5.7 a 5.10, CA y su historial), SPEC-02 (E-14 y las notas que mencionan limitaciones), SPEC-03 (2.7, 4.3, E-07, E-29, E-33, CA-13, CA-17, la tabla de 5.7 y el historial), `CLAUDE.md`, `.claude/rules/backend.md`, el código de `backend/app/` y los tests de `backend/tests/` relacionados con cada hallazgo.
- **No leído**: `ai-workspace/03-proceso/` ni `ai-workspace/04-calidad/`. No he leído historia de git con `git log`, `git show` ni `git diff`.
- **Sondas**: scripts fuera del repositorio, ejecutados con `TestClient(create_app(), raise_server_exceptions=False)` y `DATABASE_PATH` dentro del directorio temporal del sistema. Al terminar he borrado esas bases de datos.
- **Estado del repo al terminar**: `git status --short` sale vacío y `git rev-parse --short HEAD` da `eb0a27f`.

## 1. Resumen

- **Oráculo** (`uv run scripts/check.py`): `ORÁCULO EN VERDE (solo lo activo: lo inactivo no está comprobado) · 20 correctas, 0 con fallo, 4 inactivas`. Las cuatro inactivas son del frontend, porque no existe `frontend/package.json`. Las ramas del backend están cubiertas en 92 de 92 y el dominio, al 100 %.
- **Tests del backend** (`cd backend && uv run pytest -q`): `731 passed in 25.07s`.
- **Recuento de veredictos**:
  - 12 `CORREGIDO`: H-01, H-02, A-01, H-05, H-07, H-08, H-09, H-10, H-11, H-12, H-14 y H-03 (este último sin cambio de código).
  - 3 `CONFORME A LO DECIDIDO`: H-04, H-06 y H-15.
  - 1 sin veredicto posible: H-13 tiene los comentarios pedidos, pero no se puede saber si están todos sin leer la historia (ver 5).
- **Hallazgos nuevos**: 3 (N-01 de gravedad media; N-02 y N-03, baja).

## 2. Tabla por hallazgo

| Id | Veredicto | Evidencia |
|---|---|---|
| H-01 | CORREGIDO | `GET /customers/` seguido de 4301 nueves, 20000 nueves, un signo menos y 4301 nueves, un signo menos y 20000 nueves, o `1` seguido de 4300 ceros: siempre `422` con `id: out_of_range`. Con 4300 nueves, también `422` `out_of_range`. Con un `0` delante, un `+` delante, una `x` detrás o un espacio delante, todo con más de 4300 dígitos: `422` `not_an_integer`. Código: `backend/app/api/validation.py:25`. Test: `backend/tests/integration/test_customers_read.py:116-121`. Filas en SPEC-01 5.10:718-720 |
| H-02 | CORREGIDO | Un `\ud800` en cualquiera de los cinco campos de `POST /customers` da `400` `malformed_request`. Código: `backend/app/api/request_guard.py:40-51,69`. Tests: `backend/tests/integration/test_body_text.py:30-44,93-101`, que además comprueban que no se guarda nada. Regla en `ai-workspace/01-specs/README.md:156,177-184`. Un emoji, escrito como pareja de escapes o en UTF-8, da `201` y se lee igual después (`test_body_text.py:130-141`, y mi sonda) |
| A-01 | CORREGIDO | Un nombre de campo `"x\ud800"` da `400` en los tres `POST`. También dan `400`: `\udfff` suelto, el `\ud800` dentro de una lista, como clave de un objeto anidado, a tres niveles de profundidad, y la pareja invertida `\ude00\ud83d`. Una clave que es un emoji sigue dando `422` `unknown_field` con el emoji como `field` (`test_body_text.py:146-157`) |
| H-03 | CORREGIDO (sin cambio de código, como se decidió) | La regla está escrita en `README.md:135-144`. Mis sondas: `POST /simulations?debug=1` con `{"customer_id":0}` da solo `debug: unknown_field`; `GET /customers/abc?x=1`, solo `x: unknown_field`; `POST /pricing/quote?a=1&b=2&a=3` da `a` y `b` en el orden de llegada. Test: `test_customers_read.py:149-154` |
| H-04 | CONFORME A LO DECIDIDO | Con 4300 dígitos, `422` `out_of_range`; con 4301 y 5000, `400` `malformed_request`. Pasa igual en `/pricing/quote`, `/simulations` y `/customers`, así que no ha empeorado. Test: `test_body_text.py:160-182`, con el comentario de que se escribió después del código. Ver N-03 |
| H-05 | CORREGIDO | `q` igual a `%00`, `a%00`, `%00a`, U+0000 entre espacios, `ab` + U+0000 + `cd`, o 100 caracteres U+0000: siempre `200` con la lista vacía. Con 101 caracteres U+0000, `422` `too_long`. La decisión la toma el dominio (`backend/app/domain/customers.py:120-127`). Filas en SPEC-01 5.9:697-699. Tests: `test_customers_read.py:44-47` y `tests/unit/test_customers.py:144-147`. Con el defecto original, la fila `a%00` habría devuelto los clientes 2 y 3, cuyo nombre acaba en `a`, y `%00a` el listado entero, así que el test fallaría |
| H-06 | CONFORME A LO DECIDIDO | `q=<101 x>&q=a` da `200` con los clientes 2, 3, 7, 4 y 1; al revés, `422` `too_long`. Con `q=%00&q=alfa` da `200` con 2 y 3. Es lo mismo que se describió: solo cuenta el último `q`. Ver N-03 |
| H-07 | CORREGIDO | UTF-16 (con BOM, LE y BE), UTF-32 (con BOM, LE y BE), UTF-8 con BOM y Latin-1 con caracteres fuera de ASCII dan `400`. UTF-8 con espacios en blanco delante sigue dando `201`. Con un `charset=utf-16` declarado y el cuerpo en UTF-8 también da `201`, porque el cuerpo se lee como UTF-8 sin mirar el `charset`; es lo que dice la regla. Código: `request_guard.py:54-60`. Regla en `README.md:156,172-176`. Tests: `test_body_text.py:104-125`, en los tres `POST` |
| H-08 | CORREGIDO | `invalid_email` con U+00A0 en medio, delante o detrás, y con U+3000, U+2028, U+2029, U+2009, U+202F, U+1680 y U+205F. U+200B y U+0085 dan `invalid_characters`, porque son Cf y Cc y esa comprobación va antes. Un email con espacios U+0020 alrededor da `201` y se guarda recortado. Código: `domain/customers.py:33,192-201`. Regla en SPEC-01 2.1:33 y 2.12:238-243. Filas en 5.7:637-641. Tests: `tests/customer_cases.py:31-38,79` |
| H-09 | CORREGIDO, con N-01 | `/redoc`, `/docs/oauth2-redirect` y las dos con `?x=1` dan `404` `not_found`. `/docs`, `/docs?x=1`, `/openapi.json` y `/openapi.json?x=1` dan `200`. Código: `backend/app/main.py:223-226`. Regla en `README.md:207-216`. Tests: `backend/tests/integration/test_generated_docs.py`. Pero cualquier método distinto de `GET` sobre `/docs` o `/openapi.json` da `500` (N-01) |
| H-10 | CORREGIDO | La comprobación previa admitida devuelve `access-control-allow-headers: Accept, Accept-Language, Content-Language, Content-Type`. Así lo dice SPEC-03 2.7:176-179 y la fila de 5.6:482. Los tests fijan el valor exacto con `==`: `backend/tests/integration/test_cors.py:23,89` y `test_real_endpoints.py:199` |
| H-11 | CORREGIDO | La sentencia `SEARCH_CUSTOMERS` (`backend/app/repositories/customers.py:21-27`) ya no lleva `? <> ''`; la decisión está en `domain/customers.py:126-127`. El test `test_customers_search_sql.py:89-98` pasa a mano un identificador vacío y espera que coincida; con la condición en el SQL fallaría |
| H-12 | CORREGIDO, con N-02 | `repositories/simulations.py` usa los tipos `SimulationColumns` y `HistoryRow` y no aparece `Any`. `CLAUDE.md:120-125` dice que el oráculo no comprueba el `Any` sin comentario. Quedan otros `Any` sin comentario en esa misma línea (N-02) |
| H-13 | Sin veredicto (no demostrable) | Hay comentarios «Written after the code…» o «Never seen failing…» en 23 puntos de 10 ficheros de test (`grep -rn -i "written after\|never seen failing\|passed before" backend/tests`). Sin la historia de git no puedo saber qué tests se escribieron después del código, así que no puedo confirmar que estén todos |
| H-14 | CORREGIDO | `test_customers_search_sql.py:126-160`: la conexión que registra las sentencias cubre el `INSERT` de un cliente con valores hostiles, `find` y `country_of`, y comprueba que el SQL no contiene ningún valor y que los valores van en los parámetros |
| H-15 | CONFORME A LO DECIDIDO | No había nada que comprobar |

**Notas sobre algunos hallazgos**

- **H-02 y A-01, más casos**:
  - Un cuerpo con surrogate y un `Content-Type` `text/plain` da `415`: se respeta la precedencia.
  - Con surrogate y un parámetro de consulta desconocido da `400`.
  - Con surrogate en una ruta que no existe da `400`, porque el guarda va antes del enrutado.
  - Un `GET` con un cuerpo así da `400`.
  - Los bytes crudos `ED A0 80` (un surrogate codificado en UTF-8, que no es UTF-8 válido) y un UTF-8 sobrelargo (`C0 AF`) dan `400`.
- **H-05, más casos**: `q=%ED%A0%80` y `q=%FF` dan `200` con la lista vacía; no hay `500`.

## 3. Los cinco requisitos que eran `NO CUMPLE`

| Requisito | Veredicto | Evidencia |
|---|---|---|
| SPEC-01/E-24 | CUMPLE | Todas las filas de 5.10, incluidas las de 4301 y 20000 nueves y la del signo menos, dan lo que dice la tabla (sondas y `test_customers_read.py:108-146`) |
| SPEC-01/E-25 | CUMPLE | Las 22 filas de 5.9 que probé dan los `id` y el orden de la tabla, incluidas las tres de U+0000. Un `q` que solo tiene una marca diacrítica (U+0301) devuelve todos los clientes: su forma de búsqueda queda vacía y la cadena vacía está dentro de cualquier nombre. Encaja con la letra de 2.10, así que no lo cuento como defecto, pero ninguna fila de la spec lo fija |
| SPEC-01/E-30 | NO CUMPLE (limitación aceptada L-04) | `GET /customers?q=<101 x>&q=a` da `200`, cuando E-30 pide `422` si `q` supera los 100 caracteres. El incumplimiento es el que el Tech Lead aceptó, pero el contrato no lo recoge (N-03) |
| SPEC-02/E-14 | NO CUMPLE (limitación aceptada L-05) | La parte de H-03 ya cumple, porque la regla del parámetro desconocido está escrita en el índice. La de H-04 sigue igual: `{"customer_id":1,"active_users":` seguido de 4301 nueves `}` es JSON válido y está fuera del rango de E-09, y responde `400` y no `422`. La tabla del índice reserva el `400` para lo que no es JSON válido |
| SPEC-03/E-07 | NO CUMPLE (limitación aceptada L-05) | Lo mismo en `POST /simulations` con un `customer_id` de 4301 dígitos: `400` en lugar de `422` |

## 4. Regresiones y hallazgos nuevos

### N-01 · Gravedad media · Un método no admitido sobre `/docs` o `/openapi.json` responde `500` y no `405`

- **Qué pasa**: `POST /docs`, `PUT /docs`, `OPTIONS /docs` (sin ser comprobación previa), `POST /openapi.json` y `DELETE /openapi.json` responden `500` `internal_error` y escriben una traza en el log. Los demás endpoints responden `405` con su `Allow`; por ejemplo `POST /health` da `405` con `Allow: GET`.
- **Evidencia reproducible**: con la sonda de TestClient descrita en la cabecera, `c.request("POST", "/docs")` da `500`, y el log muestra `KeyError: 'route'` en `backend/app/api/contract.py:29`, llamado desde `handle_http_error` en `backend/app/api/error_handling.py:83`.
- **Causa**: `methods_of` lee `request.scope["route"]`. Las rutas de documentación que publica el framework no son `APIRoute` y no dejan esa clave en el `scope`.
- **Qué incumple**: SPEC-03/E-29 y la fila del `405` del índice («La ruta existe pero no admite ese método»). Para `OPTIONS`, también SPEC-03/E-33. Ahora el índice (`README.md:207-210`) dice de forma expresa que esas dos rutas existen.
- **¿Regresión?** No he podido determinarlo sin leer la historia. Lo más probable es que ya ocurriera en `bda2c65`, porque `/docs` ya existía entonces. Lo hace exigible la corrección de H-09, y `test_generated_docs.py` no lo cubre.

### N-02 · Gravedad baja · Quedan usos de `Any` sin comentario en esa misma línea

- **Qué pasa**: `CLAUDE.md:120-121` admite `Any` solo «con un comentario que justifique esa línea concreta». Hay líneas que no lo tienen:
  - `backend/app/api/validation.py:61-63` (`_failed_fields`) y `backend/app/api/validation.py:75` (`_field_error`). El comentario de `validation.py:37` habla solo de los parámetros de `field_errors`.
  - `backend/app/api/contract.py:28` (`methods_of`). El comentario de `contract.py:16` está encima de `operation_of`, y el de `contract.py:42` remite a ese.
- **Evidencia**: `grep -rn "Any\b" backend/app --include=*.py`.
- **¿Regresión?** No es una regresión. Es la misma clase de defecto que H-12; aquella corrección se limitó a `simulations.py`. El oráculo no lo detecta, como reconoce ahora `CLAUDE.md`.

### N-03 · Gravedad baja · Las limitaciones aceptadas y los casos nuevos del `400` no están en el contrato

1. **L-04 y L-05 no aparecen en ninguna spec ni en el análisis o la arquitectura.** Busqué `L-0`, `limitación` y `limitaci` en todo el repo salvo `03-proceso` y `04-calidad`. `L-05` solo aparece en el docstring de `backend/tests/integration/test_body_text.py:171`; `L-04`, en ningún sitio. El índice sigue diciendo que el `400` es para lo que «no es JSON válido en UTF-8», pero un entero de 4301 dígitos es JSON válido y responde `400`. E-30 sigue pidiendo `422` para cualquier `q` de más de 100 caracteres. Quien lea solo las specs no sabe nada de estas desviaciones. Puede que estén registradas en `04-calidad`, que no he leído.
2. **Los casos nuevos no están en la tabla de SPEC-03.** El índice (`README.md:186-189`) dice que los casos de prueba de los errores genéricos están en SPEC-03, «Operación del backend». La tabla de 5.7 de SPEC-03 (líneas 493-498) no tiene filas para el surrogate suelto, UTF-16 o UTF-32, el BOM, `/redoc` ni `/docs?x=1`. Hay tests de esos casos (`test_body_text.py`, `test_generated_docs.py`), pero CA-17 («cada fila de 5.7») no los alcanza.

- **¿Regresión?** No. Es una incoherencia documental de las correcciones.
- **Qué afecta**: la coherencia entre specs y código en SPEC-01/E-30, SPEC-02/E-14, SPEC-03/E-07 y SPEC-03/CA-17.

### Lo que probé sin encontrar regresiones

- **Alta**: UTF-8 con caracteres fuera de ASCII, emojis como pareja de escapes y crudos, escapes válidos (`A`, `é`), un BOM dentro de un valor (da `invalid_characters`, porque U+FEFF es Cf), `null`, `{}`, `NaN`, claves duplicadas y anidamiento muy profundo (`400`).
- **Buscador**: todas las filas de 5.9.
- **Alta, más casos**: todas las filas de separadores de 5.7 y un email con espacios U+0020 alrededor.
- **`id` de la ruta**: las filas de 5.10.
- **CORS**: comprobación previa admitida, origen rechazado, cabecera rechazada, y la cabecera de origen en un `422`, en un `400` y en `/docs`.
- **Métodos**: `OPTIONS` que no es comprobación previa sobre `/customers` da `405`.
- **Historial y cálculo**: el historial de un cliente con tres simulaciones (orden y recuento) y `POST /pricing/quote`.
- **OpenAPI**: las rutas que publica son exactamente las seis de negocio.

## 5. Lo que no he podido comprobar

- **H-13, exhaustividad**: saber qué tests se escribieron después del código exige leer la historia o la bitácora, y el encargo excluye las dos cosas.
- **N-01, ¿regresión o preexistente?**: no he ejecutado el código de `bda2c65`.
- **Registro de L-01, L-04 y L-05**: si existe, está en `ai-workspace/04-calidad/`, que no he leído.
- **Si los tests nuevos fallan con el defecto original**: lo he razonado sobre los datos de cada test (H-05, H-11 y H-10 fallarían; H-01, H-02 y H-07 también, por el estado que esperan), pero no he ejecutado ninguna mutación, porque supondría modificar el código.
- **`/docs` en un navegador**: la página carga recursos de un servidor externo y no la he abierto. Solo he comprobado el HTML y el código de estado.
