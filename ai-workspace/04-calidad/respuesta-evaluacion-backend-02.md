# Respuesta a la segunda pasada de la evaluación independiente del backend

| | |
|---|---|
| **Fecha** | 2026-11-13 |
| **Responde a** | [`evaluacion-backend-02.md`](evaluacion-backend-02.md), que queda intacto (commit `99aeec2`) |
| **Decide** | Tech Lead. Decidió los tres hallazgos nuevos, H-15 y un caso sin fila el 2026-11-13, tras revisar las correcciones y el informe (sesión 05, [`03-proceso/sesion-05.md`](../03-proceso/sesion-05.md)) |
| **Escribe** | IA (Claude Code) |
| **Estado del código** | El informe evaluó `eb0a27f`. Las decisiones están aplicadas, una por commit, hasta `bd7d269`. **No hay tercera pasada del evaluador**, por decisión del Tech Lead |

Procedimiento: el informe del evaluador no se modifica; se responde a cada
hallazgo. Esta respuesta se escribe después de decidir y de corregir, así
que recoge lo que se hizo, no una propuesta.

## 1. Qué dijo el informe

Sobre los 16 hallazgos de la primera evaluación (H-01 a H-15 y A-01):

- **12 corregidos**: H-01, H-02, A-01, H-03, H-05, H-07, H-08, H-09, H-10,
  H-11, H-12 y H-14.
- **3 conformes a lo decidido**: H-04 (L-05), H-06 (L-04) y H-15 (L-01).
- **1 sin veredicto posible**: H-13. Los comentarios están, pero el
  evaluador no puede saber si están todos sin leer la historia ni la
  bitácora, que su encargo excluye.
- **Ninguna regresión.**
- De los cinco requisitos que eran `NO CUMPLE`, dos pasan a `CUMPLE`
  (SPEC-01/E-24 y E-25) y tres siguen en `NO CUMPLE` por limitaciones
  aceptadas: SPEC-01/E-30 (L-04) y SPEC-02/E-14 y SPEC-03/E-07 (L-05).
- **Tres hallazgos nuevos**: N-01 (media), N-02 y N-03 (baja).

## 2. Respuesta por hallazgo

| Hallazgo | Grav. | ¿De acuerdo? | Qué comprobó la IA antes de tocar nada |
|---|---|---|---|
| N-01 · Un método no admitido sobre `/docs` o `/openapi.json` responde `500` | media | **Sí.** Defecto del código, y **anterior a la sesión 05**: no es una regresión. Al calcular la cabecera `Allow` del `405` se buscaba en la petición una ruta del contrato, y las páginas que publica el framework no la dejan (`KeyError: 'route'`). La primera evaluación no lo vio, y la IA tampoco | Las cinco peticiones del informe dan `500` con el código de `eb0a27f`. El mismo sondeo contra el código de `bda2c65`, extraído a una carpeta temporal fuera del repositorio, da los mismos `500`, y allí además `POST /redoc` |
| N-02 · Quedan `Any` sin comentario en su misma línea | baja | **Sí.** En `app/api/validation.py` y `app/api/contract.py` había funciones que usaban `Any` con el comentario puesto sobre otra función del fichero. El primer informe daba esos dos ficheros por buenos; los dos informes no midieron igual | Leído en el código: las líneas que cita el informe, y además las de dentro de las funciones que sí tenían el comentario encima |
| N-03 · Las limitaciones aceptadas y los casos nuevos del `400` no están en el contrato | baja | **Sí, en las dos partes.** (1) L-04 y L-05 solo estaban en `04-calidad/limitaciones-conocidas.md`. (2) Las reglas nuevas se escribieron en el índice, que es lo que pedía el encargo, pero el índice remite a la tabla 5.7 de SPEC-03 para sus casos de prueba, y esa tabla no cambió | Leído: ninguna spec nombraba `L-04` ni `L-05`, y la tabla 5.7 no tenía filas para el surrogate suelto, las codificaciones, `/redoc` ni `/docs?x=1` |
| H-13 · Sin veredicto | — | De acuerdo con que no es demostrable desde fuera. La lista de tests escritos después del código sale de lo que anotó la bitácora de la sesión 04 (r4, Y-12, Z-04, b2 y M-07) y de lo anotado en la sesión 05 | No hay nada más que comprobar: un test que pasara a la primera sin anotarse no tendría comentario |
| SPEC-01/E-30, SPEC-02/E-14 y SPEC-03/E-07 · Siguen en `NO CUMPLE` | — | De acuerdo con el hecho. Son las limitaciones L-04 y L-05, que el Tech Lead aceptó a sabiendas | — |
| Un `q` que solo lleva una marca diacrítica (U+0301) devuelve el listado inicial *(el informe lo anota sin contarlo como defecto)* | — | De acuerdo: es lo que dice SPEC-01 2.10, y ninguna fila lo fijaba. Es el caso Y-25 de la sesión 04 | Leído en el dominio: la forma de búsqueda queda vacía al quitar las marcas diacríticas |

Una cita del informe no cuadra y se deja como llegó: sitúa el cambio de
H-09 en `backend/app/main.py:223-226`, y ese fichero tiene 85 líneas.

## 3. Decisiones del Tech Lead

