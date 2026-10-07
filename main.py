import sys
import os
import argparse
from dotenv import load_dotenv
from src.config.logger import get_logger
from src.config.database import Database
from src.engine.engine import AIEngine

load_dotenv()


def main():
    
    args = configurar_argumentos_de_terminal()
    
    modo_arranque = menu_modo_arranque(args.arranque)
    if modo_arranque == 3:
        print("Saliendo de LocalAI...")
        sys.exit(0)
    
    modelo_inteligencia_artificial = menu_modelo_inteligencia_artificial(args.model)
    os.environ["MODEL_PATH"] = f"models/{modelo_inteligencia_artificial}"
    print(f"\nConfiguración lista. Modelo a cargar: {os.environ['MODEL_PATH']}")
    
    # Ya se ha establecido el modo de empleo
    log = get_logger(__name__)
    
    log.info("==== Iniciando LocalAI ====")
    log.info("Conectando a MongoDB...")
    db = Database()
    db.connect()
    db.init_db()
    log.info("Conectado a MongoDB")
            
    log.info(f"Arrancando el modelo {modelo_inteligencia_artificial}...")
    ai = AIEngine()
    log.info("Modelo arrancado adecuadamente")
    
    if modo_arranque == 1:
        from src.console.cli import iniciar_terminal
        log.info("Delegando control a la TUI de Textual...")
        iniciar_terminal(ai, db)
    elif modo_arranque == 2:
        from src.server.api import iniciar_servidor
        log.info("Arrancando servidor...")
        iniciar_servidor(ai, db)

"""
Metodos asistencia proyecto
"""
def menu_modo_arranque(arg_modo) -> int:
    """Devuelve el modo (1=CLI, 2=servidor). Si -a no es 1 ni 2, pregunta por consola."""
    if arg_modo in ("1", "2"):
        os.environ["APP_MODE"] = "console" if arg_modo == "1" else "server"
        return int(arg_modo)

    while True:
        print("\nSelecciona el modo de ejecución:")
        print("1. Modo Terminal (Chat CLI local)")
        print("2. Modo Servidor (API para conexión externa)")
        print("3. Salir")
        modo = input("\nElige una opción (1, 2, 3): ")
        
        if modo in ["1", "2", "3"]:
            match modo:
                    case "1" | "--cli":
                        os.environ["APP_MODE"] = "console"
                        return 1
                    case "2" | "--server":
                        os.environ["APP_MODE"] = "server"
                        return 2
                    case "3":
                        return 3 
        else:
            print(f"El numero {modo} no es ninguna de las 3 opciones")

       
    
def menu_modelo_inteligencia_artificial(arg_modelo) -> str:
    carpeta_modelos = "models"
    
    if not os.path.exists(carpeta_modelos):
        os.makedirs(carpeta_modelos)
        
    modelos_disponibles = [f for f in os.listdir(carpeta_modelos) if f.endswith('.gguf')]
    
    if not modelos_disponibles:
        print(f"Error: No se han encontrado archivos .gguf en la carpeta '{carpeta_modelos}/'.")
        print("Por favor, descarga un modelo y colócalo en la carpeta.")
        sys.exit(1)


    if arg_modelo and arg_modelo in modelos_disponibles:
        return arg_modelo
    elif arg_modelo:
        print(f"\nEl modelo '{arg_modelo}' no existe en la carpeta 'models/'.")

    while True:
        print("\nModelos de IA disponibles:")
        for i, mod in enumerate(modelos_disponibles):
            print(f"{i + 1}. {mod}")
            
        seleccion = input(f"\nElige el número del modelo a cargar (1-{len(modelos_disponibles)}): ")
        
        if seleccion.isdigit():
            indice = int(seleccion) - 1
            if 0 <= indice < len(modelos_disponibles):
                return modelos_disponibles[indice]
        
        print("[!] Selección no válida. Inténtalo de nuevo.")

def configurar_argumentos_de_terminal() -> str:
    parser = argparse.ArgumentParser(description="LocalAI - Motor de Inferencia")
    parser.add_argument("-a", "--arranque", help="Modo de ejecución (1: cli, 2: server)")
    parser.add_argument("-m", "--model", help="Nombre del archivo del modelo (ej: llama-3.gguf)")
    return parser.parse_args()

if __name__ == "__main__":
    main()