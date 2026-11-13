# Limitaciones conocidas

Lo que el sistema no hace o hace de forma imperfecta, sabiéndolo. Cada fila
la ha visto y aceptado el Tech Lead; no son defectos por descubrir. Esta
lista es la fuente del apartado de limitaciones del `README.md` de la raíz,
que se escribirá cuando el proyecto pueda levantarse en local.

Los casos fiscales que no se modelan no están aquí: tienen su propio
documento, [ADR-008](../02-arquitectura/ADR-008-casos-fiscales-no-modelados.md).

| # | Limitación | Qué ocurre | Causa | Aceptada por el Tech Lead |
|---|---|---|---|---|
| L-01 | El cuerpo de una petición no tiene límite de tamaño | El backend lee entero cualquier cuerpo antes de comprobar que es un objeto JSON | No se ha puesto un tope en el guarda del cuerpo | 2026-11-13, al revisar el paso 1 del backend |
| L-02 | El OpenAPI publica los límites numéricos como decimales | `minimum` y `maximum` salen como `0.0` o `100000.0`, y el máximo de un identificador como `9.223372036854776e+18`, que no es el valor exacto (`9223372036854775807`). La validación sí usa el entero exacto: lo demuestran los tests de 2^63 − 1 (admitido) y 2^63 (`out_of_range`) | Lo genera así FastAPI 0.162.0; corregirlo exige retocar el documento generado. Afecta a SPEC-02/CA-10 | 2026-11-13, al revisar SPEC-02: el documento generado no se retoca |
| L-03 | Una clave repetida en el cuerpo JSON se acepta | Gana el último valor: `{"customer_id": 999, "customer_id": 2, …}` se trata como `customer_id` = 2. No se responde `400` ni `422` | Es lo que hace el analizador de JSON de Python. Comprobado a mano contra `POST /pricing/quote`; sin test | 2026-11-13, al revisar SPEC-02 |

## Cómo se añade una fila

Una limitación entra aquí cuando el Tech Lead la acepta como tal, con la
fecha. Si deja de serlo, la fila se tacha y se indica el commit que la
resuelve; no se borra.
