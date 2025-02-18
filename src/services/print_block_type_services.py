import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

def contar_ocurrencias(archivos_csv, columna, limpiar=False):
    conteo_fallas = defaultdict(lambda: defaultdict(int))

    for archivo in archivos_csv:
        df = pd.read_csv(archivo)

        if limpiar:
            df[columna] = df[columna].str.strip().str.replace(',', '')

        for fallo in df[columna].dropna().unique():
            conteo_fallas[archivo][fallo] += df[columna].str.contains(fallo).sum()

    return conteo_fallas

def generar_grafico(conteo_fallas, titulo, xlabel, ylabel):
    archivos = [os.path.basename(archivo) for archivo in conteo_fallas.keys()]
    tipos_fallas = sorted(set(falla for fallas in conteo_fallas.values() for falla in fallas.keys()))

    valores = [[conteo_fallas[archivo].get(falla, 0) for falla in tipos_fallas] for archivo in conteo_fallas]
    valores_df = pd.DataFrame(valores, columns=tipos_fallas)

    fig, ax = plt.subplots(figsize=(12, 6))
    
    bottom = [0] * len(archivos)
    for fallo in tipos_fallas:
        ax.bar(archivos, valores_df[fallo], bottom=bottom, label=f"{fallo}")
        bottom = [b + v for b, v in zip(bottom, valores_df[fallo])]

    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(title="Tipos de Fallos", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
