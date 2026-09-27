import logging
import os
from dotenv import load_dotenv

load_dotenv()

def get_logger(module_name):
    """
    Devuelve un logger configurado según el APP_MODE.
    Si es 'server', incluye fechas y niveles de severidad.
    Si es 'console', actúa como un print normal.
    """
    
    logger = logging.getLogger(module_name)
    
    if not logger.hasHandlers():
        mode = os.getenv("APP_MODE", "console")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        
        if mode == "server":
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        elif mode == 'console':
            formatter = logging.Formatter('%(message)s')
        else:
            formatter = logging.Formatter('%(message)s')
            print(f"Error: Modo '{mode}' no reconocido en APP_MODE. Usando 'console' por defecto")
            
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger