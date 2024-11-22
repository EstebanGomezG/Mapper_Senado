# modules/data_loader.py

import pandas as pd
import os
from config.config import SENADORES_EXCEL, VOTACIONES_DIR
from modules.logger import logger

def cargar_excel_senadores():
    try:
        df = pd.read_excel(SENADORES_EXCEL)
        logger.info(f"Archivo Excel de senadores cargado correctamente desde {SENADORES_EXCEL}.")
        return df
    except Exception as e:
        logger.error(f"Error al cargar el Excel de senadores: {e}")
        raise

def listar_archivos_csv():
    try:
        archivos = [archivo for archivo in os.listdir(VOTACIONES_DIR) if archivo.endswith('.csv')]
        logger.info(f"Archivos CSV encontrados: {archivos}")
        return archivos
    except Exception as e:
        logger.error(f"Error al listar archivos. CSV no encontrados: {e}")
        raise

def cargar_csv_votaciones(nombre_archivo):
    ruta_completa = os.path.join(VOTACIONES_DIR, nombre_archivo)
    try:
        df = pd.read_csv(ruta_completa, skiprows=1)
        logger.info(f"Archivo CSV '{nombre_archivo}' cargado correctamente.")
        return df
    except pd.errors.ParserError:
        # Intentar con otro separador o codificación
        try:
            df = pd.read_csv(ruta_completa, skiprows=1, sep=';', encoding='latin1')
            logger.warning(f"ParserError en '{nombre_archivo}'. Reintentando con separador ';' y encoding 'latin1'.")
            return df
        except Exception as e:
            logger.error(f"Error al cargar el CSV '{nombre_archivo}': {e}")
            raise
    except Exception as e:
        logger.error(f"Error al cargar el CSV '{nombre_archivo}': {e}")
        raise
