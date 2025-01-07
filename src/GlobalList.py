from GetGlobalList.GetGlobalList import GetGlobalList
from helpers.calculateDate import obtener_rango_mes
from data.Query import Query
from helpers.CSV import crear_ooni_run_link

countries: list = ["UY", "VE", "HN", "AR", "CU", "SV", "NI", "GT"]
query_db = "https://api.ooni.org/api/v1/measurements"


def extraer_datos_por_mes(since: int = 2023, until: int = 2025) -> None:
    for country in countries:
        while since <= until:
            for month in range(1, 13):
                if since == 2025 and month == 2:
                    break
                inicio, final = obtener_rango_mes(since, month)
                consulta = Query(query_db, "web_connectivity", country, inicio, final, None, None, None, None, None)
                GetGlobalList(consulta, 2000, "true", "data/raw", "lista_global_bruta", "a")
            since += 1
        since = 2023
    crear_ooni_run_link("data/raw", "lista_global_bruta", "data/processed/lista_global_procesada")


extraer_datos_por_mes()