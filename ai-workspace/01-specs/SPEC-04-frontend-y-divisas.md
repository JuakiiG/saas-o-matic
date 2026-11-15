# SPEC-04 · Frontend y divisas

| | |
|---|---|
| **Estado** | `aprobada` (2026-11-14) |
| **Requisitos** | R-09, R-10, R-11, R-12 y R-17 |
| **Supuestos** | A3, A6, A7, A8, A9, A12, A13, A14, A16 y A17 (`decidido`). A3, confirmado por la respuesta del 2026-11-13 |
| **Depende de** | SPEC-01, SPEC-02 y SPEC-03 (contratos de la API), las tres aprobadas el 2026-11-13; las convenciones comunes de la API del índice de specs (ADR-006); ADR-001, ADR-002, ADR-003 y ADR-007 |
| **Bloqueos para aprobarla** | Ninguno desde el 2026-11-14: A3 decidido y confirmado por la respuesta (apartado 9), el bloque backend cerrado y los hallazgos de la evaluación independiente de esta spec, decididos y aplicados (historial). Aprobación aparte, después de ese bloque y antes de empezar el frontend (índice de specs) |

## 1. Objetivo

Definir las vistas de la aplicación web, cómo consumen la API, cómo se
muestran los estados de carga y de error y cómo se convierten los importes a
otra divisa para mostrarlos.

**Dentro**: rutas, panel con buscador, alta de cliente, detalle con
historial, simulador con proyección en tiempo real, selector de divisa y
llamada a la API pública de tipos de cambio.

**Fuera**: toda regla de negocio. El frontend no contiene la tarifa ni los
tipos impositivos (ADR-002), ni el control del identificador fiscal
(`.claude/rules/frontend.md`); los contratos de la API están en SPEC-01,
SPEC-02 y SPEC-03.

## 2. Reglas

### 2.1 Vistas y rutas

| Ruta | Vista | Requisito |
|---|---|---|
| `/` | Panel: buscador de clientes y acceso al alta | R-10 |
| `/clientes/nuevo` | Alta de cliente | A17 |
| `/clientes/:id` | Detalle: datos del cliente e historial de simulaciones | R-11 |
| `/clientes/:id/simulacion` | Simulador | R-12 |
| cualquier otra | Página «no encontrada», con enlace al panel | — |

Una cabecera común a todas las vistas lleva el nombre de la aplicación, el
enlace al panel y el **selector de divisa**. La divisa elegida vale para
todas las vistas y se conserva al navegar; al recargar la página vuelve a
EUR.

**El título del documento.** Cada una de las cuatro vistas pone su título
en el documento (el que se ve en la pestaña y en el historial del
navegador), con la opción `title` del router: el nombre de la vista y,
detrás, el de la aplicación. Son «Clientes · SaaS-O-Matic» (panel), «Nuevo
cliente · SaaS-O-Matic», «Detalle del cliente · SaaS-O-Matic» y
«Simulador · SaaS-O-Matic» (E-57). *Por qué*: el título es lo primero que
anuncia un lector de pantalla al cambiar de vista, y con uno solo para
toda la aplicación todas las vistas se anuncian igual. La página «no
encontrada» no tiene título propio.

**El `id` de la ruta (`/clientes/:id`).** El frontend **nunca convierte
ese texto en número** para pedir el cliente:

1. Comprueba su forma: de 1 a 16 dígitos ASCII (`0` a `9`), **el primero
   distinto de `0`**, y un valor que no pase de 9007199254740991 (2^53 − 1,
   el mayor entero que JavaScript representa exacto). Así quedan fuera
   tanto `01` como el `0` solo.
2. Si no la cumple, muestra «Cliente no encontrado» **sin llamar a la
   API**.
3. Si la cumple, pide `GET /customers/` seguido de ese mismo texto, y la
   respuesta del backend decide (2.4).

**El filtro se aplica al segmento ya descodificado por el router**, no al
texto de la barra de direcciones. Antes de dar el `id`, el router
descodifica lo escrito con `%` y separa del segmento los parámetros de
matriz (lo que sigue a un `;`). Por eso `/clientes/%31` pide el cliente 1,
igual que `/clientes/1`, y `/clientes/1;x=y` también: el parámetro de
matriz no forma parte del `id` (5.7). *Por qué no se mira el texto sin
descodificar*: `%31` y `1` son dos formas de escribir la misma dirección,
también para el backend, que responde con el cliente 1 a
`GET /customers/%31` (sondeado el 2026-11-15 con el cliente de test); y el
parámetro de matriz es sintaxis del router, que la aplicación no usa.

*Por qué no se convierte*: en la API un cliente tiene una sola dirección
(índice de specs, «Identificadores»), y JavaScript convierte `01`, `+1`,
`1.0` o un `1` con un espacio en el número 1: el cliente 1 tendría varias
direcciones en el frontend. *Por qué el filtro*: salvo la limitación que
sigue, todo lo que rechaza lo rechaza también el backend (`not_an_integer`
u `out_of_range`), así que no cambia lo que ve el usuario; evita construir
una URL con un texto arbitrario y garantiza que el `id` que después viaja
en el cuerpo de la proyección y del guardado es exacto. **Limitación
conocida L-06**
([`limitaciones-conocidas.md`](../04-calidad/limitaciones-conocidas.md)),
aceptada por el Tech Lead el 2026-11-14: JavaScript no representa exactos
los enteros por encima de 2^53 − 1, así que el frontend no abre un cliente
con un `id` mayor, aunque el backend lo admita. Solo existiría insertado a
mano en la base de datos.

**Nombres de país y de plan (`GET /meta`).** `/meta` se pide **una vez, al
arrancar la aplicación**, y se guarda en memoria durante la sesión. Las
cuatro vistas que muestran un país o un plan (panel, alta, detalle y
simulador) usan sus nombres («España», «Profesional»), no los códigos.
**Si un código no está en `/meta`**, se muestra el código tal como llega,
sin ninguna marca: es un dato incoherente (el caso de SPEC-02, E-10, un
cliente guardado con un país que el dominio no tiene) y ocultarlo no ayuda
a nadie.
Mientras `/meta` se está cargando, esas vistas muestran el estado de carga.
Si `/meta` falla, cada una muestra el error con «Reintentar» en lugar de su
contenido, **sin códigos sueltos**; «Reintentar» repite la petición de
`/meta`.

### 2.2 Panel y buscador

- Al entrar se muestra el listado inicial (`GET /customers` sin `q`).
- Al escribir, la búsqueda se lanza tras **300 ms** sin cambios y cancela la
  petición anterior, de modo que una respuesta antigua nunca pisa a una más
  reciente.
- **Límite del texto**: 100 caracteres como máximo, **medidos como el
  backend** (SPEC-01, 2.12 y 4.3): en puntos de código y sobre el texto tal
  como está escrito, sin recortar. Si el texto lo supera, no se llama a la
  API, se muestra junto al campo «El texto de búsqueda admite 100
  caracteres como máximo» y se retira la lista anterior. **Se cancela
  además la búsqueda que esté en curso**, para que su respuesta no vuelva a
  pintar la lista que se acaba de retirar, y **el aviso sale al momento**,
  sin esperar los 300 ms: no hay petición que agrupar. El campo no lleva
  `maxlength`, que cuenta unidades UTF-16 y cortaría antes un texto que el
  backend admite.
- **Qué se envía**: el texto tal como está escrito, sin recortar (recorta
  el backend), en **un solo parámetro `q`** puesto con los parámetros del
  cliente HTTP, nunca concatenado en la URL. Con el texto vacío la petición
  va sin `q`. *Por qué*: concatenado, un `%`, un `&`, un `#` o un `+`
  cambiarían la consulta (el backend lee `q=a+b` como «a b»); y con un `q`
  repetido el backend solo valida y usa el último (su limitación L-04).
