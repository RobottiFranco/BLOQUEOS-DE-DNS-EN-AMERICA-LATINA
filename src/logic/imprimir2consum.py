import os
import pandas as pd
import matplotlib.pyplot as plt

def grafico_errores_por_archivo(archivos_csv):
    conteo_errores_por_archivo = {}

    for archivo in archivos_csv:
        df = pd.read_csv(archivo)

        df['status'] = df['status'].str.strip().str.replace(',', '')

        conteo_errores = df['status'].value_counts()

        nombre_archivo = os.path.basename(archivo)
        conteo_errores_por_archivo[nombre_archivo] = conteo_errores

    df_errores = pd.DataFrame(conteo_errores_por_archivo).fillna(0)

    df_errores.T.plot(kind='bar', stacked=True, figsize=(12, 6), colormap="tab10")

    plt.title('Cantidad de Errores por Archivo')
    plt.xlabel('Archivo')
    plt.ylabel('Número de Errores')
    plt.xticks(rotation=45, ha='right')  
    plt.legend(title="Errores", bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()