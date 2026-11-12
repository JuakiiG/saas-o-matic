# Supuestos y ambigüedades

- **Fecha**: 2026-11-12
- **Estado**: revisado por el Tech Lead el 2026-11-12. Quedan abiertos A2 a A5,
  a la espera de respuesta y con fecha límite
- **Qué es**: cada punto que el encargo deja abierto, la opción elegida y por
  qué. Ninguna spec se aprueba mientras dependa de un supuesto sin cerrar.

## Estados

| Estado | Significado |
|---|---|
| `pendiente de confirmar` | Consultado a quien propone el reto; sin respuesta todavía. La propuesta es provisional |
| `propuesto` | Propuesta de la IA a la espera de la decisión del Tech Lead |
| `decidido` | Decisión tomada por el Tech Lead, con su fecha |
| `decidido (sin confirmación externa)` | Decidido por el Tech Lead al vencer la fecha límite sin respuesta. Se revisa si la respuesta llega después |
| `logística` | Asunto de la entrega, ajeno al producto |

## Resumen

| Id | Ambigüedad | Estado | Afecta a |
|---|---|---|---|
| A1 | Plazo de entrega | `logística` | R-19 |
| A2 | Qué es el plan y si afecta al precio | `pendiente de confirmar` | SPEC-01, SPEC-02 |
| A3 | Almacenamiento y llamadas a la API sin tarifa | `pendiente de confirmar` | SPEC-02, SPEC-03, SPEC-04 |
| A4 | Países admitidos y tipo de impuesto de cada uno | `pendiente de confirmar` | SPEC-01, SPEC-02, SPEC-03 |
| A5 | Tratamiento del IVA entre empresas de distintos países | `pendiente de confirmar` | SPEC-02 |
| A6 | Representación del dinero y redondeo | `decidido` (2026-11-12) | SPEC-02, SPEC-03, SPEC-04 |
| A7 | Límites del número de usuarios | `decidido` (2026-11-12) | SPEC-02, SPEC-03, SPEC-04 |
| A8 | Divisas: moneda de cálculo, origen de los tipos y fallo de la API | `decidido` (2026-11-12) | SPEC-04 |
| A9 | Dónde se calcula la proyección en tiempo real | `decidido` (2026-11-12) | SPEC-02, SPEC-03, SPEC-04, ADR-002 |
| A10 | Identificador fiscal de países distintos de España | `decidido` (2026-11-12) | SPEC-01 |
| A11 | Alcance exacto de la validación española | `decidido` (2026-11-12) | SPEC-01 |
| A12 | Clientes duplicados | `decidido` (2026-11-12) | SPEC-01, SPEC-04 |
| A13 | Endpoints de lectura no enumerados | `decidido` (2026-11-12) | SPEC-01, SPEC-02, SPEC-03, SPEC-04 |
| A14 | Formato de los errores de la API | `decidido` (2026-11-12) | Todas |
| A15 | Formato de entrega del repositorio | `logística` | R-19 |
| A16 | Autenticación | `decidido` (2026-11-12) | Todas |
| A17 | Vista de alta de cliente | `decidido` (2026-11-12) | SPEC-04 |
| A18 | Edición y borrado | `decidido` (2026-11-12) | SPEC-01, SPEC-03 |

A15 a A18 no estaban en la lista inicial; salieron al releer el encargo para
redactar los requisitos.

## Logística

- **A1 · Plazo de entrega.** Logística de entrega acordada con quien propone
  el reto; no afecta al producto.
- **A15 · Formato de entrega del repositorio.** Logística de entrega acordada
  con quien propone el reto; no afecta al producto.

## Pendientes de confirmar

Mientras no haya respuesta se trabaja con la propuesta, y las specs afectadas
no pasan de `borrador` en la parte que depende de ella.

**Fecha límite**: si el viernes 13 de noviembre de 2026 a las 10:00 no hay
respuesta, el Tech Lead decide A2 a A5 con la hipótesis documentada aquí.
Pasan a `decidido (sin confirmación externa)` y se revisan si la respuesta
llega después. *Por qué: una consulta sin contestar no puede bloquear el
desarrollo de forma indefinida, y la hipótesis ya está razonada.*

### A2 · Plan

El cliente tiene un «plan elegido», pero no se dice qué planes hay ni si
cambian el precio. **Propuesta**: lista cerrada de planes, guardada como dato
informativo y sin efecto en el cálculo. *Por qué*: la única tarifa definida es
la de usuarios; dar precio a los planes sería inventar una regla de negocio.
Los nombres concretos se fijan en SPEC-01.

### A3 · Almacenamiento y llamadas a la API

