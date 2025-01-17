
import csv

from src.logic.query_builder import QueryBuilder
from src.logic.query import Query
from src.services.get_lock_type import get_lock_type


def tipo_de_bloqueo(archivo_entrada: str, nombre_salida: str, archivo_salida: str):
    measurement_uids = []
    query = QueryBuilder() \
        .set_base_url("https://api.ooni.org/api/v1/raw_measurement") \
        .build()
        
    with open(archivo_entrada, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            measurement_uids.append(row.get('measurement_uid', None))

    for measurement_uid in measurement_uids:
        get_lock_type(query, measurement_uid, archivo_salida, nombre_salida, mode='a')
        
tipo_de_bloqueo("src/data/raw/lista_global_actualizada.csv", "tipo_de_bloqueo", "src/data/processed")
