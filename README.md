🌐 *Read this in [Spanish](README.es.md)*

# LocalAI - Local Inference Engine 🧠

LocalAI is a 100% locally executed artificial intelligence application built on Clean Architecture principles. It separates the inference logic, the database, and the user interface, allowing the AI to be deployed both in the console (CLI) and on a server (API).

It features persistent memory thanks to its MongoDB integration and is optimized to take advantage of hardware acceleration (NVIDIA GPU) through `llama.cpp`.

---

## 📋 1. Prerequisites (Hardware and Software)

To run this project using your graphics card, you need to prepare your operating system environment:

1. **Python 3.10 or higher** installed on the system.
2. **Docker Desktop** (to run the MongoDB database).
3. **C++ Compiler**: Install the *Visual Studio Build Tools* (or Visual Studio Community) and make sure to select the "Desktop development with C++" workload.
4. **NVIDIA CUDA Toolkit**: Download and install the NVIDIA CUDA toolkit (e.g. v13.4).
   * ⚠️ *Important:* You must install CUDA **after** Visual Studio so that the NVIDIA installer correctly injects the integration (`Nsight Visual Studio Edition`).

---

## 🚀 2. Installation and Configuration

### Step 1: Start the Database (MongoDB)

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

### Step 2: Create the Virtual Environment and Install Basic Dependencies

```bash
python -m venv venv

# Activate on Windows:
.\venv\Scripts\activate

# Activate on Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 3: Build `llama-cpp-python` with GPU (CUDA) Support

So that the AI does not run slowly on the processor (CPU), we need to build the engine with GPU support. With the virtual environment activated, run:

**On Windows (PowerShell):**

```powershell
$env:CMAKE_ARGS="-DGGML_CUDA=on"
pip install --force-reinstall --no-cache-dir llama-cpp-python
```

> **Note:** This process can take between 5 and 15 minutes while the C++ binaries are compiled.

### Step 4: Download the AI Model

1. Create a folder called `models` in the project root.
2. Download a model in `.gguf` format (for example, from HuggingFace). Make sure to choose a model that fits your graphics card's VRAM (e.g. 8B models quantized to Q4 usually take up about 5-6 GB of VRAM).
3. Place the `.gguf` file inside the `models/` folder.

### Step 5: Environment File (`.env`)

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

## 💻 3. Usage and Execution Guide

The main orchestrator (`main.py`) can be started either in a fully guided way through interactive menus, or in an unattended way using terminal arguments.

### Terminal Parameters

| Short Argument | Long Argument | Description | Accepted Values |
|:---:|:---:|---|---|
| `-a` | `--arranque` | Defines the application's execution environment. | `1` (Terminal/CLI)<br>`2` (Server/API) |
| `-m` | `--model` | Exact file name of the AI model to load. The file must exist inside the `models/` directory. | E.g.: `Meta-Llama-3-8B-Instruct-Q4_K_M.gguf` |

### Execution Examples

#### 1. Interactive Startup (Manual Mode)

If you don't provide any arguments, the system will display an interactive console menu to guide you through selecting the mode and the model.

```bash
python main.py
```

#### 2. Direct Terminal Startup (Development Mode)

Starts the engine in CLI (Terminal) mode instantly. Useful for chatting locally without going through the configuration menus.

```bash
python main.py -a 1 -m Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
```

#### 3. Direct Server Startup (Production Mode)

Starts the engine in Server/API mode, loading the specified model directly into VRAM and skipping any human interaction.

```bash
python main.py -a 2 -m Meta-Llama-3-8B-Instruct-Q4_K_M.gguf
```

### Error Handling

The system includes cascading validation. If a valid mode is passed but a model that does not exist on disk is entered, the program will avoid a forced shutdown and automatically display a safety menu showing the models that are actually available so you can choose a valid one.