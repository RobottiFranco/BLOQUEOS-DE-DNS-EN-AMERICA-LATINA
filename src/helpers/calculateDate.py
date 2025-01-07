def obtener_rango_mes(año: int, mes: int) -> tuple:
    inicio = f"{año}-{mes:02d}-01"
    if mes == 2:
        final = f"{año}-{mes:02d}-28"
    elif mes in [4, 6, 9, 11]:
        final = f"{año}-{mes:02d}-30"
    else:
        final = f"{año}-{mes:02d}-31"
    return inicio, final