# Segunda evaluación independiente del frontend (encargo acotado)

| Campo | Valor |
|---|---|
| Inicio | `Sun, Nov 15, 2026  2:00:55 PM` (salida de `date`) |
| Fin | `Sun, Nov 15, 2026  2:08:44 PM` (salida de `date`) |
| Agente y modelo | Subagente evaluador (Claude Agent SDK), modelo `claude-opus-5-5` |
| Leído | `CLAUDE.md`, `.claude/rules/frontend.md`, `ai-workspace/01-specs/README.md` (convenciones de la API), SPEC-04 entera, SPEC-01 2.12 y 4.1–4.4, SPEC-02 4, SPEC-03 4.1–4.4, todo `frontend/src/app` que se nombra abajo y sus tests, `frontend/e2e/` (contrast, rate-date, capturas, limits, support), las dos configuraciones de Playwright, `tsconfig.e2e.json`, `package.json`, los modelos y errores de `backend/app/api/` |
| No leído | `ai-workspace/03-proceso/`, `ai-workspace/04-calidad/`, ficheros `.env*`. No he usado la historia de git |
| Herramientas | uv 0.12.13, Node v24.18.0, Angular CLI 21.2.29, Vitest 4.1.12, Playwright 1.65.0 |
| Ejecuciones | Oráculo sin y con `--e2e`; `npx ng test --watch=false` (también con `--reporters=verbose`); `npm run e2e`; `npx playwright test --list` y `npx playwright test -c playwright.capturas.config.ts --list`; backend propio en el puerto 18765 con `DATABASE_PATH` temporal, parado por su PID (25380) y su carpeta temporal borrada |
| Puertos | Antes y después de cada ejecución de Playwright, ni el 8000 ni el 4200 estaban en `LISTENING`. Al terminar no quedaba ninguna carpeta `saas-o-matic-e2e-*` en la carpeta temporal del sistema |
| Estado final | `git status --short`: vacío · `git rev-parse --short HEAD`: `7f8c974` |

## 1. Resumen

- **Oráculo sin `--e2e`**: código de salida 0. «ORÁCULO EN VERDE (solo lo activo: lo inactivo no está comprobado) · 23 correctas, 0 con fallo, 1 inactiva». La inactiva es Playwright.
- **Oráculo con `--e2e`**: código de salida 0. «ORÁCULO EN VERDE · 24 correctas, 0 con fallo, 0 inactivas».
- **`npm run e2e`**: código de salida 0, `18 passed`. Entre ellas, las 4 de CA-19.
- **Tests unitarios**: código de salida 0. `Test Files 19 passed (19)`, `Tests 546 passed (546)`. Todos los tests que cito abajo aparecen en la salida detallada.
- **Filas emparejadas con un test**: 5.3, 24 de 24; 5.4, 40 de 40; 5.5, 29 de 29; 5.6, 16 de 16 (nivel 1). Ninguna fila se queda «sin test». En varias, el test no comprueba todo lo que el criterio pide: lo detallo fila a fila.
- **Veredictos**: CA-04, CA-05, CA-08 y CA-16 salen `NO CUMPLE`, todos por huecos en lo que comprueban los tests, no por un fallo de comportamiento que se observe.
- **Hallazgos**: 0 de severidad alta, 2 media y 7 baja.

## 2. Parte A

Leyenda de la tercera columna: **Sí** quiere decir que el test comprueba todo lo que dice la fila y el criterio. **Parcial** quiere decir que comprueba la fila pero le falta lo que se indica.

### 2.1 Tabla 5.3 (buscador): 24 filas, 24 emparejadas

Fichero de los tests: `frontend/src/app/features/panel/panel.spec.ts`.

