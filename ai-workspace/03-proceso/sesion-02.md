# Sesión 02 · SPEC-01 · Clientes y validación fiscal

| | |
|---|---|
| **Fecha** | 2026-11-12 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | *(se rellena al cerrar la sesión)* |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Leer antes `CLAUDE.md`, el README del workspace, los supuestos, el índice de
> specs, SPEC-02 como modelo de formato y la bitácora de la sesión 01. Abrir
> ya esta bitácora y anotar cada revisión en el momento.
>
> Tarea: SPEC-01 · Clientes y validación fiscal, con el formato de SPEC-02.
> Mínimos: alta, ficha, buscador y `GET /meta` (A13); campos y límites
> (nombre, país de A4, plan de A2, identificador fiscal); normalización antes
> de validar, sin rellenar ceros; DNI (módulo 23 con la tabla
> `TRWAGMYFPDXBNJZSQVHLCKE`); NIE (X/Y/Z → 0/1/2); CIF (letras de entidad y
> control con dígito o letra según el tipo, citando fuente oficial y fecha, y
> **diciendo si una letra es dudosa en lugar de decidirlo**); fuera de España
> solo formato (A10); errores con código estable que distingan formato de
> carácter de control sin revelar el valor correcto (A11); `409` por
> duplicado (A12); buscador sin distinguir mayúsculas, 20 resultados por
> nombre, consulta parametrizada y con `%` y `_` escapados; casos de prueba
> con identificadores sintéticos generados con el algoritmo, nunca reales,
> salvo el ejemplo público `12345678Z`.
>
> Dejarla en `borrador`, sin commit, y parar a esperar la revisión.

## 2. Cronología

| Hora | Commit | Qué |
|---|---|---|
| 14:04 | — | Lectura de los seis documentos indicados y de `requisitos.md`. Apertura de esta bitácora |
| 14:10 | — | Consulta de fuentes oficiales (apartado 4), generación de los identificadores sintéticos y redacción de SPEC-01 en `borrador`. Índice de specs actualizado. Sin commit, a la espera de revisión |
| 14:25 | — | Primera revisión de SPEC-01 por el Tech Lead (apartado 3) |
| 14:28 | `27a6581` | SPEC-01 en `borrador` con las decisiones de la revisión aplicadas; índice de specs; frase de A10 en `supuestos.md` |
| 14:30 | — | SPEC-03 en `borrador` e índice de specs actualizado. Sin commit, a la espera de revisión |
| 14:37 | — | Revisión de SPEC-03 por el Tech Lead (apartado 3) |
| 14:38 | `769e51c` | Enmienda del mensaje de `27a6581` para quitar el trailer `Co-Authored-By`. Antes se comprobó que `git diff --cached` estaba vacío; el contenido del commit no cambió (los mismos tres ficheros). `git log --pretty=%B \| grep -i co-authored` no devuelve nada. El commit no se había subido: el repo no tiene remoto |
| 14:38 | `8c9300c` | SPEC-03 en `borrador` con la revisión aplicada, e índice de specs |
| 14:38 | `f4bc741` | Regla «sin trailers de coautoría» en `CLAUDE.md` y `model: opus` en el subagente evaluador |
| 14:42 | — | SPEC-04 en `borrador` e índice de specs actualizado. Sin commit, a la espera de revisión |
| 14:53 | — | Revisión de SPEC-04 por el Tech Lead (apartado 3). Verificación de la `v2` de Frankfurter y de sus cabeceras CORS con curl |
| 14:56 | *(este commit)* | SPEC-04 en `borrador` con la revisión aplicada, índice de specs y esta bitácora, que entra por primera vez en un commit |
| 14:58 | — | El commit anterior es `1aeb653`. Lanzado el evaluador independiente sobre las cuatro specs |
| 15:05 | — | Informe del evaluador guardado tal cual en `04-calidad/evaluacion-specs-01.md`: 26 hallazgos (1 de severidad alta, 7 media, 18 baja). `git status` confirma que el evaluador no modificó ningún fichero. La IA no ha corregido nada ni ha valorado los hallazgos en el informe. Sin commit, a la espera de la revisión del Tech Lead |
| 15:13 | `292e96b` | Informe del evaluador, intacto, en un commit propio |
| 15:13 | — | Revisión del informe por el Tech Lead: decisiones sobre los 26 hallazgos (apartado 3) |
| 15:20 | `63a494c` | Correcciones de la evaluación en las cuatro specs, el índice, `supuestos.md`, `requisitos.md` (que pasa a `aprobado`), `CLAUDE.md`, las reglas por capa y ADR-002 |
| 15:20 | `3326b38` | ADR-003 (API de divisas) y ADR-004 (persistencia); «dos tablas» corregido en ADR-001; índice de arquitectura |
| 15:22 | *(este commit)* | Respuesta a la evaluación (`04-calidad/respuesta-evaluacion-specs-01.md`) y esta bitácora |