- El frontend no interpreta el texto: `%`, `_`, `\` y las comillas viajan
  como texto y el backend los busca literalmente (SPEC-01, 5.9).
- Un *surrogate* suelto no se puede codificar en una URL: antes de enviar
  se sustituye por U+FFFD, y se muestra lo que devuelva la API para ese
  texto. Cómo se detecta está en 2.3.
- Cada resultado muestra el nombre, el identificador fiscal, el país y el
  plan, y enlaza con el detalle. El país y el plan se muestran **con los
  nombres de `GET /meta`** («España», «Profesional»), no con sus códigos. Si
  `/meta` falla, el panel muestra el error con «Reintentar» en lugar del
  buscador y de la lista (2.1).
- Cuatro estados visibles de la petición: cargando, error con botón
  «Reintentar», sin resultados y lista. El aviso del límite del texto no es
  un estado de la petición: con él no hay petición.
- **Sin resultados tiene dos mensajes**, según lo que se pidió. Si la
  petición llevaba `q`: «No hay clientes que coincidan». Si era el listado
  inicial, sin `q`: «Todavía no hay clientes», con el acceso al alta. *Por
  qué*: el listado inicial vacío es lo primero que se ve con la base de
  datos recién creada, y nadie ha buscado nada.
- **Si la lista trae 20 clientes**, se indica bajo ella: «Se muestran como
  máximo 20 clientes. Escribe más texto para afinar la búsqueda.» *Por
  qué*: 20 es el máximo que devuelve la API, que no dice cuántos hay
  (SPEC-01, E-26 y 4.3), así que con 20 a la vista puede haber más. Ese 20
  es una constante de `core/`, con la cita de SPEC-01 E-26: es el único
  límite del backend que el frontend lleva escrito para mostrar un aviso.
- **La lista no espera a `/meta`.** El panel pide su listado al abrirse,
  aunque `/meta` todavía se esté cargando o haya fallado, y lo enseña
  cuando `/meta` llega; hasta entonces se ve el estado de carga o el error
  de `/meta` (2.1), nunca la lista con códigos. *Por qué*: las dos
  peticiones son independientes, y lanzar una al acabar la otra alargaría
  la espera sin evitar nada. Cuando `/meta` llega, o se reintenta con
  éxito, la lista ya está y no hace falta pedirla otra vez.
- El frontend no filtra ni ordena: muestra lo que devuelve la API, en su
  orden. También cuando, para un texto que no está vacío, el backend
  devuelve el listado inicial: es lo que hace con un texto de solo espacios
  o de solo marcas diacríticas (SPEC-01, 5.9).

### 2.3 Alta de cliente

- Los desplegables de país y plan se rellenan con `GET /meta`. Si `/meta`
  falla, se muestra el error con «Reintentar» en lugar del formulario
  (2.1), que por tanto no se puede enviar.
- **Validación en el navegador, solo de ayuda.** La ayuda rechaza
  **únicamente lo que el backend rechazaría seguro**; todo lo demás se
  envía, lo decide el backend y su error se muestra junto al campo. **El
  control del identificador fiscal no se calcula en el frontend.**

| Campo | Qué comprueba la ayuda | Qué deja al backend |
|---|---|---|
| `company_name` | De 2 a 120 caracteres tras recortar | Los caracteres no admitidos (`invalid_characters`) |
| `tax_id` | No vacío y de 30 caracteres como máximo, **medidos sin recortar**, como el backend, que mide antes de normalizar | El formato y el carácter de control |
| `contact_email` | Tras recortar: no vacío, de 254 caracteres como máximo, contiene una `@` y no empieza ni acaba en `@` | El resto de la regla del email (SPEC-01, 2.1): ningún separador Unicode, una sola `@`, un punto en el dominio y los caracteres no admitidos |
| `country` y `plan` | Elegido uno de la lista de `/meta` | — |
| Los tres campos de texto | Texto bien formado: sin ningún *surrogate* suelto | — |

- **La ayuda mide igual que el backend** (SPEC-01, 2.12): las longitudes se
  cuentan en puntos de código (`[...s].length`, no `s.length`, que cuenta
  unidades UTF-16) y recortar es quitar de los extremos solo el carácter
  U+0020 (no `trim()`, que quita también tabuladores y saltos de línea).
  *Por qué*: una ayuda que mide distinto bloquearía altas que el backend
  acepta.
- **La ayuda del email no usa el validador de email del framework
  (`Validators.email`) ni el del navegador (`type="email"`).** *Por qué*:
  el backend acepta direcciones que esos validadores rechazan. El de
  Angular 21.2.26 solo admite letras ASCII, 64 caracteres antes de la `@` y
  63 por etiqueta del dominio (expresión leída el 2026-11-14 en el paquete
  publicado): rechazaría `josé@empresa.example`, que el backend guarda. Y
  copiar entera la regla del backend sería tener dos implementaciones.
- **Ningún campo lleva el atributo `maxlength`.** *Por qué*: cuenta
  unidades UTF-16 y no puntos de código, así que impediría escribir un
  nombre que el backend acepta (la fila de los 61 caracteres `𝔸` de 5.4).
  El exceso lo dice la ayuda, con su mensaje.
- **Un texto con un *surrogate* suelto no se envía.** *Por qué*: el
  navegador lo serializa como un escape `\ud800` y el backend responde
  `400` `malformed_request` (índice de specs, «El texto del cuerpo»), que
  es un error de la petición y no de un campo: el usuario no sabría qué
  corregir. **Cómo se detecta**, aquí y en el buscador (2.2): con una
  expresión regular en modo Unicode (`/\p{Surrogate}/u`), que no ve como
  *surrogate* las dos mitades de una pareja bien formada, como un emoji.
  No con `isWellFormed()` ni `toWellFormed()`: son de ES2024, y la
  configuración por defecto del CLI compila para ES2022 y no las conoce
  (`.claude/rules/frontend.md` manda usar esa configuración).
- **Qué se envía**: el nombre y el email, **recortados** (solo U+0020, el
  mismo recorte con el que la ayuda los ha medido); el identificador, tal
  como está escrito; y los códigos de país y de plan de `/meta`. Nada se
  normaliza: lo hace el backend, y el detalle muestra lo que el backend
  devuelve (el identificador, normalizado). El cuerpo se construye siempre
  a partir de un objeto con los cinco campos del contrato y nada más. *Por
  qué se recortan el nombre y el email*: la ayuda mide el texto recortado,
  así que sin recortar se podría enviar un nombre válido rodeado de
  megabytes de espacios, y el backend lee entero cualquier cuerpo (su
  limitación L-01; 4.3). El resultado es el mismo: el backend recorta ese
  mismo carácter.
- Al enviar, el botón se desactiva hasta que llega la respuesta, para que no
  haya dos altas. **Tras un `201` sigue desactivado** hasta que la
  navegación retira el formulario. *Por qué*: un doble clic entre la
  respuesta y la navegación crearía un segundo cliente o un `409`.
- **La ayuda calla hasta el primer intento de envío** y, desde entonces,
  acompaña a lo que se escribe. *Por qué*: un formulario recién abierto no
  tiene errores que señalar. (La del simulador habla desde el primer
  carácter; 2.5.)
- **Cada desplegable lleva una primera opción desactivada**, «Elige un
  país» y «Elige un plan», que no se puede elegir y es la que se ve al
  abrir el formulario. Las opciones que se pueden elegir son exactamente
  las de `/meta`. *Por qué*: sin ella el desplegable enseñaría el primer
  país como si alguien lo hubiera elegido.
- **Tras un envío con errores, el foco va al primer campo con error**, en
  el orden del formulario (nombre, identificador, email, país y plan):
  tanto si la ayuda ha impedido el envío como si el backend responde `422`
  con errores de campo. El foco llega cuando el mensaje ya está en
  pantalla, para que el lector de pantalla lo lea con el campo. Si el
  error no tiene campo en el formulario (el `409`, un error general o un
  `422` cuyos errores van todos al aviso general), el foco no se mueve.
  *Por qué*: quien usa el teclado o un lector de pantalla llega
  directamente a lo que tiene que corregir.
- **El mensaje del backend junto a un campo se retira cuando ese campo
  cambia**, aquí y en el simulador. *Por qué*: lo que el backend juzgó ya
  no es lo que está escrito.
- Respuestas:

| Respuesta | Comportamiento |
|---|---|
| `201` | Navega al detalle del cliente creado, con el `id` **del cuerpo** de la respuesta. La cabecera `Location` no se lee: CORS no la expone al navegador (2.9) |
| `422` con `errors` | Cada error se muestra junto a su campo (`field`), con el `message` del backend. El formulario conserva lo escrito |
| `409` `customer_already_exists` | Aviso en el formulario: ya existe un cliente con ese identificador en ese país. **Sin «Reintentar»**. Conserva lo escrito |
| Otro error o sin conexión | Aviso general con «Reintentar», con el texto que le corresponde por su `code` (tabla de 2.7). Conserva lo escrito |

- **El `409` y el aviso general de un `422` no ofrecen «Reintentar»**, aquí
  y en el simulador (2.5). *Por qué*: enviar lo mismo no puede salir bien;
  el backend ya ha dicho que esos datos no valen, y lo que toca es
  cambiarlos. La salida es corregir el formulario o dejarlo, con «Cancelar»
  o con el enlace al panel de la cabecera (2.7). Un `422` que no deja
  ninguna entrada que mostrar es otro caso: se trata como un error
  inesperado, con «Reintentar» (más abajo).
- El frontend decide **por el código**, nunca por el texto. Un código de
  campo que no conoce se muestra igualmente junto a su campo; un `field` que
  no existe en el formulario se muestra en el aviso general.
- **Forma de `errors`** (índice de specs, «Errores de validación»; SPEC-01,
  2.12): el backend envía **un solo error por campo**, en el orden de los
  campos del contrato, y después un `unknown_field` por cada campo que el
  contrato no tiene. Así, cada campo muestra como mucho un mensaje, y el
  aviso general lista los errores sin campo en el orden en que llegan. Un
  `unknown_field` significa que el frontend envió un campo de más: es un
  defecto suyo, y se muestra en el aviso general como cualquier `field`
  que no está en el formulario.
- **Lo que llegue fuera de esa forma no se pierde ni rompe el formulario**,
  aquí y en el simulador (2.5):
  - Una entrada de `errors` que no sea un objeto con `field`, `code` y
    `message` de texto **se ignora**: no hay campo al que llevarla ni texto
    que enseñar. Las demás se muestran.
  - Si llegan **dos errores del mismo campo**, el primero se muestra junto
    al campo y los siguientes, en el aviso general, para que ninguno se
    pierda.
  - Si un `422` no deja ninguna entrada que mostrar, se trata como un error
    inesperado (2.7): aviso general, y el formulario conserva lo escrito.

  *Por qué*: el backend no debería enviar nada de eso, pero un `422` que
  deja el formulario sin ningún mensaje, o que hace fallar la pantalla, no
  le dice al usuario qué ha pasado.

### 2.4 Detalle del cliente

- Una tarjeta con los datos del cliente: nombre, identificador fiscal, email,
  país y plan (con los nombres de `/meta`) y fecha de alta. Si `/meta`
  falla, el detalle muestra el error con «Reintentar» (2.1).
- Una tarjeta por simulación, en el orden que devuelve la API: fecha,
  usuarios, almacenamiento, llamadas a la API, coste base, impuesto con su
  tipo y total. El desglose por tramos va en un bloque desplegable.
- Los importes se muestran en la divisa elegida (2.6).
- Si `simulation_count` es mayor que el número de simulaciones recibidas, se
  indica: «Se muestran las *M* últimas de *N*», donde *M* es el número de
  simulaciones recibidas y *N*, `simulation_count`. *Por qué no un 50
  escrito*: el límite de 50 es del backend (SPEC-03, 2.4), que devuelve las
  de `id` más alto, la última guardada primero; el frontend cuenta lo que
  recibe.
- Sin simulaciones: mensaje y enlace al simulador.
- Vista «Cliente no encontrado», con enlace al panel, en dos casos: el
  `id` de la ruta no tiene la forma de 2.1 (`/clientes/abc`,
  `/clientes/01`, `/clientes/0`), y entonces no se llama a la API; o
  `GET /customers/{id}` responde `404` con `customer_not_found`. Cualquier
  otro error se muestra como dice 2.7, no con esa vista. **También un
  `422`**: todo `id` que pasa el filtro es válido para el backend, así que
  un `422` en esta llamada solo puede venir de un defecto del frontend (un
  parámetro de consulta de más, por ejemplo) y es un error inesperado.
- **Responsive**: a 375 px, una columna y sin desplazamiento horizontal; en
  escritorio, las tarjetas del historial en varias columnas.

### 2.5 Simulador

- **Usuarios activos**: un control deslizante de 0 a 500 y, sincronizado con
  él, un campo de texto para números que admite de 0 a 100.000 (A7). Valor
  inicial: 10.
- Al abrir el simulador se pide el cliente. **Mientras el cliente no se ha
  cargado no se pide ninguna proyección**, aunque el valor inicial de
  usuarios sea válido y hayan pasado los 200 ms; la primera se pide cuando
  llega el cliente. Si el `id` de la ruta no tiene la forma de 2.1 (y
  entonces el cliente no se pide), o el cliente responde `404` con
  `customer_not_found`, se muestra la vista «Cliente no encontrado»
  y no se pide ninguna proyección. Lo mismo si una proyección o un guardado
  responde `404` `customer_not_found`.
- **El `customer_id` de la proyección y del guardado es el `id` del cliente
  cargado**, el que devolvió `GET /customers/{id}`, no el texto de la ruta.
- **Qué es un valor válido en los tres campos numéricos: decide el texto
  escrito, no el número que resulta.** Es válido un texto formado solo por
  dígitos ASCII (`0` a `9`), al menos uno, cuyo valor está dentro de los
  límites del campo. No lo son `1e3`, `15.0`, `1,5`, `-1`, `+15`, un texto
  con espacios ni el campo vacío. `015` sí: son solo dígitos y vale 15. Se
  envía el valor como número JSON sin decimales, que es lo único que el
  backend admite (SPEC-02, 4; SPEC-03, 4.1).
- **Los tres son campos de texto con `inputmode="numeric"`**, no controles
  numéricos del navegador (`type="number"`). *Por qué*: un control numérico
  solo entrega el número y esconde el texto, y el número engaña: JavaScript
  lee `100000.000000000001` como el entero 100000 y `1e3` como 1000. Con
  `inputmode="numeric"` el móvil sigue mostrando el teclado de números.
- El simulador muestra el nombre de la empresa y el **nombre del país** del
  cliente, tomado de `/meta` («España»), no su código. Si `/meta` falla,
  muestra el error con «Reintentar» (2.1).
- **Almacenamiento** y **llamadas a la API**: campos de texto para números
  enteros, con los límites de SPEC-03. Valor inicial: 0. Cambiarlos no pide una proyección
  nueva, porque no tienen precio (A3). Un valor no válido en uno de ellos
  muestra el error junto al campo y desactiva «Guardar», pero **no retira la
  proyección**, que no depende de ellos.
- **Proyección**: al cambiar los usuarios, tras **200 ms** sin cambios se
  llama a `POST /pricing/quote`, cancelando la petición anterior (ADR-002).
  Se muestran los tres tramos, el coste base, el impuesto con su tipo y el
  total, en la divisa elegida.
- **La primera proyección no espera los 200 ms**: se pide en cuanto llega
  el cliente. Tampoco espera la de «Reintentar», que pide al momento la de
  los usuarios escritos. *Por qué*: la espera existe para no pedir una
  proyección por cada paso del deslizante, y en esos dos casos no hay
  pasos intermedios.
- **Durante los 200 ms de espera** los importes que estén a la vista ya se
  marcan como «actualizando» y «Guardar» está desactivado. *Por qué*: desde
  que el valor cambia, la proyección del valor actual no está.
- **La ayuda de los tres campos numéricos habla desde el primer carácter**,
  sin esperar a un intento de guardar. *Por qué*: la proyección es en vivo,
  y un valor no válido la retira en ese mismo momento; callar dejaría la
  pantalla sin importes y sin explicación. (La del alta calla hasta el
  primer intento de envío; 2.3.)
- Con un texto no válido en el campo de usuarios, **el control deslizante
  se queda donde estaba**.
- Si `/meta` falla, el cliente y su primera proyección se piden igual,
  detrás del aviso: al reintentar `/meta` el simulador aparece ya cargado.
- Estados de la proyección:

| Estado | Qué se ve |
|---|---|
| Cargando | Los importes anteriores se marcan como «actualizando»; no se presentan como vigentes |
| Datos | El desglose y el total |
| Error | Se retiran los importes; aviso con «Reintentar». **Excepción**: con un `422` con `errors`, cada mensaje va junto a su campo o al aviso general, **sin «Reintentar»**, porque pedir lo mismo daría el mismo `422` (2.3). **Nunca queda a la vista un importe anterior como si fuera el actual** |
| Usuarios no válidos | No se llama a la API; mensaje junto al campo; se retiran los importes |

- **Guardar**: llama a `POST /simulations`. El botón está desactivado
  mientras la proyección no esté en estado «datos» para el valor actual,
  mientras haya un campo no válido y mientras se guarda. Tras un `201`
  sigue desactivado hasta que la navegación retira la vista, como en el
  alta (2.3).
- Tras un `201` se navega al detalle, donde la simulación nueva aparece la
  primera. Lo que se muestra de ella es lo que devolvió el servidor, no la
  proyección.
- **Un `422` de la proyección o del guardado** se muestra como el del alta
  (2.3): cada error junto a su campo si el campo está en el formulario
  (`active_users`, `storage_gb`, `estimated_api_calls`) y en el aviso
  general si no lo está (`customer_id` o un `unknown_field`). No debería
  llegar, porque la ayuda usa los mismos límites; si llega, los valores se
  conservan y, en la proyección, se retiran los importes.
- Cualquier otro error al guardar se muestra, con el aviso que le
  corresponde por su `code` (2.7), sin perder los valores del formulario.
- **Si el guardado agota los 10 s** (`timeout`), el aviso dice además que
  la simulación puede haberse guardado y ofrece, junto a «Reintentar», un
  enlace al detalle del cliente para comprobarlo. *Por qué*: el frontend
  deja de esperar, pero el servidor puede haber terminado; reintentar a
  ciegas crearía una segunda simulación igual.

### 2.6 Divisas

- **Divisas ofrecidas**: EUR, USD, GBP y CHF. EUR es la inicial.
- **Origen de los tipos**: la API pública Frankfurter, llamada **directamente
  desde el navegador** (A8), en una sola petición para las tres divisas a
  su versión vigente, la `v2`:
  `GET https://api.frankfurter.dev/v2/rates?base=EUR&quotes=USD,GBP,CHF`.
  La respuesta es una lista con un objeto `{date, base, quote, rate}` por
  divisa (4.2).
- **Cuándo**: una vez al arrancar la aplicación. Los tipos se guardan en
  memoria durante la sesión; cambiar de divisa no hace ninguna petición.
- **Conversión**: `importe mostrado = céntimos × tipo / 100`, redondeado a
  dos decimales al formatear. Es el único punto del frontend con coma
  flotante sobre dinero (ADR-002) y su resultado **nunca se guarda ni se
  envía al backend**.
- **Cada importe se convierte por separado**, así que en otra divisa la base
  más el impuesto puede diferir del total en un céntimo (ejemplo en 5.1). No
  se ajusta: junto a los importes convertidos se indica que son orientativos.
- **Con EUR no hay conversión**: el importe sale exacto de los céntimos y no
  depende de la API de divisas.
- **El EUR se formatea solo con enteros.** Los euros son
  `(céntimos − céntimos % 100) / 100`, una división exacta, y los céntimos,
  el resto. Se formatean los euros por partes (`formatToParts`) y la parte
  decimal se sustituye por los céntimos con dos cifras. **El importe no se
  divide entre 100.** *Por qué*: `céntimos / 100` es una operación en coma
  flotante sobre dinero, que solo se admite en la conversión de divisa
  (ADR-002 y `.claude/rules/frontend.md`); y pasar a `format` el importe
  como texto exacto exige una biblioteca de tipos que la configuración por
  defecto del CLI no declara. Da el mismo texto que la división
  (comprobado con Node el 2026-11-14 en 8.645.796 importes, de 0 a
  60520570), sin hacerla.
- **Formato**: `Intl.NumberFormat('es-ES')` con el código de la divisa
  (`169,40 EUR`, `188,69 USD`), a través de un único *pipe*. Los importes
  de cuatro cifras salen **sin punto de millar** (`1234,50 EUR`), que es
  lo que hace `es-ES`; con cinco o más, con él (`12.345,00 EUR`).
- Mientras la divisa elegida no es EUR se muestran, junto a los importes, el
  tipo aplicado y su fecha («1 EUR = 1,1139 USD · tipo del 12/11/2026») y el
  total en EUR. **El tipo se muestra con los decimales que trae, hasta 6**
  (`Intl.NumberFormat('es-ES', { maximumFractionDigits: 6 })`): `1,1139`,
  `0,92316`. La fecha es la del objeto de esa divisa: cada tipo trae la
  suya. Es una fecha sin hora y se muestra **tal cual**, solo cambiando su
  forma a día/mes/año, sin convertirla de zona horaria.
- **Dónde se muestra cada cosa** mientras la divisa elegida no es EUR:
  - El tipo aplicado, con su fecha, y el aviso de que los importes son
    orientativos van juntos y **una vez por vista**: en el simulador,
    dentro de la proyección; en el detalle, sobre el historial de
    simulaciones. El panel no muestra importes y no lleva ninguno de los
    dos.
  - El total en EUR va **junto a cada total convertido**, con el rótulo
    «Total en EUR»: uno en la proyección y uno en cada tarjeta del
    historial.
  - **Se convierten todos los importes visibles**, también los del
    desglose por tramos (el precio por usuario y el subtotal de cada
    tramo). El único importe que sigue en euros es el «Total en EUR».
- **El *pipe* de importes admite un argumento** para dar el importe en EUR
  exacto sea cual sea la divisa elegida; es lo que usa el «Total en EUR».
  Sigue habiendo un único *pipe* que convierte un importe en texto.
- **El selector enseña los códigos** de las divisas (EUR, USD, GBP y CHF),
  no sus nombres, con la etiqueta «Divisa».
- **Estados**:

| Estado | Qué se ve |
|---|---|
| Cargando | El selector solo permite EUR e indica que los tipos se están cargando |
| Datos | El selector permite las cuatro divisas |
| Error | Aviso visible, importes en EUR, selector limitado a EUR y botón «Reintentar». El resto de la aplicación funciona igual |

