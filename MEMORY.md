# MEMORY.md — Progreso de LocalAI

Memoria del proyecto para que cualquier agente (futuras sesiones de OpenCode) pueda leer el estado real sin reexplorar todo. Actualiza este archivo cuando termines algo importante (ver "Cómo actualizar" al final).

> Última actualización: 2026-10-07 (sesión de OpenCode, rama `10-implementar-de-nuevo-los-agentes-de-ia-para-claude-code`)

## Estado general

Proyecto en **fase temprana**: el esqueleto de arranque funciona (menús + motor + BD), pero las capas de negocio e interfaz están casi vacías. No hay tests, linter ni CI.

## ✅ Hecho y verificado en el código

- **Orquestación (`main.py`)**: carga `.env`, menús interactivos de modo y modelo, conexión a MongoDB (`Database.connect/init_db`), instancia `AIEngine` y arranca CLI o servidor. Manejo de modelo inexistente con menú de seguridad.
- **Config (`src/config/`)**: `logger.py` con formato según `APP_MODE` (console = print plano, server = con fecha/nivel); `database.py` con conexión pymongo, timeout 5s, colección `chat_history` inicializada con un documento semilla.
- **Motor (`src/engine/engine.py`)**: carga `.gguf` en VRAM (`n_gpu_layers=-1`, `n_ctx=4096`) e inferencia con `max_tokens=512`, `temperature=0.7`. Prompt con template hardcodeado de Llama-3.
- **Infra**: `docker-compose.yml` (MongoDB en 27017, volumen `D:\BasesDeDatos\LocalAI_Mongo`), `.example.env`, `requirements.txt` pinneado, modelo `Meta-Llama-3-8B-Instruct-Q4_K_M.gguf` en `models/`.
- **Docs**: `README.md` y `CONTRIBUTING.md` bilingües (EN + ES), `AGENTS.md` para agentes, `.opencode/agents/` con 4 subagentes SDD (planner, implementer, reviewer, coordinator).
- **Tooling de agentes**: `opencode.json` con MCP `chrome-devtools` y `context7` (la API key de context7 es un placeholder `<TU APIKEY DE CONTEXT7>`; falta poner la real).
- **Args de terminal**: `-a 1|2` y `-m <modelo>` se respetan sin pasar por menús (arreglado 2026-10-07 en `menu_modo_arranque`); sin args o con valor inválido cae al menú interactivo.
- **`docs/constitution.md`**: ✅ escrita y revisada (6 principios, aprobados 2026-10-07): stack mínimo; spec antes que código (excepción para cambios pequeños de 1 archivo con aprobación); `commands/`/`controllers/` como capa controladora con lógica en `services` y datos en `repository` (conexión en `config/database.py`); datos en `models/` (`_DTOs`/`_entidades`); tests en `src/tests/` (librería por decidir); datos locales + docstrings en español.

## ❌ Pendiente / no existe aún

- **`src/console/cli.py`**: solo `def iniciar_terminal(...): pass` → el chat por terminal **no funciona**.
- **`src/server/api.py`**: solo `pass` → el modo servidor **no funciona**. FastAPI/uvicorn **no están** en `requirements.txt` (el README los menciona como futuro).
- **Capas vacías** (solo `__init__.py`): `src/services/`, `src/repository/`, `src/models/`, `src/console/commands/`, `src/server/controllers/`.
- **Tests**: `src/tests/` vacío; no hay pytest, runner, linter, typecheck ni CI. Librería de tests **por decidir** (constitución #5): los agentes SDD verifican según lo que defina el `plan.md` de cada spec, sin instalar dependencias.
- **`specs/`**: carpeta vacía; ningún workflow SDD ejecutado aún.
- **Function calling / memoria a largo plazo real / streaming**: mencionados en la visión del proyecto, no implementados (solo se guarda/lee `chat_history` básico).

## ⚠️ Gotchas para futuras sesiones

- `pip install -r requirements.txt` reinstala `llama-cpp-python` **sin GPU**. Requiere recompilar siempre:
  `$env:CMAKE_ARGS="-DGGML_CUDA=on"; pip install --force-reinstall --no-cache-dir llama-cpp-python` (5-15 min).
- Con args válidos (`python main.py -a 1 -m X.gguf`) no hay menús; sin args o con valor inválido siempre pasa por `input()`. Para scripts/verificación no bloquea: pasar ambos args con el modelo existente.
- Arranque mínimo probado: `docker-compose up -d` → `.env` válido → `.gguf` en `models/` → `python main.py`.
- `load_dotenv()` se llama en varios módulos; `main.py` sobrescribe `MODEL_PATH` en `os.environ`. No usar `load_dotenv(override=True)`.
- Staged/Working tree pendiente de commit: `AGENTS.md`, `MEMORY.md` y `main.py` (arreglo de args) modificados; renombrado `LICENSE` → `LICENSE.md` y borrado `README.es.md`; sin trackear: `.opencode/`, `docs/`, `opencode.json`.

## Cómo actualizar este archivo

1. Al terminar una tarea relevante, mueve su punto de "Pendiente" a "Hecho" (con fecha si aporta contexto).
2. Mantén las secciones: Estado general / Hecho / Pendiente / Gotchas.
3. Borra lo que deje de ser cierto; este archivo solo es valioso si refleja el código real.
4. Solo el `coordinator` actualiza este archivo al cerrar una spec (y entonces también `specs/NNN-nombre/tasks.md`); los demás agentes no lo tocan.
