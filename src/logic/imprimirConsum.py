import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

def graficoBloqueo(archivos: list):
    archivos_csv = []
    for i in archivos:
        archivos_csv.append(i)

    conteo_fallas_dns = defaultdict(lambda: defaultdict(int))
    conteo_fallas_http = defaultdict(lambda: defaultdict(int))

    for archivo in archivos_csv:
        df = pd.read_csv(archivo)
        
        for fallo in df['dns_experiment_failure'].dropna().unique():
            conteo_fallas_dns[archivo][fallo] += df['dns_experiment_failure'].str.contains(fallo).sum()
        
        for fallo in df['http_experiment_failure'].dropna().unique():
            conteo_fallas_http[archivo][fallo] += df['http_experiment_failure'].str.contains(fallo).sum()


    tipos_fallas_dns = sorted(set(falla for fallas in conteo_fallas_dns.values() for falla in fallas.keys()))
    tipos_fallas_http = sorted(set(falla for fallas in conteo_fallas_http.values() for falla in fallas.keys()))

    valores_dns = []
    valores_http = []

    for archivo in archivos_csv:
        valores_dns.append([conteo_fallas_dns[archivo].get(falla, 0) for falla in tipos_fallas_dns])
        valores_http.append([conteo_fallas_http[archivo].get(falla, 0) for falla in tipos_fallas_http])

    valores_dns = pd.DataFrame(valores_dns, columns=tipos_fallas_dns)
    valores_http = pd.DataFrame(valores_http, columns=tipos_fallas_http)

    fig, ax = plt.subplots(figsize=(12, 6))


    archivos = [os.path.basename(archivo) for archivo in archivos_csv] 

    bottom_dns = [0] * len(archivos)  
    for fallo in tipos_fallas_dns:
        ax.bar(archivos, valores_dns[fallo], bottom=bottom_dns, label=f"DNS - {fallo}")
        bottom_dns = [bottom + valores for bottom, valores in zip(bottom_dns, valores_dns[fallo])]

    bottom_http = [0] * len(archivos)
    for fallo in tipos_fallas_http:
        ax.bar(archivos, valores_http[fallo], bottom=bottom_http, label=f"HTTP - {fallo}")
        bottom_http = [bottom + valores for bottom, valores in zip(bottom_http, valores_http[fallo])]

    ax.set_title('Número de Ocurrencias de Fallas DNS y HTTP por Archivo')
    ax.set_xlabel('Archivo')
    ax.set_ylabel('Número de Ocurrencias')

    ax.legend(title="Tipos de Fallos", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right') 
    plt.tight_layout()

    plt.show()