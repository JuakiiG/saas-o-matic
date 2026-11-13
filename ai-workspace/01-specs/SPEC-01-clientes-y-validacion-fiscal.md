# SPEC-01 · Clientes y validación fiscal

| | |
|---|---|
| **Estado** | `aprobada` (2026-11-13) |
| **Requisitos** | R-03, R-04 y la parte de backend de R-10 y R-11 |
| **Supuestos** | A2, A4, A10, A11, A12, A13, A14 y A18 (`decidido`). A2, confirmado por la respuesta del 2026-11-13; A4, solo en parte: la lista de países es decisión propia |
| **Depende de** | SPEC-03 (forma del historial dentro de la ficha, errores genéricos, CORS y esquema) y SPEC-02 (constante de países), las dos aprobadas el 2026-11-13 |
| **Bloqueos para aprobarla** | Ninguno desde el 2026-11-13: A2 y A4 decididos (apartado 8) y aprobación a la vez que SPEC-02 y SPEC-03, las tres del bloque backend (índice de specs) |

## 1. Objetivo

Definir el alta de clientes corporativos, la validación de su identificador
fiscal, la consulta de la ficha, el buscador y los datos de apoyo de los
formularios.

**Dentro**: `POST /customers`, `GET /customers/{id}`, `GET /customers?q=`,
`GET /meta`, normalización y validación del identificador fiscal, unicidad.

**Fuera**: historial de simulaciones dentro de la ficha (SPEC-03), cálculo
del impuesto (SPEC-02), formulario y vistas (SPEC-04), edición y borrado
(A18), `GET /health` y CORS (SPEC-03, «Operación del backend»), errores
genéricos de la API (convenciones comunes del índice).

## 2. Reglas de negocio

### 2.1 Campos del cliente

| Campo | Regla |
|---|---|
| `company_name` | Texto. Se recortan los espacios de los extremos; el resultado tiene de 2 a 120 caracteres y ningún carácter de las categorías Unicode Cc o Cf (saltos de línea, tabuladores, caracteres de formato invisibles). Se guarda recortado |
| `tax_id` | Texto de 30 caracteres como máximo antes de normalizar, en cualquier país. Se normaliza (2.2), se valida según el país (2.3 a 2.6 para España, 2.8 para el resto) y **se guarda normalizado** |
| `contact_email` | Texto. Se recortan los espacios de los extremos; ningún carácter Cc o Cf; 254 caracteres como máximo; **ningún separador Unicode** (categorías Zs, Zl y Zp: el espacio U+0020, el espacio de no separación U+00A0, el espacio ideográfico U+3000, los separadores de línea y de párrafo…) en ninguna posición; exactamente una `@`, con texto delante y un dominio detrás que contiene al menos un punto y no empieza ni acaba en punto. No se comprueba que el buzón exista |
| `country` | Uno de los códigos de la constante de países del dominio (SPEC-02, 2.2), en mayúsculas: `ES`, `PT`, `FR`, `DE`, `IT`, `NL`, `IE`, `BE`, `GB` |
| `plan` | Uno de los códigos de la lista cerrada: `starter` («Básico»), `professional` («Profesional»), `enterprise` («Empresa») (A2). Dato informativo, sin efecto en el precio |

Los cinco son obligatorios y deben ser cadenas JSON. El sistema añade `id`
(entero de 1 a 9223372036854775807) y `created_at` (fecha y hora UTC en
ISO 8601, con precisión de segundos: `2026-11-12T14:30:00Z`).

«Recortar», el orden de las comprobaciones y la unidad de las longitudes
están en 2.12.

### 2.2 Normalización del identificador

Se aplica **antes de validar**, igual para todos los países, y en este orden:

1. Se eliminan todos los espacios, todos los guiones (`-`) y todos los
   puntos (`.`), estén donde estén. «Espacio» es únicamente el carácter
   U+0020; el guion es U+002D y el punto, U+002E.
2. Las 26 letras ASCII de la `a` a la `z` pasan a su mayúscula, con una
   **correspondencia explícita** letra a letra. No se usa la conversión a
   mayúsculas de Unicode (`upper()`), que transforma caracteres ajenos a
   ese rango en letras ASCII: `ﬁ` (U+FB01) daría `FI` y `ſ` (U+017F), `S`.

Nada más: **no se rellenan ceros a la izquierda**, no se quitan otros signos
y no se quita un prefijo de país (`ES…`). Lo que quede debe estar formado
solo por los caracteres ASCII `0`–`9` y `A`–`Z`; cualquier otro carácter (una
barra, una `Ñ`, un dígito de otro alfabeto, la ligadura `ﬁ`, el espacio de
no separación U+00A0 o cualquier otro espacio que no sea U+0020) es un
error de formato.

*Por qué los puntos*: `12.345.678-Z` es una escritura frecuente del DNI y
rechazarla no aporta seguridad.

### 2.3 España: clasificación por formato

El identificador normalizado debe tener exactamente 9 caracteres y encajar en
uno de estos tres patrones. Si no encaja en ninguno, el error es de
**formato**; si encaja y el último carácter no es el que corresponde, el
error es de **carácter de control**.

| Tipo | Patrón | Control |
|---|---|---|
| DNI | 8 dígitos + 1 letra | 2.4 |
| NIE | `X`, `Y` o `Z` + 7 dígitos + 1 letra | 2.5 |
| CIF | Letra de entidad válida + 7 dígitos + 1 dígito o letra | 2.6 |

Los NIF de persona física con inicial `K`, `L` o `M` existen (los describe la
AEAT) pero quedan fuera de los tres formatos de A11: se rechazan como error
de formato (ver D-03).

### 2.4 DNI

```
letra = "TRWAGMYFPDXBNJZSQVHLCKE"[número mod 23]
```

`número` son los 8 dígitos leídos como entero. Ejemplo público: `12345678`,
resto 14, letra `Z` → `12345678Z`.

### 2.5 NIE

La letra inicial se sustituye por un dígito (`X`→`0`, `Y`→`1`, `Z`→`2`) y al
número de 8 dígitos resultante se le aplica el cálculo del DNI.

### 2.6 CIF

**Letras de entidad válidas** (17): `A B C D E F G H J N P Q R S U V W`.
Quince son claves de entidades españolas (`A B C D E F G H J P Q R S U V`);
`N` es entidad extranjera y `W` establecimiento permanente de entidad no
residente.

**Cálculo del valor de control** sobre los 7 dígitos `d1…d7`:

```
pares   = d2 + d4 + d6
impares = suma, para d1, d3, d5 y d7, de las cifras de (2 · d)
C       = (10 − (pares + impares) mod 10) mod 10
```

- Control **dígito**: el propio `C`.
- Control **letra**: `"JABCDEFGHI"[C]` (0→J, 1→A, … 9→I).

**Qué forma se exige según la letra de entidad** (D-01):

| Grupo | Letras |
|---|---|
| Exigen letra | `P`, `Q`, `R`, `S`, `N`, `W` |
| Exigen dígito | `A`, `B`, `E`, `H` |
| Admiten dígito o letra | `C`, `D`, `F`, `G`, `J`, `U`, `V` |

**Convención de uso común, sin fuente oficial localizada; decidido por el
Tech Lead** (2026-11-12). *Por qué*: es el comportamiento con el que se
contrastará el validador, y admitir ambos en los tipos dudosos no rechaza
ningún CIF legítimo.

### 2.7 Fuentes y grado de verificación

Consultadas el **2026-11-12**.

