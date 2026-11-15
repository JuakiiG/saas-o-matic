# Evaluación independiente del bloque frontend (SPEC-04)

| Campo | Valor |
|---|---|
| Inicio | `Sun, Nov 15, 2026 12:23:41 PM` (salida de `date`) |
| Fin | `Sun, Nov 15, 2026 12:32:05 PM` (salida de `date`) |
| Agente / modelo | Subagente evaluador (Claude Agent SDK); modelo Opus 5.5 (`claude-opus-5-5`), según mi propia configuración |
| Leído | `ai-workspace/01-specs/SPEC-04-frontend-y-divisas.md` (entera); las secciones de índice e historial de `ai-workspace/01-specs/README.md`; `CLAUDE.md`; `.claude/rules/frontend.md`; todo `frontend/src` (código y tests); `frontend/e2e/` (menos `capturas.spec.ts`, del que solo leí las 60 primeras líneas); `frontend/playwright.config.ts`, `package.json`, `angular.json`, `eslint.config.js` y `tsconfig.json`; en el backend, `app/config.py`, `app/domain/{countries,customers,pricing,simulations,tax_id}.py` (para tomar las constantes de CA-12) y las líneas de manejo de errores de `app/main.py` y `app/api/` |
| No leído | `ai-workspace/03-proceso/`, `ai-workspace/04-calidad/` (tampoco listados) y la historia de git. **No he leído enteros SPEC-01, SPEC-02, SPEC-03 ni los ADR**: el contrato lo comprobé con el código del backend y con sus respuestas reales (apartado C) |
| Herramientas | Node v24.18.0, npm 11.16.0, uv 0.12.13, `@playwright/test` 1.65.0 y Angular 21.2.26 (versiones de `package.json`), Git Bash |
| Estado del repo al terminar | `git status --short`: vacío. `HEAD`: `bab2922` |

## 1. Resumen

- **Oráculo `uv run scripts/check.py`**: código de salida 0. `ORÁCULO EN VERDE (solo lo activo: lo inactivo no está comprobado) · 23 correctas, 0 con fallo, 1 inactiva` (la inactiva es Playwright).
- **Oráculo `uv run scripts/check.py --e2e`**: código de salida 0. `ORÁCULO EN VERDE · 24 correctas, 0 con fallo, 0 inactivas`.
- **`npm run e2e`**: código de salida 0, `Running 14 tests using 1 worker … 14 passed (18.3s)`. Antes de cada ejecución comprobé con `netstat` que el 8000 y el 4200 estaban libres. Después, los dos puertos estaban libres y en la carpeta temporal no quedaba ninguna carpeta `saas-o-matic-e2e-*`.
- **Veredictos**: 54 requisitos y 18 criterios. Los 54 requisitos `CUMPLE`. De los criterios, 17 `CUMPLE` (CA-04, CA-05, CA-08 y CA-16 por muestreo) y 1 `NO DEMOSTRADO` (CA-15). Ninguno `NO CUMPLE`.
- **Hallazgos**: 10. Ninguno de severidad alta, uno de severidad media (H-02, contraste) y nueve de severidad baja.

### A. CA-12: el frontend no contiene reglas de negocio. Cómo lo he buscado

Saqué del backend lo que había que buscar:
- la tabla de letras del DNI, `DNI_LETTERS = "TRWAGMYFPDXBNJZSQVHLCKE"`;
- las letras de control del CIF, `CIF_CONTROL_LETTERS = "JABCDEFGHI"` y `CIF_LETTER_ONLY = "PQRSNW"`;
- los tramos, `TIERS = (Tier(1, 10, 1000), Tier(11, 50, 800), Tier(51, None, 500))`;
- los tipos impositivos 2100, 2300, 2000, 1900 y 2200.

Después busqué en `frontend/src` (y en `frontend/e2e`):

