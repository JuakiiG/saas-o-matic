# Respuesta a la evaluación independiente del backend

| | |
|---|---|
| **Fecha** | 2026-11-13 |
| **Responde a** | [`evaluacion-backend-01.md`](evaluacion-backend-01.md), que queda intacto (commit `1e682fd`) |
| **Decide** | Tech Lead. **Ningún hallazgo está decidido todavía**: la columna «Qué propone la IA» es una propuesta |
| **Escribe** | IA (Claude Code) |
| **Estado del código** | El mismo que evaluó el informe (`bda2c65`). **No se ha implementado ninguna corrección** |

Procedimiento: el informe del evaluador no se modifica; se responde a cada
hallazgo. Antes de responder, la IA ha repetido por su cuenta cada sonda del
informe (apartado 2). Los 15 hallazgos se reproducen tal como el informe los
describe.

Resumen de la respuesta:

- **De acuerdo, es un defecto del código** (6): H-01, H-02, H-04, H-05,
  H-07 y H-12.
- **De acuerdo, es un hueco de las specs o de los tests**, no del
  comportamiento (5): H-03, H-09, H-10, H-11 y H-14.
- **De acuerdo con el hecho, pero ya lo había decidido el Tech Lead** (4):
  H-06 (L-04), H-08 (Y-13), H-13 (r4) y H-15 (L-01). El evaluador no podía
  saberlo: no lee `03-proceso/` ni `04-calidad/`. Los cuatro vuelven a la
  mesa por si el informe cambia la decisión.
- **En desacuerdo**: ninguno.
- **Un caso más**, encontrado al repetir la sonda de H-02 y que el informe
  no trae: fila A-01.

## 1. Respuesta por hallazgo

