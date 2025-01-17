from src.logic.fetch_api import FetchAPI
from src.logic.query import Query
from src.logic.query_db import QueryDB
from src.utils.csv_utils import create_file_and_path, save_to_csv
from src.utils.data_filter import filter_and_remove_duplicates, filter_dns


def filter_data(data, update: bool):
    if update == True:
        filtered_data = filter_and_remove_duplicates(data)
    else:
        filtered_data = filter_dns(data)
    return filtered_data


def get_global_list(query: Query, limit: int, anomaly: bool, output_directory: str, file_name: str, mode: str, update: bool= False) -> None:
    """Función principal para obtener y procesar datos de acuerdo a la consulta."""
    try:
        print(f"Iniciando el proceso de datos para {query.probe_cc}... desde {query.since} hasta {query.until}")
        query_db = QueryDB(query, limit, anomaly)
        query_db = query_db.query_db()
        data = fetch_data(query_db)
        if not data:
            print(f"No se pudieron obtener datos de {query.probe_cc} desde {query.since} hasta {query.until}")
            return
        
        filtered_data = filter_data(data, update)

        path = create_file_and_path(output_directory, f"{file_name}.csv")
        save_to_csv(path, filtered_data, mode)
    except Exception as e:
        print(f"Error al obtener datos: {e}")

def fetch_data(query_db: str):
    """Obtiene los datos de la URL usando la clase FetchAPI."""
    fetcher = FetchAPI()  
    data = fetcher.execute(query_db) 
    return data
