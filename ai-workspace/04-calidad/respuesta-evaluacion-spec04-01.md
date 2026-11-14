# Respuesta a la evaluación independiente de SPEC-04

| | |
|---|---|
| **Fecha** | 2026-11-14 |
| **Responde a** | [`evaluacion-spec04-01.md`](evaluacion-spec04-01.md), que queda intacto (commit `e03fc80`) |
| **Decide** | Tech Lead. **Ningún hallazgo está decidido**: la columna «Qué propone la IA» es una propuesta y **no se ha aplicado ninguna** |
| **Escribe** | IA (Claude Code) |
| **Estado de la spec** | SPEC-04 está como la evaluó el informe (`86b2a96`, dentro de `8516f5c`), en `borrador` y sin ninguna corrección posterior |

Procedimiento: el informe del evaluador no se modifica; se responde a cada
hallazgo. Antes de responder, la IA ha repetido por su cuenta lo que cada
hallazgo afirma (apartado 2). **Los 12 hallazgos se reproducen** tal como
el informe los describe.

Resumen de la respuesta:

- **De acuerdo, lo introdujo la IA hoy** al poner la spec al día (8): H-03,
  H-04, H-06, H-07, H-08, H-10, H-11 y H-12.
- **De acuerdo, estaba en la spec desde el día 12** y ninguna revisión
  anterior lo vio (4): H-01, H-02, H-05 y H-09.
- **En desacuerdo**: ninguno.
- **Tres casos más**, que el informe trae fuera de sus hallazgos o que
  salen de leerlo: filas A-01 a A-03 (apartado 3).
- **Decisiones que no son de redacción** y piden al Tech Lead elegir entre
  alternativas: H-01 (cómo se formatea un importe en EUR sin coma
  flotante), H-06 (qué se muestra con un `422` del cliente), H-09 (tres
  detalles de presentación) y H-12 (si decide el texto o el número).

## 1. Respuesta por hallazgo

