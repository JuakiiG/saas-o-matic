# Evaluación independiente de SPEC-04 (borrador) frente al contrato real del backend

**Evaluador**: Claude Opus 5.5 (`claude-opus-5-5`). Solo he leído y sondeado; no he modificado nada del repositorio. Las bases de datos de los sondeos se crearon en el directorio temporal del sistema y se borraron después. `backend/data/` no existe, comprobado con `ls`.

## 1. Resumen

- **Oráculo** (`uv run scripts/check.py`, desde la raíz): `ORÁCULO EN VERDE (solo lo activo: lo inactivo no está comprobado) · 20 correctas, 0 con fallo, 4 inactivas`. Las cuatro inactivas son las del frontend, porque «no existe frontend/package.json».
- **`/openapi.json`**: lo obtuve con `TestClient(create_app())` dentro de `with`, desde `backend/`, con `uv run --locked python -c …` y `DATABASE_PATH` en el temporal. Estados que declara:
  - `GET /meta`: 200
  - `POST /customers`: 201, 409, 422, 503
  - `GET /customers`: 200, **422**, 503
  - `GET /customers/{id}`: 200, 404, 422, 503
  - `POST /pricing/quote`: 200, 404, 422, 500, 503
  - `POST /simulations`: 201, 404, 422, 500, 503
- **Sondeos con el mismo cliente**: alta y sus `422`, `409`, `id` de la ruta, buscador, proyección, guardado, `503` con la base de datos inaccesible, CORS y comprobación previa, `405`, `404` `not_found`, `415` y *surrogate* en el cuerpo.
- **Comprobaciones con Node 24, sin instalar nada**, leyendo los paquetes 21.2.26 de `@angular/common` y `@angular/forms`, la plantilla del CLI 21.2.29 (`@schematics/angular`) y TypeScript 5.9.3 de la caché local de npm.
- **Recuento**:
  - Requisitos E-01 a E-52: 41 `CONFORME`, 0 `NO CONFORME`, 5 `AMBIGUO`, 5 `SIN CASO DE PRUEBA`, 1 `NO COMPROBABLE`.
  - Criterios CA-01 a CA-18: 13 `CONFORME`, 2 `AMBIGUO`, 3 `SIN CASO DE PRUEBA`.
  - Hallazgos: ninguno de severidad alta, 2 medios y 10 bajos.

## 2. Tabla por requisito y por criterio

Todas las rutas de «SPEC-04:n» se refieren a `ai-workspace/01-specs/SPEC-04-frontend-y-divisas.md`.

