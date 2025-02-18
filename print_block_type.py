from src.services.print_block_type_services import contar_ocurrencias, generar_grafico


archivos_uy_dns_http = ["src/data/comparative/200.58.141.25.csv", "src/data/comparative/200.40.53.104.csv"]
conteo_dns = contar_ocurrencias(archivos_uy_dns_http, 'dns_experiment_failure')
conteo_http = contar_ocurrencias(archivos_uy_dns_http, 'http_experiment_failure')

generar_grafico(conteo_dns, 'Fallas DNS por Archivo', 'Archivo', 'Número de Ocurrencias')
generar_grafico(conteo_http, 'Fallas HTTP por Archivo', 'Archivo', 'Número de Ocurrencias')

archivos_uy_status = ["src/data/digs/toCSV/resultados_UY_ANTEL.csv", "src/data/digs/toCSV/resultados_UY_MOVISTAR.csv"]
conteo_status = contar_ocurrencias(archivos_uy_status, 'status', limpiar=True)

generar_grafico(conteo_status, 'Cantidad de Errores por Archivo', 'Archivo', 'Número de Errores')
