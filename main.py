import os
from dotenv import load_dotenv
from src.config.logger import get_logger
from src.database.database import Database

load_dotenv()
log = get_logger(__name__)

def main():
    print("=== Iniciando LocalAI ===")
    db = Database()
    db.connect()
    db.init_db()
    
    log.info("Sistema base inicializado. Todo listo para cargar el modelo.")
    
if __name__ == "__main__":
    main()