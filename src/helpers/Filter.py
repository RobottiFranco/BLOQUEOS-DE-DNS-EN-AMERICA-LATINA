def _filtrar_dns(self, datos: dict) -> list:
    result = []
    if "results" in datos:
        for item in datos["results"]:
            if item.get("scores", {}).get("analysis", {}).get("blocking_type") == "dns":
                result.append(item)
    return result


def _eliminar_duplicados(self, datos: list) -> list:
    seen_inputs = set()
    result = []

    for item in datos:
        input_value = item.get("input")
        if input_value not in seen_inputs:
            result.append(item)
            seen_inputs.add(input_value)

    return result


def filtrar_y_eliminar_duplicados(self, datos: dict) -> list:
    return self._eliminar_duplicados(self._filtrar_dns(datos))