import os
from src.logic.query_builder import QueryBuilder
from src.services.get_global_list import get_global_list
from src.utils.csv_utils import create_ooni_run_link
from src.utils.date_utils import get_month_range

countries: list = ["UY", "VE", "HN", "AR", "CU", "SV", "NI", "GT"]
query_db = "https://api.ooni.org/api/v1/measurements"

def extraer_datos_historicos(since: int = 2023, until: int = 2025) -> None:
    for country in countries:
        while since <= until:
            for month in range(1, 13):
                if since == 2025 and month == 2:
                    break
                inicio, final = get_month_range(since, month)
                query_builder = QueryBuilder() \
                    .set_base_url(query_db) \
                    .set_test_name("web_connectivity") \
                    .set_probe_cc(country) \
                    .set_since(inicio) \
                    .set_until(final) \
                    .build()

                get_global_list(query_builder, 2000, True, "src/data/raw", "lista_global_bruta", "a", True)
            since += 1
        since = 2023
        
def extraer_datos_actualizados() -> None:
    if os.path.exists("src/data/raw/lista_global_actualizada.csv"):
        os.remove("src/data/raw/lista_global_actualizada.csv")
    since = 1
    until = 16
    while since <= until:
        query_builder = QueryBuilder() \
            .set_base_url(query_db) \
            .set_test_name("web_connectivity") \
            .set_since(f"2025-01-{since}") \
            .set_until(f"2025-01-{since + 1}") \
            .set_ooni_run_link_id("10118") \
            .build()
        get_global_list(query_builder, 4000, True, "src/data/raw", "lista_global_actualizada", "a", False)
        since += 1


#historico
extraer_datos_historicos()
create_ooni_run_link("src/data/raw/lista_global_bruta.csv", "lista_global_procesada", "src/data/processed")

#actualizado
extraer_datos_actualizados()

