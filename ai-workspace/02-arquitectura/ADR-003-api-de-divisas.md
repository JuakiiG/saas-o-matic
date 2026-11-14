# ADR-003 · API pública de tipos de cambio

| | |
|---|---|
| **Estado** | `aceptado` (2026-11-12) |
| **Decide** | Tech Lead |
| **Requisitos** | R-09, R-17 |
| **Supuestos** | A8 |
| **Specs** | SPEC-04 (D-01, D-02) |

## Contexto

La interfaz debe mostrar los importes en otras divisas con tipos de cambio
obtenidos de una API pública (R-09). A8 fija que la llamada la hace el
frontend directamente, que todo se calcula y se guarda en EUR y que la
conversión es solo de presentación.

Lo que pesa en la elección:

- La llamada sale del navegador: la API no puede exigir una clave, porque
  una clave en un frontend es pública, y tiene que admitir peticiones de
  otro origen (CORS).
- Solo hacen falta los tipos de EUR a tres divisas (USD, GBP y CHF).
- Es una dependencia de un tercero: el fallo tiene que estar previsto
  (R-17).

## Opciones

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **Frankfurter, versión `v2`** (`/v2/rates?base=EUR&quotes=USD,GBP,CHF`) | Sin clave ni registro; sin cuota diaria ni mensual; es la versión vigente; admite cualquier origen; una sola petición para las tres divisas | Servicio de un tercero sin garantía de disponibilidad; agrega varias fuentes, así que cada tipo trae su propia fecha |
| B | Frankfurter, versión `v1` (`/v1/latest`) | Lo mismo, con una respuesta algo más simple (un objeto con un mapa de tipos) | La propia API la declara obsoleta en favor de la `v2` |
| C | Una API pública que exija clave | Más oferta donde elegir | La clave quedaría expuesta en el navegador; para ocultarla habría que pasar por el backend, en contra de A8 |
| D | Pasar la llamada por el backend | Aísla el fallo del tercero y permitiría guardar los tipos | A8 lo descarta: el encargo dice que es la interfaz la que conecta |

## Decisión

**Opción A: Frankfurter `v2`.**

- Petición: `GET https://api.frankfurter.dev/v2/rates?base=EUR&quotes=USD,GBP,CHF`,
  una vez al arrancar la aplicación.
- Respuesta: una lista con un objeto `{date, base, quote, rate}` por divisa.
- La respuesta se valida antes de usarla y cualquier fallo deja la interfaz
  en EUR, con aviso y reintento. El detalle está en SPEC-04 (2.6 y 5.2).
- La URL está en los ficheros de entorno del frontend, no en el código.

## Por qué

1. **Un proyecto nuevo no nace dependiendo de algo obsoleto.** La `v1`
   funciona hoy, pero su propia documentación la da por sustituida. Es el
   motivo por el que el Tech Lead descartó la opción B, que la IA había
   propuesto por ser la única cuya respuesta había verificado.
2. **Sin clave**, que es la única forma de cumplir A8 sin exponer un
   secreto.
3. **CORS abierto**, comprobado, así que el navegador puede llamarla.

## Verificación

Hecha el 2026-11-12.

| Qué | Cómo | Resultado |
|---|---|---|
| Sin clave, sin cuotas; la `v1` declarada obsoleta | Lectura de <https://frankfurter.dev/> | Confirmado |
| Forma de la respuesta de la `v2` | `curl` a la petición de arriba, a las 14:53 | `200`, `application/json`; lista de tres objetos con fecha 2026-11-12 (CHF 0,92316, GBP 0,83583, USD 1,1139) |
| CORS | `curl` con la cabecera `Origin: http://localhost:4200`, a la `v2` y a la `v1` | `access-control-allow-origin: *` y `access-control-allow-methods: GET, OPTIONS` en las dos. Lo comprobó también el Tech Lead |
| Divisa inexistente | `curl` con `quotes=XXX` | `422` con `{"status":422,"message":"invalid currency: XXX"}` |
| Caché | Cabeceras de la misma respuesta | `cache-control: public, max-age=36362` |

**Repetida el 2026-11-14, sábado, a las 09:29**, antes de aprobar SPEC-04,
con `curl` y la cabecera `Origin: http://localhost:4200`. La decisión no
cambia.

| Qué | Resultado |
|---|---|
| Forma de la respuesta de la `v2` | `200`, `application/json; charset=utf-8`; la misma lista de tres objetos, con fecha 2026-11-14 (CHF 0,92491, GBP 0,83559, USD 1,1083) |
| CORS | `access-control-allow-origin: *` y `access-control-allow-methods: GET, OPTIONS`, como el día 12; una comprobación previa `OPTIONS` responde `200` con las mismas cabeceras |
| Divisa inexistente | El mismo `422` |
| Caché | `cache-control: public, max-age=55805, stale-if-error=86400` |
| Fin de semana | En sábado la `v2` responde igual, y los tres tipos traen la fecha de ese mismo día |
| La `v1` | Responde `200` con fecha 2026-11-13 y una cabecera `deprecation` |

**No verificado**: la llamada desde un navegador real; el límite de
peticiones por segundo, que la documentación no declara; el comportamiento
en festivos (en fin de semana, solo se ha visto un sábado); que los tres
tipos traigan siempre la misma fecha.

## Consecuencias

A favor:

- Ningún secreto en el repo ni en el navegador.
- Una petición por sesión; cambiar de divisa no usa la red.

En contra, y cómo se trata:

| Consecuencia | Tratamiento |
|---|---|
| La disponibilidad depende de un tercero | Con EUR la aplicación no depende de la API; si falla, aviso, importes en EUR y reintento (SPEC-04, E-28 y E-30) |
| La forma de la respuesta puede cambiar | Se valida entera antes de usarla; una respuesta que no cumple se trata como error (SPEC-04, 2.6) |
| Los tipos son de referencia y pueden ser de un día anterior | Se muestra la fecha de cada tipo y se avisa de que los importes convertidos son orientativos |
| Las pruebas no pueden depender de la red | Los tests simulan la respuesta; la prueba de principio a fin la intercepta (SPEC-04, CA-02 y CA-14) |

## Cuándo habría que revisarla

- Si la API empezara a exigir clave o cerrara CORS: la salida sería la
  opción D, que obliga a revisar A8.
- Si retirara la `v2` o cambiara su respuesta.
