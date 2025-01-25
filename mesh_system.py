from src.services.process_files import process_files, delete_no_exist_files


def mesh(directory: str) -> None:
    output_file = process_files(directory)
    print(f"Archivo generado con archivos inexistentes: {output_file}")

def delete_url(directory, output_file) -> None:
    output_file = delete_no_exist_files(directory, output_file)

""" mesh("src/data/comparative") """
delete_url("src/data/comparative","src/data/comparative/pages_no_longer_exist.csv")