| Qué | Fuente | Resultado |
|---|---|---|
| Estructura del NIF de entidades (letra + 7 dígitos + carácter de control) y las 17 letras | Orden EHA/451/2008, de 20 de febrero (BOE núm. 49, de 26/02/2008, ref. BOE-A-2008-3580), arts. 2 a 5; texto consolidado, última actualización 15/01/2016: <https://www.boe.es/buscar/act.php?id=BOE-A-2008-3580> | **Verificado** leyendo la página |
| Lo mismo, y los tipos de NIF de persona física (DNI, NIE, K, L, M) | Agencia Tributaria, guía del modelo 036, «Composición del NIF» (páginas actualizadas el 26/03/2026 y el 10/09/2026): <https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/guia-practica-cumplimentacion-modelo-censal-036/anexos/anexo-01-solicitud-nif-documentacion-aportar/informacion-sobre-numero-identificacion-fiscal/composicion-nif/personas-juridicas-entidades.html> | **Verificado** leyendo la página |
| Cálculo de la letra del DNI y sustitución del NIE | Ministerio del Interior, «Cálculo del dígito de control del NIF/NIE»: <https://www.interior.gob.es/opencms/es/servicios-al-ciudadano/tramites-y-gestiones/dni/calculo-del-digito-de-control-del-nif-nie/> | **Verificado solo a través del extracto de un buscador**: la lectura directa devolvió `403`. El extracto recoge la división entre 23, la tabla, el ejemplo `12345678Z` y X/Y/Z → 0/1/2. No se ha visto la fecha de la página |
| Cálculo del carácter de control del CIF y tabla `JABCDEFGHI` | Ninguna oficial encontrada | **Sin fuente oficial**: convención de uso común |
| Qué letras de entidad exigen letra, dígito o admiten ambos | Ninguna oficial encontrada | **Sin fuente oficial**: convención de uso común, decidida por el Tech Lead (D-01) |

Sobre las dos últimas filas: ni la Orden EHA/451/2008 ni la página de la AEAT
describen el cálculo ni la forma del carácter de control; solo dicen «un
carácter de control». El Decreto 2423/1975 (derogado desde el 01/01/2008)
remite a un anexo publicado como imagen, que no se pudo leer. El cálculo de
2.6 es la convención que usan los validadores de uso común, **escrita de
memoria por la IA**, sin una fuente oficial que la respalde; los grupos de
letras los fijó el Tech Lead con esa misma convención. No se adopta la
regla, que algunas referencias citan, de exigir letra cuando los dos
primeros dígitos son `00`: tampoco tiene fuente y la Orden de 2008 declara
los siete dígitos aleatorios.

**Contraste con una implementación independiente.** Como los casos de
prueba del apartado 5 se generaron con este mismo algoritmo, por sí solos
solo demuestran coherencia interna. Para romper esa circularidad, un test
compara el validador con el de la biblioteca `python-stdnum`, fijada como
dependencia **solo de test** (CA-19, D-15 y ADR-005).

**Resultado esperado**: todo identificador que acepta el validador del
dominio lo acepta también `python-stdnum`, y las únicas diferencias son las
de la forma del control: un CIF con el valor de control correcto, escrito
como dígito o como letra, en una forma que el grupo de su letra de entidad
no admite (D-01). Cualquier otra discrepancia la decide el Tech Lead; no se
resuelve cambiando el test ni el validador por cuenta propia.

El 2026-11-12 la última versión publicada era la 2.2 (consultado en PyPI).
**Comprobado el 2026-11-13** con `python-stdnum` 2.2, instalada como
dependencia de test y con la versión fijada: el resultado esperado se
cumple. Las cifras están en la nota «Sobre CA-19» (apartado 6).

### 2.8 Fuera de España

Tras la normalización, el identificador debe tener **de 4 a 20 caracteres**
`0`–`9` o `A`–`Z`. No se calcula ningún control (A10). Un fallo es siempre de
formato.

### 2.9 Unicidad

No puede haber dos clientes con el mismo par **(país, identificador
normalizado)** (A12). La garantiza una restricción `UNIQUE` de la base de
datos, no solo una consulta previa.

### 2.10 Buscador

**Forma de búsqueda del nombre.** Al dar de alta un cliente, el dominio
calcula a partir del nombre recortado una forma de búsqueda, que se guarda en
su propia columna y no se devuelve en la API:

1. Descomposición Unicode NFD.
2. Se eliminan las marcas diacríticas (caracteres de categoría `Mn`).
3. `casefold`.

Así `José`, `JOSE` y `jose` dan `jose`, y `Ñandú` da `nandu`: ni las
mayúsculas ni los acentos distinguen, y la `Ñ` busca y ordena como `N`.

**Búsqueda.**

- El texto buscado `q` se recorta. Si falta o queda vacío, se devuelven los
  primeros clientes por orden de nombre (D-07).
- Un cliente coincide si la forma de búsqueda de `q` aparece **dentro** de
  la forma de búsqueda de su nombre, o si `q` normalizado como en 2.2 (sin
  espacios, guiones ni puntos, en mayúsculas) no queda vacío y aparece
  dentro del identificador fiscal guardado.
- Un `q` que contiene el carácter U+0000 **no coincide con ningún
  cliente**, esté donde esté el carácter: la respuesta es `200` con la
  lista vacía. *Por qué: ningún nombre ni identificador guardado puede
  contenerlo (es de la categoría Cc y no es `0`–`9` ni `A`–`Z`).*
- **Qué se compara lo decide el dominio**: que un `q` normalizado vacío no
  se compara con el identificador y que un `q` con U+0000 no se compara
  con nada. La sentencia SQL solo compara lo que recibe y no contiene
  ninguna de esas dos condiciones (2.11).
