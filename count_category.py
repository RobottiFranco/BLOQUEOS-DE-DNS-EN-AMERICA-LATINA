import pandas as pd
import os

def count_category(archivo, column):
    df = pd.read_csv(archivo)
    return df[column].value_counts()

directorio = "src/data/comparative"
for archivo in os.listdir(directorio):
    print(count_category(f"src/data/comparative/{archivo}", 'category'))