**Evaluador: no se pudo lanzar como subagente con nombre.** La sesión no
reconoció el tipo `evaluador` de `.claude/agents/evaluador.md` (la lista de
agentes disponibles no lo incluía). La IA lanzó en su lugar un subagente de
propósito general con contexto limpio y modelo `opus`, con la orden de leer
primero ese fichero y adoptar su papel y sus límites. Diferencia con lo
previsto: ese subagente sí dispone de herramientas de escritura; se le
ordenó no usarlas y la IA comprueba con `git status` que no ha tocado nada.
El encargo no incluía ninguna conclusión de la IA sobre las specs.

**Causa, indicada por el Tech Lead (15:09)**: el tipo `evaluador` no estaba
disponible porque los agentes se cargan al arrancar el proceso. Por eso se
usó la alternativa: subagente de propósito general, contexto limpio, modelo
`opus` y orden de solo lectura. La IA no ha comprobado esa causa por su
cuenta; solo constató que el tipo no figuraba entre los disponibles.

**Comprobación pedida por el Tech Lead (15:09)**, con `git status` y
`git diff --stat` tras terminar el evaluador:

- Único fichero modificado: `ai-workspace/03-proceso/sesion-02.md` (11
  líneas añadidas, todas escritas por la IA: las filas de cronología de las
  14:58 y las 15:05 y la nota sobre el evaluador).
- Único fichero sin seguimiento: `ai-workspace/04-calidad/evaluacion-specs-01.md`,
  el informe, que guardó la IA.
- Nada preparado en el índice. `HEAD` sigue en `1aeb653`.
- Ninguna spec, ADR, regla ni `CLAUDE.md` aparece modificado: el evaluador
  no escribió en el repo.

Límite de la comprobación: `git status` no muestra ficheros ignorados por
`.gitignore` ni nada escrito fuera del repo.

**Desviación que se anota**: la bitácora se creó después de leer los
documentos y de lanzar las primeras consultas a fuentes oficiales, no como
primera acción de la sesión. No había ocurrido todavía ninguna revisión.

## 3. Revisiones del Tech Lead

En cada tabla: qué propuso o hizo la IA, qué decidió el Tech Lead y por qué.

### SPEC-01 · Primera revisión (14:25)

El Tech Lead verificó por su cuenta los identificadores de 5.2 y 5.3 y el
orden de 5.9. Los motivos de la tabla son los que dio él; donde no dio
ninguno figura un guion.

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| s1 | D-01: no decidió los grupos de letras del CIF por falta de fuente oficial; marcó como dudosas `N`, `R`, `W` y `C`, `D`, `F`, `G`, `J`, `U`, `V` | **Decidido**: exigen letra `P Q R S N W`; exigen dígito `A B E H`; admiten ambos `C D F G J U V`. Se escribe como «convención de uso común, sin fuente oficial localizada; decidido por el Tech Lead». Fijar 5.5 y CA-04 | Es el comportamiento con el que se contrastará el validador, y admitir ambos en los tipos dudosos no rechaza ningún CIF legítimo |
| s2 | D-08: los acentos distinguían en el buscador (`jose` no encontraba `José`); una nota avisaba de que el `LIKE` de SQLite solo iguala mayúsculas en ASCII | **Descartado**: los acentos no distinguen. El dominio calcula en el alta una forma de búsqueda del nombre (casefold y sin marcas diacríticas, con NFD) que se guarda en su propia columna; se busca y se ordena sobre ella, con `LIKE` parametrizado y comodines escapados. Sustituye la nota sobre el `LIKE` | — |
| s3 | D-14: orden por código de carácter, con la `Ñ` después de la `Z` | **Cambiado** por s2: se ordena sobre la forma de búsqueda y la `Ñ` ordena como `N`. Aprobado con ese cambio | — |
| s4 | D-10: los puntos del identificador no se eliminaban (`12.345.678-Z` era error de formato), siguiendo el prompt de la sesión | **Descartado, rectificando su propio prompt**: la normalización elimina también los puntos. `1234.5678` en `IT` pasa a ser válido. Afecta también al buscador | Es una escritura frecuente y rechazarla no aporta seguridad |
| s5 | D-04: códigos `starter`, `professional`, `enterprise` y los mismos nombres en inglés para mostrar | **Aprobados los códigos; cambiados los nombres**: «Básico», «Profesional» y «Empresa» | — |
| s6 | Usó `00000022E` y `00000023T` en 5.2 mientras la propia spec decía evitar los DNI de numeración baja | **Corregido**: sustituirlos por `99999997E` (resto 22) y `99999998T` (resto 0), comprobados con el script | Son justo lo que la spec dice evitar |
| s7 | D-02, D-03, D-05, D-06, D-07, D-09, D-11, D-12, D-13 | **Aprobadas** | — |
| s8 | Dejó una línea en blanco que partía en dos la tabla de cronología de esta bitácora | **Ordenó arreglarla** | — |

