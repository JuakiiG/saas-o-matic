# Pruebas manuales

Guion para recorrer la aplicación a mano, en algo más de una hora: la
pasada del 16/11/2026 llevó 75 minutos, con pausas. Lo ejecuta
una persona; **la columna «Resultado» se deja vacía hasta entonces**. Cada
paso dice qué hacer, qué se debe ver y de qué requisito o criterio sale.

Lo que este guion añade a las pruebas automáticas: lo que solo ve una
persona en un navegador de verdad (el anillo de foco, el título de la
pestaña, la barra de direcciones, la API de divisas real y su caída) y dos
cosas que ninguna prueba ejecuta (el backend parado y una ejecución de
Playwright interrumpida).

## Quién, cuándo y con qué

Lo rellena quien ejecuta el guion o quien anota a su dictado.

| | |
|---|---|
| **Fecha y hora** | 16/11/2026, de 12:39 a 13:55 |
| **Quién** | JGH |
| **Commit** (`git log -1 --format=%h`) | `06a6314` |
| **Navegador y versión** | Google Chrome 157.0.8103.78 |
| **Sistema operativo** | Windows 11 (10.0.26300) |

## Preparación

1. Arrancar el backend y el frontend como dice el
   [`README.md`](../../README.md) de la raíz, cada uno en su terminal.
2. Abrir `http://localhost:4200` (no `127.0.0.1`) con las herramientas de
   desarrollo del navegador abiertas en la pestaña «Red» (F12).
3. **El guion escribe en la base de datos local**
   (`backend/data/saas-o-matic.db`): crea un cliente y dos simulaciones.
   Si se prefiere no tocarla, arrancar el backend con `DATABASE_PATH`
   apuntando a un fichero nuevo (README, «Configuración»).
4. El guion usa el identificador fiscal `B12345674`, de España. **Si ya
   existe en la base** (de una pasada anterior), el paso 7 dará el aviso de
   duplicado: usar entonces otro válido en los pasos 6 a 8, por ejemplo
   `A12345674` (con control erróneo, `A12345675`) o `E99999997`
   (`E99999998`).

En la columna «Resultado»: **OK**, o lo que se ha visto en su lugar.

## A. Panel, alta con errores y foco

| # | Qué hacer | Qué se debe ver | Sale de | Resultado |
|---|---|---|---|---|
| 1 | Abrir `http://localhost:4200/` | Pestaña: «Clientes · SaaS-O-Matic». Cabecera con «SaaS-O-Matic», el enlace «Panel» y el selector «Divisa» en EUR. Título «Clientes» y botón «Nuevo cliente». Debajo, la lista de clientes o, con la base vacía, «Todavía no hay clientes.» con «Dar de alta el primer cliente». En «Red», una petición a `/meta`, una a `/customers` y una a `api.frankfurter.dev` | SPEC-04/E-01, E-54, E-39, E-26, E-57 | OK |
| 2 | Pulsar «Nuevo cliente» | Pestaña: «Nuevo cliente · SaaS-O-Matic». Formulario vacío y **sin ningún mensaje de error**. Los desplegables muestran «Elige un país» y «Elige un plan»; al abrirlos, nueve países y tres planes, por su nombre | E-05, E-35, E-57; SPEC-04, 2.3 | OK |
| 3 | Sin escribir nada, pulsar «Guardar» | Cinco mensajes, uno bajo cada campo: «El nombre debe tener entre 2 y 120 caracteres.», «Escribe el identificador fiscal.», «Escribe el email de contacto.», «Elige un país.» y «Elige un plan.». **El foco queda en «Nombre de la empresa»**, con el cursor dentro y el anillo azul alrededor. En «Red», ninguna petición nueva | E-56; SPEC-04, 2.3 | OK |
| 4 | Escribir `Pruebas Manuales SL` en el nombre y pulsar «Guardar» | El mensaje del nombre desaparece. **El foco pasa a «Identificador fiscal»**, el primer campo que sigue con error | E-56 | OK |
| 5 | Hacer clic en el título «Nuevo cliente» y pulsar el tabulador siete veces, despacio | El foco recorre, en este orden: nombre, identificador, email, país, plan, «Guardar» y «Cancelar» (antes, si el clic no cae en el formulario, «Panel» y «Divisa»). **En cada uno se ve un anillo azul.** Sobre el botón «Guardar», que también es azul, **el anillo se distingue del botón**: queda separado de él por una franja del color del fondo | SPEC-04, 2.8 y CA-19; pendiente AE-06 de la sesión 08 | OK |

## B. Identificador no válido, alta y duplicado