| Hallazgo | Grav. | ¿De acuerdo? | Qué propone la IA | Qué habría que tocar |
|---|---|---|---|---|
| H-01 · Un `id` de ruta de 4301 dígitos o más responde `500` | media | **Sí.** Defecto del código, introducido con la forma única del `id` (`ce04f42`): la expresión regular lo da por entero y la biblioteca falla después con un tipo de error (`int_parsing_size`) que el traductor no conoce. Los tests llegan hasta 2^63 | Que un entero bien escrito, por grande que sea, responda `422` con `out_of_range`: es un entero y está fuera del rango. Traducir ese tipo de error a `out_of_range`, con dos filas de test (4300 y 4301 dígitos), vistas en rojo antes | `app/api/validation.py`, test de 5.10. Si se quiere la fila en la spec: SPEC-01 5.10, con historial |
| H-02 · Un surrogate suelto en el nombre o en el email responde `500` | media | **Sí.** Defecto: una entrada del cliente acaba en un `500`. La spec solo excluye las categorías `Cc` y `Cf`, y un surrogate es `Cs`; el fallo salta al escribir en la base de datos | **La regla la decide el Tech Lead**; la spec no la tiene. Opción recomendada: tratar `Cs` como las otras dos, `invalid_characters` en `company_name` y `contact_email`. Alternativa: rechazar en el guarda cualquier cuerpo con un surrogate suelto, con `400` `malformed_request`; es más amplia, pero el cuerpo sí es JSON válido según la gramática. Ver también A-01 | SPEC-01 2.1 o 2.12 y filas en 5.7, con historial; `app/domain/customers.py`; tests en rojo antes |
| H-03 · Un parámetro de consulta desconocido oculta los errores del cuerpo y del `id` | media | **Sí en lo esencial.** El comportamiento no lo inventó el código en silencio: la IA lo declaró (W-15) y el Tech Lead pidió el test que lo fija al revisar SPEC-02. Pero el evaluador tiene razón en que **la regla no está escrita en las convenciones**, y debería | Escribir la regla en «Errores de validación» del índice, con historial: los parámetros de consulta se comprueban antes que la ruta y el cuerpo, y si alguno no está documentado se responde solo con ellos. Sin cambio de código. Alternativa: juntar los dos grupos de errores en una sola respuesta; cambia el código, el test de W-15 y exige fijar el orden entre ambos | Opción recomendada: solo `01-specs/README.md`. Alternativa: `app/api/request_guard.py`, `app/api/error_handling.py` y tests |
| H-04 · Un entero JSON de más de 4300 dígitos responde `400` | baja | **Sí.** Defecto: el cuerpo es JSON válido y el `400` está reservado a lo que no lo es. La causa es el límite de dígitos de `int` de Python al leer el JSON | Leer los enteros del cuerpo de forma que uno desmesurado no falle, sino que llegue a la validación como un entero fuera de cualquier rango: `422` con `out_of_range` en un campo entero y `not_a_string` en uno de texto. Filas de test con 4300 y 4301 dígitos, en rojo antes. Alternativa: dejarlo y anotarlo como limitación conocida | `app/api/request_guard.py` y tests. O `04-calidad/limitaciones-conocidas.md` |
| H-05 · `q` con el carácter NUL devuelve todos los clientes | baja | **Sí.** Defecto: SQLite corta el patrón de `LIKE` en el NUL. Comprobado además que `q=a%00` busca «acaba en `a`» en vez de «contiene `a` y un NUL» | **La regla la decide el Tech Lead.** Opción recomendada: `q` no admite caracteres de control ni de formato (`Cc` y `Cf`), igual que el nombre, con `422` e `invalid_characters` en el campo `q`; ningún nombre guardado puede contenerlos. Alternativa sin tocar el contrato: un `q` con NUL no coincide con nada y devuelve la lista vacía | Recomendada: SPEC-01 2.10, E-30, 4.3 y filas en 5.9, con historial; validación de `q`; tests en rojo antes |
| H-06 · Con un `q` repetido solo se valida el último | baja | **Sí con el hecho.** Que gana el último ya está aceptado como **L-04** (2026-11-13). Lo nuevo del informe es la consecuencia: un `q` de 101 caracteres pasa sin error si no es el último. Ese valor se descarta y no llega a usarse | Mantener L-04 y ampliar su texto con esta consecuencia. Alternativa: rechazar un parámetro documentado repetido; no hay código de campo para eso en el contrato, habría que crearlo | `04-calidad/limitaciones-conocidas.md`. La alternativa: índice de specs, SPEC-01 y código |
| H-07 · Se aceptan cuerpos en UTF-16 o con BOM | baja | **Sí.** Defecto: la intención, visible en el test `not-utf8`, es aceptar solo UTF-8, y el lector de JSON de Python adivina la codificación por su cuenta | Decodificar el cuerpo como UTF-8 estricto antes de leer el JSON: UTF-16, UTF-32 y un BOM inicial responden `400` `malformed_request`. Precisar en la tabla de errores genéricos que el cuerpo es JSON **en UTF-8**. Tests en rojo antes | `app/api/request_guard.py`, tests y una frase en `01-specs/README.md` con historial |
| H-08 · El email admite espacios distintos de U+0020 | baja | **Sí con el hecho.** Es la lectura que la IA declaró (Y-13) y que el Tech Lead admitió al revisar SPEC-01: «espacio» es U+0020. El evaluador acierta en que la spec no lo dice | Que la spec diga lo que hace el código: en SPEC-01 2.1, «sin espacios (U+0020)». Alternativa más estricta: rechazar en el email cualquier separador Unicode (categorías `Zs`, `Zl` y `Zp`) con `invalid_email`, con filas nuevas en 5.7 | Recomendada: una frase en SPEC-01 2.1, con historial. La alternativa: además, `app/domain/customers.py` y tests en rojo |
| H-09 · Hay endpoints que ninguna spec define (`/docs`, `/redoc`) | baja | **Sí.** Son los que FastAPI publica por defecto; nadie los pidió, y `/docs` carga recursos de un servidor externo. `/openapi.json` es distinto: es el contrato, y los tests de CA-10, CA-14 y CA-16 lo leen | Desactivar `/docs` y `/redoc` (pasan a `404` `not_found`) y dejar `/openapi.json`, escribiendo en el índice de specs que existe, que no es un endpoint de negocio y que no aplica la regla del parámetro desconocido. Alternativa: conservar `/docs` como ayuda de desarrollo y documentarlo en el README | `app/main.py`, un test en rojo antes y una frase en `01-specs/README.md` |
| H-10 · CORS anuncia más cabeceras admitidas que la spec | baja | **Sí con el hecho; no es un defecto del código.** Es lo que hace el middleware estándar: añade las cabeceras que la norma CORS admite siempre. La spec dice «la cabecera admitida, `content-type`» | Ajustar el texto de SPEC-03 2.7 («`content-type`, además de las que la norma CORS admite siempre») y fijar en el test de la comprobación admitida el valor exacto de la cabecera, como ya se hace en las rechazadas. Sin cambio de código | SPEC-03 2.7 con historial; `tests/integration/test_real_endpoints.py` |
| H-11 · Parte de la regla del buscador está en SQL (`? <> ''`) | baja | **En parte.** La spec manda hacer la comparación con `LIKE`, así que la coincidencia se ejecuta en SQL por fuerza. Pero la decisión «si `q` normalizado queda vacío, no se compara con el identificador» sí es una regla y podría tomarla el dominio | Que `customer_search` del dominio devuelva «sin identificador que comparar» (ningún valor) cuando la forma normalizada queda vacía, y que el repositorio pase ese valor como parámetro nulo: en SQL, `LIKE` con un nulo no coincide con nada y la condición `? <> ''` desaparece. Mismo resultado, la regla en `domain/`. Alternativa: dejarlo, por ser un detalle de la consulta | `app/domain/customers.py`, `app/repositories/customers.py` y sus tests |
| H-12 · `Any` sin un comentario que lo justifique | baja | **Sí.** Descuido de la IA en `app/repositories/simulations.py`; en los demás ficheros cada `Any` lleva su comentario. El oráculo no lo comprueba | Añadir el comentario (las filas que devuelve `sqlite3` no tienen tipo) o, mejor, dar a la fila un tipo concreto. Anotar en `CLAUDE.md` que esta regla no la comprueba el oráculo, o hacer que la compruebe | `app/repositories/simulations.py`; opcional, `scripts/` y `CLAUDE.md` |
| H-13 · Un test declara que se escribió después del código | baja | **Sí con el hecho; fue una orden.** El Tech Lead pidió ese test «anotado como escrito después del código» al revisar SPEC-01 (r4). **No es el único**: también se escribieron después, y solo consta en la bitácora, los de `test_customers_repository.py` y `test_customer_errors.py` (Y-12), la aserción de los límites del `id` en el OpenAPI (Z-04) y las siete filas de CORS con endpoints reales (b2); las de 5.7 y CA-09 que pasaron a la primera están en M-07 | Dejar el test como está. Para que quien lea el código lo vea sin ir a la bitácora, poner el mismo comentario en los otros tests escritos después. Alternativa: no tocar nada | Solo comentarios en ficheros de test |
| H-14 · La prueba con conexión que registra no cubre todas las sentencias | baja | **Sí.** El alta de un cliente, la lectura de un cliente y la del país no pasan por esa prueba; que usan parámetros solo se ha visto leyendo el código | Ampliar la prueba a esas tres sentencias. Serían tests escritos después del código: se anotarían así y se comprobarían con una mutación | `tests/integration/test_customers_search_sql.py` o un fichero nuevo |
| H-15 · No hay límite de tamaño del cuerpo | baja | **Sí con el hecho.** Aceptado por el Tech Lead como **L-01** el 2026-11-13, al revisar el paso 1. El informe añade la medida: un nombre de 2.000.000 de caracteres se procesa entero | Mantener L-01 y añadirle esa medida. Si el Tech Lead quiere cerrarla: un máximo de cuerpo en el guarda, con un `413` nuevo en la tabla de errores genéricos; es un cambio del contrato y del frontend | `04-calidad/limitaciones-conocidas.md`. Cerrarla: índice de specs, ADR-006, SPEC-03 5.7, SPEC-04 y código |
| A-01 · *(no está en el informe)* Un **nombre de campo desconocido** con un surrogate suelto responde `500` | — | Lo encontró la IA al repetir la sonda de H-02. `POST /customers` y `POST /pricing/quote` con una clave como `"x\ud800"` responden `500` `internal_error`: el fallo salta al escribir la respuesta `422`, que lleva ese nombre en `field` | Decidirlo junto con H-02. Si se elige rechazar en el guarda todo cuerpo con un surrogate suelto (`400`), este caso queda cubierto; si se elige `invalid_characters` por campo, hace falta además una regla para los nombres de campo | Lo mismo que H-02 |

