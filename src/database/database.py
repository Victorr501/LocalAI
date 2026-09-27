import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from src.config.logger import get_logger

load_dotenv()
log = get_logger(__name__)

class Database:
    def __init__(self):
        self.uri = os.getenv("MONGO_URI")
        self.db_name = os.getenv("MONGO_DB_NAME")
        self.client = None
        self.db = None
        
    def connect(self):
        """Establece la conexión con el contenedor Docker de MongoDB."""
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            log.info(f"Conectado con éxito a MongoDB (Base de datos: {self.db_name})")
        except ConnectionFailure:
            log.error("Error crítico: No se pudo conectar a MongoDB. ¿Está Docker encendido?")
            
    def init_db(self):
        """Inserta un documento de prueba para forzar la creación de la BD y la colección."""
        if self.db is not None:
            collection = self.db["chat_history"]
            if collection.count_documents({}) == 0:
                collection.insert_one({
                    "role": "system",
                    "content": "Inicialización de la memoria del Agente LocalAI.",
                    "timestamp": "auto"
                })
                log.info("Base de datos y colección 'chat_history' inicializadas.")
            else:
                log.info("La base de datos ya contiene historial previo.")
        