La simulación los recoge, pero la tarifa solo habla de usuarios.
**Propuesta**: guardarlos y mostrarlos en el historial, sin que intervengan en
el importe. *Por qué*: el mismo que en A2. Si la respuesta fuera que sí tienen
precio, cambia SPEC-02, y por eso no se cierra todavía.

Con independencia de la respuesta, **los dos valores se validan**: enteros,
no negativos y con un máximo razonable que se fija en SPEC-03. *Por qué*: que
un dato no tenga precio no justifica guardar basura.

### A4 · Impuesto por país

Hay que sumar el impuesto del país del cliente, pero no se da la lista de
países ni los tipos. **Propuesta**:

- Lista cerrada de países admitidos, cada uno con su tipo general de IVA.
- El tipo aplicado **se guarda con cada simulación**. *Por qué*: si un tipo
  cambia, las simulaciones antiguas deben seguir mostrando lo que se calculó
  entonces.
- Un país fuera de la lista se rechaza en el alta, en lugar de aplicarle un
  0 % en silencio.

Tipos generales, **verificados el 2026-11-12**:

| País | Código | Tipo general | Fuente |
|---|---|---|---|
| España | ES | 21 % | Comisión Europea |
| Portugal | PT | 23 % | Comisión Europea |
| Francia | FR | 20 % | Comisión Europea |
| Alemania | DE | 19 % | Comisión Europea |
| Italia | IT | 22 % | Comisión Europea |
| Países Bajos | NL | 21 % | Comisión Europea |
| Irlanda | IE | 23 % | Comisión Europea |
| Bélgica | BE | 21 % | Comisión Europea |
| Reino Unido | GB | 20 % | Gobierno del Reino Unido |

Fuentes consultadas:

- Comisión Europea, tabla «VAT rates applied in EU member countries»:
  <https://europa.eu/youreurope/business/taxation/vat/vat-rules-rates/index_en.htm>.
  La página indica «Last checked: 13/07/2026» y recomienda confirmar los tipos
  con la autoridad fiscal de cada país.
- Gobierno del Reino Unido: <https://www.gov.uk/vat-rates>. La página no
  muestra fecha de actualización.

Simplificaciones conocidas:

- **«España» aplica el 21 % de península y Baleares.** Canarias tiene su
  propio impuesto (IGIC), y Ceuta y Melilla el suyo (IPSI); no se modelan. La
  tabla de la Comisión avisa de que no incluye los tipos de regiones
  específicas como Canarias. El caso de Ceuta y Melilla no aparece en la
  fuente consultada y no se ha verificado aparte.
- **Estados Unidos queda fuera de la lista.** No tiene IVA, sino impuestos
  sobre las ventas que dependen de cada estado; representarlo con un 0 %
  sería una simplificación que nadie ha pedido. El comportamiento con un tipo
  del 0 % se cubre con tests unitarios del dominio.

Sigue pendiente de confirmar si esta lista de países y el uso del tipo
general son lo que se espera.

### A5 · IVA entre empresas de distintos países

En una venta real entre empresas de dos países de la UE suele aplicarse la
inversión del sujeto pasivo y la factura va sin IVA. **Propuesta**: no
modelarlo y aplicar siempre el tipo del país del cliente, como dice el
encargo. Se deja constancia de que es una simplificación conocida. *Por qué*:
la herramienta hace presupuestos orientativos, no facturas, y la regla pedida
es explícita.

## Decididos

### A6 · Dinero y redondeo

Importes en **céntimos enteros** en el dominio, la base de datos y la API. El
impuesto se calcula sobre el coste base total y se redondea al céntimo más
próximo, con el medio céntimo hacia arriba. El tipo impositivo se guarda en
puntos básicos (21 % = 2100). *Por qué*: la coma flotante binaria no
representa de forma exacta importes decimales, y los enteros eliminan el
problema de raíz y son triviales de comparar en los tests.

Con las tarifas actuales, que son euros enteros por usuario, y tipos
impositivos enteros, **el impuesto sale siempre exacto al céntimo** y el
redondeo nunca llega a actuar. La regla existe para tarifas o tipos futuros
con decimales, y se prueba con un caso sintético.

### A7 · Límites del número de usuarios

Entero entre 0 y 100.000. Cero usuarios cuesta 0 €. Negativos, decimales y
valores por encima del máximo se rechazan. *Por qué*: el primer tramo empieza
en cero, y un máximo evita entradas absurdas sin limitar ningún uso real. El
máximo del control de la interfaz puede ser menor y se fija en SPEC-04.

### A8 · Divisas

- Todo se calcula y se guarda en EUR. La conversión a otra divisa es solo de
  presentación y nunca se persiste. *Por qué*: un importe guardado no puede
  depender del tipo de cambio del día en que se consulta.
