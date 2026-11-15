# Respuesta a la evaluación independiente del frontend

| | |
|---|---|
| **Fecha** | 2026-11-15 |
| **Responde a** | [`evaluacion-frontend-01.md`](evaluacion-frontend-01.md), que no se modifica |
| **Decide** | Tech Lead. **Sin decidir**: la columna «Qué propone la IA» es una propuesta. **No se ha aplicado nada** |
| **Escribe** | IA (Claude Code) |
| **Estado del código** | El informe evaluó el repositorio en `bab2922`, con el árbol limpio |

Procedimiento: el informe del evaluador no se modifica; se responde a cada
hallazgo. Antes de responder, la IA ha repetido por su cuenta, solo
leyendo y ejecutando, lo que cada hallazgo afirma (apartado 2). **Los diez
hallazgos se reproducen** en lo que la IA ha podido comprobar; lo que no ha
podido comprobar está en el apartado 5.

Resumen de la respuesta:

- **De acuerdo, error de la IA en esta sesión** (2): H-07 (la prueba de la
  fecha del tipo cita E-27 y es E-29) y H-08 (una orden habitual de
  Playwright reescribiría las capturas versionadas).
- **De acuerdo, estaba en el código desde la sesión 07** y ni los tests ni
  las tres paradas lo vieron (5): H-02, H-03, H-04, H-06 y H-09.
- **De acuerdo con el hecho, con un matiz sobre lo que significa** (3):
  H-01, H-05 y H-10.
- **En desacuerdo**: ninguno.
- **Cuatro casos más**, que salen de leer el informe y no son hallazgos
  suyos: filas B-01 a B-04 (apartado 3).
- **Decisiones que no son de redacción** y piden al Tech Lead elegir:
  H-01 (si un `id` codificado es otra dirección), H-02 (dos colores), H-03
  y H-04 (cuánta accesibilidad entra, que pide requisitos nuevos en
  SPEC-04), H-09 (test o criterio) y H-10 (si se pone una política de
  contenido).

## 1. Respuesta por hallazgo

