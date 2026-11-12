# SPEC-01 · Clientes y validación fiscal

| | |
|---|---|
| **Estado** | `borrador` (2026-11-12) |
| **Requisitos** | R-03, R-04 y la parte de backend de R-10 y R-11 |
| **Supuestos** | A10, A11, A12, A13, A14 y A18 (`decidido`) · A2 y A4 (`pendiente de confirmar`) |
| **Bloqueos para aprobarla** | A2 y A4 sin respuesta (con fecha límite, ver apartado 8) |

## 1. Objetivo

Definir el alta de clientes corporativos, la validación de su identificador
fiscal, la consulta de la ficha, el buscador y los datos de apoyo de los
formularios.

**Dentro**: `POST /customers`, `GET /customers/{id}`, `GET /customers?q=`,
`GET /meta`, normalización y validación del identificador fiscal, unicidad.

**Fuera**: historial de simulaciones dentro de la ficha (SPEC-03), cálculo
del impuesto (SPEC-02), formulario y vistas (SPEC-04), edición y borrado
(A18), `GET /health` (se especifica con el esqueleto del backend).

## 2. Reglas de negocio

### 2.1 Campos del cliente

| Campo | Regla |
|---|---|
| `company_name` | Texto. Se recortan los espacios de los extremos; el resultado tiene de 2 a 120 caracteres y ningún carácter de control (saltos de línea, tabuladores). Se guarda recortado |
| `tax_id` | Texto de 30 caracteres como máximo antes de normalizar. Se normaliza (2.2), se valida según el país (2.3 a 2.7) y **se guarda normalizado** |
| `contact_email` | Texto. Se recortan los extremos; 254 caracteres como máximo; sin espacios; exactamente una `@`, con texto delante y un dominio detrás que contiene al menos un punto y no empieza ni acaba en punto. No se comprueba que el buzón exista |
| `country` | Uno de los códigos de la tabla de A4, en mayúsculas: `ES`, `PT`, `FR`, `DE`, `IT`, `NL`, `IE`, `BE`, `GB` |
| `plan` | Uno de los códigos de la lista cerrada: `starter` («Básico»), `professional` («Profesional»), `enterprise` («Empresa») (A2). Dato informativo, sin efecto en el precio |

Los cinco son obligatorios y deben ser cadenas JSON. El sistema añade `id`
(entero positivo) y `created_at` (fecha y hora UTC en ISO 8601).

### 2.2 Normalización del identificador

Se aplica **antes de validar**, igual para todos los países, y en este orden:

1. Se eliminan todos los espacios, todos los guiones (`-`) y todos los
   puntos (`.`), estén donde estén.
2. Las letras de la `a` a la `z` pasan a mayúsculas.

Nada más: **no se rellenan ceros a la izquierda**, no se quitan otros signos
y no se quita un prefijo de país (`ES…`). Lo que quede debe estar formado
solo por los caracteres ASCII `0`–`9` y `A`–`Z`; cualquier otro carácter (una
barra, una `Ñ`, un dígito de otro alfabeto) es un error de formato.

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
Las 15 primeras de la lista oficial son de entidades españolas; `N` es
entidad extranjera y `W` establecimiento permanente de entidad no residente.

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
- Las dos comparaciones se hacen con `LIKE` y una cláusula `ESCAPE`: `%`,
  `_` y el propio carácter de escape del texto buscado se escapan y se
  buscan como texto literal.
- El texto llega a la base de datos siempre como parámetro, nunca
  concatenado en la sentencia.
- Resultado: como máximo 20 clientes, ordenados por la forma de búsqueda del
  nombre y, a igualdad, por `id` ascendente.

### 2.11 Dónde vive

Normalización, clasificación, cálculo de controles y forma de búsqueda son
funciones puras de `backend/app/domain/`, igual que las listas de países y
planes. La API y la base de datos no repiten ninguna de esas reglas.

## 3. Requisitos (EARS)

### Alta y campos

| Id | Requisito | Cubre |
|---|---|---|
| E-01 | Cuando recibe un alta válida, el sistema deberá guardar el cliente y responder `201` con el cliente creado y la cabecera `Location` de su ficha. | R-03 |
| E-02 | El sistema deberá recortar los espacios de los extremos del nombre y del email antes de validarlos y guardarlos. | R-03 |
| E-03 | Si el nombre recortado tiene menos de 2 o más de 120 caracteres, o contiene caracteres de control, entonces el sistema deberá rechazar el alta. | R-03 |
| E-04 | Si el email no cumple la regla de 2.1, entonces el sistema deberá rechazar el alta. | R-03 |
| E-05 | Si el país no es uno de los códigos de A4 escrito en mayúsculas, entonces el sistema deberá rechazar el alta en lugar de aceptarlo con un impuesto del 0 %. | A4 |
| E-06 | Si el plan no es uno de los códigos de la lista cerrada, entonces el sistema deberá rechazar el alta. | A2 |
| E-07 | Si falta un campo, un campo no es una cadena o la petición trae un campo no documentado, entonces el sistema deberá rechazar el alta. | A14 |