## 2. Qué ha comprobado la IA antes de responder

Sondas propias, con el cliente de test y una base de datos en el directorio
temporal del sistema, fuera del repositorio. Ningún fichero del repositorio
ha cambiado al ejecutarlas.

| Hallazgo | Resultado de la sonda de la IA |
|---|---|
| H-01 | 4300 nueves: `422`, `id: out_of_range`. 4301 nueves: `500` `internal_error` |
| H-02 | `company_name` y `contact_email` con `\ud800`: `500` `internal_error`. Un par de surrogates válido (un emoji) se acepta y se guarda. Un surrogate suelto en `tax_id`, `country` o `plan` responde `422` con el código de su campo, no `500` |
| H-03 | `POST /simulations?debug=1` con `{"customer_id":0}`: solo `debug: unknown_field`. `GET /customers/abc?x=1`: solo `x: unknown_field` |
| H-04 | `active_users` de 4300 dígitos: `422`, `out_of_range`. De 4301: `400` `malformed_request` |
| H-05 | `q=%00` devuelve los tres clientes. `q=zz%00` devuelve la lista vacía |
| H-06 | `q` de 101 caracteres seguido de `q=a`: `200`. En el orden inverso: `422`, `q: too_long` |
| H-07 | Cuerpo en UTF-16 y cuerpo en UTF-8 con BOM: `200` los dos |
| H-08 | Email con un espacio de no separación (U+00A0): `201`, guardado tal cual |
| H-09 | `/docs`, `/redoc` y `/docs/oauth2-redirect`: `200` con HTML. `/openapi.json?x=1` y `/docs?x=1`: `200` |
| H-10 | `access-control-allow-headers: Accept, Accept-Language, Content-Language, Content-Type` |
| H-11, H-12, H-13 | Leídos en el código: `app/repositories/customers.py` (la condición `? <> ''`), `app/repositories/simulations.py` (el `Any` sin comentario) y `tests/unit/test_customers.py` (el comentario) |
| H-14 | No ejecutado: es una ausencia, comprobada leyendo los tests |
| H-15 | Nombre de 2.000.000 de caracteres: `422`, `company_name: too_long` |
| A-01 | Clave desconocida con `\ud800` en `POST /customers` y en `POST /pricing/quote`: `500` `internal_error` |

