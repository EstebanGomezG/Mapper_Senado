# app.py

from modules.logger import logger
from modules.data_loader import cargar_excel_senadores, listar_archivos_csv, cargar_csv_votaciones
from modules.mapper import crear_mapeo_ids
from modules.normalizer import normalizar_nombre
from modules.vote_assigner import asignar_votos
from modules.backup import crear_respaldo
import pandas as pd
import os

def main():
    try:
        # Crear respaldo del Excel original
        ruta_respaldo = 'data/senadores_backup.xlsx'
        crear_respaldo(ruta_respaldo)
        
        # Cargar el Excel de senadores
        df_senadores = cargar_excel_senadores()
        
        # Crear el mapeo de nombres a IDs
        id_map_normalizado = crear_mapeo_ids(df_senadores)
        
        # Lista de nombres normalizados para Fuzzy Matching
        lista_nombres_normalizados = df_senadores['Nombre_Normalizado'].tolist()
        
        # Listar archivos CSV de votaciones
        archivos_csv = listar_archivos_csv()
        
        # Iterar sobre cada archivo CSV
        for archivo in archivos_csv:
            # Cargar el CSV de votaciones
            df_votacion = cargar_csv_votaciones(archivo)

            # Renombrar columnas si es necesario
            columnas = df_votacion.columns.tolist()
            if 'Senador' in columnas and 'Votación' in columnas:
                df_votacion.rename(columns={'Senador': 'Nombre_Senador', 'Votación': 'Voto'}, inplace=True)
            else:
                if len(columnas) < 2:
                    logger.error(f"El archivo {archivo} no tiene suficientes columnas.")
                    continue
                df_votacion.rename(columns={columnas[0]: 'Nombre_Senador', columnas[1]: 'Voto'}, inplace=True)
                logger.warning(f"Las columnas no se llamaban 'Senador' y 'Votación'. Se han renombrado las primeras dos columnas como 'Nombre_Senador' y 'Voto'.")
                                    
            # Aplicar funcion de  normalización a 'Nombre_Senador'
            df_votacion['Nombre_Senador_Normalizado'] = df_votacion['Nombre_Senador'].apply(normalizar_nombre)
                        
            # Asignar votos al Excel principal
            nombre_columna = os.path.splitext(archivo)[0]
            logger.info(f"Generando columna: {nombre_columna}")
            df_senadores = asignar_votos(
                df_votacion,
                df_senadores,
                id_map_normalizado,
                lista_nombres_normalizados,
                nombre_columna
                )
        
        # Guardar el Excel actualizado
        ruta_excel_actualizado = 'data/senadores_actualizado.xlsx'  # Puedes ajustar la ruta
        df_senadores.to_excel(ruta_excel_actualizado, index=False)
        logger.info(f"Excel actualizado guardado en {ruta_excel_actualizado}")
    
    except Exception as e:
        logger.error(f"Error en el proceso principal: {e}")

if __name__ == '__main__':
    main()
