from src.logic.query_builder import QueryBuilder
from src.services.get_global_list import get_global_list
from src.utils.csv_utils import create_ooni_run_link
from src.utils.date_utils import get_month_range

countries: list = ["UY", "VE", "HN", "AR", "CU", "SV", "NI", "GT"]
query_db = "https://api.ooni.org/api/v1/measurements"

def extraer_datos_por_mes(since: int = 2023, until: int = 2025) -> None:
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

                get_global_list(query_builder, 2000, True, "src/data/raw", "lista_global_bruta", "a")
            since += 1
        since = 2023
        

extraer_datos_por_mes()
create_ooni_run_link("src/data/raw/lista_global_bruta.csv", "lista_global_procesada", "src/data/processed")
create_ooni_run_link("src/data/processed/lista_global_procesada.csv", "lista_global_procesada_v2", "src/data/processed")