- Las dos comparaciones se hacen con `LIKE` y una cláusula `ESCAPE` cuyo
  carácter de escape es la barra invertida `\` (U+005C). `%`, `_` y `\` del
  texto buscado se escapan con ella y se buscan como texto literal.
- El texto llega a la base de datos siempre como parámetro, nunca
  concatenado en la sentencia.
- Resultado: como máximo 20 clientes, ordenados por la forma de búsqueda del
  nombre y, a igualdad, por `id` ascendente.

### 2.11 Dónde vive

Normalización, clasificación, cálculo de controles y forma de búsqueda son
funciones puras de `backend/app/domain/`, igual que la lista de planes. La
API y la base de datos no repiten ninguna de esas reglas.

**Países**: hay una única constante en el dominio, con el código, el nombre
y el tipo impositivo en puntos básicos de cada país. La define SPEC-02
(2.2), que es la dueña de los tipos; esta spec la usa para validar el país
del alta y para `GET /meta`. No existe una segunda lista de países.

### 2.12 Validación: recorte, unidad, orden y forma de los errores

- **Recortar** es quitar de los extremos únicamente el carácter espacio
  U+0020. Un tabulador o un salto de línea en un extremo no se recorta: es
  un carácter Cc y da `invalid_characters`.
- **Caracteres no admitidos**: cualquier carácter de las categorías Unicode
  Cc o Cf en `company_name` o en `contact_email` da `invalid_characters`.
  En `tax_id` sigue valiendo 2.2: todo lo que no sea `0`–`9` o `A`–`Z` tras
  normalizar es `invalid_tax_id_format`.
- **Separadores en el email**: cualquier carácter de las categorías Zs, Zl
  o Zp que quede en `contact_email` después de recortar da
  `invalid_email`, no `invalid_characters`. Como solo se recorta U+0020,
  un espacio de no separación en un extremo no se quita y da
  `invalid_email`. *Por qué: un espacio de no separación llega al copiar y
  pegar un correo, y una dirección guardada así no sirve.*
- **Las longitudes se miden en puntos de código Unicode.**
- **Un solo error por campo: el primero que falle**, en este orden:

| Campo | Orden de las comprobaciones |
|---|---|
| `company_name` | `missing` → `not_a_string` → `invalid_characters` → `too_short` → `too_long` |
| `tax_id` | `missing` → `not_a_string` → `too_long` (más de 30 antes de normalizar) → `invalid_tax_id_format` → `invalid_tax_id_check_character` |
| `contact_email` | `missing` → `not_a_string` → `invalid_characters` → `too_long` → `invalid_email` |
| `country` | `missing` → `not_a_string` → `unsupported_country` |
| `plan` | `missing` → `not_a_string` → `unsupported_plan` |

- **Identificador con un país no válido o ausente**: si `country` tiene
  cualquier error (`missing`, `not_a_string` o `unsupported_country`), del
  identificador solo se comprueba lo que no depende del país: `missing`,
  `not_a_string` y `too_long`. No se comprueban su formato ni su carácter
  de control. Los dos campos pueden traer error a la vez.
- **Orden de `errors`**: el de los campos en el contrato (`company_name`,
  `tax_id`, `contact_email`, `country`, `plan`) y, después, un
  `unknown_field` por cada campo no documentado, por orden alfabético de su
  nombre.
- **Valor de `field`**: el nombre del campo del cuerpo; `id` para el
  identificador de la ruta; `q` para el parámetro de búsqueda; el nombre
  recibido para un campo o un parámetro desconocido.
- **El límite de 100 caracteres de `q` se mide antes de recortar.**

## 3. Requisitos (EARS)

### Alta y campos

| Id | Requisito | Cubre |
|---|---|---|
| E-01 | Cuando recibe un alta válida, el sistema deberá guardar el cliente y responder `201` con el cliente creado y la cabecera `Location` de su ficha. | R-03 |
| E-02 | El sistema deberá recortar los espacios (U+0020) de los extremos del nombre y del email antes de validarlos y guardarlos. | R-03 |
| E-03 | Si el nombre recortado tiene menos de 2 o más de 120 caracteres, o contiene algún carácter de las categorías Cc o Cf, entonces el sistema deberá rechazar el alta. | R-03 |
| E-04 | Si el email no cumple la regla de 2.1, entonces el sistema deberá rechazar el alta. | R-03 |
| E-05 | Si el país no es uno de los códigos de la constante de países del dominio, escrito en mayúsculas, entonces el sistema deberá rechazar el alta en lugar de aceptarlo con un impuesto del 0 %. | A4 |
| E-06 | Si el plan no es uno de los códigos de la lista cerrada, entonces el sistema deberá rechazar el alta. | A2 |
| E-07 | Si falta un campo, un campo no es una cadena o la petición trae un campo no documentado, entonces el sistema deberá rechazar el alta. | A14 |
| E-34 | Si el identificador fiscal recibido supera los 30 caracteres antes de normalizar, entonces el sistema deberá rechazar el alta con el código de campo `too_long`, sea cual sea el país. | A10, A11 |
| E-35 | El sistema deberá informar de un solo error por campo, el primero que falle según el orden de 2.12, y devolver `errors` en el orden de los campos del contrato. | A14 |

### Identificador fiscal

| Id | Requisito | Cubre |
|---|---|---|
| E-08 | El sistema deberá normalizar el identificador como define 2.2 (sin espacios U+0020, guiones ni puntos, y con las letras `a`–`z` en mayúsculas mediante una correspondencia explícita) antes de validarlo, y guardar y devolver siempre la forma normalizada. | A10, A11 |
| E-09 | El sistema no deberá completar con ceros ni corregir de ningún otro modo un identificador para que resulte válido. | A11 |
| E-10 | Mientras el país es España, el sistema deberá aceptar solo identificadores que encajen en el patrón de DNI, NIE o CIF de 2.3. | R-04, A11 |
| E-11 | Mientras el país es España, el sistema deberá comprobar la letra del DNI con el resto de dividir su número entre 23 y la tabla `TRWAGMYFPDXBNJZSQVHLCKE`. | R-04 |
| E-12 | Mientras el país es España, el sistema deberá comprobar la letra del NIE sustituyendo la inicial `X`, `Y` o `Z` por `0`, `1` o `2` y aplicando el cálculo del DNI. | R-04 |
| E-13 | Mientras el país es España, el sistema deberá comprobar el carácter de control del CIF con el cálculo de 2.6, exigiendo dígito, letra o cualquiera de los dos según el grupo de su letra de entidad. | R-04 |
| E-14 | Mientras el país no es España, el sistema deberá comprobar únicamente que el identificador normalizado tiene de 4 a 20 caracteres alfanuméricos. | A10 |
| E-15 | Si el identificador no encaja en ningún patrón admitido para su país, entonces el sistema deberá rechazar el alta con el código de campo `invalid_tax_id_format`. | A11 |
| E-16 | Si el identificador encaja en un patrón español pero su carácter de control no es el correcto o no tiene la forma exigida, entonces el sistema deberá rechazar el alta con el código de campo `invalid_tax_id_check_character`. | A11 |
| E-17 | El sistema no deberá incluir en ninguna respuesta de error el carácter de control correcto ni ningún dato del que pueda deducirse. | A11 |
| E-18 | Si el país no es válido o falta, entonces el sistema deberá informar del error del país y comprobar del identificador solo lo que no depende del país (`missing`, `not_a_string` y `too_long`), sin validar su formato ni su carácter de control. | — |

### Unicidad

| Id | Requisito | Cubre |
|---|---|---|
| E-19 | Si ya existe un cliente con el mismo país e identificador normalizado, entonces el sistema deberá responder `409` con el código `customer_already_exists` y no guardar nada. | A12 |
| E-20 | El sistema deberá permitir el mismo identificador normalizado en dos países distintos. | A12 |
| E-21 | Si un alta tiene a la vez errores de validación y un duplicado, entonces el sistema deberá responder `422`. | — |

### Ficha

| Id | Requisito | Cubre |
|---|---|---|
| E-22 | Cuando recibe `GET /customers/{id}` de un cliente existente, el sistema deberá responder `200` con sus datos y con su historial de simulaciones, en la forma que define SPEC-03. | R-11, A13 |
| E-23 | Si no existe un cliente con ese `id`, entonces el sistema deberá responder `404` con el código `customer_not_found`. | A13 |
| E-24 | Si el `id` de la ruta no es un entero de 1 a 9223372036854775807, entonces el sistema deberá responder `422` con el código `validation_error` y, en el campo `id`, `not_an_integer` o `out_of_range`. | A14 |

### Buscador

| Id | Requisito | Cubre |
|---|---|---|
| E-25 | Cuando recibe `GET /customers?q=`, el sistema deberá devolver los clientes cuyo nombre contiene el texto, comparando las formas de búsqueda de ambos (sin distinguir mayúsculas ni acentos), o cuyo identificador fiscal contiene el texto normalizado. | R-10 |
| E-26 | El sistema deberá devolver como máximo 20 clientes, ordenados por la forma de búsqueda del nombre y, a igualdad, por `id`. | A13 |
| E-27 | El sistema deberá tratar `%`, `_` y `\` (el carácter de escape) del texto buscado como caracteres literales. | R-10 |
| E-28 | El sistema deberá pasar el texto buscado a la base de datos únicamente como parámetro de la consulta. | R-10 |
| E-29 | Cuando `q` falta o queda vacío tras recortarlo, el sistema deberá devolver los 20 primeros clientes por orden de nombre. | A13 |
| E-30 | Si `q` supera los 100 caracteres antes de recortarlo o la petición trae un parámetro no documentado, entonces el sistema deberá responder `422`. | A14 |
| E-31 | Cuando ningún cliente coincide, el sistema deberá responder `200` con una lista vacía. | R-10 |
| E-33 | Cuando guarda un cliente, el sistema deberá calcular en el dominio la forma de búsqueda de su nombre (NFD, sin marcas diacríticas, `casefold`) y guardarla en una columna propia. | R-10 |

**Sobre E-30**: tiene una limitación conocida y aceptada por el Tech Lead,
**L-04** ([`limitaciones-conocidas.md`](../04-calidad/limitaciones-conocidas.md)).
Si el parámetro `q` llega repetido, solo se usa y se valida el último
valor: un `q` de más de 100 caracteres que no sea el último no responde
`422`, porque se descarta sin usarse.

### `GET /meta`

| Id | Requisito | Cubre |
|---|---|---|
| E-32 | El sistema deberá devolver en `GET /meta` los países admitidos, con su código, nombre y tipo impositivo, y los planes, con su código y nombre, tomados de la constante única de países (SPEC-02, 2.2) y de la lista de planes del dominio, las mismas que usan la validación y el cálculo. | A13, A2, A4 |

## 4. Contratos

### 4.1 `POST /customers`

| Campo | Tipo | Obligatorio | Regla |
|---|---|---|---|
| `company_name` | cadena | sí | 2 a 120 caracteres tras recortar |
| `tax_id` | cadena | sí | Según el país (2.2 a 2.6 y 2.8) |
| `contact_email` | cadena | sí | Regla de 2.1 |
| `country` | cadena | sí | Código de la constante de países, en mayúsculas |
| `plan` | cadena | sí | `starter`, `professional` o `enterprise` |

```json
{
  "company_name": "  Ejemplo Uno SL ",
  "tax_id": "b-1234567 4",
  "contact_email": "compras@ejemplo-uno.example",
  "country": "ES",
  "plan": "professional"
}
```

Respuesta `201`, con `Location: /customers/1`:

```json
{
  "id": 1,
  "company_name": "Ejemplo Uno SL",
  "tax_id": "B12345674",
  "contact_email": "compras@ejemplo-uno.example",
  "country": "ES",
  "plan": "professional",
  "created_at": "2026-11-12T14:30:00Z"
}
```

| Estado | `code` | Cuándo | Códigos por campo |
|---|---|---|---|
| `409` | `customer_already_exists` | Ya hay un cliente con ese país e identificador normalizado | — |
| `503` | `service_unavailable` | La base de datos no puede abrirse o consultarse (error genérico de las convenciones comunes) | — |
| `422` | `validation_error` | La petición no es válida | `missing`, `not_a_string`, `too_short`, `too_long`, `invalid_characters`, `invalid_email`, `unsupported_country`, `unsupported_plan`, `invalid_tax_id_format`, `invalid_tax_id_check_character`, `unknown_field` |

Ejemplo de `422` por carácter de control:

```json
{
  "type": "about:blank",
  "title": "Unprocessable Content",
  "status": 422,
  "code": "validation_error",
  "detail": "La petición contiene datos no válidos.",
  "errors": [
    {
      "field": "tax_id",
      "code": "invalid_tax_id_check_character",
      "message": "El carácter de control del identificador fiscal no es correcto."
    }
  ]
}
```

Ejemplo de `422` por formato del identificador (solo cambia `errors`):

```json
"errors": [
  {
    "field": "tax_id",
    "code": "invalid_tax_id_format",
    "message": "El identificador fiscal no tiene un formato válido."
  }
]
```

Ejemplo de `422` con errores en dos campos, en el orden del contrato:

```json
"errors": [
  {
    "field": "company_name",
    "code": "too_short",
    "message": "Debe tener entre 2 y 120 caracteres."
  },
  {
    "field": "contact_email",
    "code": "invalid_email",
    "message": "El email no tiene un formato válido."
  }
]
```

Ejemplo de `409`:

```json
{
  "type": "about:blank",
  "title": "Conflict",
  "status": 409,
  "code": "customer_already_exists",
  "detail": "Ya existe un cliente con ese identificador fiscal en ese país."
}
```

El `message` de los dos errores del identificador es un texto fijo: no cambia
con el valor recibido. El `409` no incluye datos del cliente existente (ver
D-06).

### 4.2 `GET /customers/{id}`

Respuesta `200`: los siete campos que devuelve el alta y, además, el
historial del cliente en dos campos: `simulation_count` (entero) y
`simulations` (lista). La forma de esos dos campos y un ejemplo completo
están en SPEC-03, apartado 4.2; un cliente recién creado devuelve
`"simulation_count": 0` y `"simulations": []`.

| Estado | `code` | Cuándo | Códigos por campo (`field`: `id`) |
|---|---|---|---|
| `404` | `customer_not_found` | No existe un cliente con ese `id` | — |
| `422` | `validation_error` | El `id` no es un entero de 1 a 9223372036854775807 | `not_an_integer`, `out_of_range` |
| `503` | `service_unavailable` | La base de datos no puede abrirse o consultarse (error genérico de las convenciones comunes) | — |

### 4.3 `GET /customers?q=`

| Parámetro | Tipo | Obligatorio | Regla |
|---|---|---|---|
| `q` | cadena | no | 100 caracteres como máximo, medidos antes de recortar |

Respuesta `200` para `GET /customers?q=ejemplo`:

```json
{
  "items": [
    { "id": 1, "company_name": "Ejemplo Uno SL", "tax_id": "B12345674", "country": "ES", "plan": "professional" }
  ]
}
```

No se devuelve el total de coincidencias ni hay paginación (A13).

| Estado | `code` | Cuándo | Códigos por campo |
|---|---|---|---|
| `422` | `validation_error` | `q` demasiado largo o parámetro desconocido | `too_long` (`field`: `q`), `unknown_field` (`field`: el nombre del parámetro) |
| `503` | `service_unavailable` | La base de datos no puede abrirse o consultarse (error genérico de las convenciones comunes) | — |

### 4.4 `GET /meta`

```json
{
  "countries": [
    { "code": "ES", "name": "España",       "tax_rate_bp": 2100 },
    { "code": "PT", "name": "Portugal",     "tax_rate_bp": 2300 },
    { "code": "FR", "name": "Francia",      "tax_rate_bp": 2000 },
    { "code": "DE", "name": "Alemania",     "tax_rate_bp": 1900 },
    { "code": "IT", "name": "Italia",       "tax_rate_bp": 2200 },
    { "code": "NL", "name": "Países Bajos", "tax_rate_bp": 2100 },
    { "code": "IE", "name": "Irlanda",      "tax_rate_bp": 2300 },
    { "code": "BE", "name": "Bélgica",      "tax_rate_bp": 2100 },
    { "code": "GB", "name": "Reino Unido",  "tax_rate_bp": 2000 }
  ],
  "plans": [
    { "code": "starter",      "name": "Básico" },
    { "code": "professional", "name": "Profesional" },
    { "code": "enterprise",   "name": "Empresa" }
  ]
}
```

El orden es el de las tablas de esta spec y es estable. No tiene errores
propios.

## 5. Casos de prueba

Todos los identificadores son **sintéticos**: números de patrón artificial
(`00000000`, `1234567`, `9999999`…) cuyo control se ha calculado con el
algoritmo de 2.4 a 2.6 mediante un script aparte. La única excepción es el
ejemplo público `12345678Z`. Se evitan a propósito los DNI de numeración
baja: el único que empieza por ceros es `00000000`. No se ha comprobado, ni
se puede, que un número válido no esté asignado a alguien; no se ha tomado
ninguno de una persona o empresa real.

### 5.1 Normalización

| Entrada | Normalizado | Qué demuestra |
|---|---|---|
| `12345678Z` | `12345678Z` | Ya normalizado |
| `12345678z` | `12345678Z` | Minúsculas |
| `12345678-Z` | `12345678Z` | Guion |
| `12.345.678-Z` | `12345678Z` | Puntos y guion |
| ` 12 345 678 z ` | `12345678Z` | Espacios en cualquier posición |
| `x-1234567-l` | `X1234567L` | NIE con guiones y minúsculas |
| `b-1234567 4` | `B12345674` | CIF con guion y espacio |

### 5.2 España: identificadores válidos

| Entrada | Tipo | Cálculo |
|---|---|---|
| `12345678Z` | DNI | resto 14 (ejemplo público) |
| `00000000T` | DNI | resto 0, primera letra de la tabla |
| `99999997E` | DNI | resto 22, última letra de la tabla |
| `99999998T` | DNI | resto 0: la tabla vuelve a empezar |
| `99999999R` | DNI | número máximo, resto 1 |
| `X0000000T` | NIE | `X`→0: 0, resto 0 |
| `X1234567L` | NIE | 01234567, resto 19 |
| `Y0000000Z` | NIE | `Y`→1: 10000000, resto 14 |
| `Y1234567X` | NIE | 11234567, resto 10 |
| `Z0000000M` | NIE | `Z`→2: 20000000, resto 5 |
| `Z9999999H` | NIE | 29999999, resto 18 |
| `A12345674` | CIF, dígito | pares 12, impares 14, C = 4 |
| `B12345674` | CIF, dígito | misma numeración, otra letra de entidad |
| `E99999997` | CIF, dígito | pares 27, impares 36, C = 7 |
| `H00000000` | CIF, dígito | suma 0, C = 0 |
| `A24680241` | CIF, dígito | pares 14, impares 15, C = 1 |
| `P1234567D` | CIF, letra | C = 4 → `D` |
| `Q9999999G` | CIF, letra | C = 7 → `G` |
| `S0000000J` | CIF, letra | C = 0 → `J`, primera de la tabla |
| `P1111111I` | CIF, letra | C = 9 → `I`, última de la tabla |

### 5.3 España: error de carácter de control (`invalid_tax_id_check_character`)

| Entrada | Por qué |
|---|---|
| `12345678A` | DNI con letra de la tabla que no corresponde |
| `12345678I` | DNI con una letra que no está en la tabla |
| `X1234567T` | NIE con letra de la tabla que no corresponde |
| `Y0000000T` | NIE calculado como si `Y` valiera 0 |
| `A12345675` | CIF con dígito incorrecto |
| `A1234567D` | CIF de un tipo que exige dígito, con la letra equivalente |
| `P12345674` | CIF de un tipo que exige letra, con el dígito equivalente |
| `P1234567E` | CIF con letra incorrecta |
| `P1234567K` | CIF con una letra fuera de la tabla `JABCDEFGHI` |

### 5.4 España: error de formato (`invalid_tax_id_format`)

| Entrada | Por qué |
|---|---|
| cadena vacía, o solo espacios y guiones | Nada que validar |
| `1234567Z` | 7 dígitos: no se rellena con ceros |
| `123456789Z` | 9 dígitos |
| `12345678` | Falta la letra |
| `12345678/Z` | La barra no se elimina |
| `ES12345678Z` | El prefijo de país no se elimina |
| `1234567AZ` | Letra donde debe ir un dígito |
| `X123456L` | NIE con 6 dígitos |
| `I12345674` | `I` no es letra de entidad |
| `O12345674` | `O` no es letra de entidad |
| `T12345674` | `T` no es letra de entidad |
| `K1234567D` | NIF de persona física `K`, fuera de A11 (D-03) |
| `1234567８Z` | El octavo dígito es `８` de ancho completo (U+FF18), no ASCII |
| `1234567ÑZ` | Letra fuera de `A`–`Z` |
| `12345678`, U+00A0 y `Z` | El espacio de no separación no es U+0020: no se elimina |
| `12345679ſ` | `ſ` (U+017F) no es `a`–`z` y no se convierte en `S`; con `upper()` saldría `12345679S`, un DNI con la letra correcta (resto 15) |

### 5.5 CIF: letras sin fuente oficial (D-01)

Numeración `1234567`, con C = 4 y letra `D`.

| Entrada | Resultado |
|---|---|
| `N1234567D`, `R1234567D`, `W1234567D` | Válido: exigen letra |
| `N12345674`, `R12345674`, `W12345674` | `invalid_tax_id_check_character`: dígito donde se exige letra |
| `C12345674`, `D12345674`, `F12345674`, `G12345674`, `J12345674`, `U12345674`, `V12345674` | Válido: admiten dígito |
| `C1234567D`, `D1234567D`, `F1234567D`, `G1234567D`, `J1234567D`, `U1234567D`, `V1234567D` | Válido: admiten letra |
| `C12345675`, `C1234567E` | `invalid_tax_id_check_character`: admitir ambas formas no es admitir cualquier valor |

### 5.6 Fuera de España

| País | Entrada | Resultado |
|---|---|---|
| `FR` | `ab-12 34` | Válido, se guarda `AB1234` |
| `PT` | `1234` | Válido: longitud mínima |
| `DE` | 20 caracteres alfanuméricos | Válido: longitud máxima |
| `PT` | `123` | `invalid_tax_id_format`: demasiado corto |
| `DE` | 21 caracteres alfanuméricos | `invalid_tax_id_format`: demasiado largo |
| `IT` | `1234.5678` | Válido, se guarda `12345678`: los puntos se eliminan |
| `IT` | `1234/5678` | `invalid_tax_id_format`: carácter no admitido |
| `FR` | `12345678A` | Válido: fuera de España no se calcula el control del DNI |
| `FR` | `ﬁ1234` | `invalid_tax_id_format`: la ligadura `ﬁ` (U+FB01) no es `a`–`z` y no se convierte en `FI`; con `upper()` saldría `FI1234`, que sería válido |
| `FR` | `AB`, U+00A0 y `1234` | `invalid_tax_id_format`: el espacio de no separación no se elimina |

### 5.7 Otros campos

| Campo | Valor | Resultado | Código por campo |
|---|---|---|---|
| `company_name` | `"  Ejemplo Uno SL "` | Válido; se guarda `Ejemplo Uno SL` | — |
| `company_name` | `"AB"` | Válido: mínimo | — |
| `company_name` | 120 caracteres | Válido: máximo | — |
| `company_name` | `" A "` | `422` | `too_short` |
| `company_name` | solo espacios | `422` | `too_short` |
| `company_name` | 121 caracteres | `422` | `too_long` |
| `company_name` | `"Ejemplo\nUno"` | `422` | `invalid_characters` |
| `company_name` | `"\nEjemplo Uno"` | `422` | `invalid_characters`: el salto de línea no se recorta |
| `company_name` | `"\tEjemplo Uno "` | `422` | `invalid_characters`: el tabulador tampoco |
| `company_name` | `"Ejemplo​Uno"` (espacio de anchura cero, Cf) | `422` | `invalid_characters` |
| `company_name` | `"A\n"` | `422` | `invalid_characters`, no `too_short`: un error por campo, el primero |
| `company_name` | 120 caracteres con `ñ` y `é` | Válido: se cuentan puntos de código | — |
| `tax_id` | 31 caracteres, país `ES` | `422` | `too_long`, no `invalid_tax_id_format` |
| `tax_id` | 31 caracteres, país `FR` | `422` | `too_long` |
| `tax_id` | `12345678Z` seguido de 21 espacios (30 en total), país `ES` | Válido: el límite es de 30 | — |
| `contact_email` | `"a\t@b.example"` | `422` | `invalid_characters` |
| `company_name` | `123` (número) | `422` | `not_a_string` |
| `contact_email` | `a@b.example` | Válido | — |
| `contact_email` | `sin-arroba.example`, `a@@b.example`, `@b.example`, `a@b`, `a b@c.example`, `a@.example` | `422` | `invalid_email` |
| `contact_email` | `a`, U+00A0 y `b@c.example` (espacio de no separación, Zs) | `422` | `invalid_email` |
| `contact_email` | `a@b.example` seguido de U+00A0 | `422` | `invalid_email`: en los extremos solo se recorta U+0020 |
| `contact_email` | `a`, U+3000 y `b@c.example` (espacio ideográfico, Zs) | `422` | `invalid_email` |
| `contact_email` | `a`, U+2028 y `b@c.example` (separador de línea, Zl) | `422` | `invalid_email` |
| `contact_email` | `a`, U+2029 y `b@c.example` (separador de párrafo, Zp) | `422` | `invalid_email` |
| `contact_email` | 255 caracteres | `422` | `too_long` |
| `country` | `US`, `XX`, `es`, `España`, `""` | `422` | `unsupported_country` |
| `plan` | `premium`, `Starter`, `""` | `422` | `unsupported_plan` |
| cualquiera | ausente | `422` | `missing` |
| cualquiera | `null` | `422` | `not_a_string` |
| adicional | `id` o `created_at` en la petición | `422` | `unknown_field` |
| `country` y `tax_id` | `XX` y `12345678A` | `422` | solo `unsupported_country` (E-18) |
| `country` y `tax_id` | `XX` y un identificador de 31 caracteres | `422` | `too_long` en `tax_id` y `unsupported_country`, en ese orden: la longitud no depende del país |
| `country` y `tax_id` | `XX` y `tax_id` ausente | `422` | `missing` en `tax_id` y `unsupported_country`, en ese orden |
| `country` y `tax_id` | `XX` y `tax_id` = `123` (número) | `422` | `not_a_string` en `tax_id` y `unsupported_country`, en ese orden |
| `country` y `tax_id` | `country` ausente y `12345678A` | `422` | solo `missing` en `country`: sin país no se valida el formato ni el control |
| `country` y `tax_id` | `country` = `34` (número) y un identificador de 31 caracteres | `422` | `too_long` en `tax_id` y `not_a_string` en `country`, en ese orden |
| `company_name` y `contact_email` | `"A"` y `sin-arroba.example` | `422` | `too_short` y después `invalid_email`, en ese orden |
| `plan`, `company_name` y un campo adicional `zeta` | `premium`, `"A"` y cualquier valor | `422` | `too_short`, `unsupported_plan` y `unknown_field`, en ese orden |

### 5.8 Duplicados

| Clientes guardados | Alta | Resultado |
|---|---|---|
| `ES` + `B12345674` | `ES` + `B12345674` | `409` |
| `ES` + `B12345674` | `ES` + `b-1234567 4` | `409`: se compara la forma normalizada |
| `ES` + `B12345674` | `PT` + `B12345674` | `201`: otro país |
| `ES` + `B12345674` | `ES` + `B12345674` y email no válido | `422`: gana la validación |
| `ES` + `B12345674` | `ES` + `A12345674`, mismo nombre | `201`: el nombre no es único |

### 5.9 Buscador

Datos de partida (todos de `ES` salvo que se indique):

| `id` | Nombre | Identificador |
|---|---|---|
| 1 | `Zeta Datos SL` | `B12345674` |
| 2 | `alfa Ejemplo SA` | `A24680241` |
| 3 | `Alfa Ejemplo SA` | `AB1234` (`FR`) |
| 4 | `Ñandú Pruebas SL` | `B99999997` |
| 5 | `100% Ejemplo SL` | `E99999997` |
| 6 | `Ejemplo_Uno SL` | `H00000000` |
| 7 | `José Pruebas SL` | `P1234567D` |

| `q` | `id` devueltos, en orden | Qué demuestra |
|---|---|---|
| `alfa` | 2, 3 | Sin distinguir mayúsculas; empate de nombre resuelto por `id` |
| `EJEMPLO` | 5, 2, 3, 6 | Coincidencia dentro del nombre; orden por nombre |
| `ñandú` | 4 | Mayúsculas fuera de ASCII |
| `nandu` | 4 | Ni la `Ñ` ni el acento distinguen (D-08) |
| `jose` | 7 | El acento del nombre guardado no distingue |
| `JOSÉ` | 7 | Tampoco el del texto buscado, ni sus mayúsculas |
| `b-12345` | 1 | El texto se normaliza para compararlo con el identificador |
| `b.1234` | 3, 1 | Los puntos también se eliminan; coincide con `AB1234` y `B12345674` |
| `9999999` | 5, 4 | Coincidencia por identificador; el orden sigue siendo por nombre |
| `%` | 5 | `%` literal, no «cualquier cosa» |
| `_` | 6 | `_` literal, no «un carácter» |
| `\` | — | El carácter de escape es literal |
| `' OR 1=1 --` | — | Texto tratado como dato |
| `noexiste` | — | `200` con lista vacía |
| `%00` (solo el carácter U+0000) | — | `200` con lista vacía: no coincide con nada, y no devuelve el listado inicial |
| `a%00` | — | `200` con lista vacía, aunque hay nombres con `a` |
| `%00a` | — | `200` con lista vacía |
| ausente, vacío o solo espacios | 5, 2, 3, 6, 7, 4, 1 | Listado inicial; `Ñandú` ordena como `nandu`, entre la `j` y la `z` |
| 101 caracteres | `422` | `too_long`, en el campo `q` |
| 100 caracteres seguidos de un espacio | `422` | `too_long`: el límite se mide antes de recortar |
| `q=alfa` y un parámetro `limit=5` | `422` | `unknown_field`, en el campo `limit` |