| Hallazgo | Grav. | ¿De acuerdo? | Qué propone la IA | Qué habría que tocar |
|---|---|---|---|---|
| H-01 · Un cliente tiene más de una dirección: el router descodifica el segmento | baja | **Sí en el hecho; con matiz.** Reproducido con el serializador de Angular 21.2.26: `/clientes/%31` da el segmento `1` y `/clientes/1;x=y`, también. Matiz: `%31` y `1` son la misma dirección para la norma de las URL (RFC 3986, 6.2.2.2: un carácter no reservado codificado equivale al carácter), y **el backend hace lo mismo**: `GET /customers/%31` responde `200` con el cliente 1 (sondeado con el cliente de test). Lo que sí es propio del frontend es `;x=y`: Angular lo lee como parámetro de matriz y lo aparta, mientras que el backend responde `422` a `/customers/1;x=y` | **Lo decide el Tech Lead.** **Recomendada**: no tocar el código y precisar 2.1: el filtro se aplica al segmento **ya descodificado por el router**, que es lo que la fila de `1%20` de 5.7 ya da por hecho; añadir a 5.7 las filas de `%31` (se pide el cliente 1) y de `1;x=y` (se pide el cliente 1; el parámetro de matriz no forma parte del `id`). **Alternativa**: leer el segmento sin descodificar de la dirección del navegador y rechazar lo que no sea igual a su forma descodificada; es código nuevo que se salta al router, para un caso que solo se da escribiendo la dirección a mano. **Antes de decidir convendría verlo en un navegador**: la IA no sabe si Angular reescribe la barra de direcciones a `/clientes/1` (apartado 5) | Con la recomendada: SPEC-04 2.1 y dos filas en 5.7, con historial, y dos casos en los tests de 5.7 del detalle y del simulador (CA-17) |
| H-02 · Contraste del anillo de foco y del borde de los campos por debajo de 3:1 | media | **Sí.** Reproducidos los cuatro ratios (apartado 2). Está así desde el armazón; el Tech Lead vio las vistas en Chrome y no es algo que se vea a ojo. El anillo naranja es además el que en las capturas parecía un aviso | **Lo decide el Tech Lead, porque es aspecto.** Cambiar dos valores de `src/styles/tokens.css`. Candidatos calculados: para el anillo, `#b45309` (5,02:1 sobre blanco y 4,64:1 sobre el fondo) o el azul de acento `#1d4ed8` (6,70 y 6,20), que sobre el botón principal no se distinguiría del propio botón salvo por los 2 px de separación; para el borde, `#7c8698` (3,67 y 3,39) o `#868e9c` (3,30 y 3,05). Después, generar otra vez las capturas y que el Tech Lead las mire | `tokens.css` (dos líneas) y las doce capturas. Ningún test lo comprueba hoy: si se quiere vigilar, una prueba que calcule el ratio de esos dos colores. SPEC-04 no fija ningún contraste: si pasa a ser regla, una frase en 2.8 |
| H-03 · Título único, foco al navegar y resultado de la búsqueda sin anunciar | baja | **Sí.** Los tres se ven en el código: ninguna ruta declara `title`, `app.html` no tiene enlace de salto ni nada mueve el foco al cambiar de vista, y la región de resultados no es `aria-live` | **Lo decide el Tech Lead: son tres mejoras, no defectos contra la spec, y cada una pide un requisito nuevo.** Por orden de lo que cuesta: (1) un título por ruta («Clientes», «Nuevo cliente», «Detalle del cliente», «Simulador»), con la opción `title` del router; (2) la región de resultados del panel como región viva, para que se anuncie la lista o «No hay clientes que coincidan»; (3) al navegar, llevar el foco al título de la vista. La IA haría (1) y (2) y dejaría (3) para decidirlo viéndolo con un lector de pantalla, que no tiene | SPEC-04 2.1 o 2.8 y requisitos nuevos; `app.routes.ts`, `panel.html` y sus tests, con rojo antes |
| H-04 · Cinco `role="alert"` a la vez en un envío vacío | baja | **Sí.** Cada mensaje de campo es `role="alert"` y además el campo ya lo referencia con `aria-describedby`. 2.7 pide `role="alert"` para «los avisos de error», y la IA lo aplicó también a los mensajes de campo, que la spec no nombra | **Lo decide el Tech Lead.** **Recomendada**: quitar `role="alert"` de los mensajes de campo del alta y del simulador y dejarlo en los avisos generales; el mensaje se sigue leyendo con el campo, por `aria-describedby`, que es lo que E-56 busca al llevar el foco. **Sin comprobar con un lector de pantalla**: en el simulador el foco no se mueve y el mensaje sale mientras se escribe, así que ahí quitarlo puede dejar el error sin anunciar; quizá convenga quitarlo solo en el alta | SPEC-04 2.7 (qué lleva `role="alert"`), `alta.html`, `simulador.html` y los tests que lo afirmen |
| H-05 · Reglas del código que la spec no dice: el `409` y el aviso general de un `422` no llevan «Reintentar»; un `created_at` que no es fecha se muestra tal cual | baja | **Sí en el hecho.** Son reglas que puso la IA en la sesión 07 y no llevó a la spec, como Y-07, Z-01 y AA-05. Matiz sobre 2.7 («todo error ofrece una salida»): la salida existe en los dos casos, «Cancelar» o «Volver al detalle» en el formulario y «Panel» en la cabecera | Escribirlas en SPEC-04 tal como están, con historial: el `409` y el aviso general de un `422` no ofrecen «Reintentar», porque enviar lo mismo no puede salir bien (2.3 y 2.5, y la fila «Error» de la tabla de 2.5 dice «aviso con «Reintentar»» sin esa excepción); y un `created_at` que no se puede leer como fecha se muestra como llega (2.8). **Alternativa** para el `422` de la proyección: darle «Reintentar», que hoy sería repetir una petición que el backend ya rechazó | SPEC-04 2.3, 2.5 y 2.8, con historial. Código, ninguno |
| H-06 · El comentario de `core/limits.ts` es falso, y varios textos repiten la cifra | baja | **Sí.** El comentario dice «los únicos límites del backend que el frontend lleva escritos» y hay siete más en `alta-help.ts` y `simulador-help.ts`. La frase viene de SPEC-04 2.2, que la dice solo del 20 | Corregir el comentario: son los límites del buscador; los de los formularios están junto a su ayuda. Los textos con la cifra, **lo decide el Tech Lead**. **Recomendada**: dejarlos, porque SPEC-04 fija esos textos literalmente y un cambio del límite lo detectan las pruebas de L-09 (mutación M6 de la sesión 08). **Lo que no detecta nada**: que, cambiado el límite a propósito en los dos lados, el texto se quede con la cifra vieja; eso lo ve quien revise. **Alternativa**: componer los tres textos con la constante, como ya hace la ayuda del simulador | Una línea de comentario en `core/limits.ts`; con la alternativa, `panel.html` o su componente y `alta-help.ts` |
| H-07 · La prueba de la fecha del tipo cita E-27 y es E-29 | baja | **Sí. Error de la IA en esta sesión**: copió E-27 de la lista de CA-08 sin leer el requisito. E-29 es el que dice «su fecha tal como la da la API, sin convertirla de zona horaria» | Cambiar la cita en `frontend/e2e/rate-date.spec.ts` (el comentario, en la línea 6, y el título, en la 14; el informe dice 7 y 14). **También está mal en tres mensajes de commit** (`895f55d`, `6123e69` y `409a393`) y en la tabla de pruebas de la bitácora de la sesión 08: los commits no se reescriben; se anota la corrección en la bitácora | `rate-date.spec.ts` (dos líneas) y una nota en la bitácora |
| H-08 · `npx playwright test` sin `--project` reescribe las capturas versionadas | baja | **Sí. Error de la IA en esta sesión.** Reproducido sin ejecutar nada: `npx playwright test --list` enumera 18 pruebas, las 14 de `pruebas` y las 4 de `capturas` | **Recomendada**: sacar las capturas de la configuración por defecto. `playwright.config.ts` se queda solo con las pruebas, y un segundo fichero, `playwright.capturas.config.ts`, que parte del primero, apunta a `e2e/capturas/`; `npm run e2e:capturas` lo usa con `-c`. Así ninguna orden sin opciones escribe fuera de `frontend/`. **Alternativa**: que las capturas se salten si no está puesta una variable de entorno; pide una forma de ponerla que funcione igual en Windows y fuera, que hoy no hay sin otra dependencia | `playwright.config.ts`, un fichero de configuración nuevo, `package.json`, `tsconfig.e2e.json` y una línea de `.claude/rules/frontend.md` |
| H-09 · CA-10: `MetaStore` no tiene test propio del tiempo agotado | baja | **Sí.** Sus seis tests no adelantan el reloj. La espera de 10 s vive en `BackendApi`, que es quien la prueba; `MetaStore` solo guarda lo que `BackendApi` le da | **Lo decide el Tech Lead.** **Recomendada**: añadir el test en `meta-store.spec.ts` (a los 10 s sin respuesta, el almacén queda en error con `timeout`). Nacerá en verde: se demuestra con una mutación. **Alternativa**: precisar CA-10 para que diga que la espera se prueba en el servicio que hace la llamada | `meta-store.spec.ts`, o una frase de CA-10 con historial |
| H-10 · Sin `Content-Security-Policy` | baja | **Sí en el hecho**, y el propio informe dice que la spec no lo exige. Matiz: el proyecto solo se sirve en local con `ng serve`, que inyecta estilos y recarga en caliente; una política en una etiqueta `meta` tendría que admitir eso o rompería el desarrollo. **No comprobado** qué política admite el servidor de desarrollo de Angular 21 | **Lo decide el Tech Lead.** **Recomendada**: no ponerla en el código ahora y dejarla como limitación conocida, con cómo se cerraría en un despliegue: una cabecera del servidor que sirva la compilación, con `connect-src` limitado al backend y a la API de divisas. **Alternativa**: una etiqueta `meta` en `index.html`, probada antes contra `ng serve` y contra las pruebas de Playwright | Con la recomendada: una fila en `limitaciones-conocidas.md` |