### Identificador fiscal

| Id | Requisito | Cubre |
|---|---|---|
| E-08 | El sistema deberá normalizar el identificador (sin espacios, guiones ni puntos, en mayúsculas) antes de validarlo, y guardar y devolver siempre la forma normalizada. | A10, A11 |
| E-09 | El sistema no deberá completar con ceros ni corregir de ningún otro modo un identificador para que resulte válido. | A11 |
| E-10 | Mientras el país es España, el sistema deberá aceptar solo identificadores que encajen en el patrón de DNI, NIE o CIF de 2.3. | R-04, A11 |
| E-11 | Mientras el país es España, el sistema deberá comprobar la letra del DNI con el resto de dividir su número entre 23 y la tabla `TRWAGMYFPDXBNJZSQVHLCKE`. | R-04 |
| E-12 | Mientras el país es España, el sistema deberá comprobar la letra del NIE sustituyendo la inicial `X`, `Y` o `Z` por `0`, `1` o `2` y aplicando el cálculo del DNI. | R-04 |
| E-13 | Mientras el país es España, el sistema deberá comprobar el carácter de control del CIF con el cálculo de 2.6, exigiendo dígito, letra o cualquiera de los dos según el grupo de su letra de entidad. | R-04 |
| E-14 | Mientras el país no es España, el sistema deberá comprobar únicamente que el identificador normalizado tiene de 4 a 20 caracteres alfanuméricos. | A10 |
| E-15 | Si el identificador no encaja en ningún patrón admitido para su país, entonces el sistema deberá rechazar el alta con el código de campo `invalid_tax_id_format`. | A11 |
| E-16 | Si el identificador encaja en un patrón español pero su carácter de control no es el correcto o no tiene la forma exigida, entonces el sistema deberá rechazar el alta con el código de campo `invalid_tax_id_check_character`. | A11 |
| E-17 | El sistema no deberá incluir en ninguna respuesta de error el carácter de control correcto ni ningún dato del que pueda deducirse. | A11 |
| E-18 | Si el país no es válido, entonces el sistema deberá informar del error del país y no validar el identificador, que depende de él. | — |

### Unicidad

| Id | Requisito | Cubre |
|---|---|---|
| E-19 | Si ya existe un cliente con el mismo país e identificador normalizado, entonces el sistema deberá responder `409` con el código `customer_already_exists` y no guardar nada. | A12 |
| E-20 | El sistema deberá permitir el mismo identificador normalizado en dos países distintos. | A12 |
| E-21 | Si un alta tiene a la vez errores de validación y un duplicado, entonces el sistema deberá responder `422`. | — |

### Ficha

| Id | Requisito | Cubre |
|---|---|---|
| E-22 | Cuando recibe `GET /customers/{id}` de un cliente existente, el sistema deberá responder `200` con sus datos. | R-11, A13 |
| E-23 | Si no existe un cliente con ese `id`, entonces el sistema deberá responder `404` con el código `customer_not_found`. | A13 |
| E-24 | Si el `id` de la ruta no es un entero positivo, entonces el sistema deberá responder `422` con el código `validation_error`. | A14 |

### Buscador

| Id | Requisito | Cubre |
|---|---|---|
| E-25 | Cuando recibe `GET /customers?q=`, el sistema deberá devolver los clientes cuyo nombre contiene el texto, comparando las formas de búsqueda de ambos (sin distinguir mayúsculas ni acentos), o cuyo identificador fiscal contiene el texto normalizado. | R-10 |
| E-26 | El sistema deberá devolver como máximo 20 clientes, ordenados por la forma de búsqueda del nombre y, a igualdad, por `id`. | A13 |
| E-27 | El sistema deberá tratar `%`, `_` y el carácter de escape del texto buscado como caracteres literales. | R-10 |
| E-28 | El sistema deberá pasar el texto buscado a la base de datos únicamente como parámetro de la consulta. | R-10 |
| E-29 | Cuando `q` falta o queda vacío tras recortarlo, el sistema deberá devolver los 20 primeros clientes por orden de nombre. | A13 |
| E-30 | Si `q` supera los 100 caracteres o la petición trae un parámetro no documentado, entonces el sistema deberá responder `422`. | A14 |
| E-31 | Cuando ningún cliente coincide, el sistema deberá responder `200` con una lista vacía. | R-10 |
| E-33 | Cuando guarda un cliente, el sistema deberá calcular en el dominio la forma de búsqueda de su nombre (NFD, sin marcas diacríticas, `casefold`) y guardarla en una columna propia. | R-10 |

