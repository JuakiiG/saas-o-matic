# ADR-001 · Stack tecnológico

| | |
|---|---|
| **Estado** | `aceptado` (2026-11-12) |
| **Decide** | Tech Lead |
| **Requisitos** | R-01, R-02, R-08 |

## Contexto

El encargo pide dos piezas separadas que se comunican entre sí: un frontend
interactivo y un backend con base de datos. Fija **SQLite**, prefiere Node.js
con TypeScript o Python para el backend y deja libre el frontend. Solo exige
ejecución en local.

Lo que pesa en la elección:

- El contrato de la API debe poder leerse y comprobarse (se valora la
  planificación previa).
- Las validaciones y el cálculo tienen que ser exactos y estar muy probados.
- El código lo genera una IA bajo dirección: cuanto más opinado sea el
  framework, menos margen hay para que mezcle estilos.
- El plazo es de pocos días.

## Backend

| Criterio | Python + FastAPI | Node.js + TypeScript (Fastify o NestJS) |
|---|---|---|
| Admitido por el encargo | Sí | Sí |
| Validación de entrada | Pydantic v2, declarativa y estricta | Zod o TypeBox, equivalente |
| Contrato de la API | OpenAPI generado de serie a partir de los tipos | Requiere un plugin y mantenerlo alineado |
| Dinero sin coma flotante | Enteros de precisión arbitraria de serie | `number` es coma flotante; exige disciplina o `bigint` |
| Tests | pytest, con casos en tabla muy legibles | Vitest o Jest, equivalente |
| Experiencia previa de quien revisa | Alta | Menor |

**Decisión: Python 3.12 + FastAPI + Pydantic v2, gestionado con uv; pytest,
ruff y mypy.**

Motivos:

1. El OpenAPI sale del propio código, así que el contrato de la spec se puede
   comparar con lo que de verdad expone la API.
2. Los enteros de Python no desbordan ni pierden precisión, lo que encaja con
   guardar el dinero en céntimos (A6).
3. Quien revisa cada diff conoce bien este stack. Auditar código generado
   exige entenderlo sin esfuerzo.

## Frontend

| Criterio | Angular | React + Vite |
|---|---|---|
| Admitido por el encargo | Sí | Sí |
| Estructura | Opinada: inyección de dependencias, `HttpClient`, formularios reactivos tipados y tests, todo de serie | Se compone con librerías a elegir (datos remotos, formularios, rutas) |
| Margen para que la IA mezcle estilos | Menor: hay una forma canónica de casi todo | Mayor: cada librería trae sus patrones |
| Estados de carga y error | Signals y RxJS, con cancelación de peticiones nativa | Depende de la librería elegida |
| Curva de aprendizaje y ceremonia | Mayor | Menor |

**Decisión: Angular con componentes standalone, signals, modo estricto y
ESLint.**

Motivos:

1. Trae resuelto lo que este proyecto necesita (HTTP, formularios, rutas,
   tests), sin sumar dependencias ni decisiones.
2. Sus convenciones se pueden escribir como reglas cortas y comprobables
   (ver `.claude/rules/frontend.md`).
3. La cancelación de peticiones de RxJS es justo lo que pide la proyección en
   tiempo real (ADR-002).

Descartados:

- **Next.js y similares**: unen frontend y backend en un solo proyecto, y el
  encargo pide dos piezas que se comunican.
- **Vue y Svelte**: válidos, pero sin ninguna ventaja aquí frente a los dos
  comparados.

## Versiones

| Pieza | Versión | Comprobación |
|---|---|---|
| Node.js | 24 | Rango `engines` de Angular CLI |
| Angular CLI | **21.2.29** (LTS) | Etiqueta `v21-lts` del registro de npm el 2026-11-12. Su campo `engines` declara `node: ^20.19.0 \|\| ^22.12.0 \|\| >=24.0.0` (consultado con `npm view @angular/cli@21.2.29 engines`) |
| Python | 3.12 | — |
| uv | Fija las dependencias de Python en `uv.lock` | — |

El frontend se crea con `npx @angular/cli@21.2.29`, nunca con `latest`. Las
versiones exactas de FastAPI, Pydantic y el resto quedan fijadas en los
ficheros de bloqueo (`uv.lock`, `package-lock.json`) al crear cada proyecto.

**Por qué la 21 y no la 22**, que es la estable más reciente (22.2.6) y
también admite Node 24:

1. La 21 es una versión con soporte de larga duración.
2. La IA que genera el código conoce mejor la 21 que la 22. Eso reduce el
   riesgo de que use APIs inventadas o mal recordadas en un código que luego
   hay que auditar.

**Verificado**: la compatibilidad declarada por el paquete. **No
verificado** todavía: que el proyecto se cree, compile y pase sus tests con
esa combinación; se comprobará al crearlo.

**Comprobado de nuevo el 2026-11-14**, antes de aprobar SPEC-04, con el
margen de una semana de ADR-007 (fecha de corte de ese día:
`2026-11-07T00:00:00Z`) y las fechas del registro de npm. **La decisión no
cambia.**

| Pieza | Versión elegible con el margen | Publicada | Nota |
|---|---|---|---|
| Angular CLI (`@angular/cli`, con `@angular/build` y `@schematics/angular`) | 21.2.29 | 2026-10-28 | La etiqueta `v21-lts` apunta desde el 2026-11-12 a la 21.2.30, que queda fuera del margen |
| Paquetes de Angular (`@angular/core`, `common`, `compiler`, `compiler-cli`, `forms`, `platform-browser` y `router`) | 21.2.26 | 2026-11-02 | Es la última de la línea 21. Su numeración no es la del CLI |
| TypeScript | 5.9.3 | 2025-09-30 | El CLI 21.2.29 escribe `~5.9.2` en un proyecto nuevo |
| RxJS | 7.8.2 | 2025-02-22 | El CLI escribe `~7.8.0` |
| Vitest, el runner por defecto del CLI 21 | 4.1.12 | 2026-10-15 | El CLI escribe `^4.0.8`, con `jsdom` `^28.0.0` (28.1.0, del 2026-02-15) |

El CLI 21.2.29 y los paquetes 21.2.26 declaran
`node: ^20.19.0 || ^22.12.0 || >=24.0.0`. Los rangos que escribe el CLI se
leyeron en su paquete de plantillas publicado, sin instalar nada. Las
versiones exactas se fijan en `package-lock.json` al crear el proyecto; la
tabla completa, con ESLint y Playwright, está en la bitácora de la sesión
06. **Sigue sin verificar** lo mismo que arriba: que el proyecto se cree,
compile y pase sus tests.

**Versiones exactas del frontend, decididas el 2026-11-14** con el plan
(sesión 06, decisiones P-01 y P-02). Son las que resuelve npm con la fecha
de corte `2026-11-07T00:00:00Z` (ADR-007), y se escriben en `package.json`
sin rangos.

| Dependencia directa | Versión | Publicada | De dónde sale |
|---|---|---|---|
| `@angular/common`, `compiler`, `core`, `forms`, `platform-browser` y `router` | 21.2.26 | 2026-11-02 | El CLI, que escribe `^21.2.0` |
| `rxjs` | 7.8.2 | 2025-02-22 | El CLI (`~7.8.0`) |
| `tslib` | 2.9.1 | 2026-10-30 | El CLI (`^2.3.0`) |
| `@angular/cli` y `@angular/build` (desarrollo) | 21.2.29 | 2026-10-28 | El CLI |
| `@angular/compiler-cli` (desarrollo) | 21.2.26 | 2026-11-02 | El CLI |
| `typescript` (desarrollo) | 5.9.3 | 2025-09-30 | El CLI (`~5.9.2`) |
| `vitest` (desarrollo) | 4.1.12 | 2026-10-15 | El CLI (`^4.0.8`) |
| `jsdom` (desarrollo) | 28.1.0 | 2026-02-15 | El CLI (`^28.0.0`) |
| `prettier` (desarrollo) | 3.9.10 | 2026-10-10 | El CLI (`^3.8.1`) |
| `@vitest/coverage-v8` (desarrollo) | 4.1.12 | 2026-10-15 | **Nueva**: la cobertura del 80 % de líneas que exige el oráculo |
| `eslint` (desarrollo) | 10.14.0 | 2026-10-30 | **Nueva**: la decisión de este ADR |
| `@eslint/js` (desarrollo) | 10.0.1 | 2026-02-06 | **Nueva**: las reglas recomendadas de ESLint, que ESLint 10 ya no trae consigo |
| `angular-eslint` (desarrollo) | 21.4.0 | 2026-05-13 | **Nueva**: las reglas de Angular y de sus plantillas |
| `typescript-eslint` (desarrollo) | 8.72.1 | 2026-10-26 | **Nueva**: ESLint sobre TypeScript |
| `@playwright/test` (desarrollo) | 1.65.0 | 2026-11-05 | **Nueva**, instalada el 2026-11-15, en la fase de QA (ADR-005) |
| `@types/node` (desarrollo) | 24.19.2 | 2026-10-09 | **Nueva**, instalada el 2026-11-15 por decisión del Tech Lead (sesión 08): los tipos de Node que necesita `tsc` para comprobar `e2e/` y `playwright.config.ts` dentro de `npm run lint`. Trae `undici-types` 7.24.6 (2026-03-25) |