## 2. Lo que la IA ha comprobado

Todo en solo lectura; ningún fichero del repositorio ha cambiado por estas
comprobaciones.

| Qué | Cómo | Resultado |
|---|---|---|
| El informe guardado es el del evaluador | Comparación del fichero con el mensaje que consta en el registro del subagente, con un script de solo lectura fuera del repositorio (12:36) | 203 líneas y 20.039 caracteres los dos. **Una línea distinta, la 43** (fila B-01) |
| Qué agente y qué modelo respondió | Fichero de metadatos y registro del subagente | Tipo de agente `evaluador`. Las 130 respuestas del registro llevan el modelo `claude-opus-5-5`, que es lo que dice su cabecera. El fichero de metadatos trae además un campo `pickedEffortModel` con `claude-fable-5-2`; la IA no sabe qué significa |
| Qué ejecutó | Recuento de sus llamadas en el registro | 69 órdenes de terminal y 5 lecturas de fichero. Ninguna herramienta de escritura: no la tiene |
| Estado tras el evaluador | `git status --short`, `netstat` y la carpeta temporal (12:34) | Árbol limpio en `bab2922`; nada escucha en el 8000, el 4200 ni en ningún 80xx; ninguna carpeta `saas-o-matic-e2e-*` |
| H-01 | `DefaultUrlSerializer` de `@angular/router` 21.2.26, con Node | `/clientes/%31` → `1`; `/clientes/1;x=y` → `1`; `/clientes/1%30` → `10`; `/clientes/1%20` → `1` y un espacio; `/clientes/01` → `01` |
| H-01, el backend | Cliente de test de FastAPI con una base temporal fuera del repositorio, borrada después | `/customers/%31` → `200`, el cliente 1; `/customers/1;x=y` → `422`; `/customers/1%20` → `422` |
| H-02 | Fórmula de luminancia relativa de WCAG, con Node | Anillo `#f59e0b`: 2,15 sobre blanco y 1,99 sobre `#f5f6f8`. Borde `#c9ced8`: 1,58 y 1,46. Los cuatro, por debajo de 3 |
| H-03 y H-04 | Lectura de `app.routes.ts`, `app.html`, `panel.html`, `alta.html` y `simulador.html` | Como dice el informe |
| H-05 | Lectura de `alta.ts:54-60` y `core/api-error.ts:117-122` | `retryable: false` en el `409` y en el aviso general de un `422` |
| H-06 | Lectura de `core/limits.ts`, `alta-help.ts` y `simulador-help.ts` | Como dice el informe |
| H-07 | Texto de E-27 y de E-29 en SPEC-04 | E-29 es el de la fecha |
| H-08 | `npx playwright test --list`, que no arranca servidores ni ejecuta pruebas | 18 pruebas en 5 ficheros: 14 de `pruebas` y 4 de `capturas` |
| H-09 | Lista de tests de `meta-store.spec.ts` | Seis, ninguno del tiempo agotado |
| H-10 | Lectura de `src/index.html` | Sin política |

