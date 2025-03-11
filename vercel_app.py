from main import app

# Para depuración
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uvicorn")
logger.info("Iniciando aplicación en Vercel")

# Este archivo sirve como punto de entrada para Vercel
# Vercel buscará un objeto 'app' que sea compatible con ASGI