### `GET /meta`

| Id | Requisito | Cubre |
|---|---|---|
| E-32 | El sistema deberá devolver en `GET /meta` los países admitidos, con su código, nombre y tipo impositivo, y los planes, con su código y nombre, tomados de las mismas constantes del dominio que usan la validación y el cálculo. | A13, A2, A4 |

## 4. Contratos

### 4.1 `POST /customers`

| Campo | Tipo | Obligatorio | Regla |
|---|---|---|---|
| `company_name` | cadena | sí | 2 a 120 caracteres tras recortar |
| `tax_id` | cadena | sí | Según el país (2.2 a 2.8) |
| `contact_email` | cadena | sí | Regla de 2.1 |
| `country` | cadena | sí | Código de A4 en mayúsculas |
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

El `message` de los dos errores del identificador es un texto fijo: no cambia
con el valor recibido. El `409` no incluye datos del cliente existente (ver
D-06).

### 4.2 `GET /customers/{id}`

Respuesta `200`: el mismo objeto que devuelve el alta. SPEC-03 define cómo se
obtiene el historial de simulaciones de la ficha (dentro de esta respuesta o
en un endpoint propio); esta spec no lo fija.

| Estado | `code` | Cuándo | Códigos por campo |
|---|---|---|---|
| `404` | `customer_not_found` | No existe un cliente con ese `id` | — |
| `422` | `validation_error` | El `id` no es un entero positivo | `not_an_integer`, `out_of_range` |

### 4.3 `GET /customers?q=`

| Parámetro | Tipo | Obligatorio | Regla |
|---|---|---|---|
| `q` | cadena | no | 100 caracteres como máximo |

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
| `422` | `validation_error` | `q` demasiado largo o parámetro desconocido | `too_long`, `unknown_field` |

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
| cadena de 31 caracteres | Supera el máximo antes de normalizar |

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
| `company_name` | `123` (número) | `422` | `not_a_string` |
| `contact_email` | `a@b.example` | Válido | — |
| `contact_email` | `sin-arroba.example`, `a@@b.example`, `@b.example`, `a@b`, `a b@c.example`, `a@.example` | `422` | `invalid_email` |
| `contact_email` | 255 caracteres | `422` | `too_long` |
| `country` | `US`, `XX`, `es`, `España`, `""` | `422` | `unsupported_country` |
| `plan` | `premium`, `Starter`, `""` | `422` | `unsupported_plan` |
| cualquiera | ausente | `422` | `missing` |
| cualquiera | `null` | `422` | `not_a_string` |
| adicional | `id` o `created_at` en la petición | `422` | `unknown_field` |
| `country` y `tax_id` | `XX` y `12345678A` | `422` | solo `unsupported_country` (E-18) |

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
| ausente, vacío o solo espacios | 5, 2, 3, 6, 7, 4, 1 | Listado inicial; `Ñandú` ordena como `nandu`, entre la `j` y la `z` |
| 101 caracteres | `422` | `too_long` |

Además, con 25 clientes cuyo nombre contiene `Ejemplo`, la búsqueda
`ejemplo` devuelve exactamente los 20 primeros por nombre.

## 6. Criterios de aceptación