1. `grep -rlnE "TRWAGMYF|JABCDEFGHI" src e2e`: **ningún fichero**. `grep -rnE "TRWAGMYF|JABCDEFGHI|PQRSNW|% *23|%23|\b23\b" src` sin contar los `.spec.ts`: solo dos comentarios con «E-23».
2. Tipos impositivos (`2100|2300|2000|1900|2200|0\.21|21|23|20|19|22`) sin contar los `.spec.ts`: solo el comentario de `src/app/core/format.ts:65` (``2100` is `21 %``), la constante `SEARCH_MAX_RESULTS = 20` y textos de la interfaz.
3. Tarifa (`1000|800|500|10|11|50|51`) sin contar los `.spec.ts`: solo `SLIDER_MAX_USERS = 500` (`src/app/features/simulador/simulador-help.ts:10`), `INITIAL_USERS = 10` (`simulador.ts:28`) y comentarios. Ninguno es un precio ni un límite de tramo.
4. Palabras clave (`tier|tramo|cif|dni|nif|tax_rate|checksum|control|modulo|%`): solo aparecen modelos, presentación (`tierLabel` rotula `from_users` y `to_users` tal como llegan, `format.ts:89-90`) y `cents % CENTS_PER_UNIT`, que da formato a un importe (`format.ts:32`).

Los precios y los tipos solo aparecen como **datos simulados de respuestas** en los `.spec.ts`: 30 apariciones en 7 ficheros, todas `unit_price_cents`/`tax_rate_bp` dentro de cuerpos de respuesta. `tax_rate_bp` de `/meta` se declara en `core/models.ts:8` y no se usa. **Veredicto: CUMPLE.**

### B. Ejecución propia del código

- **Backend propio**: arrancado en el 8011 (PID 18132, confirmado con `netstat`) con `DATABASE_PATH` en la carpeta temporal del sistema. Lo paré con `taskkill //PID 18132` y borré su fichero temporal.
- **Funciones puras**, transpiladas con el `typescript` del proyecto:
  - `isRouteCustomerId`: `9007199254740991`→true, `…992`→false, `9999999999999999`→false, `0000000000000001`→false, `"1\n"`→false, U+FF11→false, vacío→false.
  - `trimSpaces("\t a   ")` → `"\t a "` seguido de U+00A0: solo quita U+0020.
  - `hasLoneSurrogate`: no marca una pareja bien formada y sí marca un *surrogate* suelto o una pareja invertida.
- **`DefaultUrlSerializer` de `@angular/router` 21.2.26** (con Node): ver H-01.

### C. Contrato real del backend (comprobado con `curl` contra el 8011)

- `/meta`, `POST /customers` (201, `created_at` `"2026-11-15T11:26:23Z"`, con `Z`), `GET /customers/1`, `POST /pricing/quote`, `POST /simulations` y `GET /customers?q=`: los campos coinciden exactamente con `src/app/core/models.ts`.
- Errores con la forma esperada: `customer_not_found` (404), `not_found` (404), `validation_error` con `errors` (422 en `/customers/abc`), `malformed_request` (400), `method_not_allowed` (405).
- Todas esas respuestas de error llevan `access-control-allow-origin: http://localhost:4200`, así que el navegador las puede leer y el frontend no las convierte en `network_error`.
- Comprobación previa CORS de `POST` con `content-type`: 200, `allow-methods: GET, POST`. Con una cabecera de más (`x-foo`): **400**. Confirma que CA-14 detectaría una cabecera propia.

## 2. Tabla por requisito y criterio

Las rutas de los tests son relativas a `frontend/src/app/` salvo las que empiezan por `frontend/e2e/`.