| # | Qué hacer | Qué se debe ver | Sale de | Resultado |
|---|---|---|---|---|
| 6 | Rellenar: identificador `B12345675`, email `pruebas@empresa.example`, país «España», plan «Profesional». Pulsar «Guardar» | Bajo el identificador: «El carácter de control del identificador fiscal no es correcto.». Lo escrito se conserva y el foco va al identificador. En «Red», `POST /customers` con estado `422`. Ningún otro mensaje | SPEC-04/E-09, E-06, E-56; SPEC-01/E-16 | OK |
| 7 | Cambiar el identificador por `b-1234567.4` (con la minúscula, el guion y el punto) y pulsar «Guardar» | El mensaje desaparece al escribir. Se abre el detalle: pestaña «Detalle del cliente · SaaS-O-Matic», dirección `/clientes/` y un número. La tarjeta muestra el nombre, **el identificador normalizado, `B12345674`**, el email, «España», «Profesional» y la fecha de alta, **con la hora local de ahora**. Debajo, «Este cliente todavía no tiene simulaciones.» y «Crear la primera simulación» | SPEC-04/E-08, E-46, E-12, E-13, E-35, E-57; SPEC-01/E-08 | OK |
| 8 | «Panel» → «Nuevo cliente». Rellenar otro nombre y otro email, **el mismo identificador `B12345674`**, «España» y cualquier plan. «Guardar» | Aviso: «Ya existe un cliente con ese identificador fiscal en ese país.», **sin botón «Reintentar»**. Lo escrito se conserva. En «Red», `409`. Pulsar «Cancelar»: vuelve al panel | SPEC-04/E-10; SPEC-01/E-19 | OK |
| 9 | En el panel, escribir `manual` en «Buscar cliente» y esperar. Después, `zzzz` | Con `manual`: la lista se queda en «Pruebas Manuales SL», con su identificador, «España» y «Profesional». Con `zzzz`: «No hay clientes que coincidan.». En «Red», una petición por cada pausa al escribir, no una por letra | SPEC-04/E-02, E-03, E-04, E-35 | OK |

## C. Simulador, guardar y la simulación nueva la primera

| # | Qué hacer | Qué se debe ver | Sale de | Resultado |
|---|---|---|---|---|
| 10 | Borrar la búsqueda, abrir «Pruebas Manuales SL» y pulsar «Crear la primera simulación» | Pestaña: «Simulador · SaaS-O-Matic». El nombre de la empresa y «España». Usuarios activos: 10, en el campo y en el deslizante. Proyección: coste base 100,00 EUR, impuesto al 21 % de 21,00 EUR y total 121,00 EUR, con los tres tramos («del 1 al 10», «del 11 al 50», «del 51 en adelante») | SPEC-04/E-17, E-18, E-19, E-35, E-57; SPEC-02, 5.1 | OK |
| 11 | Escribir `15` en usuarios activos | El deslizante se mueve a 15. Un instante de «Actualizando…» y la proyección cambia: 140,00 EUR, 29,40 EUR y **169,40 EUR** | SPEC-04/E-17, E-18, E-21; SPEC-02, 5.1 | OK |
| 12 | Escribir `1e3` en usuarios activos. Después, volver a `15` | Con `1e3`: bajo el campo, «Escribe un número entero de 0 a 100.000, solo con cifras.»; **los importes desaparecen**; «Guardar» se desactiva; el deslizante no se mueve. Con `15`: vuelve la proyección de 169,40 EUR | SPEC-04/E-22, E-23 | OK |
| 13 | Almacenamiento `500`, llamadas `1000`. Pulsar «Guardar» | Vuelve al detalle. Una tarjeta de simulación con la fecha y hora de ahora, 15 usuarios activos, «500 GB» de almacenamiento, 1000 llamadas a la API y total 169,40 EUR | SPEC-04/E-24, E-12 | OK |
| 14 | «Nueva simulación», usuarios `51`, «Guardar» | En el detalle hay dos tarjetas y **la primera es la nueva**: 51 usuarios, total 514,25 EUR. La de 15 usuarios queda debajo | SPEC-04/CA-14, E-12; SPEC-03/E-13 | OK |

## D. Otra divisa y la API de divisas sin conexión