| Hallazgo | Grav. | ¿De acuerdo? | Qué propone la IA | Qué habría que tocar |
|---|---|---|---|---|
| H-01 · Formatear un importe en EUR obliga a usar coma flotante | media | **Sí.** 2.6 dice desde el día 12 que con EUR «el importe sale exacto de los céntimos» y no dice cómo; lo directo es dividir entre 100, que es justo lo que la regla del dinero prohíbe fuera de la conversión | **Recomendada**: formatear el EUR solo con enteros. Los euros son `(céntimos − céntimos % 100) / 100`, una división exacta, y los céntimos, el resto; se formatean los euros con `Intl.NumberFormat` por partes (`formatToParts`) y la parte decimal se sustituye por los céntimos con dos cifras. Comprobado con Node: da el mismo texto que dividir entre 100 en 8.645.796 valores, de 0 a 60520570 en pasos de 7, y en las celdas de EUR de 5.1. La regla del dinero no cambia. **Alternativa 1**: escribir que dividir entre 100 para mostrar entra en la excepción; cambia `CLAUDE.md`, `.claude/rules/frontend.md` y ADR-002. **Alternativa 2**: pasar el texto exacto (`'169.40'`) a `format`, que funciona en ejecución pero obliga a declarar la biblioteca ES2023 en `tsconfig.json`, fuera de la configuración por defecto del CLI | Recomendada: una frase en SPEC-04 2.6 y una fila en 5.1 (5 céntimos, `0,05 EUR`), con historial. Las alternativas: además, los documentos citados |
| H-02 · Requisitos citados por un criterio sin ningún caso | media | **Sí.** E-03, E-05, E-21, E-23 y E-35 en el alta no tienen fila en el apartado 5; CA-04, CA-05 y CA-08 dicen reproducir «cada fila» y no los alcanzan | Filas nuevas, sin cambiar ningún requisito. 5.3: una respuesta con tres clientes en un orden que no es el alfabético se muestra en ese orden. 5.4: los desplegables ofrecen exactamente los nueve países y los tres planes del ejemplo de SPEC-01 4.4, con sus nombres y en su orden. 5.5: con una proyección en curso, los importes anteriores se ven marcados como «actualizando» y «Guardar» está desactivado; y con un guardado en curso, «Guardar» está desactivado y un segundo clic no hace otra petición | SPEC-04 5.3, 5.4 y 5.5, con historial |
| H-03 · U+FFFD sí puede coincidir con un cliente | baja | **Sí. Error de la IA de hoy**: afirmó que U+FFFD «no coincide con ningún cliente» sin sondearlo. El backend admite ese carácter en un nombre y el buscador lo encuentra | Quitar esa frase de 2.2. La regla (sustituir el *surrogate* suelto antes de enviar) y la fila de 5.3 no cambian: se muestra lo que devuelve la API | Una frase de SPEC-04 2.2, con historial |
| H-04 · 4.1 no recoge el `422` del buscador | baja | **Sí. Error de la IA de hoy**: la columna dice que recoge lo que declara el OpenAPI y la fila del buscador omite el `422`, que la IA explicó en el párrafo de debajo en vez de ponerlo en la fila | Añadir el `422` a la fila, con la nota de que el frontend no debería provocarlo (2.2) | La fila de `GET /customers?q=` de SPEC-04 4.1, con historial |
| H-05 · CA-01 cita E-27, que un test del *pipe* no demuestra | baja | **Sí.** Está así desde el día 12 | CA-01 pasa a citar solo E-28; CA-02 y CA-08, que son los que tienen las filas del cambio de divisa, añaden E-27 | Tres celdas de la tabla de SPEC-04 6, con historial |
| H-06 · El `422` del cliente no puede darse con el filtro, y choca con 2.7 | baja | **Sí. Incoherencia de la IA de hoy**: al escribir el filtro del `id` dejó la rama del `422` del día 12, y la tabla de 2.7 trata un `422` que el frontend no debería provocar como error inesperado | **Recomendada**: quitar la rama. Con el filtro, un `422` de `GET /customers/{id}` solo puede venir de un defecto del frontend (sondeado: un parámetro de más da `422` con `unknown_field`), y se muestra como error inesperado, igual que el del buscador. «Cliente no encontrado» queda para dos casos: el `id` no pasa el filtro, o `404` con `customer_not_found`. **Alternativa**: dejar la rama como defensa y decirlo en 2.7 como excepción | Recomendada: SPEC-04 2.4, 2.5, 2.7, E-15, la fila de 5.7 y CA-17, con historial |
| H-07 · La regla de 2.1 no excluye el `0` | baja | **Sí. Redacción de la IA de hoy**: «sin ceros a la izquierda» no descarta el `0` solo, y los casos esperan que no se pida | Decirlo sin ambigüedad: «de 1 a 16 dígitos ASCII, el primero distinto de `0`» | Una frase de SPEC-04 2.1, con historial |
| H-08 · E-50 no dice qué pasa con la búsqueda en curso | baja | **Sí. Hueco de la IA de hoy** | Al superar el límite se cancela la petición en curso, para que su respuesta no pinte la lista que se acaba de retirar, y el aviso sale al momento, sin esperar los 300 ms, porque no hay petición que agrupar. Una fila en 5.3 | SPEC-04 2.2, E-50 y 5.3, con historial |
| H-09 · Tres detalles de presentación sin fijar | baja | **Sí.** Los tres están así desde el día 12. Comprobado con Node: el formato por defecto de `es-ES` da `1,114` y `0,923` para los tipos, y `1234,50 EUR` sin punto de millar | **Los decide el Tech Lead.** Recomendación: (1) el tipo de cambio se muestra con los decimales que trae, hasta 6 (con ese máximo salen `1,1139` y `0,92316`); (2) los importes de cuatro cifras se dejan como los da `es-ES`, sin punto de millar, y se añade a 5.1 una fila que lo fije (`123450` → `1234,50 EUR`); la alternativa, forzar el punto, usa una opción que la biblioteca ES2022 no declara; (3) los tramos se rotulan «del 1 al 10», «del 11 al 50» y «del 51 en adelante», como la tabla de SPEC-02 2.1 | SPEC-04 2.6, 2.8 y 5.1, con historial |
| H-10 · D-13 no recoge la comprobación del *surrogate* | baja | **Sí. Descuido de la IA de hoy**: amplió 2.3 y E-45 y no llevó el cambio entero a D-13 | Añadirlo a D-13. **Aviso**: D-13 es una decisión que el Tech Lead dio por buena el día 12, y la IA ya cambió hoy su texto (precisión S-02 de la bitácora); lo que diga al final lo decide él | La fila D-13 de SPEC-04 7 |
| H-11 · La remisión de 5.7 a SPEC-01 5.10 está incompleta | baja | **Sí. Frase de la IA de hoy**: cinco de los textos de 5.7 no están en SPEC-01 5.10 | Corregir la frase de SPEC-04: lo que responde el backend está en SPEC-01 5.10 para los textos que esa tabla recoge; los demás (`1e0`, U+0661 y los tres números grandes) se sondearon el 2026-11-14, con su resultado. **No se propone tocar SPEC-01**, que está cerrada | Una frase de SPEC-04 5.7, con historial |
| H-12 · No se dice si decide el texto o el número | baja | **Sí. Definición de la IA de hoy**: `Number.isInteger` sobre el valor da por entero `100000.000000000001` y `1e3` (comprobado con Node) | **Lo decide el Tech Lead.** **Recomendada**: decide el texto. Válido es un texto formado solo por dígitos ASCII cuyo valor está dentro de los límites; `1e3`, `15.0`, `1,5`, `-1` y el campo vacío no lo son. Consecuencia: el campo tiene que dar acceso al texto escrito, así que no puede ser un control numérico del navegador, que solo entrega el número; y la fila de `15.0` que la IA añadió hoy a 5.5 pasa a ser un error junto al campo. **Alternativa**: decide el número, como está, añadiendo a 5.5 las filas de `1e3` y del decimal largo para fijarlo | SPEC-04 2.5, E-22, E-36, E-49 y 5.5, con historial |