| Id | Veredicto | Evidencia |
|---|---|---|
| E-01 | CUMPLE | `features/panel/panel.spec.ts` «should ask for the initial list, without q…»; `panel.ts:103` |
| E-02 | CUMPLE | `panel.spec.ts:147-162` (nada a los 299 ms, una petición a los 300 ms), `:164` (cancelación) |
| E-03 | CUMPLE | `panel.spec.ts` «should keep the order of the API…» |
| E-04 | CUMPLE | `panel.spec.ts` «should say that nothing matches…» |
| E-50 | CUMPLE | `panel.spec.ts:371-372, 388-393, 414`; `frontend/e2e/limits.spec.ts:188` |
| E-51 | CUMPLE | `core/backend-api.spec.ts:216-249`; `panel.spec.ts:345-346` (`q=100%25%20a%2Bb%26c%23d`) |
| E-53 | CUMPLE | `panel.spec.ts` (20 y 19 clientes); `frontend/e2e/limits.spec.ts:212` |
| E-54 | CUMPLE | `panel.spec.ts` «should say there are no customers yet…» |
| E-35 | CUMPLE | Tests de nombres y de código desconocido en panel, detalle, alta y simulador; `core/meta-store.ts:38-45` |
| E-39 | CUMPLE | `app.spec.ts` «should ask at the start for /meta and for the rates, once each…»; `core/meta-store.spec.ts` |
| E-40 | CUMPLE | Tests de `/meta` en error en las cuatro vistas; `shared/meta-gate.ts` |
| E-05 | CUMPLE | `features/alta/alta.spec.ts` «should offer exactly the countries and plans of /meta…» |
| E-06 | CUMPLE | CA-12 (apartado A) |
| E-07 | CUMPLE | `alta.spec.ts` «should send a single request when «Guardar» is pressed twice»; `alta.ts:110-113` |
| E-08 | CUMPLE | `alta.spec.ts` (201); `frontend/e2e/journey.spec.ts` |
| E-09 | CUMPLE | `alta.spec.ts` (422 con dos campos, código desconocido, campo inexistente) |
| E-10 | CUMPLE | `alta.spec.ts` «should warn that the customer exists…» |
| E-11 | CUMPLE | `core/api-error.spec.ts` (CA-06); `alta.spec.ts` y `panel.spec.ts` con otro texto |
| E-41 | CUMPLE | `core/text.spec.ts`; filas de `alta.spec.ts`; `frontend/e2e/limits.spec.ts:102` (cuatro casos contra el backend real) |
| E-44 | CUMPLE | `alta.spec.ts:277-338`; `features/alta/alta-help.ts:47-63` (sin `Validators.email` ni `type="email"`) |
| E-45 | CUMPLE | `alta.spec.ts:338` y fila del nombre con *surrogate* suelto |
| E-46 | CUMPLE | `core/backend-api.spec.ts:256-285`; `alta.spec.ts:257` (sin `Location`) |
| E-56 | CUMPLE | `alta.spec.ts:584-638` (comprueba `document.activeElement`) |
| E-12 a E-14 | CUMPLE | `features/detalle/detalle.spec.ts` (orden, sin simulaciones, «Se muestran las 50 últimas de 55» en `:281-285`) |
| E-15 | CUMPLE | `detalle.spec.ts:310-345`; `features/simulador/simulador.spec.ts:746-800`. Ver H-01 |
| E-47 | CUMPLE | `core/customer-loader.spec.ts:87`; `detalle.spec.ts:310-345`. Ver H-01 |
| E-16 | CUMPLE | `frontend/e2e/responsive.spec.ts` (5 pruebas en verde) |
| E-17 | CUMPLE | `simulador.spec.ts:342` |
| E-18 | CUMPLE | `simulador.spec.ts:324-340` |
| E-38 | CUMPLE | `simulador.spec.ts:290` |
| E-19 | CUMPLE | CA-12; `features/simulador/projector.ts` solo copia la respuesta |
| E-20 | CUMPLE | `simulador.spec.ts` (sin conexión, `timeout`, 503) |
| E-21 | CUMPLE | `simulador.spec.ts` «should mark the amounts as «actualizando»…» |
| E-22 | CUMPLE | `simulador.spec.ts:417` (`-1`, `1,5`, `100001`, vacío, `15.0`, `1e3`, `+15`, `1 5`, `100000.000000000001`) |
| E-36 | CUMPLE | `simulador.spec.ts:568-571`; `frontend/e2e/limits.spec.ts:130` |
| E-37 | CUMPLE | `simulador.spec.ts` (404 en la proyección y en el guardado) |
| E-23 | CUMPLE | `simulador.spec.ts` (Guardar desactivado: antes de la primera proyección, proyección distinta, doble clic) |
| E-24 | CUMPLE | `simulador.spec.ts` (201); `frontend/e2e/journey.spec.ts` |
| E-25 | CUMPLE | `simulador.spec.ts:642-643` |
| E-48 | CUMPLE | `simulador.spec.ts` (422 de la proyección y del guardado) |
| E-49 | CUMPLE | `simulador.spec.ts` (`customer_id` del cliente cargado, `015`→15); `core/backend-api.spec.ts:295` |
| E-55 | CUMPLE | `simulador.spec.ts` «should warn that it may have been saved…» |
| E-26 | CUMPLE | `core/exchange-rates.spec.ts:54`; `app.spec.ts` |
| E-27 | CUMPLE | `shared/currency-selector.spec.ts` (diez cambios sin petición); tests de divisa del detalle y del simulador |
| E-28 | CUMPLE | `shared/money-pipe.spec.ts`; `app.journeys.spec.ts` (CA-03) |
| E-29 | CUMPLE | `shared/rate-note.spec.ts`; `simulador.spec.ts` (fecha del tipo); `frontend/e2e/rate-date.spec.ts`. Ver H-07 |
| E-30 | CUMPLE | `core/exchange-rates.spec.ts:92-199`; `currency-selector.spec.ts`; `frontend/e2e/responsive.spec.ts:106` |
| E-31 | CUMPLE | `app.journeys.spec.ts` (CA-09); no hay ningún `localStorage` ni `sessionStorage` (grep sin resultados) |
| E-32 | CUMPLE | `core/backend-api.spec.ts:151-200` (seis llamadas) |
| E-33 | CUMPLE | `core/backend-api.spec.ts:185` (9999 ms → cargando; 10000 ms → `timeout` y petición cancelada) |
| E-34 | CUMPLE | `app.routes.spec.ts` |
| E-42, E-43 | CUMPLE | `core/api-error.spec.ts:29-110`; tests de 503 y 500 en cada vista |
| E-52 | CUMPLE | `app.journeys.spec.ts` (CA-18); CORS real en `frontend/e2e/journey.spec.ts`; comprobación previa con `x-foo` → 400 (apartado C) |
| CA-01 | CUMPLE | `shared/money-pipe.spec.ts` (las cuatro columnas × 9 filas); `core/format.spec.ts` (tipo y rótulos) |
| CA-02 | CUMPLE | `core/exchange-rates.spec.ts`; `shared/currency-selector.spec.ts` |
| CA-03 | CUMPLE | `app.journeys.spec.ts` «should show the panel, the detail and the simulator in EUR…» |
| CA-04 | CUMPLE (muestreo) | `panel.spec.ts`; comprobé por muestreo las filas de 5.3, no todas |
| CA-05 | CUMPLE (muestreo) | `alta.spec.ts`; filas de 5.4 comprobadas por muestreo |
| CA-06 | CUMPLE | `core/api-error.spec.ts`; `alta.spec.ts`; `panel.spec.ts` |
| CA-07 | CUMPLE | `detalle.spec.ts` |
| CA-08 | CUMPLE (muestreo) | `simulador.spec.ts`; filas de 5.5 comprobadas por muestreo |
| CA-09 | CUMPLE | `app.journeys.spec.ts` |
| CA-10 | CUMPLE (con H-09) | `core/backend-api.spec.ts`, `core/customer-loader.spec.ts`, `core/exchange-rates.spec.ts:103` |
| CA-11 | CUMPLE | `app.routes.spec.ts` (cinco filas) |
| CA-12 | CUMPLE | Apartado A |
| CA-13 | CUMPLE | `frontend/e2e/responsive.spec.ts`, 5 pruebas en verde |
| CA-14 | CUMPLE | `frontend/e2e/journey.spec.ts`, en verde contra el backend real |
| CA-15 | NO DEMOSTRADO | Las capturas están en `ai-workspace/04-calidad/`, que no puedo leer, y su revisión es de una persona |
| CA-16 | CUMPLE (muestreo) | `core/api-error.spec.ts`, `core/backend-api.spec.ts` y tests de avisos de cada vista |
| CA-17 | CUMPLE | `detalle.spec.ts:310-345`; `simulador.spec.ts:746-800` |
| CA-18 | CUMPLE | `app.journeys.spec.ts`: métodos, `headers.keys()` vacío y cuerpos exactos |

