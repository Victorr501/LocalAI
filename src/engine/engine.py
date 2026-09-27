import os
from llama_cpp import Llama
from dotenv import load_dotenv
from src.config.logger import get_logger

load_dotenv()
log = get_logger(__name__)

class AIEngine:
    def __init__(self):
        self.model_path = os.getenv("MODEL_PATH")
        self.model = None
        self.load_model()
        
    def load_mode(self):
        """Carga el modelo .gguf físico directamente en la VRAM de la GPU"""
        try:
            log.info(f"Cargando modelo de IA desde: {self.model_path}...")
            
            self.model = Llama(
                model_path=self.model_path,
                n_gpu_layers=-1,
                n_ctx=4096,
                verbose=False
            )

            log.info("Modelo cargado con éxito en la VRAM de la GPU por acelaración CUDA")
        except Exception as e:
            log.error(f"Error crítico al cargar el modelo en la VRAM: {e}")
            
    def generate_response(self, prompt: str) -> str:
        """ Recibe un texto plaon, lo propcesa en la gráfica y devuelve la respuesta de la IA"""
        if not self.model:
            return "Error: El motor de IA no está inicialidao en memoria"
        
        try:
            formatted_prompt = f"<|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
            
            output = self.model(
                formatted_prompt,
                max_tokens=512,
                temperature=0.7,
                stop=["<|eot_id|>"],
                echo=False
            )
            
            return output['choices'][0]['text'].strip()
        except Exception as e:
            log.error(f"Error durante la inferencia en GPU: {e}")
            return "Error procesando la respuesta en el motor."