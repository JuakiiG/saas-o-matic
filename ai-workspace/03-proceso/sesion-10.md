# Sesión 10 · Cierre tras la pasada manual

| | |
|---|---|
| **Fecha** | 2026-11-16 |
| **Participantes** | Tech Lead (persona) · IA: Claude Code, modelo Claude Fable 5.2 |
| **Resultado** | Sesión abierta a las 14:02 |

Esta bitácora la redacta la IA y la revisa el Tech Lead. Se abre al empezar
la sesión y cada revisión se anota en el momento en que ocurre (acuerdo f4 de
la sesión 01).

**La conversación es nueva**, sin el contexto de la sesión 09: la IA llega
con lo que ha leído al empezar (`CLAUDE.md`, los pendientes de la bitácora
de la sesión 09 y `04-calidad/pruebas-manuales.md`, con los resultados del
Tech Lead sin commit) y con sus cuatro notas de memoria, no con lo que hizo
ayer.

## 1. Encargo de la sesión

**Prompt** (resumen fiel):

> Sesión 10: cierre tras la pasada manual. Antes de nada, leer `CLAUDE.md`,
> los pendientes de `03-proceso/sesion-09.md` y
> `04-calidad/pruebas-manuales.md`. Abrir esta bitácora con el mismo
> formato que las anteriores.
>
> Parada 2 de la sesión 09 aprobada. Admitidas AH-01 a AH-06.
>
> El Tech Lead ha ejecutado el guion de pruebas manuales hoy, 16/11, de
> 12:39 a 13:55, sobre `06a6314`, en Chrome 157 y Windows 11, con una base
> de datos nueva. Los 30 pasos, OK. Sus resultados están escritos en
> `pruebas-manuales.md`, sin commit. No cambiar la columna «Resultado» ni
> la tabla de cabecera. Lo que vio, para la bitácora:
>
> - Paso 5: el anillo azul se distingue sobre el botón «Guardar». El
>   pendiente AE-06 de la sesión 08 queda cerrado.
> - Paso 17: con el tipo 1,1054, la base y el impuesto suman 187,26 USD y
>   el total dice 187,25 USD. Es lo esperado.
> - Paso 22: hacen falta las dos pulsaciones y lo ve aceptable. El
>   comportamiento se queda como está.
> - Paso 24: tras abrir `/clientes/%31`, la barra de direcciones queda en
>   `/clientes/1`.
> - Pasos 29 y 30: tras Ctrl+C a mitad de `npm run e2e`, los puertos 8000
>   y 4200 libres, ninguna carpeta temporal y la base de datos sin tocar.
>   El pendiente del Ctrl+C queda cerrado.
>
> Tres cambios, un commit cada uno, con el oráculo en verde por su código
> de salida; con `--e2e` donde se toque `frontend/`.
>
> **1. El guion.** Commit de `pruebas-manuales.md` con los resultados del
> Tech Lead tal como están. Tres retoques de la IA en el texto, sin tocar
> los resultados: la introducción dice «unos 15 minutos» y la pasada llevó
> 75, con pausas: poner una cifra honrada; las órdenes del paso 30 dicen
> que se lanzan desde la raíz del repositorio (la tercera usa una ruta
> relativa y desde `frontend/` falla); y el apartado final dice que la IA
> no lo ha ejecutado en un navegador: sigue siendo cierto, y se añade que
> lo ejecutó el Tech Lead el 16/11, con los 30 pasos en OK.
>
> **2. Los dos «Reintentar» en el detalle y en el simulador.** Añadir los
> tres tests que hoy solo dice la spec (2.1): el cliente en el detalle, el
> cliente en el simulador y la primera proyección en el simulador. Nacen
> en verde: cada uno con su mutación, deshecha y anotada. Si SPEC-04
> necesita una fila en sus tablas para ellos, con historial.
>
> **3. Puesta al día.** Regenerar la matriz de trazabilidad. Corregir las
> cifras de tests en `README.md` y en `ai-workspace/README.md`. En el
> «Estado» de `ai-workspace/README.md`, el guion pasa de pendiente a
> ejecutado, con su fecha y su resultado. La integración continua y el
> clon limpio siguen pendientes.
>
> **Parar ahí (parada 1)** y cerrar la bitácora de la sesión 10: qué
> cambió, qué mutación mató cada test nuevo, cuántos tests hay y qué no se
> ha podido comprobar. La prueba en limpio y el `push` los hace el Tech
> Lead.

## 2. Cronología

