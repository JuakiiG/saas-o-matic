# Especificaciones

Cada spec define qué debe hacer una parte del sistema antes de escribir su
código. No se programa una parte hasta que su spec está `aprobada`.

## Índice

| Spec | Ámbito | Requisitos | Supuestos de los que depende | Estado |
|---|---|---|---|---|
| [SPEC-01](SPEC-01-clientes-y-validacion-fiscal.md) | Clientes y validación fiscal | R-03, R-04, R-10, R-11 | A2, A4, A10, A11, A12, A13, A14, A18 | `borrador` (2026-11-12) |
| [SPEC-02](SPEC-02-tarificacion-e-impuestos.md) | Tarificación e impuestos | R-06, R-07, R-12 | A2, A3, A4, A5, A6, A7, A9 | `borrador` (2026-11-12) |
| [SPEC-03](SPEC-03-simulaciones-y-persistencia.md) | Simulaciones y persistencia | R-05, R-11 | A3, A6, A7, A9, A13, A14, A18 | `borrador` (2026-11-12) |
| [SPEC-04](SPEC-04-frontend-y-divisas.md) | Frontend y divisas | R-09 a R-12, R-17 | A8, A9, A13, A14, A16, A17 | `borrador` (2026-11-12) |

Una spec no puede pasar a `aprobada` mientras dependa de un supuesto que no
esté `decidido` (ver [`supuestos.md`](../00-analisis/supuestos.md)).

**Fecha límite de los supuestos pendientes de confirmar (A2 a A5)**: si el
viernes 13 de noviembre de 2026 a las 10:00 no hay respuesta, el Tech Lead
los decide con la hipótesis ya documentada y pasan a
`decidido (sin confirmación externa)`, revisables si la respuesta llega
después. *Por qué: una consulta sin contestar no puede bloquear el
desarrollo de forma indefinida.*

## Ciclo de vida

| Estado | Significado |
|---|---|
| `borrador` | Redactada por la IA; se puede discutir y cambiar. No autoriza a programar |
| `aprobada` (fecha) | Firmada por el Tech Lead. Autoriza a programar esa parte |

Un cambio en una spec aprobada se anota en su historial, con fecha y motivo,
y vuelve a pasar por aprobación.

## Formato de los requisitos (EARS)

Cada requisito es una sola frase comprobable, con identificador propio
(`SPEC-02/E-03`), y sigue uno de estos patrones:

| Patrón | Forma |
|---|---|
| Ubicuo | «El sistema deberá…» |
| Por evento | «Cuando *ocurre algo*, el sistema deberá…» |
| Por estado | «Mientras *se da una condición*, el sistema deberá…» |
| Comportamiento no deseado | «Si *ocurre algo indebido*, entonces el sistema deberá…» |

Los criterios de aceptación (`CA-xx`) dicen cómo se demuestra que los
requisitos se cumplen. Cada test cita el requisito que comprueba.

## Convenciones comunes de la API

Valen para todas las specs, que solo detallan lo que les es propio.

- **Formato**: JSON, con nombres de campo en inglés y `snake_case`.
- **Dinero**: enteros en céntimos de euro, en campos acabados en `_cents`.
  Nunca decimales (A6).
- **Tipos impositivos**: enteros en puntos básicos, en campos acabados en
  `_bp` (21 % = `2100`).
- **Campos desconocidos**: una petición con un campo no documentado se
  rechaza; no se ignora en silencio.
- **Errores**: `application/problem+json` (RFC 9457) con esta forma (A14):

  ```json
  {
    "type": "about:blank",
    "title": "Unprocessable Content",
    "status": 422,
    "code": "validation_error",
    "detail": "La petición contiene datos no válidos.",
    "errors": [
      {
        "field": "active_users",
        "code": "out_of_range",
        "message": "Debe estar entre 0 y 100000."
      }
    ]
  }
  ```

  `code` es estable y forma parte del contrato; `detail` y `message` son
  texto en español para mostrar y pueden cambiar. `errors` solo aparece en
  los errores de validación.
