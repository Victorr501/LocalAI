import os
from dotenv import load_dotenv

load_dotenv()

db_uri = os.getenv("MONGO_URI")
db_name = os.getenv("MONGO_DB_NAME")
model_path = os.getenv("MODEL_PATH")

def main():
    print("=== Iniciando LocalAI ===")
    print(f"[*] Base de datos configurada en: {db_uri} (Nombre: {db_name})")
    print(f"[*] Directorio de modelos establecido en: {model_path}")
    print("[*] Sistema base inicializado. Todo listo para el siguiente paso.")
    
if __name__ == "__main__":
    main()