**Comprobado el 2026-11-14 en un ensayo fuera del repositorio**, con Node
24.18.0 y npm 11.16.0: el proyecto que crea el CLI 21.2.29 se instala con
estas versiones sin conflictos, compila y pasa los dos tests que trae.
**No verificado todavía**: lo mismo dentro del repositorio, con la
aplicación.

Dos consecuencias de quedarse en estas versiones, aceptadas: las
correcciones posteriores a la fecha de corte no entran (ADR-007), y
`npm audit` da avisos de gravedad moderada en herramientas de desarrollo
(limitación conocida L-07).

## Acceso a SQLite

| Opción | A favor | En contra |
|---|---|---|
| **Módulo `sqlite3` de la biblioteca estándar**, con SQL parametrizado dentro de `repositories/` | Ninguna dependencia; el SQL es visible y revisable; tres tablas no justifican más | Sin migraciones automáticas; el mapeo de filas a objetos se escribe a mano |
| SQLAlchemy 2 Core | Portabilidad a otra base de datos; constructor de consultas | Una dependencia grande y una capa más que entender para tres tablas |
| ORM completo (SQLAlchemy ORM o SQLModel) | Menos código de mapeo | Oculta el SQL; fácil acabar con lógica en los modelos |

**Decisión: `sqlite3` de la biblioteca estándar**, con un `schema.sql`
versionado y una conexión por petición. Los endpoints serán funciones
síncronas, que FastAPI ejecuta en su grupo de hilos. *Por qué*: es la opción
más pequeña que cumple, y la capa `repositories/` ya aísla el resto del
código, de modo que cambiar de base de datos más adelante afecta solo a esa
capa.

Al aceptar este ADR se contaba con dos tablas; SPEC-03 define tres
(`customers`, `simulations` y `simulation_tiers`), y el texto de la tabla
se corrigió el 2026-11-12. La decisión no cambia. El modelo de datos y sus
alternativas están en ADR-004.

**Cada conexión ejecuta `PRAGMA foreign_keys = ON` al abrirse.** SQLite no
aplica las claves foráneas por defecto, y sin ese ajuste aceptaría una
simulación de un cliente que no existe. Un test lo comprobará intentando
guardar exactamente eso y esperando el rechazo de la base de datos.

## Fuera de alcance

Nube, infraestructura como código y contenedores como requisito. Docker
Compose es opcional y, si se hace, va al final.

## Consecuencias

A favor:

- Contrato de la API generado y comprobable.
- Dos proyectos independientes con una frontera HTTP clara; cualquiera de los
  dos se podría sustituir sin tocar el otro.

En contra:

- Dos lenguajes y dos cadenas de herramientas. Se mitiga con un único comando
  de comprobación (`scripts/check.py`).
- Angular exige más ceremonia que otras opciones. Se mitiga con un alcance de
  interfaz pequeño y cerrado, la configuración por defecto del CLI y reglas
  explícitas.
- Quien revisa tiene menos experiencia en Angular que en Python. Se mitiga
  con reglas explícitas, revisión explicada de cada componente generado y el
  evaluador independiente.
- Las interfaces TypeScript de la API se escriben a mano a partir del
  contrato y pueden desalinearse. Se mitiga con tests del frontend que usan
  las respuestas de ejemplo de las specs.
