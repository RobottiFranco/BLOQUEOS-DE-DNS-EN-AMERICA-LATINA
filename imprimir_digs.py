from src.logic.imprimir2consum import grafico_errores_por_archivo


archivos_uy = ["src/data/digs/toCSV/resultados_UY_ANTEL.csv",
               "src/data/digs/toCSV/resultados_UY_MOVISTAR.csv"]

grafico_errores_por_archivo(archivos_uy)
