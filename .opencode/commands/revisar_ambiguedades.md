---
description: Busca ambigüedades y contradicciones en los .md de la estructura de trabajo con IA/agentes y propone 2 opciones por hallazgo
agent: build
---
Revisa la coherencia de la estructura de trabajo con IA de este repo. Enfoque opcional: $ARGUMENTS

## Fuentes (léelas todas)

- `AGENTS.md`, `MEMORY.md`, `docs/constitution.md`
- `.opencode/agents/*.md` (coordinator, planner, implementer, reviewer)
- `.opencode/commands/*.md`
- `README.md`, `CONTRIBUTING.md`, `models/README.md` (solo sección de reglas)

## Regla de verdad

El código manda sobre los documentos. Antes de marcar una contradicción, verifica el
comportamiento real leyendo el archivo implicado (`main.py`, `src/...`) o comprobando que
el path/herramienta existe (`Get-ChildItem`, grep). No corrijas nada por prosa en contra
del código; propón arreglar el código como una de las opciones.

## Qué buscar (checklist)

1. **Contradicción entre archivos**: la misma regla dicha de dos formas incompatibles
   (p. ej. "X es el único que hace Y" vs "X y Z hacen Y").
2. **Doc vs código**: comandos, argumentos, flags o flujos que el README/AGENTS promete
   pero el código no respeta (o al revés).
3. **Referencias fantasma**: skills, comandos `/...`, MCPs, agentes o ficheros citados
   que no existen en el repo.
4. **Stack ajeno**: herramientas de otro ecosistema (p. ej. `node --test` en este repo
   Python) o dependencias que no están en `requirements.txt` presentadas como actuales.
5. **Ambigüedad de términos**: palabra con dos significados posibles en la misma capa
   (p. ej. "interfaces" = UI `console`/`server` vs contratos `abc.ABC`).
6. **Propiedad compartida**: dos agentes/personas responsables de actualizar el mismo
   archivo (p. ej. `MEMORY.md`).
7. **Erratas verificables**: fechas imposibles, rutas rotas (`@fichero` que no existe),
   enlaces a ficheros renombrados.

## Proceso

1. Lee las fuentes y el código implicado; lista solo hallazgos **verificados**.
2. Si no hay hallazgos, di "SIN HALLAZGOS" y termina.
3. Si hay hallazgos, presenta **una sola tanda de preguntas** con el formato:
   `archivo:línea — qué dice A vs qué dice B — ¿cuál de las 2 opciones?`
   (cada hallazgo con exactamente 2 opciones; si una opción es "corregir el código",
   dilo explícitamente).
4. Aplica SOLO lo que el usuario elija: edición quirúrgica en el archivo afectado.
5. Mantén MEMORY.md sincronizada (las correcciones relevantes se reflejan ahí; los
   cambios de código, en "Hecho" con fecha).
6. **Verificación final**: grep por todos los patrones del problema resuelto sobre
   `**/*.md`; cero coincidencias = correcto. Informa en una tabla: hallazgo → decisión →
   dónde se aplicó.
