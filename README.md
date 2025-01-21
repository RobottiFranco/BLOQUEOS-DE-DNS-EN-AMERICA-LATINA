## Flujo de Obtención Primaria de Datos

La clase principal de este flujo es `fetch_db_data.py`, específicamente la función `extraer_datos_historicos`. Esta función permite iterar a través de un rango de años y meses, para cada país de interés, y realiza llamadas al servicio `get_global_list` con una consulta específica. Los parámetros incluyen el límite superior de filas por solicitud, el directorio de almacenamiento, el nombre del archivo de salida, el modo de escritura y una bandera para aplicar filtros y eliminar duplicados.

### Codigo

```python
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

                get_global_list(
                    query=query_builder,
                    limit=2000,
                    anomaly=True,
                    output_directory="src/data/raw",
                    file_name="lista_global_bruta",
                    mode="a",
                    update=True
                )
            since += 1
        since = 2023
```

### Descripción del Servicio

El servicio `get_global_list` realiza los siguientes pasos:
1. **Preparación de la consulta**: Construye una consulta personalizada utilizando `QueryBuilder`, incluyendo parámetros como el país, rango de fechas, y tipo de prueba (`web_connectivity`).
2. **Obtención de datos**: Realiza la llamada a la API de OONI utilizando la consulta generada.
3. **Filtrado de datos**: Según el valor de `update`, aplica un filtro para eliminar duplicados (`filter_and_remove_duplicates`) o filtrar datos relacionados con DNS (`filter_dns`).
4. **Escritura en CSV**: Guarda los datos filtrados en un archivo CSV en la ruta especificada.


#### Función de Filtrado de Datos

```python
def filter_data(data, update: bool):
    if update:
        filtered_data = filter_and_remove_duplicates(data)
    else:
        filtered_data = filter_dns(data)
    return filtered_data
```

#### Función Principal: `get_global_list`

```python
def get_global_list(query: Query, limit: int, anomaly: bool, output_directory: str, file_name: str, mode: str, update: bool) -> None:
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
```



## Flujo de Obtención Secundaria de Datos

El archivo principal utilizado es el mismo que en el flujo anterior, `fetch_db_data.py`. Sin embargo, en este caso, el flujo se centra en configurar los días específicos en los que se procesan las listas y el ID de la lista, además de modificar el número máximo de filas, el nombre del archivo de salida, y la bandera para la eliminación de duplicados y el filtrado.

### Codigo

```python
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
```

### Detalles del Flujo

1. **Eliminación del archivo existente**: Antes de comenzar, verifica si el archivo `lista_global_actualizada.csv` ya existe en la carpeta `src/data/raw` y, de ser así, lo elimina.
2. **Configuración de fechas**: Define un rango de días, desde el 1 hasta el 16 de enero de 2025, para generar consultas específicas.
3. **Construcción de consultas**: Utiliza `QueryBuilder` para configurar parámetros personalizados, como las fechas (`since` y `until`), el nombre de la prueba (`web_connectivity`), y el ID de la lista (`set_ooni_run_link_id`).
4. **Obtención de datos**: Llama a la función `get_global_list`, ajustando los parámetros de número máximo de filas, nombre del archivo de salida y configuraciones de filtrado.



## Flujo de Procesamiento de Datos

El archivo principal de este flujo es `fetch_db_data.py`. Esta clase contiene una función que, basado en el archivo de entrada, el nombre del archivo de salida y el directorio de salida, crea una query de tipo raw. Para cada fila en el archivo de entrada, se carga el ID de la medición y, por cada medición, se llama al servicio `get_lock_type`.

### Codigo
```python
def lock_type(archivo_entrada: str, output_directory: str):
    measurement_uids = []
    query = QueryBuilder() \
        .set_base_url("https://api.ooni.org/api/v1/raw_measurement") \
        .build()
        
    with open(archivo_entrada, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            measurement_uids.append(row.get('measurement_uid', None))

    for measurement_uid in measurement_uids:
        get_lock_type(query, measurement_uid, output_directory, mode='a')
        
lock_type("src/data/raw/lista_global_actualizada.csv", "src/data/comparative")
```

### Detalles del Flujo

1. **Carga de mediciones**: La función `lock_type` comienza abriendo el archivo de entrada (`lista_global_actualizada.csv`), extrayendo los identificadores de medición (`measurement_uid`) de cada fila.
2. **Construcción de la consulta**: Para cada `measurement_uid`, se construye una consulta usando `QueryBuilder`, con la base URL para obtener las mediciones.
3. **Llamada al servicio**: La función `get_lock_type` es llamada para cada `measurement_uid` para obtener los datos correspondientes.