| Id | Veredicto | Evidencia |
|---|---|---|
| E-01 | CONFORME | `GET /customers` sin `q` devuelve 200 con `items`; fila 1 de 5.3 |
| E-02 | CONFORME | Filas de 5.3 de `eje` y `ejem` (SPEC-04:613-614) |
| E-03 | SIN CASO DE PRUEBA | Ninguna fila de 5.3 comprueba el orden de varios resultados; CA-04 lo cita (H-04) |
| E-04 | CONFORME | El backend responde 200 `{"items":[]}` (sondeo `q=a+b`); fila de 5.3 |
| E-05 | SIN CASO DE PRUEBA | Ninguna fila de 5.4 comprueba que los desplegables sean los de `/meta`; CA-05 lo cita (H-04) |
| E-06 | CONFORME | CA-12, revisión del evaluador |
| E-07 | CONFORME | Fila «Doble clic» de 5.4 |
| E-08 | CONFORME | El `201` trae `id` en el cuerpo (sondeo: `{"id":1,…}`) |
| E-09 | CONFORME | Los `422` llevan `errors` con `field`, `code` y `message` (sondeos «121 ñ» y «tab AB») |
| E-10 | CONFORME | `409` `customer_already_exists` (sondeo «alta dup») |
| E-11 | CONFORME | CA-06 y última fila de 5.6 |
| E-12 | CONFORME | `GET /customers/1` devuelve `simulations` por `id` descendente; CA-07 |
| E-13 | CONFORME | `simulation_count: 0, simulations: []`; CA-07 |
| E-14 | CONFORME | Límite de 50 en SPEC-03 2.4; CA-07 (55/50) |
| E-15 | AMBIGUO | La rama del `422` es inalcanzable con el filtro, y la regla 2.1 es ambigua con `0` (H-06, H-07) |
| E-16 | CONFORME | CA-13, con Playwright, pendiente de la fase de QA |
| E-17 | CONFORME | Fila de 20000 en 5.5 |
| E-18 | CONFORME | `quote 10` devuelve 200 con `total_cents` 12100; filas de 5.5 |
| E-19 | CONFORME | CA-12 |
| E-20 | CONFORME | Fila «La proyección falla» de 5.5 |
| E-21 | SIN CASO DE PRUEBA | Ninguna fila de 5.5 comprueba que los importes se marquen como «actualizando» (H-04) |
| E-22 | AMBIGUO | ¿Decide el texto o el número? `Number('100000.000000000001')` da un entero (H-12) |
| E-23 | SIN CASO DE PRUEBA | Falta caso para «mientras se guarda» y para «proyección en carga» (H-04) |
| E-24 | CONFORME | El `201` de `/simulations` y el orden por `id` descendente, comprobados |
| E-25 | CONFORME | Fila de 500 y 503 en 5.5 |
| E-26 | NO COMPROBABLE | Depende del CORS real de Frankfurter; no hice peticiones a internet |
| E-27 | CONFORME | Filas 5.2 «diez veces» y 5.5 «USD» (mal asociadas a su criterio: H-05) |
| E-28 | AMBIGUO | Formatear EUR exige coma flotante o una vía no prevista (H-01) |
| E-29 | CONFORME | Fila de la fecha y fila de USD en 5.5 (formato del tipo sin fijar: H-09) |
| E-30 | CONFORME | Tabla 5.2, con dobles de prueba |
| E-31 | CONFORME | CA-09 |
| E-32 | CONFORME | CA-10 |
| E-33 | CONFORME | CA-10 y fila de 10 s de 5.6 |
| E-34 | CONFORME | CA-11 |
| E-35 | SIN CASO DE PRUEBA | Hay casos en el panel, el detalle y el simulador; en el alta, ninguno (H-04) |
| E-36 | CONFORME | Fila de almacenamiento en 5.5 |
| E-37 | CONFORME | Proyección con `customer_id` 2^53−1 inexistente: 404 `customer_not_found` |
| E-38 | CONFORME | Fila de los 500 ms en 5.5 |
| E-39 | CONFORME | Fila «Navegar … y volver» de 5.3 |
| E-40 | CONFORME | Filas de `/meta` en 5.3, 5.4 y 5.5; CA-07 |
| E-41 | CONFORME | El backend acepta 61 veces U+1D538 (201) y rechaza 121 `ñ` (`too_long`) |
| E-44 | CONFORME | `josé@empresa.example` da 201; `a@b` da `invalid_email`; un email de 255 da `too_long` |
| E-45 | CONFORME | Un *surrogate* suelto en el cuerpo da 400 `malformed_request` |
| E-46 | CONFORME | Identificador más 21 espacios: 201; más 22: `too_long`; email de 254 entre espacios: 201 |
| E-12 a E-14 | — | (ya listados arriba) |
| E-47 | CONFORME | `GET /customers/9007199254740991` da 404 `customer_not_found` |
| E-48 | CONFORME | `sim 422` devuelve `customer_id` y `storage_gb` en `errors` |
| E-49 | AMBIGUO | Mismo problema que E-22 (H-12) |
| E-50 | AMBIGUO | No dice qué pasa con la petición en curso al superar el límite (H-08) |
| E-51 | CONFORME | La codificación de `HttpParams` de Angular 21.2.26 da `100%25%20a%2Bb%26c%23d`, la URL que espera 5.3; el backend lee `q=a+b` como «a b» y `q=a%2Bb` como «a+b» |
| E-52 | CONFORME | Comprobación previa con `x-custom` o `x-xsrf-token`: 400 «Disallowed CORS headers». El interceptor XSRF de Angular no actúa con un origen distinto (`xsrfInterceptorFn`) |
| CA-01 | AMBIGUO | Las 28 celdas de 5.1 coinciden con Node, separador U+00A0; pero el criterio cita E-27, que un test del *pipe* no demuestra (H-05) |
| CA-02 | CONFORME | Tabla 5.2, con dobles de prueba |
| CA-03 | CONFORME | — |
| CA-04 | SIN CASO DE PRUEBA | Cita E-03 sin ninguna fila que lo cubra (H-04) |
| CA-05 | SIN CASO DE PRUEBA | Cita E-05 sin ninguna fila que lo cubra (H-04). Los ejemplos de SPEC-01 4.1 existen: `201`, `409` y tres `422` |
| CA-06 | CONFORME | — |
| CA-07 | CONFORME | — |
| CA-08 | SIN CASO DE PRUEBA | Cita E-21 y E-23 sin filas completas (H-04). Los importes de 10, 15, 51 y 20000 coinciden con SPEC-02 5.1 |
| CA-09 | CONFORME | — |
| CA-10 | CONFORME | — |
| CA-11 | CONFORME | 2.1 tiene cinco filas |
| CA-12 | CONFORME | Revisión manual |
| CA-13 | CONFORME | Pendiente de la fase de QA |
| CA-14 | CONFORME | El backend real admite el origen `http://localhost:4200` |
| CA-15 | CONFORME | Comprobación manual |
| CA-16 | CONFORME | Todas las filas de 5.6 son construibles con la forma real de los errores |
| CA-17 | AMBIGUO | La fila «/clientes/7 y 422» no puede darse con el backend real (H-06) |
| CA-18 | CONFORME | Ver «Lo que no he podido comprobar» sobre dónde añade Angular las cabeceras |