- **Qué cuenta como error**: fallo de red, más de 5 s sin respuesta, estado
  distinto de `200` o una respuesta que no supera la validación.
- **Validación de la respuesta**: debe ser una lista en la que, para cada
  una de las tres divisas pedidas, haya **exactamente un** objeto con ese
  `quote`, con `base` igual a `EUR`, un `date` con forma de fecha
  (`AAAA-MM-DD`) y un `rate` numérico mayor que 0. Una divisa ausente o
  repetida, o un objeto que incumpla algo de lo anterior, invalida la
  respuesta entera: una respuesta parcial se trata como error completo. Los
  objetos de divisas no pedidas se ignoran. Una respuesta que no supera la
  validación deja el estado de error con el código `invalid_rates`.
- **El aviso del error vive en la cabecera**, junto al selector, y por eso
  se ve en todas las vistas, con su botón «Reintentar», que repite la
  petición de los tipos.
- **Textos**: «Divisa» (etiqueta del selector); «Cargando tipos…» (mientras
  se cargan); «No se han podido cargar los tipos de cambio. Los importes se
  muestran en EUR.» (aviso del error); «Importes orientativos: cada uno se
  convierte por separado.» (junto al tipo aplicado); y «Total en EUR».

### 2.7 Estados de carga y de error (R-17)

- **Toda llamada remota tiene tres estados explícitos**: cargando, error y
  datos, y la interfaz muestra los tres.
- Ninguna llamada espera sin límite: 10 s para el backend y 5 s para la API
  de divisas. Pasado ese tiempo el estado es «error».
- Todo error ofrece una salida: «Reintentar» o un enlace al panel. En un
  formulario, el `409` del alta y el aviso general de un `422` no ofrecen
  «Reintentar» (2.3 y 2.5): su salida es corregir lo escrito, o el enlace
  del propio formulario y el del panel en la cabecera.
- Los indicadores de carga llevan `role="status"` y los avisos de error
  `role="alert"`. **Qué lleva `role="alert"`**: los avisos generales (el de
  una carga o un envío que falla y el del fallo de los tipos en la
  cabecera) y los mensajes junto a un campo que salen mientras se escribe,
  sin que el foco se mueva: los de los tres campos del simulador y el del
  campo de búsqueda del panel. **Qué no lo lleva**: los mensajes junto a un
  campo del alta. Salen al enviar, hasta cinco a la vez, y el foco va
  entonces al primer campo con error (E-56): cada uno se lee con su campo,
  que lo señala con `aria-describedby` y `aria-invalid`. Con `role="alert"`
  se anunciarían todos de golpe. Nada de esto se ha probado con un lector
  de pantalla (limitación conocida L-10).
- Los errores no se tragan: el servicio los convierte en un estado de error
  con el `code` de la API cuando existe, y en `network_error` o `timeout`
  cuando no hay respuesta.
- **Errores del backend que no son propios de una vista.** Las seis
  llamadas de 4.1 pueden recibir los errores genéricos de las convenciones
  comunes (índice de specs). El frontend los distingue **por su `code`** y
  los muestra donde la vista muestra su estado de error (en los
  formularios, el aviso general):

| Lo que llega | `code` del estado de error | Qué se ve |
|---|---|---|
| `503` `service_unavailable` | `service_unavailable` | Aviso de servicio no disponible: «El servicio no está disponible en este momento. Inténtalo de nuevo dentro de unos minutos.», con «Reintentar» |
| `500` `internal_error` o `tax_rate_not_defined` | El recibido | Aviso de error inesperado: «Se ha producido un error inesperado.», con «Reintentar» |
| `400` `malformed_request`, `415` `unsupported_media_type`, `405` `method_not_allowed`, `404` `not_found` o un `422` `validation_error` en el buscador o en la petición del cliente | El recibido | El aviso de error inesperado, con «Reintentar» |
| Un `code` que el frontend no conoce | El recibido | El aviso de error inesperado, con «Reintentar» |
| Una respuesta de error sin `code` (su cuerpo no es el de la API) | `unknown_error` | El aviso de error inesperado, con «Reintentar» |
| Ninguna respuesta | `network_error` | Aviso de falta de conexión: «No se ha podido conectar con el servidor.», con «Reintentar» |
| Ninguna respuesta en 10 s | `timeout` | Aviso de espera agotada: «El servidor tarda demasiado en responder.», con «Reintentar» |

  *Por qué el `503` tiene su propio aviso*: el `500` dice «fallo nuestro» y
  el `503`, «no disponible ahora» (índice de specs); al usuario le sirve
  saber que basta con esperar. *Por qué se tratan el `400`, el `415`, el
  `405` y el `not_found`*: el frontend no debería provocarlos, y si llegan
  es un defecto suyo; aun así la pantalla tiene que mostrar algo y dejar
  una salida, y el `code` recibido queda en el estado de error para que lo
  vea un test o quien depure. «Reintentar» repite la misma petición. El
  texto de los avisos es del frontend: el `detail` del backend no decide
  nada.
- **«Reintentar» en un formulario** (el alta y el guardado del simulador)
  hace lo mismo que «Guardar»: envía **lo que el formulario tiene en ese
  momento**, pasando otra vez por la ayuda, y no el cuerpo de la petición
  que falló. *Por qué*: si algo se cambió después del error, enviar el
  cuerpo anterior guardaría datos que ya no están en pantalla. Si nada se
  cambió, es la misma petición.
- **El `404` tiene dos códigos** y solo uno es «Cliente no encontrado»:
  `customer_not_found` es un cliente que no existe; `not_found` es una ruta
  de la API que no existe, es decir, una URL mal construida por el
  frontend, y se trata como error inesperado.

### 2.8 Presentación

- Textos en español.
- Los tipos impositivos llegan en puntos básicos y se muestran como
  porcentaje (`2100` → «21 %»).
- Los tramos se rotulan con sus límites: «del 1 al 10», «del 11 al 50» y
  «del 51 en adelante». El último llega con `to_users` `null` (SPEC-02, 4),
  y es el que se rotula «en adelante».
- Las fechas con hora del backend (`created_at`) llegan en UTC y se muestran
  en la zona horaria del navegador, con formato `es-ES`. La fecha del tipo de
  cambio no tiene hora y queda fuera de esta regla (2.6). **Un `created_at`
  que no se puede leer como fecha se muestra como llega**, sin marca. *Por
  qué*: el backend no debería enviarlo, y si lo envía, ocultarlo o
  sustituirlo por un texto propio no ayuda a nadie; es el mismo criterio
  que con un código que `/meta` no trae (2.1).
- Controles con etiqueta, manejables con teclado; HTML semántico.
- **El anillo de foco y el borde de los campos de formulario tienen un
  contraste de 3:1 o más** sobre el blanco y sobre el fondo de la página
  (CA-19). El anillo es del color de acento, no naranja: junto al rojo de
  un error, un anillo naranja parecería otro error. El borde de las
  tarjetas, de los avisos y de la cabecera es más claro y queda fuera de
  esta regla: solo decora, y oscurecerlo carga la vista.
- **El corrector ortográfico del navegador se desactiva**
  (`spellcheck="false"`) en el campo de búsqueda del panel y, en el alta,
  en el nombre, el identificador fiscal y el email. *Por qué*: lo que se
  escribe ahí son nombres propios, códigos y direcciones, y el corrector
  los subraya como si fueran faltas.

### 2.9 Configuración

La URL del backend y la de la API de divisas están en los ficheros de
entorno de Angular, no repartidas por el código. El backend admite por CORS
solo el origen del frontend (A16); el requisito y su criterio están en
SPEC-03, «Operación del backend».

Lo que esa configuración de CORS exige del frontend (SPEC-03, 2.7):

- **Origen**: el frontend se sirve desde `http://localhost:4200`, el origen
  que el backend admite por defecto. Desde otro origen
  (`http://127.0.0.1:4200` lo es) el navegador oculta todas las respuestas
  del backend y cada llamada acaba en `network_error`.
- **Métodos y cabeceras**: solo `GET` y `POST`, y **ninguna cabecera
  propia**. Las únicas que viajan son `Accept` y, en los `POST`,
  `Content-Type: application/json`. Con una cabecera de más (la de un
  interceptor, por ejemplo) el backend rechaza la comprobación previa, y el
  frontend vería un `network_error`.
- **Cabeceras de respuesta**: el frontend no lee ninguna. El backend no
  expone ninguna por CORS, así que `Location` (en el `201` del alta) y
  `Allow` (en el `405`) no se pueden leer desde el navegador.
- **Cuerpos**: siempre un objeto JSON serializado por el cliente HTTP, en
  UTF-8 y sin marca de orden de bytes, que es lo único que el backend lee
  (índice de specs, «El texto del cuerpo»).

## 3. Requisitos (EARS)

### Panel y buscador

| Id | Requisito | Cubre |
|---|---|---|
| E-01 | Cuando se abre el panel, el sistema deberá mostrar el listado inicial de clientes. | R-10 |
| E-02 | Cuando el texto del buscador lleva 300 ms sin cambiar, el sistema deberá pedir la búsqueda y cancelar la petición anterior si sigue en curso. | R-10 |
| E-03 | El sistema deberá mostrar los resultados en el orden en que los devuelve la API, sin filtrarlos ni reordenarlos. | R-10 |
| E-04 | Cuando la búsqueda no devuelve clientes, el sistema deberá mostrar un mensaje de «sin resultados» distinto del estado de carga y del de error. | R-10, R-17 |
| E-50 | Si el texto del buscador supera los 100 caracteres, medidos en puntos de código y sin recortarlo, entonces el sistema deberá mostrar al momento un aviso junto al campo, cancelar la búsqueda que esté en curso, no llamar a la API y retirar la lista. | R-10, A14 |
| E-51 | El sistema deberá enviar el texto del buscador tal como está escrito, en un único parámetro `q` codificado por el cliente HTTP, y sin `q` cuando el texto está vacío. | R-10 |
| E-53 | Cuando la lista del panel trae 20 clientes, el sistema deberá indicar bajo ella que se muestran como máximo 20. | R-10, A13 |
| E-54 | Cuando el listado inicial, pedido sin `q`, llega vacío, el sistema deberá mostrar «Todavía no hay clientes» con un acceso al alta, en lugar del mensaje de «sin resultados» de una búsqueda. | R-10, R-17 |
| E-35 | El sistema deberá mostrar el país y el plan con los nombres que devuelve `GET /meta`, no con sus códigos, en el panel, el alta, el detalle y el simulador; si un código no está en `/meta`, deberá mostrar ese código tal como llega. | R-10, R-11, R-12 |
| E-39 | Cuando arranca la aplicación, el sistema deberá pedir `GET /meta` una sola vez y conservar la respuesta en memoria durante la sesión. | A13 |
| E-40 | Si `GET /meta` falla, entonces el sistema deberá mostrar en el panel, el alta, el detalle y el simulador el error con un botón «Reintentar» en lugar de su contenido, sin mostrar ningún código de país o de plan. | R-17 |

### Alta

| Id | Requisito | Cubre |
|---|---|---|
| E-05 | El sistema deberá ofrecer como países y planes exactamente los que devuelve `GET /meta`. | A17 |
| E-06 | El sistema no deberá calcular ni comprobar en el navegador el carácter de control del identificador fiscal. | `.claude/rules/frontend.md` |
| E-07 | Mientras un alta está en curso, el sistema deberá impedir un segundo envío. | A17 |
| E-08 | Cuando el alta responde `201`, el sistema deberá navegar al detalle del cliente creado. | A17 |
| E-09 | Si el alta responde `422`, entonces el sistema deberá mostrar cada error junto a su campo y conservar los valores escritos. | A14, R-17 |
| E-10 | Si el alta responde `409` con `customer_already_exists`, entonces el sistema deberá avisar de que el cliente ya existe y conservar los valores escritos. | A12 |
| E-11 | El sistema deberá decidir el tratamiento de un error de la API por su `code`, nunca por su texto. | A14 |
| E-41 | El sistema deberá medir en la validación de ayuda del navegador las longitudes en puntos de código y recortar solo el carácter U+0020, igual que el backend. | A17 |
| E-44 | El sistema deberá comprobar del email, en la validación de ayuda, únicamente que tras recortarlo no está vacío, no supera los 254 caracteres y contiene una `@` que no está en un extremo, sin usar el validador de email del framework ni el del navegador. | A17 |
| E-45 | Si un campo de texto del alta contiene un *surrogate* suelto, entonces el sistema deberá mostrar el error junto al campo y no enviar el alta. | A14 |
| E-46 | El sistema deberá enviar el nombre y el email del alta recortados (solo U+0020) y el identificador tal como está escrito, sin normalizar ninguno, y tomar el `id` del cliente creado del cuerpo del `201`. | A17 |
| E-56 | Si un envío del alta termina con errores en algún campo del formulario, porque la ayuda lo impide o porque el backend responde `422`, entonces el sistema deberá llevar el foco al primer campo con error, en el orden del formulario. | A14, R-17 |
### Detalle

| Id | Requisito | Cubre |
|---|---|---|
| E-12 | Cuando se abre el detalle de un cliente existente, el sistema deberá mostrar sus datos y una tarjeta por cada simulación recibida, en el orden de la API. | R-11 |
| E-13 | Cuando el cliente no tiene simulaciones, el sistema deberá mostrar un mensaje y un enlace al simulador. | R-11 |
| E-14 | Mientras el cliente tiene más simulaciones de las recibidas, el sistema deberá indicar cuántas se muestran y cuántas hay. | R-11 |
| E-15 | Si el `id` de la ruta no tiene la forma de 2.1, o la petición del cliente responde `404` con `customer_not_found`, entonces el sistema deberá mostrar la vista «Cliente no encontrado» con un enlace al panel, tanto en el detalle como en el simulador. | R-11, R-17 |
| E-47 | El sistema deberá pedir el cliente con el texto del `id` de la ruta, sin convertirlo en número, y no deberá pedirlo cuando ese texto no tiene la forma de 2.1. | R-11, A14 |
| E-16 | El sistema deberá mostrar el detalle sin desplazamiento horizontal a 375 px de ancho. | R-11 |

### Simulador