| # | Fila | Test | ¿Lo comprueba? |
|---|---|---|---|
| 1 | Abrir el panel | :136 `should ask for the initial list, without q…` | Sí: una petición (`onlySearch`), URL sin `q`, la lista |
| 2 | `eje` deprisa | :147 `should search once, 300 ms after…` | Parcial: cero peticiones a los 299 ms y una a los 300, con `q`=`eje`. **No mira la URL** |
| 3 | `eje`, esperar, añadir `m` | :164 `should cancel the search in flight…` | Parcial: la primera queda cancelada y se muestra solo `ejem`. No mira la URL |
| 4 | `q=noexiste` con `items: []` | :179 `should say that nothing matches…` | Parcial: el mensaje y la ausencia del otro mensaje. No mira ni `q` ni la URL de la petición |
| 5 | Listado inicial vacío | :191 `should say there are no customers yet…` | Parcial: el mensaje, el enlace al alta y una sola petición. **No mira que vaya sin `q`** (ni la URL) |
| 6 | 20 clientes | :201 | Sí |
| 7 | 19 clientes | :210 | Sí |
| 8 | Orden de la API | :219 | Sí |
| 9 | `ES` y `professional` | :231 | Sí |
| 10 | `XX` y `legacy` | :243 | Sí |
| 11 | `/meta` falla | :260 | Parcial: el aviso, sin buscador y sin lista, y que no aparece `ES`. No mira que haya «Reintentar» ni la ausencia del código del plan (`professional`) |
| 12 | `/meta` falla y «Reintentar» funciona | :290 | Sí: una petición más a `/meta` y la lista con nombres |
| 13 | `/meta` llega después que la lista | :277 | Sí: la lista sin esperar y ninguna petición nueva |
| 14 | Del panel al detalle y vuelta | :304, más `src/app/app.journeys.spec.ts:196` | Parcial: :304 destruye y vuelve a crear el panel sin navegar. Como `Panel` nunca llama a `MetaStore.load()` (lo hace `app.config.ts:25`), el test no podría fallar. El recorrido de `app.journeys.spec.ts:196` sí navega panel → alta → detalle → simulador → detalle con un solo `GET /meta`, pero no vuelve al panel |
| 15 | La petición falla y se reintenta | :316 | Sí: el aviso y, al reintentar, `q`=`eje` |
| 16 | Borrar el texto | :330 | Sí: la URL sin `q` |
| 17 | Tres espacios | :344 (caso 1) | Sí: `getAll('q')` y la URL `q=%20%20%20` |
| 18 | `100% a+b&c#d` | :344 (caso 2) | Sí: `q` y la URL exacta |
| 19 | 100 emojis U+1F600 | :359 | Parcial: una petición y `q`. No mira la URL |
| 20 | 101 `x` | :370 (caso 1) | Sí: cero peticiones, el aviso con `role="alert"` y sin lista |
| 21 | 100 `x` y un espacio | :370 (caso 2) | Sí |
| 22 | Con el aviso, borrar hasta 100 | :385 | Parcial: una petición, `q` y el aviso retirado. No mira la URL |
| 23 | `a`, U+D800, `b` | :397 | Parcial: `q` con U+FFFD y una petición. No mira la URL |
| 24 | `eje` en curso y pegar 101 | :407 | Sí: cancelada, aviso al momento antes de avanzar el reloj, sin lista y ninguna petición nueva |

**CA-04: `NO CUMPLE`.** Todas las filas tienen su test, pero CA-04 pide comprobar «el parámetro `q` y la URL de cada una». En las filas 2, 3, 4, 5, 19, 22 y 23 no se mira la URL, y en la 4 y la 5 tampoco `q`. La fila 14 no la demuestra el test del panel. Ver N-04.

### 2.2 Tabla 5.4 (alta): 40 filas, 40 emparejadas

Fichero de los tests: `frontend/src/app/features/alta/alta.spec.ts`. CA-05 pide además que se compruebe el cuerpo de cada fila que se envía.

| # | Fila | Test | ¿Lo comprueba? |
|---|---|---|---|
| 1 | `201` con `id` 7 | :252 `should send the codes… and go to the detail on 201` | Sí: el cuerpo y `/clientes/7` |
| 2 | `422` `invalid_tax_id_format` | :378 (caso 1) | Parcial: el mensaje y los campos intactos. No mira el cuerpo |
| 3 | `422` `invalid_tax_id_check_character` | :378 (caso 2) | Parcial: igual que la fila 2. Que los dos mensajes son distintos se deduce de que cada caso compara con su propio texto |
| 4 | `422` en `company_name` y `contact_email` | :395 | Parcial: no mira el cuerpo |
| 5 | `422` con un `field` desconocido | :415 | Parcial: va al aviso general. No mira el cuerpo |
| 6 | `409` | :471 | Parcial: el aviso, los valores y que no navega. **No mira que falte «Reintentar»** (N-01) ni el cuerpo |
| 7 | `500` o sin conexión | :496 (caso `500`), :519 | Sí: el aviso con «Reintentar» y, en :496, el cuerpo del reintento |
| 8 | Doble clic en «Guardar» | :554 | Parcial: una sola petición. No mira el cuerpo |
| 9 | `/meta` falla | :563 | Sí |
| 10 | Ejemplo de `/meta` | :238, :252 | Parcial: las opciones que se pueden elegir, sus nombres y su orden, y el código que se envía. **No mira las primeras opciones desactivadas «Elige un país» y «Elige un plan»** ni que sean las que se ven al abrir |
| 11 | Un carácter sin pulsar «Guardar» | :358 | Sí |
| 12 | `422` en el identificador y se cambia | :461 | Sí |
| 13 | `500`, se cambia el nombre y «Reintentar» | :543 | Sí: el cuerpo con el nombre nuevo |
| 14 | Sin nombre y sin email | :626 (caso 1) | Sí: no se envía y el foco va al nombre |
| 15 | Solo el email mal | :626 (caso 2) | Sí |
| 16 | `422`, foco en el nombre | :642 (casos 1 y 2) | Sí |
| 17 | `422` en `plan`, foco | :642 (caso 4) | Sí |
| 18 | `409`, `500` o un `unknown_field` solo: el foco no se mueve | :659 | Sí |
| 19 | 61 caracteres U+1D538 | :268 (caso 1) | Sí: el cuerpo |
| 20 | 121 `ñ` | :325 | Sí |
| 21 | `A` rodeado de U+0020 | :325 | Sí |
| 22 | `AB` precedido de U+0009 | :268, :301 | Sí: el cuerpo y el `422` junto al campo |
| 23 | Nombre con U+0020 en los extremos | :268 (caso 4) | Parcial: el cuerpo recortado. «El detalle muestra el nombre que devuelve el backend» no está en este test |
| 24 | `AB` y U+00A0 | :268 (caso 3) | Sí |
| 25 | `AB` y U+D800 | :325 | Sí |
| 26 | `josé@empresa.example` | :268 | Sí |
| 27 | `a@b` | :268, :301 | Sí |
| 28 | `a`, U+00A0 y `b@c.example` | :268, :301 | Sí |
| 29 | `sin-arroba.example`, `@b.example`, `a@` | :325 (tres casos) | Sí |
| 30 | Email de 255 tras recortar | :325 | Sí (242 + 13 = 255) |
| 31 | Email de 254 entre U+0020 | :268 | Sí (241 + 13 = 254, cuerpo recortado) |
| 32 | Identificador con 21 espacios | :268 | Sí |
| 33 | Identificador con 22 espacios | :325 | Sí |
| 34 | Identificador de solo espacios | :268, :301 | Sí |
| 35 | `plan` y `unknown_field` `zeta` | :415 | Parcial: no mira el cuerpo |
| 36 | `plan` y una entrada sin `message` | :430 | Parcial: no mira el cuerpo |
| 37 | Dos errores en `tax_id` | :441 | Parcial: no mira el cuerpo |
| 38 | `422` sin ninguna entrada válida | :451 | Parcial: no mira el cuerpo |
| 39 | `503` | :496 (caso 2) | Sí: el aviso, «Reintentar» pulsado y el cuerpo |
| 40 | `201` sin `Location` | :252 | Sí: el flush no lleva cabeceras |

