---
paths:
  - "backend/**"
---

# Backend (Python 3.12 · FastAPI · Pydantic v2 · SQLite · uv)

## Capas y dependencias

```
backend/app/
  api/           routers, esquemas Pydantic de entrada y salida, mapeo de errores
  services/      casos de uso: orquestan dominio y repositorios
  domain/        reglas de negocio como funciones puras
  repositories/  acceso a SQLite
backend/tests/
  unit/          dominio y servicios, sin red ni disco
  integration/   API y repositorios contra una base de datos temporal
```

Las dependencias van en un solo sentido: `api → services → domain` y
`services → repositories`.

- **`domain/` no importa FastAPI, Pydantic, `sqlite3` ni nada de las otras
  capas**, y no hace entrada/salida ni lee el reloj. *Por qué: así las reglas
  de negocio se prueban de forma exhaustiva y rápida, y sobreviven a un cambio
  de framework o de base de datos.*
- **Los routers son finos**: validan la entrada, llaman a un servicio y
  devuelven la respuesta. Sin condicionales de negocio ni SQL.
- **El SQL solo aparece en `repositories/`** y siempre parametrizado; nunca se
  construye concatenando o formateando cadenas.

## FastAPI y Pydantic

- Cada endpoint declara `response_model` y sus códigos de estado; el OpenAPI
  generado es el contrato y debe coincidir con la tabla de la spec.
- Los esquemas de entrada rechazan campos desconocidos (`extra="forbid"`) y
  acotan rangos y longitudes. Los esquemas de la API no se reutilizan como
  modelos de dominio ni de persistencia.
- Las dependencias (conexión, servicios) se inyectan con `Depends`; nada de
  estado global mutable.
- Los errores de dominio son excepciones propias que la capa `api/` traduce a
  respuestas HTTP en un único sitio. Las respuestas de error no exponen trazas
  ni detalles internos.
- Cada error lleva un **código estable en inglés y en `snake_case`** (p. ej.
  `invalid_tax_id_format`) y un mensaje legible en español. Los códigos se definen
  en un único módulo, figuran en la spec y no se renombran: son parte del
  contrato. Los tests comprueban el código, no el texto del mensaje.
- La configuración (ruta de la base de datos, orígenes CORS) llega por
  variables de entorno con valores por defecto para local; CORS limitado al
  origen del frontend.

## Calidad

- `ruff` (lint y formato) y `mypy --strict` sin avisos. Todas las funciones
  llevan anotaciones de tipo.
- `domain/` se cubre al 100 % de ramas; el oráculo falla por debajo de ese
  umbral (`--cov-branch --cov-fail-under=100`) *(lo implementa el oráculo,
  pendiente)*.

## Tests (pytest)

- Fichero: `tests/<unit|integration>/test_<módulo>.py`.
- Nombre: `test_<qué>_<condición>_<resultado>`, por ejemplo
  `test_base_price_with_15_users_is_140_eur`.
- Cada test cita en su docstring el requisito EARS que comprueba
  (`SPEC-02/E-03`), para poder generar la matriz de trazabilidad.
- Los casos límite de una regla se escriben como tabla con
  `pytest.mark.parametrize`, uno por fila de la spec.
- Los tests no dependen del orden, de la red ni de datos de otro test.
