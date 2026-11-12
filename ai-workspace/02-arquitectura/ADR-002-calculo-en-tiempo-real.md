# ADR-002 · Dónde se calcula la proyección en tiempo real

| | |
|---|---|
| **Estado** | `aceptado` (2026-11-12) |
| **Decide** | Tech Lead |
| **Requisitos** | R-06, R-07, R-12 |
| **Supuestos** | A8, A9 |

## Contexto

El simulador tiene un control para el número de usuarios y debe mostrar al
momento la factura mensual prevista: tramos, impuesto y total, en la divisa
elegida. Aparte, guardar una simulación debe persistir ese mismo cálculo.

Hay dos cosas distintas bajo «tiempo real»:

- **El importe** (tramos e impuesto) es una regla de negocio.
- **La divisa** es presentación: el mismo importe en euros visto con otro
  tipo de cambio.

La pregunta es dónde vive la regla de negocio cuando la interfaz necesita el
resultado en cada movimiento del control.

## Opciones

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **El backend calcula siempre.** `POST /pricing/quote` devuelve el cálculo sin guardarlo; el frontend lo llama con una espera corta y cancela la petición anterior | Una sola implementación de la tarifa. El precio lo fija el servidor. Cambiar una tarifa es tocar un sitio | Una petición por cambio de valor. Hay que gestionar estados de carga y error |
| B | El frontend calcula con su propia copia de la tarifa | Respuesta instantánea y sin red | Dos implementaciones, en dos lenguajes, que pueden divergir. El importe en pantalla puede no coincidir con el guardado |
| C | El frontend calcula y el backend recalcula al guardar | Respuesta instantánea y guardado fiable | La lógica sigue duplicada. Para que no diverja hacen falta vectores de prueba compartidos y disciplina permanente |
| D | El backend sirve la tabla de tarifas y el frontend aplica un motor genérico de tramos | Tarifa configurable desde un sitio | El algoritmo (tramos, impuesto, redondeo) sigue en dos sitios. Es la opción más compleja |

## Decisión

**Opción A: el backend es la única fuente del cálculo.**

- `POST /pricing/quote` calcula y devuelve el desglose sin persistir nada.
- `POST /simulations` usa la misma función del dominio y guarda el resultado.
- El frontend no contiene la tarifa ni los tipos impositivos.
- Al mover el control, el frontend espera 200 ms sin cambios antes de
  pedir (*debounce*) y, si llega un valor nuevo, cancela la petición en curso
  para que una respuesta antigua nunca pise a una más reciente.
- **Todo se calcula y se guarda en EUR.** La conversión a otra divisa la hace
  el frontend solo para mostrar, con tipos de cambio que obtiene directamente
  de la API pública (A8), y nunca se persiste.

## Por qué

1. **Una sola fuente de verdad.** Con B, C o D la tarifa existe en Python y
   en TypeScript. El día que cambie un precio, alguien tiene que acordarse de
   cambiarlo dos veces; el fallo típico es que la pantalla enseñe un importe
   y se guarde otro.
2. **El precio es autoritativo.** Un importe que se presenta a un cliente no
   debería poder alterarse desde el navegador.
3. **El coste es pequeño y conocido.** Una petición ligera por cada pausa del
   usuario, no por cada píxel del control. En local la latencia debería ser
   imperceptible; no está medida todavía.
4. **Separar importe y divisa** mantiene estable lo guardado: una simulación
   no cambia de valor porque cambie el tipo de cambio del día.

## Consecuencias

A favor:

- El frontend queda más simple: pide, muestra y convierte para presentar.
- Los tests exhaustivos de la tarifa viven en un solo sitio (SPEC-02).
- Se puede comprobar con un test que la cifra proyectada y la guardada son
  idénticas (SPEC-02, CA-08).

En contra, y cómo se trata:

| Consecuencia | Tratamiento |
|---|---|
| La proyección depende de la red | La interfaz muestra estados de carga y de error; un fallo no deja el importe anterior como si fuera válido. El detalle va en SPEC-04 |
| Más peticiones al backend | *Debounce* y cancelación de la petición anterior |
| No se puede proyectar sin conexión | Aceptado: es una herramienta interna que ya depende del backend para todo lo demás |
| La conversión de divisa usa coma flotante en el navegador | Aceptado: es solo presentación, se redondea al mostrar y no se guarda |

## Cuándo habría que revisarla

- Si la proyección tuviera que funcionar sin conexión.
- Si la latencia medida hiciera incómodo el control. La salida natural sería
  la opción C con vectores de prueba compartidos, no la B.