| Id | Requisito | Cubre |
|---|---|---|
| E-17 | El sistema deberá mantener sincronizados el control deslizante y el campo numérico de usuarios. | R-12 |
| E-18 | Cuando el número de usuarios lleva 200 ms sin cambiar y es válido, y el cliente ya se ha cargado, el sistema deberá pedir la proyección a `POST /pricing/quote` y cancelar la petición anterior si sigue en curso. | R-12, A9 |
| E-38 | Mientras el cliente no se ha cargado, el sistema no deberá pedir ninguna proyección. | R-12 |
| E-19 | El sistema deberá mostrar como proyección únicamente los importes devueltos por el backend, sin calcular ninguno en el navegador salvo la conversión de divisa. | A9, ADR-002 |
| E-20 | Si la proyección falla, entonces el sistema deberá retirar los importes anteriores y mostrar un aviso con opción de reintentar. | R-17, ADR-002 |
| E-21 | Mientras una proyección está en curso, el sistema deberá marcar los importes visibles como no vigentes. | R-17 |
| E-22 | Si el texto del campo de usuarios no está formado solo por dígitos ASCII, o su valor está fuera de sus límites, entonces el sistema deberá mostrar el error junto al campo, no llamar a la API y retirar los importes. | A7 |
| E-36 | Si el texto del campo de almacenamiento o del de llamadas no está formado solo por dígitos ASCII, o su valor está fuera de sus límites, entonces el sistema deberá mostrar el error junto al campo y desactivar el guardado, sin retirar la proyección. | A3 |
| E-37 | Si una proyección o un guardado responde `404` con `customer_not_found`, entonces el sistema deberá mostrar la vista «Cliente no encontrado». | R-17 |
| E-23 | Mientras la proyección del valor actual no esté disponible, haya un campo no válido o se esté guardando, el sistema deberá mantener desactivado el botón de guardar. | R-12 |
| E-24 | Cuando el guardado responde `201`, el sistema deberá navegar al detalle del cliente. | R-05, R-11 |
| E-25 | Si el guardado falla con un error distinto de `customer_not_found`, entonces el sistema deberá mostrar el error y conservar los valores del formulario. | R-17 |
| E-48 | Si la proyección o el guardado responde `422`, entonces el sistema deberá mostrar cada error junto a su campo cuando el campo está en el formulario, y en el aviso general cuando no lo está. | A14, R-17 |
| E-49 | El sistema deberá enviar como `customer_id` de la proyección y del guardado el `id` del cliente cargado, y los valores de los campos numéricos como números JSON enteros. | R-12, A14 |
| E-55 | Si el guardado agota el tiempo de espera, entonces el sistema deberá avisar de que la simulación puede haberse guardado y ofrecer un enlace al detalle del cliente, además de «Reintentar». | R-17 |

### Divisas

| Id | Requisito | Cubre |
|---|---|---|
| E-26 | Cuando arranca la aplicación, el sistema deberá pedir una sola vez a la API pública los tipos de EUR a USD, GBP y CHF, directamente desde el navegador. | R-09, A8 |
| E-27 | Cuando se elige otra divisa, el sistema deberá mostrar al momento todos los importes visibles convertidos, sin hacer ninguna petición. | R-09 |
| E-28 | Mientras la divisa elegida es EUR, el sistema deberá mostrar los importes exactos en céntimos, sin depender de la API de divisas. | A8 |
| E-29 | Mientras la divisa elegida no es EUR, el sistema deberá mostrar el tipo aplicado, su fecha tal como la da la API, sin convertirla de zona horaria, y el total en EUR. | A8 |
| E-30 | Si la API de divisas falla, tarda más de 5 s o devuelve una respuesta no válida, entonces el sistema deberá mostrar un aviso, presentar los importes en EUR y ofrecer un botón para reintentar, manteniendo utilizable el resto de la aplicación. | R-17, A8 |
| E-31 | El sistema no deberá enviar al backend ni guardar ningún importe convertido ni la divisa elegida. | A8 |

### Estados

| Id | Requisito | Cubre |
|---|---|---|
| E-32 | El sistema deberá mostrar de forma distinguible los estados de carga, error y datos de cada llamada remota. | R-17 |
| E-33 | Si una llamada al backend no responde en 10 s, entonces el sistema deberá pasar al estado de error. | R-17 |
| E-34 | Si la ruta no corresponde a ninguna vista, entonces el sistema deberá mostrar la página «no encontrada» con un enlace al panel. | — |
| E-42 | Si una llamada al backend responde `503` con `service_unavailable`, entonces el sistema deberá mostrar el aviso de servicio no disponible, distinto del de error inesperado, con un botón «Reintentar». | R-17, A14 |
| E-43 | Si una llamada al backend responde con un error que su vista no trata por su `code` (un `500`, un `400`, un `415`, un `405`, un `404` con `not_found`, un código que el frontend no conoce o un error sin `code`), entonces el sistema deberá mostrar el aviso de error inesperado con un botón «Reintentar» y conservar en el estado de error el `code` recibido, o `unknown_error` si no lo hay. | R-17, A14 |
| E-52 | El sistema deberá llamar al backend solo con `GET` y `POST`, sin cabeceras propias y con cuerpos JSON, y no deberá leer ninguna cabecera de sus respuestas. | A16 |
| E-57 | Cuando el usuario abre el panel, el alta, el detalle o el simulador, el sistema deberá poner como título del documento el nombre de esa vista seguido del nombre de la aplicación. | — |

## 4. Contratos consumidos

### 4.1 Backend

| Llamada | Desde | Spec | Respuestas propias |
|---|---|---|---|
| `GET /meta` | Al arrancar la aplicación. La usan el panel, el detalle y el simulador (nombres de país y plan) y el alta (desplegables) | SPEC-01, 4.4 | `200`. No lee la base de datos y no responde `503` |
| `GET /customers?q=` | Panel | SPEC-01, 4.3 | `200` con `items`; `422` (el frontend no debería provocarlo: 2.2); `503` |
| `POST /customers` | Alta | SPEC-01, 4.1 | `201`; `422` con `errors`; `409` `customer_already_exists`; `503` |
| `GET /customers/{id}` | Detalle, simulador (nombre y país del cliente) | SPEC-01, 4.2, y SPEC-03, 4.2 | `200`; `404` `customer_not_found`; `422` (el frontend no debería provocarlo: 2.1); `503` |
| `POST /pricing/quote` | Simulador | SPEC-02, 4 | `200`; `404` `customer_not_found`; `422`; `500` `tax_rate_not_defined`; `503` |
| `POST /simulations` | Simulador | SPEC-03, 4.1 | `201`; `404` `customer_not_found`; `422`; `500` `tax_rate_not_defined`; `503` |

`/meta` se pide una vez, al arrancar, y se guarda en memoria durante la
sesión (2.1).

La columna «Respuestas propias» recoge los estados que el OpenAPI del
backend declara para cada operación (`/openapi.json`, leído el 2026-11-14
con la aplicación arrancada). Además, cualquier llamada puede recibir los
errores genéricos de las convenciones comunes; qué muestra el frontend con
cada uno está en 2.7. El `422` del buscador y el del cliente no son
respuestas que el frontend deba provocar (2.2 y 2.1) y se tratan como
error genérico.

**Las interfaces de `core/` se escriben a mano a partir de las specs**
(ADR-001), no se generan del OpenAPI. Campos que llegan y el frontend no
usa:

| Campo | Dónde llega | Por qué no se usa |
|---|---|---|
| `tax_rate_bp` de cada país | `GET /meta` | El frontend no calcula impuestos (ADR-002). El tipo que se muestra es el de la proyección o el de la simulación guardada |
| `currency` | Proyección y simulaciones | Los importes del backend son siempre céntimos de euro (convenciones comunes); la divisa que se muestra la elige el usuario (2.6) |
| `country` y `customer_id` | Proyección y simulaciones | El país que se muestra es el del cliente (2.4 y 2.5) |
| `active_users` | Proyección | La interfaz muestra el valor del formulario; la petición anterior se cancela, así que la respuesta es la del valor actual (2.5) |

### 4.2 API de divisas

Petición: `GET https://api.frankfurter.dev/v2/rates?base=EUR&quotes=USD,GBP,CHF`

Respuesta `200` real (`application/json; charset=utf-8`), obtenida con curl
el 2026-11-12 a las 14:53:

```json
[{"date":"2026-11-12","base":"EUR","quote":"CHF","rate":0.92316},{"date":"2026-11-12","base":"EUR","quote":"GBP","rate":0.83583},{"date":"2026-11-12","base":"EUR","quote":"USD","rate":1.1139}]
```

Con una divisa inexistente (`quotes=XXX`) respondió `422` con
`{"status":422,"message":"invalid currency: XXX"}`.

**Comprobada de nuevo el 2026-11-14 a las 09:29, sábado**, con curl y la
cabecera `Origin: http://localhost:4200`: `200`, el mismo tipo de contenido
y la misma forma, con los tipos de ese día:

```json
[{"date":"2026-11-14","base":"EUR","quote":"CHF","rate":0.92491},{"date":"2026-11-14","base":"EUR","quote":"GBP","rate":0.83559},{"date":"2026-11-14","base":"EUR","quote":"USD","rate":1.1083}]
```

El ejemplo del día 12 sigue siendo el de los casos de prueba (5.1, 5.2 y
5.5): los tests no salen a la red y no dependen del tipo del día.