Además pidió anotar estas decisiones, enseñar el diff, hacer el commit de
SPEC-01 con el mensaje que dio y pasar a SPEC-03, parando antes de su commit.

**Error propio en s6**: la IA escribió la regla («se evitan los números
bajos de DNI») y la incumplió dos filas más abajo, porque pensó solo en
`00000001` y siguientes. Lo detectó el Tech Lead, no la IA.

**Cambio no pedido al aplicar s4**: la IA actualizó también la frase de A10
en `supuestos.md` («sin espacios ni guiones» → «sin espacios, guiones ni
puntos») para que los dos documentos no se contradigan. **Entró en el commit
`27a6581` sin confirmación previa del Tech Lead**; se le avisó al entregar.

**Sobre el commit `27a6581`**: el diff se obtuvo añadiendo el primer
borrador al índice de git antes de aplicar las correcciones. El commit se
hizo en el mismo turno en que se enseñó el diff, sin esperar una segunda
confirmación, porque la instrucción pedía las dos cosas seguidas. El mensaje
lleva, además del título que dio el Tech Lead, un cuerpo con los requisitos
cubiertos y una línea `Co-Authored-By` de la IA, que los commits de la
sesión 01 no llevaban. Esta bitácora no entró en ese commit.

Al aplicar las decisiones, la IA retiró también dos frases propias: que
`00000000` «no es un número asignable» (afirmación sin fuente) y que la
lectura pendiente de la página del Ministerio del Interior no bloquea la
aprobación (eso lo decide el Tech Lead).

### SPEC-03 · Revisión (14:37)

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| t1 | Propuso D-01 a D-10 de SPEC-03 | **Aprobadas las diez**, con el cambio de t2 | La foto completa del cálculo en `simulation_tiers` y las restricciones `CHECK` de invariantes son el criterio que busca |
| t2 | Historial ordenado por `created_at` descendente y, a igualdad, por `id` descendente | **Cambiado**: solo por `id` descendente. Actualizar 2.4, E-13 y la tabla 5.3 | El `id` refleja el orden real de inserción; la fecha puede empatar o desajustarse si cambia el reloj |
| t3 | Añadió una línea `Co-Authored-By` al commit `27a6581` | **Descartado**: sin trailers de coautoría. Corregir solo el mensaje con `git commit --amend`, comprobando antes que no haya nada preparado; añadir la regla a `CLAUDE.md` y verificar con `git log --pretty=%B \| grep -i co-authored` | La autoría es de quien responde del cambio, y el uso de la IA ya se documenta entero en `ai-workspace/`. El commit no se había subido |
| t4 | El subagente evaluador no fijaba modelo en su cabecera | **Añadido**: `model: opus` | Que no herede un modelo pequeño de la configuración del entorno y que no comparta modelo con quien genera |

Pidió además dos commits separados, con el diff de cada uno, y pasar a
SPEC-04 parando antes de su commit.

**Incidente del trailer (t3)**. Al hacer el commit `27a6581`, la IA añadió
por su cuenta `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>`,
siguiendo una indicación por defecto de su herramienta. Los commits de la
sesión 01 no lo llevaban y el Tech Lead había dado el mensaje literal. La IA
lo avisó al entregar; no lo consultó antes. Corrección: ver la cronología
(el commit cambia de identificador al enmendarlo).