## 3. Lo que esta respuesta no demuestra

- **Ninguna propuesta está probada**: no hay código ni tests nuevos. Que
  cada una funcione como se describe es una previsión de la IA.
- Las sondas de la IA se hicieron con el cliente de test, como las del
  evaluador; ninguna con un servidor real.
- En el fichero del informe, el ejemplo de H-08 dice llevar un espacio de
  no separación. El informe se guardó a partir del mensaje que devolvió el
  subagente, quitando solo la sangría que añade la herramienta a cada
  línea; la IA no puede asegurar que ese carácter se haya conservado y no
  haya quedado como un espacio corriente. El resto del texto es el que
  llegó.
- El informe dice que su modelo es Opus 5.5 (`claude-opus-5-5`). La
  definición del subagente (`.claude/agents/evaluador.md`) pide `model:
  opus`; la IA no tiene otra forma de comprobar qué modelo respondió.
- Los cinco «NO CUMPLE» del informe (SPEC-01/E-24, E-25 y E-30,
  SPEC-02/E-14 y SPEC-03/E-07) son casos límite fuera de las tablas de las
  specs. Hasta que el Tech Lead decida cada hallazgo, esos requisitos no
  pueden darse por cumplidos del todo.

## 4. Decisiones del Tech Lead

Pendientes. Esta tabla se rellena cuando decida cada hallazgo.

| Hallazgo | Decisión | Fecha |
|---|---|---|
| H-01 a H-15 y A-01 | — | — |