Además, con 25 clientes cuyo nombre contiene `Ejemplo`, la búsqueda
`ejemplo` devuelve exactamente los 20 primeros por nombre.

### 5.10 `id` de la ruta

| `GET /customers/…` | Resultado | Código en el campo `id` |
|---|---|---|
| `1` (existe) | `200` | — |
| `999` (no existe) | `404` `customer_not_found` | — |
| `9223372036854775807` (no existe) | `404` `customer_not_found` | — |
| `0` | `422` | `out_of_range` |
| `-1` | `422` | `out_of_range` |
| `9223372036854775808` (2^63) | `422` | `out_of_range` |
| 4301 nueves | `422` | `out_of_range` |
| 20000 nueves | `422` | `out_of_range` |
| un signo menos y 4301 nueves | `422` | `out_of_range` |
| `abc` | `422` | `not_an_integer` |
| `1.5` | `422` | `not_an_integer` |
| `1.0` | `422` | `not_an_integer` |
| `+1` | `422` | `not_an_integer` |
| `01` | `422` | `not_an_integer` |
| `1_0` | `422` | `not_an_integer` |
| `1` con un espacio delante (`%201`) | `422` | `not_an_integer` |
| `1` con un espacio detrás (`1%20`) | `422` | `not_an_integer` |