Las respuestas simuladas coinciden con SPEC-01 4.1: el `409`, los tres `422` y el `201`, este con `id` 7 como pide 5.4.

**CA-05: `NO CUMPLE`.** «De cada fila que se envía, el test comprueba además el cuerpo de la petición», y en las filas 2–6, 8 y 35–38 no se comprueba. La fila 10 no mira las opciones desactivadas. Ver N-03.

### 2.3 Tabla 5.5 (simulador): 29 filas, 29 emparejadas

Fichero de los tests: `frontend/src/app/features/simulador/simulador.spec.ts`. CA-08 pide además el cuerpo de cada petición.

| # | Fila | Test | ¿Lo comprueba? |
|---|---|---|---|
| 1 | Abrir | :302 | Sí: el cuerpo, 121,00 EUR y «España» |
| 2 | El cliente tarda 500 ms | :314 | Sí |
| 3 | `/meta` falla | :336 | Sí: el formulario y el cliente están ocultos, así que el código no puede verse |
| 4 | Arrastrar de 10 a 15 | :348 | Sí: el cuerpo de la única petición |
| 5 | 15 con la respuesta lenta | :379 | Parcial: «actualizando», «Guardar» y los importes. No mira el cuerpo de la petición de 15 |
| 6 | 51 mientras la de 15 sigue en curso | :404 | Sí |
| 7 | `20000` | :418 | Sí |
| 8 | `-1`, `1,5`, `100001`, vacío | :441 | Sí: cero peticiones, el error, sin importes y «Guardar» desactivado |
| 9 | `15.0`, `1e3`, `+15`, `1 5`, `100000.000000000001` | :441 | Sí |
| 10 | La proyección falla | :466 | Sí |
| 11 | «Reintentar» de la proyección | :466, :511 | Sí: la petición sale sin avanzar el reloj, con el cuerpo, y el aviso se retira |
| 12 | 15 antes de los 200 ms | :379 | Parcial: se ve «actualizando» y «Guardar» desactivado, pero **no comprueba «0 todavía»**: no cuenta las peticiones antes de los 200 ms |
| 13 | «Guardar» con `500` y «Reintentar» | :664 | Parcial: **los valores no cambian entre el fallo y el reintento**, así que el test no distingue «lo que el formulario tiene en ese momento» del cuerpo anterior (N-02) |
| 14 | Cambiar almacenamiento o llamadas | :578 | Sí |
| 15 | `-1`, `1,5`, `2.0`, `1e2` en almacenamiento | :591 | Sí |
| 16 | `/clientes/999/simulacion` | :827 | Sí |
| 17 | `/clientes/abc/simulacion` | :800 | Sí |
| 18 | `/clientes/7/simulacion` y proyectar | :302, :327 | Sí (`JSON.stringify` en :327) |
| 19 | `015` | :430 | Sí |
| 20 | `422` `active_users` de la proyección | :544 | Parcial: no mira el cuerpo |
| 21 | «Guardar» con `422` en `storage_gb` y `customer_id` | :707 | Parcial: no mira el cuerpo |
| 22 | `404` de la proyección | :748 | Parcial: no mira el cuerpo |
| 23 | Zona horaria con desfase negativo | `frontend/e2e/rate-date.spec.ts:14` (Playwright, `America/Los_Angeles`), más :877 en la zona de los tests | Sí, en Playwright. No es un test «con temporizadores simulados» como dice CA-08 |
| 24 | USD con 15 | :877 | Sí |
| 25 | «Guardar» con `201` | :638 | Parcial: el cuerpo y la navegación. «La simulación nueva es la primera» lo comprueba la prueba de principio a fin (CA-14), no este test |
| 26 | Doble «Guardar» | :653 | Parcial: no mira el cuerpo |
| 27 | «Guardar» con `500` o `503` | :664 | Sí |
| 28 | `timeout` al guardar | :686 | Parcial: no mira el cuerpo |
| 29 | «Guardar» con `404` | :740 | Parcial: no mira el cuerpo |

