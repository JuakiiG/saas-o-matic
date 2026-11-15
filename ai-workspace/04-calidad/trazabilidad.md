# Trazabilidad requisito → test

Qué tests citan cada requisito EARS de las cuatro specs. Sale de las citas
que hay escritas en los tests, no de una lista mantenida a mano.

| | |
|---|---|
| **Generada** | 2026-11-15, 17:41. La primera, el mismo día a las 16:24, sobre `f2379c4` |
| **Sobre el commit** | `f82184e`, más un cambio que entra en el mismo commit que esta versión del documento: el título de la prueba del detalle de `frontend/e2e/responsive.spec.ts`, que pasa a citar `SPEC-04/E-16`. Ningún otro cambio en `backend/` ni en `frontend/` (`git status --short backend frontend`) |
| **Orden** | `uv run scripts/traceability.py`, desde la raíz. Solo lee; escribe la matriz en la salida estándar |
| **Qué es salida de la orden** | El apartado 4 entero, sin retocar. Los apartados 1 a 3 los escribe la IA leyendo esa salida |

Para regenerarla: ejecutar la orden, sustituir con su salida todo lo que
hay bajo el título del apartado 4, y poner al día esta tabla y los
apartados 2 y 3.

## 1. Cómo se cuenta

**Qué es una cita.** `SPEC-nn/` seguido de uno o varios identificadores de
requisito (`E-nn`) o de criterio (`CA-nn`), unidos por coma, por «y» o, para
un rango, por «a»: `SPEC-04/E-05 a E-11, E-40` cita ocho requisitos. Un
identificador sin su spec delante (`(CA-05)`, `(E-29)`) no cuenta: es texto.

**Dónde se busca.**

| Grupo | Ficheros | Qué es un test | Dónde está la cita |
|---|---|---|---|
| Backend | `backend/tests/**/test_*.py` | Una función `test_…` | En su docstring |
| Frontend | `frontend/src/**/*.spec.ts` | Una declaración `it` o `it.each` | En su título o en el de un `describe` que lo contiene |
| Playwright | `frontend/e2e/**/*.spec.ts` | Una declaración `test` | En su título o en el de un `test.describe` que lo contiene |

Un comentario no es una cita, ni encima del test ni dentro.

**Se cuentan declaraciones, no casos.** Un test parametrizado es una
declaración aunque el *runner* haga de él muchos casos. Por eso las cifras
de la matriz son menores que las que dan los *runners* (salidas del
2026-11-15, 16:23):

| Grupo | Declaraciones (esta matriz) | Casos que ejecuta el *runner* |
|---|---|---|
| Backend | 183, en 23 ficheros | 741 (`pytest --collect-only`) |
| Frontend | 249, en 19 ficheros | 565 (`ng test`) |
| Playwright | 14, en 6 ficheros | 18 pruebas en 5 ficheros (`playwright test --list`) y 4 capturas en 1, con su propia configuración |

**Las columnas.** `Backend`, `Frontend` y `Playwright`: cuántos tests de
cada grupo citan el requisito. `Total`: la suma. **`En su título`**: de
ellos, cuántos lo citan en su propio título o docstring; el resto lo hereda
del bloque que los contiene. `Ficheros`: dónde están, con cuántos hay en
cada uno.

## 2. Lo que dice la matriz y lo que no dice

**Los 140 requisitos** (35, 15, 33 y 57) **tienen al menos un test que los
cita.** En la primera matriz eran 139: faltaba SPEC-04/E-16 (apartado 3).
Ninguna cita apunta a un requisito o a un criterio que no exista.

**En el backend cada número es exacto.** Cada test cita en su docstring lo
que comprueba (lo exige el oráculo), así que `Total` y `En su título`
coinciden en los 83 requisitos de SPEC-01 a SPEC-03.

