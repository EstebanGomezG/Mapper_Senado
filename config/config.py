# config/config.py

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, 'data')
SENADORES_EXCEL = os.path.join(DATA_DIR, 'senadores.xlsx')
VOTACIONES_DIR = os.path.join(DATA_DIR, 'votaciones')

LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'proceso_asignacion.log')