Las respuestas simuladas usan la forma de SPEC-02 4 y SPEC-03 4.1, con los importes de 10, 15, 51 y 20000 usuarios. He recalculado el de 20000: 10017000 + 2103570 = 12120570.

**CA-08: `NO CUMPLE`.** Faltan el cuerpo en las filas 5, 20–22, 26, 28 y 29; la fila 12 no comprueba «0 todavía»; y la 13 no demuestra lo que dice. Ver N-02 y N-03.

### 2.4 Tabla 5.6 (errores del backend): 16 filas, 16 emparejadas

**Nivel 1: servicios de `core/`.** El reparto de un código a su aviso está en `core/api-error.spec.ts`: `toApiError` en :30 y :53–72 y `noticeFor` en :92. Los estados por llamada, en `core/backend-api.spec.ts:354` (`503`, red y `timeout` para las seis llamadas) y en `core/customer-loader.spec.ts:97–128`.

| # | Fila | Test en `core/` | ¿Lo comprueba? |
|---|---|---|---|
| 1 | `GET /customers` `503` | backend-api :368 (searchCustomers), api-error :30 y :92 | Sí. La repetición de la misma búsqueda está en panel :433 |
| 2 | `GET /customers/{id}` `503` | customer-loader :105 | Sí: error y no «no encontrado» |
| 3 | `POST /customers` `503` | backend-api :368 (createCustomer) | Sí. Lo de no navegar está en alta :496 |
| 4 | `POST /pricing/quote` `503` | backend-api :368 (quote) | Sí. En la vista, simulador :466 |
| 5 | `POST /simulations` `503` | backend-api :368 (saveSimulation) | Sí. En la vista, simulador :664 |
| 6 | `/meta` `200` y `/customers` `503` | Ningún test de `core/`; la cubre panel :433 | Parcial: es una composición de vista |
| 7 | `500` `internal_error` | api-error :30 y :92; customer-loader :105 | Sí |
| 8 | `500` `tax_rate_not_defined` | api-error :30 y :92 | Sí |
| 9 | `400`, `415`, `405` | api-error :30 y :92 | Sí |
| 10 | `GET /customers/{id}` `404` `not_found` | customer-loader :105 | Sí |
| 11 | `422` `validation_error` en el buscador o en el cliente | customer-loader :105; api-error :92 | Sí |
| 12 | `teapot` | api-error :30 y :92 | Sí |
| 13 | `502` con un cuerpo que no es JSON | api-error :53 | Sí: `unknown_error` |
| 14 | Error de red | backend-api :381; api-error :64 y :92 | Sí |
| 15 | Sin respuesta en 10 s | backend-api :391; customer-loader :118; meta-store :253 | Sí |
| 16 | El mismo `503` con otro `detail` | api-error :82 | Sí |

**Nivel 2: un aviso distinto por vista, con «Reintentar».**

| Vista | Servicio no disponible | Error inesperado | Falta de conexión | Espera agotada |
|---|---|---|---|---|
| Panel | :433, con «Reintentar» pulsado | :445, con «Reintentar» | :464, **no comprueba «Reintentar»** | :473, **no comprueba «Reintentar»** |
| Alta | :496, pulsado | :496, pulsado | :519, con «Reintentar» | :530, con «Reintentar» |
| Detalle | :368, pulsado | :368, pulsado | :389, con «Reintentar» | No está en la vista; el servicio sí (customer-loader :118, código `timeout`) |
| Simulador, proyección | :466, pulsado | :466, pulsado | :489, **no comprueba «Reintentar»** | :500, con «Reintentar» |
| Simulador, guardado | :664, pulsado | :664, pulsado | Ningún test | :686, con «Reintentar» |
| Simulador, cliente | :842, pulsado | :842, pulsado | Servicio (customer-loader) | Servicio (customer-loader :118) |

**CA-16: `NO CUMPLE`.** El nivel 1 está completo salvo la fila 6, que solo se ve en la vista. En el nivel 2, tres casos no comprueban que haya «Reintentar»: panel :464 y :473, y simulador :489. Ver N-05.

## 3. Parte B

### 3.1 Modelos (`frontend/src/app/core/models.ts`) contra el contrato

He contrastado las specs con `backend/app/api/{meta,customers,pricing,simulations}.py`, y además con el backend real (sondeo de abajo).