**En el frontend el número dice menos de lo que parece.** La cita va casi
siempre en el `describe`, con una lista o un rango, y la heredan todos sus
tests. La matriz dice entonces **cuántos tests hay en bloques que citan el
requisito, no cuántos lo comprueban**:

- De los 57 requisitos de SPEC-04, **solo 11 tienen algún test que los cite
  en su propio título** (E-16, E-22, E-26, E-29, E-30, E-36, E-39, E-41,
  E-50, E-53 y E-57). **Los otros 46 se citan solo desde un `describe`.**
- El caso extremo es E-40, con 102 tests: son todos los de los bloques
  que lo nombran en su título, en cinco ficheros, no 102 comprobaciones de
  `/meta` en error.
- Qué test comprueba qué requisito del frontend **no se puede leer de las
  citas**. Lo que sí lo dice, fila a fila, son las tablas de casos de
  SPEC-04 (5.1 a 5.7) y sus criterios; la segunda evaluación independiente
  (`evaluacion-frontend-02.md`) contrastó las 109 filas de 5.3 a 5.6 con
  sus tests.
- **E-06 y E-19** (el navegador no comprueba el carácter de control del
  identificador y no calcula importes) solo se citan dentro de un rango
  (`E-05 a E-11` y `E-17 a E-22`). Su criterio, CA-12, no es un test: es
  la revisión del evaluador independiente. Que la matriz les dé 25 y 24
  tests no significa que alguno demuestre esa ausencia.

**21 tests del frontend no citan ningún requisito** (lista al final del
apartado 4). Los 21 citan un apartado de SPEC-04 que no tiene requisito
EARS propio: 2.1 (la cabecera), 2.2, 2.6 (el tipo y su fecha), 2.7 (los
mensajes de campo sin `role="alert"`) y 2.8 (la presentación: fechas,
porcentajes, tramos y enteros). No sobran: prueban reglas escritas en la
spec. Lo que falta es un requisito EARS al que atarlas.

**Los criterios no se cuentan.** Un `(CA-05)` suelto en un título no es una
cita, y la matriz no tiene filas de criterios. Solo se miran, para el
apartado 3, las citas completas (`SPEC-04/CA-13`).

**La matriz no ejecuta nada**: dice qué citan los tests, no que pasen. Eso
lo dice el oráculo.

## 3. Requisitos sin ningún test que los cite

**Ninguno.**

En la primera matriz (2026-11-15, 16:24) había uno:

| Requisito | Qué pide | Criterio que lo cubría | Qué se hizo |
|---|---|---|---|
| SPEC-04/E-16 | El detalle, sin desplazamiento horizontal a 375 px de ancho | **CA-13**: una prueba de Playwright por vista, la del detalle entre ellas. Estaba comprobado; faltaba su nombre en el título de la prueba. El comentario de cabecera de `frontend/e2e/responsive.spec.ts` dice «SPEC-04/CA-13 (E-16)», que no es una cita | Decisión del Tech Lead al aprobar la parada 1 de la sesión 09: la prueba del detalle a 375 px cita también `SPEC-04/E-16` en su título, además de CA-13. La prueba no cambia |

## 4. Matriz

<!-- Salida literal de `uv run scripts/traceability.py`. No se edita a mano. -->

### Tests contados

| Grupo | Tests declarados | Ficheros | Con alguna cita | Sin ninguna cita |
|---|---|---|---|---|
| Backend | 183 | 23 | 183 | 0 |
| Frontend | 249 | 19 | 228 | 21 |
| Playwright | 14 | 6 | 14 | 0 |

### SPEC-01

