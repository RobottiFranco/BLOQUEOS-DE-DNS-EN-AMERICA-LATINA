from src.GetGlobalList.GetGlobalList import GetGlobalList
from src.helpers.calculateDate import obtener_rango_mes
from src.data import Query
from src.helpers.CSV import crear_ooni_run_link

countries: list = ["UY", "VE", "HN", "AR", "CU", "SV", "NI", "GT"]
query_db = "https://api.ooni.org/api/v1/measurements"


def extraer_datos_por_mes(since: int, until: int) -> None:
    for country in countries:
        while since <= until:
            for month in range(1, 13):
                inicio, final = obtener_rango_mes(since, month)
                consulta = Query(query_db, "web_connectivity", country, inicio, final, None, None, None, None, None)
                GetGlobalList(consulta, 2000, "true", "data/raw", "lista_global_bruta", "a")
            since += 1
    crear_ooni_run_link("data/raw", "lista_global_bruta", "data/processed", "lista_global_procesada", "a")

# Main

extraer_datos_por_mes(since=2023, until=2025)