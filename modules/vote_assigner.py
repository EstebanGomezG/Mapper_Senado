import pandas as pd
from modules.logger import logger
from modules.mapper import obtener_mejor_coincidencia
from modules.normalizer import normalizar_nombre

def asignar_votos(df_votacion, df_senadores, id_map, lista_nombres_normalizados, nombre_columna):
    """
    Asigna votos al DataFrame principal de senadores.

    Parámetros:
    df_votacion (DataFrame): DataFrame de votaciones.
    df_senadores (DataFrame): DataFrame principal de senadores.
    id_map (dict): Diccionario de mapeo de nombres normalizados a IDs.
    lista_nombres_normalizados (list): Lista de nombres normalizados para coincidencia difusa.
    nombre_columna (str): Nombre de la columna de votación a añadir.

    Retorna:
    DataFrame: DataFrame de senadores actualizado con la nueva columna de votos.
    """
    if not nombre_columna:
        raise ValueError("El argumento 'nombre_columna' no puede estar vacío.")
    # Normalizar los nombres en df_votacion
    df_votacion['Nombre_Senador_Normalizado'] = df_votacion['Nombre_Senador'].apply(normalizar_nombre)

    # Asignar IDs a los senadores
    df_votacion['ID_Senador'] = df_votacion['Nombre_Senador_Normalizado'].map(id_map)
    
    # Identificar nombres faltantes
    nombres_faltantes = df_votacion[df_votacion['ID_Senador'].isnull()]['Nombre_Senador_Normalizado'].unique()
    if len(nombres_faltantes) > 0:
        logger.info(f"Nombres que no se encontraron en el Excel de senadores en el archivo: {nombres_faltantes}")
        for nombre in nombres_faltantes:
            mejor_coincidencia = obtener_mejor_coincidencia(nombre, lista_nombres_normalizados)
            if mejor_coincidencia:
                id_correspondiente = id_map.get(mejor_coincidencia)
                logger.info(f"Se asignó la coincidencia '{mejor_coincidencia}' al nombre '{nombre}'.")
                # Actualizar el ID_Senador en el DataFrame
                df_votacion.loc[df_votacion['Nombre_Senador_Normalizado'] == nombre, 'ID_Senador'] = id_correspondiente
            else:
                logger.warning(f"No se encontró una coincidencia adecuada para '{nombre}'.")
    
    # Eliminar registros con IDs faltantes después de intentar coincidencia difusa
    cantidad_before = len(df_votacion)
    df_votacion = df_votacion.dropna(subset=['ID_Senador'])
    cantidad_after = len(df_votacion)
    logger.info(f"Registros eliminados por IDs faltantes: {cantidad_before - cantidad_after}")
    
    # Crear una Serie que mapea 'ID_Senador' a 'Voto_Estandarizado'
    votos_series = pd.Series(data=df_votacion['Voto'].values, index=df_votacion['ID_Senador'].values)
    
    # Verificar duplicados en la Serie de votos
    duplicados_votos = votos_series.index.duplicated().sum()
    if duplicados_votos > 0:
        logger.warning(f"Número de IDs duplicados en la Serie de votos: {duplicados_votos}")
        # Seleccionar el primer voto en caso de duplicados
        votos_series = votos_series[~votos_series.index.duplicated()]
        logger.info("Duplicados eliminados, manteniendo el primer voto.")
    
    # Asignar los votos al DataFrame principal
    df_principal = df_senadores.copy()
    df_principal[nombre_columna] = df_principal['ID'].map(votos_series)
    
    logger.info(f"Integrado {nombre_columna} al Excel principal.")
    
    return df_principal
    