import csv
import os
import pandas as pd

def guardar_en_csv(archivo_salida: str, datos, modo: str):
    if datos:
        with open(archivo_salida, mode=modo, newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=datos[0].keys())
            writer.writeheader()
            writer.writerows(datos)
        print(f"Datos guardados en {archivo_salida}")
    else:
        print("No hay datos para guardar.")
        
        
def escribir_tipo_de_bloqueo_csv(archivo_salida: str, datos: list, modo: str):
    if datos:
        with open(archivo_salida, mode=modo, newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=datos[0].keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(datos)
        print(f"Datos guardados en {archivo_salida}")
    else:
        print("No hay datos para guardar.")


def _compenetrar_csv(archivo_entrada: str, archivo_salida: str) -> None:
    try:
        df = pd.read_csv(archivo_entrada)
        df = df[df['input'].str.lower() != 'input']
        df_sin_repetidos = df.drop_duplicates(subset='input', keep='first')
        df_sin_repetidos[['input']].to_csv(archivo_salida, index=False)
        
        print(f"Archivo {archivo_entrada} procesado y guardado como {archivo_salida}")
    
    except Exception as e:
        print(f"Error al procesar el archivo {archivo_entrada}: {e}")
        
        
def crear_archivo_y_ruta(base_dir: str, nombre_archivo: str) -> str:
    base_dir = os.path.normpath(base_dir)  
    os.makedirs(base_dir, exist_ok=True)
    ruta_completa = os.path.join(base_dir, nombre_archivo)
    print(f"Ruta creada o verificada: {ruta_completa}")
    return ruta_completa


def crear_ooni_run_link(archivo_entrada: str, nombre_archivo: str, directorio_salida: str) -> None:
    archivo_salida = crear_archivo_y_ruta(directorio_salida, f"{nombre_archivo}.csv")
    _compenetrar_csv(archivo_entrada, archivo_salida)