## 3. Cuatro casos más

No son hallazgos del informe: salen de leerlo y de compararlo.

| # | Caso | Qué propone la IA |
|---|---|---|
| B-01 | **El informe guardado no es idéntico al mensaje en un carácter.** En la línea 43, dentro del argumento de `trimSpaces`, el evaluador escribió un espacio de no separación (U+00A0) literal, aunque el encargo le pedía nombrarlos por su código; la herramienta de escritura lo guarda como un espacio corriente (U+0020). El resto de la línea, que lo nombra, está igual | Restaurarlo exige escribir ese carácter con una orden de una línea de Python, que es una excepción a la norma de no escribir contenido desde la terminal. **La IA no la ha usado sin pedirla**: lo decide el Tech Lead. Mientras tanto, la diferencia queda dicha aquí y en la bitácora |
| B-02 | **El resumen del informe dice «54 requisitos» y SPEC-04 tiene 56**; su tabla sí recoge los 56 (E-01 a E-56, con E-12 a E-14 y E-42 y E-43 agrupados) | Ninguna: es un recuento mal hecho en el resumen. El informe no se toca |
| B-03 | **El evaluador no leyó enteros SPEC-01, SPEC-02 y SPEC-03 ni los ADR**, y revisó por muestreo las filas de 5.3 a 5.6 (lo dice él). Sus cuatro «CUMPLE (muestreo)» no son una comprobación fila a fila | Si el Tech Lead quiere esa comprobación, un segundo encargo acotado a CA-04, CA-05, CA-08 y CA-16, fila a fila |
| B-04 | **Del generador de capturas leyó solo las 60 primeras líneas**; lo que escribe y dónde lo dedujo de la línea 13. H-08 lo confirma el listado de Playwright, no esa lectura | Ninguna |

## 4. Decisión del Tech Lead

~~Pendiente. Esta respuesta se entrega en la parada 2 de la sesión 08 sin
aplicar nada.~~

**Decidido el 2026-11-15, a las 13:11, al aprobar la parada 2 de la sesión
08.** El informe no se toca. Los apartados 1 a 3 y el 5 se quedan como se
entregaron; lo que sigue es la decisión y dónde quedó aplicada. Cada
hallazgo, en un commit, con el oráculo con `--e2e` en verde antes.