| Llamada | Modelo | Contrato (spec y backend) | Diferencias |
|---|---|---|---|
| `GET /meta` | `MetaData{countries, plans}`, `Country{code, name, tax_rate_bp: number}`, `Plan{code, name}` | SPEC-01 4.4; `MetaResponse`, `CountryItem`, `PlanItem` | Ninguna. Todos los campos obligatorios y no nulos |
| `GET /customers` | `CustomerList{items}`, `CustomerSummary{id, company_name, tax_id, country, plan}` | SPEC-01 4.3; `CustomerItem` | Ninguna |
| `POST /customers` (petición) | `NewCustomer`, con los cinco campos de texto | SPEC-01 4.1; `CustomerRequest` con `extra="forbid"` | Ninguna. El cuerpo se construye campo a campo (`backend-api.ts:54-60`) |
| `POST /customers` (`201`) | `Customer` = `NewCustomer` + `id: number` + `created_at: string` | SPEC-01 4.1; `CustomerResponse` | Ninguna |
| `GET /customers/{id}` | `CustomerDetail` = `Customer` + `simulation_count` + `simulations: Simulation[]` | SPEC-01 4.2 y SPEC-03 4.2; `CustomerProfileResponse` | Ninguna |
| `POST /pricing/quote` | `QuoteRequest{customer_id, active_users}`; `Quote{currency, active_users, tiers, base_cents, country, tax_rate_bp, tax_cents, total_cents}`; `Tier{…, to_users: number \| null}` | SPEC-02 4; `QuoteResponse` y `TierChargeResponse` | Ninguna. `to_users` admite nulo en los dos lados. `currency` es `string` frente al literal `"EUR"`, sin efecto |
| `POST /simulations` | `NewSimulation` = `QuoteRequest` + `storage_gb` + `estimated_api_calls`; `Simulation` = `Quote` + `id`, `customer_id`, `storage_gb`, `estimated_api_calls`, `created_at` | SPEC-03 4.1; `SimulationRequest` y `SimulationResponse` | Ninguna |
| Errores | `FieldError{field, code, message}`; el cuerpo de error no tiene interfaz: solo se lee `code` y `errors` (`api-error.ts:53-60`) | Convenciones: `type`, `title`, `status`, `code`, `detail` y, a veces, `errors` | `type`, `title`, `status` y `detail` no se modelan porque no se usan (2.7: «el `detail` del backend no decide nada»). Es coherente |

El único desajuste de tipo es que todos los `id` son `number` y el contrato llega a 2^63 − 1. Es la limitación conocida L-06 y no la cuento como defecto.

**Sondeo del backend real** en el puerto 18765, con base temporal:

- `GET /customers/%31` responde `200` con el cliente 1. Confirma lo que afirma SPEC-04 2.1.
- `GET /customers/1;x=y` responde `422` `not_an_integer`. La spec no afirma nada del backend para ese texto, y el frontend nunca lo envía: el router quita el parámetro de matriz.
- `GET /customers/1?x=1` responde `422` con un solo error, `x` `unknown_field`, como dicen las convenciones.
- Un `POST /customers` con varios errores los devuelve en el orden del contrato y deja `unknown_field` al final, como dice 2.12. Con el país no válido, no hay error de `tax_id`.

### 3.2 Qué hace el frontend con cada `code`

Abreviaturas que uso en las tablas:

- **EN**: `ErrorNotice` (`shared/error-notice.ts`). Muestra `noticeFor(code)` y siempre lleva «Reintentar».
- **Aviso de formulario con reintento**: `formErrors` (`api-error.ts:114-115`). Aviso general con `noticeFor` y «Reintentar».
- **Campo o aviso general**: `formErrors` con `validation_error` y entradas válidas (`api-error.ts:117-119`). Cada entrada va junto a su campo si el formulario lo tiene; si no, va al aviso general, sin «Reintentar».

**`service_unavailable` (503)**

| Llamada | Qué hace | ¿Coincide con SPEC-04? |
|---|---|---|
| `GET /meta` | `MetaGate`: EN «no disponible»; «Reintentar» repite `/meta` | Sí (2.1). SPEC-04 4.1 dice que `/meta` no lo responde |
| `GET /customers` | EN en la región de resultados; «Reintentar» repite la búsqueda | Sí (5.6) |
| `POST /customers` | Aviso de formulario con reintento | Sí |
| `GET /customers/{id}` | EN, no «no encontrado» (`customer-loader.ts:56-58`) | Sí |
| `POST /pricing/quote` | Aviso con reintento; se retiran los importes (`projector.ts:301-302`) | Sí |
| `POST /simulations` | Aviso con reintento; los valores se conservan | Sí |

**`internal_error` (500)**: en las seis llamadas, el mismo camino que el `503`, pero con el aviso «inesperado». Coincide con 2.7.

**`tax_rate_not_defined` (500)**: en la proyección y en el guardado, aviso «inesperado» con «Reintentar», y el código queda en el estado (`simulador.spec.ts:466` y :664). En el resto de llamadas no puede llegar. Coincide.

**`malformed_request` (400), `unsupported_media_type` (415) y `method_not_allowed` (405)**: en las seis llamadas, EN o aviso de formulario «inesperado» con «Reintentar», y el código queda en el estado (`toApiError`). Coincide.

**`not_found` (404)**

| Llamada | Qué hace | ¿Coincide? |
|---|---|---|
| `GET /customers/{id}` | EN «inesperado», no «no encontrado» (`customer-loader.ts:57` solo mira `customer_not_found`) | Sí |
| Las otras cinco | «Inesperado» con «Reintentar» | Sí |

**`validation_error` (422)**

