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