Las seis últimas filas son la forma única del `id` de la ruta (convenciones
del índice, «Identificadores»): con la forma se decide si es un entero y
después se aplica el rango.

Las tres filas de miles de nueves fijan que **un entero bien escrito, por
largo que sea, es un entero fuera del rango**: `out_of_range`, nunca un
`500`. 4301 dígitos es el primer tamaño que la biblioteca de validación
deja de leer como número.

## 6. Criterios de aceptación

| Id | Criterio | Requisitos |
|---|---|---|
| CA-01 | Un test unitario parametrizado del dominio reproduce cada fila de 5.1. | E-08 |
| CA-02 | Tests unitarios parametrizados reproducen cada fila de 5.2, 5.3 y 5.4, distinguiendo válido, error de formato y error de control. | E-09 a E-13, E-15, E-16 |
| CA-03 | Un test recorre las 23 letras de la tabla del DNI: para un número con cada resto de 0 a 22, la letra correcta se acepta y las otras 22 se rechazan como error de control. | E-11 |
| CA-04 | Un test recorre las 17 letras de entidad y los 10 valores de `C`, y comprueba que se acepta exactamente la forma (dígito, letra o ambas) del grupo de cada letra según 2.6, y reproduce cada fila de 5.5. | E-13 |
| CA-05 | Un test unitario reproduce cada fila de 5.6. | E-14 |
| CA-06 | Un test de integración envía el ejemplo de 4.1 y obtiene `201`, la cabecera `Location` y el cuerpo del ejemplo (salvo `id` y `created_at`), y `GET /customers/{id}` devuelve esos mismos siete campos; la comparación excluye `simulation_count` y `simulations`, que comprueba SPEC-03. | E-01, E-02, E-08, E-22 |
| CA-07 | Tests de integración cubren cada fila de 5.7, comprobando el estado, el `code`, el código por campo y el orden de `errors`, no el texto. | E-03 a E-07, E-18, E-34, E-35 |
| CA-08 | Tests de integración comprueban que un identificador con error de formato y otro con error de control devuelven códigos de campo distintos. | E-15, E-16 |
| CA-09 | Un test envía dos identificadores con controles correctos distintos y ambos incorrectos, y comprueba que los dos cuerpos de error son idénticos byte a byte. | E-17 |
| CA-10 | Tests de integración reproducen cada fila de 5.8, y comprueban que tras un `409` o un `422` el número de clientes guardados no cambia. | E-19, E-20, E-21 |
| CA-11 | Un test inserta directamente en la base de datos dos filas con el mismo país e identificador y la segunda falla por la restricción de unicidad. | E-19 |
| CA-12 | Tests de integración reproducen cada fila de 5.10. | E-22 a E-24 |
| CA-13 | Tests de integración reproducen cada fila de 5.9, incluidas las tres de error, y el caso de los 25 clientes, comprobando los `id` y su orden. | E-25 a E-27, E-29 a E-31 |
| CA-14 | Un test sustituye la conexión por una que registra las sentencias y comprueba que el texto buscado no aparece en el SQL ejecutado, solo en sus parámetros. | E-28 |
| CA-15 | Un test compara `GET /meta` con la constante única de países y la lista de planes del dominio y con el ejemplo de 4.4, y comprueba que cada país de `/meta` se acepta en el alta y que su tipo es el de la tabla 2.2 de SPEC-02. | E-32, E-05 |
| CA-16 | El OpenAPI generado declara para los cuatro endpoints los campos, tipos y códigos de estado del apartado 4. | E-01, E-22, E-25, E-32 |
| CA-17 | El oráculo comprueba que los módulos de validación fiscal de `domain/` no importan nada ajeno a la biblioteca estándar y tienen el 100 % de ramas cubiertas. | E-10 a E-14 |
| CA-18 | Un test unitario del dominio comprueba la forma de búsqueda de cada nombre de 5.9 (`José Pruebas SL` → `jose pruebas sl`, `Ñandú Pruebas SL` → `nandu pruebas sl`), y un test de integración comprueba que la columna guardada tras el alta coincide con ella. | E-33 |
| CA-19 | Un test diferencial compara el validador del dominio con `python-stdnum` (dependencia solo de test, con la versión fijada; ADR-005) sobre dos conjuntos. **Exhaustivo del CIF**: las 17 letras de entidad × los 10 valores de control × las dos formas (dígito y letra), 340 identificadores. **Aleatorio**: 10.000 números generados con la semilla fija `20261112`, escrita como constante en el test; con cada uno se forman un DNI, un NIE y un CIF, cada uno con su carácter de control correcto y con uno incorrecto. **Resultado esperado**: todo lo que acepta el dominio lo acepta `python-stdnum`, y lo único que `python-stdnum` acepta y el dominio rechaza son CIF con el valor de control correcto en una forma que el grupo de su letra no admite (D-01). Cualquier otra discrepancia hace fallar el test y la decide el Tech Lead. | E-11, E-12, E-13 |