| Llamada | Qué hace | ¿Coincide? |
|---|---|---|
| `GET /meta` | EN «inesperado» | Sí (E-43) |
| `GET /customers` | EN «inesperado»; las `errors` (`q` `too_long`, `unknown_field`) no se muestran junto al campo | Sí (2.7 y 2.2) |
| `POST /customers` | Campo o aviso general; con cero entradas válidas, «inesperado» con «Reintentar» | Sí (2.3) |
| `GET /customers/{id}` | EN «inesperado» | Sí (2.4) |
| `POST /pricing/quote` | Campo o aviso general, sin «Reintentar»; se retiran los importes | Sí (2.5) |
| `POST /simulations` | Campo o aviso general, sin «Reintentar»; los valores se conservan | Sí |

**`customer_already_exists` (409, solo en `POST /customers`)**: aviso propio «Ya existe un cliente…», sin «Reintentar» (`alta.ts:55-59`); el foco no se mueve. Coincide con 2.3 y 2.7, pero ningún test fija que falte «Reintentar» (N-01).

**`customer_not_found` (404)**

| Llamada | Qué hace | ¿Coincide? |
|---|---|---|
| `GET /customers/{id}` | Vista «Cliente no encontrado», en el detalle y en el simulador | Sí |
| `POST /pricing/quote`, `POST /simulations` | Vista «Cliente no encontrado» (`simulador.ts:107-112`) | Sí (E-37) |

**Un código desconocido (`teapot`)**: en todas las llamadas, «inesperado» con «Reintentar», y el código se conserva. Coincide.

**Códigos de campo**: `missing`, `not_a_string`, `too_short`, `too_long`, `invalid_characters`, `invalid_email`, `unsupported_country`, `unsupported_plan`, `invalid_tax_id_format`, `invalid_tax_id_check_character`, `not_an_integer` y `out_of_range`.

| Llamada | Qué hace | ¿Coincide? |
|---|---|---|
| `POST /customers` | El `message` junto al campo indicado por `field`, sin mirar el código (`alta.spec.ts:406`, con un código desconocido); se retira al cambiar el campo | Sí (2.3, D-12) |
| `POST /pricing/quote`, `POST /simulations` | Si `field` es uno de los tres campos numéricos, el mensaje va junto a él; `customer_id` va al aviso general sin «Reintentar» | Sí (2.5) |
| `GET /customers` (`q` `too_long`), `GET /customers/{id}` (`id`) | Nunca se muestran: EN «inesperado» | Sí (2.7) |

**`unknown_field`**: en los `POST`, al aviso general como un campo que el formulario no tiene; en los `GET`, «inesperado». Coincide con 2.3.

**Códigos propios del frontend**:

- `network_error`: el aviso de falta de conexión con «Reintentar».
- `timeout`: el aviso de espera agotada con «Reintentar»; al guardar, además, el enlace al detalle (`simulador-view.ts:395-401`).
- `unknown_error`: «inesperado».

Los tres coinciden con 2.7.

No he encontrado ninguna diferencia entre spec y backend, ni entre spec y frontend, en el tratamiento de los códigos.

## 4. Parte C