Sobre el cambio de A10 que entró en `27a6581` sin confirmación previa: el
Tech Lead no lo objetó en esta revisión, pero tampoco lo aprobó de forma
literal.

### SPEC-04 · Revisión (14:53)

| # | La IA | El Tech Lead | Motivo |
|---|---|---|---|
| u1 | D-01: propuso la `v1` de Frankfurter porque era la única respuesta que había verificado, dejando la `v2` como alternativa sin verificar | **Descartado**: usar la `v2` (`/v2/rates?base=EUR&quotes=USD,GBP,CHF`, una lista de `{date, base, quote, rate}`). Verificarla con una petición real, pegar la respuesta con su fecha en 4.2 y adaptar la validación de 2.6: exactamente un tipo mayor que 0 por divisa, con `base` EUR y `date` | La propia API declara obsoleta la `v1`; un proyecto nuevo no nace dependiendo de algo obsoleto |
| u2 | D-02: dejó el CORS de la API de divisas como no verificado, a comprobar al implementar | **Cerrada**: él comprobó que la `v1` y la `v2` devuelven `access-control-allow-origin: *`. Ordenó comprobarlo con curl enviando la cabecera `Origin` y anotarlo como verificado | — |
| u3 | D-09: comprobación *responsive* solo manual, para no añadir una dependencia | **Cambiado**: automatizar lo esencial con Playwright, con versión fijada y como dependencia de desarrollo: una prueba de principio a fin (alta → simulador → guardar → la simulación aparece la primera en el detalle) y la ausencia de desplazamiento horizontal a 375 px en las cuatro vistas. Las capturas manuales quedan como complemento en `04-calidad/`. Se implementa en la fase de QA | — |
| u4 | D-03 a D-08 y D-10 a D-13 | **Aprobadas** | — |
| u5 | Apartado 8 de SPEC-04: cambios en ADR-002 y en A8, sin aplicar | **Aplicarlos cuando se aprueben las specs, no ahora** | — |
| u6 | Dejó esta bitácora fuera de los tres commits de la sesión | **Incluirla** en el commit de SPEC-04, con estas decisiones | — |

Pidió además el diff, el commit de SPEC-04 y lanzar después el subagente
evaluador sobre las cuatro specs, sin corregir nada, guardando su informe
tal cual en `04-calidad/evaluacion-specs-01.md`.

**Sobre u1**: la IA eligió lo verificado frente a lo vigente y lo presentó
como decisión; pudo haber verificado la `v2` con una petición más antes de
proponer, y no lo hizo.

**Sobre u2**: la IA dio el CORS por pendiente cuando bastaba una petición
con curl y la cabecera `Origin`.

**Error propio en esta bitácora**: al anotar la revisión de SPEC-03, la IA
borró sin querer el encabezado «4. Comprobaciones hechas en la sesión». Lo
detectó al anotar esta revisión y lo restauró; la tabla no perdió filas.

### Informe del evaluador · Revisión (15:13)

Procedimiento fijado por el Tech Lead: **el informe no se toca; se responde a
cada hallazgo**. Primero un commit solo con el informe intacto; después las
correcciones, y un documento de respuesta
(`04-calidad/respuesta-evaluacion-specs-01.md`) con hallazgo, decisión,
motivo y dónde se cambió. Todas las decisiones de esta tabla son suyas. Donde
no dio motivo figura un guion.

