# Conversaciones con la IA

Las conversaciones de la sesión de Claude Code que implementa, exportadas
con `/export`: lo que el Tech Lead escribió, lo que la IA respondió y lo que
ejecutó, en bruto. La bitácora de cada sesión es su resumen, con las
decisiones; esto es lo que hay debajo.

## Los ficheros

Uno por sesión, de la 01 a la 12:

| Fichero | Líneas | Sesión y bitácora | Fecha |
|---|---|---|---|
| [`sesion-01.txt`](sesion-01.txt) | 2.566 | [Sesión 01](../sesion-01.md) · Arranque, análisis, SPEC-02 y ADR | 2026-11-12 |
| [`sesion-02.txt`](sesion-02.txt) | 4.109 | [Sesión 02](../sesion-02.md) · SPEC-01 | 2026-11-12 |
| [`sesion-03.txt`](sesion-03.txt) | 6.015 | [Sesión 03](../sesion-03.md) · Segunda evaluación de las specs | 2026-11-12 |
| [`sesion-04.txt`](sesion-04.txt) | 17.455 | [Sesión 04](../sesion-04.md) · Aprobación del bloque backend y backend | 2026-11-13 |
| [`sesion-05.txt`](sesion-05.txt) | 5.839 | [Sesión 05](../sesion-05.md) · Correcciones de la evaluación del backend | 2026-11-13 |
| [`sesion-06-07.txt`](sesion-06-07.txt) | 15.899 | [Sesión 06](../sesion-06.md) · SPEC-04 al día, y [Sesión 07](../sesion-07.md) · Frontend | 2026-11-14 |
| [`sesion-08.txt`](sesion-08.txt) | 13.478 | [Sesión 08](../sesion-08.md) · QA del frontend | 2026-11-15 |
| [`sesion-09.txt`](sesion-09.txt) | 4.427 | [Sesión 09](../sesion-09.md) · Documentación de entrega e integración continua | 2026-11-15 |
| [`sesion-10.txt`](sesion-10.txt) | 1.437 | [Sesión 10](../sesion-10.md) · Cierre tras la pasada manual | 2026-11-16 |
| [`sesion-11.txt`](sesion-11.txt) | 1.379 | [Sesión 11](../sesion-11.md) · Las conversaciones publicadas y la nota de método | 2026-11-16 |
| [`sesion-12.txt`](sesion-12.txt) | 1.394 | [Sesión 12](../sesion-12.md) · La nota de método corregida y las conversaciones sin rutas de usuario ni correo | 2026-11-16 |

Lo que falta:

- **El principio de la sesión 06.** La 06 y la 07 comparten conversación y
  fichero, que empieza a mitad de la 06 (14/11, hacia las 10:47): la
  conversación se había compactado y lo anterior no se pudo exportar. Lo
  que falta está en la [bitácora de la sesión 06](../sesion-06.md).
- **La sesión 13**, la que publica la conversación de la 12: no puede
  exportarse a sí misma antes de acabar. Su bitácora es
  [`sesion-13.md`](../sesion-13.md).

## Cómo leerlas

Cada intervención del Tech Lead empieza con «❯». Con buscar ese carácter
se recorren los prompts de una sesión.

Lo que se ve y conviene saber:

- Las líneas **«※ recap»** son resúmenes de la herramienta.
- Los comentarios **«buddy»** son de un complemento de la barra de estado.
- Las rutas de **`.private/`** son material privado del Tech Lead, que no
  se publica.
- Los ficheros son largos porque incluyen las salidas de las herramientas.

## Qué se ha cambiado al publicarlas

- Los finales de línea.
- Los espacios al final de cada línea.
- En la 03, dos líneas que listaban otra sesión abierta en el equipo, ajena
  al proyecto, sustituidas por una marca.
- La carpeta de usuario de las rutas locales del equipo, sustituida por
  `<usuario>`: 19 veces, en las sesiones 05, 06-07, 08 y 09, y 3 en la 11.
- El correo `noreply` del autor de los commits, sustituido por una marca:
  7 veces, en la 01.

Nada más: el contenido de la interacción no se ha tocado.

La primera versión publicada, la del commit `4655810`, todavía llevaba esas
rutas y ese correo.
