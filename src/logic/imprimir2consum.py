import os
import pandas as pd
import matplotlib.pyplot as plt

def grafico_errores_por_archivo(archivos_csv):
    conteo_errores_por_archivo = {}

    for archivo in archivos_csv:
        df = pd.read_csv(archivo)

        # Limpiar la columna 'status' (eliminar comas y espacios)
        df['status'] = df['status'].str.strip().str.replace(',', '')

        # Contar las ocurrencias de cada error
        conteo_errores = df['status'].value_counts()

        # Guardar en el diccionario con el nombre del archivo sin la ruta
        nombre_archivo = os.path.basename(archivo)
        conteo_errores_por_archivo[nombre_archivo] = conteo_errores

    # Convertir el diccionario en un DataFrame
    df_errores = pd.DataFrame(conteo_errores_por_archivo).fillna(0)  # Rellenar NaN con 0

    # Graficar los errores por archivo en barras apiladas
    df_errores.T.plot(kind='bar', stacked=True, figsize=(12, 6), colormap="tab10")

    # Personalizar la gráfica
    plt.title('Cantidad de Errores por Archivo')
    plt.xlabel('Archivo')
    plt.ylabel('Número de Errores')
    plt.xticks(rotation=45, ha='right')  # Rotar nombres de archivos
    plt.legend(title="Errores", bbox_to_anchor=(1.05, 1), loc='upper left')

    # Mostrar la gráfica
    plt.tight_layout()
    plt.show()
    
# Lista de archivos CSV
archivos_uy = ["src/data/digs/toCSV/resultados_UY_ANTEL.csv",
               "src/data/digs/toCSV/resultados_UY_MOVISTAR.csv"]

grafico_errores_por_archivo(archivos_uy)