| Id | Criterio | Requisitos |
|---|---|---|
| CA-01 | Un test unitario parametrizado del dominio reproduce cada fila de 5.1. | E-08 |
| CA-02 | Tests unitarios parametrizados reproducen cada fila de 5.2, 5.3 y 5.4, distinguiendo válido, error de formato y error de control. | E-09 a E-13, E-15, E-16 |
| CA-03 | Un test recorre las 23 letras de la tabla del DNI: para un número con cada resto de 0 a 22, la letra correcta se acepta y las otras 22 se rechazan como error de control. | E-11 |
| CA-04 | Un test recorre las 17 letras de entidad y los 10 valores de `C`, y comprueba que se acepta exactamente la forma (dígito, letra o ambas) del grupo de cada letra según 2.6, y reproduce cada fila de 5.5. | E-13 |
| CA-05 | Un test unitario reproduce cada fila de 5.6. | E-14 |
| CA-06 | Un test de integración envía el ejemplo de 4.1 y obtiene `201`, la cabecera `Location` y el cuerpo del ejemplo (salvo `id` y `created_at`), y `GET /customers/{id}` devuelve el mismo objeto. | E-01, E-02, E-08, E-22 |
| CA-07 | Tests de integración cubren cada fila de 5.7, comprobando el estado, el `code` y el código por campo, no el texto. | E-03 a E-07, E-18 |
| CA-08 | Tests de integración comprueban que un identificador con error de formato y otro con error de control devuelven códigos de campo distintos. | E-15, E-16 |
| CA-09 | Un test envía dos identificadores con controles correctos distintos y ambos incorrectos, y comprueba que los dos cuerpos de error son idénticos byte a byte. | E-17 |
| CA-10 | Tests de integración reproducen cada fila de 5.8, y comprueban que tras un `409` o un `422` el número de clientes guardados no cambia. | E-19, E-20, E-21 |
| CA-11 | Un test inserta directamente en la base de datos dos filas con el mismo país e identificador y la segunda falla por la restricción de unicidad. | E-19 |
| CA-12 | Tests de integración cubren el `404` y el `422` de `GET /customers/{id}` (`abc`, `0`, `-1`, `1.5`). | E-23, E-24 |
| CA-13 | Tests de integración reproducen cada fila de 5.9 y el caso de los 25 clientes, comprobando los `id` y su orden. | E-25 a E-27, E-29 a E-31 |
| CA-14 | Un test sustituye la conexión por una que registra las sentencias y comprueba que el texto buscado no aparece en el SQL ejecutado, solo en sus parámetros. | E-28 |
| CA-15 | Un test compara `GET /meta` con las constantes del dominio y con el ejemplo de 4.4, y comprueba que cada país de `/meta` se acepta en el alta y tiene tipo en la tabla de SPEC-02. | E-32, E-05 |
| CA-16 | El OpenAPI generado declara para los cuatro endpoints los campos, tipos y códigos de estado del apartado 4. | E-01, E-22, E-25, E-32 |
| CA-17 | El oráculo comprueba que los módulos de validación fiscal de `domain/` no importan nada ajeno a la biblioteca estándar y tienen el 100 % de ramas cubiertas. | E-10 a E-14 |
| CA-18 | Un test unitario del dominio comprueba la forma de búsqueda de cada nombre de 5.9 (`José Pruebas SL` → `jose pruebas sl`, `Ñandú Pruebas SL` → `nandu pruebas sl`), y un test de integración comprueba que la columna guardada tras el alta coincide con ella. | E-33 |

**Sobre CA-17**: depende de `scripts/check.py`, que aún no existe; hasta
entonces está **pendiente de implementar**, igual que CA-09 de SPEC-02.

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
| D-11 | **País no válido**: solo se informa del país; el identificador no se valida (E-18) | Aprobada |
| D-12 | **`id` de ruta mal formado**: `422` | Aprobada |
| D-13 | **Historial**: `GET /customers/{id}` devuelve aquí solo los datos del cliente; SPEC-03 decide dónde va el historial | Aprobada |
| D-14 | **Orden del buscador**: por la forma de búsqueda del nombre, de modo que la `Ñ` ordena como `N` y las vocales acentuadas como las no acentuadas | Aprobada con el cambio de D-08 (la IA proponía el orden por código de carácter, con la `Ñ` tras la `Z`) |

## 8. Pendiente antes de aprobar

| Asunto | Qué cambiaría en esta spec |
|---|---|
| A2 · plan | Si el plan tuviera significado propio, la lista de 2.1 y `/meta` |
| A4 · países y tipos | La lista de países de 2.1 y el ejemplo de 4.4 |

**Fecha límite**: si el viernes 13 de noviembre de 2026 a las 10:00 no hay
respuesta, el Tech Lead decide estos dos supuestos con la hipótesis ya
documentada. Pasan a `decidido (sin confirmación externa)` y esta spec puede
aprobarse. Si la respuesta llega después, se revisan.

Queda además **sin verificar** la lectura directa de la página del
Ministerio del Interior (devolvió `403`) y su fecha. Si eso bloquea la
aprobación lo decide el Tech Lead.

## Historial

| Fecha | Cambio |
|---|---|
| 2026-11-12 | Primer borrador |
| 2026-11-12 | Revisión del Tech Lead: decididos los grupos de letras del CIF (D-01, filas de 5.5 y CA-04); los acentos dejan de distinguir en el buscador, con una forma de búsqueda guardada en columna propia (D-08, D-14, E-25, E-26, nuevo E-33 y CA-18, tabla 5.9); la normalización elimina también los puntos (D-10, 2.2, 5.1, 5.4, 5.6); nombres de los planes en español (D-04); sustituidos dos DNI de numeración baja en 5.2; aprobadas las demás decisiones |
