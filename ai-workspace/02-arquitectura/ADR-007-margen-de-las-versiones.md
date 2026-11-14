# ADR-007 · Margen de una semana para las versiones de las dependencias

| | |
|---|---|
| **Estado** | `aceptado` (2026-11-13) |
| **Decide** | Tech Lead |
| **Requisitos** | R-01, R-02 |
| **Specs** | Ninguna en particular: afecta a las dependencias de los dos proyectos |
| **Relacionado** | ADR-001 (stack y versiones) · ADR-005 (dependencias de test) · `CLAUDE.md` («Sin dependencias nuevas sin aprobación. Versiones siempre fijadas») |

## Contexto

Al crear el backend el 2026-11-13, las dependencias se resolvieron a la
última versión publicada. Varias tenían días u horas: `ruff` 0.17.5 y
`coverage` 7.17.3 eran del día anterior, `fastapi` 0.162.5 del día 11,
`annotated-doc` 0.0.6 del 10 y `click` 8.5.1 del 6.

Una versión recién publicada ha tenido poco tiempo para que alguien detecte
un fallo grave o una publicación maliciosa. Fijar la versión exacta
(`uv.lock`) evita que cambie sola, pero no dice nada de la que se fija.

## Opciones

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **Fecha de corte**: `exclude-newer` en `[tool.uv]`, con una fecha una semana anterior al día en que se resuelve | Lo aplica la herramienta, no la memoria de nadie; la fecha queda escrita en `pyproject.toml` y en `uv.lock`; resolver dos veces da lo mismo | Las correcciones llegan una semana tarde; la fecha hay que moverla a mano |
| B | La última versión siempre | Nada que mantener | Es lo que se hizo al crear el esqueleto: versiones de la víspera |
| C | Revisar a mano cada versión antes de fijarla | El control más fino | No se sostiene con más de treinta paquetes entre directos y transitivos |

**Decisión: opción A**, con `exclude-newer = "2026-11-06T00:00:00Z"`. La IA
había fijado las últimas versiones (opción B) y planteó la A como
alternativa sin aplicarla; el Tech Lead la eligió.

## Reglas

1. Ninguna dependencia, directa o transitiva, se fija en una versión
   publicada después de la fecha de corte.
2. Para actualizar se adelanta la fecha, como mucho hasta una semana antes
   del día en que se hace, y se vuelve a resolver. El cambio de versiones se
   enseña en una tabla de antes y después.
3. **Excepción**: si una versión que queda fuera corrige un fallo de
   seguridad publicado, la IA lo dice y decide el Tech Lead.
4. El oráculo ejecuta las herramientas con `uv run --locked`: un `uv.lock`
   que no corresponde a `pyproject.toml` falla en vez de reescribirse.

## Efecto el 2026-11-13

| Paquete | Sin margen | Con la fecha de corte | Publicada |
|---|---|---|---|
| `fastapi` | 0.162.5 | 0.162.0 | 2026-10-23 |
| `ruff` | 0.17.5 | 0.17.4 | 2026-11-05 |
| `coverage` | 7.17.3 | 7.17.2 | 2026-11-04 |
| `click` | 8.5.1 | 8.5.0 | 2026-08-26 |
| `annotated-doc` | 0.0.6 | 0.0.5 | 2026-07-28 |

Las demás no cambian. Lo que queda fuera, según las notas de versión de cada
proyecto en GitHub: en `fastapi`, dos correcciones (0.162.4 exige AnyIO
4.1.0 o posterior en ejecución; 0.162.5 corrige la limpieza de dependencias
síncronas al cancelarse la petición) y cambios de documentación; ninguna
nota de las versiones saltadas menciona seguridad.

## No verificado

- Las notas de versión se buscaron por palabras («security», «CVE»,
  «GHSA», «advisory», «vulnerab»); no se leyeron enteras, salvo el apartado
  de correcciones de `fastapi` 0.162.4 y 0.162.5.
- Que no existan avisos de seguridad solo se consultó en PyPI y en OSV, el
  2026-11-13, para las cinco versiones a las que se retrocede y para
  `httpx2`, `httpcore2`, `httpx2-jsfetch`, `truststore`, `starlette` y
  `pydantic`. No para los otros 23 paquetes.