## 3. Hallazgos

**H-01 · baja · Un cliente sigue teniendo más de una dirección en el frontend.**
El router de Angular descodifica el segmento antes de que llegue a `isRouteCustomerId`. Ejecutando `DefaultUrlSerializer.parse` de `@angular/router` 21.2.26 con Node:
- `/clientes/%31` → segmento `"1"`;
- `/clientes/1;x=y` → `"1"`;
- `/clientes/1%30` → `"10"`.

`core/customer-loader.ts:42` toma `params.get('id')`, que ya viene descodificado. Por tanto `/clientes/%31` pide `GET /customers/1` y muestra el cliente 1, que es lo que 2.1 dice querer evitar («el cliente 1 tendría varias direcciones»). La tabla 5.7 no tiene ninguna fila para un `id` codificado; la de `1%20` pasa porque se descodifica en `"1 "`.
*No comprobado en un navegador*, solo en el serializador. Afecta a 2.1 y E-47 (al propósito, no a la letra).

**H-02 · media · Contraste insuficiente del anillo de foco y del borde de los campos (WCAG 2.1 SC 1.4.11).**
- Anillo de foco `#f59e0b` (`src/styles/tokens.css:30`, aplicado en `src/styles/base.css:43-45`): **2,15:1** sobre blanco (tarjetas y campos) y **1,99:1** sobre el fondo `#f5f6f8`.
- Borde de los campos `#c9ced8` (`tokens.css:12`, `src/styles/controls.css:18`): **1,58:1** sobre blanco. El fondo del campo (blanco) frente al de la página es casi igual, así que el borde es lo único que delimita el campo.

