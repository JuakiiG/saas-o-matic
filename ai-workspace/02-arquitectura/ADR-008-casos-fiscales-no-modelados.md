# ADR-008 · Casos fiscales que hoy no se modelan y cómo se abordarían

| | |
|---|---|
| **Estado** | `aceptado` (2026-11-13). **Nada de esto está implementado** |
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
| Particular de otro país de la UE, si quien vende supera el umbral de 10.000 € (ver abajo) | IVA del país del cliente | Igual | [1] [6] |
| Particular de otro país de la UE, si quien vende no lo supera | IVA del país de **quien vende**, salvo que haya optado por la regla general | **Distinto**: suma siempre el IVA del país del cliente | [6] [8] |
| Cliente del país de quien vende | IVA de ese país | Igual | No verificado |
| Cliente de fuera de la UE | Normalmente, sin IVA de la UE | **Distinto** | [1] |
| Empresa del Reino Unido | El IVA lo liquida ella (inversión del sujeto pasivo) | **Distinto**: suma el 20 % | [4] |
| Particular del Reino Unido | IVA británico; quien vende desde fuera se registra allí | Igual en importe | [5] |

**El umbral de 10.000 €** [6]. Desde el 1 de enero de 2019, los servicios
prestados por vía electrónica a particulares de otros Estados miembros
tributan en el Estado de quien vende mientras se cumplan tres condiciones:

- quien vende está establecido en **un solo** Estado miembro;
- presta esos servicios a particulares de otro Estado miembro; y
- el total de esas ventas, sin IVA, no supera 10.000 € ni en el año en curso
  ni en el anterior. Desde el 1 de julio de 2021 el umbral suma también las
  ventas a distancia de bienes dentro de la UE: no se cuenta por separado.

En cuanto se supera, se aplica la regla general (IVA del país del cliente)
sin excepción. Quien no lo supera puede optar por la regla general, y queda
obligado por esa opción dos años naturales. Las mismas condiciones están en
el artículo 59c de la Directiva [8].

## 2. Qué datos le faltan hoy al sistema

- **El país de quien vende**: distingue la venta interior de la
  transfronteriza. Sería configuración del backend, no un dato del cliente.
- **Si quien vende supera el umbral de 10.000 €**, o si ha optado por la
  regla general: decide qué IVA paga un particular de otro país de la UE.
  También sería configuración del backend; el sistema no conoce las ventas
  anuales de quien vende.
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
  del sujeto pasivo. Para un particular de la UE y un vendedor por encima
  del umbral, los importes de SPEC-02 (5.2) no cambian.
- Por debajo del umbral, un particular de otro país de la UE paga el tipo
  del país de quien vende; con la opción por la regla general, el del suyo.
- La simulación guarda el tratamiento, y el historial lo muestra aunque
  después cambien los datos fiscales del cliente.

## 5. Qué otros casos quedan fuera

- **Canarias, Ceuta y Melilla están fuera del territorio del IVA de la UE.**
  La Directiva no se aplica en ellas (artículo 6 [8]): Canarias figura entre
  los territorios que sí forman parte del territorio aduanero de la Unión,
  y Ceuta y Melilla, entre los que no. La tabla de la Comisión [7] dice lo
  mismo: en las tres, «VAT rules apply: no»; las normas aduaneras se
  aplican en Canarias y no en Ceuta ni en Melilla. Hoy «España» aplica el
  21 % a cualquier cliente español; para distinguirlos haría falta el
  territorio del cliente, no solo el país. **No verificado**: qué impuesto
  se aplica allí en su lugar (se conocen como IGIC en Canarias e IPSI en
  Ceuta y Melilla) y a qué tipo; no se ha podido leer ninguna fuente
  española.
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
7. Comisión Europea, «Territorial Scope» (modificada el 13/08/2026): <https://taxation-customs.ec.europa.eu/taxation/vat/vat-directive/how-does-vat-work/territorial-scope_en>
8. Directiva 2006/112/CE, artículos 6 y 59c, leídos en el documento de trabajo de la Comisión «VAT Directive, including all amendments already adopted» (10/07/2018): <https://taxation-customs.ec.europa.eu/system/files/2018-07/vat_directive_with_details_for_the_definitive_system_en.pdf>

**No verificado**: el texto consolidado vigente de la Directiva 2006/112/CE.
Los artículos 6 y 59c se leyeron en [8], un documento de trabajo de 2018
que advierte de que es solo informativo; EUR-Lex respondió `202` sin
contenido a todas las peticiones, y el resto de artículos no se ha leído
(solo las páginas divulgativas). Tampoco: que una suscripción SaaS sea a
efectos fiscales un servicio prestado por vía electrónica, que el apartado 1
da por hecho; la venta dentro del mismo país y cualquier fuente española
(las páginas de la Agencia Tributaria y del Gobierno de Canarias que se
intentaron leer devolvieron `404`); las excepciones que las fuentes anuncian
sin detallar. Nada de esto lo ha revisado un asesor fiscal.

## Historial

| Fecha | Cambio |
|---|---|
| 2026-11-13 | Propuesto por la IA, a raíz de la respuesta a la consulta |
| 2026-11-13 | Aceptado por el Tech Lead con dos añadidos: el umbral de 10.000 € de las ventas a particulares de otros países de la UE, que divide en dos la fila del apartado 1 y añade un dato al apartado 2 y un test al 4; y Canarias, Ceuta y Melilla, fuera del territorio del IVA, con fuente oficial (apartado 5). Fuentes [7] y [8] nuevas |