| # | Qué hacer | Qué se debe ver | Sale de | Resultado |
|---|---|---|---|---|
| 15 | En el detalle, recargar la página (F5). En «Red», abrir la respuesta de `api.frankfurter.dev` y apuntar el `rate` y el `date` de USD | El selector está en EUR. **Una sola petición** a la API de divisas, con tres objetos (USD, GBP y CHF) | SPEC-04/E-26; SPEC-04, 2.1 y 2.6 | OK. USD: `rate` 1.1054 y `date` 2026-11-16 |
| 16 | Elegir «USD» en el selector «Divisa» y abrir «Desglose por tramos» de una tarjeta | **Todos los importes cambian a USD al momento, sin ninguna petición nueva** en «Red», también los del desglose. Sobre el historial: «1 EUR = … USD · tipo del …», **con el `rate` apuntado** (con coma decimal) **y el `date` apuntado**, escrito día/mes/año, y «Importes orientativos: cada uno se convierte por separado.». En cada tarjeta, además, «Total en EUR» con el total en euros (514,25 EUR y 169,40 EUR) | SPEC-04/E-27, E-29; SPEC-04, 2.6 | OK |
| 17 | Con USD elegido, pulsar «Nueva simulación» y escribir `15` usuarios. Sumar a mano el coste base y el impuesto | La divisa se conserva al cambiar de vista. La proyección sale en USD, con el tipo y el aviso de importes orientativos dentro, y «Total en EUR» 169,40 EUR. **La suma de la base y el impuesto puede diferir del total en un céntimo**, según el tipo del día: es lo esperado y no un fallo. Anotar los tres importes | SPEC-04/E-27, E-29; SPEC-04, 2.6 y 5.1 | OK. Coste base 154,76 USD, impuesto 32,50 USD y total 187,25 USD: la suma de los dos primeros da 187,26 USD, un céntimo más que el total, que es lo esperado |
| 18 | En «Red», bloquear el dominio `api.frankfurter.dev` (en Chrome: botón derecho sobre esa petición → «Block request domain», o su traducción) y recargar | En la cabecera, el aviso «No se han podido cargar los tipos de cambio. Los importes se muestran en EUR.» con «Reintentar». **El selector solo ofrece EUR** (al recargar, además, la divisa elegida vuelve a EUR). El simulador funciona igual, con los importes en EUR | SPEC-04/E-30, E-28; CA-03 | OK |
| 19 | Quitar el bloqueo y pulsar «Reintentar» en la cabecera | Un instante de «Cargando tipos…», el aviso desaparece y el selector vuelve a ofrecer las cuatro divisas | SPEC-04/E-30 | OK |

## E. El backend parado

| # | Qué hacer | Qué se debe ver | Sale de | Resultado |
|---|---|---|---|---|
| 20 | En el simulador, con una proyección a la vista, **parar el backend** (Ctrl+C en su terminal) y cambiar los usuarios a `20` | **Los importes anteriores desaparecen**: no queda ninguno a la vista como si fuera el actual. Aviso «No se ha podido conectar con el servidor.» con «Reintentar». «Guardar», desactivado. Lo escrito se conserva | SPEC-04/E-20, E-23, E-32; SPEC-04, 2.7 | OK |
| 21 | Pulsar «Reintentar» con el backend todavía parado. Después, arrancar el backend y pulsar «Reintentar» otra vez | La primera vez vuelve el mismo aviso. La segunda, la proyección de 20 usuarios: 180,00 EUR, 37,80 EUR y 217,80 EUR | SPEC-04/E-20; SPEC-04, 2.7 | OK |
| 22 | Parar el backend otra vez. Pulsar «Panel» y recargar la página | En lugar del buscador y de la lista, el aviso «No se ha podido conectar con el servidor.» con «Reintentar». La cabecera y el selector de divisa siguen en su sitio. Ningún código de país o de plan a la vista. **Arrancar el backend** y pulsar «Reintentar»: aparece el buscador y, **en el sitio de la lista, el mismo aviso con su propio «Reintentar»**, porque la lista también se pidió con el backend parado; pulsarlo: aparece la lista. **Hacen falta las dos pulsaciones**: cada aviso reintenta su petición, y reintentar `/meta` no vuelve a pedir la lista | SPEC-04/E-40, E-32; SPEC-04, 2.1, 2.2 y 5.3 | OK. Han hecho falta las dos pulsaciones; lo veo aceptable |

## F. Direcciones y títulos

| # | Qué hacer | Qué se debe ver | Sale de | Resultado |
|---|---|---|---|---|
| 23 | Abrir `http://localhost:4200/no-existe` | «Página no encontrada», con «Volver al panel». Pestaña: **«Página no encontrada · SaaS-O-Matic»**. Pulsar el enlace: vuelve al panel y la pestaña vuelve a «Clientes · SaaS-O-Matic» | SPEC-04/E-34, E-57 | OK |
| 24 | Abrir `http://localhost:4200/clientes/%31` | **El detalle del cliente 1**, igual que con `/clientes/1` (con una base nueva, el cliente del paso 7). Anotar qué queda escrito en la barra de direcciones | SPEC-04/E-47; SPEC-04, 2.1 y 5.7 | OK. En la barra de direcciones queda `http://localhost:4200/clientes/1` |
| 25 | Abrir `/clientes/abc`, `/clientes/01` y `/clientes/999999` | Las tres: «Cliente no encontrado», con «Volver al panel». Con las dos primeras, **ninguna petición a `/customers/…`** en «Red»; con la tercera, una, con estado `404` | SPEC-04/E-15, E-47 | OK |
| 26 | Repasar la pestaña en las cinco vistas: `/`, `/clientes/nuevo`, el detalle, el simulador y `/no-existe` | «Clientes», «Nuevo cliente», «Detalle del cliente», «Simulador» y «Página no encontrada», cada uno seguido de « · SaaS-O-Matic». Los mismos cinco títulos en el historial del navegador | SPEC-04/E-57, CA-11 | OK |