**Sobre CA-17**: la comprobación la hace `scripts/check.py`, que existe
desde el 2026-11-12, igual que la de CA-09 de SPEC-02. Recorre el árbol
sintáctico de los módulos de `domain/` y exige el 100 % de sentencias y
ramas de `domain/`. Desde el 2026-11-13 la validación fiscal existe
(`app/domain/tax_id.py` y `app/domain/customers.py`) y el criterio se
comprueba en cada ejecución del oráculo.

**Sobre CA-19**: es lo que permite decir que R-04 se apoya, para el CIF, en
una convención contrastada con una implementación independiente y no solo
en casos generados con el propio algoritmo. **Comprobado el 2026-11-13**
con `python-stdnum` 2.2 (`stdnum.es.nif.is_valid`); el resultado esperado
de 2.7 se cumple:

- **Exhaustivo del CIF** (340 identificadores con el valor de control
  correcto, en las dos formas): el dominio no acepta ninguno que
  `python-stdnum` rechace, y `python-stdnum` acepta 100 que el dominio
  rechaza, todos por la forma del control: las 6 letras de entidad que
  exigen letra y las 4 que exigen dígito, por 10 valores (D-01).
- **Aleatorio** (semilla `20261112`, 10.000 números y 60.000
  identificadores): los dos validadores coinciden en todos, 30.000
  aceptados y 30.000 rechazados.