| Dato | Estado |
|---|---|
| Sin clave ni registro; sin cuota diaria ni mensual | **Verificado** en la documentación (<https://frankfurter.dev/>, leída el 2026-11-12) |
| Forma de la respuesta de la `v2` | **Verificado** con las dos peticiones de arriba |
| La `v1` está declarada obsoleta en favor de la `v2` | **Verificado** en la documentación; por eso se usa la `v2` (D-01). El 2026-11-14 la `v1` responde además con una cabecera `deprecation` |
| El navegador puede llamarla (CORS) | **Verificado** el 2026-11-12 con curl y la cabecera `Origin: http://localhost:4200`: la `v2` y la `v1` responden `access-control-allow-origin: *` y `access-control-allow-methods: GET, OPTIONS`. Lo comprobó también el Tech Lead. **Verificado otra vez el 2026-11-14**: las mismas dos cabeceras, y una comprobación previa `OPTIONS` responde `200` con ellas. No se ha probado desde un navegador real |
| La respuesta se puede servir desde caché | **Verificado**: la cabecera fue `cache-control: public, max-age=36362` el día 12 y `cache-control: public, max-age=55805, stale-if-error=86400` el día 14; por eso se muestra la fecha de cada tipo |
| Límite de peticiones por segundo | **No declarado** por la documentación |
| Que los tres tipos traigan siempre la misma fecha | **No verificado**: en las dos lecturas coincidían; la documentación dice que agrega varias fuentes |
| Comportamiento en fines de semana | **Verificado solo para un sábado**, el 2026-11-14: la API responde igual y los tres tipos traen la fecha de ese mismo día |
| Comportamiento en festivos | **No verificado**: la documentación no lo dice |

### 4.3 Limitaciones del backend y lo que el frontend envía

Las limitaciones conocidas del backend
([`limitaciones-conocidas.md`](../04-calidad/limitaciones-conocidas.md))
dependen de lo que un cliente le envíe. Esto es lo que el frontend envía y
por qué no las alcanza:

| Limitación del backend | Lo que envía el frontend |
|---|---|
| **L-01**: el cuerpo de una petición no tiene límite de tamaño | Ningún cuerpo pasa de unos pocos kilobytes: el nombre y el email se envían recortados y la ayuda los acota a 120 y a 254 caracteres, el identificador a 30 sin recortar (2.3), y los demás campos son códigos de `/meta` o números |
| **L-02**: el OpenAPI publica los límites numéricos como decimales, y el máximo de un `id`, inexacto | Las interfaces y los límites del frontend salen de las specs, no del OpenAPI. Todos los importes y máximos del contrato caben exactos en un número de JavaScript; los `id`, hasta 2^53 − 1 (2.1) |
| **L-03**: una clave repetida en el cuerpo se acepta y gana la última | El cuerpo se serializa a partir de un objeto, que no puede repetir una clave |
| **L-04**: con un `q` repetido solo se valida y se usa el último | El buscador envía un solo `q`, o ninguno (2.2) |
| **L-05**: un entero de más de 4300 dígitos en el cuerpo responde `400` | Ningún número que envía el frontend pasa de 16 dígitos: los campos numéricos se validan antes de enviar (2.5) y el `id` de la ruta se filtra (2.1) |

La sexta limitación de ese documento, **L-06**, no es del backend sino del
frontend: el `id` por encima de 2^53 − 1 (2.1).

## 5. Casos de prueba

### 5.1 Conversión y formato

Tipos del ejemplo de 4.2. Los valores se calcularon con Node 24 y su
`Intl.NumberFormat('es-ES', { style: 'currency', currencyDisplay: 'code' })`.
El separador entre el número y el código es un espacio de no separación.

| Céntimos | EUR | USD (1,1139) | GBP (0,83583) | CHF (0,92316) | Qué demuestra |
|---|---|---|---|---|---|
| 0 | 0,00 EUR | 0,00 USD | 0,00 GBP | 0,00 CHF | Cero |
| 1 | 0,01 EUR | 0,01 USD | 0,01 GBP | 0,01 CHF | Un céntimo |
| 5 | 0,05 EUR | 0,06 USD | 0,04 GBP | 0,05 CHF | Céntimos de una cifra: el EUR lleva el cero delante (`0,05`) |
| 1000 | 10,00 EUR | 11,14 USD | 8,36 GBP | 9,23 CHF | Redondeo hacia arriba y hacia abajo |
| 14000 | 140,00 EUR | 155,95 USD | 117,02 GBP | 129,24 CHF | Base del ejemplo del encargo |
| 2940 | 29,40 EUR | 32,75 USD | 24,57 GBP | 27,14 CHF | Su impuesto |
| 16940 | 169,40 EUR | 188,69 USD | 141,59 GBP | 156,38 CHF | Su total |
| 123450 | 1234,50 EUR | 1375,11 USD | 1031,83 GBP | 1139,64 CHF | Cuatro cifras: sin punto de millar, como lo da `es-ES` |
| 60520570 | 605.205,70 EUR | 674.138,63 USD | 505.849,08 GBP | 558.701,69 CHF | Separador de miles |

**Diferencia de un céntimo**: en USD, 155,95 + 32,75 = 188,70, pero el total
convertido es 188,69. Es el caso que la interfaz avisa como orientativo. En
EUR, 140,00 + 29,40 = 169,40 siempre.

**Tipo de cambio** (hasta 6 decimales, con coma). Valores calculados con
Node 24 el 2026-11-14:

| Tipo recibido | Se muestra | Qué demuestra |
|---|---|---|
| `1.1139` | 1,1139 | Cuatro decimales: no se redondea a tres |
| `0.92316` | 0,92316 | Cinco decimales |
| `1.12345678` | 1,123457 | Más de seis: se redondea al sexto |
| `1` | 1 | Sin decimales de relleno |

**Rótulos de los tramos**, con el desglose del ejemplo de SPEC-02 (4): «del
1 al 10», «del 11 al 50» y «del 51 en adelante».

### 5.2 API de divisas

| Situación | Selector | Importes | Aviso |
|---|---|---|---|
| Respuesta de 4.2 | Cuatro divisas | En la divisa elegida | No |
| Petición en curso | Solo EUR | En EUR | «Cargando tipos» |
| Error de red | Solo EUR | En EUR | Sí, con «Reintentar» |
| Sin respuesta en 5 s | Solo EUR | En EUR | Sí |
| `404`, `422` o `500` | Solo EUR | En EUR | Sí |
| Lista sin el objeto de `GBP` | Solo EUR | En EUR | Sí: una respuesta parcial es un error |
| Lista con dos objetos de `USD` | Solo EUR | En EUR | Sí: debe haber exactamente uno |
| Lista vacía | Solo EUR | En EUR | Sí |
| `rate` `0`, negativo, `null` o `"1.1"` en una divisa | Solo EUR | En EUR | Sí |
| `base` distinto de `EUR` en una divisa | Solo EUR | En EUR | Sí |
| `date` ausente o sin forma de fecha en una divisa | Solo EUR | En EUR | Sí |
| Un objeto (como el de la `v1`) en lugar de una lista | Solo EUR | En EUR | Sí |
| Lista válida con un objeto añadido de `JPY` | Cuatro divisas | En la divisa elegida | No: lo no pedido se ignora |
| Cuerpo que no es JSON | Solo EUR | En EUR | Sí. El estado es de error; su `code` puede ser `invalid_rates` o `unknown_error` |
| Error y después «Reintentar» con éxito | Cuatro divisas | En la divisa elegida | Desaparece |
| Cambio de divisa diez veces | — | Se actualizan | Ninguna petición nueva |

En todas las filas de error, el buscador, el detalle y el simulador siguen
funcionando.

En la fila del cuerpo que no es JSON lo que se exige es el **estado de
error**, no un `code` concreto: si el cliente HTTP entrega el texto, lo
rechaza la validación (`invalid_rates`); si falla antes, al leer el JSON,
el error es el genérico (`unknown_error`). La interfaz es la misma en los
dos casos, porque el selector y el aviso deciden por el estado.

### 5.3 Buscador

| Acción | Peticiones | Resultado |
|---|---|---|
| Abrir el panel | 1, sin `q` | Listado inicial |
| Escribir `eje` deprisa (tres pulsaciones en menos de 300 ms) | 1, con `q=eje` | Lista |
| Escribir `eje`, esperar, añadir `m` antes de que responda | 2; la primera se cancela | Solo se muestra la respuesta de `ejem` |
| La respuesta a una búsqueda con texto (`q=noexiste`) trae `items: []` | — | «No hay clientes que coincidan» |
| Abrir el panel con la base de datos recién creada: el listado inicial, sin `q`, trae `items: []` | 1, sin `q` | «Todavía no hay clientes», con el acceso al alta; no «No hay clientes que coincidan» |
| La respuesta trae 20 clientes | — | La lista y, bajo ella, «Se muestran como máximo 20 clientes. Escribe más texto para afinar la búsqueda.» |
| La respuesta trae 19 clientes | — | La lista, sin esa nota |
| La respuesta trae tres clientes en este orden: `Zeta Datos SL`, `alfa Ejemplo SA` y `Ñandú Pruebas SL` | — | Se muestran en ese mismo orden, que no es el alfabético: el frontend no reordena |
| Un resultado con `country` `ES` y `plan` `professional` | — | Se muestra «España» y «Profesional» |
| Un resultado con `country` `XX` y `plan` `legacy`, que `/meta` no trae | — | Se muestra `XX` y `legacy`, tal como llegan y sin marca |
| `/meta` falla | — | Error con «Reintentar» en lugar del buscador y de la lista; no se muestra ningún código |
| `/meta` falla y después «Reintentar» con éxito | 1 más a `/meta` | El panel muestra el listado inicial, con nombres |
| `/meta` tarda más en responder que el listado inicial | 1 a `/customers`, sin esperar a `/meta`; ninguna más cuando `/meta` llega | Estado de carga hasta que llega `/meta`; después, el listado con nombres |
| Navegar del panel al detalle y volver, con `/meta` ya cargado | Ninguna nueva a `/meta` | Se pide una sola vez por sesión |
| La petición falla | — | Aviso con «Reintentar»; al pulsarlo se repite la misma búsqueda |
| Borrar el texto después de una búsqueda | 1, sin `q` | Listado inicial |
| Escribir tres espacios | 1, con un `q` de tres espacios (`q=%20%20%20`) | Lo que devuelve la API, que para ese texto es el listado inicial |
| Escribir `100% a+b&c#d` | 1; el parámetro `q` vale exactamente ese texto y la URL lleva `q=100%25%20a%2Bb%26c%23d` | Lo que devuelve la API |
| Escribir 100 veces el emoji U+1F600 (100 puntos de código, 200 unidades UTF-16) | 1 | Lo que devuelve la API: el texto está dentro del límite |
| Escribir 101 caracteres `x` | 0 | Aviso del límite junto al campo; sin lista |
| Escribir 100 caracteres `x` y un espacio | 0 | Aviso del límite: se mide sin recortar, como el backend |
| Con el aviso del límite a la vista, borrar hasta 100 caracteres | 1 | Desaparece el aviso; lo que devuelve la API |
| Escribir `a`, un *surrogate* suelto (U+D800) y `b` | 1, con `q` igual a `a`, U+FFFD y `b` | Lo que devuelve la API |
| Escribir `eje`, esperar a que salga su petición y, antes de que responda, pegar un texto de 101 caracteres | La de `eje` se cancela; ninguna nueva | El aviso del límite sale al momento, sin esperar 300 ms; sin lista, y la respuesta de `eje` no llega a pintarse |

### 5.4 Alta: respuesta → interfaz

| Respuesta | Interfaz |
|---|---|
| `201` con `id` 7 | Navega a `/clientes/7` |
| `422`, `tax_id` · `invalid_tax_id_format` | Mensaje junto al identificador; resto de campos intactos |
| `422`, `tax_id` · `invalid_tax_id_check_character` | Mensaje junto al identificador, distinto del anterior |
| `422`, errores en `company_name` y `contact_email` a la vez | Los dos mensajes, cada uno en su campo |
| `422`, `field` desconocido | Mensaje en el aviso general |
| `409` `customer_already_exists` | Aviso de cliente existente; no navega |
| `500` o sin conexión | Aviso general con «Reintentar» |
| Doble clic en «Guardar» | Una sola petición |
| `/meta` falla | Error con «Reintentar»; sin formulario enviable |
| `/meta` responde con el ejemplo de SPEC-01 (4.4) | Los desplegables ofrecen exactamente sus nueve países y sus tres planes, con sus nombres («España», «Básico») y en su orden, y ninguna otra opción que se pueda elegir: la primera de cada uno, «Elige un país» y «Elige un plan», está desactivada; lo que se envía al elegir uno es su código (`ES`, `starter`) |
| Escribir un nombre de un solo carácter sin haber pulsado «Guardar» | Ningún mensaje de ayuda: calla hasta el primer intento de envío |
| `422` en el identificador y, después, se cambia el identificador | El mensaje del backend se retira |
| `500`, se cambia el nombre y se pulsa «Reintentar» | Se envía el nombre nuevo: «Reintentar» envía lo que el formulario tiene en ese momento |
| «Guardar» sin nombre y sin email | No se envía; el foco va al nombre, el primer campo con error |
| «Guardar» con solo el email mal | No se envía; el foco va al email |
| `422` con errores en `company_name` y `contact_email` | El foco va al nombre |
| `422` con un error en `plan` | El foco va al desplegable del plan |
| `409`, `500` o un `422` con solo un `unknown_field` | El foco no se mueve: ningún campo tiene error |
| Nombre de 61 caracteres `𝔸` (U+1D538; 61 puntos de código, 122 unidades UTF-16) | La ayuda no lo rechaza: se envía |
| Nombre de 121 caracteres `ñ` | Error de ayuda junto al campo; no se envía |
| Nombre `A` rodeado de espacios U+0020 | Error de ayuda: un carácter tras recortar; no se envía |
| Nombre `AB` precedido de un tabulador | La ayuda no recorta el tabulador ni lo rechaza: se envía, y el `422` `invalid_characters` del backend se muestra junto al campo |
| Nombre `  Ejemplo Uno SL ` (con espacios U+0020 en los extremos) | Se envía recortado, `Ejemplo Uno SL`; el detalle muestra el nombre que devuelve el backend |
| Nombre `AB` seguido de un espacio de no separación (U+00A0) | Se envía tal cual: solo se recorta U+0020 |
| Nombre `AB` seguido de un *surrogate* suelto (U+D800) | Error de ayuda junto al campo; no se envía |
| Email `josé@empresa.example` | La ayuda no lo rechaza: se envía (el backend lo acepta) |
| Email `a@b` | La ayuda no lo rechaza: se envía, y el `422` `invalid_email` del backend se muestra junto al campo |
| Email `a`, U+00A0 y `b@c.example` | La ayuda no lo rechaza: se envía, y el `422` `invalid_email` del backend se muestra junto al campo |
| Email `sin-arroba.example`, `@b.example` o `a@` | Error de ayuda junto al campo; no se envía |
| Email de 255 caracteres tras recortar | Error de ayuda junto al campo; no se envía |
| Email de 254 caracteres rodeado de espacios U+0020 | La ayuda no lo rechaza: se envía recortado |
| Identificador `12345678Z` seguido de 21 espacios (30 caracteres) | La ayuda no lo rechaza: se envía tal cual, con sus espacios |
| Identificador `12345678Z` seguido de 22 espacios (31 caracteres) | Error de ayuda junto al campo; no se envía |
| Identificador de solo espacios | La ayuda no lo rechaza (no está vacío): se envía, y el `422` `invalid_tax_id_format` del backend se muestra junto al campo |
| `422` con un error en `plan` y un `unknown_field` en `zeta` | El de `plan`, junto a su campo; el de `zeta`, en el aviso general |
| `422` con un error en `plan` y una entrada de `errors` sin `message` | El de `plan`, junto a su campo; la entrada sin la forma del contrato se ignora |
| `422` con dos errores en `tax_id` | El primero, junto al identificador; el segundo, en el aviso general |
| `422` cuyo `errors` no trae ninguna entrada con la forma del contrato | Aviso general de error inesperado; el formulario conserva lo escrito |
| `503` `service_unavailable` | Aviso general de servicio no disponible, con «Reintentar»; el formulario conserva lo escrito |
| `201` sin cabecera `Location` legible, con `id` 7 en el cuerpo | Navega a `/clientes/7` |

### 5.5 Simulador

Con un cliente de `ES`; los importes son los de la tabla 5.1 de SPEC-02.

| Acción | Peticiones a `/pricing/quote` | Interfaz |
|---|---|---|
| Abrir el simulador | 1, con 10 usuarios | Total 121,00 EUR; se muestra «España», no `ES` |
| Abrir el simulador y el cliente tarda 500 ms en responder | 0 mientras no llega el cliente; 1, con 10 usuarios, cuando llega | Estado de carga hasta entonces |
| `/meta` falla | — | Error con «Reintentar» en lugar del simulador; no se muestra el código del país |
| Arrastrar el control de 10 a 15 pasando por 11–14 en menos de 200 ms | 1, con 15 | Total 169,40 EUR |
| Con el total de 10 usuarios a la vista, mover a 15, y la respuesta tarda | 1, en curso | Mientras llega, los importes de 10 usuarios siguen a la vista marcados como «actualizando» y «Guardar» está desactivado; al llegar, total 169,40 EUR y «Guardar» activo |
| Mover a 51 mientras la de 15 sigue en curso | La de 15 se cancela | Solo se muestra la de 51: 514,25 EUR |
| Escribir `20000` en el campo numérico | 1, con 20000 | El control deslizante queda en su máximo (500); se proyecta 20.000: total 121.205,70 EUR |
| Escribir `-1`, `1,5`, `100001` o dejarlo vacío | 0 | Error junto al campo; sin importes; «Guardar» desactivado |
| Escribir `15.0`, `1e3`, `+15`, `1 5` o `100000.000000000001` en el campo de usuarios | 0 | Error junto al campo; sin importes; «Guardar» desactivado: decide el texto, no el número que resulta |
| La proyección falla | — | Sin importes; aviso con «Reintentar»; «Guardar» desactivado |
| Con la proyección fallida, pulsar «Reintentar» | 1, al momento, con los usuarios escritos | Al llegar, los importes vuelven y el aviso se retira |
| Con el total de 10 usuarios a la vista, escribir 15, antes de que pasen los 200 ms | 0 todavía | Los importes de 10 usuarios ya están marcados como «actualizando» y «Guardar», desactivado |
| «Guardar» falla con `500` y se pulsa «Reintentar» | — | Una petición nueva a `/simulations` con lo que el formulario tiene en ese momento |
| Cambiar almacenamiento o llamadas | 0 | La proyección no cambia |
| Escribir `-1`, `1,5`, `2.0` o `1e2` en almacenamiento, con una proyección visible | 0 | Error junto al campo; la proyección sigue a la vista; «Guardar» desactivado |
| Abrir `/clientes/999/simulacion` (el cliente responde `404`) | 0 | Vista «Cliente no encontrado» |
| Abrir `/clientes/abc/simulacion` (el `id` no tiene la forma de 2.1) | 0, y tampoco se pide el cliente | Vista «Cliente no encontrado» |
| Abrir `/clientes/7/simulacion` y proyectar | 1, con `customer_id` 7 (el `id` del cliente cargado) y `active_users` 10, los dos como números JSON | Total 121,00 EUR |
| Escribir `015` en el campo de usuarios | 1, con `active_users` 15, sin decimales en el cuerpo | Total 169,40 EUR: son solo dígitos y valen 15 |
| Una proyección responde `422` con `active_users` · `out_of_range` | — | El mensaje del backend junto al campo de usuarios; sin importes; «Guardar» desactivado |
| «Guardar» con `422`: `storage_gb` · `out_of_range` y `customer_id` · `out_of_range` | — | El primero, junto al campo de almacenamiento; el segundo, en el aviso general; los valores se conservan |
| Una proyección responde `404` `customer_not_found` | — | Vista «Cliente no encontrado» |
| Con USD elegido, la fecha del tipo es `2026-11-12` y el navegador está en una zona con desfase negativo | 0 | Se muestra «12/11/2026», no el día anterior |
| Cambiar la divisa a USD con 15 usuarios | 0 | Total 188,69 USD, con el tipo, su fecha y 169,40 EUR |
| «Guardar» con respuesta `201` | — | Navega al detalle; la simulación nueva es la primera |
| Pulsar «Guardar» y, antes de que llegue la respuesta, pulsarlo otra vez | — | Una sola petición a `/simulations`: «Guardar» está desactivado mientras se guarda |
| «Guardar» con `500` o `503` | — | El aviso que le corresponde (2.7); los valores se conservan |
| «Guardar» y la respuesta no llega en 10 s (`timeout`) | — | Aviso de que la simulación puede haberse guardado, con «Reintentar» y un enlace al detalle del cliente; los valores se conservan |
| «Guardar» con `404` `customer_not_found` | — | Vista «Cliente no encontrado» |

### 5.6 Errores del backend

Las respuestas se construyen con la forma del ejemplo de error de las
convenciones comunes (índice de specs) y los códigos de su tabla de errores
genéricos. Los avisos son los de la tabla de 2.7.

| Llamada | Respuesta | Interfaz |
|---|---|---|
| `GET /customers` (panel) | `503` `service_unavailable` | Aviso de servicio no disponible con «Reintentar», en lugar de la lista; al pulsarlo se repite la misma búsqueda |
| `GET /customers/{id}` (detalle y simulador) | `503` `service_unavailable` | Aviso de servicio no disponible con «Reintentar»; **no** la vista «Cliente no encontrado» |
| `POST /customers` | `503` `service_unavailable` | Aviso general de servicio no disponible; el formulario conserva lo escrito y no navega |
| `POST /pricing/quote` | `503` `service_unavailable` | Proyección en estado de error: sin importes, aviso de servicio no disponible con «Reintentar» y «Guardar» desactivado |
| `POST /simulations` | `503` `service_unavailable` | Aviso de servicio no disponible; los valores se conservan |
| `GET /meta` responde `200` y `GET /customers`, `503` | — | El panel muestra el aviso de servicio no disponible de su lista; `/meta` no lee la base de datos y no falla con ella |
| Cualquiera | `500` `internal_error` | Aviso de error inesperado con «Reintentar», distinto del de servicio no disponible |
| `POST /pricing/quote` o `POST /simulations` | `500` `tax_rate_not_defined` | Aviso de error inesperado; el estado de error lleva `tax_rate_not_defined` |
| Cualquiera | `400` `malformed_request`, `415` `unsupported_media_type` o `405` `method_not_allowed` | Aviso de error inesperado con «Reintentar»; el estado de error lleva el `code` recibido |
| `GET /customers/{id}` | `404` `not_found` | Aviso de error inesperado, **no** «Cliente no encontrado» |
| `GET /customers` o `GET /customers/{id}` | `422` `validation_error` | Aviso de error inesperado con «Reintentar»; en la del cliente, **no** «Cliente no encontrado» |
| Cualquiera | Un `code` que el frontend no conoce (`teapot`) | Aviso de error inesperado; el estado de error lleva `teapot` |
| Cualquiera | `502` con un cuerpo que no es JSON | Aviso de error inesperado; el estado de error lleva `unknown_error` |
| Cualquiera | Error de red | Aviso de falta de conexión con «Reintentar»; el estado de error lleva `network_error` |
| Cualquiera | Sin respuesta en 10 s | Aviso de espera agotada con «Reintentar»; el estado de error lleva `timeout` |
| Cualquiera | El mismo `503` con otro `detail` | La interfaz no cambia: decide el `code` (E-11) |

### 5.7 El `id` de la ruta

Cada fila vale para el detalle (`/clientes/…`) y para el simulador
(`/clientes/…/simulacion`). En el simulador, además, solo las tres
primeras filas, las que cargan el cliente 1, llegan a pedir una
proyección.

Lo que responde el backend a `1`, `999`, `abc`, `01`, `+1`, `1.0`, `1_0`,
el `1` con un espacio, `0` y `-1` está en SPEC-01, 5.10. Los demás textos
de esta tabla no tienen fila allí y se sondearon el 2026-11-14 con el
cliente de test: `1e0` y el dígito U+0661 responden `422` con
`not_an_integer`; 9007199254740991, 9007199254740993 y el de 17 dígitos,
`404` con `customer_not_found`, porque para el backend son `id` válidos de
clientes que no existen.

| Ruta | Peticiones del cliente | Interfaz |
|---|---|---|
| `/clientes/1` (existe) | 1, a `/customers/1` | El detalle del cliente 1 |
| `/clientes/%31` (el `1` escrito con `%`) | 1, a `/customers/1` | El detalle del cliente 1: el filtro ve el segmento ya descodificado por el router (2.1) |
| `/clientes/1;x=y` (con un parámetro de matriz) | 1, a `/customers/1` | El detalle del cliente 1: el parámetro de matriz no forma parte del `id` (2.1) |
| `/clientes/999` (el backend responde `404` `customer_not_found`) | 1, a `/customers/999` | «Cliente no encontrado» |
| `/clientes/abc` | 0 | «Cliente no encontrado» |
| `/clientes/01` | 0 | «Cliente no encontrado»: el cliente 1 solo tiene una dirección, `/clientes/1` |
| `/clientes/+1`, `/clientes/1.0`, `/clientes/1e0`, `/clientes/1_0` y `/clientes/1%20` (un espacio detrás) | 0 | «Cliente no encontrado» |
| `/clientes/0` y `/clientes/-1` | 0 | «Cliente no encontrado» |
| `/clientes/١` (un dígito que no es ASCII, U+0661) | 0 | «Cliente no encontrado» |
| `/clientes/9007199254740991` (2^53 − 1; el backend responde `404`) | 1, a `/customers/9007199254740991`, con ese texto exacto | «Cliente no encontrado» |
| `/clientes/9007199254740993` (16 dígitos, por encima de 2^53 − 1) | 0 | «Cliente no encontrado»: JavaScript no lo representa exacto (limitación L-06) |
| `/clientes/99999999999999999` (17 dígitos) | 0 | «Cliente no encontrado» |
| `/clientes/7`, y el backend responde `422` | 1 | Aviso de error inesperado (2.7), **no** «Cliente no encontrado» |
| `/clientes/7`, y el backend responde `404` `not_found` | 1 | Aviso de error inesperado (2.7), **no** «Cliente no encontrado» |

## 6. Criterios de aceptación

| Id | Criterio | Requisitos |
|---|---|---|
| CA-01 | Un test parametrizado del *pipe* de importes reproduce cada celda de la tabla de importes de 5.1, incluido el caso del céntimo de diferencia, y otros dos reproducen la tabla del tipo de cambio y los rótulos de los tramos. | E-28, E-29 |
| CA-02 | Tests del servicio de divisas, con las utilidades de test de `HttpClient`, reproducen cada fila de 5.2 y comprueban que solo hay una petición por sesión salvo reintento. | E-26, E-27, E-30 |
| CA-03 | Un test comprueba que, con la API de divisas en error, el panel, el detalle y el simulador muestran sus datos en EUR. | E-28, E-30 |
| CA-04 | Tests del buscador con temporizadores simulados reproducen cada fila de 5.3, comprobando el número de peticiones, el parámetro `q` y la URL de cada una, y cuál se muestra. | E-01 a E-04, E-35, E-39, E-40, E-50, E-51, E-53, E-54 |
| CA-05 | Tests del formulario de alta reproducen cada fila de 5.4, simulando las respuestas con los ejemplos de SPEC-01, apartado 4.1 (el `201`, el `409` y los tres `422`); las demás se construyen con esa misma forma y los códigos de su tabla de errores. De cada fila que se envía, el test comprueba además el cuerpo de la petición. | E-05, E-07 a E-11, E-40, E-41, E-44 a E-46, E-56 |
| CA-06 | Un test comprueba que cambiar el `message` de una respuesta de error sin cambiar su `code` no altera el comportamiento de la interfaz. | E-11 |
| CA-07 | Tests del detalle cubren: cliente con simulaciones (orden de la API), sin simulaciones, con `simulation_count` mayor que las recibidas (55 y 50: «Se muestran las 50 últimas de 55»), `404` con `customer_not_found`, país y plan con los nombres de `/meta`, un país que `/meta` no trae (se muestra su código), y `/meta` en error (error con «Reintentar», sin códigos). | E-12 a E-15, E-35, E-40 |
| CA-08 | Tests del simulador con temporizadores simulados reproducen cada fila de 5.5. Las respuestas se construyen con la forma de los ejemplos de SPEC-02 (4) y SPEC-03 (4.1) y los importes de las filas de 10, 15, 51 y 20000 usuarios de la tabla 5.1 de SPEC-02. De cada petición, el test comprueba además el cuerpo enviado. | E-15, E-17, E-18, E-20 a E-25, E-27, E-29, E-35 a E-38, E-40, E-48, E-49, E-55 |
| CA-09 | Un test recorre los cuerpos de todas las peticiones al backend durante un alta y un guardado con la divisa en USD, y comprueba que no contienen ni la divisa ni importes. | E-31 |
| CA-10 | De cada servicio de `core/` hay tests de sus tres estados (carga, error, datos) y del paso a error por tiempo agotado. | E-32, E-33 |
| CA-11 | Un test de rutas comprueba las cinco filas de 2.1, incluida la página «no encontrada», y el título del documento de cada una de las cuatro vistas. | E-34, E-57 |
| CA-12 | El evaluador independiente comprueba que `frontend/src` no contiene la tarifa, los tipos impositivos, la tabla de letras del DNI ni el cálculo del CIF. | E-06, E-19 |
| CA-13 | Una prueba de Playwright comprueba que, a 375 px de ancho, ninguna de las cuatro vistas (panel, alta, detalle y simulador) tiene desplazamiento horizontal. | E-16 |
| CA-14 | Una prueba de Playwright de principio a fin, contra el backend y el frontend reales en local, da de alta un cliente, abre el simulador, guarda una simulación y comprueba que aparece la primera en el detalle. Corre contra el backend real con su CORS por defecto: una cabecera de más o un método no admitido harían fallar la comprobación previa del navegador y, con ella, la prueba. | E-08, E-12, E-24, E-52 |
| CA-15 | Capturas generadas con Playwright y revisadas por el Tech Lead de las cuatro vistas a 375 px y a 1280 px, y, a esos mismos anchos, del simulador con otra divisa, de la cabecera con el aviso del fallo de los tipos y del alta con un campo enfocado, para ver el anillo de foco, guardadas en `04-calidad/capturas/` como complemento de CA-13 y de CA-19. | E-16 |
| CA-16 | Tests de los servicios de `core/` reproducen **cada fila** de 5.6, comprobando el `code` del estado de error y el aviso que le corresponde. Cada una de las cuatro vistas, o el servicio que carga sus datos, reproduce **una fila por cada aviso distinto** de 2.7 (servicio no disponible, error inesperado, falta de conexión y espera agotada), comprobando el aviso que se muestra y que hay «Reintentar»; en el servicio, el `code` del estado de error. *Por qué no cada fila en cada vista*: el reparto de `code` a aviso vive en `core/` y se prueba allí fila a fila; repetirlo en cada vista probaría cuatro veces la misma tabla. | E-11, E-42, E-43 |
| CA-17 | Tests del detalle y del simulador reproducen cada fila de 5.7, comprobando el número de peticiones del cliente y la URL exacta de cada una. | E-15, E-47 |
| CA-18 | Un test recorre todas las peticiones al backend de un recorrido completo (panel, búsqueda, alta, detalle, proyección y guardado) y comprueba que su método es `GET` o `POST`, que la petición no lleva ninguna cabecera puesta por la aplicación y que el cuerpo de cada `POST` es un objeto JSON con los campos del contrato y ninguno más. `Accept` y `Content-Type` no se ven en este test: Angular las añade al enviar, no en la petición; que las peticiones reales pasan el CORS del backend lo comprueba CA-14. | E-52 |
| CA-19 | Una prueba de Playwright lee los colores que pinta el navegador (el contorno de un campo enfocado, su borde, su fondo y el fondo de la página) en un campo de texto y un desplegable del alta, en el campo de búsqueda del panel y en el selector de divisa, y comprueba que el contorno y el borde tienen un contraste de 3:1 o más sobre el blanco y sobre el fondo de la página. | — (2.8) |

**Sobre CA-12 a CA-15**: CA-12 es una revisión del evaluador y CA-15, unas
capturas que genera Playwright (`npm run e2e:capturas`) y revisa una
persona; ninguna de las dos la hace el oráculo. CA-13 y CA-14, y también
CA-19, están en
`frontend/e2e/`, con Playwright (D-09): se ejecutan con `npm run e2e` y el
oráculo los pasa con `--e2e`; sin esa opción su comprobación sale como
inactiva, no como correcta. Las pruebas de principio a fin no llaman a la
API real de divisas: la respuesta de 4.2 se da dentro del navegador, para
no depender de la red. **Se responde con el protocolo de depuración de
Chromium y no con `page.route()`**: con una ruta puesta, Playwright
contesta él mismo las comprobaciones previas de CORS, admitiendo lo que se
le pida, y CA-14 no comprobaría el CORS del backend. Por eso las pruebas
solo funcionan en Chromium.

## 7. Decisiones de diseño

Aprobadas o decididas por el Tech Lead el 2026-11-12. La columna «Origen»
dice si aprobó la propuesta de la IA o la cambió.

| Id | Decisión | Origen |
|---|---|---|
| D-01 | **API de divisas**: Frankfurter, versión `v2` (`/v2/rates?base=EUR&quotes=USD,GBP,CHF`). La propia API declara obsoleta la `v1`, y un proyecto nuevo no nace dependiendo de algo obsoleto | Cambiada (la IA proponía la `v1`, la única cuya respuesta había verificado) |
| D-02 | **CORS de la API de divisas**: cerrada. La `v1` y la `v2` devuelven `access-control-allow-origin: *` (4.2) | Cerrada por el Tech Lead, que lo comprobó; la IA lo había dejado sin verificar |
| D-03 | **Divisas ofrecidas**: EUR, USD, GBP y CHF | Aprobada |
| D-04 | **Los tipos se piden una vez al arrancar**, para que el cambio de divisa sea instantáneo | Aprobada |
| D-05 | **Código de divisa en lugar de símbolo** (`188,69 USD`) | Aprobada |
| D-06 | **Cada importe se convierte por separado** y se avisa de que los convertidos son orientativos; no se ajusta el céntimo de diferencia | Aprobada |
| D-07 | **Rutas en español y simulador en ruta propia**: `/clientes/nuevo`, `/clientes/:id`, `/clientes/:id/simulacion` | Aprobada |
| D-08 | **Control deslizante de 0 a 500**, con campo numérico hasta 100.000 y valor inicial 10 | Aprobada |
| D-09 | **Playwright para lo esencial**, con la versión fijada y como dependencia de desarrollo: una prueba de principio a fin (alta → simulador → guardar → la simulación aparece la primera en el detalle) y la ausencia de desplazamiento horizontal a 375 px en las cuatro vistas. Las capturas manuales quedan como complemento en `04-calidad/`. Se implementa en la fase de QA | Cambiada (la IA proponía solo la comprobación manual, para no añadir una dependencia) |
| D-10 | **Tiempos**: 300 ms en el buscador, 200 ms en el simulador, 10 s de espera al backend y 5 s a la API de divisas | Aprobada |
| D-11 | **La divisa elegida no se recuerda al recargar**: vuelve a EUR | Aprobada |
| D-12 | **Mensajes de error de campo**: se muestra el `message` del backend; la lógica solo mira el `code` | Aprobada |
| D-13 | **Validación de ayuda en el navegador** limitada a obligatorios, longitudes, lo mínimo del email (una `@` que no está en un extremo) y que el texto no lleve un *surrogate* suelto. Mide como el backend: puntos de código y recorte solo de U+0020. Solo rechaza lo que el backend rechazaría seguro: sin el validador de email del framework ni del navegador y sin `maxlength` (2.3) | Aprobada; la medida, fijada por el Tech Lead tras la segunda evaluación (N-10) |
| D-14 | **`/meta` se pide una vez al arrancar.** Si falla, el panel, el alta, el detalle y el simulador muestran el error con «Reintentar», sin códigos sueltos; el simulador muestra el nombre del país | Decidida por el Tech Lead tras la segunda evaluación (N-09) |

D-01 y D-02 se registran además como ADR-003, con las alternativas y la
verificación, y la dependencia de D-09 (Playwright) como ADR-005. El
criterio de qué decisiones llevan ADR está en `02-arquitectura/README.md`.

**Sobre D-09**: la versión de Playwright se fija al añadir la dependencia,
en la fase de QA. El 2026-11-12 la última publicada de `@playwright/test`
era la 1.65.0, que declara `node >=20` (consultado con `npm view`). El
2026-11-14 la última es la 1.65.1, publicada el día 13; con el margen de
una semana de ADR-007, la elegible ese día sigue siendo la 1.65.0,
publicada el 2026-11-05 (fechas del registro de npm). No se ha instalado ni
ejecutado.

**Nota del 2026-11-15 sobre D-09** (la decisión y el párrafo anterior se
conservan como se escribieron): Playwright 1.65.0 está instalado y sus
pruebas, en `frontend/e2e/`. A las dos que nombra D-09 se han sumado, por
decisión del Tech Lead, el caso de frontera de la limitación conocida L-09
y la fila de la zona horaria de 5.5. Las capturas de `04-calidad/` ya no
son manuales: las genera Playwright y las revisa el Tech Lead (CA-15). El
detalle, en ADR-005.

## 8. Cambios que provoca en otros documentos

**Aplicados el 2026-11-12.** El Tech Lead había decidido aplicarlos al
aprobar las specs; tras la evaluación independiente (H-01, H-19, H-26)
decidió aplicarlos ya: con todo en borrador, mantener destinos incoherentes
no tiene sentido.

| Documento | Cambio | Estado |
|---|---|---|
| ADR-002 | «unos 200 ms» pasa a 200 ms, fijado aquí (D-10) | Aplicado |
| A8 en `supuestos.md` | La lista de divisas queda cerrada: EUR, USD, GBP y CHF (D-03) | Aplicado |
| A17 en `supuestos.md` | El alta está en una ruta propia, `/clientes/nuevo`, con acceso desde el panel (D-07) | Aplicado |
| SPEC-01, 4.2 y CA-06 | La ficha incluye el historial (apartado 8 de SPEC-03) | Aplicado |

## 9. Pendiente antes de aprobar

**Nada pendiente: el Tech Lead dio su aprobación el 2026-11-14**, aparte
del bloque backend y antes de empezar el frontend, después de decidir los
hallazgos de la evaluación independiente de esta spec y las propuestas de
la sesión 06 (historial). A3 no la bloqueaba: el Tech Lead lo decidió el
2026-11-13 y la
respuesta a la consulta, que llegó ese mismo día, lo confirma: el
almacenamiento y las llamadas a la API no se tarifican; basta con
registrarlos y mostrarlos en la simulación. La consulta está cerrada
(`supuestos.md`).

| Asunto | Qué cambiaría en esta spec |
|---|---|
| A3 · almacenamiento y API | Nada: confirmado. Cambiarlos no pide una proyección nueva (2.5) |
| SPEC-01, SPEC-02 y SPEC-03 | Sus contratos cambiaron el 2026-11-13, después de escribirse esta spec, y el 2026-11-14 se puso al día con ellos (historial). Si vuelven a cambiar: 2.7, 4.1, 4.3 y las tablas de 5.3 a 5.7 |
| Limitación del `id` por encima de 2^53 − 1 (2.1) | Aceptada por el Tech Lead el 2026-11-14 como limitación conocida L-06. Nada pendiente |

## Historial

| Fecha | Cambio |
|---|---|
| 2026-11-12 | Primer borrador |
| 2026-11-12 | Revisión del Tech Lead: la API de divisas pasa a la `v2` de Frankfurter, con su respuesta real en 4.2, la validación de 2.6 adaptada a una lista y las tablas 5.1 y 5.2 recalculadas (D-01); CORS verificado (D-02); Playwright para la prueba de principio a fin y los 375 px, con CA-13 reescrito y nuevos CA-14 y CA-15 (D-09); aprobadas las demás decisiones |
| 2026-11-12 | Correcciones de la evaluación independiente (`04-calidad/evaluacion-specs-01.md`), decididas por el Tech Lead: aplicados los cambios cruzados del apartado 8, incluido A17 (H-01, H-19, H-26); A3, A6, A7 y A12 en la cabecera, con A3 como bloqueo (H-02); CA-08 cita E-29 (H-09); CA-05 y CA-08 dicen de dónde salen las respuestas simuladas (H-14); «Cliente no encontrado» también con `422` y en el simulador, E-37 (H-15); el panel muestra los nombres de `/meta`, E-35 (H-16); la fecha del tipo de cambio se muestra tal cual (H-17); eliminado el escenario inalcanzable del reintento, y un almacenamiento o un número de llamadas no válido ya no retira la proyección, E-36 (H-18); remisión a ADR-003 (H-20); E-06 remite a la regla de frontend y no a ADR-002 (H-25) |
| 2026-11-12 | Correcciones de la segunda evaluación independiente (`04-calidad/evaluacion-specs-02.md`), decididas por el Tech Lead: esta spec se aprueba aparte, después del bloque backend (N-01); el simulador no pide proyecciones mientras el cliente no se ha cargado, con E-18, E-38 y una fila en 5.5 (N-06); la fila de 20000 usuarios tiene respuesta de origen en SPEC-02 5.1 y CA-08 la cita (N-08); `/meta` se pide una vez al arrancar y, si falla, las cuatro vistas muestran el error con «Reintentar», con E-35, E-39, E-40, D-14 y filas en 5.3 y 5.5 (N-09); la ayuda del navegador mide como el backend, con E-41 y cuatro filas en 5.4 (N-10); remisión a ADR-005 (N-14) |
| 2026-11-13 | Decisión del Tech Lead al vencer la fecha límite sin respuesta externa: A3 pasa a `decidido (sin confirmación externa)` con la hipótesis ya documentada, sin cambios en las reglas; cabecera y apartado 9 actualizados. El bloque backend (SPEC-01, SPEC-02 y SPEC-03) queda aprobado ese día; esta spec sigue en `borrador`. La consulta sigue abierta: si la respuesta llega, se aplica como cambio de esta spec |
| 2026-11-13 | Llega la respuesta a la consulta: confirma A3 (no se tarifican; se registran y se muestran). Cabecera y apartado 9 actualizados; la consulta queda cerrada. Motivo: registrar la fuente del supuesto. Sin cambios en reglas, requisitos, criterios ni casos; la spec sigue en `borrador` |
| 2026-11-14 | Puesta al día con el contrato final del backend (sesión 06, divergencias DV-01, DV-02, DV-10 y DV-11), propuesta por la IA y pendiente de la revisión del Tech Lead. **Errores genéricos del backend, por su `code`**: tabla nueva en 2.7 con el aviso de cada uno; el `503` `service_unavailable` tiene un aviso propio, distinto del de error inesperado; el `400`, el `415`, el `405`, el `404` `not_found` y un código desconocido muestran el de error inesperado y dejan su `code` en el estado de error; `tax_rate_not_defined` se trata como `internal_error`. «Cliente no encontrado» se decide por `customer_not_found` y no por el estado `404`, también al guardar (2.4, 2.5, E-15, E-25 y E-37). Requisitos nuevos E-42 y E-43, tabla 5.6, CA-16 y la fila de «Guardar» de 5.5 partida en dos. Motivo: esta spec se escribió el día 12 y el backend fijó el 13 que cualquier endpoint que lee la base de datos responde `503`, que el frontend debe tratar distinto del `500` (índice de specs); la spec no nombraba ninguno de esos errores, y decidía una vista por el estado `404` cuando ese estado tiene dos códigos |
| 2026-11-14 | Puesta al día con el contrato final del backend (sesión 06, divergencias DV-03, DV-06 y DV-09, y la parte del alta de DV-02 y DV-08), propuesta por la IA y pendiente de la revisión del Tech Lead. **Alta**: tabla en 2.3 con lo que la ayuda comprueba de cada campo y lo que deja al backend; del email, solo que no esté vacío, que no pase de 254 caracteres y que tenga una `@` que no esté en un extremo, sin el validador de email del framework ni el del navegador; el identificador se mide sin recortar; ningún campo lleva `maxlength`; un texto con un *surrogate* suelto no se envía; los valores se envían como están escritos; el `id` del cliente creado sale del cuerpo del `201`; y la forma de `errors` (un error por campo, en el orden del contrato). Requisitos nuevos E-44, E-45 y E-46, catorce filas en 5.4, CA-05 y D-13. Motivo: «forma básica del email» no decía qué se comprueba, y el validador de Angular 21.2.26 rechaza direcciones que el backend acepta desde la regla nueva del email del día 13 (SPEC-01, 2.1); el backend mide el identificador antes de normalizar; un *surrogate* suelto responde `400` desde el día 13; y CORS no expone la cabecera `Location` |
| 2026-11-14 | Puesta al día con el contrato final del backend (sesión 06, divergencias DV-04, DV-05 y DV-13, y la parte del simulador de DV-03), propuesta por la IA y pendiente de la revisión del Tech Lead. **El `id` de la ruta**: el frontend no lo convierte en número; si no es de 1 a 16 dígitos ASCII sin ceros a la izquierda o pasa de 2^53 − 1, muestra «Cliente no encontrado» sin llamar, y si lo es, pide el cliente con ese mismo texto (2.1, 2.4, 2.5, E-15, E-47 nuevo, tabla 5.7 y CA-17). `/clientes/abc` y `/clientes/01` muestran «Cliente no encontrado». **Detalle**: el aviso del historial dice el número de simulaciones recibidas, no un 50 escrito (2.4 y CA-07). **Simulador**: el `customer_id` es el `id` del cliente cargado, un campo numérico válido es un entero dentro de sus límites que se envía como número JSON, y un `422` de la proyección o del guardado se muestra junto a su campo (2.5, E-48 y E-49 nuevos, cinco filas en 5.5 y CA-08). Motivo: el backend fijó el día 13 que el `id` de la ruta tiene una sola forma (índice de specs), y JavaScript convierte `01`, `+1` y `1.0` en 1 y redondea por encima de 2^53 − 1, así que un frontend que convirtiera el texto daría varias direcciones a un cliente o pediría otro. Deja una limitación, dicha en 2.1 y pendiente de que el Tech Lead la acepte: un `id` entre 2^53 y 2^63 − 1 no puede abrirse desde el frontend |
| 2026-11-14 | Puesta al día con el contrato final del backend (sesión 06, divergencia DV-07), propuesta por la IA y pendiente de la revisión del Tech Lead. **Buscador**: el límite de 100 caracteres se mide como el backend, en puntos de código y sin recortar, y al superarlo no se llama a la API y se avisa junto al campo; el texto se envía tal como está escrito, en un solo parámetro `q` del cliente HTTP y nunca concatenado, y sin `q` si está vacío; un *surrogate* suelto se sustituye por U+FFFD; y el frontend muestra lo que llega, también cuando es el listado inicial. Requisitos nuevos E-50 y E-51, ocho filas en 5.3 y CA-04. Motivo: «el campo admite 100 caracteres» no decía en qué unidad ni sobre qué texto, y el backend mide puntos de código antes de recortar (SPEC-01, 2.12); un texto concatenado en la URL cambia la consulta (`q=a+b` se lee como «a b»), y los casos de SPEC-01 5.9 (`%`, `_`, `\`, la comilla) solo se cumplen si el texto llega literal |
| 2026-11-14 | Puesta al día con el contrato final del backend y con lo externo (sesión 06, divergencias DV-08, DV-09, DV-12 y DV-14, y el paso 2), propuesta por la IA y pendiente de la revisión del Tech Lead. **Contratos consumidos**: 4.1 gana las respuestas que el OpenAPI declara para cada llamada y los campos que llegan y no se usan; apartado nuevo 4.3 con lo que el frontend envía frente a las limitaciones L-01 a L-05 del backend; 2.9 dice lo que la configuración de CORS del backend exige (origen exacto, solo `GET` y `POST`, ninguna cabecera propia y ninguna cabecera de respuesta legible), con E-52 y CA-18 nuevos. **Corrección de un cambio de este mismo día**: el nombre y el email se envían recortados, no tal como están escritos (2.3, E-46 y dos filas de 5.4), porque al escribir 4.3 se vio que sin recortar se podía enviar un cuerpo de cualquier tamaño (L-01). **Lo externo, comprobado el 2026-11-14**: la API de divisas responde igual que el día 12, también en sábado (4.2); la nota de D-09 dice qué versión de Playwright es elegible con el margen de ADR-007; fila «Depende de» y apartado 9 al día. Motivo: la spec no decía qué respuestas trata de cada llamada ni nombraba las limitaciones del backend, que dependen de lo que un cliente envíe; y los datos de la API de divisas y de las versiones eran del día 12 |
| 2026-11-14 | Corrección de dos cambios de este mismo día, vista por la IA antes de la evaluación: 2.2 y 2.3 nombraban `isWellFormed()` y `toWellFormed()` para detectar un *surrogate* suelto. Son de ES2024, y el proyecto que crea el CLI 21.2.29 compila para ES2022 sin declarar otra biblioteca (leído en su plantilla de `tsconfig.json`), así que no las conoce; `.claude/rules/frontend.md` manda usar la configuración por defecto del CLI. La spec dice ahora cómo se detecta sin salir de ella: una expresión regular en modo Unicode, comprobada con Node 24. Sin cambios en requisitos, criterios ni casos |
| 2026-11-14 | Correcciones de la evaluación independiente de esta spec (`04-calidad/evaluacion-spec04-01.md`, H-01, H-05 y H-09), decididas por el Tech Lead. **El EUR se formatea solo con enteros** (2.6): los euros y los céntimos se separan con una división exacta y un resto, y el importe no se divide entre 100; la regla del dinero no cambia. **Presentación**: el tipo de cambio se muestra con los decimales que trae, hasta 6; los importes de cuatro cifras, sin punto de millar, como los da `es-ES`; y los tramos se rotulan «del 1 al 10», «del 11 al 50» y «del 51 en adelante» (2.6 y 2.8). Dos filas nuevas en la tabla de importes de 5.1 (5 y 123450 céntimos) y dos tablas más, del tipo de cambio y de los rótulos. CA-01 deja de citar E-27, que un test del *pipe* no demuestra, y pasa a citar E-28 y E-29; E-27 lo citan CA-02 y CA-08, que tienen sus filas. Motivo: 2.6 decía que el importe en EUR «sale exacto de los céntimos» sin decir cómo, y lo directo era dividir entre 100, que es coma flotante sobre dinero; el formato por defecto daba `1,114` para un tipo de `1.1139`; y ninguna fila fijaba un importe de cuatro cifras ni el rótulo del último tramo |
| 2026-11-14 | Correcciones de la evaluación independiente de esta spec (H-02 y el caso A-01 de su respuesta), decididas por el Tech Lead. **Casos que faltaban**, sin cambiar ningún requisito: una fila en 5.3 para el orden de la API (E-03), una en 5.4 para los desplegables del alta (E-05 y E-35) y dos en 5.5, para los importes marcados como «actualizando» y para «Guardar» desactivado mientras se proyecta y mientras se guarda (E-21 y E-23). **CA-18 se parte**: el test de `core/` comprueba que la petición no lleva ninguna cabecera puesta por la aplicación, y CA-14, la prueba de principio a fin, que las peticiones reales pasan el CORS del backend; CA-14 cita E-52. Motivo: CA-04, CA-05 y CA-08 dicen reproducir «cada fila» y esos cinco requisitos no tenían ninguna; y CA-18 pedía mirar unas cabeceras que Angular añade al enviar y que un test con sus utilidades no ve |
| 2026-11-14 | Decisión del Tech Lead sobre la propuesta C-01 de la sesión 06: la limitación del `id` por encima de 2^53 − 1 queda aceptada como **limitación conocida L-06**, con fila en `04-calidad/limitaciones-conocidas.md`. 2.1 la cita en lugar de darla por pendiente; también la fila de 5.7, una frase en 4.3 y el apartado 9. Sin cambios en reglas, requisitos ni casos. Motivo: JavaScript no representa exactos los enteros por encima de 2^53 − 1, y un cliente con un `id` mayor solo existiría insertado a mano |
| 2026-11-14 | Correcciones de la evaluación independiente de esta spec (H-06, H-07 y H-11), decididas por el Tech Lead. **Se quita la rama del `422` del cliente**: con el filtro del `id`, un `422` de `GET /customers/{id}` solo puede venir de un defecto del frontend y se muestra como error inesperado; «Cliente no encontrado» queda para dos casos, el `id` que no pasa el filtro y el `404` con `customer_not_found` (2.4, 2.5, 2.7, 4.1, E-15 y una fila de 5.6 y otra de 5.7). **La forma del `id`** dice «el primero distinto de `0`», que excluye el `0` solo (2.1). **La remisión de 5.7 a SPEC-01 5.10** dice qué textos están allí y cuáles se sondearon aparte, con su resultado. Motivo: la rama del `422` venía de antes del filtro y contradecía la tabla de 2.7; «sin ceros a la izquierda» no descartaba el `0`, y los casos esperan que no se pida; y cinco textos de 5.7 no tienen fila en SPEC-01 5.10 |
| 2026-11-14 | Correcciones de la evaluación independiente de esta spec (H-03, H-04 y H-08) y propuestas C-02 y C-03 de la sesión 06, decididas por el Tech Lead. **Buscador**: al superar el límite se cancela la búsqueda en curso y el aviso sale al momento (2.2 y E-50); ya no se afirma que U+FFFD no coincide con ningún cliente, porque el backend lo admite en un nombre (2.2); y la fila del buscador de 4.1 recoge el `422` que declara el OpenAPI. **Panel**: una nota bajo la lista cuando llegan 20 clientes, el máximo de la API (E-53 nuevo), y un mensaje propio, «Todavía no hay clientes», con el acceso al alta, cuando el listado inicial llega vacío (E-54 nuevo). Cinco filas nuevas en 5.3 y CA-04. Motivo: una respuesta que llegara tarde podía pintar la lista retirada; la frase de U+FFFD era falsa (sondeado); la columna de 4.1 decía recoger lo que el OpenAPI declara y omitía un estado; la API no dice cuántos clientes hay; y el listado inicial vacío es lo primero que se ve con la base de datos recién creada, sin que nadie haya buscado nada |
| 2026-11-14 | Corrección de la evaluación independiente de esta spec (H-10) y propuesta C-04 de la sesión 06, decididas por el Tech Lead. **Un código de país o de plan que `/meta` no trae se muestra tal como llega, sin marca** (2.1, E-35, una fila en 5.3 y CA-07). D-13 recoge la comprobación del *surrogate* suelto, que 2.3 y E-45 ya tenían. Motivo: la spec decía que nunca se muestran códigos y no decía qué hacer con uno que `/meta` no conoce, que es el caso de datos incoherentes de SPEC-02 E-10; y D-13 no nombraba una de las comprobaciones de la ayuda |
| 2026-11-14 | Corrección de la evaluación independiente de esta spec (H-12) y propuesta C-05 de la sesión 06, decididas por el Tech Lead. **En los tres campos numéricos del simulador decide el texto escrito**: es válido solo si está formado por dígitos ASCII y su valor cabe en los límites; son campos de texto con `inputmode="numeric"`, no controles numéricos del navegador (2.5, E-22, E-36). En 5.5, `15.0` pasa de proyectarse a ser un error, junto con `1e3`, `+15`, `1 5` y `100000.000000000001`; `015` es válido y vale 15. **Aviso tras agotar la espera al guardar**: dice que la simulación puede haberse guardado y enlaza al detalle del cliente (2.5, E-55 nuevo, una fila en 5.5 y CA-08). Motivo: `Number.isInteger` miraba el número, y JavaScript lee `100000.000000000001` como el entero 100000 y `1e3` como 1000 (comprobado con Node), así que se enviaba un valor que el usuario no había escrito; y tras un `timeout` el servidor puede haber guardado, de modo que reintentar a ciegas duplica la simulación |
| 2026-11-14 | Aprobación del Tech Lead: el estado pasa a `aprobada` (2026-11-14), aparte del bloque backend y antes de empezar el frontend, con los doce hallazgos de la evaluación independiente y las propuestas C-01 a C-05 de la sesión 06 decididos y aplicados |
| 2026-11-14 | Cambio mandado por el Tech Lead al revisar la parada 1 del frontend (sesión 07, precisión Y-07), con la spec ya en vigor: **tres reglas que la IA había puesto en el código sin que la spec las dijera**. El panel pide su lista sin esperar a `/meta` y la enseña cuando `/meta` llega (2.2 y una fila en 5.3). De un `422`, una entrada de `errors` sin la forma del contrato se ignora, y un segundo error del mismo campo va al aviso general (2.3 y dos filas en 5.4). Añadida por la IA al escribirlas, y pendiente de que el Tech Lead la vea: un `422` que no deja ninguna entrada que mostrar se trata como error inesperado (2.3 y una fila en 5.4). Sin requisitos nuevos: precisan E-01, E-09 y E-48. Motivo: una regla no puede estar solo en el código |
| 2026-11-14 | Cambio mandado por el Tech Lead al revisar la parada 1 del frontend en el navegador (sesión 07): **el corrector ortográfico del navegador se desactiva** en el campo de búsqueda y en el nombre, el identificador fiscal y el email del alta (2.8). Sin requisitos nuevos. Motivo: el corrector subrayaba el texto del buscador como si fuera una falta |
| 2026-11-14 | Cambio mandado por el Tech Lead al revisar la parada 2 del frontend (sesión 07, precisiones Z-01, Z-05 y Z-17): **reglas del alta y del simulador que la IA había puesto en el código sin que la spec las dijera**. «Reintentar» de un formulario envía lo que el formulario tiene en ese momento, pasando otra vez por la ayuda (2.7, una fila en 5.4 y otra en 5.5). **Alta** (2.3 y tres filas en 5.4): la ayuda calla hasta el primer intento de envío; cada desplegable lleva una primera opción desactivada que no se puede elegir; el mensaje del backend junto a un campo se retira cuando ese campo cambia; y «Guardar» sigue desactivado tras el `201`. **Simulador** (2.5 y dos filas en 5.5): la primera proyección y la de «Reintentar» no esperan los 200 ms; durante la espera los importes ya se marcan «actualizando» y «Guardar» está desactivado; la ayuda de los tres campos habla desde el primer carácter, porque la proyección es en vivo; con un texto no válido el deslizante se queda donde estaba; y con `/meta` en error el cliente y la proyección se piden igual. El Tech Lead admite además la regla que la IA había añadido en el cambio de Y-07 y él no había visto: un `422` que no deja nada que mostrar es un error inesperado (2.3). Sin requisitos nuevos: precisan E-05, E-07, E-09, E-18, E-22, E-23, E-25 y E-36. Motivo: una regla no puede estar solo en el código |
| 2026-11-14 | Cambio mandado por el Tech Lead al revisar la parada 2 del frontend (sesión 07, precisiones Z-08 y Z-11): **CA-16 cambia de alcance**. Los servicios de `core/` reproducen cada fila de 5.6; cada vista, o el servicio que carga sus datos, una fila por cada aviso distinto. Antes pedía cada fila también en las cuatro vistas. Sin cambios en 5.6, en los requisitos ni en los tests: es lo que los tests ya hacían. Motivo: el reparto de `code` a aviso vive en `core/` y se prueba allí fila a fila |
| 2026-11-14 | Mejora mandada por el Tech Lead al revisar la parada 2 del frontend (sesión 07): **tras un envío del alta con errores, el foco va al primer campo con error**, en el orden del formulario, tanto si lo impide la ayuda como si el backend responde `422`; sin campo con error, el foco no se mueve (2.3, requisito nuevo E-56, cinco filas en 5.4 y CA-05). Motivo: quien usa el teclado o un lector de pantalla llega directamente a lo que tiene que corregir |
| 2026-11-14 | Cambio mandado por el Tech Lead al revisar la parada 3 del frontend (sesión 07, precisión AA-05): **reglas de las divisas que la IA había puesto en el código sin que la spec las dijera** (2.6). El tipo aplicado y el aviso de «orientativos» van una vez por vista: en el simulador, dentro de la proyección, y en el detalle, sobre el historial; el «Total en EUR» va junto a cada total convertido. Se convierten todos los importes visibles, también los del desglose por tramos. El aviso del fallo de la API vive en la cabecera, en todas las vistas, con «Reintentar». El selector enseña los códigos, no nombres. Una respuesta no válida deja el estado de error con el código `invalid_rates`. El *pipe* de importes admite un argumento para dar el EUR exacto. Y los cinco textos de la interfaz de las divisas. Sin requisitos nuevos ni filas nuevas: precisan E-27, E-29 y E-30, y los tests ya lo comprueban. Motivo: una regla no puede estar solo en el código |
| 2026-11-14 | Cambio mandado por el Tech Lead al revisar la parada 3 del frontend (sesión 07, precisión AA-07): **la fila de 5.2 del cuerpo que no es JSON dice que el estado es de error y que su `code` puede ser `invalid_rates` o `unknown_error`**, con una nota bajo la tabla. Sin cambios en requisitos, criterios ni tests. Motivo: las utilidades de test entregan el cuerpo como texto y lo rechaza la validación; en un navegador, el cliente HTTP puede fallar antes, al leer el JSON. En los dos casos la interfaz es la misma |
| 2026-11-15 | Cambio mandado por el Tech Lead al empezar la fase de QA (sesión 08): **CA-15 deja de pedir «capturas manuales» y pide «capturas generadas con Playwright y revisadas por el Tech Lead»**, guardadas en `04-calidad/capturas/`; la nota bajo la tabla de criterios dice lo mismo y nombra la orden que las genera. Sin cambios en requisitos ni en casos. D-09 y ADR-005 siguen diciendo «capturas manuales»: son el registro de lo que se decidió el día 12 y no se han tocado. Motivo: unas capturas que salen de una orden se pueden repetir y son las mismas para quien revise; la revisión sigue siendo de una persona |
| 2026-11-15 | Cambio mandado por el Tech Lead al revisar la parada 1 de la fase de QA (sesión 08, precisión AC-11). **La nota bajo la tabla de criterios** deja de dar CA-13 y CA-14 por pendientes de implementar: dice que están en `frontend/e2e/`, que se ejecutan con `npm run e2e` y que el oráculo los pasa con `--e2e`; y precisa que la API de divisas se responde con el protocolo de depuración de Chromium y no con `page.route()`, por lo que las pruebas solo funcionan en Chromium. **CA-15 nombra las dos capturas añadidas**, el simulador con otra divisa y la cabecera con el aviso del fallo de los tipos. **D-09 no se reescribe**: lleva al lado una nota fechada. Sin cambios en requisitos ni en casos. Motivo: la nota decía de CA-13 y CA-14 algo que dejó de ser cierto al implementarlos; «la intercepta» no decía cómo, y el cómo decide si CA-14 comprueba el CORS del backend (con `page.route()`, Playwright responde las comprobaciones previas y una cabecera de más no hacía fallar la prueba); y CA-15 pedía menos capturas de las que hay |
| 2026-11-15 | Decisión del Tech Lead sobre el hallazgo H-01 de la evaluación independiente del frontend (`04-calidad/evaluacion-frontend-01.md`), sin tocar el código. **El filtro del `id` se aplica al segmento ya descodificado por el router** (2.1), y 5.7 gana dos filas: `/clientes/%31` pide el cliente 1, y `/clientes/1;x=y` también, porque el parámetro de matriz no forma parte del `id`. La frase de 5.7 sobre el simulador dice «las tres primeras filas» donde decía «la primera». Sin requisitos ni criterios nuevos; los dos casos, en los tests de 5.7 del detalle y del simulador. Motivo: la spec decía que el cliente 1 tiene una sola dirección en el frontend y no decía qué pasa con las dos formas que el router reduce a `1` antes de que la aplicación vea el texto |
| 2026-11-15 | Decisión del Tech Lead sobre el hallazgo H-02 de la evaluación independiente del frontend. **El anillo de foco y el borde de los campos de formulario tienen un contraste de 3:1 o más sobre el blanco y sobre el fondo de la página** (2.8 y criterio nuevo CA-19, una prueba de Playwright que lee los colores que pinta el navegador). El anillo pasa del naranja `#f59e0b` al azul de acento, `#1d4ed8`; el borde de los campos, de `#c9ced8` a `#7c8698`, y el de las tarjetas, los avisos y la cabecera no cambia. **CA-15 nombra una captura más**, el alta con un campo enfocado. Sin requisitos nuevos. Motivo: el anillo tenía un contraste de 2,15 sobre el blanco y el borde de los campos, de 1,58; con menos de 3:1, quien ve poco no distingue qué campo tiene el foco ni dónde empieza un campo |
| 2026-11-15 | Decisión del Tech Lead sobre el hallazgo H-03 de la evaluación independiente del frontend. **Cada una de las cuatro vistas pone su título en el documento**, con la opción `title` del router y el nombre de la aplicación detrás: «Clientes», «Nuevo cliente», «Detalle del cliente» y «Simulador» (2.1, requisito nuevo E-57 y CA-11). El anuncio del resultado de la búsqueda y el foco al navegar, que el mismo hallazgo señalaba, no se hacen: son la limitación conocida L-10. Motivo: con un solo título para toda la aplicación, un lector de pantalla anuncia igual todas las vistas; lo demás no se puede comprobar sin un lector de pantalla |
| 2026-11-15 | Decisión del Tech Lead sobre el hallazgo H-04 de la evaluación independiente del frontend. **2.7 dice qué lleva `role="alert"` y qué no**: lo llevan los avisos generales y los mensajes junto a un campo que salen mientras se escribe (los del simulador y el del buscador); **los mensajes junto a un campo del alta dejan de llevarlo** y se leen con su campo, por `aria-describedby` y `aria-invalid`. Sin requisitos nuevos. Motivo: un envío del alta con los cinco campos vacíos anunciaba cinco alertas a la vez, además de leerse cada mensaje con su campo; en el simulador el foco no se mueve y el mensaje sale mientras se escribe, así que allí se quedan. No se ha probado con un lector de pantalla (L-10) |
| 2026-11-15 | Decisión del Tech Lead sobre el hallazgo H-05 de la evaluación independiente del frontend: **tres reglas que la IA había puesto en el código sin que la spec las dijera**, escritas tal como está el código. **El `409` del alta y el aviso general de un `422` no ofrecen «Reintentar»**, porque enviar lo mismo no puede salir bien (2.3, la fila del `409` de su tabla y 2.7); **la fila «Error» de la tabla de 2.5 recoge la excepción** del `422` de la proyección; y **un `created_at` que no se puede leer como fecha se muestra como llega** (2.8). Sin cambios en el código, en los requisitos ni en los tests. Motivo: 2.5 y 2.7 decían «aviso con «Reintentar»» sin esas excepciones, y 2.8 no decía qué hacer con una fecha que no lo es |
