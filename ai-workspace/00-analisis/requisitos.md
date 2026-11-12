# Requisitos

- **Fecha**: 2026-11-12
- **Estado**: `aprobado` por el Tech Lead el 2026-11-12
- **Qué es**: nuestra lectura del encargo, descompuesta en requisitos
  numerados para poder seguir cada uno hasta su spec, su test y su commit.
  No reproduce el texto original.

## El encargo en una frase

Una herramienta interna con la que un equipo comercial da de alta clientes
corporativos, simula el coste mensual de una suscripción SaaS según el número
de usuarios y lo consulta en varias divisas. Son dos piezas separadas, una
interfaz web y una API con base de datos, que se comunican entre sí.

## Requisitos funcionales

| Id | Requisito | Spec | Supuestos |
|---|---|---|---|
| R-01 | El sistema consta de un frontend interactivo y un backend con base de datos, separados y comunicados entre sí | Todas · ADR-001 | — |
| R-02 | El backend usa una tecnología de las preferidas (Node.js con TypeScript o Python) y **SQLite** como base de datos | ADR-001 | — |
| R-03 | `POST /customers` registra un cliente corporativo con nombre de empresa, identificador fiscal, email de contacto, país y plan | SPEC-01 | A2, A12 |
| R-04 | El identificador fiscal se valida de forma estricta. Si el país es España, se comprueba con el algoritmo oficial de control que el DNI/NIF/CIF es correcto | SPEC-01 | A10, A11 |
| R-05 | `POST /simulations` registra una simulación de consumo de un cliente (cliente, usuarios activos, almacenamiento contratado y llamadas a la API estimadas) y **persiste el cálculo** | SPEC-03 | A3, A7 |
| R-06 | El coste base mensual se calcula con una tarifa **acumulativa por tramos**: hasta 10 usuarios a 10 €, del 11 al 50 a 8 € y a partir del 51 a 5 €. Cada usuario se cobra al precio de su tramo (15 usuarios = 140 €) | SPEC-02 | A6, A7 |
| R-07 | Al coste base se le suma el impuesto que corresponde al país del cliente | SPEC-02 | A4, A5, A6 |
| R-08 | El frontend usa un framework de libre elección | ADR-001 | — |
| R-09 | La interfaz obtiene tipos de cambio de una API pública y permite cambiar la divisa de visualización (EUR, USD, GBP…), mostrando los costes convertidos al momento | SPEC-04 | A8 |
| R-10 | Vista de panel con un buscador de clientes por nombre de empresa o por identificador fiscal | SPEC-04 · SPEC-01 | A13 |
| R-11 | Vista de detalle con tarjetas *responsive* que muestran los datos del cliente y el historial de sus simulaciones guardadas | SPEC-04 · SPEC-03 · SPEC-01 | A13 |
| R-12 | Formulario de simulación con un *slider* o control equivalente para el número de usuarios, que muestra en tiempo real la factura mensual prevista según los tramos y en la divisa elegida | SPEC-04 · SPEC-02 | A9 |

**Sobre R-04 y el «algoritmo oficial»**: la letra del DNI y del NIE sigue
el cálculo que publica el Ministerio del Interior. Para el carácter de
control del CIF no se ha localizado una fuente oficial que lo describa: la
Orden EHA/451/2008 y la Agencia Tributaria fijan la estructura y las letras
de entidad, pero no el cálculo. SPEC-01 se apoya en la convención de uso
común, no en un texto oficial. Esa convención **se contrastará** con una
implementación independiente mediante una prueba diferencial (SPEC-01,
CA-19). **Hoy no está contrastada**: la prueba no existe todavía y la
biblioteca con la que se compara no se ha instalado.

## Requisitos de calidad

| Id | Requisito | Dónde se comprueba |
|---|---|---|
| R-17 | El frontend gestiona de forma visible los estados de carga y de error, en especial al consumir la API externa de divisas | SPEC-04 |
| — | Backend robusto: validaciones correctas, cálculo exacto de los tramos y persistencia limpia | SPEC-01, SPEC-02, SPEC-03 |
| — | Interfaz fluida y *responsive* | SPEC-04 |

Los dos últimos no llevan identificador propio porque son la forma en que se
juzgan R-03 a R-12, no funcionalidad adicional.

## Entregables

| Id | Entregable | Dónde |
|---|---|---|
| R-13 | Repositorio con el código y una carpeta de trabajo con la IA en la raíz, de estructura libre | `ai-workspace/` |
| R-14 | Especificaciones, contratos de API y validaciones definidos **antes** de programar, con los planes y prompts con que se guio a la IA | `00-analisis/`, `01-specs/` |
| R-15 | Diseño de la base de datos, organización de carpetas y directrices dadas a la IA para obtener código limpio y modular, sin ficheros enormes | `02-arquitectura/`, `CLAUDE.md`, `.claude/` |
| R-16 | Evidencia de la interacción real con la IA: prompts clave, hilos o notas tomadas sobre la marcha | `03-proceso/` |
| R-18 | README con pasos claros para levantar backend y frontend en local | `README.md` |
| R-19 | Entrega dentro de plazo por el canal indicado | A1, A15 |

## Cómo se valora

| Criterio | Peso | Requisitos que lo sostienen |
|---|---|---|
| Planificación y diseño | 35 % | R-14, R-15 |
| Calidad del software | 30 % | R-03 a R-12, R-17 |
| Criterio técnico y control de calidad | 25 % | R-16 y la carpeta `04-calidad/` |
| README y despliegue en local | 10 % | R-18 |

El 60 % depende del proceso y no del código. Por eso las specs se aprueban
antes de programar y la bitácora se escribe en el momento.

## Lo que el encargo no pide

Se deja fuera de forma deliberada, para no añadir alcance que nadie ha pedido:

- Despliegue en la nube o infraestructura como código. Solo se pide ejecución
  en local.
- Otra base de datos distinta de SQLite.
- Precio para el almacenamiento o las llamadas a la API (ver A3).
- Edición o borrado de clientes y simulaciones (ver A18).
- Autenticación de usuarios (ver A16).

## Observaciones de la lectura

Puntos donde el encargo deja margen o donde una lectura rápida lleva a error.
Cada uno se resuelve en [`supuestos.md`](supuestos.md).

1. **Tarifa acumulativa, no por volumen.** Con 15 usuarios no se cobran los 15
   a 8 €: se cobran 10 a 10 € y 5 a 8 €. El ejemplo de 140 € es el caso de
   prueba que lo fija.
2. **«DNI/NIF/CIF» son tres formatos con algoritmos distintos**, y el NIF de
   personas físicas incluye también el NIE de extranjeros. Validar solo el
   DNI dejaría sin cubrir justo el caso más habitual en clientes
   corporativos, el CIF.
3. **El impuesto depende del país, pero no se dan los tipos** ni la lista de
   países.
4. **El plan se registra, pero no se define** ni se dice si afecta al precio.
5. **Almacenamiento y llamadas a la API se registran, pero no tienen tarifa.**
6. **Faltan endpoints de lectura.** Solo se nombran dos `POST`, pero el
   buscador y el historial necesitan consultas.
7. **No hay una vista de alta de cliente entre las obligatorias**, aunque
   existe el endpoint. Sin ella, la validación fiscal no se puede probar desde
   la interfaz (ver A17).
8. **«Tiempo real» aparece dos veces con significado distinto**: en la
   conversión de divisa y en la proyección del *slider*. La primera es
   presentación; la segunda es regla de negocio.
9. **El encargo dice que es la interfaz la que conecta con la API de
   divisas.** Condiciona si esa llamada puede pasar por el backend (ver A8).