| # | Afirmación | Comprobación | Resultado |
|---|---|---|---|
| 1 | El `id` se filtra ya descodificado; `%31` y `1;x=y` piden el cliente 1 | Los tests nuevos usan el router real (`RouterTestingHarness`): `detalle.spec.ts:336` y `simulador.spec.ts:783`. Los dos pasan y comprueban la URL exacta `/customers/1`, el detalle y la proyección. El backend real responde `200` a `/customers/%31`. `customer-loader.ts:37` lee `paramMap`, que ya viene descodificado y sin el parámetro de matriz. La frase de 5.7 sobre «las tres primeras filas» cuadra con la tabla | Se sostiene. Que «el código de la aplicación no cambió» no lo puedo comprobar sin la historia de git |
| 2 | Contraste: anillo de acento y `--color-control-border` | `tokens.css:11` y :34; `controls.css:56`; el anillo, en `base.css:43-45`. La fórmula de `e2e/support/contrast.ts` es la de WCAG 2.x: linealización sRGB con umbral 0,04045 y (L1 + 0,05) / (L2 + 0,05). La he recalculado con Node. `#1d4ed8` da 6,70 sobre el blanco y 6,20 sobre `#f5f6f8`; `#7c8698`, 3,67 y 3,40; el antiguo `#c9ced8`, 1,58; el naranja `#f59e0b`, 2,15. Sobre los fondos de los avisos (`#fef3f2`, `#eef4ff`), el anillo da más de 6. La prueba lee los colores calculados de los cuatro campos que nombra CA-19, comprueba `:focus-visible`, `solid 3px` y `solid 1px`, y pasa (4 de 4 en `npm run e2e`). La tarjeta y el aviso siguen con `--color-border` (`cards.css:5`, `notice.css:5`, `app.css:9`). `capturas.spec.ts:153` añade `alta-foco` y CA-15 la nombra | Se sostiene. Dos límites, ninguno es defecto de CA-19: solo se lee el borde superior, y el deslizante (`input[type=range]`, sin borde) queda fuera de la prueba |
| 3 | Título del documento | `app.routes.ts:5-32`; `app.routes.spec.ts:85-96` pone otro título antes de navegar, así que el test puede fallar. Pasa | Se sostiene en las cuatro vistas. Pero la página «no encontrada», sin título, **conserva el de la vista anterior** al navegar dentro de la aplicación (N-06). Además, el `describe` sigue llamándose `Routes · SPEC-04/E-34`, y el comentario de :45-46 («join this file as each view arrives») ha quedado viejo |
| 4 | `role="alert"` | `alta.html`: ningún `field-error` lleva `role`. `simulador.html:496`, :512 y :528 y `panel.html:155` sí lo llevan. Los tests nuevos de `alta.spec.ts:589` y :606 pasan y comprueban también `aria-describedby` y `aria-invalid` | Se sostiene. Ningún test fija el `role="alert"` del simulador (N-08) |
| 5 | Solo spec: sin «Reintentar» en el `409` ni en el aviso general del `422`, la fila «Error» de 2.5, y `created_at` | El código coincide con el texto: `alta.ts:56-58` (`retryable: false`), `api-error.ts:114-119` (sin entradas, «inesperado» con reintento; con entradas al aviso general, sin reintento) y la proyección y el guardado por la misma vía. `format.ts:75-79` devuelve el texto si `Date` no lo lee | El texto describe el código. Pero **ningún test de vista fija la ausencia de «Reintentar»**, y la regla del `409` no la prueba ningún test (N-01). El `created_at` solo lo fija `format.spec.ts:64` con `ayer`; `Date` lee como fecha textos que no lo son (N-07) |
| 6 | Comentario de `limits.ts` | `core/limits.ts:1-3`: los límites de los formularios están junto a su ayuda (`alta-help.ts:203-206` y `simulador-help.ts:408-410`), y `e2e/limits.spec.ts` contrasta con el backend real los 100 caracteres de búsqueda (:188), los 20 resultados (:212), el nombre, el email, el identificador y los números | Correcto |
| 7 | `rate-date.spec.ts` cita E-29 | `e2e/rate-date.spec.ts:6` y :14 citan E-29 y 5.5. E-29 es el del tipo, su fecha sin convertir y el total en EUR | Correcto |
| 8 | Configuración de Playwright | `npx playwright test --list`: «Total: 18 tests in 5 files», sin `capturas`. `npx playwright test -c playwright.capturas.config.ts --list`: «Total: 4 tests in 1 file», solo `capturas.spec.ts`. `playwright.config.ts:268` (`testIgnore`) y `playwright.capturas.config.ts:18-21`; `package.json` con `e2e` y `e2e:capturas` como se dice; `tsconfig.e2e.json:9` incluye las dos configuraciones y `npm run lint` pasa (oráculo). `.claude/rules/frontend.md` lo describe igual | Se sostiene. Ninguno de los dos `--list` dejó carpetas temporales |
| 9 | Test de `meta-store` | `core/meta-store.spec.ts:253`: sigue cargando a los 9.999 ms y a los 10.000 está en error `timeout`, con la petición cancelada; «Reintentar» pide otra vez. Pasa. La espera la pone `BackendApi` (`remote.ts:23`) | Se sostiene |
| 10 | Limitaciones conocidas L-09, L-10 y L-11 | Tenidas en cuenta; no las señalo | — |

**Historial y referencias cruzadas de SPEC-04.** Las filas del 2026-11-15 de `SPEC-04-frontend-y-divisas.md:1154-1158` recogen los cambios 1 a 5, con los colores exactos de los tokens. He revisado estas referencias y siguen diciendo lo que se cita: E-56 en 2.7; 2.3 y 2.5 entre sí y con 2.7; CA-11 (E-34 y E-57); CA-19 en 2.8; CA-15 con `alta-foco`; «las tres primeras filas» de 5.7; y E-29 en `rate-date`. Hay dos detalles menores que no llevo a hallazgos: el párrafo «Sobre CA-12 a CA-15» (`:1033`) habla ya también de CA-19 sin que su título lo diga, y el nombre de la comprobación del oráculo, «Playwright: principio a fin y 375 px», no nombra CA-19 aunque la ejecuta.

## 5. Hallazgos

**N-01 · media.** La regla «sin Reintentar» del `409` y del aviso general de un `422`, que se acaba de escribir en la spec (2.3, 2.5 y 2.7), no la fija ningún test de vista. La del `409` no la fija ningún test.

- Evidencia: la regla del `409` vive solo en `alta.ts:55-59` (`retryable: false`). `alta.spec.ts:471` (`409`) y :483 (CA-06) no miran el botón; :483 compara el texto antes y después, y los dos incluirían «Reintentar» si apareciera. `grep -rn "not.toContain('Reintentar')\|retryable: false" src/app --include=*.spec.ts` solo encuentra `core/api-error.spec.ts:169` (la función `formErrors`). Ni `alta.spec.ts:415`, ni `simulador.spec.ts:561`, ni :707 comprueban que falte el botón.
- Afecta a: SPEC-04 2.3, 2.5 y 2.7 (cambio 5) y a CA-05.

**N-02 · media.** La fila de 5.5 «"Guardar" falla con `500` y se pulsa "Reintentar"» pide enviar «lo que el formulario tiene en ese momento», y el test no puede distinguirlo de reenviar el cuerpo anterior.

- Evidencia: `simulador.spec.ts:664-683` no cambia ningún valor entre el fallo y `press(page, 'Reintentar', SAVE_NOTICE)`, y espera `SAVED_BODY`, que es el mismo cuerpo. El alta sí lo prueba (`alta.spec.ts:543`). Por inspección, `simulador.ts:148-157` lee los valores del momento, pero no está demostrado.
- Afecta a: CA-08 y SPEC-04 2.7 («Reintentar» en un formulario).

