# 📊 Cosmos DB Query Assistant con Agentes y MCP

Este proyecto implementa un **asistente inteligente** que permite construir consultas SQL sobre **Azure Cosmos DB** a partir de lenguaje natural. Utiliza agentes con **Semantic Kernel**, integración con **Model Context Protocol (MCP)** en Node.js y una interfaz tipo chat para interactuar con el modelo.

---

## 🧰 Tecnologías utilizadas

- 🐍 **Python 3.13**
- 🧠 **Semantic Kernel 1.33**
- 🤖 **Azure OpenAI (GPT-4o)**
- 🌐 **FastAPI** para exponer endpoints
- 💬 **HTML + JS** para el frontend tipo chat
- 🟢 **Node.js** (para ejecutar un plugin MCP en JavaScript)
- 🗄️ **Azure Cosmos DB** como base de datos principal

---

## 🚀 Instrucciones de ejecución

1. **Clona este repositorio**:
    ```bash
    git clone https://github.com/juanpfhRM/mcp-azure-cosmos-db.git
    cd mcp-azure-cosmos-db
<br>

2. **Instala las dependencias de Python**:
    ```bash
    pip install -r requirements.txt
<br>

3. **Instala Node.js y dependencias del plugin MCP y el generador de archivos .CSV**:<br>
    Asegúrate de tener Node.js instalado (node -v). Luego:
   ```bash
    cd src/plugins/mcp/js
    npm install
    cd ../../../..
    cd src/plugins/js
    npm install
<br>

4. **Configura variables de entorno**:<br>
    Crea un archivo .env con lo siguiente:
    ```env
    COSMOSDB_URI=
    COSMOSDB_KEY=
    COSMOS_DATABASE_ID=
    COSMOS_CONTAINER_ID=

    AZURE_OPENAI_API_KEY=
    AZURE_OPENAI_ENDPOINT=
    AZURE_OPENAI_DEPLOYMENT=
    AZURE_OPENAI_API_VERSION=
<br>

5. **Ejecuta la aplicación principal desde la raíz del proyecto:**:
    ```bash
    python index.py
<br>

Esto inicializará:
- Los agentes
- El servidor FastAPI (normalmente en http://127.0.0.1:8000)
- El plugin MCP vía Node.js
<br>

## 🧪 Endpoints principales
1. **GET /**:<br>
    Interfaz de chat HTML para enviar preguntas en lenguaje natural.
<br>

2. **POST /chat**:<br>
    Endpoint al que se envían los mensajes del usuario en el cuerpo del JSON:
    ```json
    {
        "mensaje": "¿Cuál es el último telegrama de NEWIDCODE?",
        "user_id": "123"
    }
<br>

## 🖼 Captura de pantalla

![Chat funcionando](/docs/img/chat-img.png)