# ADR-009 · El alta de clientes se valida en el dominio, no con Pydantic

| | |
|---|---|
| **Estado** | `aceptado` (2026-11-13) |
| **Decide** | Tech Lead |
| **Requisitos** | R-03, R-04 |
| **Specs** | SPEC-01 (2.1, 2.11, 2.12; E-03 a E-07, E-18, E-34, E-35) |
| **Relacionado** | ADR-001 (FastAPI y Pydantic) · ADR-006 (formato de los errores) · `.claude/rules/backend.md` |

## Contexto

`.claude/rules/backend.md` dice que los esquemas de entrada de Pydantic
rechazan campos desconocidos y acotan rangos y longitudes. Así se valida
`POST /pricing/quote`: dos enteros, cada uno con su rango, sin relación
entre ellos.

El alta de clientes (`POST /customers`) no es así. SPEC-01 (2.12) fija:

- **Un orden de comprobaciones dentro de cada campo** y un solo error, el
  primero: en el nombre, `missing` → `not_a_string` → `invalid_characters`
  → `too_short` → `too_long`.
- **Reglas propias**: recortar solo el espacio U+0020, medir en puntos de
  código, rechazar las categorías Unicode Cc y Cf, normalizar el
  identificador sin `upper()`.
- **Una dependencia entre campos**: el formato y el carácter de control de
  `tax_id` dependen de `country`, y si el país no es válido solo se
  comprueba del identificador lo que no depende de él (E-18).
- **Todos los campos con error a la vez**, en el orden del contrato: un
  `tax_id` con formato incorrecto y un nombre demasiado corto salen en la
  misma respuesta.

Además, 2.11 dice que la normalización, la clasificación y el cálculo de
controles son funciones puras de `domain/`.

## Opciones

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **Una función pura de `domain/` valida el objeto JSON recibido** y devuelve un error por campo. La capa `api/` solo traduce a códigos y mensajes. Un modelo Pydantic documenta el contrato en el OpenAPI y no valida | Las reglas están donde 2.11 dice, en un solo sitio y probadas al 100 % de ramas sin red ni framework. El orden de las comprobaciones se lee de arriba abajo | Se aparta de `backend.md` en este endpoint. El modelo que documenta y el código que valida son dos cosas y pueden separarse |
| B | Validadores de Pydantic en el esquema de entrada | Lo que dice `backend.md`; un solo modelo documenta y valida | Las reglas de negocio de los campos quedan en `api/`, contra 2.11. Pydantic valida los campos en el orden en que se declaran y un validador solo ve los anteriores: para que `tax_id` conozca el país habría que declarar `country` antes, lo que cambia el orden publicado en el OpenAPI y el de `errors`; con un validador de modelo, el error del identificador no saldría cuando otro campo falla |
| C | Pydantic para la forma (presente, cadena, sin campos de más) y el dominio para los valores | Cada pieza hace lo suyo | Si falta un campo, Pydantic rechaza la petición antes de que el dominio vea los demás: no se informaría a la vez de un campo ausente y de un país no admitido, que es una fila de la tabla 5.7 |

## Decisión

**Opción A**, con tres condiciones del Tech Lead:

1. **El modelo que documenta y la validación real no pueden separarse.** Un
   test compara los campos, su orden, los obligatorios y el tipo que publica
   el OpenAPI de `POST /customers` con los que valida el dominio. El OpenAPI
   sigue declarando que no se admiten campos adicionales.
2. **El OpenAPI no declara ningún límite que el código no aplique
   exactamente así.** Si una longitud se mide tras recortar, no se publica
   como `maxLength` del valor recibido. En la práctica: del nombre y del
   email no se publica ninguna longitud; de `tax_id` sí el máximo de 30,
   que se mide sobre lo recibido; de `country` y `plan`, la lista de
   códigos, tomada de las constantes del dominio.
3. **La excepción es estrecha.** Pydantic sigue validando los endpoints
   cuyas reglas son por campo y sin dependencias entre campos, como
   `POST /pricing/quote`. El dominio valida a mano solo cuando la spec fija
   un orden de comprobaciones o una dependencia entre campos. Así queda
   escrito en `backend.md`, no como permiso general.

El cuerpo ausente sigue equivaliendo a `{}` (convenciones comunes): cinco
errores `missing`.

*Por qué*: la opción B obliga a elegir entre incumplir 2.11 y publicar un
contrato con los campos en otro orden, y la C no puede dar una fila de la
tabla de casos. La A cumple la spec tal como está escrita; su riesgo, que el
contrato publicado y la validación diverjan, se trata con un test y no con
buena voluntad.

## Consecuencias

A favor:

- Las reglas del alta se prueban como funciones puras, una fila de test por
  cada fila de la spec, y cuentan para el 100 % de ramas de `domain/`.
- El `422` del alta sale directamente con los códigos del contrato: no pasa
  por la traducción de errores de Pydantic.

En contra, y cómo se trata:

| Consecuencia | Tratamiento |
|---|---|
| Dos fuentes para el contrato del alta: el modelo que documenta y la función que valida | El test de la condición 1; falla si un campo, su orden, su obligatoriedad o su tipo difieren |
| El OpenAPI del alta dice menos que la spec: no publica las longitudes del nombre ni del email | Es la condición 2: mejor no decirlo que decirlo mal. Las reglas completas están en SPEC-01 (2.1) |
| Dos maneras de validar en el mismo backend | La regla de `backend.md` dice cuándo toca cada una |
| El dominio conoce `missing`, `not_a_string` y `unknown_field`, que son de forma y no de negocio | Aceptado: 2.12 los pone en la misma cadena de comprobaciones que el resto |

## Cuándo habría que revisarla

- Si otro endpoint necesitara validar a mano: habría que sacar a un sitio
  común lo que hoy es propio del alta, o revisar si la regla sigue siendo
  estrecha.
- Si SPEC-01 dejara de fijar el orden de las comprobaciones o la
  dependencia entre país e identificador: bastaría con Pydantic.

## Historial

| Fecha | Cambio |
|---|---|
| 2026-11-13 | Propuesto por la IA antes de la pieza (b) de SPEC-01 y aceptado por el Tech Lead con las tres condiciones |