## G. 375 px de ancho

Con el modo de diseño adaptable de las herramientas del navegador
(Ctrl+Mayús+M) y un ancho de 375 px.

| # | Qué hacer | Qué se debe ver | Sale de | Resultado |
|---|---|---|---|---|
| 27 | Recorrer el panel, el alta (pulsando «Guardar» en vacío, para ver los cinco mensajes), el detalle con USD elegido y un desglose abierto, y el simulador | En las cuatro vistas, **ningún desplazamiento horizontal** y nada cortado por la derecha. El contenido, en una columna. La cabecera, con el selector en su sitio | SPEC-04/CA-13, E-16; SPEC-04, 2.4 | OK |
| 28 | Bloquear otra vez `api.frankfurter.dev` y recargar, a 375 px | La cabecera muestra el aviso del fallo de los tipos y «Reintentar», **sin desplazamiento horizontal**. Quitar el bloqueo al acabar | SPEC-04/CA-13, E-30 | OK |

## H. Una ejecución de Playwright interrumpida

| # | Qué hacer | Qué se debe ver | Sale de | Resultado |
|---|---|---|---|---|
| 29 | **Parar el backend y el frontend.** Apuntar la fecha de modificación de `backend/data/saas-o-matic.db`. En `frontend/`, ejecutar `npm run e2e` y, **cuando hayan pasado tres o cuatro pruebas, pulsar Ctrl+C** | La ejecución se corta | `CLAUDE.md`, regla 8; pendiente de la sesión 08 | OK |
| 30 | Comprobar los puertos y la carpeta temporal, con las órdenes de abajo | **Nada escucha en el 8000 ni en el 4200. No queda ninguna carpeta `saas-o-matic-e2e-…`** en la carpeta temporal del sistema. `backend/data/saas-o-matic.db` conserva la fecha apuntada | `CLAUDE.md`, regla 8; pendiente de la sesión 08 | OK. Las dos primeras órdenes no escriben nada; la tercera, lanzada desde la raíz del repositorio, da 14/11/2026 18:37:20 |

Órdenes del paso 30. **Se lanzan desde la raíz del repositorio**, no desde
`frontend/`, donde acaba el paso 29: la tercera usa una ruta relativa y
desde allí falla. Las dos primeras no deben escribir nada.

En Windows (PowerShell):

```
netstat -ano | Select-String "LISTENING" | Select-String ":8000 ", ":4200 "
Get-ChildItem $env:TEMP -Filter "saas-o-matic-e2e-*"
Get-Item backend\data\saas-o-matic.db | Select-Object LastWriteTime
```

En Linux y macOS:

```
lsof -nP -iTCP:8000 -iTCP:4200 -sTCP:LISTEN
ls -d "${TMPDIR:-/tmp}"/saas-o-matic-e2e-* 2>/dev/null
ls -l backend/data/saas-o-matic.db
```

## De dónde sale lo que el guion espera

Los textos y los importes están copiados del código, de las specs y de las
respuestas del backend del 2026-11-15. **La IA no ha ejecutado este guion
en un navegador**: sus servidores no pueden usar los puertos 8000 y 4200
(`CLAUDE.md`, regla 8), y el frontend solo habla con el backend desde
`http://localhost:4200`. Lo que sí ha comprobado, y lo que no, está en la
bitácora de la [sesión 09](../03-proceso/sesion-09.md).

**Lo ejecutó el Tech Lead el 16/11/2026**, sobre `06a6314`: los 30 pasos,
en OK. Los datos de la pasada están en la tabla de cabecera; lo que vio en
cada paso, en la columna «Resultado»; y lo que cierra, en la bitácora de la
[sesión 10](../03-proceso/sesion-10.md). **Los resultados los anotó, al
dictado del Tech Lead mientras lo ejecutaba, la sesión de IA que audita**:
quién es y qué hace está en
[«Dos sesiones de IA y una persona»](../README.md#dos-sesiones-de-ia-y-una-persona).

Si un paso no sale como dice, puede estar mal el paso y no la aplicación:
anotar lo visto y decidir después.