| Requisito | Backend | Frontend | Playwright | Total | En su título | Ficheros |
|---|---|---|---|---|---|---|
| E-01 | 7 | 0 | 0 | 7 | 7 | `backend/tests/integration/test_body_text.py` (1), `backend/tests/integration/test_customers_contract.py` (2), `backend/tests/integration/test_customers_create.py` (1), `backend/tests/integration/test_customers_read.py` (1), `backend/tests/integration/test_customers_repository.py` (1), `backend/tests/unit/test_customers.py` (1) |
| E-02 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_customers_create.py` (2), `backend/tests/unit/test_customers.py` (1) |
| E-03 | 5 | 0 | 0 | 5 | 5 | `backend/tests/integration/test_customers_create.py` (2), `backend/tests/unit/test_customer_errors.py` (1), `backend/tests/unit/test_customers.py` (2) |
| E-04 | 6 | 0 | 0 | 6 | 6 | `backend/tests/integration/test_customers_create.py` (2), `backend/tests/unit/test_customer_errors.py` (1), `backend/tests/unit/test_customers.py` (3) |
| E-05 | 4 | 0 | 0 | 4 | 4 | `backend/tests/integration/test_customers_contract.py` (2), `backend/tests/integration/test_customers_create.py` (1), `backend/tests/unit/test_customers.py` (1) |
| E-06 | 5 | 0 | 0 | 5 | 5 | `backend/tests/integration/test_customers_contract.py` (2), `backend/tests/integration/test_customers_create.py` (1), `backend/tests/unit/test_customers.py` (2) |
| E-07 | 6 | 0 | 0 | 6 | 6 | `backend/tests/integration/test_customers_contract.py` (1), `backend/tests/integration/test_customers_create.py` (2), `backend/tests/unit/test_customer_errors.py` (1), `backend/tests/unit/test_customers.py` (2) |
| E-08 | 6 | 0 | 0 | 6 | 6 | `backend/tests/integration/test_customers_create.py` (2), `backend/tests/integration/test_customers_read.py` (1), `backend/tests/unit/test_customers.py` (1), `backend/tests/unit/test_tax_id.py` (2) |
| E-09 | 1 | 0 | 0 | 1 | 1 | `backend/tests/unit/test_tax_id.py` (1) |
| E-10 | 3 | 0 | 0 | 3 | 3 | `backend/tests/unit/test_tax_id.py` (3) |
| E-11 | 3 | 0 | 0 | 3 | 3 | `backend/tests/unit/test_tax_id.py` (2), `backend/tests/unit/test_tax_id_differential.py` (1) |
| E-12 | 2 | 0 | 0 | 2 | 2 | `backend/tests/unit/test_tax_id.py` (1), `backend/tests/unit/test_tax_id_differential.py` (1) |
| E-13 | 5 | 0 | 0 | 5 | 5 | `backend/tests/unit/test_tax_id.py` (3), `backend/tests/unit/test_tax_id_differential.py` (2) |
| E-14 | 1 | 0 | 0 | 1 | 1 | `backend/tests/unit/test_tax_id.py` (1) |
| E-15 | 5 | 0 | 0 | 5 | 5 | `backend/tests/integration/test_customers_create.py` (1), `backend/tests/unit/test_customers.py` (1), `backend/tests/unit/test_tax_id.py` (3) |
| E-16 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_customers_create.py` (1), `backend/tests/unit/test_customers.py` (1), `backend/tests/unit/test_tax_id.py` (1) |
| E-17 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_customers_create.py` (1) |
| E-18 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_customers_create.py` (1), `backend/tests/unit/test_customers.py` (1) |
| E-19 | 4 | 0 | 0 | 4 | 4 | `backend/tests/integration/test_customers_create.py` (1), `backend/tests/integration/test_customers_repository.py` (2), `backend/tests/integration/test_schema.py` (1) |
| E-20 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_customers_create.py` (1) |
| E-21 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_customers_create.py` (1) |
| E-22 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_customers_history.py` (1), `backend/tests/integration/test_customers_read.py` (2) |
| E-23 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_customers_read.py` (1) |
| E-24 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_customers_read.py` (2) |
| E-25 | 7 | 0 | 0 | 7 | 7 | `backend/tests/integration/test_customers_read.py` (4), `backend/tests/integration/test_customers_search_sql.py` (2), `backend/tests/unit/test_customers.py` (1) |
| E-26 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_customers_read.py` (2) |
| E-27 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_customers_read.py` (1), `backend/tests/integration/test_customers_search_sql.py` (1) |
| E-28 | 4 | 0 | 0 | 4 | 4 | `backend/tests/integration/test_customers_search_sql.py` (4) |
| E-29 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_customers_read.py` (2), `backend/tests/unit/test_customers.py` (1) |
| E-30 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_customers_read.py` (2) |
| E-31 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_customers_read.py` (1) |
| E-32 | 4 | 0 | 0 | 4 | 4 | `backend/tests/integration/test_customers_contract.py` (3), `backend/tests/unit/test_customers.py` (1) |
| E-33 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_customers_create.py` (1), `backend/tests/unit/test_customers.py` (2) |
| E-34 | 6 | 0 | 0 | 6 | 6 | `backend/tests/integration/test_customers_contract.py` (1), `backend/tests/integration/test_customers_create.py` (2), `backend/tests/unit/test_customer_errors.py` (1), `backend/tests/unit/test_customers.py` (2) |
| E-35 | 6 | 0 | 0 | 6 | 6 | `backend/tests/integration/test_customers_create.py` (1), `backend/tests/unit/test_customer_errors.py` (2), `backend/tests/unit/test_customers.py` (3) |

### SPEC-02

| Requisito | Backend | Frontend | Playwright | Total | En su título | Ficheros |
|---|---|---|---|---|---|---|
| E-01 | 2 | 0 | 0 | 2 | 2 | `backend/tests/unit/test_pricing.py` (2) |
| E-02 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_pricing_quote.py` (1), `backend/tests/unit/test_pricing.py` (1) |
| E-03 | 3 | 0 | 0 | 3 | 3 | `backend/tests/unit/test_pricing.py` (3) |
| E-04 | 1 | 0 | 0 | 1 | 1 | `backend/tests/unit/test_pricing.py` (1) |
| E-05 | 1 | 0 | 0 | 1 | 1 | `backend/tests/unit/test_pricing.py` (1) |
| E-06 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_pricing_quote.py` (1), `backend/tests/unit/test_pricing.py` (2) |
| E-07 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_pricing_quote.py` (3) |
| E-08 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_simulations_create.py` (2) |
| E-09 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_pricing_quote.py` (1), `backend/tests/unit/test_pricing.py` (1) |
| E-10 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_pricing_quote.py` (1), `backend/tests/unit/test_pricing.py` (1) |
| E-11 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_pricing_quote.py` (3) |
| E-12 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_pricing_quote.py` (1) |
| E-13 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_pricing_quote.py` (2) |
| E-14 | 13 | 0 | 0 | 13 | 13 | `backend/tests/integration/test_body_text.py` (1), `backend/tests/integration/test_pricing_quote.py` (8), `backend/tests/integration/test_validation_errors.py` (4) |
| E-15 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_pricing_quote.py` (2) |

### SPEC-03

| Requisito | Backend | Frontend | Playwright | Total | En su título | Ficheros |
|---|---|---|---|---|---|---|
| E-01 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_simulations_create.py` (3) |
| E-02 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_simulations_create.py` (2) |
| E-03 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_simulations_create.py` (2) |
| E-04 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_simulations_create.py` (1) |
| E-05 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_simulations_create.py` (1) |
| E-06 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_real_endpoints.py` (1), `backend/tests/integration/test_simulations_create.py` (2) |
| E-07 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_simulations_create.py` (3) |
| E-08 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_simulations_create.py` (2) |
| E-09 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_simulations_create.py` (1) |
| E-10 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_simulations_create.py` (1) |
| E-11 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_simulations_create.py` (1), `backend/tests/integration/test_simulations_repository.py` (1) |
| E-12 | 7 | 0 | 0 | 7 | 7 | `backend/tests/integration/test_customers_history.py` (6), `backend/tests/integration/test_schema.py` (1) |
| E-13 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_customers_history.py` (1) |
| E-14 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_customers_history.py` (1), `backend/tests/integration/test_schema.py` (1) |
| E-15 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_customers_history.py` (2) |
| E-16 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_customers_history.py` (2) |
| E-17 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_customers_history.py` (2) |
| E-18 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_main.py` (1), `backend/tests/integration/test_real_endpoints.py` (1) |
| E-19 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_schema.py` (2), `backend/tests/integration/test_simulations_create.py` (1) |
| E-20 | 4 | 0 | 0 | 4 | 4 | `backend/tests/integration/test_schema.py` (4) |
| E-21 | 5 | 0 | 0 | 5 | 5 | `backend/tests/integration/test_schema.py` (5) |
| E-22 | 5 | 0 | 0 | 5 | 5 | `backend/tests/integration/test_schema.py` (5) |
| E-23 | 4 | 0 | 0 | 4 | 4 | `backend/tests/integration/test_customers_history.py` (1), `backend/tests/integration/test_customers_search_sql.py` (2), `backend/tests/integration/test_simulations_repository.py` (1) |
| E-24 | 7 | 0 | 0 | 7 | 7 | `backend/tests/integration/test_cors.py` (5), `backend/tests/integration/test_real_endpoints.py` (2) |
| E-25 | 4 | 0 | 0 | 4 | 4 | `backend/tests/integration/test_cors.py` (3), `backend/tests/integration/test_real_endpoints.py` (1) |
| E-26 | 4 | 0 | 0 | 4 | 4 | `backend/tests/integration/test_cors.py` (3), `backend/tests/integration/test_real_endpoints.py` (1) |
| E-27 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_health.py` (2) |
| E-28 | 4 | 0 | 0 | 4 | 4 | `backend/tests/integration/test_health.py` (4) |
| E-29 | 39 | 0 | 0 | 39 | 39 | `backend/tests/integration/test_body_text.py` (6), `backend/tests/integration/test_customers_create.py` (1), `backend/tests/integration/test_customers_read.py` (2), `backend/tests/integration/test_generated_docs.py` (6), `backend/tests/integration/test_generic_errors.py` (13), `backend/tests/integration/test_pricing_quote.py` (2), `backend/tests/integration/test_real_endpoints.py` (4), `backend/tests/integration/test_schema.py` (2), `backend/tests/integration/test_simulations_create.py` (2), `backend/tests/integration/test_validation_errors.py` (1) |
| E-30 | 2 | 0 | 0 | 2 | 2 | `backend/tests/integration/test_cors.py` (1), `backend/tests/integration/test_real_endpoints.py` (1) |
| E-31 | 3 | 0 | 0 | 3 | 3 | `backend/tests/integration/test_cors.py` (2), `backend/tests/integration/test_real_endpoints.py` (1) |
| E-32 | 1 | 0 | 0 | 1 | 1 | `backend/tests/integration/test_schema.py` (1) |
| E-33 | 4 | 0 | 0 | 4 | 4 | `backend/tests/integration/test_cors.py` (1), `backend/tests/integration/test_generated_docs.py` (1), `backend/tests/integration/test_generic_errors.py` (1), `backend/tests/integration/test_real_endpoints.py` (1) |

