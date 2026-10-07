# Constitución de LocalAI

1. **Stack mínimo.** No se instalan librerías nuevas si `requirements.txt` ya cubre ese uso; toda dependencia nueva requiere aprobación explícita.
2. **Spec antes que código.** Todo cambio nace en `specs/NNN-nombre/` (spec → plan → tasks); código sin spec = tarea no hecha. Excepción: cambios pequeños de un solo archivo que no toquen arquitectura, con aprobación explícita del usuario.
3. **Lógica, interfaz y datos.** `console`/`server` solo contienen `commands/` y `controllers/`: capturan excepciones y controlan lo que entra y sale del flujo, sin lógica. La lógica vive en `services` y los datos en `repository`; ambos se comunican por interfaces (`abc.ABC`). La conexión a MongoDB la hace `src/config/database.py`; `repository` es el único que lee o escribe datos.
4. **Datos en models.** Los objetos de datos van en `src/models/` por archivo según su uso: `<nombre_dato>_DTOs.py` (entrada/salida) y `<nombre_dato>_entidades.py` (persistencia).
5. **Tests.** Viven en `src/tests/`; su librería se elegirá cuando se llegue a ese punto (hoy no hay ninguna instalada); nada se da por hecho en rojo.
6. **Datos e idioma.** Procesamiento 100% local (cero APIs externas/telemetría); `.env`, `models/*` e historiales nunca se commitean. Código y textos en español; comentarios siempre estilo docstring, sin emojis, lo más cortos posibles e indicando qué entra y qué devuelve; README/CONTRIBUTING en EN + ES.