El test se repite en cada ejecución del oráculo. Si una versión nueva de la
biblioteca cambia el resultado, lo decide el Tech Lead.

## 7. Decisiones de diseño

Aprobadas o decididas por el Tech Lead el 2026-11-12. La columna «Origen»
dice si aprobó la propuesta de la IA o la cambió.

| Id | Decisión | Origen |
|---|---|---|
| D-01 | **Control del CIF**: cálculo de 2.6; exigen letra `P Q R S N W`, exigen dígito `A B E H`, admiten ambos `C D F G J U V`. Convención de uso común, sin fuente oficial localizada. Es el comportamiento con el que se contrastará el validador, y admitir ambos en los tipos dudosos no rechaza ningún CIF legítimo | Decidido por el Tech Lead; la IA no lo decidió por falta de fuente |
| D-02 | **Email de contacto** obligatorio (R-03), con validación de forma hecha a mano y sin dependencia nueva | Aprobada |
| D-03 | **NIF `K`, `L`, `M`** de persona física: error de formato; A11 fija tres formatos | Aprobada |
| D-04 | **Planes**: códigos `starter`, `professional`, `enterprise`; nombres para mostrar «Básico», «Profesional» y «Empresa» | Códigos aprobados; nombres cambiados (la IA proponía los nombres en inglés) |
| D-05 | **Límites**: nombre de 2 a 120; identificador extranjero de 4 a 20; entrada del identificador de 30 como máximo; `q` de 100 como máximo; email de 254 | Aprobada |
| D-06 | **El `409` no incluye** el `id` del cliente existente | Aprobada |
| D-07 | **`q` ausente o vacío** devuelve los 20 primeros por nombre | Aprobada |
| D-08 | **Los acentos no distinguen en el buscador.** El dominio calcula en el alta una forma de búsqueda del nombre (NFD, sin marcas diacríticas, `casefold`), guardada en su propia columna; se busca y se ordena sobre ella | Cambiada (la IA proponía que los acentos distinguieran) |
| D-09 | **País en minúsculas** (`es`): se rechaza | Aprobada |
| D-10 | **La normalización elimina también los puntos**: `12.345.678-Z` es una escritura frecuente y rechazarla no aporta seguridad | Cambiada (la IA los rechazaba, siguiendo el encargo de la sesión, que el Tech Lead rectificó) |
| D-11 | **País no válido o ausente**: se informa del país y, del identificador, solo de lo que no depende del país (`missing`, `not_a_string`, `too_long`); su formato y su control no se validan (E-18) | Aprobada; precisada por el Tech Lead tras la segunda evaluación (N-03) |
| D-12 | **`id` de ruta mal formado**: `422` | Aprobada |
| D-13 | **Historial**: SPEC-03 decide dónde va el historial. Resuelta por SPEC-03/D-01: va dentro de `GET /customers/{id}` (4.2) | Aprobada; resuelta el 2026-11-12 |
| D-14 | **Orden del buscador**: por la forma de búsqueda del nombre, de modo que la `Ñ` ordena como `N` y las vocales acentuadas como las no acentuadas | Aprobada con el cambio de D-08 (la IA proponía el orden por código de carácter, con la `Ñ` tras la `Z`) |
| D-15 | **Prueba diferencial con `python-stdnum`**, dependencia solo de test, para no apoyar el CIF únicamente en casos generados con el propio algoritmo (2.7, CA-19). La dependencia se registra en ADR-005 | Decidida por el Tech Lead tras la primera evaluación (H-06); CA-19 fijado tras la segunda (N-15) |

El criterio de qué decisiones llevan además un ADR está en
`02-arquitectura/README.md`. De esta tabla, lo lleva la dependencia de D-15
(ADR-005).

## 8. Pendiente antes de aprobar

**Nada pendiente desde el 2026-11-13.** El Tech Lead decidió A2 y A4 al
cumplirse la fecha límite, y la respuesta a la consulta llegó ese mismo
día, más tarde, sin cambiar ninguna regla de esta spec. La consulta está
cerrada (`supuestos.md`).

| Supuesto | Qué dice la respuesta | Efecto en esta spec |
|---|---|---|
| A2 · plan | El plan es informativo y no modifica el precio; sus valores son de libre elección | Ninguno. Se mantienen los códigos y los nombres de D-04, por decisión del Tech Lead |
| A4 · países y tipos | Basta con el tipo general de IVA del país del cliente. No menciona qué países se admiten | Ninguno. La lista de países de 2.1 sigue siendo decisión propia |