Las horas son las del reloj del sistema (`date`) al escribir cada fila; las
de los commits se toman de `git log --format=%ci` después de hacerlos.

| Hora | Commit | Qué |
|---|---|---|
| 14:05 | — | Mensaje recibido a las 14:02 (primera lectura del reloj, 14:02:35). El último commit es `06a6314` (2026-11-15 17:57:50), el último de la sesión 09. **`git status`: un solo fichero cambiado y sin commit, `04-calidad/pruebas-manuales.md`**, con los resultados del Tech Lead; su `git diff` toca las cinco filas de la tabla de cabecera y la columna «Resultado» de los 30 pasos, y nada más (35 líneas). **`netstat` a las 14:02:59: nada escucha en el 8000, el 4200, el 8011 ni el 4211.** `backend/data/saas-o-matic.db`, del Tech Lead: 28.672 bytes, 2026-11-14 18:37; la IA no lo toca. Lecturas del encargo hechas, y además SPEC-04 (2.1, 2.4, 2.5, 5.3, 5.5, 5.6, los criterios y el historial), `detalle.spec.ts`, `simulador.spec.ts`, el test del panel de la sesión 09, `detalle.ts`, `simulador.ts`, `projector.ts`, `meta-gate.ts`, `customer-loader.ts`, `meta-store.ts`, los dos README y la cabecera de `trazabilidad.md`. Apertura de esta bitácora |

## 3. Revisiones y decisiones del Tech Lead

### Decisiones del encargo (14:02)

**Parada 2 de la sesión 09, aprobada. Admitidas AH-01 a AH-06**, sin
comentario. La bitácora de la sesión 09 no se toca: la aprobación queda
anotada aquí.

**El guion de pruebas manuales, ejecutado por el Tech Lead** (lo afirma él;
la IA no estaba): el 16/11/2026, de 12:39 a 13:55, sobre `06a6314`, en
Google Chrome 157 y Windows 11, con una base de datos nueva. **Los 30
pasos, OK.** Lo que vio:

| Paso | Qué vio el Tech Lead | Qué cierra o decide |
|---|---|---|
| 5 | El anillo azul se distingue sobre el botón «Guardar» | **Cerrado el pendiente AE-06 de la sesión 08** |
| 17 | Con el tipo 1,1054, la base y el impuesto suman 187,26 USD y el total dice 187,25 USD | Es lo esperado: el céntimo de SPEC-04, 2.6 y 5.1 |
| 22 | Hacen falta las dos pulsaciones de «Reintentar» | **Lo ve aceptable: el comportamiento se queda como está** |
| 24 | Tras abrir `/clientes/%31`, la barra de direcciones queda en `/clientes/1` | Visto por primera vez en un navegador |
| 29 y 30 | Tras Ctrl+C a mitad de `npm run e2e`: los puertos 8000 y 4200, libres; ninguna carpeta temporal; la base de datos, sin tocar | **Cerrado el pendiente del Ctrl+C de la sesión 08** |

**Reglas de esta sesión**, del encargo:

- **Tres cambios, un commit cada uno**, con el oráculo en verde por su
  código de salida; con `--e2e` donde se toque `frontend/`.
- **La columna «Resultado» y la tabla de cabecera del guion no se tocan.**
- **La prueba en limpio y el `push` son del Tech Lead.**

## 4. Comprobaciones hechas en la sesión

| Qué | Cómo | Resultado |
|---|---|---|
| Estado del repo al empezar | `git status --short` y `git log -1` (14:02:35) | `06a6314`; cambiado y sin commit, solo `04-calidad/pruebas-manuales.md` |
| Qué cambia en el guion sin commit | `git diff` del fichero (14:02:59) | 35 líneas: las cinco filas de la tabla de cabecera y las 30 filas de pasos, en las que solo cambia la última celda |
| Puertos al empezar | `netstat -ano` filtrado por `LISTENING` y los puertos 8000, 4200, 8011 y 4211 (14:02:59) | Ninguno en escucha |
| La base local del Tech Lead | Listado de `backend/data/` (14:02:59) | 28.672 bytes, 2026-11-14 18:37 |

## 5. No verificado

Se rellena al llegar a la parada.

## 6. Tareas pendientes

| Tarea | Cuándo |
|---|---|
| Cambio 1: el guion, con los resultados del Tech Lead y tres retoques | Ahora |
| Cambio 2: tres tests de los dos «Reintentar», en el detalle y en el simulador, con su mutación | Después |
| Cambio 3: la matriz, las cifras de tests y el «Estado» | Después |
| Parada 1 y cierre de esta bitácora | Al acabar |