### SPEC-04

| Requisito | Backend | Frontend | Playwright | Total | En su título | Ficheros |
|---|---|---|---|---|---|---|
| E-01 | 0 | 24 | 0 | 24 | 0 | `frontend/src/app/features/panel/panel.spec.ts` (24) |
| E-02 | 0 | 24 | 0 | 24 | 0 | `frontend/src/app/features/panel/panel.spec.ts` (24) |
| E-03 | 0 | 24 | 0 | 24 | 0 | `frontend/src/app/features/panel/panel.spec.ts` (24) |
| E-04 | 0 | 24 | 0 | 24 | 0 | `frontend/src/app/features/panel/panel.spec.ts` (24) |
| E-05 | 0 | 25 | 0 | 25 | 0 | `frontend/src/app/features/alta/alta.spec.ts` (25) |
| E-06 | 0 | 25 | 0 | 25 | 0 | `frontend/src/app/features/alta/alta.spec.ts` (25) |
| E-07 | 0 | 25 | 0 | 25 | 0 | `frontend/src/app/features/alta/alta.spec.ts` (25) |
| E-08 | 0 | 25 | 0 | 25 | 0 | `frontend/src/app/features/alta/alta.spec.ts` (25) |
| E-09 | 0 | 35 | 0 | 35 | 0 | `frontend/src/app/core/api-error.spec.ts` (10), `frontend/src/app/features/alta/alta.spec.ts` (25) |
| E-10 | 0 | 25 | 0 | 25 | 0 | `frontend/src/app/features/alta/alta.spec.ts` (25) |
| E-11 | 0 | 37 | 0 | 37 | 0 | `frontend/src/app/core/api-error.spec.ts` (7), `frontend/src/app/features/alta/alta.spec.ts` (25), `frontend/src/app/features/panel/panel.spec.ts` (5) |
| E-12 | 0 | 19 | 0 | 19 | 0 | `frontend/src/app/features/detalle/detalle.spec.ts` (19) |
| E-13 | 0 | 19 | 0 | 19 | 0 | `frontend/src/app/features/detalle/detalle.spec.ts` (19) |
| E-14 | 0 | 19 | 0 | 19 | 0 | `frontend/src/app/features/detalle/detalle.spec.ts` (19) |
| E-15 | 0 | 35 | 0 | 35 | 0 | `frontend/src/app/core/customer-id.spec.ts` (2), `frontend/src/app/core/customer-loader.spec.ts` (9), `frontend/src/app/features/detalle/detalle.spec.ts` (19), `frontend/src/app/features/simulador/simulador.spec.ts` (5) |
| E-16 | 0 | 0 | 1 | 1 | 1 | `frontend/e2e/responsive.spec.ts` (1) |
| E-17 | 0 | 24 | 0 | 24 | 0 | `frontend/src/app/features/simulador/simulador.spec.ts` (24) |
| E-18 | 0 | 24 | 0 | 24 | 0 | `frontend/src/app/features/simulador/simulador.spec.ts` (24) |
| E-19 | 0 | 24 | 0 | 24 | 0 | `frontend/src/app/features/simulador/simulador.spec.ts` (24) |
| E-20 | 0 | 24 | 0 | 24 | 0 | `frontend/src/app/features/simulador/simulador.spec.ts` (24) |
| E-21 | 0 | 24 | 0 | 24 | 0 | `frontend/src/app/features/simulador/simulador.spec.ts` (24) |
| E-22 | 0 | 28 | 1 | 29 | 1 | `frontend/e2e/limits.spec.ts` (1), `frontend/src/app/features/simulador/simulador-help.spec.ts` (4), `frontend/src/app/features/simulador/simulador.spec.ts` (24) |
| E-23 | 0 | 12 | 0 | 12 | 0 | `frontend/src/app/features/simulador/simulador.spec.ts` (12) |
| E-24 | 0 | 12 | 0 | 12 | 0 | `frontend/src/app/features/simulador/simulador.spec.ts` (12) |
| E-25 | 0 | 12 | 0 | 12 | 0 | `frontend/src/app/features/simulador/simulador.spec.ts` (12) |
| E-26 | 0 | 21 | 0 | 21 | 1 | `frontend/src/app/app.spec.ts` (1), `frontend/src/app/core/exchange-rates.spec.ts` (10), `frontend/src/app/shared/currency-selector.spec.ts` (10) |
| E-27 | 0 | 16 | 0 | 16 | 0 | `frontend/src/app/features/detalle/detalle.spec.ts` (2), `frontend/src/app/features/simulador/simulador.spec.ts` (4), `frontend/src/app/shared/currency-selector.spec.ts` (10) |
| E-28 | 0 | 8 | 0 | 8 | 0 | `frontend/src/app/app.journeys.spec.ts` (1), `frontend/src/app/shared/money-pipe.spec.ts` (7) |
| E-29 | 0 | 17 | 1 | 18 | 1 | `frontend/e2e/rate-date.spec.ts` (1), `frontend/src/app/features/detalle/detalle.spec.ts` (2), `frontend/src/app/features/simulador/simulador.spec.ts` (4), `frontend/src/app/shared/money-pipe.spec.ts` (7), `frontend/src/app/shared/rate-note.spec.ts` (4) |
| E-30 | 0 | 21 | 2 | 23 | 2 | `frontend/e2e/capturas/capturas.spec.ts` (1), `frontend/e2e/responsive.spec.ts` (1), `frontend/src/app/app.journeys.spec.ts` (1), `frontend/src/app/core/exchange-rates.spec.ts` (10), `frontend/src/app/shared/currency-selector.spec.ts` (10) |
| E-31 | 0 | 6 | 0 | 6 | 0 | `frontend/src/app/app.journeys.spec.ts` (2), `frontend/src/app/features/simulador/simulador.spec.ts` (4) |
| E-32 | 0 | 19 | 0 | 19 | 0 | `frontend/src/app/core/backend-api.spec.ts` (5), `frontend/src/app/core/customer-loader.spec.ts` (9), `frontend/src/app/features/panel/panel.spec.ts` (5) |
| E-33 | 0 | 28 | 0 | 28 | 0 | `frontend/src/app/core/backend-api.spec.ts` (5), `frontend/src/app/core/customer-loader.spec.ts` (9), `frontend/src/app/core/meta-store.spec.ts` (9), `frontend/src/app/features/panel/panel.spec.ts` (5) |
| E-34 | 0 | 8 | 0 | 8 | 0 | `frontend/src/app/app.routes.spec.ts` (8) |
| E-35 | 0 | 76 | 0 | 76 | 0 | `frontend/src/app/core/meta-store.spec.ts` (9), `frontend/src/app/features/detalle/detalle.spec.ts` (19), `frontend/src/app/features/panel/panel.spec.ts` (24), `frontend/src/app/features/simulador/simulador.spec.ts` (24) |
| E-36 | 0 | 4 | 1 | 5 | 1 | `frontend/e2e/limits.spec.ts` (1), `frontend/src/app/features/simulador/simulador-help.spec.ts` (4) |
| E-37 | 0 | 12 | 0 | 12 | 0 | `frontend/src/app/features/simulador/simulador.spec.ts` (12) |
| E-38 | 0 | 25 | 0 | 25 | 0 | `frontend/src/app/features/simulador/simulador.spec.ts` (25) |
| E-39 | 0 | 11 | 0 | 11 | 1 | `frontend/src/app/app.journeys.spec.ts` (1), `frontend/src/app/app.spec.ts` (1), `frontend/src/app/core/meta-store.spec.ts` (9) |
| E-40 | 0 | 102 | 0 | 102 | 0 | `frontend/src/app/core/meta-store.spec.ts` (9), `frontend/src/app/features/alta/alta.spec.ts` (25), `frontend/src/app/features/detalle/detalle.spec.ts` (19), `frontend/src/app/features/panel/panel.spec.ts` (24), `frontend/src/app/features/simulador/simulador.spec.ts` (25) |
| E-41 | 0 | 27 | 1 | 28 | 1 | `frontend/e2e/limits.spec.ts` (1), `frontend/src/app/core/text.spec.ts` (2), `frontend/src/app/features/alta/alta.spec.ts` (25) |
| E-42 | 0 | 38 | 0 | 38 | 0 | `frontend/src/app/core/api-error.spec.ts` (8), `frontend/src/app/features/alta/alta.spec.ts` (25), `frontend/src/app/features/panel/panel.spec.ts` (5) |
| E-43 | 0 | 38 | 0 | 38 | 0 | `frontend/src/app/core/api-error.spec.ts` (8), `frontend/src/app/features/alta/alta.spec.ts` (25), `frontend/src/app/features/panel/panel.spec.ts` (5) |
| E-44 | 0 | 25 | 0 | 25 | 0 | `frontend/src/app/features/alta/alta.spec.ts` (25) |
| E-45 | 0 | 26 | 0 | 26 | 0 | `frontend/src/app/core/text.spec.ts` (1), `frontend/src/app/features/alta/alta.spec.ts` (25) |
| E-46 | 0 | 29 | 0 | 29 | 0 | `frontend/src/app/core/backend-api.spec.ts` (3), `frontend/src/app/core/text.spec.ts` (1), `frontend/src/app/features/alta/alta.spec.ts` (25) |
| E-47 | 0 | 37 | 0 | 37 | 0 | `frontend/src/app/core/backend-api.spec.ts` (2), `frontend/src/app/core/customer-id.spec.ts` (2), `frontend/src/app/core/customer-loader.spec.ts` (9), `frontend/src/app/features/detalle/detalle.spec.ts` (19), `frontend/src/app/features/simulador/simulador.spec.ts` (5) |
| E-48 | 0 | 46 | 0 | 46 | 0 | `frontend/src/app/core/api-error.spec.ts` (10), `frontend/src/app/features/simulador/simulador.spec.ts` (36) |
| E-49 | 0 | 42 | 0 | 42 | 0 | `frontend/src/app/core/backend-api.spec.ts` (2), `frontend/src/app/features/simulador/simulador-help.spec.ts` (4), `frontend/src/app/features/simulador/simulador.spec.ts` (36) |
| E-50 | 0 | 25 | 1 | 26 | 1 | `frontend/e2e/limits.spec.ts` (1), `frontend/src/app/core/text.spec.ts` (1), `frontend/src/app/features/panel/panel.spec.ts` (24) |
| E-51 | 0 | 29 | 0 | 29 | 0 | `frontend/src/app/core/backend-api.spec.ts` (5), `frontend/src/app/features/panel/panel.spec.ts` (24) |
| E-52 | 0 | 7 | 0 | 7 | 0 | `frontend/src/app/app.journeys.spec.ts` (2), `frontend/src/app/core/backend-api.spec.ts` (5) |
| E-53 | 0 | 24 | 1 | 25 | 1 | `frontend/e2e/limits.spec.ts` (1), `frontend/src/app/features/panel/panel.spec.ts` (24) |
| E-54 | 0 | 24 | 0 | 24 | 0 | `frontend/src/app/features/panel/panel.spec.ts` (24) |
| E-55 | 0 | 12 | 0 | 12 | 0 | `frontend/src/app/features/simulador/simulador.spec.ts` (12) |
| E-56 | 0 | 3 | 0 | 3 | 0 | `frontend/src/app/features/alta/alta.spec.ts` (3) |
| E-57 | 0 | 8 | 0 | 8 | 2 | `frontend/src/app/app.routes.spec.ts` (8) |

### Requisitos sin ningún test que los cite

Ninguno.

### Citas de algo que no está en las specs

Ninguna.

### Tests sin ninguna cita

- `frontend/src/app/app.spec.ts` (4)
- `frontend/src/app/core/exchange-rates.spec.ts` (3)
- `frontend/src/app/core/format.spec.ts` (11)
- `frontend/src/app/core/text.spec.ts` (1)
- `frontend/src/app/features/alta/alta.spec.ts` (2)
