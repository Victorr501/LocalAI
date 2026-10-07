# LocalAI - Local Inference Engine / Interfaz de un motor local
---
## English

LocalAI is a 100% locally executed artificial intelligence application built on Clean Architecture principles. It separates the inference logic, the database, and the user interface, allowing the AI to be deployed both in the console (CLI) and on a server (API).

It features persistent memory thanks to its MongoDB integration and is optimized to take advantage of hardware acceleration (NVIDIA GPU) through `llama.cpp`.

---

### 1. Prerequisites (Hardware and Software)

To run this project using your graphics card, you need to prepare your operating system environment:

1. **Python 3.12 or higher** installed on the system.
2. **Docker Desktop** (to run the MongoDB database).
3. **C++ Compiler**: Install the *Visual Studio Build Tools* (or Visual Studio Community) and make sure to select the "Desktop development with C++" workload.
4. **NVIDIA CUDA Toolkit**: Download and install the NVIDIA CUDA toolkit (e.g. v13.4).
   * ⚠️ *Important:* You must install CUDA **after** Visual Studio so that the NVIDIA installer correctly injects the integration (`Nsight Visual Studio Edition`).

---

### 2. Installation and Configuration

#### Step 1: Start the Database (MongoDB)

The project uses MongoDB to store conversation history and give the AI long-term memory. In the project root you will find the `docker-compose.yml` file:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: local_ai_mongo
    ports:
      - "27017:27017"
    volumes:
      # Change this path according to the drive and folder on your machine
      - D:\BasesDeDatos\LocalAI_Mongo:/data/db
    restart: unless-stopped
```

Open a terminal in the project root and run:

```bash
docker-compose up -d
```

#### Step 2: Create the Virtual Environment and Install Basic Dependencies

```bash
python -m venv venv

# Activate on Windows:
.\venv\Scripts\activate

# Activate on Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

#### Step 3: Build `llama-cpp-python` with GPU (CUDA) Support

So that the AI does not run slowly on the processor (CPU), we need to build the engine with GPU support. With the virtual environment activated, run:

**On Windows (PowerShell):**

```powershell
$env:CMAKE_ARGS="-DGGML_CUDA=on"
pip install --force-reinstall --no-cache-dir llama-cpp-python
```

> **Note:** This process can take between 5 and 15 minutes while the C++ binaries are compiled.

#### Step 4: Download the AI Model

1. Create a folder called `models` in the project root.
2. Download a model in `.gguf` format (for example, from HuggingFace). Make sure to choose a model that fits your graphics card's VRAM (e.g. 8B models quantized to Q4 usually take up about 5-6 GB of VRAM).
3. Place the `.gguf` file inside the `models/` folder.

#### Step 5: Environment File (`.env`)

Create a file called `.env` in the project root with the following configuration:

```env
# Connection to your local MongoDB database
MONGO_URI="mongodb://localhost:27017/"
MONGO_DB_NAME="local_ai_db"

# Default path for the AI model
MODEL_PATH="models/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"

# Default mode
APP_MODE="console"
```

---

### 3. Usage and Execution Guide

The main orchestrator (`main.py`) can be started either in a fully guided way through interactive menus, or in an unattended way using terminal arguments.

#### Terminal Parameters

| Short Argument | Long Argument | Description | Accepted Values |
|:---:|:---:|---|---|
| `-a` | `--arranque` | Defines the application's execution environment. | `1` (Terminal/CLI)<br>`2` (Server/API) |
| `-m` | `--model` | Exact file name of the AI model to load. The file must exist inside the `models/` directory. | E.g.: `Meta-Llama-3-8B-Instruct-Q4_K_M.gguf` |

#### Execution Examples

##### 1. Interactive Startup (Manual Mode)

If you don't provide any arguments, the system will display an interactive console menu to guide you through selecting the mode and the model.

```bash
python main.py
```

##### 2. Direct Terminal Startup (Development Mode)

Starts the engine in CLI (Terminal) mode instantly. Useful for chatting locally without going through the configuration menus.

```bash
python main.py -a 1 -m Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
```

##### 3. Direct Server Startup (Production Mode)

Starts the engine in Server/API mode, loading the specified model directly into VRAM and skipping any human interaction.

```bash
python main.py -a 2 -m Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
```

#### Error Handling

The system includes cascading validation. If a valid mode is passed but a model that does not exist on disk is entered, the program will avoid a forced shutdown and automatically display a safety menu showing the models that are actually available so you can choose a valid one.

---
## Español

LocalAI es una aplicación de inteligencia artificial de ejecución 100% local, construida bajo los principios de Arquitectura Limpia (Clean Architecture). Separa la lógica de inferencia, la base de datos y la interfaz de usuario, permitiendo desplegar la IA tanto en consola (CLI) como en un servidor (API).

Cuenta con memoria permanente gracias a la integración con MongoDB y está optimizada para aprovechar la aceleración por hardware (NVIDIA GPU) mediante `llama.cpp`.