| # | Hallazgo | Decisión del Tech Lead | Motivo |
|---|---|---|---|
| v1 | H-01, H-26, H-19 | Los cambios cruzados se aplican ya, no al aprobar: SPEC-01 4.2 describe la ficha con `simulation_count` y `simulations` y CA-06 los excluye de la comparación; ADR-002 a 200 ms; A8 con la lista cerrada; A17 con el alta en ruta propia | Con todo en borrador, mantener destinos incoherentes no tiene sentido |
| v2 | H-02, H-24 | Corregir cabeceras, índice y columnas «Afecta a» de supuestos y requisitos. **Aprueba `requisitos.md`**: pasa a `aprobado` con fecha de hoy | — |
| v3 | H-03 | Errores genéricos con `code` estable en las convenciones del índice: `400 malformed_request`, `415 unsupported_media_type`, `404 not_found`, `405 method_not_allowed` para cualquier método no admitido, `422 unknown_field` para un parámetro de consulta desconocido y `500 internal_error` sin trazas; todos en `problem+json` | — |
| v4 | H-04 | Todo `id`, de ruta o de cuerpo, es un entero de 1 a 9223372036854775807; fuera de rango, `422 out_of_range`. Añadir 0, −1 y 2^63 a las tablas de casos | Es el máximo de `INTEGER` en SQLite |
| v5 | H-05 | CORS y `/health` como requisitos EARS con su criterio, en un apartado «Operación del backend» de SPEC-03. Variable `CORS_ORIGINS`, por defecto `http://localhost:4200`. `GET /health` → `200 {"status":"ok"}` si la base de datos responde y `503` si no | — |
| v6 | H-06 | Prueba diferencial: `python-stdnum`, fijado como dependencia solo de test, valida DNI, NIE y CIF; un test compara los dos validadores en todas las letras de entidad y en miles de números generados. Toda discrepancia se documenta y la decide él. Nuevo CA en SPEC-01 y nota en R-04 | Romper la circularidad de unos casos generados con el propio algoritmo |
| v7 | H-07, H-08, H-21 | `frontend.md`: importes siempre enteros en céntimos. `CLAUDE.md`: excepción explícita para la conversión de divisa solo para mostrar. Corregir el código de ejemplo inexistente | — |
| v8 | H-12 | Una única constante de países (código, nombre y tipo en puntos básicos) en el dominio; los tipos los define SPEC-02 y SPEC-01 la usa. Corregir CA-15 | — |
| v9 | H-15 a H-18 | Un `422` por `id` mal formado y un `404` en el simulador muestran «Cliente no encontrado»; el panel muestra los nombres de `/meta`; la fecha del tipo de cambio se muestra tal cual, sin convertir de zona horaria; se elimina el escenario inalcanzable; un almacenamiento o un número de llamadas no válido no retira la proyección, solo desactiva «Guardar» | — |
| v10 | H-20 | ADR-003 (API de divisas) y ADR-004 (persistencia); corregir «dos tablas» en ADR-001 | — |
| v11 | H-22 | Recortar quita solo U+0020; cualquier carácter Cc o Cf → `invalid_characters`; longitudes en puntos de código; un error por campo, el primero que falle; `errors` en el orden de los campos del contrato; `field` es `id` para la ruta y `q` para la consulta; el límite de `q` se mide antes de recortar; un `tax_id` de más de 30 caracteres → `too_long` en cualquier país | — |
| v12 | H-23 | Columna `country` en `simulations`; `created_at` con precisión de segundos en las dos tablas | Que el historial lea solo lo guardado |
| v13 | H-09, H-10, H-11, H-13, H-14, H-25 | Corregirlos como propone el informe | — |

Pidió el diff resumido y tres commits separados (specs, arquitectura y
respuesta), y parar después.

**Autocrítica de la IA sobre H-01**: es el cambio cruzado que la IA anotó en
el apartado 8 de SPEC-03 y dejó sin aplicar «hasta aprobar la spec», una
regla que se puso ella sola y que dejaba dos contratos distintos para la
misma ficha.

**Cómo se aplicaron las correcciones (15:13–15:22)**. Fueron unas 120
sustituciones de texto en 14 ficheros. La IA las aplicó con un script
propio, fuera del repo, que exige que cada texto a sustituir aparezca
exactamente una vez y se detiene si no. Un primer intento sobre el índice y
los demás documentos falló por la forma de la ruta en Windows, sin llegar a
cambiar nada; se relanzó corregido.

**Precisiones añadidas por la IA sin que estuvieran en las decisiones**:
catorce, numeradas P-01 a P-14 en el apartado 2 de
`04-calidad/respuesta-evaluacion-specs-01.md`. Las más relevantes: el orden
de las comprobaciones de cada campo (P-01), la interpretación del `422` por
parámetro de consulta desconocido (P-04), el requisito y los casos de los
errores genéricos en SPEC-03, que no se habían pedido (P-05), y el código
`service_unavailable` del `503` (P-06). **Ninguna está aprobada.**

