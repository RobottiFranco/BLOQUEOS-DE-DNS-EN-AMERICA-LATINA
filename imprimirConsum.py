import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Lista de archivos CSV que deseas analizar
def graficoBloqueo(archivos: list):
    archivos_csv = []
    for i in archivos:
        archivos_csv.append(i)

    # Diccionarios para almacenar el conteo de fallas DNS y HTTP por archivo
    conteo_fallas_dns = defaultdict(lambda: defaultdict(int))
    conteo_fallas_http = defaultdict(lambda: defaultdict(int))

    # Cargar los archivos CSV y contar las ocurrencias de las fallas
    for archivo in archivos_csv:
        df = pd.read_csv(archivo)
        
        # Contar las ocurrencias de fallas DNS
        for fallo in df['dns_experiment_failure'].dropna().unique():
            conteo_fallas_dns[archivo][fallo] += df['dns_experiment_failure'].str.contains(fallo).sum()
        
        # Contar las ocurrencias de fallas HTTP
        for fallo in df['http_experiment_failure'].dropna().unique():
            conteo_fallas_http[archivo][fallo] += df['http_experiment_failure'].str.contains(fallo).sum()

    # Preparar los datos para el gráfico
    # Convertir los conjuntos a listas ordenadas
    tipos_fallas_dns = sorted(set(falla for fallas in conteo_fallas_dns.values() for falla in fallas.keys()))
    tipos_fallas_http = sorted(set(falla for fallas in conteo_fallas_http.values() for falla in fallas.keys()))

    # Crear listas vacías para los valores de las barras
    valores_dns = []
    valores_http = []

    # Contar las ocurrencias de cada tipo de fallo por archivo
    for archivo in archivos_csv:
        valores_dns.append([conteo_fallas_dns[archivo].get(falla, 0) for falla in tipos_fallas_dns])
        valores_http.append([conteo_fallas_http[archivo].get(falla, 0) for falla in tipos_fallas_http])

    # Convertir los valores en arrays para apilarlos
    valores_dns = pd.DataFrame(valores_dns, columns=tipos_fallas_dns)
    valores_http = pd.DataFrame(valores_http, columns=tipos_fallas_http)

    # Graficar los resultados
    fig, ax = plt.subplots(figsize=(12, 6))

    # Apilar las barras de fallos DNS y HTTP
    # Primero apilamos las barras de DNS para cada archivo, luego apilamos las barras de HTTP sobre ellas
    archivos = [os.path.basename(archivo) for archivo in archivos_csv]  # Solo nombres de archivo sin ruta

    # Graficar las barras apiladas para cada tipo de fallo DNS
    bottom_dns = [0] * len(archivos)  # Empezamos con el valor base 0 para las barras de DNS
    for fallo in tipos_fallas_dns:
        ax.bar(archivos, valores_dns[fallo], bottom=bottom_dns, label=f"DNS - {fallo}")
        bottom_dns = [bottom + valores for bottom, valores in zip(bottom_dns, valores_dns[fallo])]

    # Graficar las barras apiladas para cada tipo de fallo HTTP
    bottom_http = [0] * len(archivos)  # Empezamos con el valor base 0 para las barras de HTTP
    for fallo in tipos_fallas_http:
        ax.bar(archivos, valores_http[fallo], bottom=bottom_http, label=f"HTTP - {fallo}")
        bottom_http = [bottom + valores for bottom, valores in zip(bottom_http, valores_http[fallo])]

    # Personalizar la gráfica
    ax.set_title('Número de Ocurrencias de Fallas DNS y HTTP por Archivo')
    ax.set_xlabel('Archivo')
    ax.set_ylabel('Número de Ocurrencias')

    # Añadir leyenda y ajustar la visualización
    ax.legend(title="Tipos de Fallos", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')  # Rotar las etiquetas del eje X para mayor legibilidad
    plt.tight_layout()

    # Mostrar la gráfica
    plt.show()