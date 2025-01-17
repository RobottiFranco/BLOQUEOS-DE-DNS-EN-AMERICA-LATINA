
from src.logic.query import Query
from src.logic.query_raw import QueryRaw
from src.utils.csv_utils import create_file_and_path, escribir_tipo_de_bloqueo_csv
from src.utils.fetch_data import fetch_data


def get_lock_type(query: Query, measurement_uid: str, output_directory: str, file_name: str, mode: str) -> None:
    try:
        query_raw = QueryRaw(query)
        query_raw = query_raw.QueryRaw(measurement_uid)
        data = fetch_data(query_raw)
        if not data:
            print(f"No se pudieron obtener datos")
            return
        
        test_keys = data.get("test_keys", {})
        control = test_keys.get("control", {})
        http_request = control.get("http_request", {})

        tcp_connect = test_keys.get("tcp_connect", [])
        tcp_connect_info = None
        if tcp_connect:
            tcp_connect_info = tcp_connect[0] 

        row = {
            "measurement_uid": measurement_uid or "None",
            "input": data.get("input", "None"),
            "dns_experiment_failure": test_keys.get("dns_experiment_failure", "None")  or "None",
            "http_experiment_failure": test_keys.get("http_experiment_failure", "None")  or "None",
            "dns_consistency": test_keys.get("dns_consistency", "None")  or "None",
            "accessible": test_keys.get("accessible", "None"),
            "resolver_asn": data.get("resolver_asn", "None"),
            "resolver_ip": data.get("resolver_ip", "None"),
            "status_code": http_request.get("status_code", "None"),
            "tcp_ip": tcp_connect_info.get("ip", "None") if tcp_connect_info else "None",
            "tcp_status": tcp_connect_info.get("status", "None") if tcp_connect_info else "None"
        }
        
        for key, value in row.items():
            """  quiero que por cada valor diferente en la linea de resolver_ip escriba en un archivo diferente"""
            if key == "resolver_ip":
                path = create_file_and_path(output_directory, f"{value}.csv")
                escribir_tipo_de_bloqueo_csv(path, [row], mode)
        
    except Exception as e:
        print(f"Error al obtener datos: {e}")