| # | Decisión del Tech Lead | Commit |
|---|---|---|
| H-01 | La recomendada: no se toca el código. SPEC-04 2.1 dice que el filtro se aplica al segmento ya descodificado por el router, y 5.7 gana dos filas (`%31` y `1;x=y` piden el cliente 1). Los dos casos, en los tests de 5.7 del detalle y del simulador | `35d482a` |
| H-02 | Se corrige. Anillo de foco: el azul de acento, `#1d4ed8`, **no el `#b45309`**, que se parece demasiado al color de error y haría que un campo enfocado pareciera un campo con error. Borde de los campos: `#7c8698`, **en una variable nueva solo para los controles**; las tarjetas, los avisos y la cabecera conservan el suyo. Una frase en SPEC-04 2.8, un criterio nuevo (CA-19) y una prueba de Playwright que lee los colores que pinta el navegador. Capturas regeneradas y una nueva del alta con un campo enfocado | `72f8544` |
| H-03 | **Solo el título por ruta**, con la opción `title` del router y el nombre de la aplicación detrás (requisito nuevo E-57). El anuncio del resultado de la búsqueda y el foco al navegar **no se hacen**: sin lector de pantalla no se pueden comprobar, y un atributo ARIA sin probar puede empeorar lo que hay. Son la limitación conocida L-10 | `8a16e2e` |
| H-04 | **Solo en el alta**: los mensajes de campo dejan de llevar `role="alert"`. En el simulador se quedan, porque ahí el foco no se mueve y el mensaje sale mientras se escribe. SPEC-04 2.7 dice qué lo lleva y qué no. L-10 dice que nada de esto se ha probado con lector de pantalla | `64f5e7b` |
| H-05 | A SPEC-04 tal como está el código: el `409` y el aviso general de un `422` no ofrecen «Reintentar», un `created_at` que no es una fecha se muestra como llega y la fila «Error» de la tabla de 2.5 recoge la excepción | `b33ea2e` |
| H-06 | Se corrige el comentario de `core/limits.ts`. Los textos con la cifra se quedan, y L-09 dice que son tres y que hay que cambiarlos a mano | `04404af` |
| H-07 | Se corrige la cita en `rate-date.spec.ts`. Los commits no se reescriben: nota en la bitácora | `3728349` |
| H-08 | La recomendada: las capturas salen a `playwright.capturas.config.ts` y `npm run e2e:capturas` lo usa con `-c` | `f6d0d04` |
| H-09 | La recomendada: el test del tiempo agotado en `meta-store.spec.ts`, con su mutación | `596f1ec` |
| H-10 | **No se pone política de contenido ahora.** Limitación conocida L-11, con cómo se cerraría en un despliegue | `13351c9` |
| B-01 | **El carácter de la línea 43 no se restaura.** La diferencia ya está dicha aquí y en la bitácora, y la propia línea nombra el U+00A0. No se abre una excepción a la regla de no escribir desde la terminal por un carácter invisible | — |
| B-02 | Nada | — |
| B-03 | **Sí, una segunda evaluación**, con todo lo anterior aplicado: CA-04, CA-05, CA-08 y CA-16 fila a fila, el contrato de SPEC-01 a SPEC-03 contra `core/models.ts` y los cambios de este día. Su informe, en `evaluacion-frontend-02.md` | — |
| B-04 | Nada | — |

Lo que la IA añadió o dejó sin hacer al aplicarlas (precisiones AE-01 en
adelante) está en la bitácora de la sesión 08, apartado 3.

## 5. Lo que esta respuesta no demuestra

- **H-01 en un navegador**: ni el evaluador ni la IA lo han visto. El
  serializador dice qué segmento recibe la aplicación, no qué queda en la
  barra de direcciones ni qué pasa al recargar. La IA no puede arrancar el
  frontend fuera de Playwright y no ha escrito una prueba para verlo, porque
  sería aplicar algo.
- **H-03 y H-04 con un lector de pantalla**: salen de leer el marcado, las
  del evaluador y las de la IA. Las recomendaciones sobre `role="alert"` y
  sobre la región viva son las habituales, no algo probado aquí.
- **H-10**: qué política de contenido admite `ng serve`.
- **Los colores candidatos de H-02** están calculados, no vistos.
- **Que no haya más**: el evaluador trabajó ocho minutos y medio y por
  muestreo en cuatro criterios (B-03). Diez hallazgos bajos y medios no
  demuestran que no quede ninguno alto.
- La IA redactó el encargo del evaluador, incluido el resumen de L-06, L-08
  y L-09; el texto completo consta en el registro del subagente.
