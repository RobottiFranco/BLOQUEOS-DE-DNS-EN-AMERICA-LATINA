from src.data import Query, QueryDB, GetData
from src.helpers.Filter import filtrar_y_eliminar_duplicados
from src.helpers.CSV import guardar_en_csv, crear_archivo_y_ruta

def GetGlobalList(query: Query, limit: int, anomaly: bool, directorio_salida: str, nombre_archivo: str, modo: str) -> None:
    print(f"Iniciando el proceso datos de {query.probe_cc}...")

    query_db = QueryDB(query, limit, anomaly)
    query_db = query_db.query_db()
    
    datos = GetData().execute(query_db)
    datos = datos.realizar_solicitud_obtencion()
    if datos is None:
        print(f"No se pudieron obtener datos de {query.probe_cc} desde {query.since} hasta {query.until}")
        return
    
    datos_filtrados = filtrar_y_eliminar_duplicados(datos)
    
    ruta = crear_archivo_y_ruta(directorio_salida, f"{nombre_archivo}.csv")
    guardar_en_csv(ruta, datos_filtrados, modo)