# modules/logger.py

import logging
import os
from config.config import LOG_DIR, LOG_FILE

# Crear la carpeta de logs si no existe
os.makedirs(LOG_DIR, exist_ok=True)

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
