# Evaluación independiente del bloque backend (SPEC-01, SPEC-02, SPEC-03)

| | |
|---|---|
| **Fecha y hora** | vie 13 nov 2026, de 15:42 a 15:48 (hora local, salida de `date`) |
| **Agente** | Subagente evaluador independiente (Claude Agent SDK), con contexto limpio y en solo lectura |
| **Modelo** | Opus 5.5 (`claude-opus-5-5`), según mi configuración. No sé nada más de mí que pueda comprobar |
| **Leído** | `ai-workspace/01-specs/README.md`, SPEC-01, SPEC-02 y SPEC-03 completas; `.claude/rules/backend.md`; `CLAUDE.md`; ADR-005, ADR-006 y ADR-009 (búsquedas puntuales); todo `backend/app/`, todo `backend/tests/` y `backend/pyproject.toml` |
| **No leído** | `ai-workspace/03-proceso/` y `ai-workspace/04-calidad/` (por regla); SPEC-04, que queda fuera; `ai-workspace/00-analisis/`, porque las specs bastaban como referencia; la historia de git (ni `log`, ni `show`, ni `diff`) |
| **Herramientas** | `uv` 0.12.13 · Python 3.12.0 · FastAPI 0.162.0 · Starlette 1.10.0 · Pydantic 2.14.3 · SQLite 3.42.0 |
| **Estado del repo al terminar** | `git status --short` no muestra nada y `HEAD` es `bda2c65`, igual que al empezar |

## 1. Resumen

- **Oráculo** (`uv run scripts/check.py`, desde la raíz): sale con código 0 y `ORÁCULO EN VERDE (solo lo activo: lo inactivo no está comprobado) · 20 correctas, 0 con fallo, 4 inactivas`. Las cuatro inactivas son del frontend, porque no existe `frontend/package.json`.
  - Pasan ruff, ruff format, `mypy --strict`, la cobertura (86 de 86 ramas, y el 100 % en `domain/`), la comprobación de que `domain/` no usa nada ajeno a la biblioteca estándar ni `float`, la dirección de las capas y los límites de tamaño.
- **Tests del backend** (`uv run pytest`, desde `backend/`): `639 passed in 22.04s`. No hay tests saltados, marcados como fallo esperado ni ejecutados en solitario.
- **Veredictos**: 130 en total, entre requisitos y criterios de las tres specs.
  - **125 CUMPLE.**
  - **5 NO CUMPLE**, todos en casos límite: SPEC-01/E-24, SPEC-01/E-25, SPEC-01/E-30, SPEC-02/E-14 y SPEC-03/E-07.
  - **0 NO DEMOSTRADO.**
- **Hallazgos**: 15 en total, ninguno de gravedad alta.
  - **Media (3):** H-01, H-02 y H-03. Todos son entradas del cliente que acaban en una respuesta que el contrato no prevé.
  - **Baja (12):** del H-04 al H-15.
- **En conjunto**: lo que fijan las tablas de las specs está implementado y probado. Los defectos aparecen fuera de esas tablas: números enteros muy grandes, surrogates sueltos, el carácter NUL, parámetros repetidos y la combinación de errores de la query y del cuerpo.

## 2. Tabla por requisito y criterio

Abreviaturas de rutas de tests:
- `ti` = `backend/tests/integration/`
- `tu` = `backend/tests/unit/`

### SPEC-01 · Requisitos