**Sobre H-14**: la instrucción era corregirlo «como propone el informe»,
pero el informe solo describe el defecto. La IA eligió el arreglo (P-10).

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estructura del NIF de entidades y letras de entidad | Lectura del texto consolidado de la Orden EHA/451/2008 en el BOE, delegada en un subagente de lectura web | 15 claves españolas (art. 3), `N` (art. 4) y `W` (art. 5). La orden no describe el cálculo del carácter de control ni cuándo es letra o dígito |
| Lo mismo, en la AEAT | Lectura de las páginas «Composición del NIF» de la guía del modelo 036 (actualizadas el 26/03/2026 y el 10/09/2026), delegada en un subagente | Coincide con la orden. Tampoco describe el control. Describe los NIF `K`, `L` y `M` de persona física |
| Decreto 2423/1975 | Lectura en el BOE, delegada en un subagente | Derogado desde el 01/01/2008. Su anexo es una imagen y no se pudo leer |
| Cálculo del DNI y del NIE | Búsqueda web; la lectura directa de la página del Ministerio del Interior devolvió `403` | El extracto del buscador recoge la división entre 23, la tabla, `12345678Z` y X/Y/Z → 0/1/2. No es una lectura directa |
| Identificadores de las tablas de SPEC-01 | Script aparte, fuera del repo, que aplica los algoritmos de 2.4 a 2.6 | `12345678` da resto 14 y letra `Z`, como el ejemplo público. Los demás valores de las tablas salen de esa ejecución |
| Orden esperado en la tabla 5.9 | Repaso a mano de cada fila | Corregidas dos filas antes de entregar (`9999999` tenía el orden invertido y `b-1234` coincidía también con `AB1234`) |
| DNI de sustitución y tabla 5.9 tras la revisión | Script aparte: restos de `99999997` y `99999998`, y simulación del buscador con la forma de búsqueda (NFD, sin `Mn`, `casefold`) | Restos 22 (`E`) y 0 (`T`). Las filas de 5.9 coinciden con la salida, incluido el listado inicial 5, 2, 3, 6, 7, 4, 1 |
| Importes de las tablas de SPEC-03 | Script aparte con la fórmula de SPEC-02 | Coinciden las siete filas de 5.1 y el caso sustituido de 5.4 (24000, 2400, 26400) |
| API pública de divisas (Frankfurter) | Lectura de su documentación y de tres respuestas reales, delegada en un subagente de lectura web | Sin clave ni cuotas. `v1/latest?base=EUR&symbols=USD,GBP,CHF` devuelve `200` con `base`, `date` y `rates`; la fecha era la de la víspera. La `v1` está declarada obsoleta pero disponible «indefinitely». Una divisa inexistente devolvió `404`, aunque la documentación habla de `422` |
| Importes convertidos y formato de la tabla 5.1 de SPEC-04 | Script aparte con Node 24.18.0 e `Intl.NumberFormat('es-ES')` | Todas las celdas salen de esa ejecución. En CHF, base más impuesto difiere del total en un céntimo |
| `v2` de Frankfurter | `curl` a `/v2/rates?base=EUR&quotes=USD,GBP,CHF`, a las 14:53 | `200`, lista de tres objetos `{date, base, quote, rate}` con fecha 2026-11-12: CHF 0,92316, GBP 0,83583, USD 1,1139. Con `quotes=XXX`, `422` e `invalid currency: XXX` |
| CORS de la API de divisas | `curl` con la cabecera `Origin: http://localhost:4200`, a la `v2` y a la `v1` | Las dos responden `access-control-allow-origin: *` y `access-control-allow-methods: GET, OPTIONS`. No se ha probado desde un navegador |
| Tabla 5.1 de SPEC-04 con los tipos de la `v2` | El mismo script de Node con los tipos nuevos | Recalculadas todas las celdas. El céntimo de diferencia pasa a estar en USD: 155,95 + 32,75 = 188,70 frente a 188,69 |
| Versión de Playwright | `npm view @playwright/test version engines.node` | 1.65.0, `node >=20`. No instalado ni ejecutado |
| Estado del repo tras el evaluador | `git status` y `git diff --stat`, a petición del Tech Lead | Solo esta bitácora modificada y el informe sin seguimiento; el evaluador no escribió en el repo |
| Versión de `python-stdnum` | Consulta a PyPI | 2.2, `requires_python >=3.8`. No instalado ni ejecutado |
| Trailers de coautoría | `git log --pretty=%B \| grep -i co-authored` tras cada commit | Sin resultados |
| Finales de línea tras las correcciones | Búsqueda de CRLF en `ai-workspace/`, `CLAUDE.md` y `.claude/rules/` | Ninguno |

## 5. No verificado

- **El cálculo del carácter de control del CIF y la tabla `JABCDEFGHI`**: no
  se encontró fuente oficial. Lo escribió la IA de memoria.