En la tabla, la fila «E-12 a E-14» es un separador sin veredicto propio: esos requisitos ya tienen su fila.

## 3. Hallazgos

**H-01 · media · Formatear un importe en EUR obliga a usar coma flotante, contra la regla.**
- SPEC-04:282-290 dice que la conversión es «el único punto del frontend con coma flotante sobre dinero» y que con EUR «el importe sale exacto de los céntimos». La spec obliga a formatear con `Intl.NumberFormat`.
- En la configuración por defecto del CLI (`"target": "ES2022"`, plantilla `tsconfig.json.template` de `@schematics/angular` 21.2.29), `format` solo admite `number | bigint` (`lib.es2020.bigint.d.ts:763`). Pasarle el texto exacto (`'169.40'`) solo lo admite `lib.es2023.intl.d.ts:51`.
- Por tanto, la implementación directa es `céntimos / 100`, una operación en coma flotante sobre dinero, que `CLAUDE.md` («El dinero nunca es `float`») y `.claude/rules/frontend.md:53-56` prohíben fuera de la conversión de divisa.
- El resultado mostrado es correcto: `céntimos / 100` y el texto exacto dan lo mismo en todos los valores probados, de 0 a 60520570 en pasos de 7, con 0 discrepancias. Pero la spec no dice cómo cumplir la regla.
- Afecta a: E-28, 2.6, CA-01 y la regla de dinero.

**H-02 · media · Requisitos citados por un criterio sin ningún caso que los demuestre.**
- E-03 (orden de la API en el panel): ninguna fila de 5.3 trae varios resultados en un orden dado. Lo cita CA-04.
- E-05 (países y planes «exactamente» los de `/meta`): ninguna fila de 5.4. Lo cita CA-05.
- E-21 (importes marcados como no vigentes): ninguna fila de 5.5. Lo cita CA-08.
- E-23: no hay caso para el botón desactivado «mientras se guarda» ni mientras la proyección está en carga.
- E-35, en el alta: ningún caso de los desplegables con nombres.
- Afecta a: CA-04, CA-05 y CA-08.

**H-03 · baja · Lo que SPEC-04 afirma del buscador con U+FFFD es falso.**
- SPEC-04:97-98 dice que el *surrogate* suelto se sustituye por U+FFFD, «que no coincide con ningún cliente».
- Pero el backend admite U+FFFD en un nombre (categoría So, no Cc/Cf): el alta con `company_name="a"+U+FFFD+"b Corp"` dio 201. Después, `GET /customers?q=a%EF%BF%BDb` devolvió ese cliente.
- Afecta a: 2.2 y la fila de 5.3 SPEC-04:628 (su resultado, «lo que devuelve la API», sigue valiendo).

**H-04 · baja · La tabla 4.1 no recoge el `422` del buscador que sí declara el OpenAPI.**
- SPEC-04:492-494 dice que la columna «Respuestas propias» recoge los estados que declara el OpenAPI, leído el 2026-11-14.
- Para `GET /customers?q=`, la fila SPEC-04:483 pone «`200`; `503`». El OpenAPI real declara `['200', '422', '503']`.
- El resto de filas coincide.

**H-05 · baja · CA-01 cita E-27, que un test del *pipe* no puede demostrar.**
- E-27 pide que, al cambiar de divisa, todos los importes visibles se conviertan sin hacer ninguna petición. Un test del *pipe* no puede mostrarlo.
- Las filas que sí lo muestran están en criterios que no citan E-27:
  - 5.2 «Cambio de divisa diez veces» (SPEC-04:603), de CA-02.
  - 5.5 «Cambiar la divisa a USD» (SPEC-04:687), de CA-08.

**H-06 · baja · El `422` del detalle no puede darse con el filtro, y su tratamiento choca con 2.7.**
- Todo `id` que pasa el filtro de 2.1 (de 1 a 2^53−1) es válido para el backend: `ROUTE_INTEGER`, en `backend/app/api/identifiers.py:17`.
- Así, `GET /customers/{id}` solo podría responder `422` por un parámetro de consulta no documentado. Ese es un defecto del frontend, que 2.7 (SPEC-04:344-352) manda mostrar como error inesperado.
- Sin embargo, 2.4 (SPEC-04:209-213) y la fila de 5.7 SPEC-04:736 lo muestran como «Cliente no encontrado».
- Afecta a: E-15 y CA-17.