Ratios calculados con la fórmula de luminancia relativa de WCAG, en Node. El umbral es 3:1. Afecta a `.claude/rules/frontend.md` («manejables con teclado») y a SPEC-04 2.8.

**H-03 · baja · Accesibilidad no cubierta por la spec que un revisor señalaría.**
- El título del documento es siempre «SaaS-O-Matic» (`src/index.html:5`) y ninguna ruta de `app.routes.ts` declara `title` (WCAG 2.4.2).
- Al navegar, el foco no se mueve a la vista nueva y no hay enlace para saltar al contenido.
- El resultado de una búsqueda no se anuncia: «No hay clientes que coincidan.» y la lista se pintan fuera de cualquier región `aria-live` (`features/panel/panel.html:44-47`, `:49`). El lector de pantalla oye «Cargando clientes…» (`role="status"`) y después nada.

**H-04 · baja · Muchas alertas a la vez.**
Cada error de campo es `role="alert"` (`features/alta/alta.html:17, 33, 51, 69, 86`; `features/simulador/simulador.html:43, 60, 77`). Un «Guardar» con el formulario vacío inserta cinco alertas a la vez y además mueve el foco (E-56), así que el lector de pantalla las lee todas e interrumpe la lectura del campo enfocado.

**H-05 · baja · Reglas aplicadas en el código que la spec no dice.**
- El aviso del `409` no tiene «Reintentar» (`features/alta/alta.ts:57-58`, `retryable: false`).
- El aviso general de un `422` tampoco (`core/api-error.ts:124-126`). En el simulador, un `422` de la proyección con `customer_id` deja el panel de la proyección sin «Reintentar» (`features/simulador/quote-panel.html:36-42`), y la tabla de 2.5 dice para el error «aviso con «Reintentar»». La única salida en la vista es «Volver al detalle», no un enlace al panel (2.7); el panel sí está enlazado en la cabecera.
- `formatDateTime` enseña tal cual un `created_at` que no es una fecha (`core/format.ts:75-80`), algo que 2.8 no dice.

**H-06 · baja · Comentario falso y límites escritos en varios sitios (relacionado con L-09).**
- `core/limits.ts:1` dice «The only limits of the backend that the frontend writes down». También los escriben `features/alta/alta-help.ts:13-16` (2, 120, 30, 254) y `features/simulador/simulador-help.ts:6-8`.
- Varios textos repiten la cifra en lugar de tomarla de la constante: `panel.html:20` («100 caracteres») y `:68` («20 clientes»), y `alta-help.ts:30` («entre 2 y 120»). Si cambia la constante, el texto se queda atrás sin que falle ningún test de tipos.

**H-07 · baja · Una prueba cita un requisito equivocado.**
`frontend/e2e/rate-date.spec.ts:7` y `:14` citan **E-27** para la fila de la zona horaria. E-27 trata del cambio de divisa sin petición; la fecha mostrada sin convertirla de zona horaria es **E-29**. La prueba comprueba bien lo que hace, pero la trazabilidad es errónea.