Decididas el 2026-11-13, a las 20:06, tras revisar las correcciones y el
informe. El Tech Lead dice haber comprobado contra un servidor real con
`uvicorn` que las sondas de H-01 a H-14 y A-01 dan lo decidido, que no hay
regresiones y que N-01 se reproduce (lo afirma él; la IA no lo ha visto).

| Hallazgo | Decisión del Tech Lead | Commit | Cómo se comprobó |
|---|---|---|---|
| N-01 | **Se corrige.** Un método no admitido sobre `/docs` o `/openapi.json` responde `405` `method_not_allowed`, con una cabecera `Allow` que dice los métodos que la ruta admite de verdad (`GET, HEAD`). Por qué: el índice dice ahora que esas rutas existen, y un `500` nunca es respuesta a una petición del cliente. Frase en «Documentación generada» del índice, con historial | `b5c468d` | **Rojo antes del código**, a las 20:08: las seis filas pedidas (`POST`, `PUT`, `DELETE` y `OPTIONS /docs`; `POST` y `DELETE /openapi.json`) fallan por aserción, `500 == 405`. Después, verde. Un test más comprueba que `HEAD` responde `200` en las dos, que es lo que dice `Allow`; pasó a la primera y está anotado |
| N-02 | **De acuerdo.** Cada `Any` que queda lleva su comentario en esa línea o un tipo concreto | `7cc5858` | Sin rojo: no cambia el comportamiento. Los errores de validación de Pydantic se anotan con su propio tipo y dejan de necesitar `Any`. Quedan dos, cada uno en un alias con el comentario en la misma línea. **Búsqueda al terminar** (apartado 4). `mypy --strict` y los tests, en verde |
| N-03 (1) | **De acuerdo.** Una nota en SPEC-01 junto a E-30 hacia L-04 y una en la fila del `400` del índice hacia L-05, con historial | `040eba3` | Solo documentación |
| N-03 (2) | **De acuerdo.** Seis filas nuevas en SPEC-03 5.7: el surrogate suelto, UTF-16 y UTF-32, UTF-8 con BOM, `/redoc` y `/docs/oauth2-redirect`, `/docs?x=1` y `/openapi.json?x=1`, y el `405` de N-01, con historial. Los tests que ya existían citan esas filas | `040eba3` | Solo documentación y docstrings de tests; ningún test cambia |
| H-15 | **Se mantiene L-01.** Se añade la medida y cómo se cerraría en producción: un límite en el proxy inverso | `aef612a` | Medido por la IA a las 20:15, con el cliente de test: un `company_name` de 2.000.000 de caracteres y uno de 20.000.000 se procesan enteros y responden `422` con `too_long` (0,3 y 2,1 segundos en el equipo de desarrollo); no se guarda nada |
| `q` con solo U+0301 | Se fija con una fila en SPEC-01 5.9 y un test, anotado como escrito después del código | `bd7d269` | Sin rojo, por decisión: el test fija lo que el código ya hace y pasó a la primera |
| H-13 | Sin decisión nueva | — | — |
| R-01 a R-23 | **Admitidas.** En R-09 vale la representación con `None` | — | — |
| V-08 a V-11 | El mensaje no las nombra: siguen sin aprobar | — | — |

Oráculo en verde antes de cada commit: 20 correctas, 0 con fallo y 4
inactivas (las del frontend). Al terminar: 741 tests del backend, `domain/`
al 100 % y 96 de 96 ramas.

## 4. La búsqueda de N-02

Líneas con la palabra `Any` en el código Python de `backend/` y `scripts/`
(sin el entorno virtual), a las 20:13 sobre el commit `7cc5858`:

| Fichero y línea | Qué es |
|---|---|
| `backend/app/api/contract.py:7` | `from typing import Any` |
| `backend/app/api/contract.py:15` | El alias del objeto de un documento OpenAPI, **con su comentario en esa línea** |
| `backend/app/api/problems.py:11` | `from typing import Any` |
| `backend/app/api/problems.py:162` | El alias del parámetro `responses` de FastAPI, **con su comentario en esa línea** |
| `backend/tests/unit/test_tax_id_differential.py:7` | La palabra inglesa, dentro de un docstring |
| `scripts/hooks/pre_tool_use.py:12` | La palabra inglesa, dentro de un docstring |

No queda ningún uso de `Any` sin su comentario en la misma línea. El
frontend no existe todavía: allí lo comprobará ESLint cuando exista.

## 5. Lo que esta respuesta no demuestra

- **No hay una comprobación independiente de estas cinco correcciones**: el
  Tech Lead decidió que no hace falta una tercera pasada. Lo que hay son
  los tests y las comprobaciones de la IA sobre su propio código.
- Nada de esta respuesta se ha probado con un servidor real: todo es con el
  cliente de test. Que N-01 da `405` con `uvicorn` no lo ha visto la IA.
- La cabecera `Allow` de `/docs` y `/openapi.json` sale de lo que el
  framework dice de sus propias rutas, con la versión fijada. Un test fija
  su valor (`GET, HEAD`) y que `HEAD` responde `200`; si una versión nueva
  lo cambia, el test falla.
- Los tiempos de H-15 son de una sola ejecución en el equipo de desarrollo
  y con el cliente de test; valen como orden de magnitud.
- Tres requisitos siguen en `NO CUMPLE` en sus casos límite (SPEC-01/E-30,
  SPEC-02/E-14 y SPEC-03/E-07), por las limitaciones L-04 y L-05. Ahora las
  specs lo dicen.
