# ADR-008 · Casos fiscales que hoy no se modelan y cómo se abordarían

| | |
|---|---|
| **Estado** | `propuesto` (2026-11-13), pendiente de revisión del Tech Lead. **Nada de esto está implementado** |
| **Decide** | Tech Lead |
| **Afecta a** | A4, A5 · SPEC-02 (E-03, E-07); si se aplicara, también SPEC-01, SPEC-03 y SPEC-04 |

**Contexto.** Hoy el impuesto es siempre el tipo general de IVA del país del
cliente. La respuesta a la consulta (2026-11-13) lo da por suficiente y
valora que quede documentado cómo se abordarían la inversión del sujeto
pasivo y otros casos especiales. Esto es un diseño, no un cambio: la
herramienta presupuesta, no factura ni declara.

## 1. Cuándo aplica cada caso

Para un servicio prestado por vía electrónica. Las fuentes avisan de que
todas las reglas tienen excepciones.

| Quién compra | Tratamiento | Hoy | Fuente |
|---|---|---|---|
| Empresa de otro país de la UE | Sin IVA en la venta; lo paga el cliente al tipo de su país (inversión del sujeto pasivo) | **Distinto**: suma el IVA | [1] |
| Particular de otro país de la UE | IVA del país del cliente | Igual | [1] |
| Cliente del país de quien vende | IVA de ese país | Igual | No verificado |
| Cliente de fuera de la UE | Normalmente, sin IVA de la UE | **Distinto** | [1] |
| Empresa del Reino Unido | El IVA lo liquida ella (inversión del sujeto pasivo) | **Distinto**: suma el 20 % | [4] |
| Particular del Reino Unido | IVA británico; quien vende desde fuera se registra allí | Igual en importe | [5] |

## 2. Qué datos le faltan hoy al sistema

- **El país de quien vende**: distingue la venta interior de la
  transfronteriza. Sería configuración del backend, no un dato del cliente.
- **Si el cliente es empresa o particular**: campo nuevo del cliente.
- **Un identificador de IVA validado**, con la fecha y el resultado: sin él
  no se trata al cliente como empresa. En la UE se comprueba en VIES, y se
  recomienda conservar constancia [2]. Consultar VIES sería una dependencia
  externa nueva, con su propio ADR.

## 3. Cómo cambiaría cada pieza

- **Dominio**: la regla del impuesto pasa a ser una función pura que recibe
  el país de quien vende y los datos fiscales del cliente y devuelve **el
  tratamiento y el tipo** (`standard` con 2100, `reverse_charge` con 0,
  `outside_scope` con 0). El resultado de VIES entra como dato.
- **Esquema**: `simulations` guardaría el tratamiento y lo que lo decidió,
  igual que hoy guarda el tipo, porque el historial no se recalcula;
  `customers`, el tipo de cliente, el identificador de IVA y su validación.
- **Pantalla**: el alta pediría el tipo de cliente y el identificador de
  IVA; el simulador mostraría el tratamiento («IVA 0 %: inversión del sujeto
  pasivo»), porque un 0 por ese motivo no es un país sin impuesto.

## 4. Qué tests lo cubrirían

- Una tabla del dominio, una fila por cada fila del apartado 1: país de
  quien vende × país del cliente × empresa o particular × identificador
  validado o no, con el tratamiento y el tipo esperados.
- Un identificador sin validar, o VIES sin respuesta, nunca da inversión
  del sujeto pasivo. Para un particular de la UE, los importes de SPEC-02
  (5.2) no cambian.
- La simulación guarda el tratamiento, y el historial lo muestra aunque
  después cambien los datos fiscales del cliente.

## 5. Qué otros casos quedan fuera

- **IGIC (Canarias) e IPSI (Ceuta y Melilla)**: «España» aplica el 21 %. La
  tabla de la Comisión no incluye regiones como Canarias [3]; haría falta
  además el territorio del cliente. Qué tipo correspondería: no verificado.
- **Tipos reducidos**, y **ventas fuera de la UE** distintas del Reino
  Unido, que no está en la lista de países.
- **Obligaciones de quien vende** (registro, ventanilla única [6]): son de
  la declaración, no del presupuesto.

## Fuentes (consultadas el 2026-11-13) y lo no verificado

1. Comisión Europea, «Cross-border VAT» (revisada el 13/07/2026): <https://europa.eu/youreurope/business/taxation/vat/cross-border-vat/index_en.htm>
2. Comisión Europea, «Check a VAT number (VIES)» (18/06/2026): <https://europa.eu/youreurope/business/taxation/vat/check-vat-number-vies/index_en.htm>
3. Comisión Europea, «VAT rules and rates» (13/07/2026): <https://europa.eu/youreurope/business/taxation/vat/vat-rules-rates/index_en.htm>
4. HMRC, «VAT Notice 741A» (29/09/2022): <https://www.gov.uk/guidance/vat-place-of-supply-of-services-notice-741a>
5. HMRC, servicios digitales a consumidores (28/03/2022): <https://www.gov.uk/guidance/the-vat-rules-if-you-supply-digital-services-to-private-consumers>
6. Comisión Europea, «The One Stop Shop» (sin fecha visible): <https://vat-one-stop-shop.ec.europa.eu/one-stop-shop_en>

**No verificado**: los artículos de la Directiva 2006/112/CE (se leyeron las
páginas divulgativas, no el texto legal); que una suscripción SaaS sea a
efectos fiscales un servicio prestado por vía electrónica, que el apartado 1
da por hecho; la venta dentro del mismo país y cualquier fuente española
(las páginas de la Agencia Tributaria y del Gobierno de Canarias que se
intentaron leer devolvieron `404`); las excepciones que las fuentes anuncian
sin detallar. Nada de esto lo ha revisado un asesor fiscal.