**N-03 · baja.** CA-05 y CA-08 piden comprobar el cuerpo de cada envío, y muchas filas no lo hacen.

- Evidencia, alta: `alta.spec.ts:378`, :395, :415, :430, :441, :451, :471 y :554 no miran el cuerpo. La fila de los desplegables (:238) no comprueba las opciones desactivadas «Elige un país» y «Elige un plan»: ninguna búsqueda de `Elige` en el fichero.
- Evidencia, simulador: `simulador.spec.ts:379`, :544, :653, :686, :707, :740 y :748 no miran el cuerpo; :379 tampoco cuenta las peticiones antes de los 200 ms («0 todavía»).
- Afecta a: CA-05 y CA-08.

**N-04 · baja.** CA-04 pide comprobar «el parámetro `q` y la URL de cada una», y varias filas no miran la URL. La fila de «navegar y volver» no la demuestra el test del panel.

- Evidencia: `panel.spec.ts:147`, :164, :359, :385 y :397 solo miran `params.get('q')`; :179 y :191 no miran ni `q` ni la URL.
- `panel.spec.ts:304` no puede fallar: `Panel` no llama a `MetaStore.load()`, que solo se llama en `app.config.ts:25`.
- `panel.spec.ts:260` no mira que haya «Reintentar».
- Afecta a: CA-04 y E-39.

**N-05 · baja.** En el nivel 2 de CA-16, tres casos no comprueban que haya «Reintentar», y el guardado del simulador no tiene caso de falta de conexión.

- Evidencia: `panel.spec.ts:464` y :473 y `simulador.spec.ts:489` solo comprueban el texto del aviso. No hay ningún test con `ProgressEvent` sobre `simulationRequests`.
- Afecta a: CA-16.

**N-06 · baja.** La página «no encontrada» conserva el título de la vista anterior cuando se llega a ella navegando dentro de la aplicación, por ejemplo con «Atrás» del navegador a una dirección que no existe. Un lector de pantalla anunciaría otra vista.

- Evidencia: la ruta `**` no tiene `title` (`app.routes.ts:33-36`). `DefaultTitleStrategy.updateTitle` solo cambia el título si `title !== undefined` (`node_modules/@angular/router/fesm2022/_router-chunk.mjs:3345-3349`). El título inicial, `SaaS-O-Matic`, solo lo pone `index.html`, al cargar la página. Ningún test cubre el título de esa página.
- Afecta a: E-57 y su razón (2.1). La spec solo dice que esa página «no tiene título propio».

**N-07 · baja.** «Un `created_at` que no se puede leer como fecha se muestra como llega» (2.8) depende de lo que acepte `Date`, que lee como fecha textos que no lo son.

- Evidencia: `format.ts:76-79`. Con `node -e` en Node 24, `new Date('Ejemplo 7')` da `2001-06-30T22:00:00.000Z`, `new Date('1')` da `2000-12-31T23:00:00.000Z` y `new Date('12/11/2026')` da el 10-11 de diciembre. Es decir, se mostraría una fecha inventada en lugar del texto. El único test es `format.spec.ts:64`, con `ayer`.
- Afecta a: SPEC-04 2.8 (cambio 5).

**N-08 · baja.** Ningún test fija que los mensajes junto a los campos del simulador lleven `role="alert"`, que 2.7 dice ahora expresamente. El del buscador sí está fijado (`panel.spec.ts:381`).

- Evidencia: `grep -n "role" src/app/features/simulador/*.spec.ts` solo encuentra `[role="status"]` y el `[role="alert"]` de los avisos generales (:319, :340, :854, :857 y :937), nunca en `#simulador-*-error`.
- Afecta a: SPEC-04 2.7 (cambio 4).

**N-09 · baja.** Dos filas de 5.5 se cumplen fuera del test del simulador. La de la zona horaria está en Playwright (`e2e/rate-date.spec.ts:14`) y no en un test «con temporizadores simulados». La de «la simulación nueva es la primera» está en CA-14 (`e2e/journey.spec.ts:9`), no en `simulador.spec.ts:638`.

- Evidencia: las líneas citadas. Las dos pasan en `npm run e2e` (18 de 18).
- Afecta a: la redacción literal de CA-08.

## 6. Lo que no he podido comprobar

- **Que el código de la aplicación no cambiara con el cambio 1, y cuáles de los tests son nuevos**: hace falta la historia de git, que el encargo no permite usar.
- **El anillo de foco y los bordes a la vista**: no he abierto las capturas de CA-15, que están en `04-calidad/`, ni he mirado un navegador fuera de Playwright. Tampoco el contraste del deslizante, que CA-19 no cubre, ni cómo se ve el foco en el desplegable nativo abierto.
- **Cualquier comportamiento con un lector de pantalla**: lo que se anuncia con `role="alert"` y con el título. Es la limitación L-10.
- **El OpenAPI publicado**: he contrastado el contrato con el código de `backend/app/api/` y con peticiones reales al backend, no con `/openapi.json`.
- **La página «no encontrada» con el título viejo (N-06) en un navegador**: la conclusión sale del código del router y de la configuración de rutas, no de una ejecución.
