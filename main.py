import os
from dotenv import load_dotenv
from src.config.logger import get_logger
from src.config.database import Database
from src.engine.engine import AIEngine

load_dotenv()
log = get_logger(__name__)

def main():
    log.info("==== Iniciando LocalAI ====")
    db = Database()
    db.connect()
    db.init_db()
    log.info("Sistema base inicializado. Todo listo para cargar el modelo.")
    
    ai = AIEngine()
    resultado = ai.generate_response(input("Introduce el promt: "))
    log.info(resultado)
    
    
if __name__ == "__main__":
    main()