**H-07 · baja · La regla 2.1 no excluye `0` en su texto.**
- SPEC-04:46-47 dice «de 1 a 16 dígitos ASCII, sin ceros a la izquierda». La convención del índice trata `0` como la forma escrita sin ceros a la izquierda (`ai-workspace/01-specs/README.md:96-97`).
- Leída al pie de la letra, `/clientes/0` cumple la forma y haría una petición. En cambio, 2.4 (SPEC-04:211) y la fila de 5.7 SPEC-04:731 esperan 0 peticiones.

**H-08 · baja · E-50 no dice qué pasa con la petición que ya está en curso.**
- Si hay una búsqueda en curso y el texto pasa de 100 caracteres, no se lanza una búsqueda nueva, así que E-02 no cancela la anterior. Su respuesta podría pintar la lista que E-50 manda retirar.
- Tampoco dice si el aviso espera los 300 ms.

**H-09 · baja · Hay detalles de presentación sin fijar.**
- El formato del tipo de cambio: el ejemplo «1,1139» (SPEC-04:294) no sale con el formato por defecto. `new Intl.NumberFormat('es-ES').format(1.1139)` da `1,114`, y para CHF da `0,923`.
- Los importes de 4 cifras: es-ES no pone separador de miles con 4 cifras (`1234,50 EUR` frente a `12.345,00 EUR`, comprobado). 5.1 no tiene ninguna fila de 4 cifras, aunque son habituales en el simulador.
- El tramo con `to_users: null`: no se dice cómo se rotula.

**H-10 · baja · D-13 no recoge la comprobación del *surrogate*.**
- D-13 (SPEC-04:788) limita la ayuda a «obligatorios, longitudes y lo mínimo del email».
- 2.3 y E-45 añaden la comprobación del *surrogate* suelto, que D-13 no menciona.

**H-11 · baja · La remisión de 5.7 a SPEC-01 5.10 está incompleta.**
- SPEC-04:721-722 dice: «Lo que responde el backend a cada texto está en SPEC-01, 5.10».
- SPEC-01 5.10 no tiene filas para `1e0`, U+0661, 9007199254740991, 9007199254740993 ni 17 dígitos.
- Respuestas reales comprobadas:
  - U+0661: 422 `not_an_integer`.
  - Los otros tres valores: 404 `customer_not_found`.

**H-12 · baja · «Valor válido» no aclara si decide el texto o el número.**
- SPEC-04:231-234 define un valor válido como `Number.isInteger` sobre el valor.
- `Number('100000.000000000001')` da 100000, un entero, así que se enviaría como entero un texto con decimales. Lo mismo pasa con `1e3`, que da 1000.
- La fila «`1,5` → error» no aclara si el criterio es el texto escrito o el número que resulta.
- Afecta a: E-22 y E-49.

## 4. Lo que no he podido comprobar

- **La API de Frankfurter**: su forma, su CORS, la caché, el fin de semana y los tipos del 4.2. No hice peticiones a internet; queda no comprobado por mí. Por eso E-26 sale como `NO COMPROBABLE`.
- **El comportamiento de un navegador real** con CORS: la respuesta oculta desde `127.0.0.1:4200`, que en realidad solo vi como ausencia de `access-control-allow-origin`, y la comprobación previa. Tampoco el `<input type="number">` con `1,5`.
- **Angular en ejecución**: solo leí su código, no lo ejecuté. Dos hechos que dependen de esa lectura:
  - Angular añade `Accept` y `Content-Type` en el *backend* HTTP (`_module-chunk.mjs:946-950` y `1079-1083`), no en `HttpRequest.headers`. Así que un test de CA-18 con `HttpTestingController` solo puede comprobar que no hay cabeceras de más, no las que viajan.
  - El cuerpo de un error se interpreta como JSON sea cual sea su `Content-Type` (`_module-chunk.mjs:1127-1131`).
- **Lo que sí está comprobado** de las afirmaciones de la spec:
  - La expresión regular del email de Angular 21.2.26 (`forms.mjs:269`).
  - El *target* ES2022 del CLI 21.2.29.
  - `isWellFormed` existe solo en `lib.es2024.string.d.ts`.
  - `/\p{Surrogate}/u` detecta las mitades sueltas y no la pareja de un emoji.
  - `encodeURIComponent` lanza `URIError` con una mitad suelta.
- **Mostrar la fecha tal cual con un desfase horario negativo** (fila de 5.5): `TZ` no surtió efecto con Node en Windows.
- **El `500` `tax_rate_not_defined`**: no lo provoqué contra el backend real, porque exige cambiar las constantes del dominio. Solo puede probarse con dobles de prueba, como dice 5.6.
- **`limitaciones-conocidas.md`**: no lo abrí. Comparé 4.3 con el resumen de L-01 a L-05 del encargo, y coincide. Además comprobé L-02 (el OpenAPI publica `maximum: 9.223372036854776e+18` y `minimum: 1.0`) y L-04 (con `q=a&q=` seguido de 101 `x`, el backend responde 422).