## 2. Lo que la IA ha comprobado

Con el cliente de test y una base de datos en la carpeta temporal, con
Node 24.18.0 y leyendo el paquete publicado `@angular/common` 21.2.26, a
las 10:17 y las 10:18. Nada del repositorio cambia.

| Hallazgo | Comprobación | Resultado |
|---|---|---|
| H-01 | Node: el formato por partes con enteros frente a dividir entre 100 | 8.645.796 valores, ninguna discrepancia; `169,40 EUR`, `605.205,70 EUR` y `0,05 EUR`. Pasar el texto `'169.40'` a `format` funciona en ejecución. **No comprobado por la IA**: lo que declaran las bibliotecas de tipos de TypeScript (lo dice el informe) |
| H-02 | Lectura de 5.3, 5.4 y 5.5 | Ninguna fila para esos cinco requisitos |
| H-03 | Alta con un nombre que lleva U+FFFD y búsqueda de ese texto | `201`, y la búsqueda devuelve ese cliente |
| H-04 | El `/openapi.json` volcado a las 09:29 | `GET /customers` declara 200, 422 y 503 |
| H-05 | Lectura de la tabla de criterios | CA-01 cita E-27 y E-28; CA-02, E-26 y E-30 |
| H-06 | `GET /customers/7?x=1` | `422` con `x: unknown_field` |
| H-07, H-08, H-10 | Lectura de 2.1, 2.2 y D-13 | Como dice el informe |
| H-09 | Node: formato del tipo y de un importe de cuatro cifras | `1,114` y `0,923` por defecto, `1,1139` y `0,92316` con seis decimales como máximo; `1234,50 EUR` y `12.345,00 EUR` |
| H-11 | Búsqueda en SPEC-01 5.10 | Ninguna fila con `1e0`, 9007199254740991 ni 9007199254740993 |
| H-12 | Node | `Number('100000.000000000001')` vale 100000 y es entero; una expresión de solo dígitos rechaza ese texto y `1e3` |

## 3. Tres casos más

| # | Caso | De dónde sale | Qué propone la IA |
|---|---|---|---|
| A-01 | **CA-18 no puede comprobarse como está escrito.** Pide comprobar que las peticiones «no llevan más cabeceras que `Accept` y `Content-Type`», pero Angular añade esas dos al enviar, no en la petición que ve un test: con las utilidades de test de `HttpClient`, las cabeceras de la petición salen vacías | Apartado 4 del informe, fuera de sus hallazgos. La IA lo ha leído en el paquete publicado (el código que escribe `Accept` y `Content-Type` está en el envío); no lo ha ejecutado | Partir el criterio: el test de `core/` comprueba que la petición no lleva ninguna cabecera propia, y la prueba de principio a fin con Playwright (CA-14), que las peticiones reales al backend solo llevan las que el navegador y Angular ponen. Tocaría CA-18 y CA-14 |
| A-02 | **El informe no da veredicto a E-42 ni a E-43**, los dos requisitos nuevos de los errores genéricos: su tabla pasa de E-41 a E-44. Tiene 50 filas de requisitos y 39 `CONFORME`; el resumen dice 52 y 41. Las filas de 5.6, que los cubren, sí las da por construibles (CA-16) | Recuento de la IA sobre el informe guardado | Lo decide el Tech Lead: darlo por bueno con CA-16, o pedir al evaluador esas dos filas. El informe se queda como llegó |
| A-03 | En la tabla del informe, las filas sin caso de prueba remiten a «H-04», y el hallazgo que las describe es el **H-02**; el H-04 es otro (el `422` de 4.1) | Lectura del informe | Nada que tocar: se anota para que no confunda al leerlo |

Otra observación del informe, sin efecto: Angular lee como JSON el cuerpo
de un error sea cual sea su tipo de contenido. La regla de 2.7 ya decide
por la presencia de `code`, no por el tipo de contenido.

## 4. Decisión del Tech Lead

Pendiente. Se rellena cuando el Tech Lead decida cada fila.

| Hallazgo | Decisión | Commit |
|---|---|---|
| H-01 a H-12 | — | — |
| A-01 a A-03 | — | — |

## 5. Lo que esta respuesta no demuestra

- Nada del frontend se ha ejecutado: no existe. Lo que se dice de Angular
  sale de leer sus paquetes publicados, y lo de JavaScript, de Node 24, no
  de un navegador.
- Lo que el informe afirma de las bibliotecas de tipos de TypeScript
  (H-01) y de `<input type="number">` no lo ha comprobado la IA.
- La fila de 5.5 de la fecha con un desfase horario negativo no la ha
  podido comprobar nadie: al evaluador no le funcionó cambiar la zona
  horaria con Node en Windows, y la IA no lo ha intentado.
- La API de divisas no la comprobó el evaluador, por encargo; la petición
  real de hoy es de la IA (bitácora de la sesión 06).
- El informe es de una sola pasada, y sobre una spec: que SPEC-04 pueda
  implementarse solo se sabrá al implementarla.
