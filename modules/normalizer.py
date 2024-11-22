import unicodedata
import re
import pandas as pd


def normalizar_nombre(nombre):
    """
    Normaliza el nombre eliminando acentos, comas y caracteres especiales,
    y estandarizando espacios.
    """
    if pd.isnull(nombre):
        return nombre
    # Eliminar acentos
    nombre = ''.join(
        c for c in unicodedata.normalize('NFD', nombre)
        if unicodedata.category(c) != 'Mn'
    )
    # Eliminar comas
    nombre = nombre.replace(',', '')
    # Eliminar caracteres especiales (excepto espacios)
    nombre = re.sub(r'[^\w\s]', '', nombre)
    # Reemplazar múltiples espacios por uno solo
    nombre = re.sub(r'\s+', ' ', nombre)
    # Eliminar espacios al inicio y al final
    nombre = nombre.strip()
    return nombre