- **La llamada a la API de divisas la hace el frontend directamente.** *Por
  qué*: es la letra del encargo, que dice que es la interfaz la que conecta.
  Pasarla por el backend aislaría mejor el fallo de un tercero, pero se
  aparta de lo pedido.
- Divisas ofrecidas: EUR, USD, GBP y CHF. Lista cerrada en SPEC-04 (D-03)
  el 2026-11-12.
- Se muestra la fecha del tipo de cambio usado.
- Si la API de divisas falla o tarda demasiado: aviso visible, importes en
  EUR y un botón para reintentar. La aplicación sigue siendo utilizable.
- Los tipos se guardan en memoria durante la sesión para no pedirlos en cada
  cambio de divisa.

### A9 · Dónde se calcula la proyección en tiempo real

El backend es la única fuente del cálculo. El control de usuarios llama a
`POST /pricing/quote`, que calcula sin guardar, con una espera corta entre
pulsaciones (*debounce*) y cancelando la petición anterior.
`POST /simulations` usa el mismo cálculo y lo guarda. *Por qué*: una sola
implementación de la tarifa; con dos, tarde o temprano el importe en pantalla
y el guardado dejan de coincidir. Alternativas y consecuencias en ADR-002.

### A10 · Identificador fiscal fuera de España

Para otros países se normaliza (mayúsculas, sin espacios, guiones ni puntos) y se
comprueba solo el formato general: alfanumérico y de longitud acotada. *Por
qué*: el encargo exige el algoritmo de control solo para España. Implementar
los de cada país es alcance no pedido.

### A11 · Validación española

Se admiten tres formatos, cada uno con su control:

- **DNI**: ocho dígitos y una letra de control.
- **NIE**: letra inicial X, Y o Z, siete dígitos y letra de control.
- **CIF**: letra del tipo de entidad, siete dígitos y un carácter de control
  que es dígito o letra según el tipo de entidad.

Antes de validar se normaliza la entrada. El error indica qué ha fallado
(formato o carácter de control) sin revelar cuál sería el valor correcto.
*Por qué*: son los tres identificadores que cubre la expresión «DNI/NIF/CIF».
El detalle de cada algoritmo va en SPEC-01.

### A12 · Duplicados

La unicidad es del par **(país, identificador fiscal normalizado)**. Un
segundo alta con el mismo par se rechaza con `409 Conflict`. *Por qué*: el
identificador solo es único dentro de su país; dos empresas de países
distintos pueden tener legítimamente la misma cadena. Dentro de un país, dos
fichas iguales repartirían el historial de simulaciones.

### A13 · Endpoints de lectura

El encargo solo nombra los dos `POST`, pero las vistas necesitan consultas.
Se añaden los mínimos:

| Endpoint | Para qué |
|---|---|
| `GET /customers?q=` | Buscador por nombre o identificador fiscal (R-10) |
| `GET /customers/{id}` | Ficha del cliente con su historial (R-11) |
| `POST /pricing/quote` | Proyección sin guardar (R-12, A9) |
| `GET /meta` | Países admitidos con su impuesto y planes, para los formularios |
| `GET /health` | Comprobar que el backend está levantado (SPEC-03, «Operación del backend») |

El buscador devuelve **como máximo 20 resultados, ordenados por nombre de
empresa**. *Por qué*: una respuesta acotada y con orden estable es predecible
para la interfaz y para los tests; quien busca afina el texto en lugar de
paginar.

### A14 · Formato de los errores

Todas las respuestas de error siguen `application/problem+json` (RFC 9457),
con un código estable por error y, en los errores de validación, el detalle
por campo. El código va en inglés y el mensaje en español, y el frontend
decide por el código. *Por qué*: es un estándar, y un formato único simplifica
el frontend y los tests.

### A16 · Autenticación

Sin inicio de sesión. *Por qué*: es una herramienta interna, el encargo no lo
menciona y añadirlo desviaría el esfuerzo de lo que se evalúa. Sí se limita
CORS al origen del frontend (SPEC-03, «Operación del backend»).

### A17 · Vista de alta de cliente

No figura entre las vistas obligatorias, pero sin ella no hay forma de crear
clientes desde la interfaz. Se añade un formulario sencillo de alta en una
ruta propia (`/clientes/nuevo`), con acceso desde el panel (SPEC-04, D-07).
*Por qué*: es donde la validación fiscal se hace visible para quien
evalúa, y evita depender de datos precargados.

### A18 · Edición y borrado

Fuera de alcance. Los clientes y las simulaciones se crean y se consultan,
pero no se modifican ni se eliminan. *Por qué*: no se pide, y un historial de
simulaciones tiene más valor si es inmutable.
