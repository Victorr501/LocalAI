# AI_RULES - Arquitectura y Reglas del Proyecto LocalAI

Este documento define la estructura del proyecto bajo los principios de **Clean Architecture**[cite: 21]. Cualquier agente de IA (OpenCode, Claude, Cursor) o desarrollador que interactúe con este repositorio debe respetar estrictamente la siguiente separación de responsabilidades para mantener el código escalable y modular.

## Propósito de la Aplicación

LocalAI es un **agente inteligente autónomo y soberano**, diseñado para ejecutarse 100% en local (Edge AI)[cite: 21]. Su objetivo es proporcionar un asistente de IA privado, de baja latencia y sin costes de API, aprovechando la aceleración por hardware (NVIDIA GPU)[cite: 21]. El proyecto evolucionará desde un chat de terminal reactivo hacia un agente autónomo con memoria a largo plazo (vía MongoDB) y capacidades de *Function Calling* para interactuar con el sistema operativo y nubes privadas[cite: 21].

## Stack Tecnológico Principal

*   **Lenguaje:** Python 3.12 (o superior)[cite: 21]
*   **Inferencia AI:** `llama-cpp-python==0.3.35` (compilado con soporte CUDA `-DGGML_CUDA=on` para NVIDIA VRAM)
*   **Modelos:** Archivos `.gguf` (ej. Llama 3, Mistral cuantizados)[cite: 21]
*   **Base de Datos (Memoria):** MongoDB (Driver: `pymongo==4.18.2`)[cite: 21]
*   **API / Servidor:** `FastAPI` (Mantenido para el futuro desarrollo web)
*   **Gestión de Entorno:** `python-dotenv==1.2.3`[cite: 21]
*   **Compilación y Rendimiento:** `cmake==4.4.3`, `ninja==1.13.2`, `numpy==2.5.3`
*   **Caché y Estructuras:** `diskcache==5.6.3`, `typing_extensions==4.16.0`
*   **Plantillas (Futuro soporte web/prompts):** `Jinja2==3.1.6`, `MarkupSafe==3.0.3`
*   **Red (Opcional/Soporte):** `dnspython==2.8.0
*   **Interfaz de termianl:** `textual==8.2.8` 

## Mapa del Proyecto

La estructura principal se divide de la siguiente manera basándose en el árbol del directorio[cite: 20]:

*   **`models/` (Raíz):** Directorio exclusivo para almacenar los archivos binarios pesados de los modelos de IA (formato `.gguf`).
*   **`main.py`:** Orquestador principal. Su única responsabilidad es arrancar la base de datos, cargar el modelo en la VRAM y delegar el control a la interfaz seleccionada (Terminal o Servidor)[cite: 21].

### Capas Internas (`src/`)
Todo el código lógico reside dentro de `src/`[cite: 20], dividido en capas estrictas:

*   **`src/config/`**: Configuración global del sistema. Contiene la inicialización del *logger* y la lectura de variables de entorno (del archivo `.env`)[cite: 20, 21].
*   **`src/engine/`**: Cerebro del sistema. Contiene la lógica de inferencia, la optimización de hardware (NVIDIA CUDA / VRAM) mediante `llama-cpp-python` y la gestión interna del Agente[cite: 21]. No debe contener lógica de base de datos ni de interfaces.
*   **`src/repository/`**: Capa de persistencia. Único lugar autorizado para ejecutar consultas directas y gestionar la conexión con MongoDB (historiales, sesiones, etc.)[cite: 20, 21].
*   **`src/services/`**: Lógica de negocio (Puente). Consume el `repository` y el `engine` para crear flujos de trabajo (ej. guardar un mensaje, generar respuesta, guardar respuesta)[cite: 20, 21]. **Esta capa es agnóstica a la interfaz y se comparte entre el CLI y la API**[cite: 21].
*   **`src/models/`**: Definición de esquemas de datos, entidades y modelos de dominio (por ejemplo, clases de Pydantic o estructuras de datos internas)[cite: 20].
*   **`src/console/`**: Interfaz de línea de comandos (CLI). Contiene la lógica visual de la terminal (`cli.py`) y sus comandos (`commands/`)[cite: 20, 21]. Consume los métodos de `src/services/`.
*   **`src/server/`**: Interfaz web/API (FastAPI). Contiene el archivo de arranque (`api.py`) y los controladores (`controllers/`) que exponen el motor a la red[cite: 20, 21]. Consume los métodos de `src/services/`.
*   **`src/tests/`**: Directorio dedicado a las pruebas unitarias y de integración del código[cite: 20].

## Reglas Estrictas de Desarrollo (Inyección de Dependencias)

1.  **Cero lógica de negocio en los controladores:** Los archivos dentro de `src/console/` y `src/server/` solo manejan entradas y salidas (imprimir en pantalla o devolver JSONs). Toda la lógica compleja vive en `src/services/`.
2.  **Unidireccionalidad:** Las interfaces (`console`, `server`) pueden llamar a `services`, pero los servicios **nunca** deben llamar a las interfaces.
3.  **Aislamiento de la Base de Datos:** Está estrictamente prohibido importar librerías de MongoDB en `console`, `server` o `engine`. Cualquier acceso a datos debe pasar por `repository`.
4.  **Orquestación centralizada:** La instanciación pesada (arrancar la IA y la BD) se hace una sola vez en `main.py` y se inyecta en las capas inferiores para evitar colapsos de memoria[cite: 21].
5. **Uso de Interfaces (Abstracción Obligatoria):** Las capas de `services` y `repository` deben definir y utilizar interfaces (clases abstractas mediante `abc.ABC` en Python). Las capas superiores deben depender de estas abstracciones (los "contratos") y nunca de las implementaciones concretas, garantizando un acoplamiento débil.
6.  **Estructuración Estricta de Modelos de Datos (`src/models/`):** Cualquier objeto, esquema, entidad de datos (ej. clases Pydantic, estructuras para JSON) o modelo de dominio **DEBE** crearse exclusivamente dentro de la carpeta `src/models/`. Además, estos modelos deben subdividirse lógicamente (en archivos o subcarpetas) según su propósito, por ejemplo, separando explícitamente los modelos de entrada/salida (DTOs, Request/Response) de los modelos de referencia de base de datos (Entidades/Schemas de MongoDB).