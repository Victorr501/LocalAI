# AGENTS.md — LocalAI

Agente IA 100% local (llama.cpp + CUDA) con Clean Architecture. En desarrollo temprano: verifica el código antes de confiar en README/docs.

## Comandos

- Usa el Python del venv (`.\venv\Scripts\python.exe` o venv activado): el `python` del sistema no tiene las dependencias.
- Arranque: `python main.py` (menús interactivos) o `python main.py -a 1|2 -m <modelo.gguf>` (con args válidos no pregunta por consola).
- `-a` solo acepta `1` (CLI) o `2` (servidor); valor ausente o inválido → menú interactivo. `-m` solo se salta su menú si el `.gguf` existe en `models/`.
- Requisitos para arrancar: `docker-compose up -d` (MongoDB), `.env` válido (ver `.example.env`: `MONGO_URI`, `MONGO_DB_NAME`, `MODEL_PATH`, `APP_MODE`) y al menos un `.gguf` en `models/` (si no, `sys.exit(1)`).
- No hay ningún runner de tests, linter, typecheck ni CI. La librería de tests está **por decidir** (constitución, principio 5): no instales ninguna ni inventes comandos de verificación; la estrategia la define el plan de cada spec.
- `pip install -r requirements.txt` reinstala `llama_cpp_python` **sin GPU**. Tras cada instalación, recompilar en PowerShell:
  `$env:CMAKE_ARGS="-DGGML_CUDA=on"; pip install --force-reinstall --no-cache-dir llama-cpp-python` (5-15 min).

## Arquitectura (reglas estrictas)

- `main.py` es el único orquestador: carga `.env`, conecta BD, instancia `AIEngine` y lo inyecta en la interfaz. No duplicar esa carga.
- Dirección de dependencias: `console`/`server` → `services` → `repository`/`engine`.
- `commands/` (CLI) y `controllers/` (server) son la capa controladora: capturan excepciones y controlan lo que entra y sale del flujo; nunca contienen lógica de negocio.
- `services` (lógica) y `repository` (datos) se comunican mediante contratos `abc.ABC`; las capas superiores dependen de abstracciones, no de implementaciones.
- Conexión a MongoDB en `src/config/database.py`; `repository` es el único que lee o escribe datos. `pymongo` solo en esas dos capas.
- Todo modelo de datos (DTOs, entidades, esquemas) vive en `src/models/`, separando request/response de schemas de BD.

## Estado real del código (no todo lo que dice el README existe)

- Stub vacíos: `src/console/cli.py`, `src/server/api.py` (solo `pass`). `src/repository/`, `src/services/`, `src/models/`, `src/tests/` contienen solo `__init__.py`.
- FastAPI/uvicorn **no** están en `requirements.txt`; el "modo servidor" aún no usa red.
- `src/engine/engine.py` hardcodea el template de chat Llama-3 (`<|start_header_id|>...`). Cambiar si se usa otro modelo.
- `load_dotenv()` se llama en varios módulos; `main.py` sobrescribe `MODEL_PATH` en `os.environ` (no usar `load_dotenv(override=True)`).

## Workflows de agentes (`.opencode/agents/`)

- Subagentes SDD: `planner` → `implementer` → `reviewer` + `coordinator`. Specs en `specs/NNN-nombre/{spec,plan,tasks}.md`; reglas en `docs/constitution.md`.
- Cada spec define su verificación en `plan.md` (tests en `src/tests/`, sin instalar dependencias). Cualquier sesión actualiza `MEMORY.md` cuando algo importante cambie; al cerrar una spec el obligado es el `coordinator` (y también con `specs/NNN-nombre/tasks.md`). Herramienta: `/actualizar_memory`.
- Comandos: `/revisar_ambiguedades` (coherencia de los .md de esta estructura) y `/actualizar_memory`.

## Repo

- `venv/`, `.env`, `models/*` (salvo `models/README.md`) están en `.gitignore`: nunca commitear.
- Código y comentarios en español; docs `README.md`/`CONTRIBUTING.md` bilingües (secciones EN + ES, mantener ambas).

## Memory

- En el archivo `MEMORY.md` se guardara todo el progreso del proyecto para que lo puedas leer y poder actualizar cuando hayas hecho algun punto importante nuevo
