# modules/backup.py

import shutil
from config.config import SENADORES_EXCEL
from modules.logger import logger

def crear_respaldo(ruta_respaldo):
    """
    Crea una copia de seguridad del archivo Excel principal.
    
    Parámetros:
    ruta_respaldo (str): Ruta donde se guardará el respaldo.
    
    Retorna:
    None
    """
    try:
        shutil.copyfile(SENADORES_EXCEL, ruta_respaldo)
        logger.info(f"Respaldo creado en {ruta_respaldo}")
    except Exception as e:
        logger.error(f"Error al crear el respaldo: {e}")
        raise
