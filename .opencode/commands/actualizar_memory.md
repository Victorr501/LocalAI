---
description: Actualiza MEMORY.md de forma verificada: incorpora progreso nuevo, mueve puntos a Hecho y deja al día el estado real del proyecto
agent: build
---
Actualiza `MEMORY.md` con el progreso del proyecto. Puntos a incorporar: $ARGUMENTS

## Fuentes

- `MEMORY.md` (estructura propia y reglas de su sección "Cómo actualizar")
- `AGENTS.md` y `docs/constitution.md` (reglas de trabajo del repo)
- El código implicado (`main.py`, `src/...`) y `git status`/`git diff` como prueba

## Reglas

1. **Nada sin verificar**: cada punto nuevo se confirma en el código (o en git) antes de
   escribirlo. Si no puedes verificarlo, márcalo como "(sin verificar)" o PARA y pregunta.
2. **No borres sin aprobación**: ningún punto existente se elimina ni se reescribe de
   forma sustancial sin preguntarme antes. Sí puedes moverlo entre secciones.
3. **Mueve, no dupliques**: lo que estaba en "❌ Pendiente" y ya es real pasa a "✅ Hecho"
   con la fecha de hoy; se elimina el original para no duplicar.
4. **Secciones fijas**: Estado general / ✅ Hecho / ❌ Pendiente / ⚠️ Gotchas / Cómo
   actualizar. No crees secciones nuevas ni reordenes las existentes.
5. **Cabecera al día**: actualiza la línea `> Última actualización:` con la fecha
   (`YYYY-MM-DD`) y la rama/sesión si aporta contexto.
6. **Estado general**: reescribe la frase superior si el estado real del proyecto cambió
   (sigue diciendo la fase, si hay tests/lint/CI, etc.).
7. **Gotchas verificadas**: solo hechos reproducibles — comandos ejecutados o trampas
   observadas en el código. Nunca gotchas por deducción sin probar.
8. **Consistencia**: no contradigas `AGENTS.md` ni la constitución. Si MEMORY.md y otra
   regla se contradicen, PARA y pregúntame cuál manda antes de escribir.
9. **Contexto SDD**: si esto es el cierre de una spec, ese paso le corresponde al
   `coordinator` (y entonces debe actualizar también `specs/NNN-nombre/tasks.md`);
   infórmalo si no estás actuando como coordinator.
10. **Calidad del texto**: español, sin emojis fuera de los marcadores de sección, y sin
    puntos vagos ("mejorar X") — cada punto dice qué está o qué falta, y dónde se
    verifica.

## Proceso

1. Lee `MEMORY.md`, `AGENTS.md` y `docs/constitution.md`.
2. Si no hay puntos en `$ARGUMENTS`: solo revisa Pendiente→Hecho y el Estado general
   (modo mantenimiento). Si los hay: verifica cada uno en código/git y luego aplícalos.
3. Edita `MEMORY.md` de forma quirúrgica (usa edición por búsqueda, no reescribas el
   archivo entero).
4. Responde con un informe: **añadidos** / **movidos a Hecho** / **borrados (pendientes
   de tu aprobación)** / **dudas que dejé sin tocar**.
