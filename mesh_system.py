from src.services.process_files import process_files


def mesh(directory: str) -> None:
    output_file = process_files(directory)
    print(f"Archivo generado con archivos inexistentes: {output_file}")

mesh("src/data/comparative")