**H-08 · baja · Una orden habitual puede reescribir ficheros versionados.**
`frontend/playwright.config.ts:51-62` define los proyectos `pruebas` y `capturas` sin elegir uno por defecto. Un `npx playwright test` sin `--project` ejecuta también `capturas`, que escribe en `ai-workspace/04-calidad/capturas/` (`frontend/e2e/capturas/capturas.spec.ts:13`), fuera de `frontend/` y en ficheros versionados. Hoy solo lo impide que `npm run e2e` pase `--project=pruebas`. Lo saco de la lectura del código; no lo he ejecutado, porque está prohibido.

**H-09 · baja · CA-10: `MetaStore` no tiene un test propio de tiempo agotado.**
`grep -n "timeout\|useFakeTimers\|advanceTimers" core/meta-store.spec.ts` no da ningún resultado. El paso a error en 10 s solo se prueba en `core/backend-api.spec.ts:185` para `getMeta`, de forma indirecta. CA-10 pide el test «de cada servicio de `core/`».

**H-10 · baja · Seguridad del navegador.**
`src/index.html` no declara ninguna `Content-Security-Policy`, y la aplicación llama a un tercero (Frankfurter) desde el navegador. La spec no lo exige.

Lo que sí está bien:
- no hay `innerHTML`, `bypassSecurityTrust*`, almacenamiento local ni `withCredentials`, y todo se interpola con el escape de Angular;
- la respuesta de divisas se valida (`core/exchange-rates.ts:30-60`, incluido `Number.isFinite`);
- no hay interceptores (`app.config.ts:19-21`).

**Las pruebas de `e2e/` no tocan nada fuera de lo suyo:**
- la base de datos va en una carpeta de `mkdtempSync` del sistema (`frontend/e2e/support/temporary-folder.ts:29-37`), y tras dos ejecuciones no quedó ninguna;
- se borra `CORS_ORIGINS` antes de arrancar (`playwright.config.ts:21`);
- `reuseExistingServer: false` con comprobación de puerto, que Playwright hace en `127.0.0.1` y `::1`;
- el navegador no resuelve más que localhost (`--host-resolver-rules`);
- la API de divisas se responde por el protocolo de depuración de Chromium y no hay ningún `page.route()`;
- las llamadas directas van solo a `127.0.0.1:8000`, el backend que la propia ejecución arranca.

**Lo que no encontré:** código muerto, dependencias sin fijar, saltos de tests, reglas silenciadas, dependencias entre capas al revés (las reglas de ESLint de `eslint.config.js:42-76` y mi grep no dan nada) ni `HttpClient` fuera de `core/` (solo `provideHttpClient` en `app.config.ts`).

**Limitaciones conocidas L-06, L-08 y L-09:** las veo tratadas como dice SPEC-04: `core/customer-id.ts:6`, `features/simulador/simulador-view.ts:9-10` y `frontend/e2e/limits.spec.ts`. H-06 es un matiz de L-09.

## 4. Lo que no he podido comprobar

- **CA-15**: las capturas de `ai-workspace/04-calidad/capturas/` no puedo leerlas y las revisa una persona.
- **H-01 en un navegador real**: solo lo comprobé con el serializador de URL de Angular en Node.
- **Una cobertura completa, fila a fila, de 5.3, 5.4, 5.5 y 5.6**: las revisé por muestreo (unas 40 filas y todos los nombres de test). Por eso CA-04, CA-05, CA-08 y CA-16 llevan «muestreo».
- **SPEC-01, SPEC-02, SPEC-03 y los ADR**, que no leí enteros: el contrato lo contrasté con el código del backend y con sus respuestas reales.
- **El `503` y el `500` reales del backend en un navegador**: no los provoqué. Solo comprobé que las respuestas de error que sí provoqué llevan la cabecera CORS.
- **El borrado de la carpeta temporal de `e2e` si la ejecución se interrumpe de golpe**: depende del evento `exit` (`frontend/e2e/support/temporary-folder.ts:35`). No lo probé.
- **La experiencia real con lector de pantalla y el uso con teclado**: H-03 y H-04 salen de leer el marcado, no de probarlo con un lector de pantalla.