| Id | Veredicto | Evidencia |
|---|---|---|
| E-01 | CUMPLE | `ti/test_customers_create.py:75` (201, `Location`, cuerpo); `app/api/customers.py:97-117` |
| E-02 | CUMPLE | `app/domain/customers.py:160,172` (`strip(" ")`); filas de `tests/customer_cases.py:40,48`, ejecutadas en `ti/test_customers_create.py:111` |
| E-03 | CUMPLE | `tests/customer_cases.py:54-62`, ejecutadas en `ti/test_customers_create.py:121` (ver H-02 para los surrogates) |
| E-04 | CUMPLE | `tests/customer_cases.py:65,67-68`; `app/domain/customers.py:180-185` (ver H-08) |
| E-05 | CUMPLE | `tests/customer_cases.py:29,69`; `ti/test_customers_contract.py:83` |
| E-06 | CUMPLE | `tests/customer_cases.py:70` |
| E-07 | CUMPLE | `tests/customer_cases.py:71-74`; `ti/test_customers_create.py:137` (cuerpo ausente) |
| E-08 | CUMPLE | `tu/test_tax_id.py:80,87`; `ti/test_customers_create.py:75,89` |
| E-09 | CUMPLE | `tu/test_tax_id.py:108` (`1234567Z`, `ES…`) |
| E-10 | CUMPLE | `tu/test_tax_id.py:95,108,114` |
| E-11 | CUMPLE | `tu/test_tax_id.py:123` (CA-03) |
| E-12 | CUMPLE | `tu/test_tax_id.py:95,102` (`Y0000000T`) |
| E-13 | CUMPLE | `tu/test_tax_id.py:134,148`; `tu/test_tax_id_differential.py:96` |
| E-14 | CUMPLE | `tu/test_tax_id.py:156` |
| E-15 | CUMPLE | `tu/test_tax_id.py:108`; `tests/customer_cases.py:107-108`, en integración |
| E-16 | CUMPLE | `tu/test_tax_id.py:102`; `tests/customer_cases.py:106` |
| E-17 | CUMPLE | `ti/test_customers_create.py:147` (cuerpos idénticos byte a byte); mensajes fijos en `app/api/customer_errors.py:15-28` |
| E-18 | CUMPLE | `tests/customer_cases.py:76-93`; `app/domain/customers.py:198-209` |
| E-19 | CUMPLE | `ti/test_customers_create.py:156`; `ti/test_schema.py:289` |
| E-20 | CUMPLE | `ti/test_customers_create.py:170` |
| E-21 | CUMPLE | `ti/test_customers_create.py:180` |
| E-22 | CUMPLE | `ti/test_customers_read.py:82`; `ti/test_customers_history.py:178` |
| E-23 | CUMPLE | `ti/test_customers_read.py:96` (999 y 2^63−1) |
| E-24 | **NO CUMPLE** | Las 16 formas probadas en `ti/test_customers_read.py:104` pasan, pero un `id` de 4301 dígitos o más responde `500` (H-01) |
| E-25 | **NO CUMPLE** | Las filas de 5.9 (`ti/test_customers_read.py:29,135`) pasan, pero `q` igual a NUL (`%00`) devuelve todos los clientes (H-05) |
| E-26 | CUMPLE | `ti/test_customers_read.py:165` (25 clientes) |
| E-27 | CUMPLE | `ti/test_customers_search_sql.py:65` (busca `100%_\` con datos que lo contienen); `ti/test_customers_read.py:135` (`%` y `_`) |
| E-28 | CUMPLE | `ti/test_customers_search_sql.py:54` |
| E-29 | CUMPLE | `ti/test_customers_read.py:135,143` |
| E-30 | **NO CUMPLE** | Los casos de `ti/test_customers_read.py:178,186` pasan, pero con un `q` repetido se acepta un `q` de 101 caracteres (H-06) |
| E-31 | CUMPLE | Fila `noexiste` de `ti/test_customers_read.py:29` |
| E-32 | CUMPLE | `ti/test_customers_contract.py:70`; `app/api/meta.py:32-37` |
| E-33 | CUMPLE | `tu/test_customers.py:99`; `ti/test_customers_create.py:89` |
| E-34 | CUMPLE | `tests/customer_cases.py:46,63-64`; `ti/test_customers_contract.py:119` |
| E-35 | CUMPLE | `tests/customer_cases.py:94-131`; `tu/test_customers.py:68,80` |

### SPEC-01 · Criterios de aceptación

| Id | Veredicto | Evidencia |
|---|---|---|
| CA-01 | CUMPLE | `tu/test_tax_id.py:80` |
| CA-02 | CUMPLE | `tu/test_tax_id.py:95,102,108` |
| CA-03 | CUMPLE | `tu/test_tax_id.py:123` |
| CA-04 | CUMPLE | `tu/test_tax_id.py:134,148` |
| CA-05 | CUMPLE | `tu/test_tax_id.py:156` |
| CA-06 | CUMPLE | `ti/test_customers_create.py:75`; `ti/test_customers_read.py:82` |
| CA-07 | CUMPLE | `ti/test_customers_create.py:111,121` comprueban el estado, el `code`, el código por campo y el orden de `errors` |
| CA-08 | CUMPLE | `tests/customer_cases.py:106-107`, en integración |
| CA-09 | CUMPLE | `ti/test_customers_create.py:147` |
| CA-10 | CUMPLE | `ti/test_customers_create.py:121,156,170,180` |
| CA-11 | CUMPLE | `ti/test_schema.py:289` |
| CA-12 | CUMPLE | `ti/test_customers_read.py:82,96,104` (todas las filas de 5.10) |
| CA-13 | CUMPLE | `ti/test_customers_read.py:135,143,165,178,186` |
| CA-14 | CUMPLE | `ti/test_customers_search_sql.py:54` |
| CA-15 | CUMPLE | `ti/test_customers_contract.py:70,83` |
| CA-16 | CUMPLE | `ti/test_customers_contract.py:98,119,143`; `ti/test_customers_read.py:204` |
| CA-17 | CUMPLE | Oráculo: «domain/ solo importa la biblioteca estándar…» y «100 % de sentencias y ramas en domain/» |
| CA-18 | CUMPLE | `tu/test_customers.py:99`; `ti/test_customers_create.py:89` |
| CA-19 | CUMPLE | `tu/test_tax_id_differential.py:96,107` (semilla `20261112`, 340 CIF y 60 000 identificadores) |

### SPEC-02 · Requisitos

| Id | Veredicto | Evidencia |
|---|---|---|
| E-01 | CUMPLE | `tu/test_pricing.py:54,86` |
| E-02 | CUMPLE | `tu/test_pricing.py:54` (fila 0) |
| E-03 | CUMPLE | `tu/test_pricing.py:93,105`; `app/domain/pricing.py:68-70` |
| E-04 | CUMPLE | `tu/test_pricing.py:54` |
| E-05 | CUMPLE | Comprobación AST del oráculo; `tu/test_pricing.py:113` |
| E-06 | CUMPLE | `tu/test_pricing.py:69` |
| E-07 | CUMPLE | `ti/test_pricing_quote.py:117,168` |
| E-08 | CUMPLE | `ti/test_simulations_create.py:128,143` |
| E-09 | CUMPLE | `ti/test_pricing_quote.py:154`; `tu/test_pricing.py:134` |
| E-10 | CUMPLE | `ti/test_pricing_quote.py:255` |
| E-11 | CUMPLE | `ti/test_pricing_quote.py:107` |
| E-12 | CUMPLE | `ti/test_pricing_quote.py:141` |
| E-13 | CUMPLE | `ti/test_pricing_quote.py:175` |
| E-14 | **NO CUMPLE** | Las filas de 5.4 y 5.5 pasan. Fallan dos casos límite: un entero JSON de 4301 dígitos responde `400` (H-04), y con un parámetro desconocido en la query se omiten los errores del cuerpo (H-03) |
| E-15 | CUMPLE | `ti/test_pricing_quote.py:184,203` (con la base de datos apartada responde `422`) |

### SPEC-02 · Criterios de aceptación

| Id | Veredicto | Evidencia |
|---|---|---|
| CA-01 | CUMPLE | `tu/test_pricing.py:54` |
| CA-02 | CUMPLE | `tu/test_pricing.py:93,105` |
| CA-03 | CUMPLE | `tu/test_pricing.py:86` |
| CA-04 | CUMPLE | `tu/test_pricing.py:134,141` |
| CA-05 | CUMPLE | `ti/test_pricing_quote.py:107` |
| CA-06 | CUMPLE | `ti/test_pricing_quote.py:141` |
| CA-07 | CUMPLE | `ti/test_pricing_quote.py:154,168,175,184,198` |
| CA-08 | CUMPLE | Lo cubre SPEC-03/CA-03: `ti/test_simulations_create.py:128` |
| CA-09 | CUMPLE | Oráculo en verde en las tres comprobaciones de `domain/` |
| CA-10 | CUMPLE | `ti/test_pricing_quote.py:244,267` (límites publicados como decimales, limitación aceptada en la spec) |
| CA-11 | CUMPLE | `ti/test_pricing_quote.py:255` |

### SPEC-03 · Requisitos

| Id | Veredicto | Evidencia |
|---|---|---|
| E-01 | CUMPLE | `ti/test_simulations_create.py:95,111` |
| E-02 | CUMPLE | `ti/test_simulations_create.py:128,143`; `app/services/simulations.py:32` |
| E-03 | CUMPLE | `ti/test_simulations_create.py:111` (compara también las filas guardadas) |
| E-04 | CUMPLE | Filas de 0 y de máximos en `tests/simulation_cases.py:173-181` |
| E-05 | CUMPLE | `tests/simulation_cases.py:192-203`, ejecutadas en `ti/test_simulations_create.py:158` |
| E-06 | CUMPLE | `tests/simulation_cases.py:204-207` |
| E-07 | **NO CUMPLE** | Las filas de 5.2 pasan; fallan los mismos casos límite que SPEC-02/E-14 (H-03 y H-04) |
| E-08 | CUMPLE | `ti/test_simulations_create.py:183` |
| E-09 | CUMPLE | `tests/simulation_cases.py:213` |
| E-10 | CUMPLE | `ti/test_simulations_create.py:194` |
| E-11 | CUMPLE | `ti/test_simulations_repository.py:50`; `ti/test_simulations_create.py:207` |
| E-12 | CUMPLE | `ti/test_customers_history.py:104,118,135` |
| E-13 | CUMPLE | `ti/test_customers_history.py:104` (fecha atrasada y fechas empatadas) |
| E-14 | CUMPLE | `ti/test_customers_history.py:145` |
| E-15 | CUMPLE | `ti/test_customers_history.py:128,178` |
| E-16 | CUMPLE | `ti/test_customers_history.py:158` (los seis pasos de 5.4) |
| E-17 | CUMPLE | `ti/test_customers_history.py:118,145` |
| E-18 | CUMPLE | `ti/test_real_endpoints.py:218`; `ti/test_main.py:10` |
| E-19 | CUMPLE | `ti/test_schema.py:143,224` |
| E-20 | CUMPLE | `ti/test_schema.py:182,204,279` |
| E-21 | CUMPLE | `ti/test_schema.py:182,204,224,261,269` |
| E-22 | CUMPLE | `ti/test_schema.py:97,112,122` |
| E-32 | CUMPLE | `ti/test_schema.py:134` |
| E-23 | CUMPLE | Todas las sentencias de `app/repositories/` usan `?`; tests en `ti/test_simulations_repository.py:67`, `ti/test_customers_history.py:211` y `ti/test_customers_search_sql.py:54` (ver H-14) |
| E-24 | CUMPLE | `ti/test_real_endpoints.py:142,160`; `ti/test_cors.py:103,114` |
| E-25 | CUMPLE | `ti/test_real_endpoints.py:160` |
| E-26 | CUMPLE | `ti/test_real_endpoints.py:160`; `ti/test_cors.py:49,63` |
| E-27 | CUMPLE | `ti/test_health.py:20` |
| E-28 | CUMPLE | `ti/test_health.py:31,49` |
| E-29 | CUMPLE | `ti/test_real_endpoints.py:50-65,110`; filas de `503` en cinco endpoints (`ti/test_customers_create.py:188`, `ti/test_customers_read.py:192`, `ti/test_pricing_quote.py:211`, `ti/test_simulations_create.py:228`) |
| E-30 | CUMPLE | `ti/test_real_endpoints.py:182` |
| E-31 | CUMPLE | `ti/test_real_endpoints.py:195-216` (estado y conjunto completo de cabeceras) |
| E-33 | CUMPLE | Filas `OPTIONS` de `ti/test_real_endpoints.py:63-64` |

### SPEC-03 · Criterios de aceptación

| Id | Veredicto | Evidencia |
|---|---|---|
| CA-01 | CUMPLE | `ti/test_simulations_create.py:95` |
| CA-02 | CUMPLE | `ti/test_simulations_create.py:111` |
| CA-03 | CUMPLE | `ti/test_simulations_create.py:128` |
| CA-04 | CUMPLE | `ti/test_simulations_create.py:158` (comprueba también que no se guarda nada) |
| CA-05 | CUMPLE | `ti/test_simulations_create.py:194` |
| CA-06 | CUMPLE | `ti/test_simulations_repository.py:50` |
| CA-07 | CUMPLE | `ti/test_customers_history.py:104,118,128,145` |
| CA-08 | CUMPLE | `ti/test_customers_history.py:158` |
| CA-09 | CUMPLE | `ti/test_real_endpoints.py:218` |
| CA-10 | CUMPLE | `ti/test_schema.py:143` |
| CA-11 | CUMPLE | `ti/test_schema.py:182-286` (las 13 filas de 5.5) |
| CA-12 | CUMPLE | `ti/test_schema.py:112,122,134` |
| CA-13 | CUMPLE | `ti/test_simulations_repository.py:67` (cobertura parcial: H-14) |
| CA-14 | CUMPLE | `ti/test_simulations_create.py:243`; `ti/test_customers_history.py:188`; `ti/test_health.py:69,81` |
| CA-15 | CUMPLE | `ti/test_real_endpoints.py:142,160,182,195` |
| CA-16 | CUMPLE | `ti/test_health.py:20,49` |
| CA-17 | CUMPLE | `ti/test_real_endpoints.py:50-65,110,124,132,142` |

## 3. Hallazgos

Los resultados citados como «sonda» salen de scripts de Python ejecutados con `uv run python`, desde `backend/` y con `PYTHONPATH=.`. Cada script crea `TestClient(create_app(), raise_server_exceptions=False)` y lo usa con `with`. `DATABASE_PATH` apunta a un fichero del directorio temporal del sistema. Los scripts están fuera del repositorio.

**H-01 · media · Un `id` de ruta con 4301 dígitos o más responde `500` en vez de `422 out_of_range`**
- **Evidencia (sonda):**
  - `GET /customers/` seguido de 4300 nueves responde `422`, con `id: out_of_range`.
  - `GET /customers/` seguido de 4301 nueves responde `500 internal_error`.
  - El log registra `UntranslatedValidationError: id: int_parsing_size`.
- **Causa:** Pydantic emite `int_parsing_size` y ese tipo no está en `TRANSLATIONS` (`app/api/validation.py:17-26`), así que `app/api/validation.py:74-75` lanza la excepción.
- **Por qué es un defecto:** según la convención, un `500` en una validación es «un fallo nuestro». Además, un cliente cualquiera puede llenar el log de errores.
- **Afecta a:** SPEC-01/E-24 y a las convenciones («Identificadores», «Errores de validación»).

**H-02 · media · Un surrogate suelto (`\ud800`) en `company_name` o `contact_email` responde `500 internal_error`**
- **Evidencia (sonda):** `POST /customers` con el cuerpo `{"company_name":"Ab\ud800c",…}` (escape JSON válido) responde `500`. El log registra `UnicodeEncodeError: 'utf-8' codec can't encode character '\ud800'… surrogates not allowed`. Con `contact_email` pasa lo mismo.
- **Causa:**
  - El dominio solo rechaza las categorías Cc y Cf (`app/domain/customers.py:212-213`), y U+D800 es de la categoría Cs.
  - El repositorio solo trata `IntegrityError` (`app/repositories/customers.py:61-68`).
  - La excepción llega a `UnexpectedErrorGuard`.
- **Afecta a:** las convenciones («la validación va antes»; un error de la petición nunca es un `500`) y a SPEC-01/E-01.
- **Decisión pendiente:** la spec no dice qué hacer con un surrogate. Le toca decidir al Tech Lead.

**H-03 · media · Un parámetro de consulta desconocido oculta los errores del cuerpo y del `id` de la ruta**
- **Evidencia (sonda):**
  - `POST /simulations?debug=1` con `{"customer_id":0}` devuelve solo `[debug: unknown_field]`. Faltan `customer_id: out_of_range` y los tres `missing`.
  - `GET /customers/abc?x=1` devuelve solo `[x: unknown_field]`.
- **El test lo da por bueno:** `tests/integration/test_pricing_quote.py:236-241` (`…reported_alone_when_the_body_is_also_invalid`).
- **Qué dice la spec:**
  - Las convenciones fijan cómo se ordenan los parámetros desconocidos dentro de `errors`, lo que supone que conviven con los del cuerpo.
  - SPEC-02/E-14 y SPEC-03/E-07 piden «el detalle de cada campo».
  - Ninguna spec ni ADR (busqué en ADR-006 y ADR-009) dice que el error de la query excluya a los demás.
- **Por qué es un defecto:** es una regla del contrato que solo está en el código y en el test.
- **Afecta a:** SPEC-02/E-14, SPEC-03/E-07 y `CLAUDE.md`, flujo 1 («no se inventa la regla»).

**H-04 · baja · Un JSON válido con un entero de más de 4300 dígitos responde `400 malformed_request`**
- **Evidencia (sonda):**
  - `POST /pricing/quote` con `active_users` de 4300 dígitos responde `422`, con `active_users: out_of_range`.
  - Con 4301 dígitos responde `400 malformed_request`.
- **Causa:** `json.loads` lanza `ValueError` por el límite de dígitos de `int`, y `app/api/request_guard.py:39-44` lo trata como JSON no válido.
- **Por qué es un defecto:** RFC 8259 admite enteros de cualquier tamaño, y la convención reserva el `400` para un cuerpo que no es JSON.
- **Afecta a:** las convenciones (tabla de errores genéricos), SPEC-02/E-14 y SPEC-03/E-07.

**H-05 · baja · `q` con el carácter NUL devuelve los 20 primeros clientes**
- **Evidencia (sonda):** con tres clientes, `GET /customers?q=%00` devuelve los tres, aunque ningún nombre ni identificador contiene U+0000.
- **Causa:** SQLite corta el patrón de `LIKE` en el NUL, así que `%\x00%` queda en `%` (`app/repositories/customers.py:20-26,90`).
- **Afecta a:** SPEC-01/E-25.
- **Impacto:** no expone datos que no estén ya en el listado inicial, pero el resultado no es el que dice la spec.

**H-06 · baja · Con un `q` repetido solo se valida el último**
- **Evidencia (sonda):**
  - `GET /customers?q=<101 'x'>&q=a` responde `200` con resultados.
  - En orden inverso responde `422`, con `q: too_long`.
- **Causa:** `app/api/request_guard.py:85` deduplica los nombres con `dict.fromkeys`, y FastAPI se queda con el último valor (`app/api/customers.py:147`).
- **Afecta a:** SPEC-01/E-30. La spec no regula los parámetros repetidos, así que es un caso que nadie ha decidido.

**H-07 · baja · Se aceptan cuerpos en UTF-16 o con BOM**
- **Evidencia (sonda):** `POST /pricing/quote` con el cuerpo codificado en UTF-16, o en UTF-8 con BOM, responde `200`.
- **Causa:** `json.loads(bytes)` detecta la codificación por su cuenta (`app/api/request_guard.py:41`).
- **Por qué es un defecto:** RFC 8259 §8.1 exige UTF-8. El propio caso `not-utf8` de `tests/integration/test_generic_errors.py:87` muestra que la intención es rechazar lo que no sea UTF-8.
- **Afecta a:** las convenciones (`400 malformed_request`).

**H-08 · baja · El email admite espacios distintos de U+0020**
- **Evidencia (sonda):** `contact_email` = `a b@c.example` (con un espacio de no separación) responde `201` y se guarda tal cual.
- **Causa:** `app/domain/customers.py:185` solo busca U+0020.
- **Qué dice la spec:** SPEC-01 2.1 dice «sin espacios» pero no define qué es un espacio. 2.12 define «recortar» con U+0020, no esta regla.
- **Afecta a:** SPEC-01/E-04. Es una ambigüedad de la spec.

**H-09 · baja · Hay endpoints que ninguna spec define**
- **Evidencia (sonda):**
  - `GET /docs`, `GET /redoc` y `GET /docs/oauth2-redirect` responden `200` con HTML. `/docs` carga recursos de un CDN externo.
  - En esas rutas no se aplica la regla del parámetro desconocido: `GET /openapi.json?x=1` y `GET /docs?x=1` responden `200`.
- **Causa:** `app/main.py:61-67` no desactiva `docs_url` ni `redoc_url`.
- **Afecta a:** el ámbito de SPEC-01 y SPEC-03 (funcionalidad no pedida) y a las convenciones, que aplican el parámetro desconocido a todos los endpoints.

**H-10 · baja · CORS anuncia más cabeceras admitidas que la spec**
- **Evidencia (sonda):** la comprobación previa admitida de `OPTIONS /simulations` devuelve `access-control-allow-headers: Accept, Accept-Language, Content-Language, Content-Type`.
- **Qué dice la spec:** SPEC-03 2.7 dice «la cabecera admitida, content-type».
- **Causa:** es el comportamiento estándar de Starlette, que añade las cabeceras CORS-safelisted. El test de la comprobación admitida (`tests/integration/test_real_endpoints.py:191`) solo comprueba que `content-type` esté.
- **Afecta a:** SPEC-03 2.7 y E-30. Es una diferencia de texto sin riesgo práctico.

**H-11 · baja · Parte de la regla de coincidencia del buscador está en SQL**
- **Evidencia:** la condición «solo se compara el identificador si `q` normalizado no queda vacío» está escrita como `? <> ''` en `app/repositories/customers.py:24`.
- **Qué dice la spec:** SPEC-01 2.11 y SPEC-03 2.6 dicen que «las reglas de negocio no viven en SQL».
- **Afecta a:** esas dos reglas de arquitectura. Es discutible: la condición también puede verse como un detalle de cómo se construye la consulta.

**H-12 · baja · `Any` sin un comentario que lo justifique**
- **Evidencia:** `app/repositories/simulations.py:5,37` (`rows: list[tuple[Any, ...]]`). En `app/api/contract.py`, `problems.py` y `validation.py` cada `Any` lleva su comentario.
- **Afecta a:** `CLAUDE.md`, «Estilo común» (`any` solo con un comentario que justifique esa línea).

**H-13 · baja · Un test declara en un comentario que no siguió el ciclo TDD**
- **Evidencia:** `tests/unit/test_customers.py:105` dice: `# Written after the code that it tests (session 04, r4): it was never seen failing.`
- **Afecta a:** `CLAUDE.md`, flujo 2 (el rojo se ve antes de escribir el código). No he comprobado el resto del historial.

**H-14 · baja · La prueba con conexión que registra (SPEC-03/CA-13) no cubre todas las sentencias**
- **Qué cubre:** el alta de una simulación, el historial y la búsqueda.
- **Qué no cubre:** el `INSERT` de un cliente, `find` ni `country_of`.
- **Por qué cumple igualmente:** por lectura del código, todas usan `?`, y está activa la regla `S` de ruff.
- **Afecta a:** SPEC-03/E-23 y CA-13. Lo de esas tres sentencias está comprobado leyendo el código, no con un test.

**H-15 · baja · No hay límite de tamaño del cuerpo**
- **Evidencia:** `app/api/request_guard.py:65` lee el cuerpo entero en memoria antes de validarlo. Un `company_name` de 2 000 000 de caracteres se procesa entero hasta responder `422 too_long` (sonda).
- **Afecta a:** la seguridad (posible denegación de servicio). Ninguna spec fija un máximo, así que le toca decidir al Tech Lead.

## 4. Lo que no he podido comprobar

- **Que el desarrollo siguiera el ciclo TDD** (rojo visto antes del código). No he leído la historia de git ni la bitácora, por las restricciones del encargo; solo cuento lo que deja ver H-13.
- **Que las comprobaciones de capas y de `float` del oráculo detecten bien los incumplimientos.** Solo he visto su resultado (OK); no he leído `scripts/check.py` ni he provocado un incumplimiento para ver si falla, porque eso exigía modificar ficheros. La dirección de las capas la he revisado leyendo los `import` y no he encontrado ninguna violación.
- **El comportamiento con un servidor real (uvicorn)**, con concurrencia, bloqueos de SQLite (`database is locked`) o cuerpos enviados por trozos. Todas las pruebas han sido con `TestClient`.
- **Que la tabla de control del CIF y los grupos de letras sean correctos según una fuente oficial.** La spec reconoce que no hay ninguna; solo he verificado la coherencia con `python-stdnum`, a través del test diferencial que pasa.
- **El comportamiento con SQLite anterior a 3.37.0** (sin `STRICT`). El entorno tiene la 3.42.0.