El servicio realiza lo siguiente:

- **Preparación de la consulta**: Se configura la consulta para obtener la medición.
- **Obtención de los datos**: Se recuperan los datos de la medición.
- **Filtrado de datos**: Los datos obtenidos se filtran para extraer solo los valores de interés, tales como:
  - `measurement_uid`
  - `input`
  - `dns_experiment_failure`
  - `http_experiment_failure`
  - `dns_consistency`
  - `accessible`
  - `resolver_asn`
  - `resolver_ip`
  - `status_code`
  - `tcp_ip`
  - `tcp_status`
  
Los valores filtrados se guardan en un archivo CSV separado por `resolver_ip`.

### Codigo
```python
def get_lock_type(query: Query, measurement_uid: str, output_directory: str, mode: str) -> None:
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
```

### Descripción del Servicio `get_lock_type`

- **Preparación de la consulta**: Se construye una consulta de tipo `QueryRaw` usando `QueryRaw` y se ejecuta con el `measurement_uid`.
- **Obtención de los datos**: Se realiza la obtención de los datos con la función `fetch_data`.
- **Filtrado de información**: Los datos obtenidos se filtran para los valores de interés y se organizan en un diccionario `row` con claves como `measurement_uid`, `input`, `dns_experiment_failure`, entre otros.
- **Guardado de datos**: Por cada valor único de `resolver_ip`, se crea un archivo CSV con el nombre de `resolver_ip` y se guarda la información de la fila.



## Flujo de Eliminación de Páginas No Existentes

El archivo principal de este flujo es `mesh_system.py`. Esta clase contiene una función que, basado en el directorio de entrada (donde se guardan todos los archivos del flujo anterior), llama al servicio `process_files`.

### Codigo
```python
def mesh(directory: str) -> None:
    output_file = process_files(directory)
    print(f"Archivo generado con archivos inexistentes: {output_file}")

mesh("src/data/comparative")
```

### Descripción del Flujo

1. **Lectura de Archivos**: La función `mesh` recibe como parámetro el directorio de entrada (`src/data/comparative`), donde se encuentran todos los archivos generados en el flujo anterior. Luego llama a la función `process_files`, que se encarga de procesar todos los archivos CSV en ese directorio.
2. **Generación del Archivo de Salida**: El servicio `process_files` devuelve el archivo de salida, que es el archivo `pages_no_longer_exist.csv` con las páginas que ya no existen.

### Servicio `process_files`

Este servicio realiza lo siguiente:

- **Lectura de Archivos CSV**: Primero, se obtiene una lista de todos los archivos `.csv` dentro del directorio de entrada.
- **Carga de Archivos**: Luego, cada archivo se carga en un DataFrame de pandas.
- **Comparación de Archivos**: Para cada archivo, se compara con los demás archivos usando el servicio `compare_files`. En cada fila de cada archivo, se obtiene el valor de `input` y se compara con el valor `input` de las demás filas de otros archivos.
- **Identificación de Páginas No Existentes**: Si un valor de `input` se repite en todos los archivos, se considera que la página asociada a ese `input` ya no existe, y se coloca en el archivo de salida `pages_no_longer_exist.csv`.

### Codigo
```python
def process_files(directory):
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    dataframes = {file: pd.read_csv(file) for file in csv_files}

    all_common_inputs = pd.DataFrame(columns=["input"])

    for file in csv_files:
        reference_data = dataframes[file]
        common_inputs = compare_files(reference_data, dataframes, file)
        all_common_inputs = pd.concat([all_common_inputs, common_inputs]).drop_duplicates().reset_index(drop=True)

    output_file = create_file_and_path(directory, "pages_no_longer_exist.csv")
    all_common_inputs.to_csv(output_file, index=False)

    return output_file
```

### Detalles del Servicio `process_files`

- **Lectura de Archivos**: Se obtienen todos los archivos `.csv` en el directorio de entrada y se cargan en un diccionario de DataFrames (`dataframes`), donde las claves son los nombres de los archivos y los valores son los DataFrames correspondientes.
- **Comparación de Archivos**: Se compara cada archivo con los demás usando la función `compare_files`. Esto permite encontrar los valores de `input` comunes entre todos los archivos.
- **Generación del Archivo de Salida**: Después de realizar las comparaciones, se genera un archivo CSV (`pages_no_longer_exist.csv`) con las páginas (valores de `input`) que ya no existen en todos los archivos.