---

### 1. Requisitos Previos (Hardware y Software)

Para ejecutar este proyecto aprovechando la tarjeta gráfica, necesitas preparar el entorno de tu sistema operativo:

1. **Python 3.12 o superior** instalado en el sistema.
2. **Docker Desktop** (para levantar la base de datos MongoDB).
3. **Compilador C++**: Instala las *Visual Studio Build Tools* (o Visual Studio Community) y asegúrate de marcar la carga de trabajo "Desarrollo para el escritorio con C++".
4. **NVIDIA CUDA Toolkit**: Descarga e instala el kit de herramientas CUDA de NVIDIA (ej. v13.4).
   * ⚠️ *Importante:* Debes instalar CUDA **después** de Visual Studio para que el instalador de NVIDIA inyecte correctamente la integración (`Nsight Visual Studio Edition`).

---

### 2. Instalación y Configuración

#### Paso 1: Levantar la Base de Datos (MongoDB)

El proyecto utiliza MongoDB para almacenar el historial de las conversaciones y dotar a la IA de memoria a largo plazo. En la raíz del proyecto encontrarás el archivo `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:latest
    container_name: local_ai_mongo
    ports:
      - "27017:27017"
    volumes:
      # Modifica esta ruta según la unidad y carpeta de tu equipo
      - D:\BasesDeDatos\LocalAI_Mongo:/data/db
    restart: unless-stopped
```

Abre una terminal en la raíz del proyecto y ejecuta:

```bash
docker-compose up -d
```

#### Paso 2: Crear el Entorno Virtual y Dependencias Básicas

```bash
python -m venv venv

# Activar en Windows:
.\venv\Scripts\activate

# Activar en Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

#### Paso 3: Compilar `llama-cpp-python` con soporte GPU (CUDA)

Para que la IA no se ejecute lentamente en el procesador (CPU), debemos compilar el motor gráfico a medida. Con el entorno virtual activado, ejecuta:

**En Windows (PowerShell):**

```powershell
$env:CMAKE_ARGS="-DGGML_CUDA=on"
pip install --force-reinstall --no-cache-dir llama-cpp-python
```

> **Nota:** Este proceso puede tardar entre 5 y 15 minutos mientras se compilan los binarios en C++.

#### Paso 4: Descarga del Modelo de IA

1. Crea una carpeta llamada `models` en la raíz del proyecto.
2. Descarga un modelo en formato `.gguf` (por ejemplo, desde HuggingFace). Asegúrate de elegir un modelo que se ajuste a la VRAM de tu tarjeta gráfica (ej. modelos de 8B cuantizados en Q4 suelen ocupar unos 5-6 GB de VRAM).
3. Coloca el archivo `.gguf` dentro de la carpeta `models/`.

#### Paso 5: Archivo de Entorno (`.env`)

Crea un archivo llamado `.env` en la raíz del proyecto con la siguiente configuración:

```env
# Conexión a tu base de datos local MongoDB
MONGO_URI="mongodb://localhost:27017/"
MONGO_DB_NAME="local_ai_db"

# Ruta por defecto para el modelo de IA
MODEL_PATH="models/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf"

# Modo por defecto
APP_MODE="console"
```

---

### 3. Guía de Uso y Ejecución

El orquestador principal (`main.py`) puede iniciarse de forma totalmente guiada mediante menús interactivos, o de forma desatendida mediante argumentos de terminal.

#### Parámetros de Terminal

| Argumento Corto | Argumento Largo | Descripción | Valores Aceptados |
|:---:|:---:|---|---|
| `-a` | `--arranque` | Define el entorno de ejecución de la aplicación. | `1` (Terminal/CLI)<br>`2` (Servidor/API) |
| `-m` | `--model` | Nombre exacto del archivo del modelo de IA a cargar. El archivo debe existir dentro del directorio `models/`. | Ej: `Meta-Llama-3-8B-Instruct-Q4_K_M.gguf` |

#### Ejemplos de Ejecución

##### 1. Arranque Interactivo (Modo Manual)

Si no proporcionas argumentos, el sistema desplegará un menú interactivo por consola para guiarte en la selección del modo y del modelo.

```bash
python main.py
```

##### 2. Despliegue Directo de Terminal (Modo Desarrollo)

Arranca el motor en modo CLI (Terminal) de forma instantánea. Útil para chatear en local sin pasar por los menús de configuración.

```bash
python main.py -a 1 -m Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
```

##### 3. Despliegue Directo de Servidor (Modo Producción)

Inicia el motor en modo Servidor/API cargando directamente el modelo indicado en la VRAM y omitiendo cualquier interacción humana.

```bash
python main.py -a 2 -m Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
```

#### Manejo de Errores

El sistema incorpora validación en cascada. Si se pasa un modo correcto pero se introduce un modelo que no existe en el disco duro, el programa evitará un cierre forzoso y desplegará automáticamente un menú de seguridad mostrando los modelos reales disponibles para que escojas uno válido.