- **El frontend.** Esta decisión nombra el mecanismo de uv. Cómo se aplica
  el mismo margen con npm no está decidido ni probado, y no se ha comprobado
  la fecha de publicación de Angular CLI 21.2.29 (ADR-001). Se decide al
  crear el frontend. **Añadido el 2026-11-14**: la fecha ya está
  comprobada en el registro de npm. Angular CLI 21.2.29 se publicó el
  2026-10-28 y cumple el margen; la 21.2.30, del 2026-11-12, no (tabla en
  ADR-001). El mecanismo **sigue sin decidir**: el npm del equipo
  (11.16.0) tiene dos opciones de configuración que podrían servir,
  `before` y `min-release-age`, vistas en su lista de opciones y sin
  probar. **Decidido el 2026-11-14**: apartado «El mecanismo en npm».

## El mecanismo en npm (2026-11-14)

Decisión del Tech Lead al aprobar el plan del frontend (sesión 06, P-01 y
P-03), después de probar las dos opciones en una carpeta temporal fuera
del repositorio, con npm 11.16.0.

| | Opción | A favor | En contra |
|---|---|---|---|
| **A** | **`before` con una fecha fija**, en `frontend/.npmrc` | Es el equivalente de `exclude-newer`: la fecha queda escrita en el repositorio, resolver dos veces da lo mismo y adelantarla se ve en un diff | La fecha hay que moverla a mano |
| B | `min-release-age=7`, en `frontend/.npmrc` | Nada que mover | Es una ventana que avanza sola: la misma orden da un árbol distinto según el día y no deja escrito con qué corte se resolvió |

**Decisión: opción A.** `frontend/.npmrc`, versionado, lleva dos líneas:

```
before=2026-11-07T00:00:00Z
save-exact=true
```

Lo que se probó, con las dos opciones salvo donde se dice:

| Caso | Resultado |
|---|---|
| Un rango (`prettier@3`) | Resuelve a la última versión anterior al corte (3.9.10; sin la opción, 3.10.1) |
| Una versión exacta posterior al corte | Falla con `ETARGET`, sin instalar |
| `npm exec` de un paquete posterior al corte (solo con `before`) | Falla con `ETARGET` |
| El árbol entero de un proyecto de Angular con sus herramientas (solo con `before`) | 652 versiones de 620 paquetes, ninguna posterior al corte |
| **Un fichero de bloqueo que ya trae una versión posterior al corte**, con `npm ci` y con `npm install` | **La instalan sin avisar** |

**Lo que npm no hace, y cómo se trata.** El margen actúa al resolver: ni
`before` ni `min-release-age` revisan un `package-lock.json` ya escrito, y
la fecha no queda dentro de él. Por eso, en el frontend:

1. `package.json` lleva versiones exactas, sin rangos (`save-exact=true`).
2. `package-lock.json` está versionado y las instalaciones se hacen con
   `npm ci`, que falla si no corresponde a `package.json`. Es el
   equivalente de la regla 4.
3. Cada vez que el fichero de bloqueo cambia, se consulta en el registro la
   fecha de publicación de cada una de sus entradas y el resultado se anota
   en la bitácora. **El oráculo no lo comprueba.**
4. El CLI se ejecuta con el mismo corte
   (`npm exec --before=… --package=@angular/cli@21.2.29`), para que el
   margen alcance también a lo que arrastra al crear el proyecto.

**La regla 3, aplicada el 2026-11-14.** `npm audit` da avisos de gravedad
moderada en `minimatch` y `glob`, que llegan por ESLint, `typescript-eslint`
y el CLI. ESLint 10.15.0 corrige su parte y se publicó el 2026-11-13, fuera
del margen. La IA lo dijo y el Tech Lead decidió **no hacer la excepción**:
el fallo afecta solo a herramientas de desarrollo, la excepción no quitaba
los avisos de las otras dos y la versión tenía un día. Queda como
limitación conocida L-07, con la fecha en que se vuelve a mirar.

## Consecuencias

A favor:

- Ninguna versión entra con menos de una semana de vida sin que alguien lo
  decida.
- La resolución es repetible: la fecha forma parte del lock.

En contra, y cómo se trata:

| Consecuencia | Tratamiento |
|---|---|
| Las correcciones de fallos llegan una semana tarde | Regla 3 para las de seguridad; las demás esperan |
| La fecha no avanza sola | Se adelanta al actualizar dependencias, no en cada sesión |
| Un paquete nuevo puede no tener ninguna versión anterior a la fecha | Lo decide el Tech Lead, como cualquier dependencia nueva |

## Cuándo habría que revisarla

- Al crear el frontend, para fijar el mecanismo equivalente en npm.
- Si el margen obliga a quedarse en una versión con un fallo que afecte al
  proyecto.
