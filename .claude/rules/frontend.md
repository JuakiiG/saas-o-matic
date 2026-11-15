---
paths:
  - "frontend/**"
---

# Frontend (Angular · TypeScript strict · ESLint)

La versión de Angular es la fijada en ADR-001. Se usa la configuración por
defecto del CLI; no se añaden librerías de UI ni de estado sin aprobación.

**Los generadores del CLI se usan para el proyecto (`ng new`) y para los
ficheros de entorno (`ng generate environments`). Los componentes, los
servicios y los pipes se escriben a mano**, con las herramientas de
edición y con el nombre de fichero y de clase que les daría el CLI
(`panel.ts` y `Panel`, `money-pipe.ts` y `MoneyPipe`). *Por qué: el
generador escribe el componente y su test a la vez, y aquí el test va antes
y se ve fallar.*

## Estructura

```
frontend/src/app/
  core/       servicios de API, modelos de la API, interceptores
  features/   una carpeta por vista (búsqueda, cliente, simulador)
  shared/     componentes y pipes de presentación reutilizables
```

- `features/` puede importar de `core/` y `shared/`; nunca al revés, y una
  feature no importa de otra.
- Las rutas de cada feature se cargan de forma diferida.

## Componentes

- Solo componentes **standalone** con `ChangeDetectionStrategy.OnPush`.
- **Estado con signals** (`signal`, `computed`, `input`, `output`). RxJS se
  reserva para flujos asíncronos (peticiones, *debounce*, cancelación) y se
  convierte a signal en el borde del componente.
- Inyección con `inject()`. Control de flujo con `@if`, `@for` y `@switch`.
- **Las plantillas no contienen lógica**: sin cálculos ni llamadas a métodos
  que computen; se enlazan signals o `computed`.
- Un componente o presenta datos o coordina una vista, no las dos cosas. Si la
  plantilla supera unas 30 líneas va en su propio `.html`.

## Datos y lógica

- **El frontend no implementa reglas de negocio** (tramos, impuestos,
  validación fiscal): las pide al backend. Aquí solo hay presentación,
  validación de formato para ayudar al usuario y conversión de divisa para
  mostrar. *Por qué: una sola fuente de verdad (ADR-002).*
- `HttpClient` solo se usa dentro de los servicios de `core/`. Los componentes
  no conocen URLs.
- **Toda llamada remota expone tres estados explícitos: cargando, error y
  datos**, y la interfaz muestra los tres. Un error de red nunca deja la
  pantalla en blanco ni un indicador de carga infinito.
- **Los errores de la API se distinguen por su código estable**
  (`invalid_tax_id_format`), nunca comparando el texto del mensaje. El mensaje del
  backend se puede mostrar tal cual; la lógica solo mira el código.
- Formularios reactivos tipados. Las respuestas de la API tienen su interfaz
  en `core/`; no se usa `any`.
- Los importes llegan del backend **siempre como enteros en céntimos** y se
  formatean con un único pipe; no se hacen operaciones con `number` en coma
  flotante sobre dinero más allá de la conversión de divisa para mostrar,
  que nunca se guarda ni se envía al backend.

## Interfaz

- Textos de la interfaz en español.
- Diseño *mobile-first*; cada vista se comprueba a 375 px y en escritorio.
- HTML semántico, controles con etiqueta y manejables con teclado.

## Tests

- Fichero `<nombre>.spec.ts` junto al fichero que prueba, con el runner que
  trae el CLI.
- `describe('<Unidad>')` e `it('should <resultado> when <condición>')`.
- Las llamadas HTTP se simulan con las utilidades de test de `HttpClient`;
  ningún test sale a la red.
- De cada servicio de API se prueban los tres estados (carga, error, datos).

## Pruebas de principio a fin (`e2e/`)

- Van en `frontend/e2e/`, con Playwright y solo en Chromium, y cada una
  cita su requisito. `npm run e2e` arranca el backend y el frontend
  (`CLAUDE.md`, regla 8) y el oráculo las ejecuta con `--e2e`. Sus tipos
  los comprueba `npm run lint`.
- **Comparten una base de datos por ejecución**, temporal, y van una
  detrás de otra. Cada prueba trae su propio identificador fiscal: uno
  repetido sería un `409`.
- **No se usa `page.route()` ni `context.route()`.** *Por qué: con una ruta
  puesta, Playwright responde él mismo las comprobaciones previas de CORS
  y ninguna llega al backend, que es justo lo que CA-14 comprueba.* La API
  de divisas la responde `e2e/support/fixtures.ts`, de donde las pruebas
  importan `test` y `expect`.
- **Las capturas de CA-15** (`e2e/capturas/`) tienen su propia
  configuración, `playwright.capturas.config.ts`, que parte de la de las
  pruebas, y se generan con `npm run e2e:capturas`. La configuración por
  defecto deja fuera esa carpeta: `npx playwright test` sin opciones solo
  ejecuta las pruebas. El oráculo no ejecuta las capturas. *Por qué:
  llevan la fecha del día y cambiarían los ficheros versionados de
  `04-calidad/capturas/` en cada pasada.*
- **Las capturas no se regeneran sin motivo.** Se generan cuando cambia lo
  que se ve, y entonces van en el commit de ese cambio. *Por qué: entre
  dos pasadas seguidas cambian unos pocos píxeles aunque nada haya
  cambiado; es ruido del dibujado, de 1 o 2 niveles sobre 255, que no se
  ve, pero ensucia el árbol y el historial (sesión 08, AE-12).*
