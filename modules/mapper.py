
from modules.normalizer import normalizar_nombre
from fuzzywuzzy import process
from modules.logger import logger

def crear_mapeo_ids(df_senadores):
    """
    Crea un diccionario que mapea nombres normalizados a IDs.

    Parámetros:
    df_senadores (DataFrame): DataFrame que contiene los datos de los senadores.

    Retorna:
    dict: Diccionario de mapeo.
    """
    df_senadores['Nombre_Normalizado'] = df_senadores['Nombre'].apply(normalizar_nombre)
    id_map_normalizado = dict(zip(df_senadores['Nombre_Normalizado'], df_senadores['ID']))
    logger.info("Diccionario de mapeo de nombres normalizados a IDs creado.")
    return id_map_normalizado

def obtener_mejor_coincidencia(nombre, lista_nombres, umbral=50):
    """
    Encuentra la mejor coincidencia para un nombre dado dentro de una lista de nombres.
    
    Parámetros:
    nombre (str): Nombre a buscar.
    lista_nombres (list): Lista de nombres donde buscar.
    umbral (int): Puntuación mínima para considerar una coincidencia válida.
    
    Retorna:
    str or None: Mejor coincidencia si la puntuación está por encima del umbral, de lo contrario None.
    """
    mejor_coincidencia, puntuacion = process.extractOne(nombre, lista_nombres)
    if mejor_coincidencia and puntuacion >= umbral:
        return mejor_coincidencia
    else:
        return None