SPEC-02 y SPEC-03 forman con esta el bloque backend. Si cambian la
constante de países o la forma del historial, cambian 2.1, 4.2 y 4.4.

Sigue **sin verificar** la lectura directa de la página del Ministerio del
Interior (devolvió `403`) y su fecha.

## Historial

| Fecha | Cambio |
|---|---|
| 2026-11-12 | Primer borrador |
| 2026-11-12 | Revisión del Tech Lead: decididos los grupos de letras del CIF (D-01, filas de 5.5 y CA-04); los acentos dejan de distinguir en el buscador, con una forma de búsqueda guardada en columna propia (D-08, D-14, E-25, E-26, nuevo E-33 y CA-18, tabla 5.9); la normalización elimina también los puntos (D-10, 2.2, 5.1, 5.4, 5.6); nombres de los planes en español (D-04); sustituidos dos DNI de numeración baja en 5.2; aprobadas las demás decisiones |
| 2026-11-12 | Correcciones de la evaluación independiente (`04-calidad/evaluacion-specs-01.md`), decididas por el Tech Lead: la ficha incluye el historial y CA-06 lo excluye de la comparación (H-01); `id` de 1 a 9223372036854775807 y tabla 5.10 (H-04); prueba diferencial con `python-stdnum`, CA-19 (H-06); caso de parámetro desconocido en 5.9 (H-10); constante única de países, definida en SPEC-02 (H-12); referencias internas (H-13); ejemplos de `409` y de `422` (H-14); nuevo apartado 2.12 con el recorte, la unidad, el orden y la forma de los errores, E-34, E-35 y `too_long` para un identificador de más de 30 caracteres en cualquier país (H-22); precisión de `created_at` (H-23) |
| 2026-11-12 | Correcciones de la segunda evaluación independiente (`04-calidad/evaluacion-specs-02.md`), decididas por el Tech Lead: fila «Depende de» y aprobación en bloque con SPEC-02 y SPEC-03 (N-01); con un país no válido o ausente solo se comprueba del identificador lo que no depende del país, con E-18, 2.12, D-11 y cinco filas en 5.7 (N-03); normalización con «espacio» solo U+0020 y correspondencia explícita `a`–`z`, con casos de `ﬁ`, `ſ` y U+00A0 en 5.4 y 5.6 (N-11); el carácter de escape es `\` (N-12); D-15 y remisión a ADR-005 (N-14); CA-19 exacto y en futuro, con su resultado esperado (N-15, H-06); CA-19 dentro de la tabla (N-16); referencia de 4.1 (H-13) |
| 2026-11-12 | Decisión del Tech Lead sobre la cuestión Q-04 de la segunda respuesta: la semilla de CA-19 es `20261112` |
| 2026-11-13 | Decisión del Tech Lead al vencer la fecha límite sin respuesta externa: A2 y A4 pasan a `decidido (sin confirmación externa)` con la hipótesis ya documentada, sin cambios en las reglas; cabecera y apartado 8 actualizados. La consulta sigue abierta: si la respuesta llega, se aplica como cambio de esta spec |
| 2026-11-13 | Aprobación del Tech Lead: el estado pasa a `aprobada` (2026-11-13), a la vez que SPEC-02 y SPEC-03 (bloque backend) |
| 2026-11-13 | Confirmación del Tech Lead sobre el apartado 8: aprobó esta spec sabiendo que la lectura directa de la página del Ministerio del Interior sigue sin verificar. Motivo: el algoritmo queda cubierto por los vectores de prueba y por la prueba diferencial de CA-19. Sin cambios en requisitos, criterios ni casos |
| 2026-11-13 | Llega la respuesta a la consulta: confirma A2 (plan informativo, valores de libre elección) y, de A4, solo el uso del tipo general; la lista de países sigue siendo decisión propia. El Tech Lead mantiene los planes de D-04 y su visto bueno a esta spec. Cabecera y apartado 8 actualizados; la consulta queda cerrada. Motivo: registrar la fuente de cada supuesto. Sin cambios en reglas, requisitos, criterios ni casos |
| 2026-11-13 | Decisión del Tech Lead al revisar la implementación: el `id` de la ruta tiene una sola forma, escrita en las convenciones del índice («Identificadores»). Seis filas nuevas en 5.10 (`1.0`, `+1`, `01`, `1_0` y un espacio delante o detrás), todas `not_an_integer`; E-24 y CA-12 no cambian de texto y las cubren. Motivo: un cliente, una dirección; antes esas formas devolvían un cliente (`1_0`, el 10) |
| 2026-11-13 | Decisión del Tech Lead al revisar la implementación: fila `503` `service_unavailable` en las tablas de errores de 4.1, 4.2 y 4.3. Motivo: todo endpoint que lee la base de datos declara el `503` que ya responde (regla de las convenciones comunes); `GET /meta` no la lee y no lo declara. El OpenAPI de las tres operaciones lo declara (CA-16) |
| 2026-11-13 | Corrección ordenada por el Tech Lead: tres notas que habían quedado desfasadas dicen ahora lo que ya es un hecho. 2.7: `python-stdnum` 2.2 está instalada y la prueba diferencial se ha ejecutado. «Sobre CA-17»: `scripts/check.py` existe y comprueba el criterio en cada ejecución. «Sobre CA-19»: el resultado esperado se cumple, con sus cifras. Sin cambios en reglas, requisitos, criterios ni casos |
| 2026-11-13 | Corrección de la evaluación independiente del backend (`04-calidad/evaluacion-backend-01.md`, H-01), decidida por el Tech Lead: un entero bien escrito en la ruta, por largo que sea, responde `422` con `out_of_range`. Tres filas nuevas en 5.10 (4301 nueves, 20000 nueves y un signo menos con 4301 nueves); E-24 y CA-12 no cambian de texto y las cubren. Motivo: un `id` de 4301 dígitos o más respondía `500` `internal_error`, porque la biblioteca de validación deja de leerlo como número y su error no tenía código en el contrato |
| 2026-11-13 | Corrección de la evaluación independiente del backend (H-05 y H-11), decidida por el Tech Lead: un `q` con U+0000 devuelve la lista vacía, sin cambio en el contrato, y qué se compara lo decide el dominio, no la sentencia SQL. Dos puntos nuevos en 2.10 y tres filas en 5.9 (`%00`, `a%00` y `%00a`); E-25, E-31 y CA-13 no cambian de texto y las cubren. Motivo: SQLite corta el patrón de `LIKE` en ese carácter, de modo que `%00` devolvía el listado inicial y `a%00` buscaba «acaba en `a`»; y la condición de no comparar un identificador vacío estaba escrita en el SQL (`? <> ''`), contra 2.11 |
| 2026-11-13 | Corrección de la evaluación independiente del backend (H-08), decidida por el Tech Lead: un email con cualquier separador Unicode (categorías Zs, Zl y Zp) responde `invalid_email`. Regla del email en 2.1, punto nuevo en 2.12 y cinco filas en 5.7; E-04 y CA-07 no cambian de texto y las cubren. Motivo: «sin espacios» no decía qué es un espacio y solo se rechazaba U+0020, de modo que un email con un espacio de no separación se aceptaba y se guardaba tal cual; ese carácter llega al copiar y pegar un correo, y guardado así no sirve |
| 2026-11-13 | Corrección de la segunda pasada de la evaluación independiente del backend (`04-calidad/evaluacion-backend-02.md`, N-03), decidida por el Tech Lead: nota «Sobre E-30» tras la tabla de requisitos del buscador, que cita la limitación conocida L-04 (con un `q` repetido solo se valida el último). Sin cambios en requisitos, criterios ni casos. Motivo: quien leyera solo la spec no sabía que E-30 tiene esa desviación aceptada, registrada solo en `04-calidad/` |