- **Qué letras de entidad exigen letra, dígito o admiten ambos**: igual. La
  IA marcó como dudosas `N`, `R`, `W` y `C`, `D`, `F`, `G`, `J`, `U`, `V`, y
  lo dejó como decisión D-01 en lugar de decidirlo.
- La página del Ministerio del Interior, leída directamente, y su fecha.
- Que los identificadores sintéticos no estén asignados a nadie: no se puede
  comprobar. Se eligieron números de patrón artificial y se evitaron los DNI
  de numeración baja.
- Las filas de las tablas 5.1, 5.3, 5.4, 5.6, 5.7, 5.8 y 5.9 no las ha
  ejecutado ningún código: son el comportamiento esperado, razonado a mano.
- ~~Que un navegador pueda llamar a la API de divisas (CORS)~~ y ~~la forma
  de la respuesta de la `v2`~~: verificados a las 14:53 (apartado 4). Sigue
  sin probarse desde un navegador real.
- El límite de peticiones de la API de divisas, su comportamiento en fines
  de semana y que los tres tipos traigan siempre la misma fecha.
- Playwright: solo se ha consultado su versión; no se ha instalado.
- Que el formato de `Intl.NumberFormat` del navegador coincida con el de
  Node 24 usado para la tabla 5.1 de SPEC-04.
- Las tablas 5.2 a 5.5 de SPEC-04 y 5.2 a 5.5 de SPEC-03 son comportamiento
  esperado; no las ha ejecutado ningún código.
- Si la validación del CIF de `python-stdnum` coincide con los grupos de
  letras de SPEC-01: no se ha ejecutado. Es lo que debe mostrar la prueba
  diferencial (SPEC-01, CA-19).
- Las tablas de casos nuevas que salen de las correcciones: comportamiento
  esperado, sin código que las ejecute.
- Que FastAPI permita devolver los estados y códigos de los errores
  genéricos (en especial `400` y `415`) sin código a medida.
- Las specs corregidas no han pasado por una segunda evaluación
  independiente.

## 6. Propuestas de la IA no pedidas en el encargo

Se anotan para que el Tech Lead las vea como añadidos y no como parte de lo
pedido. Todas están en el apartado 7 de SPEC-01, sin aprobar.

- `contact_email`: el encargo de la sesión no lo citaba; R-03 sí (D-02).
- Nombres de los planes, inventados (D-04).
- Todos los límites numéricos (D-05).
- `q` vacío devuelve un listado inicial (D-07).
- Rechazo de caracteres de control en el nombre.
- R-11, A14 y A18 añadidos a la fila de SPEC-01 del índice de specs.

En SPEC-03 (apartado 7 de la spec, sin aprobar):

- Guardar el desglose por tramos en una tabla propia (D-02).
- Unidades, nombres y máximos de almacenamiento y llamadas, inventados
  (D-03, D-04).
- Límite de 50 simulaciones en el historial y `simulation_count` (D-05).
- `405` con `method_not_allowed` (D-08) y variable `DATABASE_PATH` (D-10).
- Columnas de la tabla `customers`, que salen de SPEC-01 pero no estaban
  escritas en ninguna parte.
- A9 y A14 añadidos a la fila de SPEC-03 del índice de specs.
- SPEC-03 obliga a retocar SPEC-01 (4.2 y CA-06); no se ha aplicado.

En SPEC-04 (apartado 7 de la spec, sin aprobar): la elección de Frankfurter
y de su `v1` (D-01), CHF como cuarta divisa (D-03), el código de divisa en
lugar del símbolo (D-05), las rutas y el simulador en vista propia (D-07),
el control deslizante de 0 a 500 (D-08), todos los tiempos (D-10) y la
comprobación *responsive* manual (D-09). A13, A14 y A16 añadidos a la fila
de SPEC-04 del índice.

## 7. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| Revisión por el Tech Lead de las correcciones y de las precisiones P-01 a P-14 | Ahora |
| Segunda evaluación independiente de las specs corregidas | A decidir por el Tech Lead |
| Aprobación literal del cambio de A10 que entró en el commit de SPEC-01 | Cuando el Tech Lead lo vea |
| Playwright: prueba de principio a fin y comprobación a 375 px | Fase de QA |
| DDL definitivo (`schema.sql`) | Con el esqueleto del backend |
| Decidir A2 a A5 | Viernes 13 de noviembre de 2026, 10:00 |
